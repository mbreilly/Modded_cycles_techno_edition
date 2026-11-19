# Changelog

## v1.6.5

- **UBSAW, simpler**: one filter and one Attack per track, as on the other machines. UBSAW's own Pad Filter and
  Attack are gone: the track filter (LP / LP24) and the track's Attack (`VOL + DIST` on the knob layer) do the same.
  CONTOUR is now **Chord Level**; the high pass that follows the note moved to the knob layer as **Low Cut**
  (hold `MACHINES` + `PITCH`); Drift stays on `MACHINES` + `DECAY`.
- **UBSAW chords are now ATMOS's**: OFF, then OCT 5TH MIN MI7 MI9 M11 SU2 SU4 MAJ MA7 DRK CLU, shown by name. Four-note
  chords play three chord saws over the supersaw. Both machines read the same list, so chords added later reach both.
- UBSAW projects saved with v1.5 to v1.6.4 sound different: CONTOUR is read as Chord Level, the old Attack value as
  Low Cut, and the chord numbers follow the new list. ATMOS is unchanged.
- Manual: thirteenth edition (UBSAW page and knob tables).

Thanks to the user who suggested it.

## v1.6.4

- **SAMPLER, fine Start and End with a waveform zoom**: hold `FUNC` and turn `COLOR` (Start) or `SHAPE` (End) to move
  it in 1/64 of a step instead of whole steps. While `FUNC` stays held, the screen zooms in around that bar (about two
  steps, at least 50 ms) and shows its value (`ZOOM ST40.50`) and where it is in the sample in seconds. Let go of
  `FUNC` to see the whole sample. Works on p-locks too. The plug-in still shows and sends whole steps. Proven in
  emulation, not yet tried on hardware.
- Manual: twelfth edition ("Fine Start and End, and the zoom").

Thanks to the user who asked for it.

## v1.6.3

- **Trig preview**: with the sequencer stopped or paused, hold a trig and press `PAGE` to hear that step (its note,
  length, p-locks and sound lock); the page does not turn. drumkilla's mod (MIT). The manual already mentioned it,
  but no build had it.
- **SAMPLER, setting a locked Start or End**: holding a trig shows the trig menu (NOTE / VEL / LEN) over the left half
  of the waveform. Turning `COLOR` (Start) or `SHAPE` (End) now hides the menu, so the whole waveform shows with that
  trig's bars; press or turn `LEVEL/DATA` to bring the menu back. Proven in emulation, not yet tried on hardware.
- Manual: eleventh edition (trig preview in chapters 2 and 3, the trig menu in "Seeing a p-locked Start or End").

Thanks to the user who reported both.

## v1.6.2

- **Model:Samples** (experimental): the web builder and `patch.py --machine samples` pack the firmware for a Model:Samples from
  both official OS 1.13 files, to send through its startup menu over MIDI IN (or with Transfer while it still runs
  its own OS). Same packing as Modded-Cycles' (original flasher by RDS (AIM), integrated by DaftMaple), same bytes.
  Tested on a real Model:Samples through the startup menu over MIDI, and DaftMaple loaded this edition's Samples
  file on a Model:Samples (18/11/2026); Elektron Transfer is not verified yet. The
  packing checks Elektron's code by SHA-256 only, so no byte of the OS is stored in the repository.
- Manual: tenth edition ("On a Model:Samples" in chapter 1; Attack and the Model:Samples option in the overview).

## v1.6.1

- Fixed: **stereo samples** played at half speed, an octave too low, on SAMPLER, GRANULAR and WAVETABLE. A stereo
  file is now mixed to mono (left + right) as it loads, so it plays at its own speed and pitch, like a mono one.
  A slot holds up to about 35 seconds of stereo (71 seconds of mono). The plug-in's sample window shows stereo
  samples at their right length too.
- Manual: ninth edition (stereo samples in "Sending and loading a sample").

Thanks to the user who reported it.

## v1.6

- **Attack on every track**: on the knob layer (double-tap `PUNCH`, or hold `MACHINES`), `VOL + DIST` now sets a
  fade-in that restarts on every note, after the filter and the insert effect. It works on all 27 machines, the
  six Elektron machines included. 0 = off (the default, the track is unchanged), 1 = 1.4 ms, 64 ≈ 53 ms, 127 = 2 s.
  Saves with the sound, takes p-locks, LFO and velocity; CC 29 / NRPN 1:22. The plug-in has it in TRACK FX.
- Fixed: a sound saved with the **RAT** insert effect came back with the effect OFF when reloaded.
- Manual: eighth edition (Attack in chapters 2 and 4, MIDI tables).

Tested on a Model:Cycles before release.

Thanks to the user who asked.

## v1.5.1

- **SAMPLER, GRANULAR, WAVETABLE**: the screen now says what to do instead of LOADING forever. Choosing the machine
  loads no sample: it shows **NO SAMPLE** and **FUNC+MACHINES: PICK**. A saved sample that is gone shows
  **NOT FOUND** (or **NOT A SAMPLE** / **READ ERROR**) with the same hint. LOADING only shows while a sample really
  loads.
- **SAMPLER**: hold a trig and turn COLOR (Start) or SHAPE (End) to see that trig's locked Start and End on the
  waveform, instead of a number. The bottom line starts with **LK** while you look at a trig's locks.
- Manual (seventh edition) and README: sample loading as clear steps, with what each screen message means.

Thanks to the users who asked.

## v1.5

- **New machine 27, UBSAW**: the JP-8000 style supersaw. Seven detuned saws on the curves measured on the original,
  up to two chord saws (SWEEP: octave, fifth, major, minor, sus, sevenths...), a high pass that follows the note,
  and four extras: Attack, Drift, Pad Filter and Chord Level. It comes after MIDI, so the machines of your projects
  keep their numbers.
- Manual: sixth edition (UBSAW page, machine tables).
- README and manual: how to switch firmware cleanly (load or start a project made on the new firmware before
  playing, answer NO to saving the old one, one set of projects per firmware), and what happens to projects saved on
  this firmware when you go back to the official OS or to another mod.

## v1.4.1

- **CPU Lim** now defaults to **80 %** (was 70 %). A project made before flashing keeps the six stock machines, which
  already count about 74 % with the rest of the OS, so at 70 % every heavier machine was greyed out even with nothing
  playing. New projects still start with EMPTY on all six tracks. If you had set CPU Lim to 80 % yourself, it now
  reads 70 %: press LEVEL/DATA to move it on.
- Manual: fifth edition.

Thanks to the user who reported it.

## v1.4

- **SAMPLER**: Start, End and Loop Start now follow the knobs while a note plays, as on the Model:Samples (before,
  a turn was only heard at the next trig).
- **SAMPLER**: new Mode **SLD** (slide, SWEEP at the top): SHAPE sets the loop length, and the loop keeps that length
  and moves through the sample as you turn Start.
- Manual: fourth edition.

Thanks to the user who asked for both.

## v1.3

Bug fixes in the machines, the sound otherwise unchanged:

- **909**: the hand clap with DECAY above the middle got shorter instead of longer; same jump on the clap's CONTOUR,
  the toms' CONTOUR and the Tail extra. They now keep growing to the end of the knob.
- **METL2**: SHAPE (Bright) above about 98 turned the hit into full-scale noise. It now keeps getting brighter.
- **VACF**: the Detune extra now reaches +40 cents, as the manual says (it stopped at +20).
- **RUMBL**: with Rumble Level and Tail Pitch turned up, the tail could hum very quietly for ever and keep using CPU.
  It now dies away.

Patcher and web builder: the mod files no longer carry any bytes of Elektron's firmware. Each change used to hold the
few original bytes it replaces, to check your file before writing; it now holds their length and SHA-256 instead. The
firmware you get is byte for byte the same.

## v1.2

- **Your own DX sounds:** the web builder and the patcher (`--dx-bank`) can put a DX7 32-voice bank in place of the
  DX machine's 32 built-in sounds. The built-in sounds are also available as a DX7 bank,
  `docs/dx/modded-cycles-dx-bank.syx`, to edit in Dexed. Without a bank the firmware is unchanged.
- Manual: third edition, with your own DX sounds.

## v1.1

- **MIDI machine** (26, after EMPTY): makes no sound; the track plays another instrument over MIDI OUT and USB. Each
  trig sends its note on the track's channel; PITCH transposes it, DECAY sets the gate length, and COLOR / SHAPE /
  SWEEP / CONTOUR send four CCs (74 / 71 / 1 / 10 by default, any CC or OFF on the knob layer), on knob turns and on
  p-locked trigs.
- The plug-in knows the MIDI machine and its CC numbers, and ignores those CCs coming back from the Cycles.
- Manual: second edition, with the MIDI machine.

## v1.0

First public release.

- 25 machines: Elektron's six, 909BD, 808BD, RUMBL, 909 (with a new 909 snare), 606, 808, METL2, BIAS, ACID, GROWL,
  MACRO, VACF, XMOD, DX, ATMOS, SAMPLER, GRANULAR, WAVETABLE and EMPTY.
- Drum machines tuned against real 909, 808 and 606 recordings, with Accent and Drift extras.
- A filter (LP / HP / BP, LP24 / HP24) and an insert effect (drive, bitcrush, fold, ring, resonator, RAT) on every
  track.
- Sidechain, master DJ EQ, LFO polarity, 6-channel USB audio, CPU monitor and CPU budget, machine list with
  press-to-load, knob layer on PUNCH, track buttons that only select, multi-line browser with scrolling names, level
  and pan as numbers.
- Samples sent with Elektron Transfer for SAMPLER, GRANULAR and WAVETABLE.
- The Modded Cycles Techno Edition plug-in (VST3 / AU / standalone) for macOS, Windows and Linux.
- An owner's manual in PDF: `docs/Modded-Cycles-Techno-Edition-Manual.pdf`.

**Bugs and features.** If something doesn't work as described, please open an issue on GitHub with what you did and
what happened, and I'll do my best to fix it. I'm keeping this edition focused, though, so I won't be taking feature
requests. Everything is open source, so if you want something different, you're very welcome to fork it and make your
own version. I'd love to hear what you come up with!
