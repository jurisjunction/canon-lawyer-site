// ============================================================
// ON THESE TWO HANG, THE CATHEDRAL FORM: a double fugue for the household,
// sounded for a church
// "On these two commandments hang all the law and the prophets"
// (Matthew 22:40) · mode III x the clock
// 120 BPM · 76 bars · ~2:32, then it loops
// For Strudel (https://strudel.cc): paste, press play (Ctrl+Enter).
// Dedicated to the public domain (CC0 1.0).
//
// The short form of "On These Two Hang" (on-these-two-hang.strudel.js,
// beside this file), sounded as a parish or a cathedral could pray with
// it. The household plays the short one, and every track hangs on that;
// this stands beside it, as the organ edition (scores/on-these-two-hang-
// organ.pdf) stands beside it on paper. Nothing in the counterpoint is
// touched: the choir sings every note the published score and MIDI
// have, and the sections, the bars and the order are the short form's.
// What changes is creation's sound, and the room.
//   * The room is a stone one. Everything stands in a long reverb; the
//     choir's attacks are slow and its releases long, as a choir in a
//     nave is heard.
//   * The organ doubles the choir colla parte, Principal 8', soft, as it
//     did; the pedal holds the fifth at the start, and 16' under the
//     earthquake.
//   * The bells, the tintinnabuli, ring on handbells (a glockenspiel)
//     with a celesta under them.
//   * The clock, the saeculum, is still here, and it is good: a soft
//     drum on the half bar and a woodblock in eighths, as the organ
//     edition gives the percussionist, played quietly and far; and the
//     wheel, the triad turned in even eighths, on a harp. It still
//     enters three bars into "Simile" and stays; before the Cross the
//     bells and the harp still take turns, bar by bar, a flip-flop; in
//     the darkness the harp is muffled and the drum alone; at "It is
//     finished" the clock stops; at the stone it returns.
//   * The carpenter's hammer, in Morse, is a temple block (a low
//     woodblock), as the organ edition writes it; the rocks the same.
//   * The veil is still a falling noise, far off; the earth still quakes,
//     with the organ's 32' under it; the timpani, as before.
//   * "The light", at the Amen: a single bell tolls E as the third is
//     raised.
//   * The words. The ascended choir's lines (the Lord's words, the cry,
//     the confession) sound as the short form has them, in the room.
//     SAM, the 1982 speech program, who chants the lawyer, the crowd and
//     the centurion, is off by default (SAM = 0): his voice is not a
//     register for prayer. A reader or the priest could say those lines
//     where the organ edition marks them; set SAM = 1 to hear his.
//   * A church may want it slower. Change the first line to
//     setcpm(100/4) and everything keeps its shape: Strudel counts in
//     bars, not seconds.
//
// The notes are made by rule (counterpoint.py, beside this file):
//   * Each subject is carved from its words, as Josquin carved a Mass
//     from a duke's name (soggetto cavato): each syllable's vowel picks
//     the solmization syllable with the same vowel, u ut, e re, i mi,
//     o sol, a fa. The words are the Vulgate's. So "Diliges Dominum"
//     and "Diliges proximum" begin with the same six notes, because
//     their vowels are the same: the second is like unto it. The cry,
//     "lamma sabacthani", hangs on fa and falls to mi, the mode's own
//     final; the crowd's "Eliam vocat iste" goes up and comes down.
//   * The voices around each subject are found by a search under
//     Fux's rules (1725), and every half note is audited.
//   * The bells are tintinnabuli, a procedure Arvo Part made his own:
//     over each note of the melody the nearest note of the triad.
//     His music is not quoted; his way of ringing is followed.
//
// The voices are persons: the choir sings the subjects, the parts
// that have words. The instruments are creation, made to sing to God
// through the law of man, as in "Brother Electron"; Strudel is one of
// them. The clock is the saeculum, and it is good. The darkness at
// the sixth hour is not the clock stopping: it is the clock alone,
// nothing but the mechanism, the bells and voices traced out. Then
// the cry; then "it is finished", and the clock stops; then the veil
// rent from the top to the bottom, and the earth quakes. One Roman
// says "Truly this was the Son of God", alone. Then the tomb: God's
// sabbath rest (CCC 624), and in a score a rest is silence. Then the
// stone (Matthew 28:2), the clock returns with the bells, and what
// one man said on Friday the whole household sings on Sunday: one
// voice, then two, three, all.
//
// The code is a DAG, like the essays. Each part names its PARENTS,
// the parts it is made from, which stand above it.
//
// PARENTS. A track carries its parents in its own material. This one
// has four, so it quotes all four, each line with a short hash of the
// parent's original (sha256 of the quoted text, first 12 hex):
//   whether-the-cloud.strudel.js   VIRI       fd123dbc28e8
//   what-is-to-be-done.strudel.js  CARPENTER  3b8716d43c19
//   brother-electron.strudel.js    TRIPLUM    2b82b56f32b5
//   a-new-song.strudel.js          THINGS     ab645d0aae4c
//
// TIMELINE (bar / time):
//   PENDET     1  0:00  the household's law and prophets hang on a
//                       pedal; the lawyer's question (a reader, or SAM)
//   DILIGES    9  0:16  "Thou shalt love the Lord thy God": the first
//                       subject enters four times, alto, soprano, tenor,
//                       bass; the handbells ring over it
//   SIMILE    25  0:48  "The second is like unto it": the clock enters,
//                       the saeculum, and the second subject, from the
//                       bass up; the bells and the harp flip-flop, bar
//                       by bar
//   GOLGOTHA  37  1:12  darkness, the clock alone; the cry; Elias; it is
//                       finished; the veil and the earthquake; the
//                       centurion, alone; the tomb, three bars of rest
//   VERE      53  1:44  the stone; the clock and the bells come back;
//                       his line in two voices, three, four
//   DUOBUS    61  2:00  both commandments at once, and the household
//                       hangs on them: "on these two commandments hang
//                       all the law and the prophets"
//   AMEN      69  2:16  the phrygian cadence, F to E, and the light, a
//                       bell; then, in the silence, "If ye love me, keep
//                       my commandments" (John 14:15)
//
// The sung lines load from canon-lawyer.ca the first time they play;
// if they are slow, stop and play again.
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
// "python3 counterpoint.py --check" confirms they are quoted as made)
// The subjects, carved from the Vulgate:
//   DILIGES      Diliges Dominum Deum tuum ex toto corde tuo (Mt 22:37)
//   SIMILE       Diliges proximum tuum sicut teipsum (Mt 22:39)
//   ELI          Eli, Eli, lamma sabacthani (Mt 27:46)
//   ELIAM        Eliam vocat iste (Mt 27:47)
//   CONSUMMATUM  Consummatum est (Jn 19:30)
//   VERE         Vere Filius Dei erat iste (Mt 27:54)
// and the voices found around them, S A T B, and the bells (TIN).
// parents: THE MODE
const DILIGES = 'e4@2 e4 d4 g4@2 e4 c4 d4@2 c4 c4@2 c4 d4@2 g4@2 g4 g4@2 d4 c4@2 g3@8'
const SIMILE = 'e4@2 e4 d4 g4@2 e4 c4 c4@2 c4 e4@2 c4 d4 e4@2 c4@7'
const ELI = 'd4@2 e4 d4@2 e4 f4@2 f4 f4 f4@2 f4 e4@3'
const ELIAM = 'd4 e4@2 f4 g4@2 f4 e4@2 d4@7'
const CONSUMMATUM = 'g4 c5 f5@2 c5 d5@3'
const VERE = 'd4@2 d4 e4@2 e4 c4 d4@2 e4 d4@2 f4 e4@2 d4'
const DILIGES_TIN = 'g5@2 g5 e5 b5@2 g5 e5 e5@2 e5 e5@2 e5 e5@2 b5@2 b5 b5@2 e5 e5@2 b4@8 e5@2 e5 b4 e5@2 e5 b4 b4@2 b4 b4@2 b4 b4@2 e5@2 e5 e5@2 b4 b4@2 e4@8 g5@2 g5 e5 b5@2 g5 e5 e5@2 e5 e5@2 e5 e5@2 b5@2 b5 b5@2 e5 e5@2 b4@8 e5@2 e5 b4 e5@2 e5 b4 b4@2 b4 b4@2 b4 b4@2 e5@2 e5 e5@2 b4 b4@2 e4@8'
const DILIGES_S = '~@32 b4@2 b4 a4 d5@2 b4 g4 a4@2 g4 g4@2 g4 a4@2 d5@2 d5 d5@2 a4 g4@2 d4@8 b4@4 g4@4 a4@4 a4@4 g4@4 g4@4 e4@4 d4@4 b4@4 b4@4 e5@4 e5@4 d5@4 b4@4 d5@4 a4@4'
const DILIGES_A = 'e4@2 e4 d4 g4@2 e4 c4 d4@2 c4 c4@2 c4 d4@2 g4@2 g4 g4@2 d4 c4@2 g3@8 d4@4 b3@4 c4@4 c4@4 b3@4 g3@4 b3@4 g3@4 b3@4 b3@4 a3@4 a3@4 b3@4 d4@4 b3@4 g3@4 d4@4 d4@4 e4@4 e4@4 f4@4 d4@4 f4@4 d4@4'
const DILIGES_T = '~@32 ~@32 e3@2 e3 d3 g3@2 e3 c3 d3@2 c3 c3@2 c3 d3@2 g3@2 g3 g3@2 d3 c3@2 g2@8 g3@4 b3@4 e3@4 e3@4 a3@4 b3@4 a3@4 a3@4'
const DILIGES_B = '~@32 ~@32 ~@32 b2@2 b2 a2 d3@2 b2 g2 a2@2 g2 g2@2 g2 a2@2 d3@2 d3 d3@2 a2 g2@2 d2@8'
const SIMILE_S = '~@24 ~@24 ~@24 b4@2 b4 a4 d5@2 b4 g4 g4@2 g4 b4@2 g4 a4 b4@2 g4@7'
const SIMILE_A = '~@24 ~@24 e4@2 e4 d4 g4@2 e4 c4 c4@2 c4 e4@2 c4 d4 e4@2 c4@7 d4@4 b3@4 b3@4 b3@4 b3@4 c4@4'
const SIMILE_T = '~@24 b3@2 b3 a3 d4@2 b3 g3 g3@2 g3 b3@2 g3 a3 b3@2 g3@7 b3@4 c4@4 a3@4 c4@4 a3@4 g3@4 d3@4 g3@4 e3@4 g3@4 e3@4 g3@4'
const SIMILE_B = 'e3@2 e3 d3 g3@2 e3 c3 c3@2 c3 e3@2 c3 d3 e3@2 c3@7 d3@4 b2@4 b2@4 g2@4 b2@4 c3@4 g3@4 e3@4 c3@4 a2@4 c3@4 c3@4 b2@4 g2@4 g2@4 e2@4 g2@4 c3@4'
const SIMILE_TIN = 'g5@2 g5 e5 b5@2 g5 e5 e5@2 e5 g5@2 e5 e5 g5@2 e5@7 e5@2 e5 b4 e5@2 e5 b4 b4@2 b4 e5@2 b4 b4 e5@2 b4@7 g5@2 g5 e5 b5@2 g5 e5 e5@2 e5 g5@2 e5 e5 g5@2 e5@7 e5@2 e5 b4 e5@2 e5 b4 b4@2 b4 e5@2 b4 b4 e5@2 b4@7'
const DUOBUS_TIN = '~@4 e5@2 e5 b4 e5@2 e5 b4 b4@2 b4 e5@2 b4 b4 e5@2 b4@7 ~@4'
const DUOBUS_S = '~@4 b4@2 b4 a4 d5@2 b4 g4 g4@2 g4 b4@2 g4 a4 b4@2 g4@7 ~@4'
const DUOBUS_A = 'b4@4 g4@4 b4@4 g4@4 e4@4 g4@4 e4@4 d4@4'
const DUOBUS_T = 'b3@4 e4@4 d4@4 e4@4 b3@4 b3@4 b3@4 g3@4'
const DUOBUS_B = 'e3@2 e3 d3 g3@2 e3 c3 d3@2 c3 c3@2 c3 d3@2 g3@2 g3 g3@2 d3 c3@2 g2@8'
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

// ---------------- THE ROOM: a stone one. Every sound stands in it.
// parents: none
const NAVE = (p, g = .85) => p.room(g).roomsize(8)
const SAM = 0 // 1 brings back SAM's chanted lines; the choir's are always on

// ---------------- THE PERSONS: the choir sings the lines with words;
// the organ, creation, doubles them softly, Principal 8', colla parte
// parents: THE LINES MADE BY RULE, THE ROOM
const bars = (line) => line.split(' ').reduce((k, t) => k + (t.includes('@') ? +t.split('@')[1] : 1), 0) / 8
const choir = (line, pan = .5, g = .28) => NAVE(note(mini(line)).slow(bars(line)).s('gm_choir_aahs')
  .attack(.22).release(1.4).lpf(5200).gain(g * 3).pan(pan).orbit(6))
const organ = (line, g = .03) => NAVE(note(mini(line)).slow(bars(line)).s('gm_church_organ')
  .attack(.08).release(.9).lpf(3000).gain(g * 3).orbit(4), .7)
const satb = (S, A, T, B, g = .28) => stack(
  ...[[S, .62], [A, .42], [T, .56], [B, .48]].filter(([x]) => x).map(([x, p]) => stack(choir(x, p, g), organ(x))))
const solo = (line, g = .3) => choir(line, .5, g).lpf(4800).release(2.2)

// ---------------- THE BELLS: tintinnabuli, over each note the nearest
// note of the triad; handbells, with a celesta under them
// parents: THE LINES MADE BY RULE, THE ROOM
const bells = (line, g = .13) => stack(
  NAVE(note(mini(line)).slow(bars(line)).s('gm_glockenspiel').release(2.2).gain(g * 1.6).pan(.66).orbit(7)),
  NAVE(note(mini(line)).slow(bars(line)).s('gm_celesta').release(1.8).gain(g * 2).pan(.6).orbit(7)),
)

// ---------------- THE CLOCK: the saeculum. Brother Electron's chip,
// ticking, as the organ edition gives it to one player: a soft drum on
// the half bar, a woodblock in eighths, far off; and the wheel, the
// triad turned in even eighths, on a harp. The regular beside the
// ethereal.
// parents: THE MODE, THE ROOM
const tick = stack(
  NAVE(note("e2 ~ ~ ~ e2 ~ ~ ~").s('gm_taiko_drum').lpf(260).gain(.42).orbit(1), .5),
  NAVE(note("e4*8").s('gm_woodblock').gain(".11 .06 .09 .06").lpf(2600).pan(.4).orbit(1), .4),
)
const wheel = (cut = 2400, g = .07) => NAVE(n("0 2 4 2 0 2 4 7").scale(HOME).s('gm_orchestral_harp')
  .release(.6).lpf(cut).gain(g * 2.2).pan(.4).orbit(2), .7)
const clock = stack(tick, wheel())

// ---------------- THE HAMMER: the carpenter's, in Morse, as the parents
// tapped it; dot 1 sixteenth, dash 3; 1 between signs, 3 between letters,
// 7 between words. Here a temple block, as the organ edition writes it.
// parents: PARENTS (CARPENTER)
const CODE = { A: '.-', C: '-.-.', E: '.', H: '....', I: '..', N: '-.', O: '---',
               P: '.--.', R: '.-.', S: '...', T: '-' }
const morse = (text) => text.split(' ').map((word) =>
  word.split('').map((ch) =>
    CODE[ch].split('').map((sign) => (sign === '.' ? 'x' : 'x@3')).join(' ~ ')
  ).join(' ~@3 ')
).join(' ~@7 ') + ' ~@7'
const units = (talea) => talea.split(' ').reduce((k, t) => k + (t.includes('@') ? +t.split('@')[1] : 1), 0)
const hammer = (pitch = 'e2') => {
  const talea = morse(CARPENTER)
  return NAVE(note(pitch).s('gm_woodblock').struct(mini(talea)).slow(units(talea) / 16).lpf(1800), .5)
}

// ---------------- THE HOUSEHOLD HANGS: the parents' lines in the mode of
// the Cross, in long notes, high, hung over the rest: the Ascension line
// on the organ, the canticle on a recorder, far up in the room
// parents: PARENTS, SUNG IN THE MODE OF THE CROSS, THE ROOM
const viri = (g = .05) => NAVE(sing(VIRI, 'g3', 'mixolydian', 'E4:phrygian', 8).s('gm_church_organ')
  .attack(.5).release(2).gain(g * 3).orbit(4))
const canticle = (g = .2) => NAVE(sing(TRIPLUM, 'a3', 'mixolydian', 'E4:phrygian', 4).s('gm_recorder')
  .attack(.03).release(.5).gain(g * 2.4).pan(.7).orbit(7))

// ---------------- THE VEIL AND THE EARTH: "the veil of the temple was
// rent in twain from the top to the bottom; and the earth did quake, and
// the rocks rent" (Matthew 27:51). Creation answers, with no words. The
// veil is a falling noise, far off; under the quake the organ's 32'.
// parents: THE ROOM
const veil = NAVE(s('white').lpf(saw.slow(2).range(9000, 150)).gain(saw.slow(2).range(.12, .015)).orbit(5), .6)
const quake = stack(
  s('brown').lpf(160).gain(sine.slow(2).range(.22, .36)).orbit(5),
  note("e1").s('sine').attack(.02).release(3).gain(.45).lpf(100).orbit(5),
  NAVE(note("e1").s('gm_church_organ').attack(.3).release(3).lpf(400).gain(.2).orbit(5), .7),
)
const rocks = NAVE(note("~ e2 ~ ~ e2 ~ ~ e2").s('gm_woodblock').lpf(1800).gain(.5).orbit(5), .6)
const timpani = NAVE(note("e2*8").s('gm_timpani').gain(".15 .18 .21 .24 .27 .3 .33 .36").orbit(5), .6)
// Elijah's whirlwind, which comes and does not come
const whirlwind = s('pink').bpf(saw.range(300, 3000)).gain(saw.range(0, .1)).orbit(5)

// ---------------- VOICES: the ascended choir, in the room; SAM, when asked
const vox = (p, g = 1) => NAVE(s(p).hpf(120).lpf(7000).gain(g).orbit(3), .6)
const sam = (p, g = 1) => SAM ? vox(p, g) : silence

// ============================================================
// SECTIONS
// ============================================================

// I. PENDET. The household's law and prophets, hanging on a pedal of
// E: Viri Galilaei in long notes, Francis's canticle, the motet's
// "things new and old", and the hammer. Then the lawyer.
// parents: THE HOUSEHOLD HANGS, THE HAMMER, PARENTS (THINGS)
const pedal = NAVE(note("[e2,b2]").s('gm_church_organ').attack(1).release(2.5).gain(.05 * 3).orbit(4))
const secPENDET = stack(
  pedal, viri(),
  canticle(.16).mask("<1 1 1 1 0 0 0 0>"),
  hammer().gain(.3).pan(.35).orbit(1).mask("<0 0 0 0 1 1 1 1>"),
  vox("<~ ~ things_new_and_old ~ ~ ~ ~ ~>"),
  sam("<~ ~ ~ ~ master ~ ~ ~>"),
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

// III. SIMILE. "And the second is like unto it." The clock enters, and
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

// IV. GOLGOTHA, in seven parts.
// parents: THE CLOCK, THE LINES MADE BY RULE, THE VEIL AND THE EARTH, THE HAMMER
// "From the sixth hour there was darkness over all the land": the clock
// alone, nothing but the mechanism, the harp muffled; the hammer.
const dark = stack(tick, wheel(500, .05), hammer().gain(.25).pan(.35).orbit(1))
// "Eli, Eli, lamma sabacthani": the clock stutters
const cry = stack(tick.degradeBy(.5), solo(ELI), vox("<eli_eli ~>"))
// "This man calleth for Elias": the crowd, and a wind that does not come
const elias = stack(satb(ELIAM, '', '', '', .24), whirlwind, sam("<elias ~>", .9))
// "It is finished": the clock stops
const finished = stack(solo(CONSUMMATUM, .26), vox("<finished>"))
// the veil, top to bottom; the earth quakes; the rocks rend
const rent = stack(veil, quake, rocks, timpani.mask("<0 1>"))
// "Truly this was the Son of God": one man, alone
const centurion = stack(solo(VERE_SOLO_S, .28), sam("<truly ~>"))
const secGOLGOTHA = arrange(
  [4, dark], [2, cry], [2, elias], [1, finished], [2, rent], [2, centurion], [3, silence],
)

// V. VERE. The stone (Matthew 28:2); the clock and the bells return,
// and his line is taken up: two voices, three, four.
// parents: THE PERSONS, THE CLOCK, THE BELLS, THE VEIL AND THE EARTH
const secVERE = arrange(
  [2, stack(satb(VERE_DUO_S, '', '', VERE_DUO_B), quake.mask("<1 0>"), tick, sam("<truly_high ~>"))],
  [2, stack(satb(VERE_TRIO_S, VERE_TRIO_A, '', VERE_TRIO_B), clock, bells(VERE_TIN), vox("<truly_all ~>"))],
  [4, stack(satb(VERE_TUTTI_S, VERE_TUTTI_A, VERE_TUTTI_T, VERE_TUTTI_B), clock, bells(VERE_TIN),
    vox("<~ ~ truly_all ~>"), sam("<[truly,truly_high] ~ ~ ~>"))],
)

// VI. DUOBUS. Both commandments at once, the second a half note after
// the first and a fifth above; then the household hangs on them.
// parents: THE PERSONS, THE BELLS, THE CLOCK, THE HOUSEHOLD HANGS, THE HAMMER
const secDUOBUS = arrange(
  [4, stack(satb(DUOBUS_S, DUOBUS_A, DUOBUS_T, DUOBUS_B), bells(DUOBUS_TIN), clock)],
  [4, stack(satb(DUOBUS_S, DUOBUS_A, DUOBUS_T, DUOBUS_B), bells(DUOBUS_TIN), clock,
    viri(.06), canticle(.14), hammer().gain(.22).pan(.35).orbit(1),
    vox("<on_these_two ~ things_new_and_old ~>"))],
)

// VII. AMEN. The phrygian cadence: the bass falls a semitone, F to E,
// and the third is raised, the light: a bell tolls E. Then, in the
// silence, the line Tallis set: "If ye love me, keep my commandments."
// parents: THE MODE, THE ROOM
const FCHORD = "[f2,c3,a3,d4]", ECHORD = "[e2,b2,g#3,e4]"
const secAMEN = stack(arrange(
  [2, stack(
    NAVE(note(FCHORD).s('gm_choir_aahs').attack(.25).release(2).gain(.7).orbit(6)),
    NAVE(note(FCHORD).s('gm_church_organ').attack(.2).release(2).lpf(2500).gain(.08).orbit(4)),
  ).slow(2)],
  [2, stack(
    NAVE(note(ECHORD).s('gm_choir_aahs').attack(.25).release(4).gain(.75).orbit(6)),
    NAVE(note(ECHORD).s('gm_church_organ').attack(.1).release(4).gain(.14).orbit(4)),
    NAVE(note("[e5,g#5,b5]").s('gm_celesta').release(4).gain(.3).orbit(7)),
    NAVE(note("e4").s('gm_tubular_bells').release(5).gain(.35).orbit(7)),
  ).slow(2)],
  [4, silence],
), vox("<~ ~ ~ ~ if_ye_love_me ~ ~ ~>"))

// ============================================================
// THE ARRANGEMENT
// ============================================================
arrange(
  [8,  secPENDET],
  [16, secDILIGES],
  [12, secSIMILE],
  [16, secGOLGOTHA],
  [8,  secVERE],
  [8,  secDUOBUS],
  [8,  secAMEN],
)
