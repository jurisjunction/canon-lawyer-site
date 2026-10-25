% On These Two Hang, the long form: the choir's lines, for SATB
% The choir's part of the long form at canon-lawyer.ca/music/, bar for bar.
% Written by counterpoint.py --long --ly from the lines the track plays; do not edit by hand.
% Engrave with GNU LilyPond: lilypond on-these-two-hang-long.ly
% Dedicated to the public domain (CC0 1.0).

\version "2.24.0"

#(set-global-staff-size 18)

\paper {
  #(set-paper-size "letter")
  top-margin = 16\mm
  bottom-margin = 14\mm
  left-margin = 20\mm
  right-margin = 20\mm
  markup-system-spacing.padding = 2
  score-markup-spacing.padding = 2
  system-system-spacing.padding = 2
  print-page-number = ##t
  print-first-page-number = ##f
}

\header {
  title = "On These Two Hang"
  subtitle = "The long form: a double fugue for the household"
  subsubtitle = \markup \italic { "“On these two commandments hang all the law and the prophets” (Matthew 22:40)" }
  poet = "Words: the Vulgate"
  composer = "Notes made by rule: counterpoint.py --long"
  copyright = "Dedicated to the public domain (CC0 1.0)"
  tagline = \markup \small { "canon-lawyer.ca/music/ · Dedicated to the public domain (CC0 1.0) · Made by Claude + Richard" }
}

\markup \justify {
  The choir's part of the long form, bar for bar, in mode III, E phrygian. The notes are written out by counterpoint.py
  from the same lines the track plays, and the bar numbers are the track's. The first eight bars, I. Pendet, belong to
  the instruments and to the lawyer's question, so the score begins at bar 9. The two subjects are carved from their
  Latin words, a note to a syllable, as in the short form, and are taken through the old procedures of the fugue: the
  head they share in imitation, falling a step a bar (Caput); both subjects upside down about mi, the mirror (Speculum);
  the first subject four times slower in the bass, the Law held (Lex); the entries drawn closer together (In unum); the
  two subjects at once, in the mirror, and with the voices exchanged (Duobus); and a long E in the bass under the last
  entries (Fundamentum). Every statement, upright, inverted or long, has its words under it; in Caput the leader sings
  the first commandment's words and the follower the second's. The free voices were found by a search under Fux's
  rules; they have no text yet. In Golgotha the choir rests through the darkness, the veil and the tomb.
}

global = { \key e \phrygian \numericTimeSignature \time 4/4 }

marks = {
  \tempo 4 = 120 \set Score.currentBarNumber = #9
  \sectionLabel \markup \line { \bold "II. Diliges" \hspace #2 \italic "bar 9 (0:16)" }
  s8*128
  \section \sectionLabel \markup \line { \bold "III. Caput" \hspace #2 \italic "bar 25 (0:48)" }
  s8*48
  \section \sectionLabel \markup \line { \bold "IV. Simile" \hspace #2 \italic "bar 31 (1:00)" }
  s8*96
  \section \sectionLabel \markup \line { \bold "V. Caput" \hspace #2 \italic "bar 43 (1:24)" }
  s8*48
  \section \sectionLabel \markup \line { \bold "VI. Speculum" \hspace #2 \italic "bar 49 (1:36)" }
  s8*224
  \section \sectionLabel \markup \line { \bold "VII. Lex" \hspace #2 \italic "bar 77 (2:32)" }
  s8*128
  \set Score.skipBars = ##t
  \section \sectionLabel \markup \line { \bold "VIII. Golgotha" \hspace #2 \italic "bar 93 (3:04)" }
  s8*32
  \set Score.skipBars = ##f
  s8*40
  \set Score.skipBars = ##t
  s8*16
  \set Score.skipBars = ##f
  s8*16
  \set Score.skipBars = ##t
  s8*24
  \set Score.skipBars = ##f
  \section \sectionLabel \markup \line { \bold "IX. Vere" \hspace #2 \italic "bar 109 (3:36)" }
  s8*64
  \section \sectionLabel \markup \line { \bold "X. Caput" \hspace #2 \italic "bar 117 (3:52)" }
  s8*48
  \section \sectionLabel \markup \line { \bold "XI. In unum" \hspace #2 \italic "bar 123 (4:04)" }
  s8*216
  \section \sectionLabel \markup \line { \bold "XII. Caput" \hspace #2 \italic "bar 150 (4:58)" }
  s8*40
  \section \sectionLabel \markup \line { \bold "XIII. Duobus" \hspace #2 \italic "bar 155 (5:08)" }
  s8*96
  \section \sectionLabel \markup \line { \bold "XIV. Fundamentum" \hspace #2 \italic "bar 167 (5:32)" }
  s8*64
  \section \sectionLabel \markup \line { \bold "XV. Amen" \hspace #2 \italic "bar 175 (5:48)" }
  s8*32
  \bar "|."
}

soprano = {
  % II. Diliges
  R1*4 |
  b'4 b'8 a'8 d''4 b'8 g'8 |
  a'4 g'8 g'4 g'8 a'4 |
  d''4 d''8 d''4 a'8 g'4 |
  d'1 |
  b'2 g'2 |
  a'2 a'2 |
  g'2 g'2 |
  e'2 d'2 |
  b'2 b'2 |
  e''2 e''2 |
  d''2 b'2 |
  d''2 a'2 |
 
  % III. Caput
  e''4 e''8 d''8 g''4 e''8 c''8 |
  d''4 d''8 c''8 f''4 d''8 b'8 |
  c''4 c''8 b'8 e''4 c''8 a'8 |
  b'4 b'8 a'8 d''4 b'8 g'8 |
  a'4 a'8 g'8 c''4 a'8 f'8 |
  c''2 d''2 |
 
  % IV. Simile
  R1*9 |
  b'4 b'8 a'8 d''4 b'8 g'8 |
  g'4 g'8 b'4 g'8 a'8 b'8~ |
  b'8 g'4.~ g'2 |
 
  % V. Caput
  f'2 d''2 |
  a'2 b'2 |
  g'2 a'2 |
  a'2 g'2 |
  e'2 g'2 |
  b'2 d''2 |
 
  % VI. Speculum
  R1*12 |
  b'4 b'8 c''8 g'4 b'8 d''8 |
  c''4 d''8 d''4 d''8 c''4 |
  g'4 g'8 g'4 c''8 d''4 |
  g''1 |
  b'4 b'8 c''8 g'4 b'8 d''8 |
  d''4 d''8 b'4 d''8 c''8 b'8~ |
  b'8 d''4.~ d''2 |
  c''2 e''2 |
  e''2 e''2 |
  b'2 c''2 |
  b'2 d''2 |
  d''2 d''2 |
  d''2 f''2 |
  e''2 g''2 |
  e''2 g''2 |
  e''2 d''2 |
 
  % VII. Lex
  e''2 g''2 |
  e''2 f''2 |
  e''2 d''2 |
  e''2 g''2 |
  f''2 d''2 |
  e''2 c''2 |
  e''2 e''2 |
  d''2 d''2 |
  b'2 g'2 |
  b'2 b'2 |
  g'2 a'2 |
  c''2 e''2 |
  g''2 r2 |
  b'4 b'8 c''8 g'4 b'8 d''8 |
  d''4 d''8 b'4 d''8 c''8 b'8~ |
  b'8 d''4.~ d''2 |
 
  % VIII. Golgotha
  R1*4^\markup \small \italic "darkness: the clock alone" |
  d'4^\markup \small \italic "Solo: the cry" e'8 d'4 e'8 f'4 |
  f'8 f'8 f'4 f'8 e'4. |
  d'8^\markup \small \italic "Sopranos: the crowd" e'4 f'8 g'4 f'8 e'8~ |
  e'8 d'4.~ d'2 |
  g'8^\markup \small \italic "Solo" c''8 f''4 c''8 d''4. |
  R1*2^\markup \small \italic "the veil and the earth" |
  d''4^\markup \small \italic "Solo: the centurion" d''8 e''4 e''8 c''8 d''8~ |
  d''8 e''8 d''4 f''8 e''4 d''8 |
  R1*3^\markup \small \italic "the tomb" |
 
  % IX. Vere
  d''4 d''8 e''4 e''8 c''8 d''8~ |
  d''8 e''8 d''4 f''8 e''4 d''8 |
  d''4 d''8 e''4 e''8 c''8 d''8~ |
  d''8 e''8 d''4 f''8 e''4 d''8 |
  d''4 d''8 e''4 e''8 c''8 d''8~ |
  d''8 e''8 d''4 f''8 e''4 d''8 |
  d''4 d''8 e''4 e''8 c''8 d''8~ |
  d''8 e''8 d''4 f''8 e''4 d''8 |
 
  % X. Caput
  g''2 g''2 |
  g''2 f''2 |
  f''2 e''2 |
  e''2 d''2 |
  d''2 c''2 |
  c''2 c''2 |
 
  % XI. In unum
  R1*6 |
  b'4 b'8 a'8 d''4 b'8 g'8 |
  a'4 g'8 g'4 g'8 a'4 |
  d''4 d''8 d''4 a'8 g'4 |
  d'1 |
  e'2 e''2 |
  d''2 a'2 |
  b'2 a'2 |
  b'2 r2 |
  e''4 e''8 d''8 g''4 e''8 c''8 |
  c''4 c''8 e''4 c''8 d''8 e''8~ |
  e''8 c''4.~ c''2 |
  a'2 g'2 |
  b'2 c''2 |
  a'2 r2 |
  b'4 b'8 a'8 d''4 b'8 g'8 |
  g'4 g'8 b'4 g'8 a'8 b'8~ |
  b'8 g'4.~ g'2 |
  a'2 a'2 |
  b'2 g'2 |
  b'2 g'2 |
  g'2 g'2 |
 
  % XII. Caput
  e''4 e''8 d''8 g''4 e''8 c''8 |
  d''4 d''8 c''8 f''4 d''8 b'8 |
  c''4 c''8 b'8 e''4 c''8 a'8 |
  b'4 b'8 a'8 d''4 b'8 g'8 |
  d''2 d''2 |
 
  % XIII. Duobus
  r2 b'4 b'8 a'8 |
  d''4 b'8 g'8 g'4 g'8 b'8~ |
  b'8 g'8 a'8 b'4 g'4.~ |
  g'2 r2 |
  r2 b'4 b'8 c''8 |
  g'4 b'8 d''8 d''4 d''8 b'8~ |
  b'8 d''8 c''8 b'4 d''4.~ |
  d''2 r2 |
  b'4 b'8 a'8 d''4 b'8 g'8 |
  a'4 g'8 g'4 g'8 a'4 |
  d''4 d''8 d''4 a'8 g'4 |
  d'1 |
 
  % XIV. Fundamentum
  b'2 r2 |
  e''4 e''8 f''8 c''4 e''8 g''8 |
  g''4 g''8 e''4 g''8 f''8 e''8~ |
  e''8 g''4.~ g''2 |
  e''4 e''8 d''8 g''4 e''8 c''8 |
  c''4 c''8 e''4 c''8 d''8 e''8~ |
  e''8 c''4.~ c''2 |
  b'2 b'2 |
 
  % XV. Amen
  d'1~ |
  d'1 |
  e'1~ |
  e'1 |
}
sopranoWords = \lyricmode {
  "Di" -- "li" -- "ges" "Do" -- "mi" -- "num" "De" -- "um" "tu" -- "um" "ex"
  "to" -- "to" "cor" -- "de" "tu" -- "o" \repeat unfold 16 { \skip 1 }
  "Di" -- "li" -- "ges" "Do" -- "mi" -- "num" "Di" -- "li" -- "ges" "Do" -- "mi" -- "num"
  "Di" -- "li" -- "ges" "Do" -- "mi" -- "num" "Di" -- "li" -- "ges" "Do" -- "mi" -- "num"
  "Di" -- "li" -- "ges" "Do" -- "mi" -- "num" \repeat unfold 2 { \skip 1 }
  "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "tu" -- "um" "si" -- "cut"
  "te" -- "ip" -- "sum" \repeat unfold 12 { \skip 1 }
  "Di" -- "li" -- "ges" "Do" -- "mi" -- "num" "De" -- "um" "tu" -- "um" "ex"
  "to" -- "to" "cor" -- "de" "tu" -- "o" "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum"
  "tu" -- "um" "si" -- "cut" "te" -- "ip" -- "sum" \repeat unfold 43 { \skip 1 }
  "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "tu" -- "um" "si" -- "cut"
  "te" -- "ip" -- "sum" "E" -- "li,"
  "E" -- "li,"
  "lam" -- "ma" "sa" -- "bac" -- "tha" -- "ni" "E" -- "li" -- "am" "vo" -- "cat"
  "is" -- "te" "Con" -- "sum" -- "ma" -- "tum" "est" "Ve" -- "re" "Fi" -- "li" -- "us"
  "De" -- "i" "e" -- "rat" "is" -- "te" "Ve" -- "re" "Fi" -- "li" -- "us"
  "De" -- "i" "e" -- "rat" "is" -- "te" "Ve" -- "re" "Fi" -- "li" -- "us"
  "De" -- "i" "e" -- "rat" "is" -- "te" "Ve" -- "re" "Fi" -- "li" -- "us"
  "De" -- "i" "e" -- "rat" "is" -- "te" "Ve" -- "re" "Fi" -- "li" -- "us"
  "De" -- "i" "e" -- "rat" "is" -- "te" \repeat unfold 12 { \skip 1 }
  "Di" -- "li" -- "ges" "Do" -- "mi" -- "num" "De" -- "um" "tu" -- "um" "ex"
  "to" -- "to" "cor" -- "de" "tu" -- "o" \repeat unfold 7 { \skip 1 }
  "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "tu" -- "um" "si" -- "cut"
  "te" -- "ip" -- "sum" \repeat unfold 5 { \skip 1 }
  "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "tu" -- "um" "si" -- "cut"
  "te" -- "ip" -- "sum" \repeat unfold 8 { \skip 1 }
  "Di" -- "li" -- "ges" "Do" -- "mi" -- "num" "Di" -- "li" -- "ges" "Do" -- "mi" -- "num"
  "Di" -- "li" -- "ges" "Do" -- "mi" -- "num" "Di" -- "li" -- "ges" "Do" -- "mi" -- "num"
  \repeat unfold 2 { \skip 1 }
  "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "tu" -- "um" "si" -- "cut"
  "te" -- "ip" -- "sum" "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "tu" -- "um"
  "si" -- "cut" "te" -- "ip" -- "sum" "Di" -- "li" -- "ges" "Do" -- "mi" -- "num"
  "De" -- "um" "tu" -- "um" "ex" "to" -- "to" "cor" -- "de" "tu" -- "o" \repeat unfold 1 { \skip 1 }
  "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "tu" -- "um" "si" -- "cut"
  "te" -- "ip" -- "sum" "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "tu" -- "um"
  "si" -- "cut" "te" -- "ip" -- "sum" \repeat unfold 4 { \skip 1 }
}

alto = {
  % II. Diliges
  e'4 e'8 d'8 g'4 e'8 c'8 |
  d'4 c'8 c'4 c'8 d'4 |
  g'4 g'8 g'4 d'8 c'4 |
  g1 |
  d'2^\markup \small \italic "free voices: text to be set" b2 |
  c'2 c'2 |
  b2 g2 |
  b2 g2 |
  b2 b2 |
  a2 a2 |
  b2 d'2 |
  b2 g2 |
  d'2 d'2 |
  e'2 e'2 |
  f'2 d'2 |
  f'2 d'2 |
 
  % III. Caput
  e'2 c''2 |
  b'2 d''2 |
  a'2 c''2 |
  g'2 b'2 |
  d'2 e'2 |
  f'2 d'2 |
 
  % IV. Simile
  R1*6 |
  e'4 e'8 d'8 g'4 e'8 c'8 |
  c'4 c'8 e'4 c'8 d'8 e'8~ |
  e'8 c'4.~ c'2 |
  d'2 b2 |
  b2 b2 |
  b2 c'2 |
 
  % V. Caput
  f'4 f'8 e'8 a'4 f'8 d'8 |
  e'4 e'8 d'8 g'4 e'8 c'8 |
  d'4 d'8 c'8 f'4 d'8 b8 |
  c'4 c'8 b8 e'4 c'8 a8 |
  b4 b8 a8 d'4 b8 g8 |
  d'2 d'2 |
 
  % VI. Speculum
  R1*8 |
  e'4 e'8 f'8 c'4 e'8 g'8 |
  f'4 g'8 g'4 g'8 f'4 |
  c'4 c'8 c'4 f'8 g'4 |
  c''1 |
  e'2 d'2 |
  f'2 f'2 |
  e'2 e'2 |
  g'2 g'2 |
  e'2 d'2 |
  d'2 d'2 |
  b2 r2 |
  e'4 e'8 f'8 c'4 e'8 g'8 |
  g'4 g'8 e'4 g'8 f'8 e'8~ |
  e'8 g'4.~ g'2 |
  g'2 b'2 |
  b'2 b'2 |
  b'2 a'2 |
  c''2 g'2 |
  b'2 g'2 |
  b'2 g'2 |
 
  % VII. Lex
  g'2 b'2 |
  g'2 f'2 |
  g'2 b'2 |
  c''2 c''2 |
  a'2 b'2 |
  a'2 g'2 |
  a'2 g'2 |
  b'2 b'2 |
  g'2 d'2 |
  e'2 d'2 |
  e'2 r2 |
  e'4 e'8 f'8 c'4 e'8 g'8 |
  g'4 g'8 e'4 g'8 f'8 e'8~ |
  e'8 g'4.~ g'2 |
  b'2 g'2 |
  g'2 d'2 |
 
  % VIII. Golgotha
  R1*4 |
  R1*5 |
  R1*2 |
  R1*2 |
  R1*3 |
 
  % IX. Vere
  R1*2 |
  a'4 g'4 e'4 f'4 |
  a'4 g'4 f'4 g'4 |
  g'4 a'4 g'4 a'4 |
  b'4 g'4 f'4 g'4 |
  g'4 a'4 g'4 a'4 |
  b'4 g'4 f'4 g'4 |
 
  % X. Caput
  b'2 c''2 |
  g'2 a'2 |
  a'2 g'2 |
  e'2 g'2 |
  d'2 e'2 |
  c'2 c'2 |
 
  % XI. In unum
  e'4 e'8 d'8 g'4 e'8 c'8 |
  d'4 c'8 c'4 c'8 d'4 |
  g'4 g'8 g'4 d'8 c'4 |
  g1 |
  a2 a2 |
  b2 e'2 |
  d'2 b2 |
  c'2 c'2 |
  d'2 f'2 |
  d'2 d'2 |
  c'2 e'2 |
  f'2 f'2 |
  d'2 f'2 |
  r2 e'4 e'8 d'8 |
  g'4 e'8 c'8 c'4 c'8 e'8~ |
  e'8 c'8 d'8 e'4 c'4.~ |
  c'2 e'2 |
  a2 r2 |
  e'4 e'8 d'8 g'4 e'8 c'8 |
  d'4 c'8 c'4 c'8 d'4 |
  g'4 g'8 g'4 d'8 c'4 |
  g1 |
  b2 e'2 |
  a2 a2 |
  e'2 d'2 |
  b2 d'2 |
  e'2 d'2 |
 
  % XII. Caput
  g'2 g'2 |
  g'2 f'2 |
  a'2 a'2 |
  g'2 b'2 |
  b'2 g'2 |
 
  % XIII. Duobus
  b'2 g'2 |
  b'2 g'2 |
  e'2 g'2 |
  e'2 d'2 |
  g'2 d'2 |
  e'2 d'2 |
  d'2 d'2 |
  d'2 g'2 |
  d'2 d'2 |
  d'2 b2 |
  d'2 d'2 |
  b2 a2 |
 
  % XIV. Fundamentum
  e'4 e'8 d'8 g'4 e'8 c'8 |
  c'4 c'8 e'4 c'8 d'8 e'8~ |
  e'8 c'4.~ c'2 |
  e'4 e'8 f'8 c'4 e'8 g'8 |
  g'4 g'8 e'4 g'8 f'8 e'8~ |
  e'8 g'4.~ g'2 |
  e'2 e'2 |
  e'2 b2 |
 
  % XV. Amen
  a1~ |
  a1 |
  gis1~ |
  gis1 |
}
altoWords = \lyricmode {
  "Di" -- "li" -- "ges" "Do" -- "mi" -- "num" "De" -- "um" "tu" -- "um" "ex"
  "to" -- "to" "cor" -- "de" "tu" -- "o" \repeat unfold 36 { \skip 1 }
  "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "tu" -- "um" "si" -- "cut"
  "te" -- "ip" -- "sum" \repeat unfold 6 { \skip 1 }
  "Di" -- "li" -- "ges" "Do" -- "mi" -- "num" "Di" -- "li" -- "ges" "Do" -- "mi" -- "num"
  "Di" -- "li" -- "ges" "Do" -- "mi" -- "num" "Di" -- "li" -- "ges" "Do" -- "mi" -- "num"
  "Di" -- "li" -- "ges" "Do" -- "mi" -- "num" \repeat unfold 2 { \skip 1 }
  "Di" -- "li" -- "ges" "Do" -- "mi" -- "num" "De" -- "um" "tu" -- "um" "ex"
  "to" -- "to" "cor" -- "de" "tu" -- "o" \repeat unfold 13 { \skip 1 }
  "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "tu" -- "um" "si" -- "cut"
  "te" -- "ip" -- "sum" \repeat unfold 33 { \skip 1 }
  "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "tu" -- "um" "si" -- "cut"
  "te" -- "ip" -- "sum" \repeat unfold 40 { \skip 1 }
  "Di" -- "li" -- "ges" "Do" -- "mi" -- "num" "De" -- "um" "tu" -- "um" "ex"
  "to" -- "to" "cor" -- "de" "tu" -- "o" \repeat unfold 18 { \skip 1 }
  "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "tu" -- "um" "si" -- "cut"
  "te" -- "ip" -- "sum" \repeat unfold 2 { \skip 1 }
  "Di" -- "li" -- "ges" "Do" -- "mi" -- "num" "De" -- "um" "tu" -- "um" "ex"
  "to" -- "to" "cor" -- "de" "tu" -- "o" \repeat unfold 44 { \skip 1 }
  "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "tu" -- "um" "si" -- "cut"
  "te" -- "ip" -- "sum" "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "tu" -- "um"
  "si" -- "cut" "te" -- "ip" -- "sum" \repeat unfold 6 { \skip 1 }
}

tenor = {
  % II. Diliges
  R1*8 |
  e4 e8 d8 g4 e8 c8 |
  d4 c8 c4 c8 d4 |
  g4 g8 g4 d8 c4 |
  g,1 |
  g2 b2 |
  e2 e2 |
  a2 b2 |
  a2 a2 |
 
  % III. Caput
  r2 e'4 e'8 d'8 |
  g'4 e'8 c'8 d'4 d'8 c'8 |
  f'4 d'8 b8 c'4 c'8 b8 |
  e'4 c'8 a8 b4 b8 a8 |
  d'4 b8 g8 a4 a8 g8 |
  c'4 a8 f4~ f4. |
 
  % IV. Simile
  R1*3 |
  b4 b8 a8 d'4 b8 g8 |
  g4 g8 b4 g8 a8 b8~ |
  b8 g4.~ g2 |
  b2 c'2 |
  a2 c'2 |
  a2 g2 |
  d2 g2 |
  e2 g2 |
  e2 g2 |
 
  % V. Caput
  a2 d'2 |
  c'2 e'2 |
  b2 d'2 |
  a2 c'2 |
  g2 b2 |
  b2 g2 |
 
  % VI. Speculum
  e4 e8 f8 c4 e8 g8 |
  f4 g8 g4 g8 f4 |
  c4 c8 c4 f8 g4 |
  c'1 |
  g2 b2 |
  a2 a2 |
  b2 d'2 |
  e'2 d'2 |
  a2 g2 |
  c'2 b2 |
  a2 a2 |
  c'2 c'2 |
  e'2 b2 |
  c'2 a2 |
  b2 c'2 |
  d'2 c'2 |
  b2 b2 |
  g2 b2 |
  g2 b2 |
  a2 g2 |
  g2 c'2 |
  b2 r2 |
  b4 b8 c'8 g4 b8 d'8 |
  d'4 d'8 b4 d'8 c'8 b8~ |
  b8 d'4.~ d'2 |
  c'2 e'2 |
  e'2 e'2 |
  g'2 d'2 |
 
  % VII. Lex
  c'2 b2 |
  c'2 d'2 |
  b2 d'2 |
  c'2 e'2 |
  d'2 b2 |
  c'2 e'2 |
  c'2 r2 |
  b4 b8 a8 d'4 b8 g8 |
  g4 g8 b4 g8 a8 b8~ |
  b8 g4.~ g2 |
  b2 a2 |
  a2 g2 |
  g2 g2 |
  e2 b2 |
  b2 d'2 |
  b2 g2 |
 
  % VIII. Golgotha
  R1*4 |
  R1*5 |
  R1*2 |
  R1*2 |
  R1*3 |
 
  % IX. Vere
  R1*4 |
  b4 a4 c'4 c'4 |
  b4 d'4 c'4 g4 |
  b4 a4 c'4 c'4 |
  b4 d'4 c'4 g4 |
 
  % X. Caput
  e'4 e'8 d'8 g'4 e'8 c'8 |
  d'4 d'8 c'8 f'4 d'8 b8 |
  c'4 c'8 b8 e'4 c'8 a8 |
  b4 b8 a8 d'4 b8 g8 |
  a4 a8 g8 c'4 a8 f8 |
  a2 f2 |
 
  % XI. In unum
  R1*9 |
  b4 b8 a8 d'4 b8 g8 |
  a4 g8 g4 g8 a4 |
  d'4 d'8 d'4 a8 g4 |
  d1 |
  b2 g2 |
  r2 e4 e8 d8 |
  g4 e8 c8 c4 c8 e8~ |
  e8 c8 d8 e4 c4.~ |
  c2 g2 |
  g2 g2 |
  a2 f2 |
  g2 g2 |
  e2 e2 |
  g2 b2 |
  a2 r2 |
  b4 b8 a8 d'4 b8 g8 |
  g4 g8 b4 g8 a8 b8~ |
  b8 g4.~ g2 |
 
  % XII. Caput
  g2 c'2 |
  b2 d'2 |
  a2 a2 |
  e'2 d'2 |
  b2 d'2 |
 
  % XIII. Duobus
  b2 e'2 |
  d'2 e'2 |
  b2 b2 |
  b2 g2 |
  g2 g2 |
  g2 b2 |
  g2 b2 |
  b2 d'2 |
  d'2 b2 |
  d2 e2 |
  d2 d2 |
  d2 d2 |
 
  % XIV. Fundamentum
  g2 e2 |
  c2 r2 |
  e4 e8 d8 g4 e8 c8 |
  c4 c8 e4 c8 d8 e8~ |
  e8 c4.~ c2 |
  e4 e8 f8 c4 e8 g8 |
  g4 g8 e4 g8 f8 e8~ |
  e8 g4.~ g2 |
 
  % XV. Amen
  c1~ |
  c1 |
  b,1~ |
  b,1 |
}
tenorWords = \lyricmode {
  "Di" -- "li" -- "ges" "Do" -- "mi" -- "num" "De" -- "um" "tu" -- "um" "ex"
  "to" -- "to" "cor" -- "de" "tu" -- "o" \repeat unfold 8 { \skip 1 }
  "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum"
  "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum"
  "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum"
  "tu" -- "um" "si" -- "cut" "te" -- "ip" -- "sum" \repeat unfold 24 { \skip 1 }
  "Di" -- "li" -- "ges" "Do" -- "mi" -- "num" "De" -- "um" "tu" -- "um" "ex"
  "to" -- "to" "cor" -- "de" "tu" -- "o" \repeat unfold 35 { \skip 1 }
  "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "tu" -- "um" "si" -- "cut"
  "te" -- "ip" -- "sum" \repeat unfold 19 { \skip 1 }
  "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "tu" -- "um" "si" -- "cut"
  "te" -- "ip" -- "sum" \repeat unfold 28 { \skip 1 }
  "Di" -- "li" -- "ges" "Do" -- "mi" -- "num" "Di" -- "li" -- "ges" "Do" -- "mi" -- "num"
  "Di" -- "li" -- "ges" "Do" -- "mi" -- "num" "Di" -- "li" -- "ges" "Do" -- "mi" -- "num"
  "Di" -- "li" -- "ges" "Do" -- "mi" -- "num" \repeat unfold 2 { \skip 1 }
  "Di" -- "li" -- "ges" "Do" -- "mi" -- "num" "De" -- "um" "tu" -- "um" "ex"
  "to" -- "to" "cor" -- "de" "tu" -- "o" \repeat unfold 2 { \skip 1 }
  "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "tu" -- "um" "si" -- "cut"
  "te" -- "ip" -- "sum" \repeat unfold 12 { \skip 1 }
  "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "tu" -- "um" "si" -- "cut"
  "te" -- "ip" -- "sum" \repeat unfold 37 { \skip 1 }
  "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "tu" -- "um" "si" -- "cut"
  "te" -- "ip" -- "sum" "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "tu" -- "um"
  "si" -- "cut" "te" -- "ip" -- "sum" \repeat unfold 2 { \skip 1 }
}

bass = {
  % II. Diliges
  R1*12 |
  b,4 b,8 a,8 d4 b,8 g,8 |
  a,4 g,8 g,4 g,8 a,4 |
  d4 d8 d4 a,8 g,4 |
  d,1 |
 
  % III. Caput
  g,2 c2 |
  g2 f2 |
  f2 e2 |
  e2 d2 |
  d2 c2 |
  a,2 d2 |
 
  % IV. Simile
  e4 e8 d8 g4 e8 c8 |
  c4 c8 e4 c8 d8 e8~ |
  e8 c4.~ c2 |
  d2 b,2 |
  b,2 g,2 |
  b,2 c2 |
  g2 e2 |
  c2 a,2 |
  c2 c2 |
  b,2 g,2 |
  g,2 e,2 |
  g,2 c2 |
 
  % V. Caput
  r2 f4 f8 e8 |
  a4 f8 d8 e4 e8 d8 |
  g4 e8 c8 d4 d8 c8 |
  f4 d8 b,8 c4 c8 b,8 |
  e4 c8 a,8 b,4 b,8 a,8 |
  d4 b,8 g,4~ g,4. |
 
  % VI. Speculum
  R1*4 |
  b,4 b,8 c8 g,4 b,8 d8 |
  c4 d8 d4 d8 c4 |
  g,4 g,8 g,4 c8 d4 |
  g1 |
  a2 e2 |
  a,2 b,2 |
  c2 f2 |
  e2 f2 |
  e2 g2 |
  f2 f2 |
  g2 e2 |
  b,2 c2 |
  e2 b,2 |
  b,2 g,2 |
  b,2 g,2 |
  a,2 c2 |
  e2 c2 |
  e2 c2 |
  e2 b,2 |
  g,2 b,2 |
  g,2 r2 |
  e4 e8 f8 c4 e8 g8 |
  g4 g8 e4 g8 f8 e8~ |
  e8 g4.~ g2 |
 
  % VII. Lex
  e1 |
  e2 d2 |
  g1 |
  e2 c2 |
  d1 |
  c2 c2~ |
  c2 c2 |
  d1 |
  g1 |
  g2 g2~ |
  g2 d2 |
  c1 |
  g,1~ |
  g,1~ |
  g,1~ |
  g,1 |
 
  % VIII. Golgotha
  R1*4 |
  R1*5 |
  R1*2 |
  R1*2 |
  R1*3 |
 
  % IX. Vere
  b4 g4 g4 a4 |
  g4 b4 a4 g4 |
  f4 g4 g4 a4 |
  f4 g4 a4 g4 |
  g4 f4 e4 f4 |
  d4 b,4 a,4 g,4 |
  g4 f4 e4 f4 |
  d4 b,4 a,4 g,4 |
 
  % X. Caput
  r2 e4 e8 d8 |
  g4 e8 c8 d4 d8 c8 |
  f4 d8 b,8 c4 c8 b,8 |
  e4 c8 a,8 b,4 b,8 a,8 |
  d4 b,8 g,8 a,4 a,8 g,8 |
  c4 a,8 f,4~ f,4. |
 
  % XI. In unum
  R1*3 |
  e4 e8 d8 g4 e8 c8 |
  d4 c8 c4 c8 d4 |
  g4 g8 g4 d8 c4 |
  g,1 |
  c2 c2 |
  b,2 d2 |
  d2 b,2 |
  c2 c2 |
  d2 d2 |
  b,2 r2 |
  e4 e8 d8 g4 e8 c8 |
  c4 c8 e4 c8 d8 e8~ |
  e8 c4.~ c2 |
  a,2 e,2 |
  f,2 e,2 |
  g,2 e,2 |
  f,2 a,2 |
  b,2 g,2 |
  g,2 r2 |
  e4 e8 d8 g4 e8 c8 |
  d4 c8 c4 c8 d4 |
  g4 g8 g4 d8 c4 |
  g,1 |
  e,2 g,2 |
 
  % XII. Caput
  r2 e4 e8 d8 |
  g4 e8 c8 d4 d8 c8 |
  f4 d8 b,8 c4 c8 b,8 |
  e4 c8 a,8 b,4 b,8 a,8 |
  d4 b,8 g,4~ g,4. |
 
  % XIII. Duobus
  e4 e8 d8 g4 e8 c8 |
  d4 c8 c4 c8 d4 |
  g4 g8 g4 d8 c4 |
  g,1 |
  b,4 b,8 c8 g,4 b,8 d8 |
  c4 d8 d4 d8 c4 |
  g,4 g,8 g,4 c8 d4 |
  g1 |
  r2 b,4 b,8 a,8 |
  d4 b,8 g,8 g,4 g,8 b,8~ |
  b,8 g,8 a,8 b,4 g,4.~ |
  g,2 r2 |
 
  % XIV. Fundamentum
  e,1~ |
  e,1~ |
  e,1~ |
  e,1~ |
  e,1~ |
  e,1~ |
  e,1~ |
  e,1 |
 
  % XV. Amen
  f,1~ |
  f,1 |
  e,1~ |
  e,1 |
}
bassWords = \lyricmode {
  "Di" -- "li" -- "ges" "Do" -- "mi" -- "num" "De" -- "um" "tu" -- "um" "ex"
  "to" -- "to" "cor" -- "de" "tu" -- "o" \repeat unfold 12 { \skip 1 }
  "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "tu" -- "um" "si" -- "cut"
  "te" -- "ip" -- "sum" \repeat unfold 18 { \skip 1 }
  "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum"
  "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum"
  "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "Di" -- "li" -- "ges" "Do" -- "mi" -- "num"
  "De" -- "um" "tu" -- "um" "ex" "to" -- "to" "cor" -- "de" "tu" -- "o" \repeat unfold 33 { \skip 1 }
  "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "tu" -- "um" "si" -- "cut"
  "te" -- "ip" -- "sum" "Di" -- "li" -- "ges" "Do" -- "mi" -- "num" "De" -- "um"
  "tu" -- "um" "ex" "to" -- "to" "cor" -- "de" "tu" -- "o" \repeat unfold 32 { \skip 1 }
  "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum"
  "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum"
  "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "Di" -- "li" -- "ges" "Do" -- "mi" -- "num"
  "De" -- "um" "tu" -- "um" "ex" "to" -- "to" "cor" -- "de" "tu" -- "o" \repeat unfold 11 { \skip 1 }
  "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "tu" -- "um" "si" -- "cut"
  "te" -- "ip" -- "sum" \repeat unfold 11 { \skip 1 }
  "Di" -- "li" -- "ges" "Do" -- "mi" -- "num" "De" -- "um" "tu" -- "um" "ex"
  "to" -- "to" "cor" -- "de" "tu" -- "o" \repeat unfold 2 { \skip 1 }
  "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum"
  "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum"
  "Di" -- "li" -- "ges" "Do" -- "mi" -- "num" "De" -- "um" "tu" -- "um" "ex"
  "to" -- "to" "cor" -- "de" "tu" -- "o" "Di" -- "li" -- "ges" "Do" -- "mi" -- "num"
  "De" -- "um" "tu" -- "um" "ex" "to" -- "to" "cor" -- "de" "tu" -- "o" "Di" -- "li" -- "ges"
  "pro" -- "xi" -- "mum" "tu" -- "um" "si" -- "cut" "te" -- "ip" -- "sum"
  \repeat unfold 3 { \skip 1 }
}

\score {
  \new ChoirStaff <<
    \new Staff \with { instrumentName = "Soprano" shortInstrumentName = "S." } <<
      \marks
      \new Voice = "S" { \global \clef "treble" \soprano }
    >>
    \new Lyrics \lyricsto "S" { \sopranoWords }
    \new Staff \with { instrumentName = "Alto" shortInstrumentName = "A." } <<
      \new Voice = "A" { \global \clef "treble" \alto }
    >>
    \new Lyrics \lyricsto "A" { \altoWords }
    \new Staff \with { instrumentName = "Tenor" shortInstrumentName = "T." } <<
      \new Voice = "T" { \global \clef "treble_8" \tenor }
    >>
    \new Lyrics \lyricsto "T" { \tenorWords }
    \new Staff \with { instrumentName = "Bass" shortInstrumentName = "B." } <<
      \new Voice = "B" { \global \clef "bass" \bass }
    >>
    \new Lyrics \lyricsto "B" { \bassWords }
  >>
  \layout {
    \context { \Staff \RemoveEmptyStaves }
    \context { \Lyrics
      \override LyricText.font-size = #0.5
      \override LyricHyphen.minimum-distance = #1.2
      \override LyricSpace.minimum-distance = #1.0
    }
  }
}

\markup \small \italic \justify {
  Matthew 22:37, 22:39, 27:46, 27:47 and 27:54; John 19:30 (Vulgate). The heading is Matthew 22:40 (King James Version).
  Speculum: “For now we see through a glass, darkly” (1 Corinthians 13:12). In unum: “that also he should gather together
  in one the children of God that were scattered abroad” (John 11:52). Fundamentum: “For other foundation can no man lay
  than that is laid, which is Jesus Christ” (1 Corinthians 3:11). After the cadence the track keeps four bars of
  silence, and in them “If ye love me, keep my commandments” (John 14:15).
}
