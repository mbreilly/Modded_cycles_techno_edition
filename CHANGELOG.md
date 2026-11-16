# Changelog

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
