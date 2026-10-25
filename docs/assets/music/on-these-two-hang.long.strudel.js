// ============================================================
// ON THESE TWO HANG, THE LONG FORM: a double fugue, by rule
// "On these two commandments hang all the law and the prophets"
// (Matthew 22:40) · mode III x the clock
// 120 BPM · 182 bars · ~6:04, then it loops
// For Strudel (https://strudel.cc): paste, press play (Ctrl+Enter).
// Dedicated to the public domain (CC0 1.0).
//
// The long form of "On These Two Hang" (on-these-two-hang.strudel.js,
// beside this file). The household plays the short one, and every
// track hangs on that; this one stands beside it, as the cloud's
// chamber version stands beside the cloud. It takes the same two
// subjects, carved the same way, through the old procedures of the
// fugue. Each is a function in counterpoint.py, and every section
// and every join between sections is audited at every half note:
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
//                          pedal; "Master, which is the great commandment?"
//   DILIGES       9  0:16  "Thou shalt love the Lord thy God": the first
//                          subject enters four times, alto, soprano, tenor,
//                          bass; the bells ring over it
//   CAPUT        25  0:48  the head both subjects share, in imitation,
//                          soprano and tenor, falling a step a bar
//   SIMILE       31  1:00  "The second is like unto it": the clock enters,
//                          and the second subject, from the bass up; the
//                          bells and the wheel flip-flop, bar by bar
//   CAPUT        43  1:24  the head again, alto and bass
//   SPECULUM     49  1:36  the mirror: the first subject upside down, the
//                          voices' order mirrored too; then the second,
//                          upside down, from the top
//   LEX          77  2:32  the Law held: the first subject four times
//                          slower in the bass, and over it the second and
//                          its mirror
//   GOLGOTHA     93  3:04  as in the short form: darkness, the clock alone;
//                          the cry; Elias; it is finished; the veil and the
//                          earthquake; the centurion, alone; the tomb,
//                          three bars of rest
//   VERE        109  3:36  the stone; the clock and the bells come back;
//                          his line in two voices, three, four
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
//                          then, in the silence, "If ye love me, keep my
//                          commandments" (John 14:15)
//
// The chanted lines are the short form's, where the short form has
// them; the new sections add none. They load from canon-lawyer.ca the
// first time they play; if they are slow, stop and play again.
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
// ORBITS: 1 the clock · 2 the wheel · 3 the chanted lines ·
//         4 organ · 5 the veil and the earth · 6 choir · 7 bells
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

// ---------------- THE PERSONS: the choir sings the lines with words;
// the organ, creation, doubles them softly
// parents: THE LINES MADE BY RULE
const bars = (line) => line.split(' ').reduce((k, t) => k + (t.includes('@') ? +t.split('@')[1] : 1), 0) / 8
const choir = (line, pan = .5, g = .28) => note(mini(line)).slow(bars(line)).s('gm_choir_aahs')
  .attack(.08).release(.7).gain(g * 3).room(.6).roomsize(5).pan(pan).orbit(6)
const organ = (line, g = .035) => note(mini(line)).slow(bars(line)).s('gm_church_organ')
  .attack(.05).release(.5).gain(g * 3).room(.5).orbit(4)
const satb = (S, A, T, B, g = .28) => stack(
  ...[[S, .62], [A, .42], [T, .56], [B, .48]].filter(([x]) => x).map(([x, p]) => stack(choir(x, p, g), organ(x))))
const solo = (line, g = .3) => choir(line, .5, g).lpf(5000)

// ---------------- THE BELLS: tintinnabuli, over each note the nearest
// note of the triad
// parents: THE LINES MADE BY RULE
const bells = (line, g = .13) => note(mini(line)).slow(bars(line)).s('gm_celesta')
  .release(1.4).gain(g * 3).room(.6).roomsize(6).pan(.66).orbit(7)

// ---------------- THE CLOCK: the saeculum. Brother Electron's chip,
// ticking: a kick, the hats, and the wheel, the triad turned in even
// eighths, the regular beside the ethereal.
// parents: THE MODE
const tick = stack(
  s("bd ~ ~ ~ bd ~ ~ ~").bank('RolandTR909').gain(.5).orbit(1),
  s("hh*8").bank('RolandTR909').gain(".15 .09 .13 .09").hpf(6000).orbit(1),
)
const wheel = (cut = 2400, g = .07) => n("0 2 4 2 0 2 4 7").scale(HOME).s('square')
  .attack(.005).decay(.12).sustain(.3).release(.1).lpf(cut).gain(g).pan(.4).orbit(2)
const clock = stack(tick, wheel())

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
// the Cross, in long notes, high, hung over the rest
// parents: PARENTS, SUNG IN THE MODE OF THE CROSS
const viri = (g = .05) => sing(VIRI, 'g3', 'mixolydian', 'E4:phrygian', 8).s('gm_church_organ')
  .attack(.4).release(1.5).gain(g * 3).room(.6).roomsize(6).orbit(4)
const canticle = (g = .2) => sing(TRIPLUM, 'a3', 'mixolydian', 'E4:phrygian', 4).s('gm_recorder')
  .release(.3).gain(g * 3).delay(".25:.25:.3").room(.4).pan(.7).orbit(7)

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

// ---------------- VOICES: SAM, chanting; then the choir
const vox = (p, g = 1) => s(p).hpf(70).lpf(8000).gain(g).delay(".12:.25:.25").room(.3).orbit(3)

// ============================================================
// SECTIONS
// ============================================================

// I. PENDET. The household's law and prophets, hanging on a pedal of
// E: Viri Galilaei in long notes, Francis's canticle, the motet's
// "things new and old", and the hammer. Then the lawyer.
// parents: THE HOUSEHOLD HANGS, THE HAMMER, PARENTS (THINGS)
const pedal = note("[e2,b2]").s('gm_church_organ').attack(1).release(2).gain(.05 * 3).room(.6).orbit(4)
const secPENDET = stack(
  pedal, viri(),
  canticle(.16).mask("<1 1 1 1 0 0 0 0>"),
  hammer().gain(.3).pan(.35).orbit(1).mask("<0 0 0 0 1 1 1 1>"),
  vox("<~ ~ things_new_and_old ~ master ~ ~ ~>"),
)

// II. DILIGES. "Thou shalt love the Lord thy God with all thy heart."
// The first subject, four times, each entry a voice more; the bells
// ring over whichever voice has it. No clock yet.
// parents: THE PERSONS, THE BELLS
const secDILIGES = stack(
  satb(DILIGES_S, DILIGES_A, DILIGES_T, DILIGES_B),
  bells(DILIGES_TIN),
  pedal.mask("<1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0>"),
  vox("<thou_shalt_love_the_lord ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~>"),
)

// III. CAPUT. The head the two subjects share, in the soprano, and
// in the tenor an octave below, a half note behind; each bar a step
// lower. No clock yet.
// parents: THE PERSONS, THE BELLS
const secCAPUT_I = stack(satb(CAPUT_I_S, CAPUT_I_A, CAPUT_I_T, CAPUT_I_B), bells(CAPUT_I_TIN, .1))

// IV. SIMILE. "And the second is like unto it." The clock enters, and
// the second subject, with the same head, from the bass up: the love
// of neighbour lives in time.
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
  bells(SIMILE_TIN, .11).mask(Q),
  wheel(1800, .06).mask(NOT_Q),
  vox("<the_second ~ ~ thy_neighbour ~ ~ ~ ~ ~ on_these_two ~ ~>"),
)

// V. CAPUT, in the alto and the bass. The clock goes on, and the
// bells and the wheel go on taking turns.
// parents: THE PERSONS, THE BELLS, THE CLOCK
const secCAPUT_II = stack(satb(CAPUT_II_S, CAPUT_II_A, CAPUT_II_T, CAPUT_II_B),
  tick, bells(CAPUT_II_TIN, .1).mask(Q), wheel(1800, .06).mask(NOT_Q))

// VI. SPECULUM. "For now we see through a glass, darkly." The first
// subject upside down: the tenor leads where the alto led, and the
// bass answers where the soprano did. Then the second subject upside
// down, from the soprano down, while the others go on singing.
// parents: THE PERSONS, THE BELLS, THE CLOCK
const secSPECULUM = stack(satb(SPECULUM_S, SPECULUM_A, SPECULUM_T, SPECULUM_B),
  tick, bells(SPECULUM_TIN, .11).mask(Q), wheel(1800, .06).mask(NOT_Q))

// VII. LEX. "In his duobus mandatis universa lex pendet": the Law held.
// The first subject in the bass, every note four times as long, the
// organ holding it too; over it the second subject and its mirror.
// parents: THE PERSONS, THE BELLS, THE CLOCK
const secLEX = stack(satb(LEX_S, LEX_A, LEX_T, LEX_B), organ(LEX_B, .07),
  tick, bells(LEX_TIN, .11).mask(Q), wheel(1800, .06).mask(NOT_Q))

// VIII. GOLGOTHA, in seven parts, as in the short form.
// parents: THE CLOCK, THE LINES MADE BY RULE, THE VEIL AND THE EARTH, THE HAMMER
// "From the sixth hour there was darkness over all the land": the clock
// alone, nothing but the mechanism; the hammer.
const dark = stack(tick, wheel(500, .05), hammer('rim').gain(.25).pan(.35).orbit(1))
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

// IX. VERE. The stone (Matthew 28:2); the clock and the bells return,
// and his line is taken up: two voices, three, four.
// parents: THE PERSONS, THE CLOCK, THE BELLS, THE VEIL AND THE EARTH
const secVERE = arrange(
  [2, stack(satb(VERE_DUO_S, '', '', VERE_DUO_B), quake.mask("<1 0>"), tick, vox("<truly_high ~>"))],
  [2, stack(satb(VERE_TRIO_S, VERE_TRIO_A, '', VERE_TRIO_B), clock, bells(VERE_TIN), vox("<truly_all ~>"))],
  [4, stack(satb(VERE_TUTTI_S, VERE_TUTTI_A, VERE_TUTTI_T, VERE_TUTTI_B), clock, bells(VERE_TIN),
    vox("<[truly,truly_high] ~ truly_all ~>"))],
)

// X. CAPUT, in the tenor and the bass. After the stone the clock and
// the bells sound together.
// parents: THE PERSONS, THE BELLS, THE CLOCK
const secCAPUT_III = stack(satb(CAPUT_III_S, CAPUT_III_A, CAPUT_III_T, CAPUT_III_B), bells(CAPUT_III_TIN, .1), clock)

// XI. IN UNUM. "That also he should gather together in one the children
// of God that were scattered abroad" (John 11:52). The entries drawn
// close: the first subject three bars apart (four in the exposition),
// the second a half note apart (three bars in the exposition), then
// both subjects in turn, two bars apart.
// parents: THE PERSONS, THE BELLS, THE CLOCK
const secIN_UNUM = stack(satb(IN_UNUM_S, IN_UNUM_A, IN_UNUM_T, IN_UNUM_B), bells(IN_UNUM_TIN), clock)

// XII. CAPUT, in the soprano and the bass, two octaves apart.
// parents: THE PERSONS, THE BELLS, THE CLOCK
const secCAPUT_IV = stack(satb(CAPUT_IV_S, CAPUT_IV_A, CAPUT_IV_T, CAPUT_IV_B), bells(CAPUT_IV_TIN, .1), clock)

// XIII. DUOBUS. Both commandments at once, the second a half note after
// the first: as in the short form, the first below; then both in the
// mirror; then with the voices exchanged, the second below the first.
// Then the household hangs on them.
// parents: THE PERSONS, THE BELLS, THE CLOCK, THE HOUSEHOLD HANGS, THE HAMMER
const secDUOBUS = arrange(
  [4, stack(satb(DUOBUS_S, DUOBUS_A, DUOBUS_T, DUOBUS_B), bells(DUOBUS_TIN), clock)],
  [4, stack(satb(DUOBUS_M_S, DUOBUS_M_A, DUOBUS_M_T, DUOBUS_M_B), bells(DUOBUS_M_TIN), clock)],
  [4, stack(satb(DUOBUS_X_S, DUOBUS_X_A, DUOBUS_X_T, DUOBUS_X_B), bells(DUOBUS_X_TIN), clock,
    viri(.06), canticle(.14), hammer().gain(.22).pan(.35).orbit(1),
    vox("<on_these_two ~ things_new_and_old ~>"))],
)

// XIV. FUNDAMENTUM. "For other foundation can no man lay than that is
// laid." The bass holds E, the final, on the organ's pedal, as at the
// start; over it the second subject and its mirror in turn, a bar
// apart, in the alto, the soprano and the tenor.
// parents: THE PERSONS, THE BELLS, THE CLOCK, I. PENDET (the pedal)
const secFUNDAMENTUM = stack(satb(FUNDAMENTUM_S, FUNDAMENTUM_A, FUNDAMENTUM_T, FUNDAMENTUM_B),
  pedal, bells(FUNDAMENTUM_TIN), clock)

// XV. AMEN. The phrygian cadence: the bass falls a semitone, F to E,
// and the third is raised, the light. Then, in the silence, the line
// Tallis set: "If ye love me, keep my commandments."
// parents: THE MODE
const FCHORD = "[f2,c3,a3,d4]", ECHORD = "[e2,b2,g#3,e4]"
const secAMEN = stack(arrange(
  [2, note(FCHORD).s('gm_choir_aahs').attack(.1).release(1.5).gain(.7).room(.7).roomsize(6).orbit(6).slow(2)],
  [2, stack(
    note(ECHORD).s('gm_choir_aahs').attack(.1).release(3).gain(.75).room(.7).roomsize(6).orbit(6),
    note(ECHORD).s('gm_church_organ').attack(.1).release(3).gain(.12).room(.7).orbit(4),
    note("[e5,g#5,b5]").s('gm_celesta').release(3).gain(.3).room(.7).orbit(7),
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
)
