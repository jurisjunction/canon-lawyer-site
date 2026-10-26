% On These Two Hang: an organ edition, with optional bells and percussion
% SATB choir and organ (two manuals and pedal); bells and percussion ad libitum; a reader.
% Written by organ_edition.py (music-generation/arrange) from the events the track plays
% and from the published choir parts; do not edit by hand.
% Engrave with GNU LilyPond: lilypond on-these-two-hang-organ.ly
% It makes on-these-two-hang-organ.pdf (the full score, with a preface), on-these-two-hang-organ-bells.pdf and
% on-these-two-hang-organ-percussion.pdf (the parts), and on-these-two-hang-organ.mid (a track to a staff).
% Dedicated to the public domain (CC0 1.0).

\version "2.24.0"

#(ly:set-option 'midi-extension "mid")

\paper {
  #(set-paper-size "letter")
  top-margin = 14\mm
  bottom-margin = 12\mm
  left-margin = 16\mm
  right-margin = 14\mm
  markup-system-spacing.padding = 2
  score-markup-spacing.padding = 2
  system-system-spacing.padding = 2.5
  print-page-number = ##t
  print-first-page-number = ##f
}

\header {
  title = "On These Two Hang"
  subtitle = "A double fugue for Matthew 22:34–40"
  subsubtitle = "For SATB choir and organ, with bells and percussion ad libitum"
  poet = "Words: the Vulgate"
  composer = \markup \right-column { "Notes made by rule: counterpoint.py" "Arranged by rule from the track: organ_edition.py" }
  copyright = "Dedicated to the public domain (CC0 1.0)"
  tagline = \markup \small { "canon-lawyer.ca/music/ · Dedicated to the public domain (CC0 1.0) · Made by Claude + Richard" }
}

#(define churchPercussion '(
  (ridecymbal cross #f 5)
  (crashcymbal xcircle #f 5)
  (hiwoodblock default #f 3)
  (lowoodblock default #f 1)
  (lowfloortom default #f -1)
  (bassdrum default #f -3)))

global = { \key e \phrygian \numericTimeSignature \time 4/4 }

marks = {
  \tempo 4 = 120
  \mark \markup \box \bold "I"
  \sectionLabel \markup \line { \bold "Pendet" \hspace #1 \italic "bar 1 (0:00)" }
  s1*8
  \section
  \mark \markup \box \bold "II"
  \sectionLabel \markup \line { \bold "Diliges" \hspace #1 \italic "bar 9 (0:16)" }
  s1*16
  \section
  \mark \markup \box \bold "III"
  \sectionLabel \markup \line { \bold "Simile" \hspace #1 \italic "bar 25 (0:48)" }
  s1*12
  \section
  \mark \markup \box \bold "IV"
  \sectionLabel \markup \line { \bold "Golgotha" \hspace #1 \italic "bar 37 (1:12)" }
  \textMark \markup \italic "darkness: the clock alone (choir tacet)"
  s1*4
  \textMark \markup \italic "the cry: the clock stutters"
  s1*2
  \textMark \markup \italic "the crowd, and a wind that does not come"
  s1*2
  \textMark \markup \italic "“it is finished”: the clock stops"
  s1*1
  \textMark \markup \italic "the veil, top to bottom; the earth quakes; the rocks rend"
  s1*2
  \textMark \markup \italic "the centurion, alone"
  s1*2
  \textMark \markup \italic "the tomb: three bars of silence, all tacet, organ too"
  s1*3
  \section
  \mark \markup \box \bold "V"
  \sectionLabel \markup \line { \bold "Vere" \hspace #1 \italic "bar 53 (1:44)" }
  \textMark \markup \italic "the stone: the clock comes back"
  s1*8
  \section
  \mark \markup \box \bold "VI"
  \sectionLabel \markup \line { \bold "Duobus" \hspace #1 \italic "bar 61 (2:00)" }
  s1*4
  \textMark \markup \italic "the household hangs on them"
  s1*4
  \section
  \mark \markup \box \bold "VII"
  \sectionLabel \markup \line { \bold "Amen" \hspace #1 \italic "bar 69 (2:16)" }
  s1*4
  \textMark \markup \italic "silence"
  \textMark \markup \column { \line { \bold "Reader (or the priest), optional, spoken:" } \line { \italic "“If ye love me, keep my commandments.”" "(John 14:15)" } }
  s1*4
  \bar "|."
}

soprano = {
  % I. Pendet
  R1*8 |
 
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
 
  % III. Simile
  R1*9 |
  b'4 b'8 a'8 d''4 b'8 g'8 |
  g'4 g'8 b'4 g'8 a'8 b'8~ |
  b'8 g'4.~ g'2 |
 
  % IV. Golgotha
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
 
  % V. Vere
  d''4 d''8 e''4 e''8 c''8 d''8~ |
  d''8 e''8 d''4 f''8 e''4 d''8 |
  d''4 d''8 e''4 e''8 c''8 d''8~ |
  d''8 e''8 d''4 f''8 e''4 d''8 |
  d''4 d''8 e''4 e''8 c''8 d''8~ |
  d''8 e''8 d''4 f''8 e''4 d''8 |
  d''4 d''8 e''4 e''8 c''8 d''8~ |
  d''8 e''8 d''4 f''8 e''4 d''8 |
 
  % VI. Duobus
  r2 b'4 b'8 a'8 |
  d''4 b'8 g'8 g'4 g'8 b'8~ |
  b'8 g'8 a'8 b'4 g'4.~ |
  g'2 r2 |
  r2 b'4 b'8 a'8 |
  d''4 b'8 g'8 g'4 g'8 b'8~ |
  b'8 g'8 a'8 b'4 g'4.~ |
  g'2 r2 |
 
  % VII. Amen
  d'1~ |
  d'1 |
  e'1~ |
  e'1 |
  R1*4 |
}
sopranoWords = \lyricmode {
  "Di" -- "li" -- "ges" "Do" -- "mi" -- "num" "De" -- "um" "tu" -- "um" "ex"
  "to" -- "to" "cor" -- "de" "tu" -- "o" \repeat unfold 16 { \skip 1 }
  "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "tu" -- "um" "si" -- "cut"
  "te" -- "ip" -- "sum" "E" -- "li,"
  "E" -- "li,"
  "lam" -- "ma" "sa" -- "bac" -- "tha" -- "ni" "E" -- "li" -- "am" "vo" -- "cat"
  "is" -- "te" "Con" -- "sum" -- "ma" -- "tum" "est" "Ve" -- "re" "Fi" -- "li" -- "us"
  "De" -- "i" "e" -- "rat" "is" -- "te" "Ve" -- "re" "Fi" -- "li" -- "us"
  "De" -- "i" "e" -- "rat" "is" -- "te" "Ve" -- "re" "Fi" -- "li" -- "us"
  "De" -- "i" "e" -- "rat" "is" -- "te" "Ve" -- "re" "Fi" -- "li" -- "us"
  "De" -- "i" "e" -- "rat" "is" -- "te" "Ve" -- "re" "Fi" -- "li" -- "us"
  "De" -- "i" "e" -- "rat" "is" -- "te" "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum"
  "tu" -- "um" "si" -- "cut" "te" -- "ip" -- "sum" "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum"
  "tu" -- "um" "si" -- "cut" "te" -- "ip" -- "sum" \repeat unfold 2 { \skip 1 }
}

alto = {
  % I. Pendet
  R1*8 |
 
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
 
  % III. Simile
  R1*6 |
  e'4 e'8 d'8 g'4 e'8 c'8 |
  c'4 c'8 e'4 c'8 d'8 e'8~ |
  e'8 c'4.~ c'2 |
  d'2 b2 |
  b2 b2 |
  b2 c'2 |
 
  % IV. Golgotha
  R1*4 |
  R1*5 |
  R1*2 |
  R1*2 |
  R1*3 |
 
  % V. Vere
  R1*2 |
  a'4 g'4 e'4 f'4 |
  a'4 g'4 f'4 g'4 |
  g'4 a'4 g'4 a'4 |
  b'4 g'4 f'4 g'4 |
  g'4 a'4 g'4 a'4 |
  b'4 g'4 f'4 g'4 |
 
  % VI. Duobus
  b'2 g'2 |
  b'2 g'2 |
  e'2 g'2 |
  e'2 d'2 |
  b'2 g'2 |
  b'2 g'2 |
  e'2 g'2 |
  e'2 d'2 |
 
  % VII. Amen
  a1~ |
  a1 |
  gis1~ |
  gis1 |
  R1*4 |
}
altoWords = \lyricmode {
  "Di" -- "li" -- "ges" "Do" -- "mi" -- "num" "De" -- "um" "tu" -- "um" "ex"
  "to" -- "to" "cor" -- "de" "tu" -- "o" \repeat unfold 24 { \skip 1 }
  "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "tu" -- "um" "si" -- "cut"
  "te" -- "ip" -- "sum" \repeat unfold 48 { \skip 1 }
}

tenor = {
  % I. Pendet
  R1*8 |
 
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
 
  % III. Simile
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
 
  % IV. Golgotha
  R1*4 |
  R1*5 |
  R1*2 |
  R1*2 |
  R1*3 |
 
  % V. Vere
  R1*4 |
  b4 a4 c'4 c'4 |
  b4 d'4 c'4 g4 |
  b4 a4 c'4 c'4 |
  b4 d'4 c'4 g4 |
 
  % VI. Duobus
  b2 e'2 |
  d'2 e'2 |
  b2 b2 |
  b2 g2 |
  b2 e'2 |
  d'2 e'2 |
  b2 b2 |
  b2 g2 |
 
  % VII. Amen
  c1~ |
  c1 |
  b,1~ |
  b,1 |
  R1*4 |
}
tenorWords = \lyricmode {
  "Di" -- "li" -- "ges" "Do" -- "mi" -- "num" "De" -- "um" "tu" -- "um" "ex"
  "to" -- "to" "cor" -- "de" "tu" -- "o" \repeat unfold 8 { \skip 1 }
  "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "tu" -- "um" "si" -- "cut"
  "te" -- "ip" -- "sum" \repeat unfold 46 { \skip 1 }
}

bass = {
  % I. Pendet
  R1*8 |
 
  % II. Diliges
  R1*12 |
  b,4 b,8 a,8 d4 b,8 g,8 |
  a,4 g,8 g,4 g,8 a,4 |
  d4 d8 d4 a,8 g,4 |
  d,1 |
 
  % III. Simile
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
 
  % IV. Golgotha
  R1*4 |
  R1*5 |
  R1*2 |
  R1*2 |
  R1*3 |
 
  % V. Vere
  b4 g4 g4 a4 |
  g4 b4 a4 g4 |
  f4 g4 g4 a4 |
  f4 g4 a4 g4 |
  g4 f4 e4 f4 |
  d4 b,4 a,4 g,4 |
  g4 f4 e4 f4 |
  d4 b,4 a,4 g,4 |
 
  % VI. Duobus
  e4 e8 d8 g4 e8 c8 |
  d4 c8 c4 c8 d4 |
  g4 g8 g4 d8 c4 |
  g,1 |
  e4 e8 d8 g4 e8 c8 |
  d4 c8 c4 c8 d4 |
  g4 g8 g4 d8 c4 |
  g,1 |
 
  % VII. Amen
  f,1~ |
  f,1 |
  e,1~ |
  e,1 |
  R1*4 |
}
bassWords = \lyricmode {
  "Di" -- "li" -- "ges" "Do" -- "mi" -- "num" "De" -- "um" "tu" -- "um" "ex"
  "to" -- "to" "cor" -- "de" "tu" -- "o" "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum"
  "tu" -- "um" "si" -- "cut" "te" -- "ip" -- "sum" \repeat unfold 50 { \skip 1 }
  "Di" -- "li" -- "ges" "Do" -- "mi" -- "num" "De" -- "um" "tu" -- "um" "ex"
  "to" -- "to" "cor" -- "de" "tu" -- "o" "Di" -- "li" -- "ges" "Do" -- "mi" -- "num"
  "De" -- "um" "tu" -- "um" "ex" "to" -- "to" "cor" -- "de" "tu" -- "o" \repeat unfold 2 { \skip 1 }
}

organRHone = { \oneVoice e''8^\markup \small \italic { \bold II }^\markup \small \italic { "Gedackt 8', Flute 4': solo, legato" } e''8 f''8 g''4 f''8 e''4 |
  d''8 e''8 f''4 e''2 |
  b''8 a''8 g''8 f''8 g''4 f''8 e''8 |
  d''4 b'4 e''2 |
  R1*4 |
  R1*4 |
  b'4^\markup \small \italic { \bold I } b'8 a'8 d''4 b'8 g'8 |
  a'4 g'8 g'4 g'8 a'4 |
  d''4 d''8 d''4 a'8 g'4 |
  d'1 |
  \voiceOne b'2 g'2 |
  a'2 a'2 |
  g'2 g'2 |
  e'2 d'2 |
  b'2 b'2 |
  e''2 e''2 |
  d''2 b'2 |
  d''2 a'2 |
  \oneVoice R1*3 |
  b4 b8 a8 d'4 b8 g8 |
  g4 g8 b4 g8 a8 b8~ |
  b8 g4.~ g2 |
  \voiceOne e'4 e'8 d'8 g'4 e'8 c'8 |
  c'4 c'8 e'4 c'8 d'8 e'8~ |
  e'8 c'4.~ c'2 |
  \oneVoice b'4 b'8 a'8 d''4 b'8 g'8 |
  \voiceOne g'4 g'8 b'4 g'8 a'8 b'8~ |
  b'8 g'4.~ g'2 |
  \oneVoice R1*4 |
  R1*2 |
  d'8 e'4 f'8 g'4 f'8 e'8~ |
  e'8 d'4.~ d'2 |
  R1 |
  R1*2 |
  R1*2 |
  R1*3 |
  d''4 d''8 e''4 e''8 c''8 d''8~ |
  d''8 e''8 d''4 f''8 e''4 d''8 |
  \voiceOne d''4 d''8 e''4 e''8 c''8 d''8~ |
  d''8 e''8 d''4 f''8 e''4 d''8 |
  d''4 d''8 e''4 e''8 c''8 d''8~ |
  d''8 e''8 d''4 f''8 e''4 d''8 |
  d''4 d''8 e''4 e''8 c''8 d''8~ |
  d''8 e''8 d''4 f''8 e''4 d''8 |
  r2 b'4 b'8 a'8 |
  d''4 b'8 g'8 g'4 g'8 b'8~ |
  b'8 g'8 a'8 b'4 g'4. |
  e'2 d'2 |
  \oneVoice e''8^\markup \small \italic { \bold II }^\markup \small \italic { "Gedackt 8', Flute 4': solo, legato" } e''8 f''8 g''4 f''8 e''4 |
  d''8 e''8 f''4 e''2 |
  b''8 a''8 g''8 f''8 g''4 f''8 e''8 |
  d''4 b'4 e''2 |
  <a d'>1^\markup \small \italic { \bold I }~ |
  <a d'>1 |
  <gis e'>1^\markup \small \italic { \bold "Full organ" }~ |
  <gis e'>1 |
  R1*4 |
}
organRHtwo = { s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  \voiceTwo b2 b2 |
  a2 a2 |
  b2 d'2 |
  b2 g2 |
  d'2 d'2 |
  e'2 e'2 |
  f'2 d'2 |
  f'2 d'2 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  b2 c'2 |
  a2 c'2 |
  a2 g2 |
  s1 |
  b2 b2 |
  b2 c'2 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  a'4 g'4 e'4 f'4 |
  a'4 g'4 f'4 g'4 |
  g'4 a'4 g'4 a'4 |
  b'4 g'4 f'4 g'4 |
  g'4 a'4 g'4 a'4 |
  b'4 g'4 f'4 g'4 |
  b'2 g'2 |
  b'2 g'2 |
  e'2 g'2 |
  b2 g2 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
}
organLHone = { \clef "treble" \oneVoice e'1_\markup \small \italic { \bold I }_\markup \small \italic { "Principal 8' (soft): long notes" } |
  e'1 |
  e'2 a'2 |
  g'2 a'2~ |
  a'2 b'2 |
  a'2 c''2 |
  b'2 b'2~ |
  b'1 |
  e'4_\markup \small \italic { "Principal 8' (soft): with the choir" } e'8 d'8 g'4 e'8 c'8 |
  d'4 c'8 c'4 c'8 d'4 |
  g'4 g'8 g'4 d'8 c'4 |
  \clef "bass" g1 |
  d'2 b2 |
  c'2 c'2 |
  b2 g2 |
  b2 g2 |
  e4 e8 d8 g4 e8 c8 |
  d4 c8 c4 c8 d4 |
  g4 g8 g4 d8 c4 |
  g,1 |
  g2 b2 |
  e2 e2 |
  a2 b2 |
  a2 a2 |
  R1 |
  e8_\markup \small \italic { \bold II }_\markup \small \italic { "Gedackt 8', Flute 4': the wheel, staccato" \dynamic p } g8 b8 g8 e8 g8 b8 e'8 |
  R1 |
  e8 g8 b8 g8 e8 g8 b8 e'8 |
  R1 |
  e8 g8 b8 g8 e8 g8 b8 e'8 |
  R1 |
  e8 g8 b8 g8 e8 g8 b8 e'8 |
  R1 |
  e8 g8 b8 g8 e8 g8 b8 e'8 |
  e2_\markup \small \italic { \bold I } g2 |
  e8_\markup \small \italic { \bold II } g8 b8 g8 e8 g8 b8 e'8 |
  e8_\markup \small \italic { "Gedackt 8' alone, box closed" \dynamic pp } g8 b8 g8 e8 g8 b8 e'8 |
  e8 g8 b8 g8 e8 g8 b8 e'8 |
  e8 g8 b8 g8 e8 g8 b8 e'8 |
  e8 g8 b8 g8 e8 g8 b8 e'8 |
  R1*2 |
  R1*2 |
  R1 |
  R1*2 |
  R1*2 |
  R1*3 |
  R1*2 |
  e8_\markup \small \italic { "Gedackt 8', Flute 4', staccato" \dynamic mp } g8 b8 g8 e8 g8 b8 e'8 |
  e8 g8 b8 g8 e8 g8 b8 e'8 |
  e8 g8 b8 g8 e8 g8 b8 e'8 |
  e8 g8 b8 g8 e8 g8 b8 e'8 |
  e8 g8 b8 g8 e8 g8 b8 e'8 |
  e8 g8 b8 g8 e8 g8 b8 e'8 |
  e8 g8 b8 g8 e8 g8 b8 e'8 |
  e8 g8 b8 g8 e8 g8 b8 e'8 |
  e8 g8 b8 g8 e8 g8 b8 e'8 |
  e8 g8 b8 g8 e8 g8 b8 e'8 |
  e8 g8 b8 g8 e8 g8 b8 e'8 |
  e8 g8 b8 g8 e8 g8 b8 e'8 |
  e8 g8 b8 g8 e8 g8 b8 e'8 |
  e8 g8 b8 g8 e8 g8 b8 e'8 |
  c1_\markup \small \italic { \bold I }~ |
  c1 |
  b,1~ |
  b,1 |
  R1*4 |
}
organLHtwo = { s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
  s1 |
}
pedal = { \oneVoice <e, b,>1_\markup \small \italic { "Subbass 16', Bourdon 8': the fifth, held" }~ |
  <e, b,>1~ |
  <e, b,>1~ |
  <e, b,>1~ |
  <e, b,>1~ |
  <e, b,>1~ |
  <e, b,>1~ |
  <e, b,>1~ |
  <e, b,>1~ |
  <e, b,>1~ |
  <e, b,>1~ |
  <e, b,>1 |
  R1*8 |
  b,4_\markup \small \italic { "16' + 8': with the basses" } b,8 a,8 d4 b,8 g,8 |
  a,4 g,8 g,4 g,8 a,4 |
  d4 d8 d4 a,8 g,4 |
  d,1 |
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
  R1*4 |
  R1*2 |
  R1*2 |
  R1 |
  e,1_\markup \small \italic { "Subbass 16' (+ 32'): the earth quakes" \dynamic p }~ |
  e,1 |
  R1*2 |
  R1*3 |
  b4 g4 g4 a4 |
  g4 b4 a4 g4 |
  f4 g4 g4 a4 |
  f4 g4 a4 g4 |
  g4 f4 e4 f4 |
  d4 b,4 a,4 g,4 |
  g4 f4 e4 f4 |
  d4 b,4 a,4 g,4 |
  e4 e8 d8 g4 e8 c8 |
  d4 c8 c4 c8 d4 |
  g4 g8 g4 d8 c4 |
  g,1 |
  e4 e8 d8 g4 e8 c8 |
  d4 c8 c4 c8 d4 |
  g4 g8 g4 d8 c4 |
  g,1 |
  f,1~ |
  f,1 |
  e,1~ |
  e,1 |
  R1*4 |
}
bellCue = { R1*8 |
  g''4^\markup \tiny \italic "if no bells: R.H., II, Flute 8' + 4'" g''8 e''8 b''4 g''8 e''8 |
  e''4 e''8 e''4 e''8 e''4 |
  b''4 b''8 b''4 e''8 e''4 |
  b'1 |
  R1*12 |
  R1*12 |
  R1*4 |
  R1*2 |
  R1*2 |
  R1 |
  R1*2 |
  R1*2 |
  R1*3 |
  R1*2 |
  \ottava #1 e'''4^\markup \tiny \italic "if no bells: R.H. plays this on II, Flute 8' + 4', and leaves the choir's notes" e'''8 g'''4 g'''8 e'''8 e'''8~ |
  e'''8 g'''8 e'''4 g'''8 g'''4 e'''8 |
  e'''4 e'''8 g'''4 g'''8 e'''8 e'''8~ |
  e'''8 g'''8 e'''4 g'''8 g'''4 e'''8 |
  e'''4 e'''8 g'''4 g'''8 e'''8 e'''8~ |
  e'''8 g'''8 e'''4 g'''8 g'''4 e'''8 |
  R1*4 |
  R1*4 |
  R1*2 |
  R1*2 |
  R1*4 |
}
bells = { R1*8 |
  g''4\mp g''8 e''8 b''4 g''8 e''8 |
  e''4 e''8 e''4 e''8 e''4 |
  b''4 b''8 b''4 e''8 e''4 |
  b'1 |
  e''4 e''8 b'8 e''4 e''8 b'8 |
  b'4 b'8 b'4 b'8 b'4 |
  e''4 e''8 e''4 b'8 b'4 |
  e'1_\markup \tiny \italic "(2-oct. set: 8va)" |
  g''4 g''8 e''8 b''4 g''8 e''8 |
  e''4 e''8 e''4 e''8 e''4 |
  b''4 b''8 b''4 e''8 e''4 |
  b'1 |
  e''4 e''8 b'8 e''4 e''8 b'8 |
  b'4 b'8 b'4 b'8 b'4 |
  e''4 e''8 e''4 b'8 b'4 |
  e'1_\markup \tiny \italic "(2-oct. set: 8va)" |
  g''4 g''8 e''8 b''4 g''8 e''8 |
  R1 |
  r8 e''4.\p~ e''2 |
  R1 |
  b'4 b'8 e''4 b'8 b'8 e''8~ |
  e''8 r8 r4 r2 |
  g''4 g''8 e''8 b''4 g''8 e''8 |
  R1 |
  r8 e''4.\p~ e''2 |
  R1 |
  b'4 b'8 e''4 b'8 b'8 e''8~ |
  e''8 r8 r4 r2 |
  R1*4 |
  R1*2 |
  R1*2 |
  R1 |
  R1*2 |
  R1*2 |
  R1*3 |
  R1*2 |
  \ottava #1 e'''4\mp e'''8 g'''4 g'''8 e'''8 e'''8~ |
  e'''8 g'''8 e'''4 g'''8 g'''4 e'''8 |
  e'''4 e'''8 g'''4 g'''8 e'''8 e'''8~ |
  e'''8 g'''8 e'''4 g'''8 g'''4 e'''8 |
  e'''4 e'''8 g'''4 g'''8 e'''8 e'''8~ |
  e'''8 g'''8 e'''4 g'''8 g'''4 e'''8 |
  \ottava #0 r2 e''4 e''8 b'8 |
  e''4 e''8 b'8 b'4 b'8 e''8~ |
  e''8 b'8 b'8 e''4 b'4.~ |
  b'2 r2 |
  r2 e''4 e''8 b'8 |
  e''4 e''8 b'8 b'4 b'8 e''8~ |
  e''8 b'8 b'8 e''4 b'4.~ |
  b'2 r2 |
  R1*2 |
  <e'' gis'' b''>1\mf_\markup \small \italic "the light: let ring"\laissezVibrer~ |
  <e'' gis'' b''>1 |
  R1*4 |
}
bellsPart = { R1*6 |
  \cueDuring #"orgLH" #UP { R1*2^\markup \tiny \italic "Org. L.H." } |
  g''4\mp g''8 e''8 b''4 g''8 e''8 |
  e''4 e''8 e''4 e''8 e''4 |
  b''4 b''8 b''4 e''8 e''4 |
  b'1 |
  e''4 e''8 b'8 e''4 e''8 b'8 |
  b'4 b'8 b'4 b'8 b'4 |
  e''4 e''8 e''4 b'8 b'4 |
  e'1_\markup \tiny \italic "(2-oct. set: 8va)" |
  g''4 g''8 e''8 b''4 g''8 e''8 |
  e''4 e''8 e''4 e''8 e''4 |
  b''4 b''8 b''4 e''8 e''4 |
  b'1 |
  e''4 e''8 b'8 e''4 e''8 b'8 |
  b'4 b'8 b'4 b'8 b'4 |
  e''4 e''8 e''4 b'8 b'4 |
  e'1_\markup \tiny \italic "(2-oct. set: 8va)" |
  g''4 g''8 e''8 b''4 g''8 e''8 |
  R1 |
  r8 e''4.\p~ e''2 |
  R1 |
  b'4 b'8 e''4 b'8 b'8 e''8~ |
  e''8 r8 r4 r2 |
  g''4 g''8 e''8 b''4 g''8 e''8 |
  R1 |
  r8 e''4.\p~ e''2 |
  R1 |
  b'4 b'8 e''4 b'8 b'8 e''8~ |
  e''8 r8 r4 r2 |
  R1*13 |
  R1*3 |
  \cueDuring #"S" #UP { R1*2^\markup \tiny \italic "Sop." } |
  \ottava #1 e'''4\mp e'''8 g'''4 g'''8 e'''8 e'''8~ |
  e'''8 g'''8 e'''4 g'''8 g'''4 e'''8 |
  e'''4 e'''8 g'''4 g'''8 e'''8 e'''8~ |
  e'''8 g'''8 e'''4 g'''8 g'''4 e'''8 |
  e'''4 e'''8 g'''4 g'''8 e'''8 e'''8~ |
  e'''8 g'''8 e'''4 g'''8 g'''4 e'''8 |
  \ottava #0 r2 e''4 e''8 b'8 |
  e''4 e''8 b'8 b'4 b'8 e''8~ |
  e''8 b'8 b'8 e''4 b'4.~ |
  b'2 r2 |
  r2 e''4 e''8 b'8 |
  e''4 e''8 b'8 b'4 b'8 e''8~ |
  e''8 b'8 b'8 e''4 b'4.~ |
  b'2 r2 |
  R1*2 |
  <e'' gis'' b''>1\mf_\markup \small \italic "the light: let ring"\laissezVibrer~ |
  <e'' gis'' b''>1 |
  R1*4 |
}
perc = \drummode {
  R1*4 |
  r8 wbl16^\markup \small \italic "Temple bl."\mp r16 wbl16 r16 r8 wbl16 r16 wbl16 r16 wbl16 r16 r8 |
  r4 wbl8. r16 r8 wbl16 r16 wbl16 r16 wbl16 r16 |
  wbl16 r16 r8 wbl16 r16 r8 r4 wbl8. r16 |
  wbl16 r16 wbl8 r8 wbl16 r16 r8 wbl16 r16 wbl8. r16 |
  R1*16 |
  R1*3 |
  << {  wbh8^\markup \small \italic "Wood bl."\p wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 |
  wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 |
  wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 |
  wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 |
  wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 |
  wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 |
  wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 |
  wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 |
  wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 |
  wbl16^\markup \small \italic "Temple bl."\mp r16 wbl16 r16 r8 wbl16 r16 wbl16 r16 wbl16 r16 r4 |
  r8 wbl8 r8 wbl16 r16 r8 wbl8 r8 wbl8 |
  r8 wbl8 r4 wbl8. r16 r4 |
  r8 wbl8 r4 wbl16 r16 wbl16 r16 wbl16 r16 wbl16 r16 |
  wbh8^\markup \small \italic "Wood bl."\p r8 wbh8 r8 r4 wbh8 wbh8 |
  wbh8 r8 r8 wbh8 r4 r8 wbh8 | }
  \\ {  bd4_\markup \small \italic "B.D." r4 bd4 r4 |
  bd4 r4 bd4 r4 |
  bd4 r4 bd4 r4 |
  bd4 r4 bd4 r4 |
  bd4 r4 bd4 r4 |
  bd4 r4 bd4 r4 |
  bd4 r4 bd4 r4 |
  bd4 r4 bd4 r4 |
  bd4 r4 bd4 r4 |
  bd4 r4 bd4 r4 |
  bd4 r4 bd4 r4 |
  bd4 r4 bd4 r4 |
  bd4 r4 bd4 r4 |
  bd4 r4 r2 |
  bd4 r4 r2 | } >>
  cymc1:32^\markup \small \italic "Wind mach. (or cym.)"\pp~ |
  cymc1:32 |
  R1 |
  \after 2. \! cymr1:32^\markup \small \italic "Sus. cym., soft mallets"\f\>\laissezVibrer |
  tomfl8^\markup \small \italic "Timp."\p\< <wbl tomfl>8^\markup \small \italic "Temple bl." tomfl8 tomfl8 <wbl tomfl>8 tomfl8 tomfl8 <wbl tomfl>8\f |
  R1*2 |
  R1*3 |
  \after 2. \! bd1:32_\markup \small \italic "B.D. roll"\f\> |
  << {  wbh8^\markup \small \italic "Wood bl."\p wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 |
  wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 |
  wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 |
  wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 |
  wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 |
  wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 |
  wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 |
  wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 |
  wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 |
  wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 |
  wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 |
  wbl16^\markup \small \italic "Temple bl."\mp r16 wbl16 r16 r8 wbl16 r16 wbl16 r16 wbl16 r16 r4 |
  r8 wbl8 r8 wbl16 r16 r8 wbl8 r8 wbl8 |
  r8 wbl8 r4 wbl8. r16 r4 |
  r8 wbl8 r4 wbl16 r16 wbl16 r16 wbl16 r16 wbl16 r16 | }
  \\ {  bd4_\markup \small \italic "B.D." r4 bd4 r4 |
  bd4 r4 bd4 r4 |
  bd4 r4 bd4 r4 |
  bd4 r4 bd4 r4 |
  bd4 r4 bd4 r4 |
  bd4 r4 bd4 r4 |
  bd4 r4 bd4 r4 |
  bd4 r4 bd4 r4 |
  bd4 r4 bd4 r4 |
  bd4 r4 bd4 r4 |
  bd4 r4 bd4 r4 |
  bd4 r4 bd4 r4 |
  bd4 r4 bd4 r4 |
  bd4 r4 bd4 r4 |
  bd4 r4 bd4 r4 | } >>
  R1*2 |
  R1*2 |
  R1*4 |
}
percPart = \drummode {
  R1*3 |
  R1^\markup \tiny \italic "cue: Org." |
  r8 wbl16^\markup \small \italic "Temple bl."\mp r16 wbl16 r16 r8 wbl16 r16 wbl16 r16 wbl16 r16 r8 |
  r4 wbl8. r16 r8 wbl16 r16 wbl16 r16 wbl16 r16 |
  wbl16 r16 r8 wbl16 r16 r8 r4 wbl8. r16 |
  wbl16 r16 wbl8 r8 wbl16 r16 r8 wbl16 r16 wbl8. r16 |
  R1*16 |
  R1*2 |
  R1^\markup \tiny \italic "cue: Bass “tuum sicut teipsum”" |
  << {  wbh8^\markup \small \italic "Wood bl."\p wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 | }
  \\ {  bd4_\markup \small \italic "B.D." r4 bd4 r4 | } >>
  \repeat percent 8 { << {  wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 | }
  \\ {  bd4 r4 bd4 r4 | } >> }
  << {  wbl16^\markup \small \italic "Temple bl."\mp r16 wbl16 r16 r8 wbl16 r16 wbl16 r16 wbl16 r16 r4 | }
  \\ {  bd4 r4 bd4 r4 | } >>
  << {  r8 wbl8 r8 wbl16 r16 r8 wbl8 r8 wbl8 | }
  \\ {  bd4 r4 bd4 r4 | } >>
  << {  r8 wbl8 r4 wbl8. r16 r4 | }
  \\ {  bd4 r4 bd4 r4 | } >>
  << {  r8 wbl8 r4 wbl16 r16 wbl16 r16 wbl16 r16 wbl16 r16 | }
  \\ {  bd4 r4 bd4 r4 | } >>
  << {  wbh8^\markup \small \italic "Wood bl."\p r8 wbh8 r8 r4 wbh8 wbh8 | }
  \\ {  bd4 r4 r2 | } >>
  << {  wbh8 r8 r8 wbh8 r4 r8 wbh8 | }
  \\ {  bd4 r4 r2 | } >>
  cymc1:32^\markup \small \italic "Wind mach. (or cym.)"\pp~ |
  cymc1:32 |
  R1 |
  \after 2. \! cymr1:32^\markup \small \italic "Sus. cym., soft mallets"\f\>\laissezVibrer |
  tomfl8^\markup \small \italic "Timp."\p\< <wbl tomfl>8^\markup \small \italic "Temple bl." tomfl8 tomfl8 <wbl tomfl>8 tomfl8 tomfl8 <wbl tomfl>8\f |
  R1*2 |
  R1*3 |
  \after 2. \! bd1:32_\markup \small \italic "B.D. roll"\f\> |
  << {  wbh8^\markup \small \italic "Wood bl."\p wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 | }
  \\ {  bd4_\markup \small \italic "B.D." r4 bd4 r4 | } >>
  << {  wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 | }
  \\ {  bd4 r4 bd4 r4 | } >>
  << {  wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 | }
  \\ {  bd4 r4 bd4 r4 | } >>
  << {  wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 | }
  \\ {  bd4 r4 bd4 r4 | } >>
  << {  wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 |
  wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 |
  wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 | }
  \\ {  bd4 r4 bd4 r4 |
  bd4 r4 bd4 r4 |
  bd4 r4 bd4 r4 | } >>
  << {  wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 | }
  \\ {  bd4 r4 bd4 r4 | } >>
  << {  wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 |
  wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 |
  wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 wbh8 | }
  \\ {  bd4 r4 bd4 r4 |
  bd4 r4 bd4 r4 |
  bd4 r4 bd4 r4 | } >>
  << {  wbl16^\markup \small \italic "Temple bl."\mp r16 wbl16 r16 r8 wbl16 r16 wbl16 r16 wbl16 r16 r4 | }
  \\ {  bd4 r4 bd4 r4 | } >>
  << {  r8 wbl8 r8 wbl16 r16 r8 wbl8 r8 wbl8 | }
  \\ {  bd4 r4 bd4 r4 | } >>
  << {  r8 wbl8 r4 wbl8. r16 r4 | }
  \\ {  bd4 r4 bd4 r4 | } >>
  << {  r8 wbl8 r4 wbl16 r16 wbl16 r16 wbl16 r16 wbl16 r16 | }
  \\ {  bd4 r4 bd4 r4 | } >>
  R1*2 |
  R1*2 |
  R1*4 |
}

marksPart = {
  \tempo 4 = 120
  \mark \markup \box \bold "I"
  \sectionLabel \markup \line { \bold "Pendet" \hspace #1 \italic "bar 1 (0:00)" }
  s1*8
  \section
  \mark \markup \box \bold "II"
  \sectionLabel \markup \line { \bold "Diliges" \hspace #1 \italic "bar 9 (0:16)" }
  s1*16
  \section
  \mark \markup \box \bold "III"
  \sectionLabel \markup \line { \bold "Simile" \hspace #1 \italic "bar 25 (0:48)" }
  s1*12
  \section
  \mark \markup \box \bold "IV"
  \sectionLabel \markup \line { \bold "Golgotha" \hspace #1 \italic "bar 37 (1:12)" }
  \textMark \markup \italic "bells tacet"
  s1*16
  \section
  \mark \markup \box \bold "V"
  \sectionLabel \markup \line { \bold "Vere" \hspace #1 \italic "bar 53 (1:44)" }
  s1*8
  \section
  \mark \markup \box \bold "VI"
  \sectionLabel \markup \line { \bold "Duobus" \hspace #1 \italic "bar 61 (2:00)" }
  s1*8
  \section
  \mark \markup \box \bold "VII"
  \sectionLabel \markup \line { \bold "Amen" \hspace #1 \italic "bar 69 (2:16)" }
  s1*4
  \textMark \markup \italic "silence"
  \textMark \markup \column { \line { \bold "Reader (or the priest), optional, spoken:" } \line { \italic "“If ye love me, keep my commandments.”" "(John 14:15)" } }
  s1*4
  \bar "|."
}

marksPerc = {
  \tempo 4 = 120
  \mark \markup \box \bold "I"
  \sectionLabel \markup \line { \bold "Pendet" \hspace #1 \italic "bar 1 (0:00)" }
  s1*8
  \section
  \mark \markup \box \bold "II"
  \sectionLabel \markup \line { \bold "Diliges" \hspace #1 \italic "bar 9 (0:16)" }
  s1*16
  \section
  \mark \markup \box \bold "III"
  \sectionLabel \markup \line { \bold "Simile" \hspace #1 \italic "bar 25 (0:48)" }
  s1*12
  \section
  \mark \markup \box \bold "IV"
  \sectionLabel \markup \line { \bold "Golgotha" \hspace #1 \italic "bar 37 (1:12)" }
  \textMark \markup \italic "darkness"
  s1*4
  \textMark \markup \italic "the cry"
  s1*2
  \textMark \markup \italic "the crowd"
  s1*2
  \textMark \markup \italic "“it is finished”"
  s1*1
  \textMark \markup \italic "the rent"
  s1*2
  \textMark \markup \italic "the centurion"
  s1*2
  \textMark \markup \italic "the tomb: silence"
  s1*3
  \section
  \mark \markup \box \bold "V"
  \sectionLabel \markup \line { \bold "Vere" \hspace #1 \italic "bar 53 (1:44)" }
  \textMark \markup \italic "the stone"
  s1*8
  \section
  \mark \markup \box \bold "VI"
  \sectionLabel \markup \line { \bold "Duobus" \hspace #1 \italic "bar 61 (2:00)" }
  s1*4
  \textMark \markup \italic "the household"
  s1*4
  \section
  \mark \markup \box \bold "VII"
  \sectionLabel \markup \line { \bold "Amen" \hspace #1 \italic "bar 69 (2:16)" }
  s1*4
  \textMark \markup \italic "silence"
  \textMark \markup \column { \line { \bold "Reader (or the priest), optional, spoken:" } \line { \italic "“If ye love me, keep my commandments.”" "(John 14:15)" } }
  s1*4
  \bar "|."
}

\addQuote "S" { \soprano }
\addQuote "A" { \alto }
\addQuote "orgRH" { \organRHone }
\addQuote "orgLH" { \organLHone }

choir = \new ChoirStaff <<
  \new Staff \with { instrumentName = "Soprano" shortInstrumentName = "S." } <<
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

organ = \new PianoStaff \with {
  instrumentName = "Organ" shortInstrumentName = "Org."
  \consists Keep_alive_together_engraver
} <<
  \new Staff = "RH" <<
    \global \clef "treble"
    \new Voice = "RH1" { \organRHone }
    \new Voice = "RH2" { \organRHtwo }
  >>
  \new Staff = "LH" <<
    \global \clef "bass"
    \new Voice = "LH1" { \organLHone }
    \new Voice = "LH2" { \organLHtwo }
  >>
  \new Staff = "Ped" \with { instrumentName = "Ped." shortInstrumentName = "Ped." } <<
    \global \clef "bass"
    \new Voice = "Ped" { \pedal }
  >>
>>

bellStaff = \new Staff \with {
  instrumentName = \markup \center-column { "Bells" "(opt.)" } shortInstrumentName = "Bl."
  midiInstrument = "celesta"
} \new Voice = "Bells" { \global \clef "treble" \bells }

percStaff = \new DrumStaff \with {
  instrumentName = \markup \center-column { "Perc." "(opt.)" } shortInstrumentName = "Perc."
  drumStyleTable = #(alist->hash-table churchPercussion)
} { \numericTimeSignature \time 4/4 \perc }

\book {
  \markup \fontsize #-1.5 \column {
    \line { \bold "The edition" }
    \wordwrap-string #"The track at canon-lawyer.ca/music/ is techno: a kick drum, hi-hats and a square-wave arpeggio around a choir. This is the same piece for a parish, arranged by rule (organ_edition.py) from what the track plays. The choir's part is the choir score's, note for note and word for word; the organ doubles it, as the track's organ does, and takes the other layers in their own notes and rhythms. The bar numbers and the times are the track's: a bar is two seconds (quarter = 120); 76 bars, 2:32."
    \vspace #0.2
    \line { \bold "Forces" }
    \wordwrap-string #"SATB choir, with a soprano solo in Golgotha (the cry, “Consummatum est”, the centurion) and a few sopranos for the crowd; organ, two manuals and pedal. Optional: bells and percussion, a player each, and a reader."
    \vspace #0.2
    \line { \bold "The words" }
    \wordwrap-string #"The subjects are sung to the Latin of the Vulgate they are carved from. The free voices have no words yet (“free voices: text to be set”): they may sing on “ah”, or hum."
    \vspace #0.2
    \line { \bold "The organ" }
    \wordwrap-string #"Manual I doubles the choir (Principal 8', soft), and has Viri Galilaei in long notes. Manual II has the clock's wheel, staccato (Gedackt 8', Flute 4'), and the canticle of “Brother Electron”, a solo. The pedal doubles the basses at 16' and 8' and holds the fifth E–B in Pendet. In the darkness: Gedackt 8' alone, the box closed. In the earthquake: low E on 16' (and 32'). The last chord: full organ. Under the wheel the right hand takes the two upper voices that fit the hand, the subject first; at the end of Duobus it leaves the choir for the canticle."
    \vspace #0.2
    \line { \bold "The silences, and the spoken line" }
    \wordwrap-string #"In the darkness (37–40) the choir rests. At “it is finished” (45) the clock stops. The tomb (50–52) is silence for all, organ too. After the Amen, four bars of silence (73–76): in the first (2:24) a reader or the priest may say plainly “If ye love me, keep my commandments” (John 14:15); if not, keep the silence."
    \vspace #0.2
    \line { \bold "Bells (optional)" }
    \wordwrap-string #"One part for handbells, handchimes or glockenspiel, at the track's pitch: eight notes, the triad E–G–B over three octaves and the G♯ of the last chord (E4 B4 E5 G5 G♯5 B5 E6 G6). Handbells or handchimes (sounding an octave up): a 3-octave set plays it as written; a 2-octave set plays the low E an octave up (bars 16, 24). Glockenspiel (sounding two octaves up): the 8va passages without the 8va. Tubular bells (C4–F5) reach only the lowest notes."
    \vspace #0.2
    \line { \bold "Without bells" }
    \wordwrap-string #"The bells' line shadows whichever voice has the subject, so the music stands without them. Twice they carry what no one else has: their first entrance (9–12), the triad's light over the alto's subject, and their return after the tomb (55–60), high over the centurion's confession. There the organ has a cue staff for Manual II (in 55–60, instead of the choir's notes)."
    \vspace #0.2
    \line { \bold "Percussion (optional, one player)" }
    \wordwrap-string #"Bass drum (soft beater; soft mallets for rolls), woodblock or claves, temple block or side stick, suspended cymbal, one timpano on E, wind machine (or the cymbal). The clock: bass drum on 1 and 3, woodblock in eighths. The hammer: the Morse of “Is not this the carpenter”, a dot a sixteenth, a dash a dotted eighth. Where the track needs more than two hands, the part keeps the bass drum and the hammer (37–40, 65–68; the wheel has the eighths), the cymbal and then the timpani with the temple block in the rent (46, 47), and the bass drum roll at the stone (53). A second player could add the bass drum roll in 46–47 and the temple block in 46."
    \vspace #0.2
    \line { \bold "Without percussion, and in the liturgy" }
    \wordwrap-string #"The music stands, and loses the clock's tick (its eighths stay in the wheel), the hammer, the stutter under the cry, the wind under the crowd, the veil, rocks and timpani of the rent (the organ's low E stays), and the stone. In the liturgy choir and organ are enough, with bells if there are ringers: the clock lives on in the wheel, which a resonant building may keep on the Gedackt 8' alone, pp, throughout, at quarter = 96 to 104. The lawyer's question (Matthew 22:36) may be read first."
    \vspace #0.2
    \line { \bold "Sections" }
    \wordwrap-string #"I Pendet, bar 1 (0:00) · II Diliges, bar 9 (0:16) · III Simile, bar 25 (0:48) · IV Golgotha, bar 37 (1:12) · V Vere, bar 53 (1:44) · VI Duobus, bar 61 (2:00) · VII Amen, bar 69 (2:16)."
    \vspace #0.2
    \vspace #0.5
    \line { \italic "Dedicated to the public domain (CC0 1.0) · Made by Claude + Richard" }
  }
  \pageBreak
  \score {
    <<
      \new Staff \with { \remove "Staff_symbol_engraver" \override VerticalAxisGroup.remove-first = ##t } { \marks }
      \bellStaff
      \percStaff
      \choir
      \new Staff = "cue" \with {
        \magnifyStaff #2/3
        instrumentName = \markup \center-column { "Org. II" "(no bells)" } shortInstrumentName = "cue"
        \override VerticalAxisGroup.remove-first = ##t
      } { \global \clef "treble" \bellCue }
      \organ
    >>
    \layout {
      #(layout-set-staff-size 15)
      \context { \Staff \RemoveEmptyStaves \override VerticalAxisGroup.staff-staff-spacing.minimum-distance = #6 }
      \context { \DrumStaff \RemoveEmptyStaves }
      \context { \Score
        \override BarNumber.break-visibility = ##(#f #t #t)
        barNumberVisibility = #(every-nth-bar-number-visible 1)
        \override BarNumber.font-size = #-2
      }
      \context { \Lyrics
        \override LyricText.font-size = #0.5
        \override LyricHyphen.minimum-distance = #1.2
        \override LyricSpace.minimum-distance = #1.0
      }
    }
  }
  \score {
    <<
      \new Staff = "Bells" \with { midiInstrument = "celesta" } \new Voice = "Bells" { \bells }
      \new DrumStaff = "Percussion" { \perc }
      \new Staff = "Soprano" \with { midiInstrument = "choir aahs" } \new Voice = "S" { \soprano }
      \new Lyrics \lyricsto "S" { \sopranoWords }
      \new Staff = "Alto" \with { midiInstrument = "choir aahs" } \new Voice = "A" { \alto }
      \new Lyrics \lyricsto "A" { \altoWords }
      \new Staff = "Tenor" \with { midiInstrument = "choir aahs" } \new Voice = "T" { \tenor }
      \new Lyrics \lyricsto "T" { \tenorWords }
      \new Staff = "Bass" \with { midiInstrument = "choir aahs" } \new Voice = "B" { \bass }
      \new Lyrics \lyricsto "B" { \bassWords }
      \new Staff = "Organ right hand" \with { midiInstrument = "church organ" } << \new Voice = "RH1" { \organRHone } \new Voice = "RH2" { \organRHtwo } >>
      \new Staff = "Organ left hand" \with { midiInstrument = "church organ" } << \new Voice = "LH1" { \organLHone } \new Voice = "LH2" { \organLHtwo } >>
      \new Staff = "Organ pedal" \with { midiInstrument = "church organ" } \new Voice = "Ped" { \pedal }
    >>
    \midi { \tempo 4 = 120 }
  }
}

\book {
  \bookOutputSuffix "bells"
  \header {
    subsubtitle = \markup \bold "Handbells, chimes or glockenspiel (optional)"
    poet = ##f composer = ##f
  }
  \markup \fontsize #-1 \wordwrap-string #"Written at the track's pitch: handbells and handchimes sound an octave higher, the glockenspiel two. A 3-octave set (C4–C7) plays it as written; a 2-octave set (G4–G6) plays the low E an octave higher, where marked. Glockenspiel: play the 8va passages as printed, without the 8va. Small notes are cues. 76 bars, 2:32; a bar is two seconds."
  \score {
    <<
      \new Staff \with { \remove "Staff_symbol_engraver" \remove "Clef_engraver" \remove "Time_signature_engraver" } { \marksPart }
      \new Staff \with { instrumentName = "Bells" } { \global \clef "treble" \compressMMRests \bellsPart }
    >>
    \layout {
      #(layout-set-staff-size 18)
      \context { \Staff \RemoveEmptyStaves \override VerticalAxisGroup.remove-first = ##t }
      \context { \Score \override MultiMeasureRest.minimum-length = #30 }
    }
  }
  \paper { page-breaking = #ly:optimal-breaking }
}

\book {
  \bookOutputSuffix "percussion"
  \header {
    subsubtitle = \markup \bold "Percussion (optional, one player)"
    poet = ##f composer = ##f
  }
  \markup \fontsize #-1 \wordwrap-string #"Bass drum (soft beater; soft mallets for the rolls), woodblock (or claves), temple block (or side stick), suspended cymbal (soft mallets), one timpano tuned to E, wind machine (or the cymbal, rolled). The clock: bass drum on 1 and 3, woodblock in eighths. The hammer: the Morse of “Is not this the carpenter”, a dot a sixteenth, a dash a dotted eighth. Cues are in words. 76 bars, 2:32; a bar is two seconds."
  \markup \score {
  \new DrumStaff \with { drumStyleTable = #(alist->hash-table churchPercussion) \remove "Time_signature_engraver"
    \override StaffSymbol.staff-space = #0.9 }
  \drummode { \cadenzaOn
    cymr1_\markup \tiny \center-column { "susp." "cym." } s4 cymc1_\markup \tiny \center-column { "wind" "mach." } s4
    wbh1_\markup \tiny "woodbl." s4 wbl1_\markup \tiny \center-column { "temple" "block" } s4
    tomfl1_\markup \tiny \center-column { "timp." "(E)" } s4 bd1_\markup \tiny \center-column { "bass" "drum" } }
  \layout { indent = 0 ragged-right = ##t }
}
  \score {
    <<
      \new Staff \with { \remove "Staff_symbol_engraver" \remove "Clef_engraver" \remove "Time_signature_engraver" } { \marksPerc }
      \new DrumStaff \with { instrumentName = "Perc." drumStyleTable = #(alist->hash-table churchPercussion) }
        { \numericTimeSignature \time 4/4 \set countPercentRepeats = ##t
           \set repeatCountVisibility = #(every-nth-repeat-count-visible 4) \compressMMRests \percPart }
    >>
    \layout {
      #(layout-set-staff-size 19)
      \context { \Staff \RemoveEmptyStaves \override VerticalAxisGroup.remove-first = ##t }
      \context { \Score \override MultiMeasureRest.minimum-length = #30 }
    }
  }
  \paper { max-systems-per-page = 6 }
}
