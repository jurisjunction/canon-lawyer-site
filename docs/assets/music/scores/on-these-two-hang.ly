% On These Two Hang: the choir's lines, for SATB
% The choir's part of the track at canon-lawyer.ca/music/, bar for bar.
% Written by counterpoint.py --ly from the lines the track plays; do not edit by hand.
% Engrave with GNU LilyPond: lilypond on-these-two-hang.ly
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
  subtitle = "A double fugue for the household"
  subsubtitle = \markup \italic { "“On these two commandments hang all the law and the prophets” (Matthew 22:40)" }
  poet = "Words: the Vulgate"
  composer = "Notes made by rule: counterpoint.py"
  copyright = "Dedicated to the public domain (CC0 1.0)"
  tagline = \markup \small { "canon-lawyer.ca/music/ · Dedicated to the public domain (CC0 1.0) · Made by Claude + Richard" }
}

\markup \justify {
  The choir's part of the track, bar for bar, in mode III, E phrygian. The notes are written out by counterpoint.py
  from the same lines the track plays, and the bar numbers are the track's. The first eight bars, I. Pendet,
  belong to the instruments and to the lawyer's question, so the score begins at bar 9. Each subject is carved from
  its Latin words, a note to a syllable, and its words are set under every statement. The free voices around the
  subjects were found by a search under Fux's rules; they have no text yet. In Golgotha the choir rests through the
  darkness, the veil and the tomb. The last chords are the track's phrygian cadence, a note to a voice.
}

global = { \key e \phrygian \numericTimeSignature \time 4/4 }

marks = {
  \tempo 4 = 120 \set Score.currentBarNumber = #9
  \sectionLabel \markup \line { \bold "II. Diliges" \hspace #2 \italic "bar 9 (0:16)" }
  s8*128
  \section \sectionLabel \markup \line { \bold "III. Simile" \hspace #2 \italic "bar 25 (0:48)" }
  s8*96
  \set Score.skipBars = ##t
  \section \sectionLabel \markup \line { \bold "IV. Golgotha" \hspace #2 \italic "bar 37 (1:12)" }
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
  \section \sectionLabel \markup \line { \bold "V. Vere" \hspace #2 \italic "bar 53 (1:44)" }
  s8*64
  \section \sectionLabel \markup \line { \bold "VI. Duobus" \hspace #2 \italic "bar 61 (2:00)" }
  s8*32
  \set Score.currentBarNumber = #69
  \section \sectionLabel \markup \line { \bold "VII. Amen" \hspace #2 \italic "bar 69 (2:16)" }
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
  \repeat volta 2 { r2 b'4 b'8 a'8 |
  d''4 b'8 g'8 g'4 g'8 b'8~ |
  b'8 g'8 a'8 b'4 g'4.~ |
  g'2 r2 |
  }
  % VII. Amen
  d'1~ |
  d'1 |
  e'1~ |
  e'1 |
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
  "tu" -- "um" "si" -- "cut" "te" -- "ip" -- "sum" \repeat unfold 2 { \skip 1 }
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
  \repeat volta 2 { b'2 g'2 |
  b'2 g'2 |
  e'2 g'2 |
  e'2 d'2 |
  }
  % VII. Amen
  a1~ |
  a1 |
  gis1~ |
  gis1 |
}
altoWords = \lyricmode {
  "Di" -- "li" -- "ges" "Do" -- "mi" -- "num" "De" -- "um" "tu" -- "um" "ex"
  "to" -- "to" "cor" -- "de" "tu" -- "o" \repeat unfold 24 { \skip 1 }
  "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "tu" -- "um" "si" -- "cut"
  "te" -- "ip" -- "sum" \repeat unfold 40 { \skip 1 }
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
  \repeat volta 2 { b2 e'2 |
  d'2 e'2 |
  b2 b2 |
  b2 g2 |
  }
  % VII. Amen
  c1~ |
  c1 |
  b,1~ |
  b,1 |
}
tenorWords = \lyricmode {
  "Di" -- "li" -- "ges" "Do" -- "mi" -- "num" "De" -- "um" "tu" -- "um" "ex"
  "to" -- "to" "cor" -- "de" "tu" -- "o" \repeat unfold 8 { \skip 1 }
  "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum" "tu" -- "um" "si" -- "cut"
  "te" -- "ip" -- "sum" \repeat unfold 38 { \skip 1 }
}

bass = {
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
  \repeat volta 2 { e4 e8 d8 g4 e8 c8 |
  d4 c8 c4 c8 d4 |
  g4 g8 g4 d8 c4 |
  g,1 |
  }
  % VII. Amen
  f,1~ |
  f,1 |
  e,1~ |
  e,1 |
}
bassWords = \lyricmode {
  "Di" -- "li" -- "ges" "Do" -- "mi" -- "num" "De" -- "um" "tu" -- "um" "ex"
  "to" -- "to" "cor" -- "de" "tu" -- "o" "Di" -- "li" -- "ges" "pro" -- "xi" -- "mum"
  "tu" -- "um" "si" -- "cut" "te" -- "ip" -- "sum" \repeat unfold 50 { \skip 1 }
  "Di" -- "li" -- "ges" "Do" -- "mi" -- "num" "De" -- "um" "tu" -- "um" "ex"
  "to" -- "to" "cor" -- "de" "tu" -- "o" \repeat unfold 2 { \skip 1 }
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
  After the cadence the track keeps four bars of silence, and in them “If ye love me, keep my commandments” (John 14:15).
}
