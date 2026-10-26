// ============================================================
// ON THESE TWO HANG, THE CLUB FORM IN THREE AND EIGHT: a double fugue,
// by rule, on the floor, with a Euclidean rhythm, E(3,8) rotated by one
// "On these two commandments hang all the law and the prophets"
// (Matthew 22:40) · mode III x the clock · 120 BPM, four to the floor
// 182 bars · ~6:04, then it loops
// For Strudel (https://strudel.cc): paste, press play (Ctrl+Enter).
// Dedicated to the public domain (CC0 1.0).
//
// The club form (on-these-two-hang.club.strudel.js, beside this file),
// with one rhythm added: three strokes spread as evenly as they can be
// over eight steps (Bjorklund's algorithm; Toussaint showed in 2005 it
// makes the tresillo and much of the world's dance rhythm), turned one
// step later, so that it reads . X . . X . . X: it starts after the
// beat, and its last stroke leans into the next bar. Three in eight:
// he rose on the third day, the first day of the week, which the
// Fathers call the eighth (Barnabas 15; Justin, Dialogue 41).
//   * In the clock: a 909 tom, in eighths, a bar to the figure. It is
//     part of the clock, so it enters, stutters and stops with it.
//   * In the bass: the growl takes the figure in sixteenths, twice a
//     bar (the rolling three-three-two), in place of the offbeats. The
//     sub is unchanged, and the growl's notes are still the bass
//     voice's, note for note.
//   * EUCLID, below, holds the figure; change it to try others
//     ('3,8,0' is the plain tresillo, '5,8,2' is busier). The first
//     number is the strokes, the second the steps, the third the turn.
//   * Everything is 3 dB lower than the club form (postgain .7, at the
//     bottom), because the club form's kick clips when rendered.
// Otherwise this is the club form as it stands, which is the long form
// (on-these-two-hang.long.strudel.js, beside this file) for the floor.
// Nothing in the counterpoint is touched: every voice of every section
// is quoted unchanged from the long form, where counterpoint.py made it
// and audited every half note. What changes is creation's sound. The
// same persons sing the same notes; the room is different.
//   * The clock, the saeculum, is now a 909 four to the floor: kick,
//     claps on two and four, closed hats in sixteenths, an open hat on
//     the offbeat. It still enters with the second exposition, three
//     bars into it, and it still stays, and it still stops on Golgotha.
//   * The wheel, the triad turned in even eighths, is now an acid line:
//     a sawtooth through a resonant filter that opens and closes over
//     eight bars. Before the Cross it still flip-flops with the bells,
//     bar by bar; after the stone they sound together.
//   * The bass voice of each section, wherever the rule put it, is also
//     sent down an octave to a sub, retriggered in eighths, and to a
//     growl on the offbeats. The bass line of the club track IS the
//     bass voice of the fugue. When the bass voice rests, so does the
//     sub, so the first exposition builds voice by voice, and the sub
//     arrives with the fourth entry.
//   * The organ that doubled the choir is now a supersaw pad, and pad
//     and choir pump: a hand-made sidechain ducks them on every beat.
//   * The bells, the tintinnabuli, now ring on a celesta and on a pluck
//     with a dotted-eighth echo.
//   * The chanted lines are off by default (WORDS = 0): Strudel has no
//     speech synthesis, and the groove carries the sections without
//     them. Set WORDS = 1 and the original recordings come back,
//     filtered and ducked, in exactly the places the long form has them.
//     To use a plain spoken voice instead, record the lines with any TTS,
//     host the wavs, and point VOICES at them with the same names.
//   * Builds and drops follow the form, not the other way round. The
//     first minute is beatless and climbs, the sub comes in alone for
//     three bars at SIMILE and the kick lands on the fourth. Golgotha is
//     the breakdown: the clock alone, then stuttering, then stopped; the
//     veil, the earthquake; one man, alone; and three bars of nothing.
//     The stone is the drop. The pumping never changes the structure:
//     the kick drops out nowhere that the clock did not already stop.
//
// The procedures of the fugue, as in the long form:
//   * CAPUT, the head. Both subjects begin with the same six notes,
//     mi mi re sol mi ut, because "Diliges Dominum" and "Diliges
//     proximum" have the same vowels. The episodes are made of that
//     head alone: two voices in imitation, a half note apart, falling
//     a step each bar. The leader sings the first commandment's words,
//     the follower the second's.
//   * SPECULUM, the mirror: "For now we see through a glass, darkly"
//     (1 Corinthians 13:12). Each subject turned upside down about mi,
//     the final, on the white keys, so E stays E, D and F change
//     places, and so do C and G. The words stay under the notes.
//   * LEX, the Law held: the first subject in the bass with every
//     value four times longer, a cantus firmus, and the second subject
//     and its mirror entering over it in their own values.
//   * IN UNUM, the stretto: "that also he should gather together in
//     one the children of God that were scattered abroad" (John
//     11:52). The entries overlap closer than in the expositions. The
//     distance and the levels were searched for the closest entries
//     whose given lines do not clash at all.
//   * DUOBUS, double counterpoint: both commandments at once, as in
//     the short form; then both in the mirror; then with the voices
//     exchanged, the second commandment below the first.
//   * FUNDAMENTUM, the pedal: "For other foundation can no man lay
//     than that is laid, which is Jesus Christ" (1 Corinthians 3:11).
//     The bass holds E, the final, while the others enter a bar apart.
//     On the floor that is eight bars of E in the sub, pumping.
// Golgotha and its three bars of rest are as in the short form. They
// are the centre, and they stand near the middle of the long form.
//
// The voices are persons and the instruments are creation, as in the
// short form; the clock, the saeculum, enters with the second
// exposition and stays. Before the Cross the bells and the clock's
// wheel take turns, bar by bar, a flip-flop; after the stone they
// sound together.
//
// The code is a DAG, like the essays. Each part names its PARENTS,
// the parts it is made from, which stand above it.
//
// PARENTS. Like the short form it quotes the household, each line
// with a short hash of the parent's original (sha256 of the quoted
// text, first 12 hex):
//   whether-the-cloud.strudel.js   VIRI       fd123dbc28e8
//   what-is-to-be-done.strudel.js  CARPENTER  3b8716d43c19
//   brother-electron.strudel.js    TRIPLUM    2b82b56f32b5
//   a-new-song.strudel.js          THINGS     ab645d0aae4c
//
// TIMELINE (bar / time):
//   PENDET        1  0:00  the household's law and prophets hang on a
//                          pedal; a drone, the canticle, the hammer
//   DILIGES       9  0:16  "Thou shalt love the Lord thy God": the first
//                          subject enters four times, alto, soprano, tenor,
//                          bass; the bells ring over it; the sub arrives
//                          with the bass; hats from the tenor's entry
//   CAPUT        25  0:48  the head both subjects share, in imitation,
//                          soprano and tenor, falling a step a bar; the
//                          riser and the roll
//   SIMILE       31  1:00  "The second is like unto it": the sub alone,
//                          three bars; the clock lands on the fourth; the
//                          bells and the acid flip-flop, bar by bar
//   CAPUT        43  1:24  the head again, alto and bass
//   SPECULUM     49  1:36  the mirror: the first subject upside down, the
//                          voices' order mirrored too; then the second,
//                          upside down, from the top
//   LEX          77  2:32  the Law held: the first subject four times
//                          slower in the bass, and over it the second and
//                          its mirror
//   GOLGOTHA     93  3:04  the breakdown, as in the short form: darkness,
//                          the clock alone; the cry; Elias; it is finished;
//                          the veil and the earthquake; the centurion,
//                          alone; the tomb, three bars of rest
//   VERE        109  3:36  the stone: the drop; the clock and the bells
//                          come back; his line in two voices, three, four
//   CAPUT       117  3:52  the head, tenor and bass, the clock and the
//                          bells together now
//   IN UNUM     123  4:04  the entries drawn close: the first subject three
//                          bars apart; the second a half note apart; then
//                          both, two bars apart
//   CAPUT       150  4:58  the head, soprano and bass
//   DUOBUS      155  5:08  both commandments at once, as in the short form;
//                          in the mirror; then with the voices exchanged,
//                          and the household hangs on them
//   FUNDAMENTUM 167  5:32  a long E in the bass, and over it the second
//                          subject and its mirror, a bar apart
//   AMEN        175  5:48  the phrygian cadence, F to E, and the light;
//                          then four bars of silence, and it loops
//
// The chanted lines, when WORDS = 1, are the short form's, where the
// short form has them; the new sections add none. They load from
// canon-lawyer.ca the first time they play; if they are slow, stop and
// play again.
// ============================================================

setcpm(120/4) // one cycle = one bar, the household's tempo

// the lines, in the order they come: SAM's, then the choir's
const VOICES = 'https://www.canon-lawyer.ca/assets/music/voices/on-these-two-hang/'
samples({
  master: 'sam/master_which_is_the_great_commandment_in_the_law.wav',
  thou_shalt_love_the_lord: 'ascended/thou_shalt_love_the_lord_thy_god_with_all_thy_heart.wav',
  the_second: 'ascended/the_second_is_like_unto_it.wav',
  thy_neighbour: 'ascended/thou_shalt_love_thy_neighbour_as_thyself.wav',
  on_these_two: 'ascended/on_these_two_commandments_hang_all_the_law_and_the_prophets.wav',
  eli_eli: 'ascended/eli_eli_lama_sabachthani.wav',
  elias: 'sam/this_man_calleth_for_elias.wav',
  finished: 'ascended/it_is_finished.wav',
  truly: 'sam/truly_this_was_the_son_of_god.wav',
  truly_high: 'sam/truly_this_was_the_son_of_god_f.wav',
  truly_all: 'ascended/truly_this_was_the_son_of_god.wav',
  if_ye_love_me: 'ascended/if_ye_love_me_keep_my_commandments.wav',
}, VOICES)
// and one line of the motet's, its own recording: "things new and old"
samples({ things_new_and_old: 'ascended/things_new_and_old.wav' },
  'https://www.canon-lawyer.ca/assets/music/voices/a-new-song/')

// ============================================================
// ORBITS: 1 the clock · 2 the wheel, acid · 3 the chanted lines ·
//         4 pads and bass · 5 the veil, the earth, risers · 6 choir · 7 bells
// ============================================================

// ---------------- ROOTS

// ROOT 1. THE MODE: mode III, E phrygian. The family moves up by
// fifths, G, D, A, and E is next; and mode III is the mode of the
// Corpus Christi "Pange lingua".
// parents: none
const HOME = 'E3:phrygian'
const STEPS = { major: [0, 2, 4, 5, 7, 9, 11], mixolydian: [0, 2, 4, 5, 7, 9, 10], phrygian: [0, 1, 3, 5, 7, 8, 10] }

// ---------------- PARENTS
// from whether-the-cloud.strudel.js: "Viri Galilaei" (fd123dbc28e8),
// the line every track shares, the Ascension: "this same Jesus"
const VIRI = 'g3@2 g3@2 g3 c4 b3 c4@2 d4 c4 e4 d4 d4@3'
// from what-is-to-be-done.strudel.js: the hammer (3b8716d43c19). The
// carpenter's hammer drives the nails now.
const CARPENTER = 'IS NOT THIS THE CARPENTER'
// from brother-electron.strudel.js: Francis's canticle (2b82b56f32b5),
// creation praising "per frate", in A mixolydian
const TRIPLUM = 'a4 a4 b4 c#5@2 b4 a4@2 g4 a4 b4@2 a4@4 e5 d5 c#5 b4 c#5@2 b4 a4 g4@2 e4@2 a4@4'
// from a-new-song.strudel.js: its ascended voice singing "things new
// and old" (ab645d0aae4c), loaded above, as the motet recorded it
const THINGS = 'ascended/things_new_and_old.wav'

// ---------------- SUNG IN THE MODE OF THE CROSS
// Each parent's line is read as steps of its own scale, from its own
// final, and sung on the same steps of mode III, as "A New Song" sang
// its children in its own mode.
// parents: THE MODE, PARENTS
const PC = { c: 0, d: 2, e: 4, f: 5, g: 7, a: 9, b: 11 }
const midiOf = (t) => {
  const m = t.match(/^([a-g])(#|b)?(\d)$/)
  return 12 * (+m[3] + 1) + PC[m[1]] + (m[2] === '#' ? 1 : m[2] === 'b' ? -1 : 0)
}
const stepOf = (note, final, mode) => {
  for (let d = -21; d <= 28; d++) {
    const o = Math.floor(d / 7), k = ((d % 7) + 7) % 7
    if (midiOf(final) + 12 * o + STEPS[mode][k] === midiOf(note)) return d
  }
  throw new Error(note + ' is not in ' + final + ' ' + mode)
}
const inMode = (phrase, final, mode) => phrase.split(' ').map((t) => {
  const [p, d] = t.split('@')
  return (p === '~' ? '~' : stepOf(p, final, mode)) + (d ? '@' + d : '')
}).join(' ')
const sing = (phrase, final, mode, home, bars) => n(mini(inMode(phrase, final, mode))).scale(home).slow(bars)

// ---------------- THE LINES MADE BY RULE (counterpoint.py makes them;
// "python3 counterpoint.py --long --check" confirms they are quoted as made)
// parents: THE MODE
// The subjects, carved from the Vulgate, as in the short form:
const DILIGES = 'e4@2 e4 d4 g4@2 e4 c4 d4@2 c4 c4@2 c4 d4@2 g4@2 g4 g4@2 d4 c4@2 g3@8'
const SIMILE = 'e4@2 e4 d4 g4@2 e4 c4 c4@2 c4 e4@2 c4 d4 e4@2 c4@7'
const ELI = 'd4@2 e4 d4@2 e4 f4@2 f4 f4 f4@2 f4 e4@3'
const ELIAM = 'd4 e4@2 f4 g4@2 f4 e4@2 d4@7'
const CONSUMMATUM = 'g4 c5 f5@2 c5 d5@3'
const VERE = 'd4@2 d4 e4@2 e4 c4 d4@2 e4 d4@2 f4 e4@2 d4'
// and their forms in the long one: the mirror (inverted about mi), the Law
// held (each value four times longer), and the head they share:
const DILIGES_INV = 'e4@2 e4 f4 c4@2 e4 g4 f4@2 g4 g4@2 g4 f4@2 c4@2 c4 c4@2 f4 g4@2 c5@8'
const SIMILE_INV = 'e4@2 e4 f4 c4@2 e4 g4 g4@2 g4 e4@2 g4 f4 e4@2 g4@7'
const DILIGES_AUG = 'e4@8 e4@4 d4@4 g4@8 e4@4 c4@4 d4@8 c4@4 c4@8 c4@4 d4@8 g4@8 g4@4 g4@8 d4@4 c4@8 g3@32'
const CAPUT = 'e4@2 e4 d4 g4@2 e4 c4'
// II. Diliges, the first exposition, as in the short form
const DILIGES_S = '~@32 b4@2 b4 a4 d5@2 b4 g4 a4@2 g4 g4@2 g4 a4@2 d5@2 d5 d5@2 a4 g4@2 d4@8 b4@4 g4@4 a4@4 a4@4 g4@4 g4@4 e4@4 d4@4 b4@4 b4@4 e5@4 e5@4 d5@4 b4@4 d5@4 a4@4'
const DILIGES_A = 'e4@2 e4 d4 g4@2 e4 c4 d4@2 c4 c4@2 c4 d4@2 g4@2 g4 g4@2 d4 c4@2 g3@8 d4@4 b3@4 c4@4 c4@4 b3@4 g3@4 b3@4 g3@4 b3@4 b3@4 a3@4 a3@4 b3@4 d4@4 b3@4 g3@4 d4@4 d4@4 e4@4 e4@4 f4@4 d4@4 f4@4 d4@4'
const DILIGES_T = '~@32 ~@32 e3@2 e3 d3 g3@2 e3 c3 d3@2 c3 c3@2 c3 d3@2 g3@2 g3 g3@2 d3 c3@2 g2@8 g3@4 b3@4 e3@4 e3@4 a3@4 b3@4 a3@4 a3@4'
const DILIGES_B = '~@32 ~@32 ~@32 b2@2 b2 a2 d3@2 b2 g2 a2@2 g2 g2@2 g2 a2@2 d3@2 d3 d3@2 a2 g2@2 d2@8'
const DILIGES_TIN = 'g5@2 g5 e5 b5@2 g5 e5 e5@2 e5 e5@2 e5 e5@2 b5@2 b5 b5@2 e5 e5@2 b4@8 e5@2 e5 b4 e5@2 e5 b4 b4@2 b4 b4@2 b4 b4@2 e5@2 e5 e5@2 b4 b4@2 e4@8 g5@2 g5 e5 b5@2 g5 e5 e5@2 e5 e5@2 e5 e5@2 b5@2 b5 b5@2 e5 e5@2 b4@8 e5@2 e5 b4 e5@2 e5 b4 b4@2 b4 b4@2 b4 b4@2 e5@2 e5 e5@2 b4 b4@2 e4@8'
// III. Caput: soprano and tenor
const CAPUT_I_S = 'e5@2 e5 d5 g5@2 e5 c5 d5@2 d5 c5 f5@2 d5 b4 c5@2 c5 b4 e5@2 c5 a4 b4@2 b4 a4 d5@2 b4 g4 a4@2 a4 g4 c5@2 a4 f4 c5@4 d5@4'
const CAPUT_I_A = 'e4@4 c5@4 b4@4 d5@4 a4@4 c5@4 g4@4 b4@4 d4@4 e4@4 f4@4 d4@4'
const CAPUT_I_T = '~@4 e4@2 e4 d4 g4@2 e4 c4 d4@2 d4 c4 f4@2 d4 b3 c4@2 c4 b3 e4@2 c4 a3 b3@2 b3 a3 d4@2 b3 g3 a3@2 a3 g3 c4@2 a3 f3@5'
const CAPUT_I_B = 'g2@4 c3@4 g3@4 f3@4 f3@4 e3@4 e3@4 d3@4 d3@4 c3@4 a2@4 d3@4'
const CAPUT_I_TIN = 'g5@2 g5 e5 b5@2 g5 e5 e5@2 e5 e5 g5@2 e5 e5 e5@2 e5 e5 g5@2 e5 b4 e5@2 e5 b4 e5@2 e5 b4 b4@2 b4 b4 e5@2 b4 g4 ~@8'
// IV. Simile, the second exposition, as in the short form
const SIMILE_S = '~@24 ~@24 ~@24 b4@2 b4 a4 d5@2 b4 g4 g4@2 g4 b4@2 g4 a4 b4@2 g4@7'
const SIMILE_A = '~@24 ~@24 e4@2 e4 d4 g4@2 e4 c4 c4@2 c4 e4@2 c4 d4 e4@2 c4@7 d4@4 b3@4 b3@4 b3@4 b3@4 c4@4'
const SIMILE_T = '~@24 b3@2 b3 a3 d4@2 b3 g3 g3@2 g3 b3@2 g3 a3 b3@2 g3@7 b3@4 c4@4 a3@4 c4@4 a3@4 g3@4 d3@4 g3@4 e3@4 g3@4 e3@4 g3@4'
const SIMILE_B = 'e3@2 e3 d3 g3@2 e3 c3 c3@2 c3 e3@2 c3 d3 e3@2 c3@7 d3@4 b2@4 b2@4 g2@4 b2@4 c3@4 g3@4 e3@4 c3@4 a2@4 c3@4 c3@4 b2@4 g2@4 g2@4 e2@4 g2@4 c3@4'
const SIMILE_TIN = 'g5@2 g5 e5 b5@2 g5 e5 e5@2 e5 g5@2 e5 e5 g5@2 e5@7 e5@2 e5 b4 e5@2 e5 b4 b4@2 b4 e5@2 b4 b4 e5@2 b4@7 g5@2 g5 e5 b5@2 g5 e5 e5@2 e5 g5@2 e5 e5 g5@2 e5@7 e5@2 e5 b4 e5@2 e5 b4 b4@2 b4 e5@2 b4 b4 e5@2 b4@7'
// V. Caput: alto and bass
const CAPUT_II_S = 'f4@4 d5@4 a4@4 b4@4 g4@4 a4@4 a4@4 g4@4 e4@4 g4@4 b4@4 d5@4'
const CAPUT_II_A = 'f4@2 f4 e4 a4@2 f4 d4 e4@2 e4 d4 g4@2 e4 c4 d4@2 d4 c4 f4@2 d4 b3 c4@2 c4 b3 e4@2 c4 a3 b3@2 b3 a3 d4@2 b3 g3 d4@4 d4@4'
const CAPUT_II_T = 'a3@4 d4@4 c4@4 e4@4 b3@4 d4@4 a3@4 c4@4 g3@4 b3@4 b3@4 g3@4'
const CAPUT_II_B = '~@4 f3@2 f3 e3 a3@2 f3 d3 e3@2 e3 d3 g3@2 e3 c3 d3@2 d3 c3 f3@2 d3 b2 c3@2 c3 b2 e3@2 c3 a2 b2@2 b2 a2 d3@2 b2 g2@5'
const CAPUT_II_TIN = 'g5@2 g5 g5 b5@2 g5 e5 g5@2 g5 e5 b5@2 g5 e5 e5@2 e5 e5 g5@2 e5 e5 e5@2 e5 e5 g5@2 e5 b4 e5@2 e5 b4 e5@2 e5 b4 ~@8'
// VI. Speculum: the mirror
const SPECULUM_S = '~@96 b4@2 b4 c5 g4@2 b4 d5 c5@2 d5 d5@2 d5 c5@2 g4@2 g4 g4@2 c5 d5@2 g5@8 b4@2 b4 c5 g4@2 b4 d5 d5@2 d5 b4@2 d5 c5 b4@2 d5@7 c5@4 e5@4 e5@4 e5@4 b4@4 c5@4 b4@4 d5@4 d5@4 d5@4 d5@4 f5@4 e5@4 g5@4 e5@4 g5@4 e5@4 d5@4'
const SPECULUM_A = '~@64 e4@2 e4 f4 c4@2 e4 g4 f4@2 g4 g4@2 g4 f4@2 c4@2 c4 c4@2 f4 g4@2 c5@8 e4@4 d4@4 f4@4 f4@4 e4@4 e4@4 g4@4 g4@4 e4@4 d4@4 d4@4 d4@4 b3@4 ~@4 e4@2 e4 f4 c4@2 e4 g4 g4@2 g4 e4@2 g4 f4 e4@2 g4@7 g4@4 b4@4 b4@4 b4@4 b4@4 a4@4 c5@4 g4@4 b4@4 g4@4 b4@4 g4@4'
const SPECULUM_T = 'e3@2 e3 f3 c3@2 e3 g3 f3@2 g3 g3@2 g3 f3@2 c3@2 c3 c3@2 f3 g3@2 c4@8 g3@4 b3@4 a3@4 a3@4 b3@4 d4@4 e4@4 d4@4 a3@4 g3@4 c4@4 b3@4 a3@4 a3@4 c4@4 c4@4 e4@4 b3@4 c4@4 a3@4 b3@4 c4@4 d4@4 c4@4 b3@4 b3@4 g3@4 b3@4 g3@4 b3@4 a3@4 g3@4 g3@4 c4@4 b3@4 ~@4 b3@2 b3 c4 g3@2 b3 d4 d4@2 d4 b3@2 d4 c4 b3@2 d4@7 c4@4 e4@4 e4@4 e4@4 g4@4 d4@4'
const SPECULUM_B = '~@32 b2@2 b2 c3 g2@2 b2 d3 c3@2 d3 d3@2 d3 c3@2 g2@2 g2 g2@2 c3 d3@2 g3@8 a3@4 e3@4 a2@4 b2@4 c3@4 f3@4 e3@4 f3@4 e3@4 g3@4 f3@4 f3@4 g3@4 e3@4 b2@4 c3@4 e3@4 b2@4 b2@4 g2@4 b2@4 g2@4 a2@4 c3@4 e3@4 c3@4 e3@4 c3@4 e3@4 b2@4 g2@4 b2@4 g2@4 ~@4 e3@2 e3 f3 c3@2 e3 g3 g3@2 g3 e3@2 g3 f3 e3@2 g3@7'
const SPECULUM_TIN = 'g5@2 g5 g5 e5@2 g5 b5 g5@2 b5 b5@2 b5 g5@2 e5@2 e5 e5@2 g5 b5@2 e6@8 e5@2 e5 e5 b4@2 e5 e5 e5@2 e5 e5@2 e5 e5@2 b4@2 b4 b4@2 e5 e5@2 b5@8 g5@2 g5 g5 e5@2 g5 b5 g5@2 b5 b5@2 b5 g5@2 e5@2 e5 e5@2 g5 b5@2 e6@8 e5@2 e5 e5 b4@2 e5 e5 e5@2 e5 e5@2 e5 e5@2 b4@2 b4 b4@2 e5 e5@2 b5@8 e5@2 e5 e5 b4@2 e5 e5 e5@2 e5 e5@2 e5 e5 e5@2 e5@7 g5@2 g5 g5 e5@2 g5 b5 b5@2 b5 g5@2 b5 g5 g5@2 b5@7 e5@2 e5 e5 b4@2 e5 e5 e5@2 e5 e5@2 e5 e5 e5@2 e5@7 g5@2 g5 g5 e5@2 g5 b5 b5@2 b5 g5@2 b5 g5 g5@2 b5@7'
// VII. Lex: the Law held
const LEX_S = 'e5@4 g5@4 e5@4 f5@4 e5@4 d5@4 e5@4 g5@4 f5@4 d5@4 e5@4 c5@4 e5@4 e5@4 d5@4 d5@4 b4@4 g4@4 b4@4 b4@4 g4@4 a4@4 c5@4 e5@4 g5@4 ~@4 b4@2 b4 c5 g4@2 b4 d5 d5@2 d5 b4@2 d5 c5 b4@2 d5@7'
const LEX_A = 'g4@4 b4@4 g4@4 f4@4 g4@4 b4@4 c5@4 c5@4 a4@4 b4@4 a4@4 g4@4 a4@4 g4@4 b4@4 b4@4 g4@4 d4@4 e4@4 d4@4 e4@4 ~@4 e4@2 e4 f4 c4@2 e4 g4 g4@2 g4 e4@2 g4 f4 e4@2 g4@7 b4@4 g4@4 g4@4 d4@4'
const LEX_T = 'c4@4 b3@4 c4@4 d4@4 b3@4 d4@4 c4@4 e4@4 d4@4 b3@4 c4@4 e4@4 c4@4 ~@4 b3@2 b3 a3 d4@2 b3 g3 g3@2 g3 b3@2 g3 a3 b3@2 g3@7 b3@4 a3@4 a3@4 g3@4 g3@4 g3@4 e3@4 b3@4 b3@4 d4@4 b3@4 g3@4'
const LEX_B = 'e3@8 e3@4 d3@4 g3@8 e3@4 c3@4 d3@8 c3@4 c3@8 c3@4 d3@8 g3@8 g3@4 g3@8 d3@4 c3@8 g2@32'
const LEX_TIN = 'g5@8 g5@4 e5@4 b5@8 g5@4 e5@4 e5@8 e5@4 e5@8 e5@4 e5@2 e5 b4 e5@2 e5 b4 b4@2 b4 e5@2 b4 b4 e5@2 b4@7 ~@8 g5@2 g5 g5 e5@2 g5 b5 b5@2 b5 g5@2 b5 g5 g5 e5@2 e5 e5 b4@2 e5 e5 e5@2 e5 e5@2 e5 e5 e5@2 e5@7'
// IX. Vere, the centurion's line, as in the short form
const VERE_SOLO_S = 'd5@2 d5 e5@2 e5 c5 d5@2 e5 d5@2 f5 e5@2 d5'
const VERE_DUO_S = 'd5@2 d5 e5@2 e5 c5 d5@2 e5 d5@2 f5 e5@2 d5'
const VERE_DUO_B = 'b3@2 g3@2 g3@2 a3@2 g3@2 b3@2 a3@2 g3@2'
const VERE_TRIO_S = 'd5@2 d5 e5@2 e5 c5 d5@2 e5 d5@2 f5 e5@2 d5'
const VERE_TRIO_A = 'a4@2 g4@2 e4@2 f4@2 a4@2 g4@2 f4@2 g4@2'
const VERE_TRIO_B = 'f3@2 g3@2 g3@2 a3@2 f3@2 g3@2 a3@2 g3@2'
const VERE_TUTTI_S = 'd5@2 d5 e5@2 e5 c5 d5@2 e5 d5@2 f5 e5@2 d5'
const VERE_TUTTI_A = 'g4@2 a4@2 g4@2 a4@2 b4@2 g4@2 f4@2 g4@2'
const VERE_TUTTI_T = 'b3@2 a3@2 c4@2 c4@2 b3@2 d4@2 c4@2 g3@2'
const VERE_TUTTI_B = 'g3@2 f3@2 e3@2 f3@2 d3@2 b2@2 a2@2 g2@2'
const VERE_TIN = 'e6@2 e6 g6@2 g6 e6 e6@2 g6 e6@2 g6 g6@2 e6'
// X. Caput: tenor and bass
const CAPUT_III_S = 'g5@4 g5@4 g5@4 f5@4 f5@4 e5@4 e5@4 d5@4 d5@4 c5@4 c5@4 c5@4'
const CAPUT_III_A = 'b4@4 c5@4 g4@4 a4@4 a4@4 g4@4 e4@4 g4@4 d4@4 e4@4 c4@4 c4@4'
const CAPUT_III_T = 'e4@2 e4 d4 g4@2 e4 c4 d4@2 d4 c4 f4@2 d4 b3 c4@2 c4 b3 e4@2 c4 a3 b3@2 b3 a3 d4@2 b3 g3 a3@2 a3 g3 c4@2 a3 f3 a3@4 f3@4'
const CAPUT_III_B = '~@4 e3@2 e3 d3 g3@2 e3 c3 d3@2 d3 c3 f3@2 d3 b2 c3@2 c3 b2 e3@2 c3 a2 b2@2 b2 a2 d3@2 b2 g2 a2@2 a2 g2 c3@2 a2 f2@5'
const CAPUT_III_TIN = 'g5@2 g5 e5 b5@2 g5 e5 e5@2 e5 e5 g5@2 e5 e5 e5@2 e5 e5 g5@2 e5 b4 e5@2 e5 b4 e5@2 e5 b4 b4@2 b4 b4 e5@2 b4 g4 ~@8'
// XI. In unum: the stretti
const IN_UNUM_S = '~@48 b4@2 b4 a4 d5@2 b4 g4 a4@2 g4 g4@2 g4 a4@2 d5@2 d5 d5@2 a4 g4@2 d4@8 e4@4 e5@4 d5@4 a4@4 b4@4 a4@4 b4@4 ~@4 e5@2 e5 d5 g5@2 e5 c5 c5@2 c5 e5@2 c5 d5 e5@2 c5@7 a4@4 g4@4 b4@4 c5@4 a4@4 ~@4 b4@2 b4 a4 d5@2 b4 g4 g4@2 g4 b4@2 g4 a4 b4@2 g4@7 a4@4 a4@4 b4@4 g4@4 b4@4 g4@4 g4@4 g4@4'
const IN_UNUM_A = 'e4@2 e4 d4 g4@2 e4 c4 d4@2 c4 c4@2 c4 d4@2 g4@2 g4 g4@2 d4 c4@2 g3@8 a3@4 a3@4 b3@4 e4@4 d4@4 b3@4 c4@4 c4@4 d4@4 f4@4 d4@4 d4@4 c4@4 e4@4 f4@4 f4@4 d4@4 f4@4 ~@4 e4@2 e4 d4 g4@2 e4 c4 c4@2 c4 e4@2 c4 d4 e4@2 c4@7 e4@4 a3@4 ~@4 e4@2 e4 d4 g4@2 e4 c4 d4@2 c4 c4@2 c4 d4@2 g4@2 g4 g4@2 d4 c4@2 g3@8 b3@4 e4@4 a3@4 a3@4 e4@4 d4@4 b3@4 d4@4 e4@4 d4@4'
const IN_UNUM_T = '~@72 b3@2 b3 a3 d4@2 b3 g3 a3@2 g3 g3@2 g3 a3@2 d4@2 d4 d4@2 a3 g3@2 d3@8 b3@4 g3@4 ~@4 e3@2 e3 d3 g3@2 e3 c3 c3@2 c3 e3@2 c3 d3 e3@2 c3@7 g3@4 g3@4 g3@4 a3@4 f3@4 g3@4 g3@4 e3@4 e3@4 g3@4 b3@4 a3@4 ~@4 b3@2 b3 a3 d4@2 b3 g3 g3@2 g3 b3@2 g3 a3 b3@2 g3@7'
const IN_UNUM_B = '~@24 e3@2 e3 d3 g3@2 e3 c3 d3@2 c3 c3@2 c3 d3@2 g3@2 g3 g3@2 d3 c3@2 g2@8 c3@4 c3@4 b2@4 d3@4 d3@4 b2@4 c3@4 c3@4 d3@4 d3@4 b2@4 ~@4 e3@2 e3 d3 g3@2 e3 c3 c3@2 c3 e3@2 c3 d3 e3@2 c3@7 a2@4 e2@4 f2@4 e2@4 g2@4 e2@4 f2@4 a2@4 b2@4 g2@4 g2@4 ~@4 e3@2 e3 d3 g3@2 e3 c3 d3@2 c3 c3@2 c3 d3@2 g3@2 g3 g3@2 d3 c3@2 g2@8 e2@4 g2@4'
const IN_UNUM_TIN = 'g5@2 g5 e5 b5@2 g5 e5 e5@2 e5 e5@2 e5 e5@2 b5@2 b5 b5@2 e5 e5@2 g5@2 g5 e5 b5@2 g5 e5 e5@2 e5 e5@2 e5 e5@2 b5@2 b5 b5@2 e5 e5@2 e5@2 e5 b4 e5@2 e5 b4 b4@2 b4 b4@2 b4 b4@2 e5@2 e5 e5@2 b4 b4@2 e5@2 e5 b4 e5@2 e5 b4 b4@2 b4 b4@2 b4 b4@2 e5@2 e5 e5@2 b4 b4@2 e4@8 g5@2 g5 e5 g5@2 g5 e5 g5@2 g5 e5 g5@2 g5 e5 b5@2 g5 e5 e5@2 e5 g5@2 e5 e5 g5@2 e5@7 ~@4 g5@2 g5 e5 b5@2 g5 e5 e5@2 e5 e5@2 e5 e5@2 e5@2 e5 b4 e5@2 e5 b4 b4@2 b4 e5@2 b4 b4 e5 g5@2 g5 e5 b5@2 g5 e5 e5@2 e5 e5@2 e5 e5@2 e5@2 e5 b4 e5@2 e5 b4 b4@2 b4 e5@2 b4 b4 e5@2 b4@7'
// XII. Caput: soprano and bass
const CAPUT_IV_S = 'e5@2 e5 d5 g5@2 e5 c5 d5@2 d5 c5 f5@2 d5 b4 c5@2 c5 b4 e5@2 c5 a4 b4@2 b4 a4 d5@2 b4 g4 d5@4 d5@4'
const CAPUT_IV_A = 'g4@4 g4@4 g4@4 f4@4 a4@4 a4@4 g4@4 b4@4 b4@4 g4@4'
const CAPUT_IV_T = 'g3@4 c4@4 b3@4 d4@4 a3@4 a3@4 e4@4 d4@4 b3@4 d4@4'
const CAPUT_IV_B = '~@4 e3@2 e3 d3 g3@2 e3 c3 d3@2 d3 c3 f3@2 d3 b2 c3@2 c3 b2 e3@2 c3 a2 b2@2 b2 a2 d3@2 b2 g2@5'
const CAPUT_IV_TIN = 'g5@2 g5 e5 b5@2 g5 e5 e5@2 e5 e5 g5@2 e5 e5 e5@2 e5 e5 g5@2 e5 b4 e5@2 e5 b4 e5@2 e5 b4 ~@8'
// XIII. Duobus: as in the short form; in the mirror; with the voices exchanged
const DUOBUS_S = '~@4 b4@2 b4 a4 d5@2 b4 g4 g4@2 g4 b4@2 g4 a4 b4@2 g4@7 ~@4'
const DUOBUS_A = 'b4@4 g4@4 b4@4 g4@4 e4@4 g4@4 e4@4 d4@4'
const DUOBUS_T = 'b3@4 e4@4 d4@4 e4@4 b3@4 b3@4 b3@4 g3@4'
const DUOBUS_B = 'e3@2 e3 d3 g3@2 e3 c3 d3@2 c3 c3@2 c3 d3@2 g3@2 g3 g3@2 d3 c3@2 g2@8'
const DUOBUS_TIN = '~@4 e5@2 e5 b4 e5@2 e5 b4 b4@2 b4 e5@2 b4 b4 e5@2 b4@7 ~@4'
const DUOBUS_M_S = '~@4 b4@2 b4 c5 g4@2 b4 d5 d5@2 d5 b4@2 d5 c5 b4@2 d5@7 ~@4'
const DUOBUS_M_A = 'g4@4 d4@4 e4@4 d4@4 d4@4 d4@4 d4@4 g4@4'
const DUOBUS_M_T = 'g3@4 g3@4 g3@4 b3@4 g3@4 b3@4 b3@4 d4@4'
const DUOBUS_M_B = 'b2@2 b2 c3 g2@2 b2 d3 c3@2 d3 d3@2 d3 c3@2 g2@2 g2 g2@2 c3 d3@2 g3@8'
const DUOBUS_M_TIN = '~@4 e5@2 e5 e5 b4@2 e5 e5 e5@2 e5 e5@2 e5 e5 e5@2 e5@7 ~@4'
const DUOBUS_X_S = 'b4@2 b4 a4 d5@2 b4 g4 a4@2 g4 g4@2 g4 a4@2 d5@2 d5 d5@2 a4 g4@2 d4@8'
const DUOBUS_X_A = 'd4@4 d4@4 d4@4 b3@4 d4@4 d4@4 b3@4 a3@4'
const DUOBUS_X_T = 'd4@4 b3@4 d3@4 e3@4 d3@4 d3@4 d3@4 d3@4'
const DUOBUS_X_B = '~@4 b2@2 b2 a2 d3@2 b2 g2 g2@2 g2 b2@2 g2 a2 b2@2 g2@7 ~@4'
const DUOBUS_X_TIN = 'e5@2 e5 b4 e5@2 e5 b4 b4@2 b4 b4@2 b4 b4@2 e5@2 e5 e5@2 b4 b4@2 e4@8'
// XIV. Fundamentum: the pedal and the last stretto
const FUNDAMENTUM_S = 'b4@4 ~@4 e5@2 e5 f5 c5@2 e5 g5 g5@2 g5 e5@2 g5 f5 e5@2 g5@7 e5@2 e5 d5 g5@2 e5 c5 c5@2 c5 e5@2 c5 d5 e5@2 c5@7 b4@4 b4@4'
const FUNDAMENTUM_A = 'e4@2 e4 d4 g4@2 e4 c4 c4@2 c4 e4@2 c4 d4 e4@2 c4@7 e4@2 e4 f4 c4@2 e4 g4 g4@2 g4 e4@2 g4 f4 e4@2 g4@7 e4@4 e4@4 e4@4 b3@4'
const FUNDAMENTUM_T = 'g3@4 e3@4 c3@4 ~@4 e3@2 e3 d3 g3@2 e3 c3 c3@2 c3 e3@2 c3 d3 e3@2 c3@7 e3@2 e3 f3 c3@2 e3 g3 g3@2 g3 e3@2 g3 f3 e3@2 g3@7'
const FUNDAMENTUM_B = 'e2@64'
const FUNDAMENTUM_TIN = 'g5@2 g5 e5 b5@2 g5 e5 g5@2 g5 g5 e5@2 g5 b5 g5@2 g5 e5 b5@2 g5 e5 g5@2 g5 g5 e5@2 g5 b5 g5@2 g5 e5 b5@2 g5 e5 g5@2 g5 g5 e5@2 g5 b5 b5@2 b5 g5@2 b5 g5 g5@2 b5@7'

// ---------------- THE PUMP: the sidechain, by hand. Four times a bar the
// kick lands and everything that is not the kick ducks and comes back:
// creation makes room for the clock. The clock itself is never ducked.
// parents: none
const DUCK = "[.38 .72 1 .88]*4"
const WORDS = 0 // 1 brings the chanted lines back, filtered and ducked
const EUCLID = '3,8,1' // strokes, steps, turn: . X . . X . . X

// ---------------- THE PERSONS: the choir sings the lines with words, as
// before; a supersaw pad, creation, doubles every voice and pumps with
// it. The bass voice, wherever the rule put it, also goes down an octave
// into a sub retriggered in eighths and a growl on the offbeats: the bass
// line of the floor is the bass voice of the fugue, note for note.
// parents: THE LINES MADE BY RULE, THE PUMP
const bars = (line) => line.split(' ').reduce((k, t) => k + (t.includes('@') ? +t.split('@')[1] : 1), 0) / 8
const sung = (x) => note(mini(x)).slow(bars(x))
const choir = (x, pan = .5, g = .22) => sung(x).s('gm_choir_aahs')
  .attack(.06).release(.5).lpf(4200).gain(g * 3).velocity(DUCK).room(.5).roomsize(5).pan(pan).orbit(6)
const pad = (x, g = .06) => sung(x).s('supersaw').unison(5).detune(.22).spread(.8)
  .attack(.04).release(.35).lpf(sine.slow(8).range(900, 2600)).lpq(1.5).gain(g * 3).velocity(DUCK).room(.35).orbit(4)
const subbass = (x, g = .55) => sung(x).transpose(-12).struct("x*8").s('sine')
  .attack(.004).decay(.18).sustain(.7).release(.06).lpf(200).gain(g).velocity("[.55 1]*4").orbit(4)
const growl = (x, g = .14) => sung(x).transpose(-12).struct(`[x(${EUCLID})]*2`).s('sawtooth')
  .attack(.004).decay(.14).sustain(.15).release(.05).lpf(650).lpq(5).shape(.3).gain(g).pan(.5).orbit(4)
const satb = (S, A, T, B, g = .22) => stack(
  ...[[S, .62], [A, .42], [T, .56]].filter(([x]) => x).map(([x, p]) => stack(choir(x, p, g), pad(x))),
  ...(B ? [choir(B, .48, g), pad(B, .05), subbass(B), growl(B)] : []),
)
// one voice alone, no pump: the clock has stopped when these are sung
const solo = (x, g = .3) => sung(x).s('gm_choir_aahs').attack(.08).release(1.2).lpf(5000)
  .gain(g * 3).room(.7).roomsize(6).orbit(6)

// ---------------- THE BELLS: tintinnabuli, over each note the nearest
// note of the triad; on a celesta, and on a pluck with a dotted-eighth
// echo, the bell's own ring answered down the room
// parents: THE LINES MADE BY RULE
const bells = (x, g = .12) => stack(
  sung(x).s('gm_celesta').release(1.2).gain(g * 3).room(.5).roomsize(6).pan(.66).orbit(7),
  sung(x).s('triangle').attack(.002).decay(.09).sustain(0).release(.05).hpf(700)
    .gain(g * 1.8).delay(.45).delaytime(.375).delayfeedback(.45).pan(.3).orbit(7),
)

// ---------------- THE CLOCK: the saeculum. Brother Electron's chip,
// ticking, on the floor: a 909 four to the floor, claps on two and four,
// closed hats in sixteenths, an open hat on the offbeat; and the wheel,
// the triad turned in even eighths, now a sawtooth through a resonant
// filter that opens and closes over eight bars. The regular beside the
// ethereal, and the ethereal ducks.
// parents: THE MODE
const kick = s("bd*4").bank('RolandTR909').gain(.95).shape(.18).orbit(1)
const hats = stack(
  s("hh*16").bank('RolandTR909').gain("[.24 .1 .17 .1]*4").hpf(7000).orbit(1),
  s("[~ oh]*4").bank('RolandTR909').gain(.26).release(.07).hpf(5000).orbit(1),
)
const clap = s("~ cp ~ cp").bank('RolandTR909').gain(.5).room(.3).roomsize(2).orbit(1)
// three in eight, in the clock: a tom, a bar to the figure
const turn = s(`lt(${EUCLID})`).bank('RolandTR909').gain(.42).lpf(3000).pan(.6).room(.2).orbit(1)
const tick = stack(kick, hats, clap, turn)
const wheel = (cut = 2400, g = .08) => n("0 2 4 2 0 2 4 7").scale(HOME).s('sawtooth')
  .attack(.003).decay(.14).sustain(.15).release(.05)
  .lpf(sine.slow(8).range(cut * .2, cut)).lpq(9).lpenv(3).lpd(.12).shape(.2).gain(g).pan(.4).orbit(2)
const clock = stack(tick, wheel())
// before the clock: 808 hats, not the clock, keeping time in the intro
const hats808 = s("hh*16").bank('RolandTR808').gain("[.18 .07 .13 .07]*4").hpf(8000).orbit(1)
// the roll and the riser: creation leaning into a downbeat
const roll = s("sd*16").bank('RolandTR909').gain(saw.range(.1, .5)).hpf(400).room(.3).orbit(1)
const riser = (b) => s('white').hpf(saw.slow(b).range(300, 5000)).lpf(9000)
  .gain(saw.slow(b).range(.015, .17)).room(.4).orbit(5)
const crash = s("cr ~ ~ ~").bank('RolandTR909').gain(.45).room(.4).roomsize(4).orbit(1)
// bar masks over an n-bar section: on these bars, or from this bar on
const onBars = (n, ...ks) => '<' + Array.from({ length: n }, (_, i) => (ks.includes(i + 1) ? 1 : 0)).join(' ') + '>'
const fromBar = (n, k) => '<' + Array.from({ length: n }, (_, i) => (i + 1 >= k ? 1 : 0)).join(' ') + '>'

// ---------------- THE HAMMER: the carpenter's, in Morse, as the parents
// tapped it; dot 1 sixteenth, dash 3; 1 between signs, 3 between letters,
// 7 between words
// parents: PARENTS (CARPENTER)
const CODE = { A: '.-', C: '-.-.', E: '.', H: '....', I: '..', N: '-.', O: '---',
               P: '.--.', R: '.-.', S: '...', T: '-' }
const morse = (text) => text.split(' ').map((word) =>
  word.split('').map((ch) =>
    CODE[ch].split('').map((sign) => (sign === '.' ? 'x' : 'x@3')).join(' ~ ')
  ).join(' ~@3 ')
).join(' ~@7 ') + ' ~@7'
const units = (talea) => talea.split(' ').reduce((k, t) => k + (t.includes('@') ? +t.split('@')[1] : 1), 0)
const hammer = (sound = 'rim') => {
  const talea = morse(CARPENTER)
  return s(sound).struct(mini(talea)).slow(units(talea) / 16).bank('RolandTR909')
}

// ---------------- THE HOUSEHOLD HANGS: the parents' lines in the mode of
// the Cross, in long notes, high, hung over the rest; the Ascension line
// on the pad, the canticle on a pluck with the bells' echo
// parents: PARENTS, SUNG IN THE MODE OF THE CROSS, THE PUMP
const viri = (g = .05) => sing(VIRI, 'g3', 'mixolydian', 'E4:phrygian', 8).s('supersaw').unison(4).detune(.18)
  .attack(.5).release(1.5).lpf(1800).gain(g * 3).velocity(DUCK).room(.6).roomsize(6).orbit(4)
const canticle = (g = .2) => sing(TRIPLUM, 'a3', 'mixolydian', 'E4:phrygian', 4).s('triangle')
  .attack(.003).decay(.12).sustain(.1).release(.2).gain(g * 2).velocity(DUCK)
  .delay(.4).delaytime(.375).delayfeedback(.4).room(.4).pan(.7).orbit(7)

// ---------------- THE VEIL AND THE EARTH: "the veil of the temple was
// rent in twain from the top to the bottom; and the earth did quake, and
// the rocks rent" (Matthew 27:51). Creation answers, with no words.
const veil = s('white').lpf(saw.slow(2).range(9000, 150)).gain(saw.slow(2).range(.16, .02)).orbit(5)
const quake = stack(
  s('brown').lpf(180).gain(sine.slow(2).range(.25, .4)).orbit(5),
  note("e1").s('sine').attack(.02).release(3).gain(.45).lpf(100).orbit(5),
)
const rocks = s("~ rim ~ ~ rim ~ ~ rim").bank('RolandTR909').gain(.45).room(.5).roomsize(4).orbit(5)
const timpani = note("e2*8").s('gm_timpani').gain(".15 .18 .21 .24 .27 .3 .33 .36").orbit(5)
// Elijah's whirlwind, which comes and does not come
const whirlwind = s('pink').bpf(saw.range(300, 3000)).gain(saw.range(0, .12)).orbit(5)

// ---------------- VOICES: SAM, chanting; then the choir. Off unless WORDS.
const vox = (p, g = 1) => WORDS
  ? s(p).hpf(180).lpf(6500).gain(g).velocity(DUCK).delay(".18:.375:.3").room(.3).orbit(3)
  : silence

// ============================================================
// SECTIONS
// ============================================================

// I. PENDET. The household's law and prophets, hanging on a pedal of
// E: a drone, Viri Galilaei in long notes, Francis's canticle, the
// motet's "things new and old", and the hammer. Then the lawyer.
// parents: THE HOUSEHOLD HANGS, THE HAMMER, PARENTS (THINGS), THE PUMP
const pedal = stack(
  note("[e2,b2]").s('supersaw').unison(4).detune(.2).attack(1).release(2)
    .lpf(sine.slow(8).range(250, 1200)).gain(.05 * 3).velocity(DUCK).room(.6).orbit(4),
  note("e1").s('sine').attack(.5).release(2).lpf(90).gain(.3).orbit(4),
)
const secPENDET = stack(
  pedal, viri(),
  canticle(.16).mask("<1 1 1 1 0 0 0 0>"),
  hammer().gain(.3).pan(.35).orbit(1).mask("<0 0 0 0 1 1 1 1>"),
  vox("<~ ~ things_new_and_old ~ master ~ ~ ~>"),
)

// II. DILIGES. "Thou shalt love the Lord thy God with all thy heart."
// The first subject, four times, each entry a voice more; the bells
// ring over whichever voice has it; the sub arrives with the fourth
// entry, the bass. No clock yet: 808 hats from the tenor's entry.
// parents: THE PERSONS, THE BELLS
const secDILIGES = stack(
  satb(DILIGES_S, DILIGES_A, DILIGES_T, DILIGES_B),
  bells(DILIGES_TIN),
  pedal.mask("<1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0>"),
  hats808.mask(fromBar(16, 9)),
  vox("<thou_shalt_love_the_lord ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~>"),
)

// III. CAPUT. The head the two subjects share, in the soprano, and
// in the tenor an octave below, a half note behind; each bar a step
// lower. No clock yet: the riser climbs the six bars, the roll on the
// last.
// parents: THE PERSONS, THE BELLS
const secCAPUT_I = stack(satb(CAPUT_I_S, CAPUT_I_A, CAPUT_I_T, CAPUT_I_B), bells(CAPUT_I_TIN, .1),
  hats808, riser(6), roll.mask(onBars(6, 6)))

// IV. SIMILE. "And the second is like unto it." The clock enters, and
// the second subject, with the same head, from the bass up: the love
// of neighbour lives in time. On the floor: the sub alone for three
// bars, the roll on the third, and the kick lands on the fourth.
// parents: THE PERSONS, THE CLOCK
// The duet of the ethereal and the regular is a flip-flop: the clock
// toggles it every bar, the bells on Q and the wheel on not-Q, as the
// chip in "Brother Electron" holds a bit in two cross-coupled gates
// (Eccles and Jordan, 1918). Each sounds while the other rests; at the
// stone they sound together.
const Q = "<1 0>", NOT_Q = "<0 1>"
const secSIMILE = stack(
  satb(SIMILE_S, SIMILE_A, SIMILE_T, SIMILE_B),
  tick.mask("<0 0 0 1 1 1 1 1 1 1 1 1>"),
  roll.mask(onBars(12, 3)), crash.mask(onBars(12, 4)),
  bells(SIMILE_TIN, .11).mask(Q),
  wheel(1800, .07).mask(NOT_Q),
  vox("<the_second ~ ~ thy_neighbour ~ ~ ~ ~ ~ on_these_two ~ ~>"),
)

// V. CAPUT, in the alto and the bass. The clock goes on, and the
// bells and the wheel go on taking turns.
// parents: THE PERSONS, THE BELLS, THE CLOCK
const secCAPUT_II = stack(satb(CAPUT_II_S, CAPUT_II_A, CAPUT_II_T, CAPUT_II_B),
  tick, bells(CAPUT_II_TIN, .1).mask(Q), wheel(1800, .07).mask(NOT_Q), roll.mask(onBars(6, 6)))

// VI. SPECULUM. "For now we see through a glass, darkly." The first
// subject upside down: the tenor leads where the alto led, and the
// bass answers where the soprano did. Then the second subject upside
// down, from the soprano down, while the others go on singing. A roll
// into the soprano's entry at bar 19.
// parents: THE PERSONS, THE BELLS, THE CLOCK
const secSPECULUM = stack(satb(SPECULUM_S, SPECULUM_A, SPECULUM_T, SPECULUM_B),
  tick, bells(SPECULUM_TIN, .11).mask(Q), wheel(1800, .07).mask(NOT_Q),
  roll.mask(onBars(28, 18, 28)), crash.mask(onBars(28, 19)))

// VII. LEX. "In his duobus mandatis universa lex pendet": the Law held.
// The first subject in the bass, every note four times as long, the
// sub holding it too, four to the bar; over it the second subject and
// its mirror. The riser climbs the last four bars toward the dark.
// parents: THE PERSONS, THE BELLS, THE CLOCK
const secLEX = stack(satb(LEX_S, LEX_A, LEX_T, LEX_B), pad(LEX_B, .07),
  tick, bells(LEX_TIN, .11).mask(Q), wheel(1800, .07).mask(NOT_Q),
  riser(4).mask(fromBar(16, 13)))

// VIII. GOLGOTHA, in seven parts, as in the short form: the breakdown.
// parents: THE CLOCK, THE LINES MADE BY RULE, THE VEIL AND THE EARTH, THE HAMMER
// "From the sixth hour there was darkness over all the land": the clock
// alone, nothing but the mechanism, the acid shut down dark; the hammer.
const dark = stack(tick, wheel(500, .06), hammer('rim').gain(.25).pan(.35).orbit(1))
// "Eli, Eli, lamma sabacthani": the clock stutters
const cry = stack(tick.degradeBy(.5), solo(ELI), vox("<eli_eli ~>"))
// "This man calleth for Elias": the crowd, and a wind that does not come
const elias = stack(satb(ELIAM, '', '', '', .24), whirlwind, vox("<elias ~>", .9))
// "It is finished": the clock stops
const finished = stack(solo(CONSUMMATUM, .26), vox("<finished>"))
// the veil, top to bottom; the earth quakes; the rocks rend
const rent = stack(veil, quake, rocks, timpani.mask("<0 1>"))
// "Truly this was the Son of God": one man, alone
const centurion = stack(solo(VERE_SOLO_S, .28), vox("<truly ~>"))
const secGOLGOTHA = arrange(
  [4, dark], [2, cry], [2, elias], [1, finished], [2, rent], [2, centurion], [3, silence],
)

// IX. VERE. The stone (Matthew 28:2): the drop. Out of three bars of
// nothing the kick lands with the earthquake and a crash; the clock and
// the bells return, and his line is taken up: two voices, three, four.
// parents: THE PERSONS, THE CLOCK, THE BELLS, THE VEIL AND THE EARTH
const secVERE = arrange(
  [2, stack(satb(VERE_DUO_S, '', '', VERE_DUO_B), quake.mask("<1 0>"), crash.mask("<1 0>"), tick,
    vox("<truly_high ~>"))],
  [2, stack(satb(VERE_TRIO_S, VERE_TRIO_A, '', VERE_TRIO_B), clock, bells(VERE_TIN), vox("<truly_all ~>"))],
  [4, stack(satb(VERE_TUTTI_S, VERE_TUTTI_A, VERE_TUTTI_T, VERE_TUTTI_B), clock, bells(VERE_TIN),
    vox("<[truly,truly_high] ~ truly_all ~>"))],
)

// X. CAPUT, in the tenor and the bass. After the stone the clock and
// the bells sound together.
// parents: THE PERSONS, THE BELLS, THE CLOCK
const secCAPUT_III = stack(satb(CAPUT_III_S, CAPUT_III_A, CAPUT_III_T, CAPUT_III_B), bells(CAPUT_III_TIN, .1), clock,
  roll.mask(onBars(6, 6)))

// XI. IN UNUM. "That also he should gather together in one the children
// of God that were scattered abroad" (John 11:52). The entries drawn
// close: the first subject three bars apart (four in the exposition),
// the second a half note apart (three bars in the exposition), then
// both subjects in turn, two bars apart. A crash at each stretto's start.
// parents: THE PERSONS, THE BELLS, THE CLOCK
const secIN_UNUM = stack(satb(IN_UNUM_S, IN_UNUM_A, IN_UNUM_T, IN_UNUM_B), bells(IN_UNUM_TIN), clock,
  crash.mask(onBars(27, 1, 13, 20)), roll.mask(onBars(27, 12, 19, 27)))

// XII. CAPUT, in the soprano and the bass, two octaves apart.
// parents: THE PERSONS, THE BELLS, THE CLOCK
const secCAPUT_IV = stack(satb(CAPUT_IV_S, CAPUT_IV_A, CAPUT_IV_T, CAPUT_IV_B), bells(CAPUT_IV_TIN, .1), clock,
  riser(5), roll.mask(onBars(5, 5)))

// XIII. DUOBUS. Both commandments at once, the second a half note after
// the first: as in the short form, the first below; then both in the
// mirror; then with the voices exchanged, the second below the first.
// Then the household hangs on them. The peak of the track.
// parents: THE PERSONS, THE BELLS, THE CLOCK, THE HOUSEHOLD HANGS, THE HAMMER
const secDUOBUS = arrange(
  [4, stack(satb(DUOBUS_S, DUOBUS_A, DUOBUS_T, DUOBUS_B), bells(DUOBUS_TIN), clock, crash.mask("<1 0 0 0>"))],
  [4, stack(satb(DUOBUS_M_S, DUOBUS_M_A, DUOBUS_M_T, DUOBUS_M_B), bells(DUOBUS_M_TIN), clock, crash.mask("<1 0 0 0>"))],
  [4, stack(satb(DUOBUS_X_S, DUOBUS_X_A, DUOBUS_X_T, DUOBUS_X_B), bells(DUOBUS_X_TIN), clock,
    crash.mask("<1 0 0 0>"), viri(.06), canticle(.14), hammer().gain(.22).pan(.35).orbit(1),
    vox("<on_these_two ~ things_new_and_old ~>"))],
)

// XIV. FUNDAMENTUM. "For other foundation can no man lay than that is
// laid." The bass holds E, the final: eight bars of E in the sub, four
// to the bar, as at the start; over it the second subject and its
// mirror in turn, a bar apart, in the alto, the soprano and the tenor.
// parents: THE PERSONS, THE BELLS, THE CLOCK, I. PENDET (the pedal)
const secFUNDAMENTUM = stack(satb(FUNDAMENTUM_S, FUNDAMENTUM_A, FUNDAMENTUM_T, FUNDAMENTUM_B),
  pedal, bells(FUNDAMENTUM_TIN), clock, roll.mask(onBars(8, 8)))

// XV. AMEN. The phrygian cadence: the bass falls a semitone, F to E,
// and the third is raised, the light. The clock has had its say; the
// chords ring without it. Then, in the silence, the line Tallis set:
// "If ye love me, keep my commandments."
// parents: THE MODE
const FCHORD = "[f2,c3,a3,d4]", ECHORD = "[e2,b2,g#3,e4]"
const secAMEN = stack(arrange(
  [2, stack(
    note(FCHORD).s('gm_choir_aahs').attack(.1).release(1.5).gain(.7).room(.7).roomsize(6).orbit(6),
    note(FCHORD).s('supersaw').unison(5).detune(.25).attack(.1).release(1.5).lpf(1600).gain(.25).room(.6).orbit(4),
    note("f1").s('sine').attack(.02).release(1.5).lpf(90).gain(.4).orbit(4),
  ).slow(2)],
  [2, stack(
    note(ECHORD).s('gm_choir_aahs').attack(.1).release(3).gain(.75).room(.7).roomsize(6).orbit(6),
    note(ECHORD).s('supersaw').unison(5).detune(.25).attack(.1).release(3).lpf(2400).gain(.3).room(.7).orbit(4),
    note("e1").s('sine').attack(.02).release(3).lpf(90).gain(.45).orbit(4),
    note("[e5,g#5,b5]").s('gm_celesta').release(3).gain(.3).room(.7).orbit(7),
    crash,
  ).slow(2)],
  [4, silence],
), vox("<~ ~ ~ ~ if_ye_love_me ~ ~ ~>"))

// ============================================================
// THE ARRANGEMENT
// ============================================================
arrange(
  [8,  secPENDET],
  [16, secDILIGES],
  [6,  secCAPUT_I],
  [12, secSIMILE],
  [6,  secCAPUT_II],
  [28, secSPECULUM],
  [16, secLEX],
  [16, secGOLGOTHA],
  [8,  secVERE],
  [6,  secCAPUT_III],
  [27, secIN_UNUM],
  [5,  secCAPUT_IV],
  [12, secDUOBUS],
  [8,  secFUNDAMENTUM],
  [8,  secAMEN],
).postgain(.7) // 3 dB of headroom: the club form clips when rendered
