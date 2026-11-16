#!/usr/bin/env python3
"""Modded Cycles Techno Edition: builds the modded Model:Cycles firmware from YOUR official OS 1.13 file.

    python3 patch.py model-cycles_OS1.13.syx [-o modded-cycles-techno-edition.syx]
    python3 patch.py model-cycles_OS1.13.syx --dx-bank my-dx7-bank.syx

--dx-bank: a DX7 32-voice bank (.syx) whose voices replace the 32 sounds of the DX machine (machine 20, COLOR). The
build is first checked against the expected hash with the built-in sounds, then the bank goes in. The file is then
named modded-cycles-techno-edition-dx.syx unless you give -o.

Download model-cycles_OS1.13.syx from elektron.se (Model:Cycles > Support > Downloads). The script checks that it is
the official file, applies the mods below, checks the result against the expected hash and writes the new .syx next
to it. Needs Python 3.8 or later, nothing else.
"""
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
MODS = ['rel-macro-acid-t9-t8-606-909-smp-gran-wave-rumbl-vacf-metl2-xmod-dx-growl-atmos-empty-bias-midi', 'browser-scroll', 'boot-anim-te', 'multiline-browser', 'level-pan-values', 'mod-settings', 'cpu-monitor', 'track-filter-soft', 'filter-no-poli', 'usb-recover', 'lfo-polarity', 'sidechain', 'track-select', 'sidechain-project', 'machine-click', 'midi-dump']
EXPECT_MAIN_OS = "6e0635017d06ddbba92017020e443f2da99adb00cf51040d27d45cc444c285bf"


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 0 if args else 1
    src, out, bank = None, None, None
    i = 0
    while i < len(args):
        if args[i] in ("-o", "--dx-bank") and i + 1 < len(args):
            if args[i] == "-o":
                out = pathlib.Path(args[i + 1]).expanduser()
            else:
                bank = pathlib.Path(args[i + 1]).expanduser()
            i += 2
        elif src is None and not args[i].startswith("-"):
            src = pathlib.Path(args[i]).expanduser()
            i += 1
        else:
            print(f"Unexpected argument: {args[i]}\n{__doc__}")
            return 1
    if src is None:
        print(__doc__)
        return 1
    if out is None:
        out = src.with_name("modded-cycles-techno-edition-dx.syx" if bank else "modded-cycles-techno-edition.syx")
    for f in (src, bank):
        if f is not None and not f.is_file():
            print(f"File not found: {f}")
            return 1
    extra = ["--dx-bank", str(bank)] if bank else []
    r = subprocess.run([sys.executable, str(HERE / "tools" / "build.py"), "-i", str(src), "-t", ",".join(MODS),
                        "--expect-mainos", EXPECT_MAIN_OS, "-o", str(out), *extra])
    if r.returncode:
        print("\nThe build stopped (see above). Is this the official model-cycles_OS1.13.syx from elektron.se?"
              + (" Is the bank a DX7 32-voice .syx?" if bank else ""))
        return r.returncode
    print(f"\nDone: {out}\nSend it to the Model:Cycles with Elektron Transfer (see README.md, 'Flash it').")
    return 0


if __name__ == "__main__":
    sys.exit(main())
