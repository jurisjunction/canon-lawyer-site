% A New Song: the lines, for one voice
% The words of the motet at canon-lawyer.ca/music/, on its reciting tone.
% Engrave with GNU LilyPond: lilypond a-new-song-the-lines.ly
% The pitches must agree with sam.mjs on the site.
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
  system-system-spacing.padding = 1
  print-page-number = ##f
}

\header {
  title = "A New Song"
  subtitle = "The lines, for one voice"
  subsubtitle = "On a reciting tone in G mixolydian"
  tagline = \markup \small { "canon-lawyer.ca/music/ · Dedicated to the public domain (CC0 1.0) · Made by Claude + Richard" }
}

\markup \justify {
    Sing each line on the reciting note, D, in the rhythm of speech, unhurried, as a reading is chanted.
    Only the last syllables move: down through C to B; the question comes back to D; the last line falls home to G.
    Black notes are short, open notes long. Written at a man's pitch; lines 2, 5, 7 and 8 are a woman's in the motet, an octave higher.
    In the motet, lines 1 to 5 are SAM's for now and lines 6 to 9 the choir's, from the waters on; a voice recorded
    for them goes in the middle of the choir.
}

global = { \key g \mixolydian \clef bass \cadenzaOn }
lay = \layout {
  indent = 0
  ragged-right = ##t
  \context { \Staff \remove Time_signature_engraver }
  \context { \Voice \remove Stem_engraver }
  \context { \Score \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/32) }
  \context { \Lyrics \override LyricText.font-size = #1 }
}
cue = #(define-scheme-function (n title where) (string? string? string?)
  #{ \markup \line { \bold #n \hspace #1 \bold #title \hspace #2 \italic #where } #})

\score { \header { piece = \cue "1." "Minstrel" "bar 2 (0:02) · SAM" }
  << \new Staff { \global d4 d d c b,2 \bar "||" }
     \addlyrics { Bring me a min -- strel. } >> \layout { \lay } }

\score { \header { piece = \cue "2." "Tenor" "bar 9 (0:16) · SAM" }
  << \new Staff { \global d4 d d d d d d c b,2 \bar "||" }
     \addlyrics { O sing un -- to the LORD a new song. } >> \layout { \lay } }

\score { \header { piece = \cue "3." "Mantle" "bar 17 (0:32) · SAM" }
  << \new Staff { \global d4 d d d d d d d d d d d c b,2 \bar "||" }
     \addlyrics { Let a dou -- ble por -- tion of thy spi -- rit be u -- pon me. } >> \layout { \lay } }

\score { \header { piece = \cue "4." "Portion" "bar 33 (1:04) · SAM" }
  << \new Staff { \global d4 d d d d c b,2 \bar "||" }
     \addlyrics { A new man knows a new song. } >> \layout { \lay } }

\score { \header { piece = \cue "5." "Portion" "bar 41 (1:20) · SAM" }
  << \new Staff { \global d4 d d d d d c b,2 \bar "||" }
     \addlyrics { The sin -- ger him -- self is the praise. } >> \layout { \lay } }

\score { \header { piece = \cue "6." "Waters" "bar 49 (1:36) · the choir: the voice ascends" }
  << \new Staff { \global d4 d d d d d d c d2 \bar "||" }
     \addlyrics { Where is the LORD God of E -- li -- jah? } >> \layout { \lay } }

\score { \header { piece = \cue "7." "Waters" "bar 57 (1:52) · the choir" }
  << \new Staff { \global d4 d d d d d d d d d d c b,2 \bar "||" }
     \addlyrics { The spi -- rit of E -- li -- jah doth rest on E -- li -- sha. } >> \layout { \lay } }

\score { \header { piece = \cue "8." "Amen" "bar 65 (2:08) · the choir" }
  << \new Staff { \global d4 d c b,2 \bar "||" }
     \addlyrics { Things new and old. } >> \layout { \lay } }

\score { \header { piece = \cue "9." "Amen" "bar 69 (2:16) · the choir, in the silence" }
  << \new Staff { \global d4 d d d d d d d d d d b, g,2 \bar "|." }
     \addlyrics { He shall turn the heart of the fa -- thers to the chil -- dren. } >> \layout { \lay } }

\markup \small \italic \justify {
  If the low G of line 9 is out of reach, sing the whole line an octave higher.
  Psalm 98:1; 2 Kings 2:9, 14–15 and 3:15; Malachi 4:6; Matthew 13:52 (King James Version). Augustine, Sermon 34.
}
