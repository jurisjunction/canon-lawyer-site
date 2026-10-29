// ============================================================
// SOAP, BY ITS CAUSES — the dub mix
// A symposium, Bonaventure presiding · B mixolydian x dub techno
// 120 BPM · 132 bars · ~4:24, then it loops
// For Strudel (https://strudel.cc): paste, press play (Ctrl+Enter).
// Dedicated to the public domain (CC0 1.0).
//
// A dub mix takes a song apart. It strips out the singer, keeps the
// drums and the bass, and lets the other parts in and out through
// echo and reverb, which the engineers call washes. It is the method
// of parts, done to music, and it is a lovely one. This track is
// divided another way, into its causes, and the code says so: it is
// written in their order, the end first.
//   I.   THE FINAL CAUSE: what the track is for. It is declared
//        before any sound, and every part below names it as what
//        that part is FOR.
//   II.  THE MATERIAL CAUSE: what it is made of. The sounds, which
//        do not know what they will become.
//   III. THE FORMAL CAUSE: what it is. The mode and the tunes.
//   IV.  THE EFFICIENT CAUSE: what brings it about. The sections and
//        the arrangement, which are the player's: change them while
//        it plays.
// "The end is the cause of causes" (Thomas Aquinas, De principiis
// naturae 4). Each part also names its PARENTS, the parts it is made
// from, which always stand above it, except the end, which stands
// above everything and is made from nothing in the track.
//
// PARENTS. The tracks, like the essays, form a DAG, and a track
// carries its parents in its own material. This essay draws on
// "Whether the Cloud Makes Many Worlds" and "Brother Electron", so
// Thomas sings the first one's hook, the Ascension introit "Viri
// Galilaei", in fauxbourdon, between two choirs; and Francis sings
// the second one's canticle again, now for Sister Water. Each quoted
// line keeps a short hash of the parent's original (sha256 of the
// quoted text, first 12 hex):
//   whether-the-cloud.strudel.js   VIRI       fd123dbc28e8
//   brother-electron.strudel.js    CANTICLE   2b82b56f32b5
// The family moves up by fifths: the cloud in G, its children in D
// and A, the double fugue on E, and this one in B. From the parents
// it also takes the household's Morse, which taps the end at the end.
//
// TIMELINE (bar / time):
//   OPENING    1  0:00  water from a jug; the chair's bell
//   KEYNOTE    9  0:16  Francis's canticle three ways: for Sister
//                       Water, by her, and through the echo
//   TABLES    25  0:48  presence, absence and degrees: one figure,
//                       its rests, its loudness
//   TRACE     33  1:04  fat and lye, until they come together; the
//                       sweet principle let go
//   MICELLE   41  1:20  the drop: the chords gather, tails in and
//                       heads out; "the whole is prior to the part"
//   FOUR      57  1:52  the four causes enter in their order, the
//                       end first
//   JOINTS    65  2:08  a bad carver, a good one, and the ladder
//   RAZOR     73  2:24  not without necessity: one note
//   BETWEEN   77  2:32  Viri Galilaei in fauxbourdon, above; then
//                       above and below, the groove between
//   FLOOR     93  3:04  a teaspoon of oil on a pond; a tin trough;
//                       two washings
//   ORDER    101  3:20  everything, in its order: a new song
//   LUNCH    121  4:00  wash your hands; the end tapped out; the
//                       water poured where no one will walk on it
//   tail     129  4:16  the reverb, and nothing
//
// The spoken lines come from Shabda's text-to-speech and load the
// first time they play. If they are slow, stop and play again.
// ============================================================

setcpm(120/4) // one cycle = one bar = two seconds

// ---- the spoken lines: the reader, the speakers, and the floor
samples('shabda/speech/en-GB/f:praised_be_you_my_lord_through_sister_water,useful_and_humble_and_precious_and_chaste,a_cause_in_the_whole,who_did_the_washing,o_sing_unto_the_lord_a_new_song')
samples('shabda/speech/en-GB/m:it_is_for_washing,nature_to_be_commanded_must_be_obeyed,a_new_body,the_whole_is_prior_to_the_part,for_the_sake_of_what,where_the_joint_is,not_without_necessity,between_two_intellects,the_end_is_the_cause_of_causes,as_smooth_as_a_looking_glass,not_a_sum_an_order,wash_your_hands')

// ============================================================
// ORBITS: 1 drums · 2 bass and synths · 3 spoken word ·
//         4 bells and organ · 5 water · 6 choir · 7 recorder ·
//         8 the chords and their echo
// Strudel plays soundfonts at 0.3 of their gain, so the
// instruments are lifted (gain x 3) to sit with the drums.
// ============================================================

// ============================================================
// I. THE FINAL CAUSE: what the track is for
// ============================================================

// END. To clean: the first thing a child asks of soap, and the last
// thing this track says, tapped in Morse on the rim in LUNCH. Behind
// it, as Francis gives them, stand three more, each the end of the
// one before: to heal, to honour, to welcome. Every FOR below leads
// here.
// parents: none (it is intended; nothing in the track makes it)
const END = 'TO CLEAN'
const BEHIND = ['TO HEAL', 'TO HONOUR', 'TO WELCOME']

// ============================================================
// II. THE MATERIAL CAUSE: what it is made of
// ============================================================

// THE WATER: pink noise through a filter that opens and closes like
// a stream; and bubbles, short sines that rise and burst.
// parents: none (it is given)
// for: KEYNOTE, FLOOR, LUNCH, and so END
const water = (g = .05) => s('pink').hpf(220)
  .lpf(sine.slow(3).range(600, 1900)).gain(perlin.slow(2).range(g * .5, g))
  .pan(sine.slow(5).range(.3, .7)).room(.3).orbit(5)
const bubbles = (g = .07) => n(irand(8).segment(16)).scale('B5:mixolydian')
  .s('sine').attack(.001).decay(.05).sustain(0).degradeBy(.55)
  .gain(g).pan(rand).room(.4).orbit(5)

// THE BELL: the chair's, on the first beat of a bar.
// parents: none (it is struck)
// for: OPENING, ORDER
const bell = (g = .22) => note('b4').s('gm_tubular_bells')
  .gain(g * 3).room(.7).roomsize(6).orbit(4)

// THE DRUMS: a dub techno kit. The kick on every beat, soft at the
// top; the rimshot on two and four, thrown into the echo; the hats
// on the offbeats.
// parents: none (they only measure)
// for: MICELLE, and every section after it that moves
const kick = s("bd*4").bank('RolandTR909').lpf(1800).gain(.8).orbit(1)
const rim = s("~ rim ~ rim").bank('RolandTR909').gain(.32)
  .delay(.45).delaytime(.375).delayfeedback(.55).room(.3).orbit(1)
const hats = s("[~ hh]*4").bank('RolandTR909').hpf(6000)
  .gain(".2 .16 .2 .14").orbit(1)
const drums = stack(kick, rim, hats)

// THE ECHO: the dub engineer's wash, a dotted eighth (three
// sixteenths), fed back on itself. The place where a thing goes
// through.
// parents: none (it is a room, not a sound)
// for: KEYNOTE ("through"), FLOOR, and the chords
const echo = (pat, fb = .55, wet = .5) => pat.delay(wet).delaytime(.375)
  .delayfeedback(fb).room(.5).roomsize(5)

// THE MORSE: the household's telegraph, as in the parents: a dot a
// sixteenth, a dash three; one between signs, three between
// letters, seven between words.
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

// THE VOICES
// parents: none (they are lent)
const vox = (p, g = 1.4) => s(p).hpf(150).lpf(8000).gain(g)
  .delay(.25).delaytime(.375).delayfeedback(.35).room(.25).orbit(3)

// ============================================================
// III. THE FORMAL CAUSE: what it is
// ============================================================

// THE MODE: B mixolydian, I bVII IV I: B A E B. The household's mode,
// the chant's own (mode VII), a fifth above Brother Electron.
// parents: none (it is given)
// for: everything that sounds a pitch
const SCALE = 'B3:mixolydian'
const ROOTS = "<b1 a1 e2 b1>"
const CLOSE = "<[b3,d#4,f#4,a4] [a3,c#4,e4,g#4] [e3,g#3,b3,d#4] [b3,d#4,f#4,a4]>"
const OPEN = "<[b2,f#4,d#5] [a2,e4,c#5] [e2,b3,g#4] [b2,f#4,d#5]>"

// THE CANTICLE
// from brother-electron.strudel.js: Francis's canticle, four bars,
// quoted as written in A (sha256 2b82b56f32b5). It is sung here a
// tone higher, in B, and now for Sister Water: "Laudato si', mi'
// Signore, per sor'aqua."
// parents: PARENTS, THE MODE
// for: KEYNOTE, FOUR (where the end enters first), ORDER, LUNCH
const CANTICLE = 'a4 a4 b4 c#5@2 b4 a4@2 g4 a4 b4@2 a4@4 e5 d5 c#5 b4 c#5@2 b4 a4 g4@2 e4@2 a4@4'
const canticle = () => note(mini(CANTICLE)).slow(4).transpose(2)
const recorder = (pat, g = .3) => pat.s('gm_recorder').release(.3)
  .gain(g * 3).room(.4).pan(.45).orbit(7)

// VIRI: the Ascension introit, from the eldest
// from whether-the-cloud.strudel.js: "Viri Galilaei", two bars,
// quoted as written in G (sha256 fd123dbc28e8)
const VIRI = 'g3@2 g3@2 g3 c4 b3 c4@2 d4 c4 e4 d4 d4@3'
// the chant read as steps of its mode, so that it can be sung in B,
// and in three voices
const STEP = { g3: 0, a3: 1, b3: 2, c4: 3, d4: 4, e4: 5, f4: 6, g4: 7 }
const inMode = (phrase) => phrase.split(' ').map((t) => {
  const [p, d] = t.split('@'); return STEP[p] + (d ? '@' + d : '')
}).join(' ')
// FAUXBOURDON: the chant on top, a fourth and a sixth below it, as
// in Brother Electron's chariot.
// parents: PARENTS, THE MODE
// for: BETWEEN, ORDER
const viri = (lift = 0, g = .3) => stack(...[0, -3, -5].map((under) =>
  n(mini(inMode(VIRI)).add(under + lift)).scale(SCALE)))
  .slow(2).s('gm_choir_aahs').attack(.05).release(.6)
  .room(.6).roomsize(5).gain(g * 3).orbit(6)

// THE SUB AND THE SKANK: the bass on the roots, and the chords on the
// offbeats, through a filter that opens over sixteen bars and into
// the echo. OPEN spreads a chord over two octaves; CLOSE gathers it
// into one, the outer voices turned toward the middle: tails in,
// heads out, as soap molecules gather in water.
// parents: THE MODE, THE ECHO
// for: MICELLE, and every section after it that moves
const sub = (roots = ROOTS) => note(roots).struct("x ~ ~ x ~ ~ x ~")
  .s('sine').attack(.01).decay(.4).sustain(.5).release(.2).gain(.42).orbit(2)
const skank = (chords = CLOSE, g = .11) => echo(note(chords).struct("[~ x]*2")
  .s('sawtooth').attack(.003).decay(.18).sustain(0)
  .lpf(sine.slow(16).range(500, 2600)).lpq(6).gain(g), .6, .55).orbit(8)

// THE TABLES: Bacon's three, as one figure. PRESENCE is where the
// nature is found, ABSENCE where it is wanting (the same steps,
// turned inside out), DEGREES the presence growing louder.
// parents: THE DRUMS
// for: TABLES, and so (Roger Bacon says) END
const PRESENCE = 'x ~ ~ x ~ x ~ ~ x ~ x ~ ~ x ~ ~'
const ABSENCE = PRESENCE.split(' ').map((t) => (t === 'x' ? '~' : 'x')).join(' ')
const table = (fig, sound = 'hh') => s(sound).struct(mini(fig))
  .bank('RolandTR909').hpf(3000).gain(.3).orbit(1)

// FAT AND LYE: two lines a long way apart, one climbing and one
// falling, until they meet on the same B and emulsify: trace.
// parents: THE MODE
// for: TRACE
const fat = note(saw.slow(6).range(35, 59).segment(48)).s('sawtooth')
  .lpf(800).attack(.01).release(.08).gain(.08).orbit(2)
const lye = note(isaw.slow(6).range(83, 59).segment(48)).s('square')
  .lpf(2600).attack(.01).release(.08).gain(.05).orbit(2)
const emulsion = stack(note("[b3,f#4]").s('sawtooth'), note('b3').s('square'))
  .lpf(1200).attack(.4).release(1).gain(.06).room(.4).orbit(2)
// THE SWEET PRINCIPLE: glycerine, let go when the alkali takes the
// acids. Celesta, rising.
// parents: THE MODE
const sweet = note("b5 d#6 f#6 b6 d#7 ~ ~ ~").s('gm_celesta')
  .release(.6).gain(.2 * 3).room(.6).orbit(4)

// ============================================================
// IV. THE EFFICIENT CAUSE: what brings it about
// ============================================================

// I. OPENING. The jug, the glasses, the bell.
// parents: THE WATER, THE BELL
// for: KEYNOTE
const secOPENING = arrange(
  [4, stack(water(.04), bubbles(.05).mask("<0 1 1 0>"))],
  [4, stack(water(.05), bell().struct("<x ~ ~ ~>"),
    note("<b1 ~ ~ ~>").s('sine').attack(.5).release(2).gain(.2).orbit(2))],
)

// II. KEYNOTE. "Per sor'aqua": praised for her, by her, through
// her. The canticle plain on the recorder; then sung by the water
// itself, as bubbles; then through the echo, where a sound goes on
// after the one who made it.
// parents: THE CANTICLE, THE WATER, THE ECHO
// for: END (it is for washing)
const secKEYNOTE = arrange(
  [4, stack(water(.035), recorder(canticle(), .28),
    vox("<praised_be_you_my_lord_through_sister_water ~ ~ ~>"))],
  [4, stack(water(.03),
    canticle().s('sine').attack(.002).decay(.12).sustain(.2).release(.1)
      .gain(.12).room(.5).pan(sine.fast(2).range(.3, .7)).orbit(5),
    bubbles(.04))],
  [8, stack(water(.03),
    echo(recorder(canticle(), .26), .62, .55),
    note("<b1 a1 e2 b1>").s('sine').attack(.3).release(1).gain(.22).orbit(2),
    kick.gain(.5).mask("<0 0 0 0 1 1 1 1>"),
    vox("<useful_and_humble_and_precious_and_chaste ~ ~ ~ ~ ~ it_is_for_washing ~>"))],
)

// III. TABLES. Presence, absence, degrees, and the three at once;
// "Nature to be commanded must be obeyed."
// parents: THE TABLES, THE DRUMS
// for: END (they were sorted by it before they began)
const secTABLES = arrange(
  [2, stack(table(PRESENCE), kick.gain(.55),
    vox("<nature_to_be_commanded_must_be_obeyed ~>"))],
  [2, stack(table(ABSENCE, 'rim'), kick.gain(.55))],
  [2, stack(table(PRESENCE).gain(saw.segment(16).range(.05, .45)), kick.gain(.6))],
  [2, stack(table(PRESENCE), table(ABSENCE, 'rim').gain(.2), kick.gain(.65), sub().gain(.3))],
)

// IV. TRACE. Fat and lye come together and become a new body; the
// sweet principle goes free.
// parents: FAT AND LYE, THE SWEET PRINCIPLE, THE MODE
// for: MICELLE (it makes the soap that gathers)
const secTRACE = arrange(
  [6, stack(fat, lye, hats.gain(.12), vox("<~ ~ ~ ~ a_new_body ~>"))],
  [2, stack(emulsion, sweet, hats.gain(.14))],
)

// V. MICELLE. The drop. First the chords wide open, over two
// octaves, while the drums come in; then gathered, the outer voices
// turned inward. "A cause in the whole, and in no part of it."
// parents: THE SUB AND THE SKANK, THE DRUMS
// for: END (the micelle is what takes the grease into the water)
const secMICELLE = arrange(
  [8, stack(drums, sub(), skank(OPEN, .1),
    vox("<~ ~ ~ ~ a_cause_in_the_whole ~ ~ ~>"))],
  [8, stack(drums, sub(), skank(CLOSE),
    bubbles(.03),
    vox("<the_whole_is_prior_to_the_part ~ ~ ~ ~ ~ ~ ~>"))],
)

// VI. FOUR. The four causes enter in their order, two bars apart:
// the end (the canticle), the form (the chords), the matter (the
// sub), and the maker (the drums), which comes last because it is
// moved by the rest.
// parents: THE CANTICLE, THE SUB AND THE SKANK, THE DRUMS
// for: END
const secFOUR = stack(
  recorder(canticle(), .26),
  skank(CLOSE).mask("<0 0 1 1 1 1 1 1>"),
  sub().mask("<0 0 0 0 1 1 1 1>"),
  drums.mask("<0 0 0 0 0 0 1 1>"),
  vox("<for_the_sake_of_what ~ ~ ~ ~ ~ ~ ~>"),
)

// VII. JOINTS. A bad carver cuts through the middle of the beats; a
// good one at the joints, a bar at a time; then the canticle's first
// phrase climbs, a step every half bar: the ladder.
// parents: THE DRUMS, THE SUB AND THE SKANK, THE CANTICLE
// for: END
const groove = () => stack(drums, sub(), skank(CLOSE))
const secJOINTS = arrange(
  [2, groove().mask("1 1 1 [1 0] 0 [0 1] 1 [1 0]")],
  [2, stack(groove().mask("<1 0>"), vox("<where_the_joint_is ~>"))],
  [4, stack(drums, sub(),
    recorder(note(mini('b4 b4 c#5 d#5@2 c#5 b4@2')).transpose("<[0 2] [4 5] [7 9] [10 12]>"), .26))],
)

// VIII. RAZOR. "Plurality is not to be posited without necessity."
// One note, struck once a bar, and its echo.
// parents: THE ECHO, THE MODE
// for: BETWEEN (what is left is enough to start again)
const secRAZOR = stack(
  echo(note('b3').struct("x ~ ~ ~").s('sine').attack(.002).decay(.6).sustain(0)
    .gain(.3), .5, .5).orbit(2),
  vox("<not_without_necessity ~ ~ ~>"),
)

// IX. BETWEEN. "A natural thing stands between two intellects." The
// parent's chant above, then above and below at once, an octave and
// more apart, and the groove between them.
// parents: FAUXBOURDON, THE SUB AND THE SKANK, THE DRUMS
// for: ORDER
const secBETWEEN = arrange(
  [8, stack(groove(), viri(7, .26),
    vox("<between_two_intellects ~ ~ ~ ~ ~ ~ ~>"))],
  [8, stack(groove(), viri(7, .24), viri(-7, .22),
    vox("<the_end_is_the_cause_of_causes ~ ~ ~ ~ ~ ~ ~>"))],
)

// X. FLOOR. A teaspoon of oil on a pond: one drop, and its echo
// spreading wider and longer until it can spread no more, one
// molecule thick. Then a tin trough, measured on a balance; and a
// man who washed his hands twice.
// parents: THE WATER, THE ECHO, THE DRUMS
// for: ORDER
const secFLOOR = arrange(
  [4, stack(water(.03), kick.gain(.4),
    note('b6').struct("<x ~ ~ ~>").s('sine').attack(.001).decay(.2).sustain(0).gain(.2)
      .delay(.7).delaytime(.25).delayfeedback(saw.slow(4).range(.35, .82))
      .pan(sine.fast(4).range(.1, .9)).room(.6).orbit(5),
    vox("<~ ~ ~ as_smooth_as_a_looking_glass>"))],
  [4, stack(sub(), kick.gain(.6), hats,
    s("rim*8").bank('RolandTR909').hpf(4000).gain(".18 .1 .14 .1").pan(.65).orbit(1),
    s('white').struct("<~ ~ ~ [x ~ x ~]>").attack(.05).decay(.35).sustain(0)
      .lpf(3000).gain(.12).orbit(5),
    vox("<who_did_the_washing ~ ~ ~>"))],
)

// XI. ORDER. The chair sums up: not a sum but an order. Everything,
// in its order: the end above, the form, the matter, the maker; then
// the parent's chant and the bell, a new song made of old notes.
// parents: everything above but the tables and the trace
// for: LUNCH
const secORDER = arrange(
  [8, stack(groove(), recorder(canticle(), .24),
    vox("<not_a_sum_an_order ~ ~ ~ ~ ~ ~ ~>"))],
  [8, stack(groove(), echo(recorder(canticle(), .22), .5, .4), viri(7, .24),
    bell(.16).struct("<x ~ x ~>"),
    vox("<~ ~ ~ ~ o_sing_unto_the_lord_a_new_song ~ ~ ~>"))],
  [4, stack(kick.mask("<1 1 1 0>"), sub().mask("<1 1 1 0>"),
    viri(7, .26), skank(CLOSE, .12).mask("<1 1 1 0>"),
    note("<~ ~ ~ [b2,f#3,b3,d#4,f#4,b4]>").s('gm_church_organ')
      .attack(.05).release(3).gain(.1 * 3).room(.7).roomsize(6).orbit(4),
    bell(.2).struct("<~ ~ ~ x>"))],
)

// XII. LUNCH. "Wash your hands." The water again, the canticle alone,
// and END tapped on the rim, a little under five bars of it; then the bowl carried out and poured at
// the foot of a tree, the filter falling as it empties.
// parents: THE WATER, THE CANTICLE, THE MORSE, END
// for: END (here it is reached: in a basin, in someone's hands)
const secLUNCH = stack(arrange(
  [4, stack(water(.05), recorder(canticle(), .22),
    vox("<wash_your_hands ~ ~ ~>"))],
  [4, stack(
    s('pink').hpf(150).lpf(saw.slow(4).range(2600, 200)).gain(isaw.slow(4).range(.08, 0))
      .room(.4).orbit(5),
    note("<b1 ~ ~ ~>").s('sine').attack(.2).release(3).gain(.2).orbit(2))],
), telegraph(END, 'rim').gain(.38).room(.3).pan(.6).orbit(1).mask("<1 1 1 1 [1 0] 0 0 0>"))

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
