// ============================================================
// WHETHER THE CLOUD MAKES MANY WORLDS — the dance mix
// A disputation, McLuhan presiding · mode VII x deep techno
// 122 BPM · 132 bars · ~4:20, then it loops
// For Strudel (https://strudel.cc): paste, press play (Ctrl+Enter).
// Dedicated to the public domain (CC0 1.0).
//
// The track is built from its end. The hook is the opening of the
// Ascension introit, "Viri Galilaei" (Acts 1:11). The intro is that
// hook BACKWARDS, in fog: Machaut's "Ma fin est mon commencement".
// The outro plays it forwards. The pulse under everything is the
// first message ever sent by electric telegraph: WHAT HATH GOD
// WROUGHT (24 May 1844; Numbers 23:23), tapped in Morse. At the
// drop that rhythm carries the chant: the medium given back its word.
//
// TIMELINE (bar / time):
//   CLOUD     1  0:00  the hook backwards, in fog; the title spoken
//   HALL     17  0:31  build: "it seems that it does" (the objections)
//   VOICE    33  1:03  the riser: IT IS ALL MADE OF NOTHING
//                      ...then one bar of silence
//   HOREB    41  1:19  three false drops: wind, earthquake, fire
//   STILL    49  1:34  breakdown: Lumen Christi on a pure tone;
//                      "seven thousand" brings the heartbeat back
//   BRIGHT   65  2:06  build: Rorate caeli, G minor; the telegraph
//                      rings the chant on celesta
//   TAKEN UP 81  2:37  THE DROP: G mixolydian, the hook rising an
//                      octave every 8 bars until the bells peal
//   END     113  3:40  my end is my beginning: the hook forwards
//   tail    129  4:12  silence for the reverb
//
// The spoken lines come from Shabda's text-to-speech and load the
// first time they play. If they are slow, stop and play again.
// ============================================================

setcpm(122/4) // one cycle = one bar

// ---- the spoken lines
samples('shabda/speech/en-GB/f:whether_the_cloud_makes_many_worlds,it_seems_that_it_does,but_the_lord_was_not_in_the_wind,not_in_the_earthquake,not_in_the_fire,and_after_the_fire_a_still_small_voice,i_even_i_only_am_left,yet_i_have_left_me_seven_thousand,let_the_clouds_rain_down_the_just_one,what_hath_god_wrought,the_darkness_shall_not_overcome_it,the_word_was_made_flesh_and_dwelt_among_us,my_end_is_my_beginning')
// the Voice: no name, a man, pitched down
samples('shabda/speech/en-GB/m:nothing,it_is_all_made_of_nothing')

// ============================================================
// ORBITS: 1 drums · 2 pads and acid (ducked by the kick) ·
//         3 spoken word · 4 light · 5 sub · 6 fx · 7 choir
// ============================================================

// ---------------- THE CHANT -----------------------------------
// eighth-note grid: a syllable on one note = 2, notes of a neume = 1
// "Viri Galilaei, quid admiramini": two bars
const VIRI = 'g3@2 g3@2 g3 c4 b3 c4@2 d4 c4 e4 d4 d4@3'
// the same, end first
const IRIV = 'd4@3 d4 e4 c4 d4 c4@2 b3 c4 g3 g3@2 g3@2'
// "Rorate caeli desuper, et nubes pluant justum" (Isaiah 45:8),
// mode 1, raised a fourth into G minor: two four-bar phrases
const RORATE = 'bb3@3 c4 d4 d4@3 g4@4 f4@3 f4 eb4@2 d4@3 d4@3 c4@4 ~@4 ' +
               'd4@3 eb4@3 d4@3 c4 bb3 a3@3 bb3 a3 g3@8 ~@8'
// "Lumen Christi" / "Deo gratias": do do do la, two bars each
const lumen = (doh, la) => doh + '@2 ' + doh + '@2 ' + doh + '@2 ' + la + '@4 ~@6'
const gratias = (doh, la) => doh + '@2 ' + doh + '@2 ' + doh + '@2 ' + la + '@2 ' + la + '@4 ~@4'

const sing = (phrase, bars) => note(mini(phrase)).slow(bars)
const hook = (up = 0) => sing(VIRI, 2).transpose(up)

// ---------------- THE TELEGRAPH --------------------------------
// dot 1 sixteenth, dash 3; 1 between signs, 3 between letters,
// 7 between words: 189 sixteenths, 50 strokes, ~11.8 bars
const CODE = { W: '.--', H: '....', A: '.-', T: '-', G: '--.', O: '---', D: '-..', R: '.-.', U: '..-' }
const morse = (text) => text.split(' ').map((word) =>
  word.split('').map((ch) =>
    CODE[ch].split('').map((sign) => (sign === '.' ? 'x' : 'x@3')).join(' ~ ')
  ).join(' ~@3 ')
).join(' ~@7 ')
const TALEA = morse('WHAT HATH GOD WROUGHT')
const SPAN = 189 / 16
// isorhythm: the rhythm (talea) carries a melody (color), one note per stroke
const iso = (talea, color) => { let i = 0; return talea.replace(/x/g, () => color[i++ % color.length]) }
const pitches = (phrase) => phrase.split(' ').filter((t) => t && t[0] !== '~').map((t) => t.split('@')[0])
const ring = (color, up) => note(mini(iso(TALEA, color))).transpose(up).slow(SPAN)
// the introit's own tones, without its leading notes, so the bells never grind on the chords
const CHANT_TONES = pitches(VIRI).filter((p) => p[0] !== 'b' && p[0] !== 'e')
const RORATE_TONES = pitches(RORATE).filter((p) => p[0] !== 'a' && !p.startsWith('eb'))
// the telegraph as percussion: a rimshot key
const tapping = s(mini(iso(TALEA, ['rim']))).slow(SPAN).bank('RolandTR909')

// ---------------- FOUNDATION ----------------------------------
const kick = (cut = 1200) => s("bd*4").bank('RolandTR909')
  .lpf(cut).shape(.15).gain(.95)
  .duckorbit(2).duckattack(.3).duckdepth(.5)
const sub = (roots) => note(roots).struct("[~ x]*4").s('sine')
  .clip(.5).release(.05).gain(.8).orbit(5)
const hats = s("[~ hh]*4").bank('RolandTR909').hpf(6000).gain(.22).orbit(1)
const veil = s("hh*16").bank('RolandTR909').hpf(8000)
  .gain(sine.fast(4).range(.05, .12)).pan(.62).orbit(1)
const clap = s("~ cp").bank('RolandTR909').room(.4).gain(.3).orbit(1)
const riser = (bars) => s("white").seg(8)
  .gain(saw.slow(bars).range(.01, .22))
  .lpf(saw.slow(bars).range(300, 7000)).hpf(200)
  .room(.7).orbit(6)

// ---------------- HARMONY --------------------------------------
// the mode's own chords, G F C G; and, for Rorate, G minor, ending on D to pull into the drop
const MIXO = "<[g2,d3,g3,b3] [f2,c3,f3,a3] [c3,g3,c4,e4] [g2,d3,g3,b3]>"
const MINOR = "<[g2,d3,g3,bb3] [eb2,bb2,eb3,g3] [bb2,f3,bb3,d4] [f2,c3,f3,a3] [eb2,bb2,eb3,g3] [f2,c3,f3,a3] [g2,d3,g3,bb3] [d2,a2,d3,f#3]>"
const pad = (chords, cut = 900, g = .12) => note(chords)
  .s('sawtooth').attack(.6).release(1.2)
  .lpf(cut).gain(g).room(.5).roomsize(4).orbit(2)
const acid = note("<[g2 ~ g2 g3 ~ g2 d3 ~] [f2 ~ f2 f3 ~ f2 c3 ~] [c3 ~ c3 c4 ~ c3 g3 ~] [g2 ~ g2 g3 ~ b2 d3 ~]>")
  .s('sawtooth').lpf(500).lpq(10).lpenv(4).lpd(.12)
  .decay(.15).sustain(.2).gain(.22).orbit(2)
const lux = note("[g5,d6]").slow(4)
  .s('sine').attack(3).release(4).gain(.14).hpf(1200)
  .pan(sine.slow(24).range(.3, .7))
  .room(1).roomsize(6).orbit(4)
// the peal: prime periods, never repeating (2, 3, 5, 7, 11, 13, 17 beats),
// all on tones that sit on every chord of the drop
const peal = stack(
  note("g2").slow(17/4).gain(.7).pan(.5),
  note("d3").slow(13/4).gain(.55).pan(.38),
  note("g3").slow(11/4).gain(.5).pan(.62),
  note("c4").slow(7/4).gain(.45).pan(.3),
  note("d4").slow(5/4).gain(.4).pan(.7),
  note("g4").slow(3/4).gain(.34).pan(.42),
  note("a4").slow(1/2).gain(.28).pan(.58),
).s('gm_tubular_bells').postgain(2).room(.8).roomsize(6).orbit(6)

// ---------------- VOICES ---------------------------------------
const vox = (p) => s(p).speed(.94)
  .hpf(160).lpf(8000).gain(1.5)
  .delay(".18:.37:.35")
  .pan(sine.slow(16).range(.42, .58))
  .room(.2).orbit(3)
// Strudel plays soundfonts at 0.3 of their gain, so the choir is lifted to sit with the synths
const choir = (p, g = .38) => p.s('gm_choir_aahs')
  .attack(.05).release(.6).room(.6).roomsize(5).gain(g * 3).orbit(7)

// ============================================================
// SECTIONS
// ============================================================

// I. THE CLOUD: the end, first, backwards
const secCLOUD = stack(
  s("pink").attack(1).release(1).lpf(500).gain(.05).orbit(6),
  sing(IRIV, 8).s('gm_voice_oohs')
    .lpf(saw.slow(16).range(400, 1600)).room(.9).roomsize(6).gain(1).orbit(7),
  tapping.gain(.12).hpf(1500).delay(".5:.375:.5").room(.6).orbit(6).mask("<0!4 1!12>"),
  kick(saw.slow(16).range(250, 900)),
  sub("<g1>").mask("<0!12 1!4>"),
  vox("<whether_the_cloud_makes_many_worlds ~!15>"),
)

// II. THE HALL: the objections, in organum at the fourth (as in the Musica enchiriadis)
const secHALL = stack(
  kick("<700!8 1600!8>"),
  sub("<g1 f1 c2 g1>"),
  hats.mask("<0!4 1!12>"),
  tapping.gain(.16).orbit(1),
  pad(MIXO, saw.slow(16).range(500, 1600)),
  choir(hook(0)),
  choir(hook(5), .26).mask("<0!8 1!8>"),
  acid.mask("<0!8 1!8>"),
  vox("<it_seems_that_it_does ~ ~ ~>"),
)

// III. THE VOICE: fortissimo, no name. Then nothing at all.
const secVOICE = arrange(
  [7, stack(
    kick(2400).mask("<1!4 0!3>"),
    sub("<g1 f1 c2 g1>").mask("<1!4 0!3>"),
    pad(MIXO, saw.slow(7).range(1600, 5000)),
    riser(7),
    s("sd*<4 4 8 8 16 32 32>").bank('RolandTR909').gain(saw.slow(7).range(.12, .45)).orbit(1),
    s("<~ ~ ~ ~ nothing ~ it_is_all_made_of_nothing>")
      .speed(.8).distort(1.5).hpf(80).gain(2).room(.3).orbit(3),
    s("white").gain(.5).mask("<0!6 1>").orbit(6),
    note("[g2,ab2,a2,bb2,b2,c3,db3]").s('sawtooth').distort(2).gain(.1).mask("<0!6 1>").orbit(6),
  )],
  [1, silence],
)

// IV. HOREB: "but the LORD was not in the wind..."
const secHOREB = arrange(
  [2, stack(s("wind").n("<0 4>").gain(.4).room(.4).orbit(6),
            vox("<but_the_lord_was_not_in_the_wind ~>"))],
  [2, stack(s("brown").lpf(140).gain(.4).orbit(6),
            s("bd").bank('RolandTR909').speed(.4).lpf(200).gain(.9).orbit(5),
            vox("<not_in_the_earthquake ~>"))],
  [2, stack(s("crackle").density(.25).hpf(800).gain(.35).orbit(6),
            vox("<not_in_the_fire ~>"))],
  [2, vox("<~ and_after_the_fire_a_still_small_voice>").gain(1)],
)

// V. A STILL SMALL VOICE: a pure tone, three times, a step higher
// each time; the people answer. Then Elijah's correction, and the
// heartbeat comes back: the bonds were never cut.
const secSTILL = stack(
  arrange(
    [2, sing(lumen('d4', 'b3'), 2)], [2, silence],
    [2, sing(lumen('e4', 'c#4'), 2)], [2, silence],
    [2, sing(lumen('f4', 'd4'), 2)], [6, silence],
  ).s('sine').attack(.05).release(.6).room(.8).roomsize(6).gain(.25).orbit(4),
  choir(arrange(
    [2, silence], [2, sing(gratias('d4', 'b3'), 2)],
    [2, silence], [2, sing(gratias('e4', 'c#4'), 2)],
    [2, silence], [2, sing(gratias('f4', 'd4'), 2)],
    [4, silence],
  ), .3),
  s("pink").attack(1).release(1).lpf(400).gain(.03).orbit(6),
  kick(200).mask("<0!12 1!4>"),
  vox("<~!12 i_even_i_only_am_left ~ yet_i_have_left_me_seven_thousand ~>"),
)

// VI. A BRIGHT CLOUD: "drop down, ye heavens"; the telegraph rings the chant
const secBRIGHT = stack(
  pad(MINOR, saw.slow(16).range(400, 2200)),
  choir(sing(RORATE, 8), .4),
  ring(RORATE_TONES, 12).s('gm_celesta')
    .room(.7).gain(.4).orbit(6).mask("<0!4 1!12>"),
  kick(saw.slow(8).range(300, 3000)).mask("<0!8 1!8>"),
  sub("<g1 eb1 bb1 f1 eb1 f1 g1 d1>").mask("<0!8 1!8>"),
  hats.mask("<0!12 1!4>"),
  riser(4).mask("<0!12 1!4>"),
  vox("<let_the_clouds_rain_down_the_just_one ~!7 what_hath_god_wrought ~!7>"),
)

// VII. TAKEN UP: the drop. "There appeared a chariot of fire...
// and Elijah went up by a whirlwind into heaven." The hook rises.
const secTAKEN = stack(
  kick(4000), sub("<g1 f1 c2 g1>"), clap, hats, veil,
  pad(MIXO, 2000, .12), acid, lux,
  arrange(
    [8, choir(hook(0), .42)],
    [8, stack(choir(hook(12), .4), choir(hook(17), .26))],
    [8, stack(choir(hook(12), .4),
              hook(24).s('sawtooth').attack(.02).release(.3).lpf(3000).gain(.15).orbit(7))],
    [8, stack(choir(hook(12), .4),
              hook(24).s('sawtooth').attack(.02).release(.3).lpf(3500).gain(.15).orbit(7),
              hook(24).s('gm_tubular_bells').room(.8).gain(.6).orbit(6),
              peal)],
  ),
  ring(CHANT_TONES, 12).s('gm_tubular_bells').room(.7).gain(.35).orbit(6).mask("<0!16 1!16>"),
  vox("<the_darkness_shall_not_overcome_it ~!11 the_word_was_made_flesh_and_dwelt_among_us ~!3 the_darkness_shall_not_overcome_it ~!15>"),
)

// VIII. MY END IS MY BEGINNING: the hook forwards; the open fifth
const secEND = stack(
  kick("<1200!4 800!4 400!4>").mask("<1!12 0!4>"),
  sub("<g1>").mask("<1!8 0!8>"),
  hats.mask("<1!4 0!12>"),
  arrange([8, sing(VIRI, 8)], [8, silence]).s('gm_voice_oohs').room(.9).roomsize(6).gain(1.1).orbit(7),
  note("[g2,d3,g3,d4]").s('sawtooth').attack(2).release(3).lpf(900)
    .gain("<0!8 .3 .27 .24 .2 .16 .12 .08 .04>").room(.5).roomsize(4).orbit(2),
  lux,
  vox("<~!8 my_end_is_my_beginning ~!7>"),
)

// ============================================================
// THE ARRANGEMENT
// ============================================================
arrange(
  [16, secCLOUD],
  [16, secHALL],
  [8,  secVOICE],
  [8,  secHOREB],
  [16, secSTILL],
  [16, secBRIGHT],
  [32, secTAKEN],
  [16, secEND],
  [4,  silence],
)
