// ============================================================
// BROTHER ELECTRON — the clockwork mix
// In the register of Dante Alighieri · A mixolydian x motorik chip
// 120 BPM · 132 bars · ~4:24, then it loops
// For Strudel (https://strudel.cc): paste, press play (Ctrl+Enter).
// Dedicated to the public domain (CC0 1.0). For Althea.
//
// A pilgrim goes down into a chip and up again, and so does the
// track. A cursor blinks in the dark. The gates spell LAW in ASCII,
// eight bits a letter: a crossing is a note, a waiting a rest. A
// flip-flop holds its bit because each half keeps telling the other
// what it is; the memory is written back, row by row, before it
// fades; and under all of it a clock, a beat inside a beat inside a
// beat, a wheel in the middle of a wheel. At the bottom a tone falls
// for ever, every floor a ceiling, until Teilhard turns it round.
// Francis sings his canticle, and then the gates play it: praise
// PER Brother Electron. Elijah's chariot carries the parent's chant
// up in three voices, and a ring of twelve bells turns like the
// teachers in the Sun. Thomas strikes the top voice from a chord:
// God at the head of no column. Maximus had no tongue, so his
// workshop has no words: a note cut in half five times and joined
// again five times, while the carpenter's hammer taps. At the altar
// the memory stops rewriting itself and one chord is held, not
// struck again. At the end the threads are bound, and the laptop
// sleeps while its memory goes on writing itself back.
//
// The code is a DAG, like the essays. Each part names its PARENTS,
// the parts it is made from; they always stand above it. Some parts
// also name what they are FOR: a later part they foreshadow. The
// first kind of edge runs back, the second forward. A record with
// only the first is a library; with both, a family.
//
// PARENTS. The tracks, like the essays, form a DAG, and a track
// carries its parents in its own material. This essay draws on
// "Whether the Cloud Makes Many Worlds" and "What Is to Be Done?",
// so the chariot carries the first one's hook, Viri Galilaei, and
// the workshop taps the second one's hammer, IS NOT THIS THE
// CARPENTER. Each quoted line keeps a short hash of the parent's
// original (sha256 of the quoted text, first 12 hex):
//   whether-the-cloud.strudel.js   VIRI       fd123dbc28e8
//   what-is-to-be-done.strudel.js  CARPENTER  3b8716d43c19
// The family moves up by fifths: the cloud in G, its child in D,
// this one in A. From the cloud it also takes the isorhythm (a
// rhythm carrying a melody, one note per stroke) and the Morse.
//
// TIMELINE (bar / time):
//   WOOD       1  0:00  the dark wood of copper: a fan, a cursor
//   GATE       9  0:16  the gates spell LAW; the flip-flop latches;
//                       the refresh; at bar 25 the clock and the
//                       wheels; the dice
//   FLOOR     33  1:04  a tone falling for ever, every floor a
//                       ceiling; at bar 41 Teilhard turns it round
//   CANTICLE  49  1:36  Francis sings; at bar 57 the gates play it
//   SUN       65  2:08  the chariot: Viri Galilaei in fauxbourdon;
//                       at 73 the ring of twelve; at 81 the struck line
//   WORKSHOP  89  2:56  no words: cut five times, joined five times
//   ALTAR    101  3:20  everything; at bar 109 the refresh stops and
//                       one chord is held
//   VOLUME   117  3:52  the threads bound; the cursor's last blink
//                       lands on the last chord
//   SLEEP    129  4:16  the memory writes itself back in the dark
//
// The spoken lines come from Shabda's text-to-speech and load the
// first time they play. If they are slow, stop and play again.
// ============================================================

setcpm(120/4) // one cycle = one bar = two seconds

// ---- the spoken lines: the readings, and the dead
samples('shabda/speech/en-GB/f:brother_electron,law_reaches_all_the_way_down,as_it_were_a_wheel_in_the_middle_of_a_wheel,praised_be_you_my_lord_through_brother_fire,all_things_have_an_order_among_themselves,where_the_feeble_senses_fail,so_that_finally_god_may_be_all_in_all,the_love_that_moves_the_sun_and_the_other_stars')
samples('shabda/speech/en-GB/m:have_mercy_on_me,logic_memory_and_time,he_does_not_throw_dice,everything_is_climbing,nothing_was_added_to_the_wind_the_fire_or_the_cloth,not_there,it_held')

// ============================================================
// ORBITS: 1 drums and clock · 2 the chip (square, bass) ·
//         3 spoken word · 4 organ and bells · 5 the falling tone ·
//         6 choir · 7 recorder
// Strudel plays soundfonts at 0.3 of their gain, so the
// instruments are lifted (gain x 3) to sit with the drums.
// ============================================================

// ---------------- ROOTS: what everything is made of

// ROOT 1. THE MODE: A mixolydian, I bVII IV I, A G D A.
// parents: none (it is given)
const SCALE = 'A3:mixolydian'
const MIXO = "<[a2,e3,a3,c#4] [g2,d3,g3,b3] [d3,a3,d4,f#4] [a2,e3,a3,c#4]>"
const ROOTS = "<a1 g1 d2 a1>"

// ROOT 2. THE CANTICLE: Francis's tune, four bars on the eighth grid.
// "Laudato si', mi' Signore, per frate focu."
// parents: none (it is sung)
const HOOK = 'a4 a4 b4 c#5@2 b4 a4@2 g4 a4 b4@2 a4@4 e5 d5 c#5 b4 c#5@2 b4 a4 g4@2 e4@2 a4@4'
const hook = () => note(mini(HOOK)).slow(4)

// ---------------- PARENTS
// from whether-the-cloud.strudel.js: the Ascension introit, "Viri
// Galilaei", two bars, quoted as written in G (sha256 fd123dbc28e8)
const VIRI = 'g3@2 g3@2 g3 c4 b3 c4@2 d4 c4 e4 d4 d4@3'
// from what-is-to-be-done.strudel.js: the carpenter's hammer, quoted
// as written (sha256 3b8716d43c19)
const CARPENTER = 'IS NOT THIS THE CARPENTER'

// the chant read as steps of its mode (G mixolydian), so that it can
// be sung in A, a fifth above its child, and in three voices
const STEP = { g3: 0, a3: 1, b3: 2, c4: 3, d4: 4, e4: 5, f4: 6, g4: 7 }
const inMode = (phrase) => phrase.split(' ').map((t) => {
  const [p, d] = t.split('@'); return STEP[p] + (d ? '@' + d : '')
}).join(' ')
// FAUXBOURDON: the chant on top, a fourth and a sixth below it, as
// the choirs of the fifteenth century sang it. For a singer of chant
// and polyphony.
// parents: PARENTS, THE MODE
const viri = (lift = 0, g = .3) => stack(...[0, -3, -5].map((under) =>
  n(mini(inMode(VIRI)).add(under + lift)).scale(SCALE)))
  .slow(2).s('gm_choir_aahs').attack(.05).release(.6)
  .room(.6).roomsize(5).gain(g * 3).orbit(6)

// ---------------- THE TELEGRAPH: Morse, as in the parents
// dot 1 sixteenth, dash 3; 1 between signs, 3 between letters, 7 between words
const CODE = { A: '.-', C: '-.-.', E: '.', H: '....', I: '..', N: '-.', O: '---',
               P: '.--.', R: '.-.', S: '...', T: '-' }
const morse = (text) => text.split(' ').map((word) =>
  word.split('').map((ch) =>
    CODE[ch].split('').map((sign) => (sign === '.' ? 'x' : 'x@3')).join(' ~ ')
  ).join(' ~@3 ')
).join(' ~@7 ') + ' ~@7'
const units = (talea) => talea.split(' ').reduce((n, t) => n + (t.includes('@') ? +t.split('@')[1] : 1), 0)
const telegraph = (text, sound) => {
  const talea = morse(text)
  return s(sound).struct(mini(talea)).slow(units(talea) / 16).bank('RolandTR909')
}

// ---------------- THE DARK WOOD
// parents: THE MODE
const hum = s('pink').lpf(380).gain(.05).orbit(5)
const copper = note('a1').s('sawtooth').lpf(260).attack(2).release(2).gain(.06).orbit(2)
// THE CURSOR: a blink on the first and third beats.
// for: VOLUME (its last blink lands on the last chord)
const cursor = note('a6').struct("x ~ x ~").s('sine')
  .attack(.002).decay(.06).sustain(0).gain(.09).orbit(4)

// ---------------- THE GATES: crossings and waitings
// "LAW " in ASCII, eight bits a letter, an eighth note a bit:
// a 1 is a crossing (a note), a 0 a waiting (a rest). Four bars.
// The crossings carry an arpeggio, one note per stroke (isorhythm).
// parents: THE MODE
const bits = (text) => text.split('').map((c) => c.charCodeAt(0).toString(2).padStart(8, '0')).join('')
const LAW = bits('LAW ')
const GATES = LAW.split('').map((b) => (b === '1' ? 'x' : '~')).join(' ')
const iso = (talea, color) => { let i = 0; return talea.replace(/x/g, () => color[i++ % color.length]) }
const COLOR = ['a3', 'c#4', 'e4', 'a4', 'g4', 'e4', 'd4', 'b3']
const gates = (g = .14) => note(mini(iso(GATES, COLOR))).slow(4).s('square')
  .attack(.002).decay(.09).sustain(0).lpf(2600).gain(g).pan(.4).orbit(2)

// THE FLIP-FLOP: pushed once, it flips and stays, each half telling
// the other what it is.
// parents: THE GATES
const push = s("rim").bank('RolandTR909').gain(.5).orbit(1)
const flipflop = note("[a4 e5]*8").s('square').attack(.002).decay(.05).sustain(0)
  .lpf(1800).gain(.07).pan(.65).orbit(2)

// THE REFRESH: every row read and written back before it fades.
// A thirty-second at 120 BPM lasts 62.5 ms, near the 64 ms in which
// a memory chip refreshes every row.
// parents: THE GATES
// for: ALTAR (where it stops), SLEEP (where it goes on alone)
const refresh = (g = .05) => s("hh*32").bank('RolandTR909')
  .hpf(9000).lpf(saw.range(9000, 16000)).gain(g).orbit(1)

// ---------------- THE CLOCK: motorik, the beat that measures it out
// parents: none (it only measures; the wiring makes the order)
const kick = s("bd ~ ~ ~ bd ~ bd ~").bank('RolandTR909').gain(.85).orbit(1)
const snare = s("~ ~ sd ~ ~ ~ sd ~").bank('RolandTR909').gain(.55).room(.15).orbit(1)
const hats = s("hh*8").bank('RolandTR909').gain(".26 .14 .22 .14").hpf(5000).orbit(1)
const clock = stack(kick, snare, hats)
const bass = (roots = ROOTS) => note(roots).struct("x ~ x x ~ x x ~").s('square')
  .lpf(500).decay(.15).sustain(.3).gain(.16).orbit(2)
// THE WHEELS: a beat inside a beat inside a beat (Ezekiel 1:16).
// Three against sixteen inside four inside one.
// parents: THE CLOCK
const wheels = stack(
  s("{rim ~ ~}%16").bank('RolandTR909').gain(.22).pan(.7).orbit(1),
  note("a6*4").s('sine').attack(.001).decay(.04).sustain(0).gain(.05).orbit(4),
  note("a5").s('gm_tubular_bells').gain(.2 * 3).room(.5).orbit(4),
)

// THE DICE: tunnelling, "decided by nothing at all". Strudel's dice
// are loaded: rand is a hash of the time, so they fall the same way
// every time it plays.
// parents: THE GATES
const dice = note("e6*16").s('square').degradeBy(.8)
  .attack(.001).decay(.03).sustain(0).lpf(5000).gain(.06).pan(rand).orbit(2)

// ---------------- THE FALLING TONE: every floor a ceiling
// Six sines an octave apart slide together, the top fading out as
// the bottom fades in, so the fall never ends (a Shepard-Risset
// glissando), stepped in sixteenths: floors.
// parents: none (it is found at the bottom)
// for: FLOOR (where it turns round to climb)
const shepard = (dir, bars = 8) => stack(...[0, 1, 2, 3, 4, 5].map((k) =>
  (dir > 0 ? saw : isaw).slow(bars).add(k / 6).fmap((x) => x % 1).segment(16)
    .fmap((p) => ({ note: 33 + 72 * p, gain: .055 * Math.sin(Math.PI * p) ** 2 }))))
  .s('sine').release(.2).room(.4).orbit(5)

// ---------------- THE CHOIR, THE RECORDER, THE ORGAN
const recorder = (pat, g = .3) => pat.s('gm_recorder').release(.3)
  .gain(g * 3).delay(".25:.25:.3").room(.4).pan(.45).orbit(7)
const organ = (chords, g = .07) => note(chords).s('gm_church_organ')
  .attack(.05).release(.6).gain(g * 3).room(.5).roomsize(4).orbit(4)

// THE RING OF TWELVE: the teachers in the Sun, "like the numbers on
// a clock": twelve bells against sixteen steps.
// parents: THE MODE, THE WHEELS
const twelve = note("{a4 c#5 e5 a5 b5 c#6 e6 g6 e6 c#6 b5 e5}%16").s('gm_celesta')
  .release(.6).gain(.18 * 3).room(.6).pan(sine.slow(4).range(.25, .75)).orbit(4)

// THE STRUCK LINE: three voices, as on the pilgrim's hand; the top
// one is struck out. The two left are both creatures, under the one
// law in two ways: from within (a line that breathes) and from
// without (pulses that are told nothing).
// parents: THE MODE, THE CANTICLE, THE GATES
const above = note("<e4 d4 f#4 e4>").s('gm_church_organ').release(.5).gain(.07 * 3).orbit(4)
const fromWithin = recorder(note(mini(HOOK)).slow(8).transpose(-12), .26)
const fromWithout = n("0 2 4 7 4 2 0 2").scale(SCALE).fast(2).s('square')
  .attack(.002).decay(.07).sustain(0).lpf(2000).gain(.08).orbit(2)

// THE DIVISIONS: Maximus cuts the world in two, five times, and the
// one in the middle joins it again, five times.
// parents: THE GATES (cut), PARENTS (the hammer)
const DIVIDE = "<x x*2 x*4 x*8 x*16 x*32 x*32 x*16 x*8 x*4 x*2 x>"
const divisions = note("a3").struct(DIVIDE).s('gm_marimba')
  .release(.1).gain(.32 * 3).room(.3).orbit(4)
// TWO WILLS: two voices in parallel, never against each other,
// coming home together.
// parents: THE MODE
const WILL = '<~ ~ ~ ~ ~ ~ 4 5 4 2 1 0>'
const wills = stack(
  n(mini(WILL)).scale(SCALE).s('gm_recorder').release(1).gain(.24 * 3).orbit(7),
  n(mini(WILL).add(-5)).scale(SCALE).s('gm_church_organ').release(1).gain(.06 * 3).orbit(4),
)

// ---------------- VOICES
const vox = (p, g = 1.4) => s(p).hpf(150).lpf(8000).gain(g)
  .delay(".12:.25:.25").room(.2).orbit(3)

// ============================================================
// SECTIONS
// ============================================================

// I. WOOD. "Midway through the night of my life I found myself in a
// dark wood of copper." A fan, the copper, the cursor.
// parents: THE DARK WOOD
const secWOOD = stack(
  hum, copper, cursor,
  vox("<~ brother_electron ~ ~ ~ have_mercy_on_me ~ ~>"),
)

// II. GATE. The gate, the loop and the beat.
// parents: THE GATES, THE FLIP-FLOP, THE REFRESH, THE CLOCK, THE WHEELS, THE DICE
const secGATE = arrange(
  [8, stack(hum, cursor, gates(),
    vox("<law_reaches_all_the_way_down ~ ~ ~ ~ ~ ~ ~>"))],
  [8, stack(cursor, gates(), copper,
    push.mask("<1 0 0 0 0 0 0 0>").struct("x ~ ~ ~"),
    flipflop,
    refresh().mask("<0 0 0 0 1 1 1 1>"))],
  [8, stack(clock, bass(), gates(.12), flipflop.gain(.05), refresh(),
    wheels.mask("<1 1 1 1 1 1 0 0>"),
    dice.mask("<0 0 0 0 1 1 1 1>"),
    vox("<as_it_were_a_wheel_in_the_middle_of_a_wheel ~ ~ logic_memory_and_time ~ ~ he_does_not_throw_dice ~>"))],
)

// III. FLOOR. "Every time we found a floor, it turned out to be a
// ceiling." Then: "Don't stop at the bottom! Everything is climbing!"
// parents: THE FALLING TONE, THE CLOCK
const secFLOOR = arrange(
  [8, stack(shepard(-1),
    kick.mask("<1 1 1 1 0 0 0 0>"), refresh(.03).mask("<1 1 0 0 0 0 0 0>"))],
  [8, stack(shepard(1),
    hats.gain(.18).mask("<0 0 0 0 1 1 1 1>"), kick.mask("<0 0 0 0 0 0 1 1>"),
    vox("<everything_is_climbing ~ ~ ~ ~ ~ ~ ~>"))],
)

// IV. CANTICLE. Francis sings; then the gates play his tune: praise
// to you, my Lord, PER Brother Electron.
// parents: THE CANTICLE, THE GATES, THE CLOCK
const secCANTICLE = arrange(
  [8, stack(copper, cursor, gates(.08), recorder(hook()),
    organ("<[a3,e4] [g3,d4] [d3,a3] [a3,e4]>", .05),
    vox("<~ ~ ~ ~ praised_be_you_my_lord_through_brother_fire ~ ~ ~>"))],
  [8, stack(clock, bass(),
    hook().s('square').attack(.005).decay(.12).sustain(.4).release(.1)
      .lpf(3200).gain(.12).delay(".125:.25:.3").orbit(2),
    recorder(hook().transpose(-12), .14),
    vox("<brother_electron ~ ~ ~ ~ ~ ~ ~>"))],
)

// V. SUN. Carried up in Elijah's chariot, the parent's chant in three
// voices; the ring of twelve; the struck line.
// parents: PARENTS (FAUXBOURDON), THE RING OF TWELVE, THE STRUCK LINE
const secSUN = arrange(
  [8, stack(
    viri(0).mask("<1 1 1 1 0 0 0 0>"),
    viri(7, .28).mask("<0 0 0 0 1 1 1 1>"),
    s('white').lpf(saw.slow(8).range(300, 6000)).gain(saw.slow(8).range(.02, .09)).orbit(5),
    s("bd*4").bank('RolandTR909').gain(.7).orbit(1),
    vox("<nothing_was_added_to_the_wind_the_fire_or_the_cloth ~ ~ ~ ~ ~ ~ ~>"))],
  [8, stack(twelve, organ(MIXO, .05), bass().gain(.12),
    s("bd ~ ~ ~ ~ ~ ~ ~").bank('RolandTR909').gain(.8).orbit(1),
    s("~ ~ ~ ~ sd ~ ~ ~").bank('RolandTR909').gain(.5).room(.3).orbit(1),
    vox("<all_things_have_an_order_among_themselves ~ ~ ~ ~ ~ ~ ~>"))],
  [8, stack(
    above.mask("<1 1 0 0 0 0 0 0>"),
    organ("<[a3,c#4] [g3,b3] [d3,f#3] [a3,c#4]>", .06),
    fromWithin, fromWithout,
    s("bd ~ ~ ~ bd ~ ~ ~").bank('RolandTR909').gain(.75).orbit(1),
    vox("<~ not_there ~ ~ ~ ~ ~ ~>"))],
)

// VI. WORKSHOP. "The last voice had no tongue." No words: the world
// cut in half five times and joined five times, and the hammer.
// parents: THE DIVISIONS, TWO WILLS, PARENTS (CARPENTER)
const secWORKSHOP = stack(
  divisions,
  wills,
  telegraph(CARPENTER, 'rim').gain(.42).room(.2).pan(.35).orbit(1),
  note("<a1 a1 a1 a1 a1 a1 d2 d2 g1 g1 a1 a1>").s('square').lpf(400).attack(.3).release(.8).gain(.1).orbit(2),
)

// VII. ALTAR. "I, your priest, will make the whole world my altar."
// Everything above; then the refresh stops, and one chord is held:
// the one sacrifice made present, not written again.
// parents: everything above but the dice and the falling tone
const secALTAR = arrange(
  [8, stack(clock, bass(), refresh(), organ(MIXO, .07),
    hook().s('square').attack(.005).decay(.12).sustain(.4).lpf(3000).gain(.1).orbit(2),
    viri(7, .24),
    twelve.gain(.1 * 3),
    vox("<where_the_feeble_senses_fail ~ ~ ~ ~ ~ ~ ~>"))],
  [8, stack(
    note("[a2,e3,a3,c#4,e4]").s('gm_church_organ').attack(.4).release(3)
      .gain(.09 * 3).room(.6).roomsize(5).slow(8).orbit(4),
    recorder(hook(), .22).mask("<1 1 1 1 0 0 0 0>"),
    vox("<~ ~ ~ ~ so_that_finally_god_may_be_all_in_all ~ ~ ~>"))],
)

// VIII. VOLUME. "Bound by love into one volume." The threads that run
// back (the parents' lines) and the one that runs forward (the
// cursor, whose last blink is the last chord's downbeat).
// parents: PARENTS, THE CANTICLE, THE GATES, THE CURSOR
const STAB = "[a2,e3,a3,c#4,e4,a4]"
const secVOLUME = arrange(
  [8, stack(clock.mask("<1 1 1 1 1 1 0 0>"), bass(),
    viri(7, .26), recorder(hook(), .24), gates(.1),
    telegraph(CARPENTER, 'rim').gain(.3).hpf(1200).pan(.6).orbit(1),
    organ(MIXO, .06))],
  [4, stack(
    stack(
      note(STAB).s('gm_church_organ').attack(.01).release(4).gain(.1 * 3).room(.7).roomsize(6),
      note(STAB).s('gm_choir_aahs').attack(.05).release(4).gain(.22 * 3).room(.7).roomsize(6),
      note('a6').s('sine').attack(.002).decay(.06).sustain(0).gain(.09),
      s('cr').bank('RolandTR909').gain(.35).room(.5),
    ).slow(4).orbit(4),
    vox("<~ ~ it_held ~>"))],
)

// IX. SLEEP. "The memory went on writing itself back, row by row":
// moved, like the sun and the other stars, by love.
// parents: THE REFRESH
const secSLEEP = stack(
  s("hh*32").bank('RolandTR909').hpf(10000).gain("<.03 .022 .014 .007>").orbit(1),
  vox("<the_love_that_moves_the_sun_and_the_other_stars ~ ~ ~>", 1.3),
)

// ============================================================
// THE ARRANGEMENT
// ============================================================
arrange(
  [8,  secWOOD],
  [24, secGATE],
  [16, secFLOOR],
  [16, secCANTICLE],
  [24, secSUN],
  [12, secWORKSHOP],
  [16, secALTAR],
  [12, secVOLUME],
  [4,  secSLEEP],
)
