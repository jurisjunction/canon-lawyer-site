# arrange: the organ edition of "On These Two Hang"

Richard asked, on 25 October 2026: "can you score it for an organ accompaniment with optional instruments (percussion). No church choir will do this as techno." The track is a Strudel piece with a 909 kick, hi-hats and a square-wave arpeggio around a choir. This folder makes the same piece for a parish: SATB choir and organ, with optional bells and optional percussion (one player each), and an optional reader. It arranges by rule, from the events the track actually plays.

## The files

| File | What it does |
| --- | --- |
| `events.mjs` | Asks Strudel's own engine (pinned @strudel/core 1.1.0, from `checkers/`) for every event the track plays, bar by bar: onset and end as exact fractions, and every control value. It interprets nothing. |
| `organ_edition.py` | The arranger. Sorts the events into the track's layers, takes the choir from the published choir parts, arranges the rest by the rules below, and writes one LilyPond file with three books (full score with a preface, bells part, percussion part) and a MIDI score. |
| `check_edition.py` | The check. Reads back what LilyPond made (the MIDI, and the .ly only for hyphens, section marks and the spoken line) and compares it with the published choir and with the engine, layer by layer. It has its own MIDI reader and its own reading of the track's orbits, so it does not share code with the arranger. |

## How to run it

```
cd checkers && npm install && cd ..                      # once: Strudel's engine
pip install --break-system-packages lilypond             # once: LilyPond 2.25 (or any 2.24+)

python3 arrange/organ_edition.py --site ../canon-lawyer-site            # the short form
python3 arrange/organ_edition.py --site ../canon-lawyer-site --long     # the long form
#   options: --out DIR (default: the site's docs/assets/music/scores/), --engrave (runs LilyPond), --log
lilypond -dno-point-and-click -o DIR/on-these-two-hang-organ DIR/on-these-two-hang-organ.ly

python3 arrange/check_edition.py --site ../canon-lawyer-site [--long] [--dir DIR]
```

Inputs, all read from the site: the track (`docs/assets/music/on-these-two-hang.strudel.js`, or `.long.strudel.js`) and the published choir MIDI (`docs/assets/music/scores/on-these-two-hang-{S,A,T,B}.mid`, or `-long-`), which `counterpoint.py --midi` wrote with a lyric event on every sung syllable. The arranger refuses to run if the published choir is not, note for note, what the engine says the track's choir sings.

Outputs: `<stem>-organ.ly`, and from LilyPond `<stem>-organ.pdf` (the full score, a preface page first), `<stem>-organ-bells.pdf`, `<stem>-organ-percussion.pdf` and `<stem>-organ.mid` (a track to a staff: bells, percussion, S, A, T, B, organ right hand, left hand, pedal; and the lyrics). The stem is `on-these-two-hang` or `on-these-two-hang-long`. Two runs give byte-identical `.ly` files.

Needs: Python 3 (standard library only), Node 18+ with `checkers/node_modules`, LilyPond 2.24 or later for the PDFs.

## How the layers are found

The track names its own orbits: 1 the clock, 2 the wheel, 3 the chanted lines, 4 organ, 5 the veil and the earth, 6 choir, 7 bells. An event's orbit and sound say which layer it is; on the organ's orbit the envelope tells its uses apart (attack .05 the doubling under every `satb()`, .4 `viri`, 1 the `pedal`, .1 the Amen's organ). On the choir's orbit, pan tells the voices apart (as `voices.mjs` did). An event with no rule stops the arranger.

## The mapping, as built

| Track layer | Edition | Notes |
| --- | --- | --- |
| choir (`satb`, `solo`, the Amen chords) | SATB, unchanged | Notes, Latin, hyphens, solo markings and "free voices: text to be set" as in the published score, engraved by `counterpoint.py`'s own rules (copied here). The short form's repeat in Duobus is written out, because the instruments differ the second time. Bars 1-8 and the four bars of silence after the Amen are written as bars. |
| `organ()` under every `satb()` | Organ, colla parte: Manual I (Principal 8', soft); pedal 16' + 8' with the basses | Hands by rule, bar by bar: see below. |
| `organ(LEX_B, .07)` (long form) | Pedal "+ Principal 8' (or a soft reed): the Law held" | The bass's notes, already on the pedal; the extra gain becomes registration. |
| `pedal` (E2 + B2), Pendet and Fundamentum | Pedal: the fifth, held (tied, not struck each bar) | In Fundamentum it holds the sung bass's E2 too. |
| `viri` (VIRI in long notes, organ) | Manual I, left hand, in Pendet | Left out in the last part of Duobus (no hand free). |
| `canticle` (TRIPLUM, recorder) | Manual II solo, right hand (Gedackt 8', Flute 4') | In Pendet, and at the end of Duobus instead of the choir doubling. |
| `wheel` (square wave, the triad in eighths) | Manual II, left hand, staccato, every note | Low-pass as registration and dynamics: 2400 Hz mp, 1800 Hz p, 500 Hz (the darkness) Gedackt 8' alone, box closed, pp. |
| Amen chords | Both chords on the organ: the F chord on the choir's registration, the E chord full organ | The track's organ plays only the E chord; the F chord is added so the choir is not left alone before the light. |
| `bells(...)` (celesta, tintinnabuli) and the Amen's celesta chord | Bells part: handbells, handchimes or glockenspiel | Written at the track's pitch. Notes above C6 under 8va (display only). Organ cue staff (Manual II, if no bells) in the bells' first entrance (bars 9-12) and their return after the tomb (Vere, bars 55-60 / 111-116). |
| `tick`: `bd` | Bass drum, soft beater (half-bar beats, quarter notes) | |
| `tick`: `hh*8` | Woodblock (or claves), eighths | Left out where the same hands play the hammer (the darkness, the end of Duobus: the organ's wheel has the eighths) and in the bar of the stone. The clock's stutter (`degradeBy(.5)`) is exact. |
| `hammer` (rim, the Morse of CARPENTER) | Temple block (or side stick): dot a sixteenth, dash a dotted eighth | Every stroke. |
| `rocks` (rim) | Temple block | **Not Morse**: the track's `rocks` is `~ rim ~ ~ rim ~ ~ rim`, three strokes a bar. The brief said Morse; the track wins. First bar of the rent left out (both hands roll the cymbal). |
| `timpani` (E2 eighths, gain rising) | One timpano on E, eighths, p < f | |
| `veil` (white noise, low-pass falling) | Suspended cymbal, soft mallets, roll f > in the rent's first bar, then let ring | Strudel samples the sweep once per event (at its midpoint), so the track plays two bars of noise at 6788 Hz then 2363 Hz, gain .125 then .055: a step down, not a smooth sweep. |
| `quake` (brown noise + a sine on E1) | Bass drum roll at the stone (Vere, bar 1); in the rent the pedal holds low E on 16' (+32'), the sine's pitch | In the rent no hand is free for the bass drum; the preface says a second player could add it. |
| `whirlwind` (pink noise) | Wind machine (or the cymbal, rolled), pp, two bars | Strudel samples its `saw` gain at the midpoint, so the track plays a steady soft noise, not a swell. |
| `vox(...)` (SAM and the ascended choir) | Dropped | The choir and the soloist sing those lines. |
| `vox("if_ye_love_me")` | A spoken line for a reader or the priest, optional, written over the first bar of the silence after the Amen (bar 73 / 179) | |

### The organ's hands, bar by bar

- **Pedal**: the sung bass, at 16' and 8'; else the fifth; else the quake's low E.
- **Left hand**: the wheel, whole, wherever the track plays it (Manual II); else `viri` (Manual I); else choir doubling.
- **Right hand**: the canticle (Manual II); else choir doubling.
- **The choir doubling**: a free hand takes at most two of S, A, T, never more than an octave apart at any moment, the right hand's above the left's. Of the ways that fit, the one that doubles the most notes of a subject (the notes with words), then the most notes, then the same as the bar before, then the higher voices. A held note stops at the bar where its hand is given something else. Two notes in one hand more than an octave apart: the lower goes to the left hand if it is free, or is left to the choir.

So under the wheel the tenor is often left to the choir (short form 34 of 82 tenor organ notes, long form 114 of 369; reported by the check), and in the last four bars of Duobus the manuals play the canticle and the wheel, not the choir.

## What it gets wrong, or leaves to a person

- **The tenor under the wheel.** One organist cannot double four voices and play the wheel. The rule keeps the wheel whole and the subject doubled where it can; the tenors sing many free-voice bars without the organ. A second keyboard (or a second organist) could take the tenor; the edition does not.
- **Viri at the end of Duobus.** Left out of the organ: no hand is free (canticle in the right hand, wheel in the left, the bass in the pedal). It is heard in Pendet.
- **One percussionist.** Where the track has more than two hands' worth, the part keeps the bass drum and the hammer (woodblock left to the organ's wheel), the cymbal roll then the timpani and temple block in the rent, and the bass drum roll at the stone. The preface lists what a second player could add.
- **Dynamics** for the instruments are read from the track's gains and filters only roughly (a table in the code). The choir has none, as in the published score.
- **The full score's layout** is LilyPond's own: one or two systems a page, empty staves hidden. The flip-flop sections mark the left hand's manual change every bar. A hand's staff changes clef only when a bar lies well inside the other clef, so some low notes stay on ledger lines.
- **The parts.** The percussion part writes four or more identical bars once, with repeat signs (counted every fourth); the full score and the MIDI write every bar. Page turns are not chosen: the long form's bells part turns in the middle of In unum, where two ringers can share the turn.
- **Registration** is a suggestion for a two-manual organ with a swell box; names (Gedackt, Principal, Subbass) are generic.
- The rules for which bells to cue (their first entrance and their return after the tomb) are typed in `cue_bars()`, not found: they are a judgment.
- It is typed for "On These Two Hang": the layer rules read this track's orbits and envelopes, and the preface names its sections. A per-piece config is the next step, with the package the other tools are moving into.

## The check

`check_edition.py` prints a line per check and exits 1 if any fails:

1. The choir: for each voice, every note (onset, pitch, length, in sixteenths) of LilyPond's MIDI against the published MIDI; every syllable at the same onset; the hyphens, parsed from the `.ly`, against the published lyric events.
2. The instruments against the engine: the wheel, note for note, on the left hand; the canticle and `viri` on the manuals; the pedal's fifth (joined, since the track strikes it each bar); the quake's E1 on the pedal's E at 16'; each `organ()` event of the track by voice (doubled, shortened at a bar line, or left to the choir); the Amen; that every organ note is a note of the track; the bells, exactly; each percussion layer's onsets on its instrument, and that every stroke falls on an onset of the track; the recorded voices dropped.
3. Bars and times: the MIDI's length and tempo; every section mark's bar and time, read from the `.ly`, against the track's `arrange(...)`; the spoken line at the bar where the track plays its recording.
5. Ranges of every staff, with the pedal's C2-G4 and the bells' sets.

Made 25 October 2026 by Claude, with Richard Verver. The edition it writes is dedicated to the public domain (CC0 1.0) on the site; the tool's terms are the repository's.
