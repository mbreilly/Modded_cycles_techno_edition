#!/usr/bin/env python3
"""DX7 banks for the DX machine (Modded Cycles Techno Edition, MIT).

Reads a standard Yamaha DX7 32-voice bank (.syx, "VMEM" bulk dump: F0 43 0n 09 20 00, 4096 bytes, checksum, F7) and
turns each voice into a patch of the DX machine (tools/machines/dx/dx.c of Modded Cycles: struct dx_patch, 272 bytes,
big-endian), plus a 3-letter name for the COLOR knob. build.py then swaps the 32 built-in patches for these, inside
the machines' payload, before it is compressed into the firmware.

What the DX machine keeps from each voice: the algorithm, the feedback, and per operator its frequency (ratio, fine,
detune; a fixed-frequency operator is tuned as if the key were C4), output level, the four envelope rates and levels,
and key velocity sensitivity, plus the voice's transpose. What it does not have: keyboard level and rate scaling,
amplitude modulation sensitivity, the pitch envelope, the LFO and oscillator key sync (the DX machine always restarts
the operators on a note).

    python3 dx7bank.py bank.syx                       # list the 32 voices and the names the Cycles will show

The conversion is exactly the one of docs/builder/builder.js (dx7Bank), so the web builder and patch.py give the same
firmware; tools/check_dx7bank.py checks that on every possible value.
"""
import hashlib
import math
import re
import struct
import sys

VOICES, VOICE_LEN, BANK_LEN = 32, 128, 4096
HEADER = bytes([0xF0, 0x43])                 # Yamaha; then 0n (channel), 09 (format: 32 voices), 20 00 (4096 bytes)
PATCH_LEN = 4 * (2 + 6 * 11)                 # struct dx_patch: alg, fb, 6 x { pitch, att, rate[4], lev[4], vs }
NAME_LEN = 4                                 # the knob's names: char[32][4] (3 letters + NUL)

# The DX machine's built-in bank, to find it in the payload and check it before it is replaced (our own patches, MIT).
BUILTIN_BANK_SHA256 = "d8dac092c02ba76b41a959d2aee1192c66d48a709e3d98dd8d6d368e6904e1af"
BUILTIN_BANK_HEAD = "00000004000000020000000000000000"   # BEL: algorithm 5 (stored as 4), feedback 2, op 1 at ratio 1
BUILTIN_NAMES = ("BEL TUB GNG ANV CLG PIP SHD CHN BAS SUB RBS GRW SAW SQR BRS STB HRN ORG PAD DRN HIT KIK SNR HAT CYM "
                 "TOM ZAP SIR NOI SCR BLD VOX").split()

FS, BLOCK = 48000.0, 32
C4_HZ = 261.6255653005986


def _att(level):
    """level 0..99 -> attenuation, log2 << 16 (0.75 dB per step; 99 = 0)"""
    return int(round((99 - level) * 0.75 / 6.0206 * 65536))


def _speed(rate):
    """rate 0..99 -> envelope speed, log2 << 16 per block (96 dB in 30 s x 2^(-rate / 7.5))"""
    t = 30.0 * 2 ** (-rate / 7.5)
    return max(1, int(round(16 * 65536 / (t * FS / BLOCK))))


ATT = [_att(v) for v in range(100)]          # the same tables as the built-in bank (gen_dx_tables.py)
SPEED = [_speed(v) for v in range(100)]


def find_bank(raw):
    """The 4096 bytes of the 32 packed voices in a .syx file (or a bare 4096-byte file), and a warning or None."""
    raw = bytes(raw)
    if len(raw) == BANK_LEN:
        return raw, None
    for i in range(len(raw) - 5):
        if raw[i:i + 2] == HEADER and raw[i + 2] & 0xF0 == 0 and raw[i + 3] == 9:
            data = raw[i + 6:i + 6 + BANK_LEN]
            if len(data) < BANK_LEN:
                break
            if raw[i + 4:i + 6] != b"\x20\x00":
                raise ValueError("this DX7 bank header has an unexpected size")
            warn = None
            cs = raw[i + 6 + BANK_LEN] if len(raw) > i + 6 + BANK_LEN else None
            if cs is None or cs != (-sum(data)) & 0x7F:
                warn = "the bank's checksum does not match (common in banks found online); its voices are used anyway"
            return data, warn
    if len(raw) >= 6 and raw[:2] == HEADER and raw[3] == 0:
        raise ValueError("this is a single DX7 voice; the DX machine needs a 32-voice bank (.syx of about 4 KB)")
    raise ValueError("this is not a DX7 32-voice bank (.syx, 4104 bytes, starting F0 43 0n 09 20 00)")


def _alnum(name):
    return "".join(c for c in name.upper() if c.isascii() and c.isalnum())


def short_names(names):
    """3-letter names for the COLOR knob: the first three letters or digits of the voice name. Voices that would show
    the same name take the first two and the last one (BRASS 1, BRASS 2: BR1, BR2), then if still the same the first
    one and the last two (TEST 10, TEST 20: T10, T20). A name without letters or digits shows its number (01..32)."""
    full = [_alnum(n) for n in names]
    out = [s[:3] if s else f"{i + 1:02d}" for i, s in enumerate(full)]
    for alt in (lambda s: s[:2] + s[-1], lambda s: s[:1] + s[-2:]):
        dup = {x for x in out if out.count(x) > 1}
        out = [alt(s) if o in dup and len(s) > 3 else o for o, s in zip(out, full)]
    return out


def voice_name(v):
    return "".join(chr(b) if 32 <= b < 127 else " " for b in v[118:128]).rstrip()


def op_pitch(op, transpose):
    """1/65536 semitone above the note (or above C4 for a fixed-frequency operator)"""
    mode, coarse, fine, det = op[15] & 1, (op[15] >> 1) & 31, min(op[16], 99), min((op[12] >> 3) & 15, 14)
    if mode:                                 # fixed: 10^((coarse & 3) + fine / 100) Hz
        hz = 10 ** ((coarse & 3) + fine / 100)
        return int(round(12 * math.log2(hz / C4_HZ) * 65536))
    ratio = (0.5 if coarse == 0 else coarse) * (1 + fine / 100)
    return int(round((12 * math.log2(ratio) + (det - 7) / 100) * 65536)) + (transpose - 24) * 65536


def convert_voice(v):
    """128 packed bytes -> 272 bytes of struct dx_patch"""
    v = bytes(b & 0x7F for b in v)
    alg, fb, transpose = v[110] & 31, v[111] & 7, min(v[117], 48)
    words = [alg, fb]
    for k in range(6):                       # our op[0] = operator 1; the DX7 stores operator 6 first
        op = v[(5 - k) * 17:(6 - k) * 17]
        rates = [SPEED[min(op[j], 99)] for j in range(4)]
        levels = [ATT[min(op[4 + j], 99)] for j in range(4)]
        words += [op_pitch(op, transpose), ATT[min(op[14], 99)], *rates, *levels, (op[13] >> 2) & 7]
    return struct.pack(">68i", *words)


def convert(raw):
    """DX7 bank .syx -> (32 x 272 bytes of patches, 32 x 4 bytes of names, [voice names], [short names], warning)"""
    data, warn = find_bank(raw)
    voices = [data[i * VOICE_LEN:(i + 1) * VOICE_LEN] for i in range(VOICES)]
    names = [voice_name(v) for v in voices]
    shorts = short_names(names)
    bank = b"".join(convert_voice(v) for v in voices)
    table = b"".join(s.encode("ascii").ljust(NAME_LEN, b"\0") for s in shorts)
    return bank, table, names, shorts, warn


def builtin_names_bytes():
    return b"".join(n.encode("ascii").ljust(NAME_LEN, b"\0") for n in BUILTIN_NAMES)


def locate(runtime):
    """Offsets of the built-in bank and of its names in the machines' runtime payload; raises if they are not there
    exactly once, or not the expected bytes (the 'old' bytes check of every write)."""
    head = bytes.fromhex(BUILTIN_BANK_HEAD)
    hits = [m.start() for m in re.finditer(re.escape(head), runtime)
            if hashlib.sha256(runtime[m.start():m.start() + PATCH_LEN * VOICES]).hexdigest() == BUILTIN_BANK_SHA256]
    names = builtin_names_bytes()
    nhits = [m.start() for m in re.finditer(re.escape(names), runtime)]
    if len(hits) != 1 or len(nhits) != 1:
        raise SystemExit("!! the DX machine's built-in bank was not found exactly once in this firmware's payload")
    return hits[0], nhits[0]


def apply(runtime, raw):
    """Runtime payload with the bank of the DX7 file raw in place of the built-in one."""
    bank, table, *_ = convert(raw)
    at, nat = locate(runtime)
    out = bytearray(runtime)
    out[at:at + len(bank)] = bank
    out[nat:nat + len(table)] = table
    return bytes(out)


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        return 0 if a else 1
    with open(a[0], "rb") as f:
        bank, table, names, shorts, warn = convert(f.read())
    if warn:
        print("note:", warn)
    for i, (n, s) in enumerate(zip(names, shorts)):
        print(f"{i:2d}  {s:<3}  {n}")
    print(f"bank SHA-256 (as the DX machine stores it): {hashlib.sha256(bank + table).hexdigest()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
