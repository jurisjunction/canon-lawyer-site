// ============================================================
// SOAP, BY ITS CAUSES, THE CLUB FORM: the dub mix, on the floor
// A symposium, Bonaventure presiding · B mixolydian x peak-time techno
// 126 BPM · 132 bars · ~4:11, then it loops
// For Strudel (https://strudel.cc): paste, press play (Ctrl+Enter).
// Dedicated to the public domain (CC0 1.0).
//
// The club form of the dub mix (soap-by-its-causes.strudel.js, beside
// this file). The essay was given bones first and flesh after, and so
// is the track. Nothing in the skeleton is touched: the end is still
// declared before any sound, the code is still written in the order of
// the causes, every section keeps its name, its length and its place,
// the two parents are quoted as written and keep their hashes, and END
// is still tapped in Morse on the rim at the last. What changes is the
// room: a basement at two in the morning, a wall of speakers, a crowd
// that has not come to be told what soap is for and is going to find
// out anyway.
//   * The clock is a 909 four to the floor, clipped a little: kick on
//     every beat, claps on two and four, closed hats in sixteenths, an
//     open hat on the offbeat. It arrives at MICELLE and never after
//     leaves a section the dub mix had a beat in.
//   * The pump: a hand-made sidechain. Four times a bar the kick lands
//     and everything else ducks and comes back. The clock is never
//     ducked. The water makes room for the beat.
//   * The sub is retriggered in eighths, with a growl on the offbeats,
//     and the chords, which the dub mix struck on the offbeats through
//     an echo, are now a supersaw stab, still on the offbeats, still
//     through the echo, with an acid line under them: the skank's own
//     notes through a resonant filter that opens over sixteen bars.
//   * The drops are where the dub mix had its weight. MICELLE is the
//     first: eight bars of OPEN while the kick lands, then CLOSE and the
//     crowd. BETWEEN is the second: the parent's chant in fauxbourdon
//     on a supersaw, above, then above and below. ORDER is the last:
//     everything, and the bell. RAZOR is the breakdown: one note, no
//     clock, the floor holding its breath. FLOOR is the second
//     breakdown: a drop of oil, the kick gone, the echo spreading.
//   * The risers lean into every downbeat that matters; the roll under
//     them; a crash on the landing.
//   * The spoken lines are off by default (WORDS = 0): the floor does
//     not need them. Set WORDS = 1 and they come back, filtered and
//     ducked, in exactly the places the dub mix has them.
// "The end is the cause of causes" (Thomas Aquinas, De principiis
// naturae 4). It still is. It is just louder.
//
// PARENTS. As in the dub mix: this essay draws on "Whether the Cloud
// Makes Many Worlds" and "Brother Electron", so Thomas sings the first
// one's hook, "Viri Galilaei", and Francis sings the second one's
// canticle, now for Sister Water. Each quoted line keeps a short hash
// of the parent's original (sha256 of the quoted text, first 12 hex):
//   whether-the-cloud.strudel.js   VIRI       fd123dbc28e8
//   brother-electron.strudel.js    CANTICLE   2b82b56f32b5
// The family moves up by fifths; this one is in B, with the dub mix.
//
// TIMELINE (bar / time):
//   OPENING    1  0:00  water; the bell; 808 hats keeping time
//   KEYNOTE    9  0:15  the canticle three ways, over a pulse that
//                       is not yet a kick; the sub arrives alone
//   TABLES    25  0:46  presence, absence, degrees, on the clock
//                       without its kick; the riser
//   TRACE     33  1:01  fat and lye converge over the roll; the sweet
//                       principle let go; the crash
//   MICELLE   41  1:16  THE DROP: OPEN, then CLOSE; the whole prior
//                       to the part
//   FOUR      57  1:47  the four causes enter in order, the end first
//   JOINTS    65  2:02  the bad carver chops the beat; the good one
//                       cuts at the bar; the ladder
//   RAZOR     73  2:17  BREAKDOWN: one note, no clock
//   BETWEEN   77  2:25  THE SECOND DROP: Viri Galilaei above, then
//                       above and below, the floor between
//   FLOOR     93  2:55  the oil on the pond; the kick gone; the trough
//   ORDER    101  3:10  THE LAST DROP: everything in its order; the
//                       new song; the bell
//   LUNCH    121  3:48  wash your hands: END tapped on the rim over
//                       the last kicks; the water poured out
//   tail     129  4:04  the reverb, and nothing
// ============================================================

setcpm(126/4) // one cycle = one bar

// ---- the spoken lines (off unless WORDS = 1): the reader, the speakers, and the floor
samples('shabda/speech/en-GB/f:praised_be_you_my_lord_through_sister_water,useful_and_humble_and_precious_and_chaste,a_cause_in_the_whole,who_did_the_washing,o_sing_unto_the_lord_a_new_song')
samples('shabda/speech/en-GB/m:it_is_for_washing,nature_to_be_commanded_must_be_obeyed,a_new_body,the_whole_is_prior_to_the_part,for_the_sake_of_what,where_the_joint_is,not_without_necessity,between_two_intellects,the_end_is_the_cause_of_causes,as_smooth_as_a_looking_glass,not_a_sum_an_order,wash_your_hands')

// ============================================================
// ORBITS: 1 the clock · 2 bass, acid · 3 spoken word · 4 pads, stabs,
//         bells · 5 water, risers · 6 choir · 7 pluck · 8 echo
// Strudel plays soundfonts at 0.3 of their gain, so those are lifted.
// ============================================================

// ============================================================
// I. THE FINAL CAUSE: what the track is for
// ============================================================

// END. To clean. Declared before any sound, tapped on the rim at the
// last, over the last kicks. Every FOR below leads here.
// parents: none (it is intended; nothing in the track makes it)
const END = 'TO CLEAN'
const BEHIND = ['TO HEAL', 'TO HONOUR', 'TO WELCOME']

// ============================================================
// II. THE MATERIAL CAUSE: what it is made of
// ============================================================

// THE PUMP: the sidechain, by hand. Four times a bar the kick lands and
// everything that is not the clock ducks and comes back.
// parents: none (it is a room, not a sound)
// for: every drop
const DUCK = "[.34 .7 1 .86]*4"
const WORDS = 0 // 1 brings the spoken lines back, filtered and ducked

// THE WATER: pink noise through a filter that breathes; bubbles.
// parents: none (it is given)
// for: OPENING, KEYNOTE, FLOOR, LUNCH, and so END
const water = (g = .05) => s('pink').hpf(220)
  .lpf(sine.slow(3).range(600, 1900)).gain(perlin.slow(2).range(g * .5, g))
  .velocity(DUCK).pan(sine.slow(5).range(.3, .7)).room(.3).orbit(5)
const bubbles = (g = .07) => n(irand(8).segment(16)).scale('B5:mixolydian')
  .s('sine').attack(.001).decay(.05).sustain(0).degradeBy(.55)
  .gain(g).pan(rand).room(.4).orbit(5)

// THE BELL: the chair's.
// parents: none (it is struck)
// for: OPENING, ORDER
const bell = (g = .22) => note('b4').s('gm_tubular_bells')
  .gain(g * 3).velocity(DUCK).room(.7).roomsize(6).orbit(4)

// THE CLOCK: a 909 four to the floor, clipped; claps on two and four;
// hats in sixteenths; an open hat on the offbeat. Never ducked.
// parents: none (it only measures)
// for: MICELLE and every section after it that moves
const kick = s("bd*4").bank('RolandTR909').gain(.95).shape(.18).orbit(1)
const hats = stack(
  s("hh*16").bank('RolandTR909').gain("[.24 .1 .17 .1]*4").hpf(7000).orbit(1),
  s("[~ oh]*4").bank('RolandTR909').gain(.26).release(.07).hpf(5000).orbit(1),
)
const clap = s("~ cp ~ cp").bank('RolandTR909').gain(.5).room(.3).roomsize(2).orbit(1)
const drums = stack(kick, hats, clap)
// before the clock: 808 hats keeping time, and a pulse that is not yet a kick
const hats808 = s("hh*16").bank('RolandTR808').gain("[.18 .07 .13 .07]*4").hpf(8000).orbit(1)
const pulse = s("bd*4").bank('RolandTR909').lpf(300).gain(.45).orbit(1)
// the roll, the riser, the crash: the floor leaning into a downbeat
const roll = s("sd*16").bank('RolandTR909').gain(saw.range(.1, .5)).hpf(400).room(.3).orbit(1)
const riser = (b) => s('white').hpf(saw.slow(b).range(300, 5000)).lpf(9000)
  .gain(saw.slow(b).range(.015, .17)).room(.4).orbit(5)
const crash = s("cr ~ ~ ~").bank('RolandTR909').gain(.45).room(.4).roomsize(4).orbit(1)
// bar masks over an n-bar section: on these bars, or from this bar on
const onBars = (n, ...ks) => '<' + Array.from({ length: n }, (_, i) => (ks.includes(i + 1) ? 1 : 0)).join(' ') + '>'
const fromBar = (n, k) => '<' + Array.from({ length: n }, (_, i) => (i + 1 >= k ? 1 : 0)).join(' ') + '>'

// THE ECHO: the dub engineer's wash, a dotted eighth, fed back.
// parents: none (it is a room, not a sound)
// for: KEYNOTE, FLOOR, the stabs
const echo = (pat, fb = .55, wet = .5) => pat.delay(wet).delaytime(.357)
  .delayfeedback(fb).room(.5).roomsize(5)

// THE MORSE: the household's telegraph, as in the parents.
// parents: none (it is the household's)
// for: LUNCH, where it taps END
const CODE = { A: '.-', C: '-.-.', E: '.', L: '.-..', N: '-.', O: '---', T: '-' }
const morse = (text) => text.split(' ').map((word) =>
  word.split('').map((ch) =>
    CODE[ch].split('').map((sign) => (sign === '.' ? 'x' : 'x@3')).join(' ~ ')
  ).join(' ~@3 ')
).join(' ~@7 ') + ' ~@7'
const units = (talea) => talea.split(' ').reduce((k, t) => k + (t.includes('@') ? +t.split('@')[1] : 1), 0)
const telegraph = (text, sound) => {
  const talea = morse(text)
  return s(sound).struct(mini(talea)).slow(units(talea) / 16).bank('RolandTR909')
}

// THE VOICES: filtered, ducked, and off unless WORDS = 1
// parents: none (they are lent)
const vox = (p, g = 1.2) => s(p).hpf(300).lpf(5000).gain(g * WORDS).velocity(DUCK)
  .delay(.25).delaytime(.357).delayfeedback(.35).room(.25).orbit(3)

// ============================================================
// III. THE FORMAL CAUSE: what it is
// ============================================================

// THE MODE: B mixolydian, I bVII IV I: B A E B.
// parents: none (it is given)
// for: everything that sounds a pitch
const SCALE = 'B3:mixolydian'
const ROOTS = "<b1 a1 e2 b1>"
const CLOSE = "<[b3,d#4,f#4,a4] [a3,c#4,e4,g#4] [e3,g#3,b3,d#4] [b3,d#4,f#4,a4]>"
const OPEN = "<[b2,f#4,d#5] [a2,e4,c#5] [e2,b3,g#4] [b2,f#4,d#5]>"

// THE CANTICLE
// from brother-electron.strudel.js: Francis's canticle, four bars,
// quoted as written in A (sha256 2b82b56f32b5); sung a tone higher, in
// B, for Sister Water.
// parents: PARENTS, THE MODE
// for: KEYNOTE, FOUR, JOINTS, ORDER, LUNCH
const CANTICLE = 'a4 a4 b4 c#5@2 b4 a4@2 g4 a4 b4@2 a4@4 e5 d5 c#5 b4 c#5@2 b4 a4 g4@2 e4@2 a4@4'
const canticle = () => note(mini(CANTICLE)).slow(4).transpose(2)
// the recorder of the dub mix is now a pluck with the echo, and, on the
// drops, a lead: a saw with a square under it, through the filter
const pluck = (pat, g = .2) => pat.s('triangle').attack(.003).decay(.12).sustain(.1).release(.2)
  .gain(g * 2).velocity(DUCK).delay(.4).delaytime(.357).delayfeedback(.4).room(.4).pan(.6).orbit(7)
const lead = (pat, g = .16) => stack(pat.s('sawtooth'), pat.transpose(-12).s('square').gain(.6))
  .attack(.01).decay(.2).sustain(.5).release(.1).lpf(sine.slow(4).range(1200, 3600)).lpq(3)
  .shape(.15).gain(g).velocity(DUCK).delay(.3).delaytime(.357).delayfeedback(.35).room(.3).orbit(7)

// VIRI: the Ascension introit, from the eldest
// from whether-the-cloud.strudel.js: "Viri Galilaei", two bars,
// quoted as written in G (sha256 fd123dbc28e8)
const VIRI = 'g3@2 g3@2 g3 c4 b3 c4@2 d4 c4 e4 d4 d4@3'
const STEP = { g3: 0, a3: 1, b3: 2, c4: 3, d4: 4, e4: 5, f4: 6, g4: 7 }
const inMode = (phrase) => phrase.split(' ').map((t) => {
  const [p, d] = t.split('@'); return STEP[p] + (d ? '@' + d : '')
}).join(' ')
// FAUXBOURDON: the chant with a fourth and a sixth below it, on the
// choir and on a supersaw together, pumping.
// parents: PARENTS, THE MODE, THE PUMP
// for: BETWEEN, ORDER
const viriLine = (lift) => stack(...[0, -3, -5].map((under) =>
  n(mini(inMode(VIRI)).add(under + lift)).scale(SCALE))).slow(2)
const viri = (lift = 0, g = .26) => stack(
  viriLine(lift).s('gm_choir_aahs').attack(.05).release(.6).lpf(4200)
    .gain(g * 3).velocity(DUCK).room(.6).roomsize(5).orbit(6),
  viriLine(lift).s('supersaw').unison(4).detune(.18).attack(.3).release(1)
    .lpf(1800).gain(g * .5).velocity(DUCK).room(.5).orbit(4),
)

// THE SUB, THE GROWL, THE STAB AND THE ACID: the bass on the roots,
// retriggered in eighths, a growl on the offbeats; the chords as a
// supersaw stab on the offbeats through the echo; and under them the
// skank's own notes as an acid line, through a filter that opens over
// sixteen bars. OPEN spreads a chord over two octaves; CLOSE gathers
// it: tails in, heads out.
// parents: THE MODE, THE ECHO, THE PUMP
// for: MICELLE, and every section after it that moves
const sub = (roots = ROOTS, g = .55) => note(roots).struct("x*8").s('sine')
  .attack(.004).decay(.18).sustain(.7).release(.06).lpf(200).gain(g).velocity("[.55 1]*4").orbit(2)
const growl = (roots = ROOTS, g = .14) => note(roots).struct("[~ x]*4").s('sawtooth')
  .attack(.004).decay(.14).sustain(.15).release(.05).lpf(650).lpq(5).shape(.3).gain(g).orbit(2)
const stab = (chords = CLOSE, g = .09) => echo(note(chords).struct("[~ x]*2")
  .s('supersaw').unison(5).detune(.22).spread(.8).attack(.003).decay(.18).sustain(0)
  .lpf(sine.slow(16).range(700, 3200)).lpq(2).gain(g * 3).velocity(DUCK), .55, .45).orbit(4)
const acid = (cut = 2600, g = .08) => n("0 2 4 2 0 2 4 7").scale(SCALE).s('sawtooth')
  .attack(.003).decay(.14).sustain(.15).release(.05)
  .lpf(sine.slow(16).range(cut * .2, cut)).lpq(9).lpenv(3).lpd(.12).shape(.2).gain(g).pan(.4).orbit(2)
const bass = (roots = ROOTS) => stack(sub(roots), growl(roots))

// THE TABLES: Bacon's three, as one figure, on the clock without its
// kick. PRESENCE where the nature is found, ABSENCE the same steps
// turned inside out, DEGREES the presence growing louder.
// parents: THE CLOCK
// for: TABLES, and so (Roger Bacon says) END
const PRESENCE = 'x ~ ~ x ~ x ~ ~ x ~ x ~ ~ x ~ ~'
const ABSENCE = PRESENCE.split(' ').map((t) => (t === 'x' ? '~' : 'x')).join(' ')
const table = (fig, sound = 'hh') => s(sound).struct(mini(fig))
  .bank('RolandTR909').hpf(3000).gain(.3).orbit(1)

// FAT AND LYE: two lines a long way apart, converging on B: trace.
// parents: THE MODE
// for: TRACE
const fat = note(saw.slow(6).range(35, 59).segment(48)).s('sawtooth')
  .lpf(800).attack(.01).release(.08).gain(.1).velocity(DUCK).orbit(2)
const lye = note(isaw.slow(6).range(83, 59).segment(48)).s('square')
  .lpf(2600).attack(.01).release(.08).gain(.06).velocity(DUCK).orbit(2)
const emulsion = stack(note("[b3,f#4]").s('supersaw').unison(4).detune(.2), note('b3').s('square'))
  .lpf(1200).attack(.4).release(1).gain(.08).room(.4).orbit(2)
// THE SWEET PRINCIPLE: glycerine, let go. Celesta, rising, with the echo.
// parents: THE MODE
const sweet = echo(note("b5 d#6 f#6 b6 d#7 ~ ~ ~").s('gm_celesta')
  .release(.6).gain(.2 * 3), .5, .4).orbit(4)

// ============================================================
// IV. THE EFFICIENT CAUSE: what brings it about
// ============================================================

// the floor's groove, assembled once: the clock, the bass, the stab, the acid
const groove = (chords = CLOSE) => stack(drums, bass(), stab(chords), acid())

// I. OPENING. Water, the bell, and 808 hats keeping time in the dark.
// parents: THE WATER, THE BELL
// for: KEYNOTE
const secOPENING = arrange(
  [4, stack(water(.04), bubbles(.05).mask("<0 1 1 0>"), hats808.mask("<0 0 1 1>"))],
  [4, stack(water(.05), hats808, bell().struct("<x ~ ~ ~>"),
    note("<b1 ~ ~ ~>").s('sine').attack(.5).release(2).gain(.2).orbit(2))],
)

// II. KEYNOTE. The canticle three ways: on the pluck; sung by the water;
// through the echo, over a pulse that is not yet a kick. The sub
// arrives alone in the last four bars, as a promise.
// parents: THE CANTICLE, THE WATER, THE ECHO
// for: END (it is for washing)
const secKEYNOTE = arrange(
  [4, stack(water(.035), hats808, pluck(canticle(), .22),
    vox("<praised_be_you_my_lord_through_sister_water ~ ~ ~>"))],
  [4, stack(water(.03), hats808,
    canticle().s('sine').attack(.002).decay(.12).sustain(.2).release(.1)
      .gain(.12).room(.5).pan(sine.fast(2).range(.3, .7)).orbit(5),
    bubbles(.04))],
  [8, stack(water(.03), hats808, pulse,
    echo(pluck(canticle(), .22), .62, .55),
    sub(ROOTS, .4).mask(fromBar(8, 5)),
    vox("<useful_and_humble_and_precious_and_chaste ~ ~ ~ ~ ~ it_is_for_washing ~>"))],
)

// III. TABLES. Presence, absence, degrees, on the clock without its
// kick; then all three, and the riser climbs toward trace.
// parents: THE TABLES, THE CLOCK
// for: END
const secTABLES = arrange(
  [2, stack(table(PRESENCE), pulse, sub(ROOTS, .4),
    vox("<nature_to_be_commanded_must_be_obeyed ~>"))],
  [2, stack(table(ABSENCE, 'rim'), pulse, sub(ROOTS, .4))],
  [2, stack(table(PRESENCE).gain(saw.segment(16).range(.05, .45)), pulse, clap.gain(.3), sub(ROOTS, .45))],
  [2, stack(table(PRESENCE), table(ABSENCE, 'rim').gain(.2), pulse, clap.gain(.4), sub(ROOTS, .5), riser(2))],
)

// IV. TRACE. Fat and lye converge over the roll; they become one body;
// the sweet principle goes free; the crash.
// parents: FAT AND LYE, THE SWEET PRINCIPLE
// for: MICELLE (it makes the soap that gathers)
const secTRACE = arrange(
  [6, stack(fat, lye, hats808, pulse.mask(fromBar(6, 3)), riser(6), roll.mask(onBars(6, 5, 6)),
    vox("<~ ~ ~ ~ a_new_body ~>"))],
  [2, stack(emulsion, sweet, hats808, crash.mask(onBars(2, 1)))],
)

// V. MICELLE. THE DROP. Eight bars of OPEN, the chords over two
// octaves while the clock lands; then CLOSE, gathered, tails in and
// heads out, and the acid under it. "A cause in the whole."
// parents: THE GROOVE
// for: END (the micelle is what takes the grease into the water)
const secMICELLE = arrange(
  [8, stack(crash.mask(onBars(8, 1)), drums, bass(), stab(OPEN, .08), acid(1800, .06),
    vox("<~ ~ ~ ~ a_cause_in_the_whole ~ ~ ~>"))],
  [8, stack(groove(), bubbles(.03),
    vox("<the_whole_is_prior_to_the_part ~ ~ ~ ~ ~ ~ ~>"))],
)

// VI. FOUR. The four causes enter in their order, two bars apart: the
// end (the canticle, on the lead), the form (the stab), the matter (the
// bass), the maker (the clock), last, because it is moved by the rest.
// parents: THE CANTICLE, THE GROOVE
// for: END
const secFOUR = stack(
  lead(canticle(), .15),
  stab().mask("<0 0 1 1 1 1 1 1>"),
  bass().mask("<0 0 0 0 1 1 1 1>"),
  drums.mask("<0 0 0 0 0 0 1 1>"),
  hats808.mask("<1 1 1 1 1 1 0 0>"),
  vox("<for_the_sake_of_what ~ ~ ~ ~ ~ ~ ~>"),
)

// VII. JOINTS. The bad carver chops through the beats; the good one
// cuts at the bar; then the ladder, the canticle's first phrase on the
// lead climbing a step every half bar, and the riser to the breakdown.
// parents: THE GROOVE, THE CANTICLE
// for: END
const secJOINTS = arrange(
  [2, groove().mask("1 1 1 [1 0] 0 [0 1] 1 [1 0]")],
  [2, stack(groove().mask("<1 0>"), vox("<where_the_joint_is ~>"))],
  [4, stack(drums, bass(), acid(3200, .07),
    lead(note(mini('b4 b4 c#5 d#5@2 c#5 b4@2')).transpose("<[0 2] [4 5] [7 9] [10 12]>"), .15),
    riser(4).mask(fromBar(4, 2)), roll.mask(onBars(4, 4)))],
)

// VIII. RAZOR. BREAKDOWN. "Plurality is not to be posited without
// necessity." One note, struck once a bar, and its echo. No clock. The
// floor holds its breath.
// parents: THE ECHO, THE MODE
// for: BETWEEN (what is left is enough to start again)
const secRAZOR = stack(
  echo(note('b3').struct("x ~ ~ ~").s('sine').attack(.002).decay(.6).sustain(0).gain(.3), .5, .5).orbit(2),
  water(.02),
  riser(4).mask(fromBar(4, 3)), roll.mask(onBars(4, 4)),
  vox("<not_without_necessity ~ ~ ~>"),
)

// IX. BETWEEN. THE SECOND DROP. "A natural thing stands between two
// intellects." The parent's chant in fauxbourdon above the floor, on
// choir and supersaw, pumping; then above and below at once, an octave
// and more apart, the groove between them.
// parents: FAUXBOURDON, THE GROOVE
// for: ORDER
const secBETWEEN = arrange(
  [8, stack(crash.mask(onBars(8, 1)), groove(), viri(7, .24),
    vox("<between_two_intellects ~ ~ ~ ~ ~ ~ ~>"))],
  [8, stack(groove(), viri(7, .22), viri(-7, .2),
    vox("<the_end_is_the_cause_of_causes ~ ~ ~ ~ ~ ~ ~>"))],
)

// X. FLOOR. The second breakdown. A drop of oil on a pond: the kick
// gone, one drop and its echo spreading wider until it can spread no
// more. Then the tin trough on a balance, the hats back, the riser to
// the last drop.
// parents: THE WATER, THE ECHO, THE CLOCK
// for: ORDER
const secFLOOR = arrange(
  [4, stack(water(.03), hats808.gain(.5),
    note('b6').struct("<x ~ ~ ~>").s('sine').attack(.001).decay(.2).sustain(0).gain(.2)
      .delay(.7).delaytime(.238).delayfeedback(saw.slow(4).range(.35, .82))
      .pan(sine.fast(4).range(.1, .9)).room(.6).orbit(5),
    vox("<~ ~ ~ as_smooth_as_a_looking_glass>"))],
  [4, stack(sub(ROOTS, .45), hats, clap.gain(.35),
    s("rim*8").bank('RolandTR909').hpf(4000).gain(".18 .1 .14 .1").pan(.65).orbit(1),
    s('white').struct("<~ ~ ~ [x ~ x ~]>").attack(.05).decay(.35).sustain(0).lpf(3000).gain(.12).orbit(5),
    riser(4), roll.mask(onBars(4, 3, 4)),
    vox("<who_did_the_washing ~ ~ ~>"))],
)

// XI. ORDER. THE LAST DROP. Not a sum but an order: everything, in its
// order, the end above on the lead, the form, the matter, the maker;
// then the parent's chant and the bell, a new song made of old notes;
// and the last chord, held, over a stopped clock.
// parents: everything above but the tables and the trace
// for: LUNCH
const secORDER = arrange(
  [8, stack(crash.mask(onBars(8, 1)), groove(), lead(canticle(), .14),
    vox("<not_a_sum_an_order ~ ~ ~ ~ ~ ~ ~>"))],
  [8, stack(groove(), echo(pluck(canticle(), .18), .5, .4), viri(7, .22),
    bell(.14).struct("<x ~ x ~>"),
    vox("<~ ~ ~ ~ o_sing_unto_the_lord_a_new_song ~ ~ ~>"))],
  [4, stack(drums.mask("<1 1 1 0>"), bass().mask("<1 1 1 0>"), acid(3200, .07).mask("<1 1 1 0>"),
    viri(7, .24), stab(CLOSE, .1).mask("<1 1 1 0>"),
    note("<~ ~ ~ [b2,f#3,b3,d#4,f#4,b4]>").s('supersaw').unison(5).detune(.25)
      .attack(.05).release(3).lpf(2400).gain(.3).room(.7).roomsize(6).orbit(4),
    bell(.2).struct("<~ ~ ~ x>"), crash.mask(onBars(4, 4)))],
)

// XII. LUNCH. "Wash your hands." The water, the canticle on the pluck,
// and END tapped on the rim over the last kicks; then the bowl carried
// out and poured at the foot of a tree, the filter falling as it empties.
// parents: THE WATER, THE CANTICLE, THE MORSE, END
// for: END (here it is reached: in a basin, in someone's hands)
const secLUNCH = stack(arrange(
  [4, stack(water(.05), kick.gain(.7), hats808, pluck(canticle(), .2),
    vox("<wash_your_hands ~ ~ ~>"))],
  [4, stack(
    s('pink').hpf(150).lpf(saw.slow(4).range(2600, 200)).gain(isaw.slow(4).range(.08, 0)).room(.4).orbit(5),
    note("<b1 ~ ~ ~>").s('sine').attack(.2).release(3).gain(.2).orbit(2))],
), telegraph(END, 'rim').gain(.42).room(.3).pan(.6).orbit(1).mask("<1 1 1 1 [1 0] 0 0 0>"))

// ============================================================
// THE ARRANGEMENT: the player's
// ============================================================
arrange(
  [8,  secOPENING],
  [16, secKEYNOTE],
  [8,  secTABLES],
  [8,  secTRACE],
  [16, secMICELLE],
  [8,  secFOUR],
  [8,  secJOINTS],
  [4,  secRAZOR],
  [16, secBETWEEN],
  [8,  secFLOOR],
  [20, secORDER],
  [8,  secLUNCH],
  [4,  silence],
)
