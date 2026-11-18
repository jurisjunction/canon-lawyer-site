// ============================================================
// AD TE LEVAVI — the night watch (a draft)
// The First Sunday of Advent, Year B · F sharp mixolydian x plainchant
// 120 BPM · 80 bars · ~2:40, then it loops
// For Strudel (https://strudel.cc): paste, press play (Ctrl+Enter).
// Dedicated to the public domain (CC0 1.0).
//
// "Watch ye therefore: for ye know not when the master of the house
// cometh, at even, or at midnight, or at the cockcrowing, or in the
// morning" (Mark 13:35). The night has four watches, and the Mass of
// this Sunday has four chants. This track gives each watch its chant:
//   at even              the introit    Ad te levavi animam meam
//   at midnight          the gradual    Universi qui te exspectant
//   at the cockcrowing   the alleluia   Ostende nobis, Domine
//   in the morning       the communion  Dominus dabit benignitatem
// The responsorial psalm of Year B, Psalm 80, has no melody of its
// own, so it takes the introit's: half a verse on the eighth psalm
// tone, at the very end, as far as the mediant. "Turn us again, O
// God, and cause thy face to shine"; the other half, "and we shall be
// saved", is not sung.
//
// Two things happen at once, and they run opposite ways.
//
// The clocks go out. "The sun shall be darkened, and the moon shall
// not give her light, and the stars of heaven shall fall" (Mark
// 13:24-25). Those lights were made "for signs, and for seasons, and
// for days, and years" (Genesis 1:14): they are the measures. Here
// the sun is the kick, four to the bar; the moon is a small light
// every three beats, drifting against it; the stars are the hats.
// They go out in Mark's order: the sun at midnight, the moon at
// cockcrow, and through the cockcrow the stars fall.
//
// And the tenor is uncovered. From the ninth bar the whole introit is
// sung once at the bottom, in long notes, under everything. A motet's
// tenor is the voice that holds (tenere): the others stand on it. At
// first it can hardly be heard. As each clock goes out there is less
// in front of it, until at the rent nothing is. The order was there
// before the measures, and it is there after them.
// Chant is an order of notes with no clock laid on it.
//
// The same line at two scales: in the evening the introit is sung
// above its own tenor, four times as fast.
//
// The Mass begins on G and ends on D. The introit and the alleluia
// are in the eighth mode, whose final is G; the gradual and the
// communion are in the first, whose final is D, a fifth above. So the
// singing does not come home. The tenor reaches its final in the
// morning, and the communion stops a fifth above it, where the soul
// was lifted. The last thing sung is half a psalm verse. All four
// chants are written on the same seven notes; the alleluia's verse
// flattens one of them, once, and so does the Rorate, twice.
//
// What the track does not do. The rent is the Passion's, not the
// last day's: Mark shows the end early, in sign, when the veil is
// rent (15:38), and the four watches are that night's timetable. The
// master does not come back in these eighty bars. "Of that day and
// that hour knoweth no man" (13:32), so the track keeps no date for
// it: it loops, and the porter watches again.
//
// PARENTS. The tracks, like the essays, form a DAG, and a track
// carries its parents in its own material. The household's hook is
// the Ascension introit "Viri Galilaei": "this same Jesus ... shall
// so come in like manner as ye have seen him go" (Acts 1:11). Mark's
// master is "a man taking a far journey, who left his house", so the
// track opens with him leaving: the hook, once, going away.
// The cloud track also sings "Rorate caeli desuper, et nubes pluant
// justum" (Isaiah 45:8): drop down, ye heavens, and let the clouds
// rain the Just One. Isaiah's two cries frame Advent. This Sunday's
// reading asks God to rend the heavens; the last Sunday's introit
// asks them to drop down. So in the morning the Rorate comes from
// above while the communion, below, sings that the earth gives her
// fruit: heaven and earth open at once.
// Each quoted line keeps a short hash of the parent's original
// (sha256 of the quoted text, first 12 hex). The Rorate is written
// there in two halves, and each half is quoted:
//   whether-the-cloud.strudel.js   VIRI     fd123dbc28e8
//   whether-the-cloud.strudel.js   RORATE   1172fda2cfe0
//   whether-the-cloud.strudel.js   RORATE   fceb05a531d9
// The family moves up by fifths: the cloud in G, its children in D
// and A, the double fugue on E, the soap in B, and this one on F
// sharp. The chants stand below as they are written, on G and on D,
// and are sung a semitone down. From the parents it also takes the
// household's Morse, which taps Mark's last word.
//
// THE CHANTS, and where they are read from:
//   the introit      Graduale Romanum (1974), p. 15, from GregoBase
//                    (chant 7576), checked against a medieval reading
//                    in the Cantus Database
//   the gradual, the alleluia and the communion
//                    the Cantus Database (chants 638312, 644965 and
//                    638318), from a twelfth-century gradual, the
//                    communion's given as CH-P 18 (Porrentruy)
//   the Rorate       as the cloud track reads it (Isaiah 45:8, mode 1)
// On an eighth-note grid, as in the cloud track: a syllable on one
// note is two eighths, the notes of a neume one each.
//
// TIMELINE (bar / time):
//   HOUSE       1  0:00  the master leaves; the porter's bell; the
//                        clocks start: sun, moon, stars
//   EVENING     9  0:16  the tenor begins, underneath; the introit
//                        above it, the same line four times as fast
//   MIDNIGHT   25  0:48  the sun is darkened; the gradual, low:
//                        "let none that wait on thee be ashamed"
//   COCKCROW   41  1:20  the moon gives no light; the alleluia and
//                        "Shew us"; the stars begin to fall
//   RENT       57  1:52  from the top to the bottom; then the tenor,
//                        uncovered
//   MORNING    61  2:00  the communion: "our land shall yield her
//                        increase"; above it, from bar 66, the
//                        Rorate: "drop down, ye heavens"; the tenor
//                        comes home; the introit again, lifted; WATCH
//                        tapped out, then said
//   tail       77  2:32  the bell; half a verse of Psalm 80 on the
//                        introit's psalm tone
//
// The spoken lines come from Shabda's text-to-speech and load the
// first time they play. If they are slow, stop and play again.
// ============================================================

setcpm(120/4) // one cycle = one bar = two seconds

// ---- the spoken lines: Mark 13:31, 35-37; Psalm 80:3
samples('shabda/speech/en-GB/m:watch,at_even,at_midnight,at_the_cockcrowing,in_the_morning,ye_know_not_when_the_master_of_the_house_cometh,lest_coming_suddenly_he_find_you_sleeping,heaven_and_earth_shall_pass_away,but_my_words_shall_not_pass_away,turn_us_again_o_god_and_cause_thy_face_to_shine')

// ============================================================
// ORBITS: 1 the clocks and the Morse · 2 the tenor and the powers ·
//         3 the spoken lines · 4 the chants · 5 the rent · 6 bells
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

// ROOT 2. THE WORD: Mark's last, "And what I say unto you I say unto
// all, Watch" (13:37).
// parents: none
// for: HOUSE, where it is tapped out; MORNING, where it is tapped
//      and then said
const WORD = 'WATCH'

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

// ---------------- THE CHANTS

// THE INTROIT, mode VIII, the whole antiphon, one note after another:
// 116 notes. This is the tenor.
// parents: THE ORDER
// for: every section from EVENING on; RENT, where it is uncovered
const TENOR = 'g3 d3 f3 g3 a3 a3 g3 g3 c4 c4 a3 g3 a3 f3 g3 g3 a3 g3 g3 f3 a3 c4 c4 c4 c4 d4 c4 c4 d4 f3 g3 g3 f3 f3 a3 c4 b3 b3 a3 c4 c4 c4 a3 g3 g3 a3 f3 g3 g3 a3 g3 g3 c4 c4 c4 c4 c4 a3 b3 a3 a3 c4 d4 c4 b3 a3 c4 c4 c4 g3 g3 g3 g3 a3 b3 c4 c4 a3 a3 f3 f3 f3 a3 a3 g3 g3 g3 g3 g3 b3 a3 b3 g3 g3 g3 a3 c4 b3 b3 c4 d4 c4 a3 b3 a3 g3 a3 a3 a3 f3 a3 g3 g3 a3 g3 g3'
// "Ad te levavi animam meam": four bars
const AD_TE = 'g3 d3 f3@2 g3 a3 a3@2 g3@2 g3 c4 c4 a3@2 g3 a3 f3 g3 g3 a3 g3 g3 f3@2 ~@7'
// "Deus meus, in te confido, non erubescam": five bars
const DEUS_MEUS = 'a3@2 c4 c4 c4 c4 d4 c4 c4 d4 f3 g3 g3@2 f3@2 f3 a3 c4 b3 b3 a3 c4 c4 c4 a3 g3 g3 a3 f3 g3 g3 a3 g3 g3@3 ~@3'

// THE PSALM TONE, the eighth, as the introit's own verse has it
// ("Vias tuas, Domine, demonstra mihi"), as far as the mediant: three
// bars
// parents: THE ORDER
// for: the tail, where it carries Psalm 80
const TONE = 'g3@2 a3 g3 g3 c4 c4@2 c4@2 c4@2 c4 b3 c4 d4 d4@2 c4 d4 c4@3 ~'

// THE GRADUAL, mode I: "Universi qui te exspectant non confundentur,
// Domine": eleven bars
// parents: THE ORDER
// for: MIDNIGHT
const UNIVERSI = 'c3@2 d3@2 d3 f3 g3 f3 d3 e3 c3 a2 c3 d3 c3 d3 d3@3 ~@5 d3 c3 f3@2 g3 a3 a3@2 a3 g3 a3 e3@2 ~@3 f3 g3 g3 f3 g3@2 f3 e3 c3 d3@2 ~@5 f3 g3 e3 f3 g3 f3 g3 f3 e3 e3 d3 d3 e3 d3 d3 c3 d3 f3 f3 g3 a3 b3 g3 e3 f3 g3 f3 g3 f3 e3 d3@2'

// THE ALLELUIA, mode VIII: its jubilus, five bars; and its verse as
// far as "Ostende nobis, Domine, misericordiam tuam", eight
// parents: THE ORDER
// for: COCKCROW
const ALLELUIA = 'f3 g3 a3 a3 g3 a3 c4 b3 a3 c4 c4 c4 d4 c4 a3 a3 g3 c4 c4 g3 a3 g3 f3 a3 c4 b3 g3 c4 a3 b3 a3 a3 g3@2 ~@6'
const OSTENDE = 'c4@2 c4 b3 d4 c4 c4@2 c4 c4 c4@3 ~@3 b3 c4 d4 c4 a3 c4 a3 b3 c4 c4@2 c4@3 ~@2 c4@2 c4@2 c4 a3 c4 e4 d4 c4@2 b3 c4 a3 g3 b3 c4 b3 g3 a3 bb3 a3 f3 a3 c4 a3 g3 a3 g3 g3@3'

// THE COMMUNION, mode I: "Dominus dabit benignitatem, et terra nostra
// dabit fructum suum": eleven bars
// parents: THE ORDER
// for: MORNING
const DOMINUS_DABIT = 'f3 f3 f3 a3 g3 g3 a3 f3 e3 f3 e3 d3 c3 d3 c3@2 f3 f3 f3 g3 f3 d3 f3@2 g3 a3 a3 c4 b3 d4 c4 a3 b3 b3 a3@2 ~@4 a3@2 g3 a3 g3 e3 f3 g3 a3 g3 g3@3 ~@3 a3 f3 a3 g3 a3 f3 e3 d3 d3 f3 d3 d3 c3 f3 g3 e3 d3 f3 g3 f3 e3 f3 d3 e3 d3 d3@3 ~@4'

// ---------------- THE MEASURES: the three clocks

// THE SUN: four to the bar.
// parents: none
// for: HOUSE, EVENING (it is darkened at MIDNIGHT)
const sun = s("bd*4").bank('RolandTR909').lpf(1800).gain(.75).orbit(1)

// THE MOON: a small light every three beats, so that it drifts
// against the sun and comes round with it every three bars.
// parents: none
// for: HOUSE, EVENING, MIDNIGHT (it gives no light at COCKCROW)
const moon = note("c#6 ~ ~").fast(4 / 3).s('sine').attack(.002).decay(.14).sustain(0)
  .gain(.16).pan(.35).room(.5).orbit(1)

// THE STARS: sixteenths, most of them missing, scattered left and
// right. A larger thin means fewer; a smaller fall means lower.
// parents: none
// for: HOUSE, EVENING, MIDNIGHT; COCKCROW, where they fall
const stars = (thin = .6, fall = 1) => s("hh*16").bank('RolandTR909').degradeBy(thin)
  .speed(fall).hpf(6500).gain(.17).pan(rand).orbit(1)

// THE POWERS: an open fifth held under everything, on the final.
// Shaken, it is struck sixteen times a bar, unevenly.
// parents: none
// for: every section; RENT, where they are shaken
const powers = (g = .06) => note("[f#2,c#3]").s('sawtooth').lpf(520)
  .attack(.4).release(1.2).gain(g).room(.4).orbit(2)
const shaken = (g = .1) => note("[f#2,c#3]*16").s('sawtooth').lpf(700)
  .attack(.01).release(.08).gain(perlin.range(.01, g)).room(.4).orbit(2)

// ---------------- THE VOICES

// THE TENOR: the introit in long notes, two to the bar, an octave
// down. It is cut to each section's length: from which note, for how
// many bars. Forward, it is doubled an octave up.
// parents: THE INTROIT
const NOTES = TENOR.split(' ')
const held = (from, bars) => note(mini(NOTES.slice(from, from + 2 * bars).join(' ')))
  .slow(bars).transpose(DOWN - 12)
const tenor = (from, bars, g = .3) => stack(
  held(from, bars).s('triangle').attack(.05).release(.3).gain(g),
  held(from, bars).s('gm_church_organ').release(.4).gain(g * .3),
).room(.35).orbit(2)
const tenorForward = (from, bars) => stack(
  tenor(from, bars, .4),
  held(from, bars).transpose(12).s('gm_church_organ').release(.5).gain(.2).room(.5).orbit(2),
)

// THE CHOIR, THE REEDS, THE PIPE: who sings each chant.
// parents: none (they are lent)
const choir = (p, g = .34) => p.s('gm_choir_aahs').attack(.05).release(.5)
  .gain(g).room(.6).roomsize(5).orbit(4)
const reeds = (p, g = .16) => p.s('gm_church_organ').lpf(1400).release(.4)
  .gain(g).room(.5).orbit(4)
const pipe = (p, g = .3) => p.s('gm_recorder').release(.3)
  .gain(g).room(.5).delay(.2).delaytime(.375).delayfeedback(.3).orbit(4)

// THE HEAVENS: the Rorate, set back down a fourth onto its own final,
// D, like the other chants, and sung an octave up, from above. It ends
// on the communion's final, an octave higher.
// parents: PARENTS (RORATE)
// for: MORNING
const heavens = (g = .2) => sing(RORATE).transpose(-5 + 12).s('gm_voice_oohs')
  .attack(.15).release(1).gain(g).room(.6).roomsize(6).pan(.4).orbit(6)

// THE BELL: the porter's.
// parents: none
const bell = (g = .22) => note('f#4').s('gm_tubular_bells').gain(g).room(.6).orbit(6)

// THE SPOKEN LINES
// parents: none (they are lent)
const vox = (p, g = 1.3) => s(p).hpf(150).lpf(8000).gain(g)
  .delay(.2).delaytime(.375).delayfeedback(.3).room(.25).orbit(3)

// THE MORSE: the household's telegraph, as in the parents: a dot a
// sixteenth, a dash three; one between signs, three between letters,
// seven between words.
// parents: none (it is the household's)
// for: HOUSE and MORNING, where it taps THE WORD
const CODE = { A: '.-', C: '-.-.', H: '....', T: '-', W: '.--' }
const morse = (text) => text.split(' ').map((word) =>
  word.split('').map((ch) =>
    CODE[ch].split('').map((sign) => (sign === '.' ? 'x' : 'x@3')).join(' ~ ')
  ).join(' ~@3 ')
).join(' ~@7 ') + ' ~@7'
const telegraph = (text, sound) => {
  const talea = morse(text)
  return s(sound).struct(mini(talea)).slow(units(talea) / 16).bank('RolandTR909')
}
// WATCH is 54 sixteenths, three bars and three eighths; in a slot of
// four bars it is tapped once and then stops
const watch = (g = .36) => telegraph(WORD, 'rim').gain(g).room(.3).pan(.62).orbit(1)
  .mask("<1 1 1 [1 1 1 0 0 0 0 0]>")

// THE RENT: noise, its ceiling falling from the top to the bottom
// over two bars (Mark 15:38).
// parents: none
// for: RENT
const rent = s("pink*16").lpf(isaw.slow(2).range(90, 14000)).hpf(60)
  .gain(.13).room(.5).orbit(5)

// ============================================================
// THE SECTIONS
// ============================================================

// I. HOUSE. "A man taking a far journey, who left his house ... and
// commanded the porter to watch" (Mark 13:34). The household's hook,
// "Viri Galilaei", once, going away; the bell; then the clocks, one
// at a time.
// parents: PARENTS (VIRI), THE BELL, THE POWERS, THE SUN, THE MOON,
//          THE STARS, THE MORSE
// for: EVENING
const secHOUSE = stack(powers(), arrange(
  [2, stack(bell().struct("<x ~>"),
    choir(sing(VIRI), .22).pan(.7).delay(.5).delaytime(.375).delayfeedback(.55))],
  [2, stack(sun, vox("<ye_know_not_when_the_master_of_the_house_cometh ~>"))],
  [2, stack(sun, moon)],
  [2, stack(sun, moon, stars())],
), arrange([4, silence], [4, watch(.28)]))

// II. EVENING. The tenor begins, under all three clocks. Above it
// the introit at chant speed: the same line at two scales.
// parents: THE TENOR, THE INTROIT, THE CHOIR, the three clocks
// for: RENT (what is covered here is uncovered there)
const secEVENING = stack(sun, moon, stars(), powers(), tenor(0, 16), arrange(
  [4, vox("<at_even ~ ~ ~>")],
  [4, choir(sing(AD_TE))],
  [5, choir(sing(DEUS_MEUS))],
  [3, silence],
))

// III. MIDNIGHT. "The sun shall be darkened": the kick is gone. "He
// cometh, and findeth them sleeping" (14:37). The gradual, low: "let
// none that wait on thee be ashamed" (Psalm 25:3), the introit's
// last words again, to a new melody in another mode.
// parents: THE TENOR, THE GRADUAL, THE REEDS, THE MOON, THE STARS
// for: MORNING
const secMIDNIGHT = stack(moon, stars(.7), powers(), tenor(32, 16), arrange(
  [2, vox("<at_midnight ~>")],
  [11, stack(reeds(sing(UNIVERSI)), choir(sing(UNIVERSI).transpose(12), .12))],
  [3, vox("<~ lest_coming_suddenly_he_find_you_sleeping ~>")],
))

// IV. COCKCROW. "And the moon shall not give her light." The
// alleluia's jubilus on a pipe, then its verse: "Shew us thy mercy,
// O LORD". Meanwhile the stars fall: fewer each bar, and lower.
// parents: THE TENOR, THE ALLELUIA, THE PIPE, THE CHOIR, THE STARS
// for: RENT
const secCOCKCROW = stack(
  stars("<.6 .6 .65 .65 .7 .7 .75 .8 .84 .88 .9 .92 .94 .96 .98 .99>",
    "<1 1 1 1 .95 .9 .85 .8 .75 .7 .65 .6 .55 .5 .45 .4>"),
  powers(), tenor(64, 16), arrange(
    [5, pipe(sing(ALLELUIA).transpose(12))],
    [1, vox("at_the_cockcrowing")],
    [8, stack(pipe(sing(OSTENDE).transpose(12), .26), choir(sing(OSTENDE), .16))],
    [2, vox("<heaven_and_earth_shall_pass_away ~>")],
  ))

// V. RENT. No clock is left. "The powers that are in heaven shall be
// shaken" (13:25), and the veil is rent "from the top to the bottom"
// (15:38); then the tenor over its drone and nothing else. It was
// there since the ninth bar.
// parents: THE RENT, THE POWERS, THE TENOR
// for: MORNING
const secRENT = stack(tenorForward(96, 4), arrange(
  [2, stack(rent, shaken())],
  [2, stack(powers(.05), vox("<but_my_words_shall_not_pass_away ~>"))],
))

// VI. MORNING. No measure: the communion is sung over the tenor's
// last notes, and when it says "terra", the ground answers. At the
// same bar the Rorate begins above it: "Truth shall spring out of the
// earth; and righteousness shall look down from heaven" (Psalm 85:11,
// the verse before the communion's). The tenor comes home to its
// final and the communion stops a fifth above it. Then the introit
// again, lifted: "Unto thee, O LORD, do I lift up my soul".
// And THE WORD, tapped out, and then said once.
// parents: THE TENOR, THE COMMUNION, THE INTROIT, THE CHOIR, THE BELL,
//          THE HEAVENS, THE MORSE, THE WORD
// for: THE WORD (here it is said); and the next loop
const secMORNING = stack(
  powers(.05),
  arrange([6, tenorForward(104, 6)], [10, silence]),
  arrange([1, vox("in_the_morning")], [15, silence]),
  // the ground, from "et terra nostra"
  arrange([5, silence], [11, note("f#1").s('sine').attack(1).release(2).gain(.24).orbit(2)]),
  // and from above, at the same bar: drop down, ye heavens
  arrange([5, silence], [8, heavens()], [3, silence]),
  arrange(
    [11, stack(choir(sing(DOMINUS_DABIT), .36), reeds(sing(DOMINUS_DABIT).transpose(-12), .08))],
    [4, stack(
      sing(AD_TE).transpose(24).s('gm_celesta').gain(.3).room(.6).orbit(6),
      choir(sing(AD_TE).transpose(12), .3))],
    [1, bell(.2).struct("x ~ ~ ~")],
  ),
  arrange([11, silence], [4, watch()], [1, silence]),
  // the key has tapped it; a voice says it once, in the empty bar
  arrange([14, silence], [1, vox("watch")], [1, silence]),
)

// VII. THE TAIL. The responsorial psalm, on the introit's own psalm
// tone. A verse has two halves and this is the first; then the track
// loops, as the antiphon is taken up again after its verse.
// parents: THE PSALM TONE, THE REEDS, THE BELL
// for: the next loop
const secTAIL = stack(
  bell(.14).struct("<x ~ ~ ~>"),
  arrange([3, reeds(sing(TONE), .15)], [1, silence]),
  vox("<turn_us_again_o_god_and_cause_thy_face_to_shine ~ ~ ~>", 1.1),
)

// ============================================================
// THE ARRANGEMENT: the player's
// ============================================================
arrange(
  [8,  secHOUSE],
  [16, secEVENING],
  [16, secMIDNIGHT],
  [16, secCOCKCROW],
  [4,  secRENT],
  [16, secMORNING],
  [4,  secTAIL],
)
