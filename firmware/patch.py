#!/usr/bin/env python3
"""Modded Cycles Techno Edition: builds the modded firmware from YOUR official OS 1.13 file(s).

    python3 patch.py model-cycles_OS1.13.syx                                                  # Model:Cycles
    python3 patch.py --machine samples model-cycles_OS1.13.syx model-samples_OS1.13.syx       # Model:Samples
    python3 patch.py model-cycles_OS1.13.syx --dx-bank my-dx7-bank.syx                        # your DX sounds

--machine (default cycles):
  cycles           a Model:Cycles. Needs model-cycles_OS1.13.syx.
  samples          a Model:Samples. Also needs model-samples_OS1.13.syx.

--dx-bank: a DX7 32-voice bank (.syx) whose voices replace the 32 sounds of the DX machine (machine 20, COLOR). The
build is first checked against the expected hash with the built-in sounds, then the bank goes in. "-dx" is then added
to the output name unless you give -o.

Download the files from elektron.se (Support > Downloads of each machine). Give them in any order. The script checks
that they are the official files, applies the mods, checks the result against the expected hash and writes the new
.syx next to the first file. Needs Python 3.8 or later, nothing else.
"""
import argparse
import pathlib
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "tools"))
import for_samples  # noqa: E402

MODS = ['rel-macro-acid-t9-t8-ubsaw-606-909-smp-gran-wave-rumbl-vacf-metl2-xmod-dx-growl-atmos-empty-bias-midi', 'browser-scroll', 'boot-anim-te', 'multiline-browser', 'level-pan-values', 'mod-settings', 'cpu-monitor', 'track-filter-soft', 'filter-no-poli', 'usb-recover', 'lfo-polarity', 'sidechain', 'track-select', 'sidechain-project', 'machine-click', 'midi-dump']
EXPECT_MAIN_OS = "6cb41f0081da40fea337106669f4e3e96632ef68d82c6b764ed0ea27358324d2"
OUTPUT = {"cycles": "modded-cycles-techno-edition", "samples": "modded-cycles-techno-edition_model-samples"}


def build_cycles(src, out, bank):
    extra = ["--dx-bank", str(bank)] if bank else []
    r = subprocess.run([sys.executable, str(HERE / "tools" / "build.py"), "-i", str(src), "-t", ",".join(MODS),
                        "--expect-mainos", EXPECT_MAIN_OS, "-o", str(out), *extra])
    if r.returncode:
        print("\nThe build stopped (see above). Is this the official model-cycles_OS1.13.syx from elektron.se?"
              + (" Is the bank a DX7 32-voice .syx?" if bank else ""))
    return r.returncode


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+", help="model-cycles_OS1.13.syx (and model-samples_OS1.13.syx for a Model:Samples)")
    ap.add_argument("--machine", choices=tuple(OUTPUT), default="cycles", help="the machine you will flash")
    ap.add_argument("--dx-bank", help="a DX7 32-voice bank (.syx) for the DX machine")
    ap.add_argument("-o", "--output", help="output file")
    a = ap.parse_args()

    files = [pathlib.Path(f).expanduser() for f in a.files]
    bank = pathlib.Path(a.dx_bank).expanduser() if a.dx_bank else None
    for f in files + ([bank] if bank else []):
        if not f.is_file():
            print(f"File not found: {f}")
            return 1
    out = pathlib.Path(a.output).expanduser() if a.output else \
        files[0].with_name(OUTPUT[a.machine] + ("-dx" if bank else "") + ".syx")

    if a.machine == "cycles":
        if len(files) != 1:
            print("For a Model:Cycles, give only model-cycles_OS1.13.syx.")
            return 1
        rc = build_cycles(files[0], out, bank)
        if not rc:
            print(f"\nDone: {out}\nSend it to the Model:Cycles with Elektron Transfer (see README.md, 'Flash it').")
        return rc

    raws = {}
    for f in files:
        raw = f.read_bytes()
        kind = for_samples.identify(raw)
        if not kind:
            print(f"{f} is not the official model-cycles_OS1.13.syx or model-samples_OS1.13.syx from elektron.se.")
            return 1
        raws[kind] = (f, raw)
    if len(files) != 2 or set(raws) != {"cycles", "samples"}:
        print("For a Model:Samples, give both official files: model-cycles_OS1.13.syx and model-samples_OS1.13.syx.")
        return 1
    with tempfile.TemporaryDirectory() as tmp:
        cyc_out = pathlib.Path(tmp) / "cycles.syx"
        rc = build_cycles(raws["cycles"][0], cyc_out, bank)
        if rc:
            return rc
        try:
            data, main_sha = for_samples.for_samples(cyc_out.read_bytes(), raws["cycles"][1], raws["samples"][1])
        except for_samples.Error as e:
            print(f"\nPacking for the Model:Samples stopped: {e}")
            return 1
    out.write_bytes(data)
    print(f"\nPacked for a Model:Samples: Samples container and signature, MAIN OS {main_sha[:16]}..., "
          "read back and checked.")
    print(f"\nDone: {out}\nSend it to the Model:Samples through its startup menu over MIDI IN, or with Elektron "
          "Transfer while it still runs its own OS (see README.md, 'On a Model:Samples').")
    return 0


if __name__ == "__main__":
    sys.exit(main())
