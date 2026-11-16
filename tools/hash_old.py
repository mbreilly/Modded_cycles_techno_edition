#!/usr/bin/env python3
"""Replaces the stock bytes ("old") of every tweak write in firmware/tweaks/ by their length and SHA-256, so the
public release carries no bytes of Elektron's firmware. The patcher (firmware/tools/build.py) and the web builder
(docs/builder/builder.js) check the user's own file against the hash before writing, exactly as they checked the
bytes before. Writes into erased flash (every old byte 0xFF, or every byte 0x00) keep their "old": those bytes are
padding, not content, and build.py needs them to find the free zones.

    python3 tools/hash_old.py            # convert firmware/tweaks/ in place (run after tools/export_release.py)
    python3 tools/hash_old.py --check    # fail if any tweak still carries stock bytes
"""
import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TW = ROOT / "firmware" / "tweaks" / "model-cycles_OS1.13"


def blank(b):
    return len(b) > 0 and (b.count(0xFF) == len(b) or b.count(0) == len(b))


def convert(t):
    n = 0
    for w in t.get("writes", []):
        if "old" not in w:
            continue
        old = bytes.fromhex(w["old"])
        if blank(old):
            continue
        out = {}
        for k, v in w.items():
            if k == "old":
                out["old_len"] = len(old)
                out["old_sha256"] = hashlib.sha256(old).hexdigest()
            else:
                out[k] = v
        w.clear()
        w.update(out)
        n += 1
    return n


def main():
    check = "--check" in sys.argv[1:]
    bad = 0
    for p in sorted(TW.glob("*.json")):
        if p.name == "device.json":
            continue
        t = json.loads(p.read_text(encoding="utf-8"))
        n = convert(t)
        if not n:
            continue
        if check:
            print(f"!! {p.name}: {n} writes still carry stock bytes")
            bad += 1
        else:
            p.write_text(json.dumps(t, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
            print(f"{p.name}: {n} writes hashed")
    if check:
        if bad:
            sys.exit("!! run python3 tools/hash_old.py")
        print("no stock bytes in firmware/tweaks/")


if __name__ == "__main__":
    main()
