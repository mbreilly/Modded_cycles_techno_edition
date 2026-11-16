#!/usr/bin/env python3
"""Modded Cycles Techno Edition: builds the modded firmware from YOUR official OS 1.13 file(s).

    python3 patch.py model-cycles_OS1.13.syx                                                  # Model:Cycles
    python3 patch.py --machine samples model-cycles_OS1.13.syx model-samples_OS1.13.syx       # Model:Samples

--machine (default cycles):
  cycles           a Model:Cycles. Needs model-cycles_OS1.13.syx.
  samples          a Model:Samples. Also needs model-samples_OS1.13.syx.

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

MODS = ['rel-macro-acid-t9-t8-606-909-smp-gran-wave-rumbl-vacf-metl2-xmod-dx-growl-atmos-empty-bias-midi', 'browser-scroll', 'boot-anim-te', 'multiline-browser', 'level-pan-values', 'mod-settings', 'cpu-monitor', 'track-filter-soft', 'filter-no-poli', 'usb-recover', 'lfo-polarity', 'sidechain', 'track-select', 'sidechain-project', 'machine-click', 'midi-dump']
EXPECT_MAIN_OS = "f12e5875f93bb5c4ecb5f322e09ebb6f439ef8ff564602ce854addaa032f1413"
OUTPUT = {"cycles": "modded-cycles-techno-edition.syx",
          "samples": "modded-cycles-techno-edition_model-samples.syx"}


def build_cycles(src, out):
    r = subprocess.run([sys.executable, str(HERE / "tools" / "build.py"), "-i", str(src), "-t", ",".join(MODS),
                        "--expect-mainos", EXPECT_MAIN_OS, "-o", str(out)])
    if r.returncode:
        print("\nThe build stopped (see above). Is this the official model-cycles_OS1.13.syx from elektron.se?")
    return r.returncode


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+", help="model-cycles_OS1.13.syx (and model-samples_OS1.13.syx for a Model:Samples)")
    ap.add_argument("--machine", choices=tuple(OUTPUT), default="cycles", help="the machine you will flash")
    ap.add_argument("-o", "--output", help="output file")
    a = ap.parse_args()

    files = [pathlib.Path(f).expanduser() for f in a.files]
    for f in files:
        if not f.is_file():
            print(f"File not found: {f}")
            return 1
    out = pathlib.Path(a.output).expanduser() if a.output else files[0].with_name(OUTPUT[a.machine])

    if a.machine == "cycles":
        if len(files) != 1:
            print("For a Model:Cycles, give only model-cycles_OS1.13.syx.")
            return 1
        rc = build_cycles(files[0], out)
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
        rc = build_cycles(raws["cycles"][0], cyc_out)
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
