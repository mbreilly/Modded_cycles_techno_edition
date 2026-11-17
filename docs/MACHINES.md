# Machines

Machines 1–6 are Elektron's own KICK, SNARE, METAL, PERC, TONE and CHORD, unchanged. Machines 7–27 are added.

Main knobs are the usual COLOR / SHAPE / SWEEP / CONTOUR (MIDI CC 16–19). **Extras** are played on the knob layer:
double-tap PUNCH (LED blinks) and PITCH / DECAY / COLOR / SHAPE become Extra 1–4 (CC 20–23, NRPN 1:40–1:43). Holding
MACHINES works too, and SETTINGS › Mods › Knb Lyr can move the layer to the MACHINES screen.
Every extra defaults to 0, which is the machine's plain sound.

## 7 · 909BD

TR-909 kick from analog circuit models (DMDaudio model909, MIT), tuned against real 909 recordings.

**Accent** makes accented hits (PUNCH on) up to 6 dB louder, like the 909's TOTAL ACCENT; plain hits are unchanged.

| Knob | Parameter | Default |
|---|---|---|
| COLOR | BD Attack | 64 |
| SHAPE | BD Shape | 64 |
| SWEEP | BD Sweep | 64 |
| CONTOUR | Sweep Time | 64 |
| Layer + PITCH | Accent | 0 |
| Layer + DECAY | Tune Decay | 0 |
| Layer + COLOR | Click | 0 |
| Layer + SHAPE | Tone | 0 |

## 8 · 808BD

TR-808 kick from a circuit model, tuned against real 808 recordings. A new hit rings on top of the old tail instead of cutting it. DECAY 64 fades out in about 1.5 s like a classic 808, 0 in 0.1 s, 127 in about 4 s.

CONTOUR is the **Accent** level of accented hits, as on the 808. **Drift** gives every hit a slightly different pitch (up to ±25 cents) and level (about ±1 dB), like the parts of a real drum machine.

| Knob | Parameter | Default |
|---|---|---|
| COLOR | BD Tone | 64 |
| SHAPE | BD Drop | 64 |
| SWEEP | Drop Time | 64 |
| CONTOUR | Accent | 0 |
| Layer + PITCH | Drift | 0 |
| Layer + DECAY | Tail | 0 |
| Layer + COLOR | Click | 0 |

## 9 · RUMBL

A rumble kick: a sine kick with pitch drop, held at full level for a moment, fed into a dark feedback delay network, so the rumble outlives the kick. C4 at PITCH 64 = a 52 Hz kick. DECAY = kick body, 60 ms to 3 s.

| Knob | Parameter | Default |
|---|---|---|
| COLOR | Tail | 64 |
| SHAPE | Damp | 40 |
| SWEEP | Drive | 40 |
| CONTOUR | Hold | 0 |
| Layer + PITCH | Sweep | 0 |
| Layer + DECAY | Sweep Time | 0 |
| Layer + COLOR | Rumble Level | 0 |
| Layer + SHAPE | Tail Pitch | 0 |

## 10 · 909

The TR-909 kit apart from the kick, in one machine: SHAPE (Voice) picks LT, MT, HT, RIM, CLP, CH, OH, RD, CR or **SD** on each trig (lock it per step). Each part keeps ringing when another is hit, as on the real 909. The knobs go to the voice of the last trig. The SD is tuned against real 909 snare recordings.

**Accent** makes accented hits up to 6 dB louder; **Drift** varies pitch and level from hit to hit.

| Knob | Parameter | Default |
|---|---|---|
| COLOR | Tone/ Noise | 64 |
| SHAPE | Voice (LT / MT / HT / RIM / CLP / CH / OH / RD / CR / SD) | 0 |
| SWEEP | Sweep/ Spread | 64 |
| CONTOUR | Time/ Burst | 64 |
| Layer + PITCH | Accent | 0 |
| Layer + DECAY | Range/ Tail | 0 |
| Layer + COLOR | Drift | 0 |
| Layer + SHAPE | Tone | 0 |

## 11 · 606

A TR-606 kit in one machine (after Matthew Fecher's TR-606 analysis); SHAPE picks BD, SD, LT, HT, CH, OH or CY on each trig. PITCH tunes (64 = the 606), DECAY sets the decay, PUNCH is the accent.

**Drift** varies pitch and level from hit to hit. The other extras act on the voice SHAPE selects.

| Knob | Parameter | Default |
|---|---|---|
| COLOR | Tone | 64 |
| SHAPE | Voice (BD / SD / LT / HT / CH / OH / CY) | 0 |
| SWEEP | Sweep | 64 |
| CONTOUR | Noise | 64 |
| Layer + PITCH | Drift | 0 |
| Layer + DECAY | Long Decay | 0 |
| Layer + COLOR | Sweep | 0 |
| Layer + SHAPE | Accent Level | 0 |

## 12 · 808

The TR-808 hi-hat and cymbal in one machine: six square oscillators through band-pass and high-pass filters. SHAPE 0–63 is the hat, 64–127 the cymbal, and within each half it is that voice's high-pass. The hat and the cymbal each keep ringing when the other is hit.

**Drift** varies the level from hit to hit.

| Knob | Parameter | Default |
|---|---|---|
| COLOR | Color/ Tone | 64 |
| SHAPE | Voice HPF | 32 |
| SWEEP | Res/Hi Decay | 64 |
| CONTOUR | Noise/ Spread | 0 |
| Layer + PITCH | Metal Tune | 0 |
| Layer + DECAY | Drift | 0 |
| Layer + COLOR | Filter/ Curve | 0 |
| Layer + SHAPE | Accent Level | 0 |

## 13 · METL2

Modal metal: a mallet or noise exciter into 8 damped resonators whose ratios morph across six materials (after the modal resonators of Émilie Gillet's Rings and Plaits, written from scratch). DECAY = damping, the lowest mode ringing 50 ms to 10 s.

| Knob | Parameter | Default |
|---|---|---|
| COLOR | Struct (STR / PIP / SHT / PLT / BEL / BAR) | 70 |
| SHAPE | Bright | 80 |
| SWEEP | Position | 20 |
| CONTOUR | Exciter | 10 |
| Layer + PITCH | Dent | 0 |
| Layer + DECAY | Scrape | 0 |
| Layer + COLOR | Hi Damp | 0 |
| Layer + SHAPE | Drive | 0 |

## 14 · BIAS

A percussion and drone voice ported from [100demons/bias](https://github.com/100demons/bias) 2.0 (MIT): six oscillators with their own decays and an unlimited wavefolder, on an internal clock locked to the pitch (a clean-room voice after the published description of the Basimilus Iteritas Alia). COLOR adds partials, SHAPE morphs sine → triangle → saw → square, SWEEP spreads the partials from harmonic to inharmonic, CONTOUR sets the fold. DECAY 127 drones; PUNCH gives the Liquid pitch drop when the Liquid extra is 0.

| Knob | Parameter | Default |
|---|---|---|
| COLOR | Harm | 40 |
| SHAPE | Morph | 43 |
| SWEEP | Spread | 16 |
| CONTOUR | Fold | 24 |
| Layer + PITCH | Liquid | 0 |
| Layer + DECAY | Liq Time | 0 |
| Layer + COLOR | Strike | 0 |
| Layer + SHAPE | Drive | 0 |

## 15 · ACID

A TB-303 style bass (after Robin Schmidt's Open303, MIT, rewritten in integer code): saw or square into a resonant filter with its own envelope, slides from your trigs, and a drive, tuned against a TD-3. The extras are Devil Fish style modifications. Hold PUNCH half a second to switch saw / square.

Slide: make a trig longer than the gap to the next trig and the note glides into it.

| Knob | Parameter | Default |
|---|---|---|
| COLOR | Cutoff | 40 |
| SHAPE | Reso | 90 |
| SWEEP | Env Mod | 80 |
| CONTOUR | Drive | 0 |
| Layer + PITCH | Slide Time | 0 |
| Layer + DECAY | Filter FM | 0 |
| Layer + COLOR | Muffler | 0 |
| Layer + SHAPE | Accent | 0 |

## 16 · GROWL

A dark, growling bass: three detuned saws that drift slowly, a sub, a noise layer and a drive into a dark low-pass, with a fast growl (4 to 32 Hz) on the filter, the level and, at high depth, the pitch. Best between C1 and C2.

| Knob | Parameter | Default |
|---|---|---|
| COLOR | Detune | 40 |
| SHAPE | Growl Rate | 72 |
| SWEEP | Growl Depth | 64 |
| CONTOUR | Tone | 60 |
| Layer + PITCH | Sub Level | 0 |
| Layer + DECAY | Attack | 0 |
| Layer + COLOR | Noise | 0 |
| Layer + SHAPE | Drive | 0 |

## 17 · MACRO

Émilie Gillet's Braids macro-oscillator (MIT), compiled unchanged: 47 models (classic and sync waves, triple oscillators, swarm, filtered waves, vowels and formants, FM, physical models, drums, wavetables and noise). FUNC + PITCH = lo-fi (sample rate to the left, bits to the right).

| Knob | Parameter | Default |
|---|---|---|
| COLOR | Timbre | 64 |
| SHAPE | Model | 0 |
| SWEEP | Color | 64 |
| CONTOUR | Env Timbre | 0 |
| Layer + PITCH | Attack | 0 |
| Layer + DECAY | Env Color | 0 |
| Layer + COLOR | Lofi Bits | 0 |
| Layer + SHAPE | Lofi Rate | 0 |

## 18 · VACF

A virtual-analog voice: a variable-shape oscillator and a sub into two state-variable filters, with a filter envelope, hard sync, a detuned second oscillator and drive (after Plaits' VA engine, written from scratch).

| Knob | Parameter | Default |
|---|---|---|
| COLOR | Cutoff | 50 |
| SHAPE | Reso | 40 |
| SWEEP | Env Mod | 60 |
| CONTOUR | Wave (SAW / SQR / PLS) | 0 |
| Layer + PITCH | Sync | 0 |
| Layer + DECAY | Detune | 0 |
| Layer + COLOR | Sub | 0 |
| Layer + SHAPE | Drive | 0 |

## 19 · XMOD

Cross-modulation: a carrier at the note and a modulator at a musical ratio, combined by six algorithms that CONTOUR morphs through (after Warps, written from scratch).

| Knob | Parameter | Default |
|---|---|---|
| COLOR | Timbre | 40 |
| SHAPE | Mod Ratio (11 named values) | 40 |
| SWEEP | Mod Wave (SIN / TRI / SAW / SQR) | 0 |
| CONTOUR | Algo (XFD / FLD / DIO / RNG / XOR / CMP) | 50 |
| Layer + PITCH | Car Wave (SIN / TRI / SAW / SQR) | 0 |
| Layer + DECAY | Mod Env | 0 |
| Layer + COLOR | Detune | 0 |
| Layer + SHAPE | Crush | 0 |

## 20 · DX

Six-operator FM like a DX7: the 32 classic algorithms, per-operator envelopes, feedback, and a bank of 32 sounds of its own (no Yamaha patches). C4 at PITCH 64.

| Knob | Parameter | Default |
|---|---|---|
| COLOR | Patch (32 named values) | 0 |
| SHAPE | Bright | 64 |
| SWEEP | Env Time | 64 |
| CONTOUR | Algo (33 named values) | 0 |
| Layer + PITCH | Feedback | 0 |
| Layer + DECAY | Op6 Ratio | 0 |
| Layer + COLOR | Vel Sens | 0 |
| Layer + SHAPE | Detune | 0 |

**Your own sounds:** build the firmware with a DX7 32-voice bank and its voices replace the 32 built-in sounds on
COLOR (shown by the first three letters of their names). See [Your own DX sounds](../README.md#your-own-dx-sounds-optional).

## 21 · ATMOS

A dark pad: a 4-note chord of detuned saw pairs under a low-pass that drifts slowly, with its own plate tail. DECAY is the release (127 = hold). GATE on = a drone that plays by itself while the sequencer runs (STOP releases it, PLAY starts it again).

| Knob | Parameter | Default |
|---|---|---|
| COLOR | Color | 72 |
| SHAPE | Chord (OCT / 5TH / MIN / MI7 / MI9 / M11 / SU2 / SU4 / MAJ / MA7 / DRK / CLU) | 3 |
| SWEEP | Drift | 64 |
| CONTOUR | Space | 70 |
| Layer + PITCH | Swell | 0 |
| Layer + DECAY | Air | 0 |
| Layer + COLOR | Wobble | 0 |
| Layer + SHAPE | Width | 0 |

## 22 · SAMPLER

Plays a sample you sent with Elektron Transfer (see the README, Samples). One sample per track, up to about 71 s. PITCH and the trig note transpose (64 / C4 = as recorded). Start, End and Loop Start can be turned while a note plays and are heard at once (since v1.4). In SLD mode, SHAPE sets the loop length and the loop slides through the sample as you turn Start.

| Knob | Parameter | Default |
|---|---|---|
| COLOR | Start | 0 |
| SHAPE | End (in SLD: loop Length) | 127 |
| SWEEP | Mode (FWD / REV / LOP / PNG / SLD) | 0 |
| CONTOUR | Lofi | 0 |
| Layer + PITCH | Fine | 0 |
| Layer + DECAY | Attack | 0 |
| Layer + COLOR | Loop Start | 0 |
| Layer + SHAPE | Drive | 0 |

## 23 · GRANULAR

Granular playback of the track's sample: up to 8 grains under a Hann window.

| Knob | Parameter | Default |
|---|---|---|
| COLOR | Position | 0 |
| SHAPE | Size | 64 |
| SWEEP | Density | 64 |
| CONTOUR | Spray | 0 |
| Layer + PITCH | Spread | 0 |
| Layer + DECAY | Window | 0 |
| Layer + COLOR | Scan | 0 |
| Layer + SHAPE | Reverse | 0 |

## 24 · WAVETABLE

Turns the track's sample into a wavetable: frames of 2,048 samples, one period per frame. The phase restarts on each trig.

| Knob | Parameter | Default |
|---|---|---|
| COLOR | Position | 0 |
| SHAPE | Warp | 0 |
| SWEEP | Env | 0 |
| CONTOUR | Env Speed | 64 |
| Layer + PITCH | Sub | 0 |
| Layer + DECAY | Detune | 0 |
| Layer + COLOR | Crush | 0 |
| Layer + SHAPE | Drive | 0 |

## 25 · EMPTY

Silence at almost no CPU. A new project puts EMPTY on all six tracks, so you start with the whole CPU budget free.

## 26 · MIDI

Makes no sound: the track plays another instrument over MIDI OUT and USB. Each trig sends its note with the trig's
velocity on the track's MIDI channel; MIDI adds a transpose, a gate length and four CCs. Turn the track's MIDI out on
(FUNC + TRK opens TRACK SETUP: MOUT) and give the track a channel in SETTINGS › MIDI CONFIG › CHANNELS; PORT CONFIG ›
Output To picks MIDI, USB or both.

| Knob | Parameter | Default |
|---|---|---|
| PITCH | Transpose, one semitone per step | 0 |
| DECAY | Gate: 0 = the trig's length (LEN), 1–127 = DECAY / 8 steps | 0 |
| COLOR | CC A (CC 74) | 64 |
| SHAPE | CC B (CC 71) | 64 |
| SWEEP | CC C (CC 1) | 64 |
| CONTOUR | CC D (CC 10) | 64 |
| Layer + PITCH | CC A Number | 0 = 74 |
| Layer + DECAY | CC B Number | 0 = 71 |
| Layer + COLOR | CC C Number | 0 = 1 |
| Layer + SHAPE | CC D Number | 0 = 10 |

CC numbers: 0 = the default shown, 1–119 = that CC, 120–127 = OFF (not sent). A CC goes out when its value changes:
when you turn the knob (sequencer stopped too), and just before a note whose trig p-locks it. Picking the machine or
loading a project sends nothing until a knob moves. PUNCH, GATE, the filter, the insert FX, sends and level do nothing
here. The plug-in does not take these CCs as the track's filter or pan.

## 27 · UBSAW

The JP-8000 "supersaw": seven detuned saws, plus up to two chord saws, with the detune and mix curves measured on the
original (Adam Szabo's analysis, written from scratch, band-limited). Every saw starts at a random phase on each note and
drifts slowly, so no two notes are quite the same. Big trance and hoover stabs, wide leads and pads.

| Knob | Parameter | Default |
|---|---|---|
| COLOR | Detune: from unison to the wide JP-8000 spread | 64 |
| SHAPE | Mix: the centre saw alone at 0, the six side saws louder as you turn up | 80 |
| SWEEP | Chord (OFF, OCT, 5TH, 5OC, MAJ, MIN, SU4, SU2, MA7, MI7, DO7, AD9, MOC) | 0 |
| CONTOUR | High Pass that follows the note, up to twice the note's pitch (thins the low end like the JP-8000) | 0 |
| Layer + PITCH | Attack: a fade-in after each trig, up to 2 s | 0 |
| Layer + DECAY | Drift: more and slower random detune, up to about 12 cents | 0 |
| Layer + COLOR | Pad Filter: a slowly wandering low-pass, from about 5 kHz down to 250 Hz | 0 |
| Layer + SHAPE | Chord Level: louder chord saws, up to three times | 0 |

Chords: OCT octave, 5TH fifth, 5OC fifth and octave, MAJ / MIN triads, SU4 / SU2 suspended, MA7 / MI7 / DO7 sevenths,
AD9 fifth and ninth, MOC minor third and octave. Amplitude follows DECAY like TONE; GATE holds the note.
