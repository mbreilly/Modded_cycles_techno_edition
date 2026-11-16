#!/usr/bin/env python3
"""Checks that the web builder (docs/builder/builder.js, dx7Bank) converts DX7 banks exactly like the patcher
(firmware/tools/dx7bank.py), byte for byte. Needs node.

    python3 tools/check_dx7bank.py                                  # every frequency value, test banks
    python3 tools/check_dx7bank.py model-cycles_OS1.13.syx          # also: the full web build == patch.py, with a bank

Without a firmware file it compares, Python against JavaScript: the pitch of every possible operator frequency setting
(ratio and fixed, every coarse, fine, detune and transpose), the example bank docs/dx/modded-cycles-dx-bank.syx, and
200 banks of random bytes (every field out of range included). With the official OS file it also builds the firmware
with the web builder and with patch.py, without a bank and with the example bank, and compares the files.
"""
import json
import pathlib
import random
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "firmware" / "tools"))
import dx7bank  # noqa: E402

EXAMPLE = ROOT / "docs" / "dx" / "modded-cycles-dx-bank.syx"
BUILDER = ROOT / "docs" / "builder" / "builder.js"

JS = r"""
const fs = require("fs");
const B = require(process.argv[1]);
const job = JSON.parse(fs.readFileSync(0, "utf8"));
const out = { banks: job.banks.map((h) => {
  try {
    const r = B.dx7Bank(Uint8Array.from(Buffer.from(h, "hex")));
    return { bank: B.hex(r.bank), table: B.hex(r.table), shorts: r.shorts, names: r.names, warn: r.warn };
  } catch (e) { return { error: String(e.message) }; }
}) };
fs.writeFileSync(1, JSON.stringify(out));
"""


def node(script, *args, stdin=None):
    r = subprocess.run(["node", "-e", script, *args], input=stdin, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"!! node: {r.stderr}")
    return r.stdout


def bank_of(voices, cs_ok=True):
    data = b"".join(voices)
    return bytes([0xF0, 0x43, 0x00, 0x09, 0x20, 0x00]) + data + bytes([(-sum(data)) & 0x7F if cs_ok else 0, 0xF7])


def all_freq_banks():
    """Banks whose voices cover every (mode, coarse, fine, detune) of an operator, and every transpose."""
    ops = [(m, c, f, d) for m in (0, 1) for c in range(32) for f in range(100) for d in range(15)
           if m == 0 or (c < 4 and d == 7)]
    voices, banks = [], []
    for i in range(0, len(ops), 6):
        v = bytearray(128)
        for k, (m, c, f, d) in enumerate(ops[i:i + 6]):
            o = k * 17
            v[o + 12], v[o + 15], v[o + 16] = d << 3, (c << 1) | m, f
        v[117] = (i // 6) % 49
        v[118:128] = b"FREQ TEST "
        voices.append(bytes(v))
    voices += [bytes(128)] * (-len(voices) % 32)
    for i in range(0, len(voices), 32):
        banks.append(bank_of(voices[i:i + 32]))
    return banks


def py_result(raw):
    try:
        bank, table, names, shorts, warn = dx7bank.convert(raw)
        return {"bank": bank.hex(), "table": table.hex(), "shorts": shorts, "names": names, "warn": warn}
    except ValueError as e:
        return {"error": str(e)}


def main():
    rnd = random.Random(1)
    banks = all_freq_banks()
    banks.append(EXAMPLE.read_bytes())
    for n in range(200):
        voices = [bytes(rnd.randrange(128 if n % 2 else 256) for _ in range(128)) for _ in range(32)]
        banks.append(bank_of(voices, cs_ok=n % 3 != 0))
    banks.append(EXAMPLE.read_bytes()[6:6 + 4096])               # a bare 4096-byte file
    banks.append(bytes([0xF0, 0x43, 0x00, 0x00, 0x01, 0x1B]) + bytes(156) + b"\xf7")   # a single voice: refused
    banks.append(b"not a bank")
    js = json.loads(node(JS, str(BUILDER), stdin=json.dumps({"banks": [b.hex() for b in banks]})))["banks"]
    bad = 0
    for i, (b, j) in enumerate(zip(banks, js)):
        p = py_result(b)
        if ("error" in p) != ("error" in j) or ("error" not in p and p != j):
            bad += 1
            if bad < 5:
                print(f"!! bank {i}: python {str(p)[:200]} / js {str(j)[:200]}")
    nfreq = len(all_freq_banks())
    print(f"{len(banks)} banks ({nfreq} covering every operator frequency setting, the example, 200 random, 3 odd "
          f"files): {'all identical' if not bad else f'{bad} different'}")
    ex = py_result(EXAMPLE.read_bytes())
    if ex.get("shorts") != dx7bank.BUILTIN_NAMES or ex.get("warn"):
        bad += 1
        print("!! the example bank does not give the built-in names")
    if len(sys.argv) > 1:
        bad += check_build(pathlib.Path(sys.argv[1]))
    sys.exit(1 if bad else 0)


BUILD_JS = r"""
const fs = require("fs");
const B = require(process.argv[1]);
global.window = {};
eval(fs.readFileSync(process.argv[2], "utf8"));
const R = window.MCTE_RELEASE;
const raw = Uint8Array.from(fs.readFileSync(process.argv[3]));
const opts = { expectMainOsSha: R.expectMainOs };
if (process.argv[5]) opts.dxBank = Uint8Array.from(fs.readFileSync(process.argv[5]));
const out = B.build(raw, R.device, R.mods, opts);
fs.writeFileSync(process.argv[4], out.raw);
"""


def check_build(official):
    bad = 0
    with tempfile.TemporaryDirectory() as d:
        d = pathlib.Path(d)
        for bank in (None, EXAMPLE):
            py, js = d / "py.syx", d / "js.syx"
            cmd = [sys.executable, str(ROOT / "firmware" / "patch.py"), str(official), "-o", str(py)]
            if bank:
                cmd += ["--dx-bank", str(bank)]
            r = subprocess.run(cmd, capture_output=True, text=True)
            if r.returncode:
                print(r.stdout[-2000:], r.stderr[-2000:])
                return 1
            node(BUILD_JS, str(BUILDER), str(ROOT / "docs" / "builder" / "release-data.js"), str(official), str(js),
                 str(bank) if bank else "")
            same = py.read_bytes() == js.read_bytes()
            bad += not same
            print(f"full build {'with the example bank' if bank else 'without a bank'}: web builder "
                  f"{'== patch.py' if same else '!= patch.py'}")
    return bad


if __name__ == "__main__":
    main()
