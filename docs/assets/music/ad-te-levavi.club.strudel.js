// ============================================================
// AD TE LEVAVI — the vigil mix
// The night watch, on the floor · F sharp mixolydian x melodic techno
// 128 BPM · 144 bars · ~4:30, then it loops
// For Strudel (https://strudel.cc): paste, press play (Ctrl+Enter).
// Dedicated to the public domain (CC0 1.0).
//
// "And what I say unto you I say unto all, Watch" (Mark 13:37). The
// Greek for "watch" means "stay awake". A dance floor at night is a
// room full of people who are not asleep, so this is the club mix of
// the night watch (ad-te-levavi.strudel.js, beside this file): the
// same Sunday, the same four watches, the same chants and the same
// parents, with a kick under them.
//   at even              the introit    Ad te levavi animam meam
//   at midnight          the gradual    Universi qui te exspectant
//   at the cockcrowing   the alleluia   Ostende nobis, Domine
//   in the morning       the communion  Dominus dabit benignitatem
//
// What changes on the floor:
//   * The tenor is the bass line. The whole introit, 116 notes, is
//     played once, one note to a bar, from bar 17 to bar 132. Every
//     bar of the groove stands on a note of the chant. The stabs
//     double it a fifth above (a fourth over B, where the fifth would
//     be a tritone). That is organum, the first harmony chant had.
//   * The hook is an isorhythm, as in the cloud track. Its rhythm is
//     WATCH in Morse, the household's telegraph. Its notes are the
//     first fourteen of the introit. So the hook says "watch" in the
//     notes of "Ad te levavi".
//   * The gradual is an acid line. It is sung at chant speed, in even
//     eighths, through a resonant filter, with no note changed.
//   * The clocks are the drums. The sun is the kick, four to the
//     floor; the moon is the small light every three beats, drifting
//     against it; the stars are the hats. The hands, a clap and an
//     open hat, work while it is day (John 9:4).
//   * The lights go out at the breakdown, in Mark's order (13:24-25):
//     the sun at cockcrow, then the moon, then the stars fall. With
//     no drums in front of it the tenor is heard bare, in long notes.
//   * A club build goes up. This one comes down: after the roll the
//     noise falls "from the top to the bottom" (Mark 15:38), and for
//     half a bar there is nothing.
//   * The drop is the morning. The sun comes up, the hook is wide
//     open, and in its second half the communion is sung over it,
//     with the Rorate from above at "et terra nostra".
//
// What the drop is not. It is the morning watch, not the last day:
// "The night is far spent, the day is at hand" (Romans 13:12). The
// master does not come back in these 144 bars. "Of that day and that
// hour knoweth no man" (Mark 13:32), so the track keeps no date for
// it. It loops, and the floor watches again.
//
// PARENTS. The tracks, like the essays, form a DAG, and a track
// carries its parents in its own material. From the cloud track: the
// Ascension introit "Viri Galilaei", which opens the track as the
// master going away (Acts 1:11; Mark 13:34); and "Rorate caeli"
// (Isaiah 45:8), which is written there in two halves, each quoted.
// Each quoted line keeps a short hash of the parent's original
// (sha256 of the quoted text, first 12 hex):
//   whether-the-cloud.strudel.js   VIRI     fd123dbc28e8
//   whether-the-cloud.strudel.js   RORATE   1172fda2cfe0
//   whether-the-cloud.strudel.js   RORATE   fceb05a531d9
// The family moves up by fifths: the cloud in G, its children in D
// and A, the double fugue on E, the soap in B, and this one on F
// sharp. The chants stand below as they are written, on G and on D,
// and are sung a semitone down. They are read from the same books as
// in the night watch, which names them.
//
// TIMELINE (bar / time):
//   HOUSE       1  0:00  kick and Morse key, to mix in on; the master
//                        leaves; the moon and the stars come out
//   EVENING    17  0:30  the tenor begins as the bass; the hook, its
//                        filter opening; at bar 33 the introit is
//                        sung over its own bass
//   MIDNIGHT   49  1:30  the gradual as an acid line; at bar 63 the
//                        floor nods off for two bars, and is woken
//   COCKCROW   81  2:30  the breakdown: sun, moon and stars go out;
//                        the tenor bare; the alleluia and "Shew us";
//                        from bar 97 the roll
//   RENT      103  3:11  from the top to the bottom; then nothing
//   MORNING   105  3:15  the drop: the hook wide open; from bar 121
//                        the communion over it, and from bar 126 the
//                        Rorate above; the tenor comes home at 132
//   tail      137  4:15  kick and key, to mix out on; half a verse of
//                        Psalm 80 on the introit's psalm tone
//
// The spoken lines come from Shabda's text-to-speech and load the
// first time they play. If they are slow, stop and play again.
// ============================================================

setcpm(128/4) // one cycle = one bar = 1.875 seconds

// ---- the spoken lines: Mark 13:31, 35-37; Psalm 80:3
samples('shabda/speech/en-GB/m:watch,at_even,at_midnight,at_the_cockcrowing,in_the_morning,ye_know_not_when_the_master_of_the_house_cometh,lest_coming_suddenly_he_find_you_sleeping,heaven_and_earth_shall_pass_away,but_my_words_shall_not_pass_away,turn_us_again_o_god_and_cause_thy_face_to_shine')

// ============================================================
// ORBITS: 1 the clocks, the hands and the key · 2 the tenor, as bass
//         and bare · 3 the spoken lines · 4 the chants · 5 the rent,
//         the riser, the ground · 6 bells and the heavens · 7 the
//         hook, the stabs and the pads
// ============================================================

// ---------------- ROOTS

// ROOT 1. THE ORDER: the notes, before any clock is laid on them.
// parents: none
// The household sings on F sharp; the chants are written on G.
const DOWN = -1
// how many eighths a line holds
const units = (line) => line.split(' ').reduce((k, t) => k + (t.includes('@') ? +t.split('@')[1] : 1), 0)
// a line sung at chant speed: as many bars as it has eighths, over eight
const sing = (line) => note(mini(line)).slow(units(line) / 8).transpose(DOWN)

// ROOT 2. THE WORD: Mark's last, "Watch" (13:37).
// parents: none
// for: THE KEY, which taps it, and THE HOOK, which sings in its rhythm
const WORD = 'WATCH'

// ROOT 3. THE PUMP: the sidechain, by hand, as in the household's
// other club form. Four times a bar the kick lands, and whatever is
// not the kick ducks and comes back.
// parents: none
const DUCK = "[.38 .72 1 .88]*4"
// a dotted eighth at this tempo, in seconds: the echo's length
const DOTTED = .3516
// bar masks over an n-bar section: on these bars
const onBars = (n, ...ks) => mini('<' + Array.from({ length: n }, (_, i) => (ks.includes(i + 1) ? 1 : 0)).join(' ') + '>')

// ---------------- PARENTS
// from whether-the-cloud.strudel.js: "Viri Galilaei", quoted as
// written (sha256 fd123dbc28e8)
const VIRI = 'g3@2 g3@2 g3 c4 b3 c4@2 d4 c4 e4 d4 d4@3'
// from whether-the-cloud.strudel.js: "Rorate caeli desuper, et nubes
// pluant justum", mode 1, which the cloud raised a fourth into G
// minor; quoted as written there, in its two halves (sha256
// 1172fda2cfe0 and fceb05a531d9). Eight bars.
const RORATE = 'bb3@3 c4 d4 d4@3 g4@4 f4@3 f4 eb4@2 d4@3 d4@3 c4@4 ~@4 ' +
               'd4@3 eb4@3 d4@3 c4 bb3 a3@3 bb3 a3 g3@8 ~@8'

// ---------------- THE CHANTS, as in the night watch

// THE INTROIT, mode VIII, the whole antiphon, one note after another:
// 116 notes. This is the tenor, and here the bass line.
// parents: THE ORDER
// for: THE TENOR, THE HOOK
const TENOR = 'g3 d3 f3 g3 a3 a3 g3 g3 c4 c4 a3 g3 a3 f3 g3 g3 a3 g3 g3 f3 a3 c4 c4 c4 c4 d4 c4 c4 d4 f3 g3 g3 f3 f3 a3 c4 b3 b3 a3 c4 c4 c4 a3 g3 g3 a3 f3 g3 g3 a3 g3 g3 c4 c4 c4 c4 c4 a3 b3 a3 a3 c4 d4 c4 b3 a3 c4 c4 c4 g3 g3 g3 g3 a3 b3 c4 c4 a3 a3 f3 f3 f3 a3 a3 g3 g3 g3 g3 g3 b3 a3 b3 g3 g3 g3 a3 c4 b3 b3 c4 d4 c4 a3 b3 a3 g3 a3 a3 a3 f3 a3 g3 g3 a3 g3 g3'
// "Ad te levavi animam meam": four bars
const AD_TE = 'g3 d3 f3@2 g3 a3 a3@2 g3@2 g3 c4 c4 a3@2 g3 a3 f3 g3 g3 a3 g3 g3 f3@2 ~@7'
// "Deus meus, in te confido, non erubescam": five bars
const DEUS_MEUS = 'a3@2 c4 c4 c4 c4 d4 c4 c4 d4 f3 g3 g3@2 f3@2 f3 a3 c4 b3 b3 a3 c4 c4 c4 a3 g3 g3 a3 f3 g3 g3 a3 g3 g3@3 ~@3'
// THE PSALM TONE, the eighth, as far as the mediant: three bars
const TONE = 'g3@2 a3 g3 g3 c4 c4@2 c4@2 c4@2 c4 b3 c4 d4 d4@2 c4 d4 c4@3 ~'
// THE GRADUAL, mode I: "Universi qui te exspectant non confundentur,
// Domine": eleven bars
const UNIVERSI = 'c3@2 d3@2 d3 f3 g3 f3 d3 e3 c3 a2 c3 d3 c3 d3 d3@3 ~@5 d3 c3 f3@2 g3 a3 a3@2 a3 g3 a3 e3@2 ~@3 f3 g3 g3 f3 g3@2 f3 e3 c3 d3@2 ~@5 f3 g3 e3 f3 g3 f3 g3 f3 e3 e3 d3 d3 e3 d3 d3 c3 d3 f3 f3 g3 a3 b3 g3 e3 f3 g3 f3 g3 f3 e3 d3@2'
// THE ALLELUIA, mode VIII: its jubilus, five bars; and its verse as
// far as "Ostende nobis, Domine, misericordiam tuam", eight
const ALLELUIA = 'f3 g3 a3 a3 g3 a3 c4 b3 a3 c4 c4 c4 d4 c4 a3 a3 g3 c4 c4 g3 a3 g3 f3 a3 c4 b3 g3 c4 a3 b3 a3 a3 g3@2 ~@6'
const OSTENDE = 'c4@2 c4 b3 d4 c4 c4@2 c4 c4 c4@3 ~@3 b3 c4 d4 c4 a3 c4 a3 b3 c4 c4@2 c4@3 ~@2 c4@2 c4@2 c4 a3 c4 e4 d4 c4@2 b3 c4 a3 g3 b3 c4 b3 g3 a3 bb3 a3 f3 a3 c4 a3 g3 a3 g3 g3@3'
// THE COMMUNION, mode I: "Dominus dabit benignitatem, et terra nostra
// dabit fructum suum": eleven bars
const DOMINUS_DABIT = 'f3 f3 f3 a3 g3 g3 a3 f3 e3 f3 e3 d3 c3 d3 c3@2 f3 f3 f3 g3 f3 d3 f3@2 g3 a3 a3 c4 b3 d4 c4 a3 b3 b3 a3@2 ~@4 a3@2 g3 a3 g3 e3 f3 g3 a3 g3 g3@3 ~@3 a3 f3 a3 g3 a3 f3 e3 d3 d3 f3 d3 d3 c3 f3 g3 e3 d3 f3 g3 f3 e3 f3 d3 e3 d3 d3@3 ~@4'

// ---------------- THE MEASURES: the three clocks, and the hands

// THE SUN: four to the floor.
// parents: none
// for: every section but COCKCROW and RENT, where it is darkened
const sun = s("bd*4").bank('RolandTR909').gain(.95).shape(.18).orbit(1)

// THE MOON: a small light every three beats, so that it drifts
// against the sun and comes round with it every three bars.
// parents: none
// for: HOUSE to the fourth bar of COCKCROW; MORNING
const moon = note("c#6 ~ ~").fast(4 / 3).s('sine').attack(.002).decay(.12).sustain(0)
  .gain(.2).pan(.35).delay(.35).delaytime(DOTTED).delayfeedback(.35).room(.4).orbit(6)

// THE STARS: closed hats in sixteenths. A larger thin means fewer; a
// smaller fall means lower.
// parents: none
// for: the groove; COCKCROW, where they fall
const stars = (thin = .02, fall = 1) => s("hh*16").bank('RolandTR909').degradeBy(thin)
  .speed(fall).gain("[.24 .1 .17 .1]*4").hpf(7000).pan(sine.fast(2).range(.4, .6)).orbit(1)

// THE HANDS: a clap on two and four and an open hat on the offbeat.
// "To every man his work" (Mark 13:34); they work while it is day.
// parents: none
// for: wherever the sun is, from the thirteenth bar
const hands = stack(
  s("~ cp ~ cp").bank('RolandTR909').gain(.5).room(.3).roomsize(2).orbit(1),
  s("[~ oh]*4").bank('RolandTR909').gain(.26).release(.07).hpf(5000).orbit(1),
)

// THE ROLL, THE RISER, THE CRASH: the floor leaning into a downbeat.
// parents: none
const roll = s("sd*16").bank('RolandTR909').gain(saw.range(.1, .5)).hpf(400).room(.3).orbit(1)
const riser = (b) => s("white*8").hpf(saw.slow(b).range(300, 5000)).lpf(9000)
  .gain(saw.slow(b).range(.015, .16)).room(.4).orbit(5)
const crash = s("cr ~ ~ ~").bank('RolandTR909').gain(.45).room(.4).roomsize(4).orbit(1)

// THE POWERS: an open fifth on the final, held under the quiet parts.
// Shaken, it is struck sixteen times a bar, unevenly.
// parents: none
// for: HOUSE, RENT, the tail
const powers = (g = .05) => note("[f#2,c#3]").s('sawtooth').lpf(520)
  .attack(.4).release(1.2).gain(g).room(.4).orbit(5)
const shaken = (g = .12) => note("[f#2,c#3]*16").s('sawtooth').lpf(700)
  .attack(.01).release(.08).gain(perlin.range(.01, g)).room(.4).orbit(5)

// ---------------- THE TENOR: the introit, one note to a bar

// The floor stands on it for 120 bars: its 116 notes, and its final
// held four bars more.
// parents: THE INTROIT
const NOTES = TENOR.split(' ')
const FLOOR = [...NOTES, 'g3', 'g3', 'g3', 'g3']
// a run of the floor as one note a bar: from which note, for how many
// bars; f rewrites each note (into a chord, or another octave)
const run = (from, bars, f = (x) => x) => mini('<' + FLOOR.slice(from, from + bars).map(f).join(' ') + '>')
const tenorLine = (from, bars) => note(run(from, bars)).transpose(DOWN - 12)

// AS BASS: a sawtooth rolling in sixteenths off the kick, and a sub on
// the offbeats an octave below (the two lowest notes stay up, where a
// room can still hear them).
// for: EVENING, MIDNIGHT, MORNING
const bass = (from, bars, cut = 700, g = .3) => stack(
  tenorLine(from, bars).struct("[~ x x x]*4").s('sawtooth')
    .attack(.004).decay(.11).sustain(.2).release(.04)
    .lpf(cut).lpq(6).lpenv(3).lpd(.1).shape(.25).gain(g),
  note(run(from, bars, (x) => (x === 'd3' ? 'd4' : x))).transpose(DOWN - 24).struct("[~ x]*4").s('sine')
    .attack(.004).decay(.18).sustain(.7).release(.06).lpf(200).gain(.55),
).orbit(2)

// BARE: in long notes, as the night watch has it, when no clock is
// left in front of it.
// for: COCKCROW, RENT
const bare = (p, g = .34) => stack(
  p.s('triangle').attack(.05).release(.3).gain(g),
  p.s('gm_church_organ').release(.4).gain(g * .4),
  p.transpose(12).s('gm_church_organ').release(.5).gain(.2),
).room(.4).orbit(2)

// ORGANUM: each note of the tenor with the fifth above it and the
// octave; over B, the fourth, since B's fifth is a tritone.
// parents: THE TENOR
const FIFTH = { d3: 'a3', f3: 'c4', g3: 'd4', a3: 'e4', b3: 'e4', c4: 'g4', d4: 'a4' }
const organum = (from, bars) => note(run(from, bars,
  (x) => '[' + x + ',' + FIFTH[x] + ',' + x[0] + (+x[1] + 1) + ']')).transpose(DOWN)
// as stabs on the offbeat
const stabs = (from, bars, g = .26) => organum(from, bars).struct("[~ x]*4")
  .s('supersaw').unison(5).detune(.2).spread(.8)
  .attack(.004).decay(.14).sustain(.1).release(.08).lpf(2600).lpenv(2).lpd(.12)
  .gain(g).room(.35).orbit(7)
// as a pad, held
const pad = (from, bars, cut = 1800, g = .22) => organum(from, bars)
  .s('supersaw').unison(5).detune(.22).spread(.8)
  .attack(.3).release(.6).lpf(cut).gain(g).room(.35).orbit(7)
// as a gate: the pad cut into sixteenths, pumping
const gate = (from, bars, g = .2) => organum(from, bars).struct("x*16")
  .s('supersaw').unison(5).detune(.22).spread(.8)
  .attack(.005).decay(.08).sustain(.6).release(.04)
  .lpf(sine.slow(8).range(1200, 3800)).gain(g).velocity(DUCK).room(.35).orbit(7)

// ---------------- THE MORSE: the household's telegraph, as in the
// parents: a dot a sixteenth, a dash three; one between signs, three
// between letters, seven between words.
// parents: none (it is the household's)
const CODE = { A: '.-', C: '-.-.', H: '....', T: '-', W: '.--' }
const morse = (text) => text.split(' ').map((word) =>
  word.split('').map((ch) =>
    CODE[ch].split('').map((sign) => (sign === '.' ? 'x' : 'x@3')).join(' ~ ')
  ).join(' ~@3 ')
).join(' ~@7 ') + ' ~@7'
// WATCH is 54 sixteenths; with ten more of rest it is four bars
const TALEA = morse(WORD) + ' ~@10'
// an isorhythm: the notes (the color) laid in turn on the rhythm (the
// talea), as in the cloud track
const iso = (talea, color) => { let i = 0; return talea.replace(/x/g, () => color[i++ % color.length]) }

// THE KEY: WATCH tapped on a rimshot, every four bars.
// parents: THE MORSE, THE WORD
// for: every section with a kick
const key = (g = .34) => s(mini(iso(TALEA, ['rim']))).slow(4).bank('RolandTR909')
  .gain(g).room(.3).pan(.62).orbit(1)

// THE HOOK: the first fourteen notes of the introit in the rhythm of
// WATCH, an octave up, with a dotted echo. cut is the filter.
// parents: THE MORSE, THE WORD, THE INTROIT
// for: EVENING, the end of MIDNIGHT, the roll, MORNING
const HOOK = iso(TALEA, NOTES.slice(0, 14))
const hook = (cut = 3600, g = .24) => note(mini(HOOK)).slow(4).transpose(DOWN + 12)
  .s('supersaw').unison(5).detune(.22).spread(.7)
  .attack(.004).decay(.16).sustain(.45).release(.12).lpf(cut).lpq(4)
  .gain(g).delay(.3).delaytime(DOTTED).delayfeedback(.4).room(.35).orbit(7)

// ---------------- THE VOICES

// THE CHOIR, THE REEDS, THE PIPE: who sings each chant. The choir
// pumps with the kick unless it is told the kick is gone.
// parents: none (they are lent)
const choir = (p, g = .34, pump = 1) => p.s('gm_choir_aahs').attack(.05).release(.5)
  .gain(g).velocity(pump ? DUCK : 1).room(.6).roomsize(5).orbit(4)
const reeds = (p, g = .16) => p.s('gm_church_organ').lpf(1400).release(.4)
  .gain(g).room(.6).orbit(4)
const pipe = (p, g = .3) => p.s('gm_recorder').release(.3)
  .gain(g).room(.6).delay(.3).delaytime(DOTTED).delayfeedback(.4).orbit(4)

// THE ACID: the gradual at chant speed through a resonant filter that
// opens and closes over eight bars. cut is how far it opens.
// parents: THE GRADUAL
// for: MIDNIGHT
const acid = (cut = 1200, g = .2) => sing(UNIVERSI).s('sawtooth')
  .attack(.003).decay(.14).sustain(.15).release(.05)
  .lpf(sine.slow(8).range(280, cut)).lpq(12).lpenv(3).lpd(.12).shape(.2)
  .gain(g).pan(.42).room(.6).orbit(4)

// THE HEAVENS: the Rorate, set back down a fourth onto its own final,
// D, like the other chants, and sung an octave up, from above.
// parents: PARENTS (RORATE)
// for: MORNING
const heavens = (g = .24) => stack(
  sing(RORATE).transpose(-5 + 12).s('gm_voice_oohs').attack(.15).release(1).gain(g),
  sing(RORATE).transpose(-5 + 24).s('gm_celesta').release(1).gain(g * .8),
).room(.6).roomsize(6).pan(.4).orbit(6)

// THE BELL: the porter's.
// parents: none
const bell = (g = .22) => note('f#4').s('gm_tubular_bells').gain(g).room(.6).orbit(6)

// THE GROUND: one deep hit, when the communion says "terra".
// parents: none
const ground = s("bd ~ ~ ~").bank('RolandTR909').speed(.4).lpf(200).gain(.9).orbit(5)

// THE SPOKEN LINES
// parents: none (they are lent)
const vox = (p, g = 1.3) => s(p).hpf(150).lpf(8000).gain(g)
  .delay(.2).delaytime(DOTTED).delayfeedback(.3).room(.25).orbit(3)

// THE RENT: noise, its ceiling falling from the top to the bottom
// over a bar and a half; then half a bar of nothing.
// parents: none
// for: RENT
const rent = s("pink*16").lpf(isaw.slow(1.5).range(90, 14000)).hpf(60)
  .gain(.2).room(.5).orbit(5)

// ============================================================
// THE SECTIONS
// ============================================================

// I. HOUSE. "A man taking a far journey, who left his house ... and
// commanded the porter to watch" (Mark 13:34). Sixteen bars to mix in
// on: the kick, muffled, and the key. The household's hook, "Viri
// Galilaei", once, going away. Then the moon and the stars come out,
// and the hands start work.
// parents: PARENTS (VIRI), THE SUN, THE KEY, THE BELL, THE MOON, THE
//          STARS, THE HANDS, THE POWERS
// for: EVENING
const secHOUSE = stack(
  powers(), key(.3),
  arrange([8, sun.lpf(500)], [8, sun]),
  arrange([2, stack(bell().struct("<x ~>"),
    choir(sing(VIRI), .26, 0).pan(.7).delay(.5).delaytime(DOTTED).delayfeedback(.55))], [14, silence]),
  arrange([4, silence], [2, vox("<ye_know_not_when_the_master_of_the_house_cometh ~>")], [10, silence]),
  arrange([8, silence], [8, stack(moon, stars(.4), bell(.16).struct("<x ~!7>"))]),
  arrange([12, silence], [4, stack(hands, riser(4))]),
)

// II. EVENING. The tenor begins, as the bass, and will not stop until
// it comes home in the morning. Over it the hook, its filter opening for sixteen bars.
// Then the introit itself at chant speed over its own first notes:
// the same line at two speeds.
// parents: THE TENOR, THE HOOK, THE INTROIT, THE CHOIR, the clocks,
//          THE HANDS, THE KEY
// for: MIDNIGHT
const secEVENING = stack(
  sun, moon, stars(), hands, key(), bass(0, 32),
  crash.mask(onBars(32, 1, 17)),
  arrange([1, vox("at_even")], [31, silence]),
  arrange([8, silence], [24, stabs(8, 24)]),
  arrange(
    [16, hook(saw.slow(16).range(350, 3600))],
    [4, choir(sing(AD_TE), .4)],
    [5, choir(sing(DEUS_MEUS), .4)],
    [7, hook()],
  ),
  arrange([31, silence], [1, roll]),
)

// III. MIDNIGHT. The mode turns: the gradual is in the first, a fifth
// up, and darker. It is sung low, as an acid line: "let none that
// wait on thee be ashamed" (Psalm 25:3). At the fifteenth bar the
// floor nods off, kick and hands gone for two bars: "lest coming
// suddenly he find you sleeping" (Mark 13:36). The kick wakes it,
// and the gradual comes round again with its filter open.
// parents: THE TENOR, THE GRADUAL, THE ACID, THE CHOIR, THE HOOK, the
//          clocks
// for: COCKCROW
const secMIDNIGHT = stack(
  moon, stars(.12), key(.3), bass(32, 32, 460),
  arrange([14, stack(sun, hands)], [2, roll.mask("<0 1>")], [16, stack(sun, hands)]),
  crash.mask(onBars(32, 1, 17)),
  arrange([16, silence], [16, stabs(48, 16, .2)]),
  arrange(
    [2, vox("<at_midnight ~>")],
    [11, acid(1100)],
    [1, silence],
    [2, vox("<lest_coming_suddenly_he_find_you_sleeping ~>")],
    [11, stack(acid(3200, .22), choir(sing(UNIVERSI).transpose(12), .22))],
    [5, hook(saw.slow(5).range(3600, 500), .2)],
  ),
)

// IV. COCKCROW: the breakdown. "The sun shall be darkened, and the
// moon shall not give her light, and the stars of heaven shall fall"
// (Mark 13:24-25). The kick and the hands stop at the first bar; the
// moon at the fifth; the stars thin out and sink for sixteen. What is
// left is the tenor, bare, and its fifths. Over it the alleluia's
// jubilus on a pipe, and its verse: "Shew us thy mercy, O LORD". Then
// the roll: six bars, the hook coming up through the floor, and the
// word, faster and faster.
// parents: THE TENOR, ORGANUM, THE ALLELUIA, THE PIPE, THE CHOIR, THE
//          STARS, THE MOON, THE HOOK, THE ROLL
// for: RENT
const secCOCKCROW = stack(
  crash.mask(onBars(22, 1)),
  bare(tenorLine(64, 22)),
  arrange([4, moon], [18, silence]),
  arrange([16, stars("<.1 .15 .2 .3 .4 .5 .6 .7 .78 .84 .88 .92 .94 .96 .98 .99>",
    "<1 1 1 1 .95 .9 .85 .8 .75 .7 .65 .6 .55 .5 .45 .4>")], [6, silence]),
  arrange(
    [16, pad(64, 16, saw.slow(16).range(300, 1800))],
    [6, pad(80, 6, saw.slow(6).range(1800, 6000), .26)],
  ),
  arrange(
    [5, pipe(sing(ALLELUIA).transpose(12))],
    [1, vox("at_the_cockcrowing")],
    [8, stack(pipe(sing(OSTENDE).transpose(12), .26), choir(sing(OSTENDE), .22, 0))],
    [2, vox("<heaven_and_earth_shall_pass_away ~>")],
    [6, stack(
      s("sd*<4 4 8 8 16 16>").bank('RolandTR909').gain(saw.slow(6).range(.12, .5)).hpf(400).room(.3).orbit(1),
      riser(6),
      hook(saw.slow(6).range(300, 5000), .2),
      s("<watch watch watch*2 watch*2 watch*4 watch*8>").clip(1).hpf(300).gain(1.1).orbit(3),
    )],
  ),
)

// V. RENT. A build goes up; this comes down. Everything stops. "The
// powers that are in heaven shall be shaken" (13:25), and the noise
// falls "from the top to the bottom" (15:38) over the tenor, which
// has been there since the seventeenth bar. Then half a bar of
// nothing.
// parents: THE RENT, THE POWERS, THE TENOR
// for: MORNING
const secRENT = stack(
  stack(rent, shaken()).mask("<1 [1 0]>"),
  bare(tenorLine(86, 2).struct("<x [x ~]>"), .4),
  vox("<but_my_words_shall_not_pass_away ~>"),
)

// VI. MORNING: the drop. The sun comes up and the hands go back to
// work. The tenor is the bass again, the hook is wide open, and the
// fifths pump. From the seventeenth bar the communion is sung over
// all of it; when it says "terra" the ground answers, and at the same
// bar the Rorate begins above: "Truth shall spring out of the earth;
// and righteousness shall look down from heaven" (Psalm 85:11). The
// tenor comes home to its final at the twenty-eighth bar. Then the
// introit again, lifted. In the last bar everything stops, and the
// word the key has been tapping all night is said once.
// parents: THE TENOR, ORGANUM, THE HOOK, THE COMMUNION, THE INTROIT,
//          THE CHOIR, THE HEAVENS, THE GROUND, THE KEY, THE WORD
// for: THE WORD (here it is said); and the tail
const secMORNING = stack(
  stack(
    sun, moon, stars(), hands, key(.4),
    crash.mask(onBars(32, 1, 17, 22)),
    bass(88, 32, 950, .32),
    stabs(88, 32),
    gate(88, 32),
    arrange([1, vox("in_the_morning")], [31, silence]),
    arrange(
      [16, stack(hook(5200, .28), hook(5200, .1).transpose(12))],
      [11, stack(choir(sing(DOMINUS_DABIT), .44), choir(sing(DOMINUS_DABIT).transpose(12), .2))],
      [4, stack(
        hook(5200, .24),
        sing(AD_TE).transpose(24).s('gm_celesta').gain(.3).room(.6).orbit(6),
        choir(sing(AD_TE).transpose(12), .34))],
      [1, silence],
    ),
    // the ground, at "et terra nostra"; and from above, at the same bar
    arrange([21, silence], [8, stack(ground.mask("<1 0!7>"), heavens())], [3, silence]),
  ).mask("<1!31 0>"),
  arrange([31, silence], [1, stack(vox("watch"), bell(.2).struct("x ~ ~ ~"))]),
)

// VII. THE TAIL. Eight bars to mix out on: the kick and the key. The
// responsorial psalm on the introit's own psalm tone: "Turn us again,
// O God, and cause thy face to shine". A verse has two halves and
// this is the first; "and we shall be saved" is not sung. Then the
// track loops, and the floor watches again.
// parents: THE PSALM TONE, THE REEDS, THE BELL, THE SUN, THE KEY
// for: the next loop
const secTAIL = stack(
  sun, key(.3), powers(),
  arrange([4, stars(.3)], [4, silence]),
  bell(.14).struct("<x ~!7>"),
  arrange([3, reeds(sing(TONE), .2)], [5, silence]),
  arrange([1, vox("turn_us_again_o_god_and_cause_thy_face_to_shine", 1.1)], [7, silence]),
)

// ============================================================
// THE ARRANGEMENT: the player's
// ============================================================
arrange(
  [16, secHOUSE],
  [32, secEVENING],
  [32, secMIDNIGHT],
  [22, secCOCKCROW],
  [2,  secRENT],
  [32, secMORNING],
  [8,  secTAIL],
)
