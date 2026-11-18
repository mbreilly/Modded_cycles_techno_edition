# Modded Cycles Techno Edition

A free, modded firmware for the **Elektron Model:Cycles** (OS 1.13), with a companion plug-in (VST3 / AU /
standalone) for Mac, Windows and Linux.

- **27 machines**: Elektron's six, plus 21 added ones: classic drum machines (909, 808, 606), a rumble kick, modal
  metal, an additive drum voice, acid and growl basses, Braids, virtual-analog, cross-mod, 6-operator FM, a pad, a
  supersaw, a sampler, granular and wavetable engine that play your own samples, and a MIDI machine that plays your
  other gear.
- **A filter and an insert effect on every track**, a sidechain, a master DJ EQ, 6-channel USB audio, an LFO
  polarity switch, a CPU monitor and CPU budget, and quality-of-life changes to the screens.
- **The plug-in** shows every knob of every machine, follows the track and machine you pick on the Cycles, reads the
  sound back from the machine, picks samples and projects, and records automation in your DAW.

This repository never contains Elektron's firmware. You build the modded firmware yourself, on your computer, from
the official OS file you download from Elektron. The patcher checks that file and the result byte for byte.

> **Experimental firmware.** Every part is tested in emulation, running the Model:Cycles' own code, and the
> firmware has been played on real hardware, but use it at your own risk. Back up your projects and samples with
> Elektron Transfer before flashing. The official OS can always be put back (see [Going back](#going-back-to-the-official-os)).

**Manual:** the full owner's manual (49 pages, every machine, every button, the plug-in, and how the firmware
manages the CPU) is **[docs/Modded-Cycles-Techno-Edition-Manual.pdf](docs/Modded-Cycles-Techno-Edition-Manual.pdf)**.

## Contents

- [Build the firmware](#build-the-firmware)
- [Flash it](#flash-it)
- [On a Model:Samples](#on-a-modelsamples)
- [Going back to the official OS](#going-back-to-the-official-os)
- [The machines](#the-machines)
- [What else changes on the Cycles](#what-else-changes-on-the-cycles)
- [Samples](#samples)
- [MIDI](#midi)
- [The plug-in](#the-plug-in)
- [Bugs and features](#bugs-and-features)
- [Credits](#credits) and [licenses](#licenses)

## Build the firmware

**Easiest: in your browser.** Open the [web builder](https://mbreilly.github.io/Modded_cycles_techno_edition/), drop
Elektron's official `model-cycles_OS1.13.syx` on it and download `modded-cycles-techno-edition.syx`. Everything runs on
your computer; nothing is uploaded. It gives exactly the same file as the patcher below.

**Or with Python:**

You need **Python 3.8 or later** (nothing else) and the official Model:Cycles OS 1.13 file.

1. Download `model-cycles_OS1.13.syx` from [elektron.se](https://www.elektron.se/support-downloads/modelcycles)
   (Model:Cycles › Support › Downloads; unzip it if it comes as a `.zip`).
2. Download `Modded-Cycles-Techno-Edition-firmware-patcher.zip` from the latest [release](../../releases) and unzip it
   (or download this repository and use its `firmware/` folder).
3. In a terminal, in that folder:

   ```sh
   python3 patch.py path/to/model-cycles_OS1.13.syx
   ```

   On Windows, type `py` instead of `python3`. You can also drag the `.syx` file onto the terminal window to type
   its path.

The patcher checks that your file is the official one, applies the mods, checks the result against the expected
SHA-256 and writes **`modded-cycles-techno-edition.syx`** next to your file. If anything does not match, it stops and
writes nothing.

### Your own DX sounds (optional)

The DX machine (20) plays 32 sounds of its own on COLOR. You can swap them for any **DX7 32-voice bank** (a `.syx`
of about 4 KB: from a DX7, from [Dexed](https://asb2m10.github.io/dexed/), or a bank you downloaded) when you build
the firmware:

- **Web builder:** open *Optional: your own DX sounds*, choose the bank, then drop the OS file (in either order).
- **Patcher:** `python3 patch.py path/to/model-cycles_OS1.13.syx --dx-bank my-bank.syx`

The firmware is first built and checked as usual, then the bank goes in, and the file is called
`modded-cycles-techno-edition-dx.syx`. COLOR 0–31 then picks the bank's voices 1–32, and the screen shows the first
three letters of each name (BRASS 1 and BRASS 2 become BR1 and BR2). To change banks, build and flash again; your
projects keep the COLOR value, so they play whatever voice is in that slot. To edit the built-in sounds, start from
[`docs/dx/modded-cycles-dx-bank.syx`](docs/dx/modded-cycles-dx-bank.syx) (also in the patcher zip's `dx` folder), the
32 built-in sounds as a DX7 bank.

What the DX machine takes from each voice: the algorithm, feedback, each operator's frequency (ratio, fine, detune),
output level, envelope (four rates, four levels) and velocity sensitivity, and the voice's transpose. What it leaves
out: keyboard level and rate scaling, the pitch envelope, the LFO and amplitude modulation, and fixed-frequency
operators are tuned as if you played C4. So a voice sounds close to, but not exactly like, a real DX7: SHAPE (Bright)
and SWEEP (Env Time) are the quickest way to tame one that is too bright or too fast. The plug-in still shows the
built-in names (BEL, TUB...) for COLOR. Banks are your own: none is included except ours.

## Flash it

Back up your projects and samples with Elektron Transfer first.

**Over USB (simplest):** open [Elektron Transfer](https://www.elektron.se/support-downloads/transfer), connect the
Cycles, and drop `modded-cycles-techno-edition.syx` on it, as for an official OS update. The Cycles restarts by itself
after 1–3 minutes; do not switch it off before.

**Over MIDI (startup menu):** connect a MIDI interface's MIDI OUT to the Cycles' MIDI IN. Power off, hold `FUNC`,
power on, release, press `TRIG 4` (OS UPGRADE): the screen shows READY TO RECEIVE. Send the `.syx` to the
interface's port with any SysEx tool. Do not switch off during the update: sending over MIDI takes a few
minutes, then the Cycles restarts by itself within 1–3 minutes.

At power-on the new firmware shows a short logo animation and *modded cycles / techno edition*.

## On a Model:Samples

**Experimental.** The same firmware runs on a Model:Samples (same hardware): it becomes a Model:Cycles with these mods, and SAMPLER,
GRANULAR and WAVETABLE play your samples. The firmware is packed inside the Samples' own firmware, so its bootloader,
startup menu and signature stay Elektron's. You also need the official **Model:Samples OS 1.13**
(`model-samples_OS1.13.syx`, from [elektron.se](https://www.elektron.se/support-downloads/modelsamples)).

**Build it.** In the [web builder](https://mbreilly.github.io/Modded_cycles_techno_edition/), pick *Model:Samples*
and drop both official files. Or with Python, give both files in any order:

```sh
python3 patch.py --machine samples model-cycles_OS1.13.syx model-samples_OS1.13.syx
```

Both write `modded-cycles-techno-edition_model-samples.syx`. Back up your projects and samples with Elektron
Transfer first, then send it one of two ways:

- **Startup menu over MIDI** (tested on a real Model:Samples; works whatever OS the Samples runs, so this is also
  how you install a newer version later): connect a MIDI interface's MIDI OUT to the Samples' MIDI IN. Power off,
  hold `FUNC`, power on, release, press `TRIG 4` (OS UPGRADE): the screen shows READY TO RECEIVE. Send the `.syx`
  to the interface's port with any SysEx tool.
- **Elektron Transfer over USB** (not verified yet), only while the Samples still runs its own Model:Samples OS:
  drop the file on Transfer, as for an official OS update. If anything goes wrong, the startup menu brings it back.
  Once Modded Cycles is installed, Transfer can no longer update it: use the startup menu.

Do not switch off during the update: the Samples restarts by itself within 1–3 minutes after the transfer.

- The packing is the one of [Modded-Cycles](https://github.com/18nelli18/Modded-Cycles) (original flasher by RDS
  (AIM), integrated by DaftMaple). This edition was tested on a real Model:Samples through the startup menu over
  MIDI (16/11/2026), and the v1.6 build loaded on a Model:Samples again on 18/11/2026; installing it with
  Elektron Transfer is not verified yet.
- Only for a real Model:Samples: a Model:Cycles running the Samples OS would take it too, then refuse Model:Cycles
  firmwares over USB until its startup menu reinstalls the Cycles OS over MIDI IN.
- **Going back:** send the official `model-samples_OS1.13.syx` through the startup menu the same way. Before that,
  set any track that uses an added machine back to one of the six original machines.

## Going back to the official OS

Only the main OS is changed: the bootloader and the startup menu stay exactly as Elektron made them. To go back, send
Elektron's official `model-cycles_OS1.13.syx` the same way (Transfer, or the startup menu over MIDI IN).

### Your projects on the official OS (or another mod)

Projects you saved on this firmware open on the official OS without crashing, but not everything comes with them.
Before you go back, set every track that uses an added machine (7–27, EMPTY included) to one of the six original
machines and save the project. Here is what happens if you don't:

- **A track on an added machine** plays CHORD with the wrong settings; the MACHINES screen shows *Error* and the
  knobs do nothing. Turn LEVEL/DATA on the MACHINES screen: the track lands on CHORD with its own settings, and you
  can pick any original machine from there.
- **A project started on this firmware** has EMPTY on all six tracks, so on the official OS all six show *Error*
  until you change them.
- **The added settings** (track filter, machine extras, insert FX, sidechain, master EQ) are ignored by the official
  OS. An LFO aimed at the track filter moves another parameter instead. If you save the project on the official OS,
  they are erased: back on this firmware they load at their default values.
- **Another mod firmware** numbers its added machines its own way, so a track can open as a different machine, and
  its added settings may read ours differently. Set the tracks to original machines first there too.

Projects made on the official OS open on this firmware as they were, with the added settings at their defaults.

### Switching firmware cleanly

Flashing changes the firmware, not your project: after the flash, the Cycles reopens the project you were on, made on
the old firmware. A project belongs to the firmware it was made on; keep as many projects for each firmware as you like.

1. Save your project and back it up with Elektron Transfer.
2. Flash the other firmware.
3. Before you play or save anything, load a project made on this firmware, or start a new one. If the Cycles asks
   whether to save the old project first, answer **NO**.
4. Save a new project right away in a free slot. A name that tells the firmware (`OG…`, `TE…`) makes it easy to find
   later.

To take a project along: before you flash, set every track to one of the six original machines, save it as a copy in
a free slot (the original stays as it is), then flash; the Cycles opens the copy. Whatever only the old firmware has
stays behind. The Mods page settings (USB Out, Trk Trg, Mch Clk…) are kept by the Cycles itself, not by a project.

If the Cycles ever fails to start, the startup menu (`FUNC` + power on, then `TRIG 4`) over MIDI IN always brings
the official OS back.

## The machines

Press `MACHINES`: a list with a `>` on the selected machine and a counter. Turn `LEVEL/DATA` to move, **press**
`LEVEL/DATA` to load (so a bump of the encoder never changes your machine; set `Mch Clk` to OFF in
SETTINGS › Mods for the stock behaviour).

| # | Machine | What it is |
|---|---|---|
| 1–6 | KICK, SNARE, METAL, PERC, TONE, CHORD | Elektron's own machines, unchanged |
| 7 | 909BD | TR-909 kick from circuit models, tuned against real 909 recordings |
| 8 | 808BD | TR-808 kick from a circuit model, tuned against real 808 recordings |
| 9 | RUMBL | A rumble kick: kick into a dark feedback network, for long rolling low ends |
| 10 | 909 | The TR-909 kit: toms, rim, clap, hats, ride, crash and snare, picked per trig with SHAPE |
| 11 | 606 | The TR-606 kit: kick, snare, toms, hats and cymbal, picked per trig with SHAPE |
| 12 | 808 | The TR-808 hi-hat and cymbal |
| 13 | METL2 | Modal metal: bells, pipes, plates and bars |
| 14 | BIAS | Additive drum and drone voice with a wavefolder |
| 15 | ACID | TB-303 style bass with slides and Devil Fish style extras |
| 16 | GROWL | A dark growling bass |
| 17 | MACRO | Émilie Gillet's Braids, 47 models |
| 18 | VACF | Virtual-analog oscillator and filter voice |
| 19 | XMOD | Cross-modulation of two oscillators |
| 20 | DX | 6-operator FM with 32 sounds of its own, or a DX7 bank of your choice ([how](#your-own-dx-sounds-optional)) |
| 21 | ATMOS | Dark chord pad, playable as a drone |
| 22 | SAMPLER | Plays your own sample |
| 23 | GRANULAR | Granular playback of your sample |
| 24 | WAVETABLE | Your sample as a wavetable |
| 25 | EMPTY | Silence at almost no CPU; a new project starts with EMPTY on all six tracks |
| 26 | MIDI | No sound: the track plays another instrument over MIDI, with transpose, gate length and four CCs |
| 27 | UBSAW | JP-8000 style supersaw: seven detuned saws with chord saws, for stabs, leads and pads |

Every knob of every machine, with its defaults, is in **[docs/MACHINES.md](docs/MACHINES.md)**.

**Extras and the knob layer.** Added machines have up to four more parameters. **Double-tap `PUNCH`** (the LED
blinks) to turn on the knob layer, then turn `PITCH`, `DECAY`, `COLOR`, `SHAPE` for Extra 1–4; the other knobs play
the filter and insert effect (below). Double-tap `PUNCH` again to leave. Punch itself moves to a long press (half a
second). At 0 (the default) each machine plays its plain sound. Extras save with the sound and take p-locks. Holding
`MACHINES` and turning a knob does the same, and SETTINGS › Mods › `Knb Lyr` = MACH puts the layer on the open
MACHINES screen instead of `PUNCH`.

**Drum machine extras** follow the real machines: **Accent** (accented hits up to 6 dB louder, like the 909's TOTAL
ACCENT knob; plain hits unchanged) and **Drift** (each hit a little different in pitch, up to ±25 cents, and level,
about ±1 dB, like the parts of a real drum machine), plus tuning, decay and tone mods.

## What else changes on the Cycles

**Filter on every track.** On the knob layer (double-tap `PUNCH`), turn:

| Knob | Does |
|---|---|
| `LFO SPEED` | Filter Type: OFF / LP / HP / BP (12 dB) / LP24 / HP24 (24 dB) |
| `SWEEP` | Cutoff, 20 Hz–20 kHz |
| `CONTOUR` | Resonance |
| `DELAY` | Envelope amount (centre = none) |
| `REVERB` | Envelope decay, 5 ms–10 s |

**Insert effect on every track,** after the filter: on the knob layer, `SWING` picks OFF / DRV (drive) / CRS (bitcrush) /
FLD (wavefold) / RNG (ring mod) / RES (resonator) / RAT (RAT-pedal style distortion), `CHANCE` sets the
amount. Both save with the sound and take p-locks.

**Attack on every track,** after the insert effect: on the knob layer, `VOL + DIST` sets a fade-in that restarts on
every note, on every machine including Elektron's six. 0 = off (the default), 1 = 1.4 ms (softens a click), 64 ≈ 53 ms,
127 = 2 s: soft pads, bowed basses, hats that turn into a shaker. Saves with the sound, takes p-locks, CC 29.

**Settings › Mods** (a new ninth row of SETTINGS):

| Row | Does |
|---|---|
| `USB Out` | 2CH (stereo mix, stock) or 6CH (each track on its own USB channel, to record six stems) |
| `SC Src`, `SC Amt`, `SC Atk`, `SC Hold`, `SC Rel`, `Duck T1–T6` | Sidechain: one track's trigs duck the others (kick pumps the bass). Saved with the project |
| `Trk Trg` | OFF: the track buttons only select the track; `TRK` + button plays it |
| `Mch Clk` | ON: press `LEVEL/DATA` to load a machine; OFF: turning loads, as stock |
| `Knb Lyr` | PUNCH double tap (default) or the MACHINES screen for the knob layer |
| `CPU Lim` | Machines that would push the CPU past this limit are greyed out in the list (80 % default; OFF) |

**Master DJ EQ.** Double-tap `GATE`: `PITCH` / `DECAY` / `COLOR` are LOW / MID / HIGH on the whole mix (centre =
0 dB, full left = kill, right = +6 dB). Double-tap again to leave. GATE itself moves to a long press. Saved with the
project.

**LFO polarity.** `FUNC` + `LFO`, last row `Pol`: BI (stock) or UNI (the LFO only adds to the knob's position).

**CPU monitor.** SETTINGS › Device › `CPU`: load and peak bars; turn `LEVEL/DATA` right for each track's share.

**Lighter on the CPU.** The send delay and reverb stop by themselves after about 11 s with nothing sent to them
(and start again on the very block a track sends them sound), and part of the OS runs from fast internal RAM.

**Screens.** The sound browser shows three names at once and scrolls long names; turning `LEVEL/DATA` shows the
track level (and pan, with `FUNC`) as numbers.

## Samples

SAMPLER, GRANULAR and WAVETABLE play your own WAV files.

1. Connect the Cycles over USB and set SETTINGS › Device › `Transfer` to **SMP**: Elektron Transfer now sees a
   Model:Samples. Drag your WAV files onto it. (Transfer goes back to CYC at every power-on. Never update the OS while
   it is on SMP.)
2. On the Cycles, choose SAMPLER, GRANULAR or WAVETABLE on a track. **This alone loads nothing**: the screen says
   `NO SAMPLE` and `FUNC+MACHINES: PICK`.
3. Press `FUNC` + `MACHINES`. Your sample files are listed in the sound browser; find one and load it the way you load
   a sound. The waveform appears.
4. Save the sound or the project: the track finds its sample again by name when the project opens (the screen says
   `LOADING` meanwhile, or `NOT FOUND` if the file is no longer on the Cycles).

On SAMPLER, hold a trig and turn COLOR (Start) or SHAPE (End): the waveform shows that trig's locked Start and End
(`LK` on the bottom line), so you can place each step of a break by eye.

One sample per track, up to about 71 seconds each. The three machines share the track's sample, so you can switch
between them.

## MIDI

Every parameter is reachable by MIDI (enable Receive CC/NRPN in SETTINGS › MIDI CONFIG › SYNC). Added: extras on CC
20–23, filter on CC 74 / 71 / 24 / 25 / 26, insert effect on CC 27 / 28, and NRPNs on the FX channel for USB Out,
the sidechain, LFO polarity, the master EQ, sample and project selection, and a "send me everything" request. The
complete list is [plugin/midi-map.json](plugin/midi-map.json); the stock Model:Cycles CCs are unchanged.

**The MIDI machine** (26) turns a track into a sequencer track for another instrument: each trig sends its note on
the track's channel (turn the track's MIDI out on: FUNC + TRK, TRACK SETUP › MOUT), PITCH transposes it, DECAY sets
the gate (0 = the trig's length) and COLOR / SHAPE / SWEEP / CONTOUR send CC 74 / 71 / 1 / 10, or the CC numbers set
on the knob layer (120–127 = OFF). Details in [docs/MACHINES.md](docs/MACHINES.md#26--midi).

## The plug-in

`plugin/` is a JUCE plug-in (VST3, AU on Mac, and a standalone app) that talks to the Cycles over USB MIDI.

**Download** the build for your system from the latest [release](../../releases):

- **Mac** (`Modded-Cycles-Techno-Edition-plugin-macOS.zip`, Apple Silicon and Intel): copy
  `VST3/Modded Cycles Techno Edition.vst3` to `~/Library/Audio/Plug-Ins/VST3/` and `AU/Modded Cycles Techno Edition.component` to `~/Library/Audio/Plug-Ins/Components/`.
  The build is **not signed by Apple**, so macOS blocks it at first. In Terminal, run once:

  ```sh
  xattr -dr com.apple.quarantine ~/Library/Audio/Plug-Ins/VST3/"Modded Cycles Techno Edition.vst3" \
      ~/Library/Audio/Plug-Ins/Components/"Modded Cycles Techno Edition.component"
  ```

  then restart your DAW (in Logic, rescan in the Plug-in Manager). For the standalone app, right-click it › Open the
  first time.
- **Windows** (`Modded-Cycles-Techno-Edition-plugin-Windows.zip`): copy `VST3\Modded Cycles Techno Edition.vst3` to
  `C:\Program Files\Common Files\VST3\`.
- **Linux** (`Modded-Cycles-Techno-Edition-plugin-Linux.zip`): copy `VST3/Modded Cycles Techno Edition.vst3` to `~/.vst3/`.
  Each zip also has the standalone app in `Standalone/`.

**Set up the Cycles:** USB MODE (SETTINGS › Device › USB) = Audio + MIDI; SETTINGS › MIDI CONFIG › SYNC: receive
CC/NRPN on, send CC/NRPN on; note the track channels and the FX channel and set the same ones on the plug-in's SETUP
page.

**Build it yourself:** CMake 3.22+ and a C++ compiler; JUCE is downloaded by CMake.

```sh
cd plugin
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release
```

(Linux needs the JUCE dependencies: `libasound2-dev libjack-jackd2-dev libfreetype6-dev libfontconfig1-dev
libx11-dev libxcomposite-dev libxcursor-dev libxext-dev libxi-dev libxinerama-dev libxrandr-dev libxrender-dev
libglu1-mesa-dev mesa-common-dev`.)

## How the firmware is built

`firmware/patch.py` runs `firmware/tools/build.py` with the list of mods in `firmware/tweaks/model-cycles_OS1.13/`.
Each mod is a table of byte changes, each carrying a fingerprint (length and SHA-256) of the original bytes it replaces,
so the build refuses any file that is not the official OS 1.13; no byte of Elektron's firmware is in this repository. The added machines are compiled code stored compressed in the mods. The MAIN OS SHA-256
of the result is checked before anything is written. With `--dx-bank`, that check is made on the build with the
built-in DX sounds; then `firmware/tools/dx7bank.py` converts the DX7 bank and writes it over the DX machine's built-in
bank (and its names), which it first finds and checks byte for byte, before the machines are compressed. The web
builder does exactly the same (`tools/check_dx7bank.py` compares the two).

## Bugs and features

If something doesn't work as described, please [open an issue](https://github.com/mbreilly/Modded_cycles_techno_edition/issues)
with what you did and what happened, and I'll do my best to fix it. I'm keeping this edition focused, though, so I
won't be taking feature requests. The good news is that everything is open source: the toolchain, the machines and
the plug-in are all here, with a manual on how the firmware is built. If you want something different, you're very
welcome to fork it and make your own version. I'd love to hear what you come up with!

## Credits

Made by [m_reilly](https://soundcloud.com/m_reilly).

Built on the work of:

- **[18nelli18/Modded-Cycles](https://github.com/18nelli18/Modded-Cycles)** (MIT): the build toolchain, the
  per-track filter, the machine list, MACRO and ACID ports, and much of the reverse engineering.
- **[drumkilla/elektron-model-tweaks](https://github.com/drumkilla/elektron-model-tweaks)** (MIT): scrolling names
  and the `mtlib` firmware toolkit.
- **Marcel Bierling, [elektron-firmware-tool](https://github.com/mischa85/elektron-firmware-tool)** (MIT): the
  firmware container format.
- **[scottmetoyer/ms-multi-output](https://github.com/scottmetoyer/ms-multi-output)** (MIT): the original 6-channel
  USB audio mod.
- **[TinyGregAudio/Model-TG](https://github.com/TinyGregAudio/Model-TG)** (MIT): the CPU measurement, the sample
  transfer identity and the delay/reverb tricks.
- **[DMDaudio/model909](https://github.com/DMDaudio/model909)** (MIT): the 909 kick, toms, rim and clap.
- **Émilie Gillet, [Mutable Instruments eurorack](https://github.com/pichenettes/eurorack)** (MIT): Braids (MACRO),
  and the designs behind METL2, VACF, XMOD and DX's algorithms.
- **Robin Schmidt, [Open303](https://github.com/RobinSchmidt/Open303)** (MIT): the model behind ACID.
- **[100demons/bias](https://github.com/100demons/bias)** (MIT): BIAS.
- **Adam Szabo**, "How to emulate the super saw" (2010): the JP-8000 detune and mix curves behind UBSAW, and
  Graham Keane's [UberSaw](https://github.com/GrahamJamesKeane/UberSaw) (MIT) for the idea (no code used).
- **Matthew Fecher's** TR-606 analysis: the 606.
- **djd_oz**: volume and pan as numbers.
- **[JUCE](https://juce.com)** (AGPL-3.0 / commercial): the plug-in framework.

## Licenses

- Everything outside `plugin/` is **MIT** ([LICENSE](LICENSE)). The third-party licenses are in
  [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md) and next to the mods in `firmware/tweaks/model-cycles_OS1.13/`.
- `plugin/` is **AGPL-3.0** ([plugin/LICENSE](plugin/LICENSE)), as required by the open-source JUCE license.
- The tweak files contain short runs of the official OS bytes (the `old` values each change checks against your
  file) so the patcher can refuse the wrong file; they contain no Elektron firmware image.

Elektron, Model:Cycles, Model:Samples and Elektron Transfer are trademarks of Elektron Music Machines MAV AB. TR-606,
TR-808, TR-909 and TB-303 are trademarks of Roland Corporation. This project is not affiliated with or endorsed by
either company.
