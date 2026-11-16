#!/usr/bin/env python3
"""Packs a modded Model:Cycles firmware for a Model:Samples (called by patch.py --machine samples).

The firmware is always the Model:Cycles OS with the mods; only its packing changes. Its MAIN OS (section 3) goes into
the official Model:Samples OS 1.13 container: the Samples' bootstrap, updater and startup menu are kept, and it is
signed with the Samples' HMAC key, read from YOUR official Samples file (never stored here). It is wrapped in the
Samples' SysEx transport (product 0x0F, device byte 0x0A): the Samples' startup menu takes it whatever OS runs, and
Elektron Transfer takes it while the Samples still runs its own OS.

One 32-byte change is always made in the MAIN OS: the constant from which the Cycles OS derives the key it checks
updates with is recomputed to give the Samples' key, so the installed OS refuses firmwares built for a Model:Cycles
(nothing is written) and stays compatible with the Modded-Cycles Samples packing.

The output is read back from its bytes: packet checksums, product and device byte, content checksum, container header
and sections 2/4/5 equal to the official Samples, section 3 equal to the modded MAIN OS except the 32 key bytes, HMAC
valid with the Samples key and NOT with the Cycles key, and the key the installed OS will derive is the Samples key.

Original flasher by RDS (AIM), integrated into Modded Cycles by DaftMaple (tools/mods_for_samples.py,
tools/crossflash.py and notes/41 of https://github.com/18nelli18/Modded-Cycles).
"""
import hashlib
import hmac
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from mtlib import aplib, container                 # noqa: E402
from mtlib.syx import unwrap, wrap, BYTES_PER_MSG  # noqa: E402

# Official OS 1.13 files (elektron.se): SHA-256 of the .syx and of the unpacked MAIN OS
OFFICIAL = {
    "cycles": {"product": 0x11, "name": "Model:Cycles",
               "syx": "44fe586269631a0ca7da25a3383fc6733c314809505fc3cc52f1e0ed9800640c",
               "main": "cc99d4f0175d34d1e91d046e6ec85a5e8ab58ab9edbb3c24406acd48cb99ee98"},
    "samples": {"product": 0x0F, "name": "Model:Samples",
                "syx": "e11859b68deb7e5e3fe86ab32581212093849c4be5d3950add011eac398a2ce8",
                "main": "a351392c62ec1c6c3324a807baf46934690d54edfc76029a4b4882541cad1ab2"},
}

MAIN_BASE = 0x40000400
MAIN_END_LIMIT = 0x40200000      # the bootstrap unpacks section 3 below this address
CONTAINER_MAX = 0x1c0000         # written to flash at 0x20000, must end before 0x1e0000
PRODUCT, DEVICE = 0x0F, 0x0A    # the Samples' SysEx transport

# Model:Cycles OS 1.13 update check (0x40052750): key = sha256(s) ^ sha256(reversed s) ^ C, s = "REVERB SEND"
# (11 bytes at 0x40129650, also an on-screen name: left alone), C = 32 bytes at 0x401296b2, read only there.
CYC_KEY_STR_VA = 0x40129650
CYC_KEY_CONST_VA = 0x401296b2
CYC_KEY_CODE = ((0x4005275c, "487940129650"), (0x400527c0, "43f9401296b2"))   # pea "REVERB SEND" ; lea C


class Error(Exception):
    pass


def sha(b):
    return hashlib.sha256(b).hexdigest()


def identify(raw):
    """'cycles' or 'samples' if raw is the official OS 1.13 .syx, else None."""
    h = sha(raw)
    return next((k for k, v in OFFICIAL.items() if v["syx"] == h), None)


def load(raw, which):
    """Official .syx -> (info, container, {id: stored bytes}, {id: unpacked bytes})."""
    ref = OFFICIAL[which]
    if sha(raw) != ref["syx"]:
        raise Error(f"not the official {ref['name']} OS 1.13 .syx (SHA-256 {sha(raw)[:16]}...)")
    stream, info = unwrap(raw)
    if info["product"] != ref["product"]:
        raise Error(f"{ref['name']}: product 0x{info['product']:02x}, expected 0x{ref['product']:02x}")
    c = container.parse(stream)
    stored, plain = {}, {}
    for s in c["sections"]:
        stored[s["id"]] = c["blob"][s["off"]:s["off"] + s["size"]]
        try:
            plain[s["id"]] = aplib.depack(stored[s["id"]])[0]
        except Exception:
            plain[s["id"]] = stored[s["id"]]    # raw sections (meta, updater)
    if sha(plain[3]) != ref["main"]:
        raise Error(f"{ref['name']}: unexpected MAIN OS ({sha(plain[3])[:16]}...)")
    return info, c, stored, plain


def host_key(loaded):
    _, c, _, plain = loaded
    key = container.find_key(list(plain.values()), c["blob"][:-container.DIGEST_LEN], c["blob"][-container.DIGEST_LEN:])
    if not key:
        raise Error("HMAC key not found")
    return key


def key_write(main, cyc_key, new_key):
    """(offset, new 32 bytes) that make the Cycles OS check updates with new_key. Checks the code, the string and
    that the original constant gives the Cycles key."""
    for va, want in CYC_KEY_CODE:
        o = va - MAIN_BASE
        if main[o:o + 6].hex() != want:
            raise Error(f"unexpected update-check code at 0x{va:08x}")
    o = CYC_KEY_STR_VA - MAIN_BASE
    if main[o:o + 12] != b"REVERB SEND\0":
        raise Error("unexpected key string")
    text = main[o:o + 11]
    h, hr = hashlib.sha256(text).digest(), hashlib.sha256(text[::-1]).digest()
    co = CYC_KEY_CONST_VA - MAIN_BASE
    if bytes(a ^ b ^ c for a, b, c in zip(h, hr, main[co:co + 32])) != cyc_key:
        raise Error("the MAIN OS key differs from the bootstrap's")
    return co, bytes(a ^ b ^ c for a, b, c in zip(h, hr, new_key))


def load_mods(raw, cyc):
    """Modded Model:Cycles .syx -> (MAIN OS, aPLib ops). Only section 3 may differ from the official Cycles OS."""
    stream, info = unwrap(raw)
    if info["product"] != 0x11:
        raise Error(f"modded file: product 0x{info['product']:02x}, a Model:Cycles build (0x11) is expected")
    c = container.parse(stream)
    got = {s["id"]: c["blob"][s["off"]:s["off"] + s["size"]] for s in c["sections"]}
    if set(got) != set(cyc[2]) or any(got[i] != cyc[2][i] for i in got if i != 3):
        raise Error("modded file: sections other than 3 differ from the official Cycles OS")
    if hmac.new(host_key(cyc), c["blob"][:-container.DIGEST_LEN], hashlib.sha256).digest() != \
            c["blob"][-container.DIGEST_LEN:]:
        raise Error("modded file: HMAC invalid with the Cycles key")
    return aplib.depack(got[3])


def verify(out, smp, cyc_key, smp_key, main, mods_main, off):
    if out[4] != PRODUCT or out[6:8] != b"\x7f\x01" or out[8] != DEVICE:
        raise Error("read-back: start marker (product / device byte)")
    stream, _ = unwrap(out)                          # checksum of every packet
    c = container.parse(stream)
    blob = c["blob"]
    if int.from_bytes(stream[4:8], "big") != container.content_checksum(blob):
        raise Error("read-back: content checksum")
    if blob[:0x20] != smp[1]["blob"][:0x20]:
        raise Error("read-back: container header differs from the official Samples")
    got = {s["id"]: blob[s["off"]:s["off"] + s["size"]] for s in c["sections"]}
    if set(got) != set(smp[2]) or any(got[i] != smp[2][i] for i in got if i != 3):
        raise Error("read-back: sections 2/4/5 differ from the official Samples")
    m = aplib.depack(got[3])[0]
    if m != main:
        raise Error("read-back: section 3 does not unpack to the expected MAIN OS")
    if len(m) != len(mods_main) or any(a != b for i, (a, b) in enumerate(zip(m, mods_main)) if not off <= i < off + 32):
        raise Error("read-back: MAIN OS differs from the modded build outside the 32 key bytes")
    body, dig = blob[:-container.DIGEST_LEN], blob[-container.DIGEST_LEN:]
    if hmac.new(smp_key, body, hashlib.sha256).digest() != dig:
        raise Error("read-back: HMAC invalid with the Samples key")
    if hmac.new(cyc_key, body, hashlib.sha256).digest() == dig:
        raise Error("read-back: HMAC also valid with the Cycles key")
    o = CYC_KEY_STR_VA - MAIN_BASE
    text = m[o:o + 11]
    h, hr = hashlib.sha256(text).digest(), hashlib.sha256(text[::-1]).digest()
    if bytes(a ^ b ^ x for a, b, x in zip(h, hr, m[off:off + 32])) != smp_key:
        raise Error("read-back: the installed OS would not check updates with the Samples key")


def for_samples(mods_raw, cycles_raw, samples_raw):
    """Modded Cycles .syx -> .syx for a Model:Samples. Returns (bytes, MAIN OS sha)."""
    cyc, smp = load(cycles_raw, "cycles"), load(samples_raw, "samples")
    cyc_key, smp_key = host_key(cyc), host_key(smp)
    mods_main, ops = load_mods(mods_raw, cyc)
    off, new = key_write(mods_main, cyc_key, smp_key)
    main = bytearray(mods_main)
    main[off:off + 32] = new
    main = bytes(main)
    dirty = bytearray(len(main))
    dirty[off:off + 32] = b"\1" * 32
    s3 = aplib.repack(main, ops, dirty)
    if aplib.depack(s3)[0] != main:
        raise Error("MAIN OS repack: read-back differs")
    if MAIN_BASE + len(main) > MAIN_END_LIMIT:
        raise Error(f"MAIN OS too large: ends at 0x{MAIN_BASE + len(main):08x} (limit 0x{MAIN_END_LIMIT:08x})")
    blob = container.rebuild(smp[1], {3: s3}, smp_key)
    if len(blob) > CONTAINER_MAX:
        raise Error(f"container too large: {len(blob)} bytes (limit {CONTAINER_MAX})")
    out = wrap(container.build_stream(blob, BYTES_PER_MSG), PRODUCT, smp[0]["start_seq"])
    verify(out, smp, cyc_key, smp_key, main, mods_main, off)
    return out, sha(main)
