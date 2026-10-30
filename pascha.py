"""
Reading Backwards from the Pascha: a year of Scripture read from its end.

A second track beside the Benedict Year (curriculum.py). The seven readings of the Easter Vigil are the
spine; every week is placed by what it is for. Everything here is data, and the pages are made from it:

    UNITS   the units, in order, each with its weeks
    WEEKS   one entry per teaching week: what is read aloud (Session A), what is argued (Session B),
            the card for the Tile Board, and a line for the parent
    BOOKS   every book the weeks use, with the weeks that use it

The build makes /curriculum/pascha/ (from _src/pages, with {{pascha_year}} and {{pascha_calendar}} filled
here), one page per unit, one per week, and /curriculum/pascha/books/. It refuses a week that names an
unknown unit or book, a gap in the numbering, and a unit whose weeks are not its own.

Dates are those of 2026-27 (Easter 27-28 March 2027, Year B). In another year the units move with Easter.
"""
import datetime
import html

esc = html.escape
INDEX = "/curriculum/pascha/"
FIRST_MONDAY = datetime.date(2026, 9, 14)
CHRISTMAS_AFTER = 14  # two weeks off after this week

SEASONS = [
    ("michaelmas", "Michaelmas", "September to November"),
    ("advent", "Advent", "late November to December"),
    ("hilary", "Hilary", "January to early February"),
    ("lent", "Lent", "Ash Wednesday, 10 February, to Holy Saturday"),
    ("easter", "Eastertide", "the Vigil to Pentecost"),
    ("june", "June", "the spiral closes"),
]

# ---------------------------------------------------------------------------------------------------
# Books. `free` is a public-domain text online; `for_parent` books are not read aloud.

BOOKS = {
    "bible": {"group": "Scripture", "title": "A Catholic Bible with the deuterocanonical books",
              "note": "Baruch and the Greek parts of Daniel are read in Lent, so the Bible must have them. The RSV Second Catholic Edition and the NABRE both do."},
    "ap": {"group": "Popular Patristics Series (St Vladimir’s Seminary Press)", "author": "Irenaeus of Lyons",
           "title": "On the Apostolic Preaching", "detail": "trans. John Behr, PPS 17"},
    "melito": {"group": "Popular Patristics Series (St Vladimir’s Seminary Press)", "author": "Melito of Sardis",
               "title": "On Pascha", "detail": "trans. Alistair Stewart-Sykes, PPS 20"},
    "athanasius": {"group": "Popular Patristics Series (St Vladimir’s Seminary Press)", "author": "Athanasius",
                   "title": "On the Incarnation", "detail": "trans. John Behr, PPS 44B"},
    "cyril": {"group": "Popular Patristics Series (St Vladimir’s Seminary Press)", "author": "Cyril of Jerusalem",
              "title": "Lectures on the Christian Sacraments", "detail": "the Mystagogical Catecheses, ed. F. L. Cross, PPS 57"},
    "ephrem": {"group": "Popular Patristics Series (St Vladimir’s Seminary Press)", "author": "Ephrem the Syrian",
               "title": "Hymns on Paradise", "detail": "trans. Sebastian Brock"},
    "origen": {"group": "Two more in print", "author": "Origen", "title": "Homilies on Genesis and Exodus",
               "detail": "trans. Ronald E. Heine, Fathers of the Church 71"},
    "nyssa": {"group": "Two more in print", "author": "Gregory of Nyssa", "title": "The Life of Moses",
              "detail": "Classics of Western Spirituality"},
    "ah": {"group": "Free online", "author": "Irenaeus of Lyons", "title": "Against Heresies",
           "detail": "Book I, chapter 8, section 1: the mosaic", "free": "https://www.newadvent.org/fathers/0103108.htm"},
    "justin": {"group": "Free online", "author": "Justin Martyr", "title": "Dialogue with Trypho",
               "detail": "chapter 100", "free": "https://www.newadvent.org/fathers/0128.htm"},
    "ambrose": {"group": "Free online", "author": "Ambrose of Milan", "title": "On the Mysteries",
                "detail": "chapter 3: the sea as the font", "free": "https://www.newadvent.org/fathers/3405.htm"},
    "chrysostom": {"group": "Free online", "author": "John Chrysostom", "title": "The Paschal Homily",
                   "detail": "read on Easter morning in the Byzantine churches"},
    "holysat": {"group": "Free online", "author": "An ancient homily", "title": "On Holy Saturday",
                "detail": "the Office of Readings for Holy Saturday (“Something strange is happening”). The author is unknown; the Patrologia Graeca gives it to Epiphanius. It is in any Liturgy of the Hours"},
    "exsultet": {"group": "Free online", "author": "The Roman Missal", "title": "The Exsultet",
                 "detail": "the Easter Proclamation sung at the Vigil"},
    "bibleproject": {"group": "Video", "author": "BibleProject", "title": "Free animated overviews and theme videos",
                     "detail": "bibleproject.com. The catalogue gets reorganized and some theme videos are now folded into longer series, so check each title as you go",
                     "free": "https://bibleproject.com/"},
    "behr": {"group": "For the parent", "author": "John Behr", "title": "The Mystery of Christ: Life in Death",
             "detail": "St Vladimir’s Seminary Press. The theology under the whole method: Christ known from the Cross, the Scriptures read from the end", "for_parent": True},
}

# ---------------------------------------------------------------------------------------------------
# Units. `weeks` are the week numbers; `vigil` marks the readings sung at the Easter Vigil.

UNITS = [
    {"slug": "the-hypothesis", "n": "0", "title": "The Hypothesis", "season": "michaelmas", "weeks": [1, 2, 3],
     "spine": "Luke 24",
     "lead": "The governing image of the whole year, given openly in the first week: the same tiles make a king or a fox, and the picture they are for decides.",
     "why": "On the road to Emmaus the risen Christ reads the Scriptures backwards, beginning from the end and interpreting in all of them the things concerning himself. Luke does not write the lecture down. The tradition read that silence as an assignment, and its answer is the set of readings sung at the Easter Vigil. This year borrows that answer whole.",
     "whatfor": "What were the Scriptures for, on the road? Luke answers: their hearts burned within them (24:32).",
     "unanswerable": "What did Jesus actually say on the road? Luke knows and won’t tell us. Why?"},
    {"slug": "creation", "n": "1", "title": "Creation", "season": "michaelmas", "weeks": [4, 5, 6, 7],
     "spine": "Genesis 1:1–2:2", "vigil": True,
     "lead": "The Vigil opens with creation because that night is a new creation.",
     "why": "John dates the resurrection to the first day of the week, and he is not reporting a calendar. The flood is a branch, one of the older Vigil prophecies: it sets up the sea three units early, so that when Israel goes down into the water he has already seen water that drowns and rescues in one motion. 1 Peter 3:20–21 calls it baptism outright.",
     "whatfor": "The rainbow. The text answers: a sign, so that God will remember the covenant (Genesis 9:15–16).",
     "unanswerable": "What’s the seventh day for, if the work was finished on the sixth?"},
    {"slug": "the-beloved-son", "n": "2", "title": "The Beloved Son", "season": "michaelmas", "weeks": [8, 9, 10],
     "spine": "Genesis 22:1–18", "vigil": True,
     "lead": "Isaac carries the wood up the mountain, and Origen says that is the Son carrying the Cross.",
     "why": "<em>God will provide himself the lamb</em>: Abraham was right, just not about the ram. It is a terrible chapter and it is meant to be. Warn the child the week before. Then ask, once, where else a father gives up a son, and let the child get there.",
     "whatfor": "The ram. The text answers: offered “in place of his son” (Genesis 22:13).",
     "unanswerable": "Does Isaac know? He is carrying the wood and asking about the lamb. Does Abraham pass or fail?"},
    {"slug": "the-king", "n": "", "title": "The King’s Week", "season": "michaelmas", "weeks": [11],
     "spine": "Matthew 25:31–46",
     "lead": "The Church’s year ends on the feast of Christ the King, and the mosaic was always of a king.",
     "why": "A week between Genesis 22 and Advent. The Gospel of the feast is the king who says “you did it to me”. Show the mosaic image again and say nothing about it. This is also the week to show the medieval windows that set Isaac carrying the wood beside Christ carrying the Cross: the child’s own discovery, made in glass by people who could not read.",
     "whatfor": "What did the king want the sheep to do? The text answers it.",
     "unanswerable": "They didn’t know it was him. Does it count?"},
    {"slug": "the-promise", "n": "3", "title": "The Promise", "season": "advent", "weeks": [12, 13, 14],
     "spine": "Genesis 3:15; Isaiah 7, 9 and 11; Luke 1",
     "lead": "A branch for Advent that plants Isaiah 11, which comes back in May at confirmation.",
     "why": "The shoot from the stump of Jesse, with the sevenfold Spirit resting on him, returns in May as the text behind the child’s own confirmation. Irenaeus on the knot of Eve’s disobedience untied by Mary’s obedience is recapitulation in miniature: the Pascha’s logic, small enough to hold.",
     "whatfor": "The Spirit resting on the shoot. The text answers: to judge the poor with justice (Isaiah 11:2–4).",
     "unanswerable": "Why a woman’s offspring, and not a warrior, to crush the serpent?"},
    {"slug": "the-sea", "n": "4", "title": "The Sea", "season": "hilary", "weeks": [15, 16, 17, 18],
     "spine": "Exodus 12; Exodus 14:15–15:1", "vigil": True,
     "lead": "The largest unit and the heart of the year.",
     "why": "Exodus 12 is an older Vigil prophecy restored here, and Holy Thursday’s first reading. Melito’s Easter homily is the centrepiece of the whole year: second-century, hammering and repetitive, built to be heard. Read it aloud; the child will feel it where they don’t follow it. Jonah comes last because Christ gives it as his own sign, and a child who has watched Israel come up out of the sea should meet at once a man who goes down into it and comes back on the third day.",
     "whatfor": "The blood on the doorposts. The text answers: a sign, so that the destroyer passes over (Exodus 12:13).",
     "unanswerable": "Why does God harden Pharaoh’s heart?"},
    {"slug": "the-servant-and-the-waters", "n": "5", "title": "The Servant and the Waters", "season": "hilary", "weeks": [19, 20],
     "spine": "Isaiah 54:5–14; Isaiah 55:1–11", "vigil": True,
     "lead": "The fourth and fifth readings of the Vigil, with Isaiah 53 beside them: not in the Vigil, and not optional.",
     "why": "Acts 8 stands in for a Father of the Church because it is the move, earlier: a man reads Isaiah 53 aloud, asks who it means, is told, and asks at once for water.",
     "whatfor": "The rain and the word. The text answers: they do not return empty, but do what they were sent for (Isaiah 55:10–11).",
     "unanswerable": "Who is the servant? Jews and Christians have read this differently for two thousand years, and both readings are serious. Say so plainly."},
    {"slug": "wisdom", "n": "6", "title": "Wisdom", "season": "lent", "weeks": [21],
     "spine": "Baruch 3:9–4:4", "vigil": True,
     "lead": "Wisdom appeared on earth and lived among men. That is the unit; don’t inflate it.",
     "why": "It is the natural moment to explain why Baruch is in a Catholic Bible and not in a Protestant one: better from you, calmly, than from someone using it as a weapon. February is also when the four senses of Scripture arrive as a Latin couplet, after five months of practising them unnamed.",
     "whatfor": "The law. Baruch answers: all who hold her fast will live (4:1).",
     "unanswerable": "If wisdom is a gift, why is it also a command?"},
    {"slug": "the-new-heart", "n": "7", "title": "The New Heart", "season": "lent", "weeks": [22, 23],
     "spine": "Ezekiel 36:16–28", "vigil": True,
     "lead": "<em>I will sprinkle clean water upon you, and a new heart I will give you.</em> Read it, then Romans 6, then stop talking.",
     "why": "Daniel 3 is a branch, an older Vigil prophecy: three youths unburnt and a fourth figure walking with them, the Old Testament’s clearest image of the one who goes into the fire with you. Their song, the Benedicite, is no longer sung at the Roman Vigil; the Byzantine Vigil still sings it, with its verses, as the fifteenth reading.",
     "whatfor": "The new heart. The text answers: to walk in my statutes (Ezekiel 36:27).",
     "unanswerable": "Can a heart be given, or only grown?"},
    {"slug": "mark", "n": "8", "title": "Mark", "season": "lent", "weeks": [24, 25],
     "spine": "the Gospel of Mark, whole",
     "lead": "Easter 2027 is Year B, so the Vigil Gospel is Mark 16:1–7. The child reads the book in Lent and hears its last page sung in the dark.",
     "why": "About ninety minutes straight through, in four sittings: a passion narrative with a long introduction. Don’t stop to explain. Mark’s speed is the argument. Watch the overview video only after Easter.",
     "whatfor": "The message at the empty tomb. The text answers: go and tell (16:7).",
     "unanswerable": "Why does Mark end with the women saying nothing to anyone, for they were afraid (16:8)?"},
    {"slug": "holy-week", "n": "", "title": "Holy Week and the Vigil", "season": "lent", "weeks": [26],
     "spine": "the liturgy itself",
     "lead": "Stop teaching. Go to things.",
     "why": "Holy Thursday’s first reading is Exodus 12; Good Friday’s is Isaiah 53. The child will recognize both. Say nothing. Read the Exsultet at the table earlier in the week, because in the dark it goes past too fast. On Holy Saturday night, eat first and warn the child the Vigil runs two to three hours. Ring the parish in February and ask how many readings they will do; many cut to three or four. If one nearby does all seven, go there.",
     "whatfor": "",
     "unanswerable": ""},
    {"slug": "easter-week", "n": "9", "title": "Something Strange Is Happening", "season": "easter", "weeks": [27],
     "spine": "the ancient homily for Holy Saturday",
     "lead": "The explaining goes after, and now it starts.",
     "why": "That the child is already baptized does not weaken this; it sharpens it. Cyril explained to people what had happened to them the week before. You are explaining to a child what happened to them at an age they can’t remember, which they have just spent seven months learning the meaning of.",
     "whatfor": "",
     "unanswerable": ""},
    {"slug": "cyril", "n": "10", "title": "Cyril", "season": "easter", "weeks": [28, 29, 30, 31],
     "spine": "Cyril of Jerusalem, the Mystagogical Catecheses",
     "lead": "Delivered in Easter week to the newly initiated, explaining what they had just undergone. Now you can talk.",
     "why": "One catechesis a week, beside Acts read straight through, as the Easter lectionary does. The third catechesis, on the chrism, is kept for the confirmation weeks. This is when the year’s hypothesis gets its whole name: the end was first. Read Ephesians 1:10, the plan to sum up all things in Christ.",
     "whatfor": "The renunciation of Satan at the font. Cyril answers with Pharaoh: it is the crossing of the sea (Catechesis I).",
     "unanswerable": ""},
    {"slug": "confirmation", "n": "11", "title": "Confirmation", "season": "easter", "weeks": [32, 33, 34],
     "spine": "Acts 2; Isaiah 11:1–3; Romans 8",
     "lead": "Isaiah 11 comes back. The child met the sevenfold Spirit resting on the shoot in December; in May it is poured on their own forehead.",
     "why": "Point that out once, then leave it alone. Time these weeks to the child’s own date. At confirmation they renew their baptismal promises: the Creed they profess that day is the one thing nothing in either track edits. In Canada the Ascension is kept on Sunday 9 May 2027; Pentecost is Sunday 16 May.",
     "whatfor": "The chrism. Cyril answers: anointed, they share the name of the Anointed and are called Christians (Catechesis III).",
     "unanswerable": ""},
    {"slug": "the-spiral", "n": "", "title": "The Spiral", "season": "june", "weeks": [35, 36, 37, 38],
     "spine": "Luke 24, again",
     "lead": "The same texts, and the child is not the same reader.",
     "why": "The last two branches fall on their own feasts: the Trinity, which arrives out of texts the child already has, and Corpus Christi. Then Luke 24 again, Genesis 1 and 22 again, the envelope sealed in September opened, and a plain account of what was left out and why. Round two hangs on a frame that now exists.",
     "whatfor": "",
     "unanswerable": ""},
]

# ---------------------------------------------------------------------------------------------------
# Weeks. A: read aloud, in order (scripture first, then a Father); B: the argument; card: the Tile Board.
# Each reading is (text, book key or None). Each B item is (label, text).

WEEKS = {
    1: {"unit": "the-hypothesis", "title": "The road, and the mosaic",
        "A": [("Luke 24:1–35", "bible"), ("Irenaeus, <em>Against Heresies</em> I.8.1, the mosaic of the king and the fox. Show a mosaic image first; it takes ten seconds", "ah")],
        "B": [("Unanswerable", "What did Jesus actually say on the road? Luke knows and won’t tell us. Why?"),
              ("Video", "<em>The Story of the Bible</em>")],
        "card": "The road to Emmaus", "note": "Give the image of the mosaic in the first ten minutes of the year. It is the governing image of everything after it."},
    2: {"unit": "the-hypothesis", "title": "The envelope",
        "A": [("Luke 24:36–53", "bible"), ("Irenaeus, <em>On the Apostolic Preaching</em> §§1–16: the rule of faith, and creation", "ap")],
        "B": [("The envelope", "The child writes the whole Bible in three sentences, seals it in an envelope, and puts it away until June."),
              ("Video", "<em>How to Read the Bible</em>, the opening video")],
        "card": "Opened scriptures (Luke 24:45)", "note": "Don’t read the three sentences. Seal them as written."},
    3: {"unit": "the-hypothesis", "title": "Moses and all the prophets",
        "A": [("Luke 24:25–27 and 44–47, read again", "bible"), ("Irenaeus, <em>On the Apostolic Preaching</em> §§17–42: from Cain to the Incarnation", "ap")],
        "B": [("What is it for?", "What were the Scriptures for, on the road? Luke answers it (24:32).")],
        "card": "Hearts burning", "note": "Irenaeus is the year in miniature. Read it aloud and let it go over the child’s head."},
    4: {"unit": "creation", "title": "In the beginning",
        "A": [("Genesis 1:1–2:3", "bible"), ("Ephrem, <em>Hymns on Paradise</em>, the first hymn, aloud", "ephrem")],
        "B": [("Video", "<em>Genesis 1–11</em>"), ("Unanswerable", "What’s the seventh day for, if the work was finished on the sixth? Hold it; it comes back in week 7.")],
        "card": "Light on the first day", "note": "The Vigil’s first reading. Read it as poetry, not as a lab report."},
    5: {"unit": "creation", "title": "The first day of the week",
        "A": [("John 1:1–18; John 20:1", "bible"), ("Athanasius, <em>On the Incarnation</em> §§1–5", "athanasius")],
        "B": [("What is it for?", "Why does John say “on the first day of the week”? He is not reporting a calendar."),
              ("Video", "<em>Image of God</em>")],
        "card": "The first day of the week", "note": "Athanasius was exiled five times for a sentence about the Son. The child will meet that fight again in June."},
    6: {"unit": "creation", "title": "The flood",
        "A": [("Genesis 6:5–7:24", "bible"), ("Athanasius, <em>On the Incarnation</em> §§6–10", "athanasius")],
        "B": [("Video", "<em>Heaven and Earth</em>"), ("Read with parts", "Genesis 7, with a narrator, Noah and God.")],
        "card": "The ark", "note": "The flood is one of the older Vigil prophecies, a branch. It plants the sea for January."},
    7: {"unit": "creation", "title": "Water that drowns and saves",
        "A": [("Genesis 8:1–9:17; 1 Peter 3:18–22", "bible"), ("Ephrem, <em>Hymns on Paradise</em>, another hymn, aloud", "ephrem")],
        "B": [("What is it for?", "The rainbow. The text answers (Genesis 9:15–16)."),
              ("Take opposite sides", "What’s the seventh day for? One argues it is for God, the other that it is for us."),
              ("Video", "<em>7th Day Rest</em>")],
        "card": "Water that drowns and saves", "note": "Warn the child, before Friday, that next week’s chapter is a terrible one."},
    8: {"unit": "the-beloved-son", "title": "The mountain",
        "A": [("Genesis 22:1–19, and nothing else", "bible")],
        "B": [("Unanswerable", "Does Isaac know? He is carrying the wood and asking about the lamb."),
              ("Video", "<em>Genesis 12–50</em>")],
        "card": "Isaac carrying the wood", "note": "Read it and stop. Let the silence after it stand."},
    9: {"unit": "the-beloved-son", "title": "Abraham on trial",
        "A": [("Genesis 22:1–19, again", "bible"), ("Origen, <em>Homily VIII on Genesis</em>, the first half", "origen")],
        "B": [("Put someone on trial", "Abraham: does he pass or fail? The child argues one side, you the other, then swap."),
              ("What is it for?", "The ram. The text answers (Genesis 22:13).")],
        "card": "The ram in the thicket", "note": "Origen says Isaac carrying the wood is the Son carrying the Cross. Let Origen say it; don’t add to it."},
    10: {"unit": "the-beloved-son", "title": "God will provide himself the lamb",
         "A": [("Genesis 22:6–14; John 1:29; Romans 8:32", "bible"), ("Origen, <em>Homily VIII on Genesis</em>, the second half", "origen")],
         "B": [("The question, once", "Where else does a father give up a son? Ask it, then wait as long as it takes."),
               ("Video", "<em>Sacrifice and Atonement</em>; <em>The Test</em>")],
         "card": "The Lamb of God (John 1:29)", "note": "If the child gets there alone, the connection is worth ten tellings. If not, leave it open."},
    11: {"unit": "the-king", "title": "The King’s week",
         "A": [("Matthew 25:31–46, the Gospel of Christ the King (22 November 2026)", "bible")],
         "B": [("Show", "The mosaic image again, and say nothing about it. Then medieval stained glass that sets Isaac carrying the wood beside Christ carrying the Cross."),
               ("Unanswerable", "They didn’t know it was him. Does it count?")],
         "card": "The King on his throne", "note": "The child’s November discovery, made in glass by people who could not read: they are rejoining a civilization."},
    12: {"unit": "the-promise", "title": "The woman and the serpent",
         "A": [("Genesis 3:1–15", "bible"), ("Irenaeus, <em>On the Apostolic Preaching</em> §§32–33: Mary as the new Eve", "ap")],
         "B": [("Read with parts", "Genesis 3, with the serpent, the woman, the man and God."),
               ("Video", "<em>Messiah</em>")],
         "card": "The woman and the serpent’s head", "note": "Advent begins on Sunday 29 November 2026."},
    13: {"unit": "the-promise", "title": "Emmanuel",
         "A": [("Isaiah 7:10–16; Isaiah 9:1–7", "bible"), ("Justin Martyr, <em>Dialogue with Trypho</em> 100: the new Eve, earlier than Irenaeus", "justin")],
         "B": [("Unanswerable", "Why a woman’s offspring, and not a warrior, to crush the serpent?"),
               ("Video", "<em>Luke 1–2</em>")],
         "card": "The child called Emmanuel", "note": "Justin makes the same move as Irenaeus a generation earlier. That is all the child needs to notice."},
    14: {"unit": "the-promise", "title": "The shoot from the stump",
         "A": [("Isaiah 11:1–10; Luke 1:26–56", "bible")],
         "B": [("What is it for?", "The Spirit resting on the shoot. The text answers (Isaiah 11:2–4)."),
               ("By heart", "Isaiah 11:1–2.")],
         "card": "The shoot from Jesse’s stump", "note": "Then stop. Two weeks off over Christmas, 21 December to 1 January. Take them."},
    15: {"unit": "the-sea", "title": "The lamb in Egypt",
         "A": [("Exodus 12:1–28", "bible")],
         "B": [("What is it for?", "The blood on the doorposts. The text answers (Exodus 12:13)."),
               ("Video", "<em>Passover</em>")],
         "card": "The blood on the doorposts", "note": "Exodus 12 will be the first reading on Holy Thursday. Don’t say so."},
    16: {"unit": "the-sea", "title": "The sea",
         "A": [("Exodus 14:15–15:1; Exodus 15:1–21; 1 Corinthians 10:1–4", "bible"), ("Ambrose, <em>On the Mysteries</em>, chapter 3: the sea as the font", "ambrose"),
               ("Gregory of Nyssa, <em>The Life of Moses</em>, Book II, the crossing of the sea", "nyssa")],
         "B": [("Unanswerable", "Why does God harden Pharaoh’s heart?"), ("Video", "<em>Exodus</em>")],
         "card": "The sea", "note": "Paul tells new Christians in Corinth that “our fathers” passed through the sea. The scriptural furniture arrived with the gospel, out loud."},
    17: {"unit": "the-sea", "title": "Melito, first half",
         "A": [("Melito, <em>On Pascha</em> §§1–45, aloud and without stopping", "melito")],
         "B": [("Video", "<em>Exodus Way</em>"), ("Read with parts", "Melito’s lines for Israel and for the Lord, if the child wants a part.")],
         "card": "The lamb, and the Lamb (Melito)", "note": "The centrepiece of the year. Hammering and repetitive, built to be heard."},
    18: {"unit": "the-sea", "title": "Melito, second half, and Jonah",
         "A": [("Melito, <em>On Pascha</em> §§46–105", "melito"), ("Jonah 1–4, whole; Matthew 12:38–41", "bible")],
         "B": [("Video", "<em>Water of Life</em>"), ("What is it for?", "Jonah’s three days. Christ answers in Matthew 12:40.")],
         "card": "Jonah’s three days", "note": "Jonah is four chapters. Read all of it."},
    19: {"unit": "the-servant-and-the-waters", "title": "The servant",
         "A": [("Isaiah 52:13–53:12; Acts 8:26–40", "bible")],
         "B": [("Unanswerable", "Who is the servant? Both readings are serious. Say so plainly."), ("Video", "<em>Isaiah</em>")],
         "card": "The lamb led to the slaughter", "note": "Isaiah 53 is not a Vigil reading. It is Good Friday’s, and not optional."},
    20: {"unit": "the-servant-and-the-waters", "title": "Come to the waters",
         "A": [("Isaiah 54:5–14; Isaiah 55:1–11", "bible")],
         "B": [("What is it for?", "The rain and the word. The text answers (Isaiah 55:10–11)."), ("By heart", "Isaiah 55:1.")],
         "card": "Come to the waters", "note": "Ash Wednesday is 10 February 2027, in this week."},
    21: {"unit": "wisdom", "title": "Wisdom on earth",
         "A": [("Baruch 3:9–4:4; John 1:14", "bible")],
         "B": [("The four senses", "The Latin couplet: <em>Littera gesta docet, quid credas allegoria, moralis quid agas, quo tendas anagogia</em>. The letter teaches what happened; allegory what to believe; the moral sense what to do; the anagogical sense where you are heading. The child has practised all four since September. The last one is the year’s own: where you are heading."),
               ("What is it for?", "The law. Baruch answers (4:1).")],
         "card": "Wisdom living among men", "note": "Explain, calmly, why Baruch is in a Catholic Bible and not a Protestant one."},
    22: {"unit": "the-new-heart", "title": "Clean water, a new heart",
         "A": [("Ezekiel 36:16–28; Romans 6:3–11", "bible")],
         "B": [("By heart", "Romans 6:3–4."), ("What is it for?", "The new heart. The text answers (Ezekiel 36:27)."), ("Video", "<em>Ezekiel</em>")],
         "card": "Clean water", "note": "Read Ezekiel, then Romans 6, then stop talking. Nothing needs arguing."},
    23: {"unit": "the-new-heart", "title": "The valley and the furnace",
         "A": [("Ezekiel 37:1–14; Daniel 3, with the Song of the Three Young Men", "bible")],
         "B": [("Read with parts", "Daniel 3, with the king, the three, and a chorus for the song."),
               ("Unanswerable", "Can a heart be given, or only grown?"), ("Video", "<em>Holy Spirit</em>")],
         "card": "The fourth in the fire", "note": "Ring the parish now if you haven’t: how many readings at the Vigil?"},
    24: {"unit": "mark", "title": "Mark, sittings one and two",
         "A": [("Mark 1:1–4:34", "bible")],
         "B": [("A second sitting", "Mark 4:35–8:26, in place of the argument this week.")],
         "card": "The torn heavens (Mark 1:10)", "note": "Don’t stop to explain. Mark’s speed is the argument."},
    25: {"unit": "mark", "title": "Mark, sittings three and four",
         "A": [("Mark 8:27–13:37", "bible")],
         "B": [("The last sitting", "Mark 14:1–16:8."), ("Unanswerable", "Why does Mark end with the women saying nothing, for they were afraid?")],
         "card": "The young man in white (Mark 16:5)", "note": "Mark 16:1–7 will be the Vigil Gospel. The child has now read the page they will hear sung."},
    26: {"unit": "holy-week", "title": "Holy Week",
         "A": [("The Exsultet, read at the table early in the week", "exsultet")],
         "B": [("Go to things", "Holy Thursday (Exodus 12 is its first reading), Good Friday (Isaiah 53), and the Vigil on Saturday 27 March 2027.")],
         "card": "", "note": "Say nothing on Holy Thursday when the child recognizes Exodus 12, and nothing at the Vigil. You do nothing that night. That was the point of building it this way."},
    27: {"unit": "easter-week", "title": "Something strange is happening",
         "A": [("The ancient homily for Holy Saturday: “there is a great silence on earth today”", "holysat"),
               ("Chrysostom’s Paschal Homily, aloud on Easter morning", "chrysostom")],
         "B": [("The Tile Board", "Ink the pencilled lines that still hold, each as an arrow from a card to what it points to. Rub out the rest. Ask once where the arrows go, then leave it."),
               ("Video", "The overview of Mark, at last.")],
         "card": "Ink the arrows", "note": "The explaining goes after, and now it starts."},
    28: {"unit": "cyril", "title": "The renunciation",
         "A": [("Acts 1–4", "bible"), ("Cyril, <em>Mystagogical Catechesis</em> I: the renunciation of Satan, and Pharaoh at the sea", "cyril")],
         "B": [("Name it", "Ephesians 1:3–14. The plan to sum up all things in Christ (1:10): the end was first. This is the hypothesis’s whole name."),
               ("What is it for?", "The renunciation at the font. Cyril answers with Pharaoh.")],
         "card": "", "note": "Now you can talk."},
    29: {"unit": "cyril", "title": "Baptism",
         "A": [("Acts 5–8", "bible"), ("Cyril, <em>Mystagogical Catechesis</em> II: baptism, and Romans 6", "cyril")],
         "B": [("Look back", "Which cards on the Tile Board does Cyril use? Let the child find them.")],
         "card": "", "note": "The child memorized Romans 6:3–4 in Lent. Cyril quotes it."},
    30: {"unit": "cyril", "title": "The Body and Blood",
         "A": [("Acts 9–12", "bible"), ("Cyril, <em>Mystagogical Catechesis</em> IV: the Eucharist", "cyril")],
         "B": [("Take opposite sides", "Cyril says not to judge by taste. Argue for the senses, then for Cyril.")],
         "card": "", "note": ""},
    31: {"unit": "cyril", "title": "The liturgy",
         "A": [("Acts 13–15", "bible"), ("Cyril, <em>Mystagogical Catechesis</em> V: the liturgy and the Lord’s Prayer", "cyril")],
         "B": [("Look back", "Walk through Sunday’s Mass with Cyril’s fifth catechesis open beside it.")],
         "card": "", "note": "Catechesis III, on the chrism, waits for the confirmation weeks."},
    32: {"unit": "confirmation", "title": "Pentecost",
         "A": [("Acts 2:1–41", "bible"), ("Cyril, <em>Mystagogical Catechesis</em> III: the chrism", "cyril")],
         "B": [("What is it for?", "The chrism. Cyril answers it."), ("Video", "<em>Holy Spirit</em>")],
         "card": "", "note": "The Ascension is kept in Canada on Sunday 9 May 2027."},
    33: {"unit": "confirmation", "title": "The sevenfold Spirit",
         "A": [("Isaiah 11:1–3, back from Advent; Romans 8:1–17", "bible")],
         "B": [("Point it out once", "The shoot from Jesse’s stump in December, and the same Spirit on the child’s forehead in May. Then leave it alone."), ("Video", "<em>Pentecost</em>")],
         "card": "", "note": "Pentecost is Sunday 16 May 2027. Time these weeks to the child’s own date."},
    34: {"unit": "confirmation", "title": "Creation groaning",
         "A": [("Romans 8:18–39", "bible")],
         "B": [("The profession", "The child renews the baptismal promises at confirmation. Read them together beforehand, slowly, and leave them unexplained.")],
         "card": "", "note": ""},
    35: {"unit": "the-spiral", "title": "The Trinity",
         "A": [("Matthew 28:16–20, the Gospel of Trinity Sunday (23 May 2027); Genesis 1:26; John 1:1–3; Romans 8:14–17", "bible")],
         "B": [("Name it", "The doctrine arrives out of texts already in the child, and a fight already personified: Athanasius, exiled five times for a sentence.")],
         "card": "", "note": "Doctrine met this way is remembered as the grammar of something loved."},
    36: {"unit": "the-spiral", "title": "Corpus Christi",
         "A": [("John 6:35–69; 1 Corinthians 11:23–26", "bible")],
         "B": [("Look back", "The manna, the lamb in Egypt, and the Lamb of God: which cards does John 6 need?")],
         "card": "", "note": "Corpus Christi is kept in Canada on Sunday 30 May 2027."},
    37: {"unit": "the-spiral", "title": "Luke 24 again, and the envelope",
         "A": [("Luke 24, whole, as in week one", "bible")],
         "B": [("The envelope", "Read Genesis 1 and Genesis 22 again, twenty minutes each. Then open the three sentences sealed in September and read them beside three new ones."),
               ("Ask", "Luke 24 is a different chapter now. Don’t explain that. Ask.")],
         "card": "", "note": "The same texts, and the child is not the same reader."},
    38: {"unit": "the-spiral", "title": "Name what’s coming",
         "A": [],
         "B": [("Name what’s coming", "Tell the child plainly what was left out and that it was deliberate (see the list on the year’s page).")],
         "card": "", "note": "A spiral admits incompleteness and delivers appetite."},
}

DEFERRED = [
    ("The David saga", "1 Samuel through 1 Kings 2, with Robert Alter: the anointed king who suffers, betrayed by his own, going up the Mount of Olives weeping and barefoot."),
    ("Paul", "Romans whole, Galatians, 1 Corinthians. The child has had Romans 6 and 8 and 1 Corinthians 10 and 11 as fragments."),
    ("Sinai and the covenant", "Exodus 19–24 and Deuteronomy. This year has the sea but not the mountain."),
    ("The prophets and the exile", "Jeremiah, Amos, Hosea, the fall of Jerusalem."),
    ("Wisdom literature", "Job, Proverbs, Ecclesiastes."),
    ("The Psalms as a book", "and lectio divina properly, once the child has some by heart."),
    ("John’s Gospel", "deliberately held back: it rewards a reader who already has the types."),
    ("Revelation", "last, and it wants all of the above."),
]

# ---------------------------------------------------------------------------------------------------

BY_UNIT = {u["slug"]: u for u in UNITS}
SEASON_NAME = {s: (n, d) for s, n, d in SEASONS}
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def monday(n):
    return FIRST_MONDAY + datetime.timedelta(days=7 * (n - 1) + (14 if n > CHRISTMAS_AFTER else 0))


def dates(n):
    a, b = monday(n), monday(n) + datetime.timedelta(days=4)
    if a.month == b.month:
        return f"{a.day}–{b.day} {MONTHS[a.month - 1]} {a.year}"
    return f"{a.day} {MONTHS[a.month - 1]} – {b.day} {MONTHS[b.month - 1]} {b.year}"


def check():
    """Refuse a gap in the weeks, an unknown unit or book, or a unit whose weeks are not its own."""
    ns = sorted(WEEKS)
    if ns != list(range(1, len(ns) + 1)):
        raise SystemExit("pascha: weeks must be numbered 1, 2, 3 ... without a gap")
    for n, w in WEEKS.items():
        if w["unit"] not in BY_UNIT:
            raise SystemExit(f"pascha: week {n} names unknown unit {w['unit']!r}")
        if n not in BY_UNIT[w["unit"]]["weeks"]:
            raise SystemExit(f"pascha: week {n} is not among the weeks of {w['unit']}")
        for _, b in w["A"]:
            if b and b not in BOOKS:
                raise SystemExit(f"pascha: week {n} uses unknown book {b!r}")
        if monday(n).weekday() != 0:
            raise SystemExit(f"pascha: week {n} does not start on a Monday")
    for u in UNITS:
        if u["season"] not in SEASON_NAME:
            raise SystemExit(f"pascha: {u['slug']} has unknown season {u['season']!r}")
        for n in u["weeks"]:
            if WEEKS.get(n, {}).get("unit") != u["slug"]:
                raise SystemExit(f"pascha: {u['slug']} lists week {n}, which is not its own")


def unit_path(u):
    return f"{INDEX}{u['slug']}/"


def week_path(n):
    return f"{INDEX}week-{n}/"


def unit_label(u):
    return f"Unit {u['n']} · {u['title']}" if u["n"] else u["title"]


def week_books(n):
    seen = []
    for _, b in WEEKS[n]["A"]:
        if b and b not in seen:
            seen.append(b)
    return seen


def book_weeks(key):
    return [n for n in sorted(WEEKS) if key in week_books(n)]


def _read_list(n):
    w = WEEKS[n]
    if not w["A"]:
        return "<p>No reading this week.</p>"
    items = "".join(f"<li>{t}</li>" for t, _ in w["A"])
    return f"<ol>{items}</ol>"


def _b_list(n):
    return "".join(f"<p><strong>{esc(label)}.</strong> {text}</p>" for label, text in WEEKS[n]["B"])


def _crumbs(u=None):
    out = f'<p class="crumbs"><a href="/curriculum/">The Benedict Year</a> › <a href="{INDEX}">Reading Backwards from the Pascha</a>'
    if u:
        out += f' › <a href="{unit_path(u)}">{esc(unit_label(u))}</a>'
    return out + "</p>"


def _nav(prev_html, next_html, extra=""):
    return f"""
<section class="section map-nav-band">
  <div class="wrap narrow">
    <nav class="map-nav" aria-label="In the year">
      <p class="eyebrow">In the year</p>
      {prev_html}
      {next_html}
      {extra}
      <p class="more"><a href="{INDEX}">The whole year →</a> · <a href="{INDEX}books/">The books →</a></p>
    </nav>
  </div>
</section>
"""


def week_page(n):
    w = WEEKS[n]
    u = BY_UNIT[w["unit"]]
    season, _ = SEASON_NAME[u["season"]]
    books = week_books(n)
    book_html = ""
    if books:
        book_html = "<h2>Books this week</h2><ul>" + "".join(
            f'<li><a href="{INDEX}books/#{b}">{esc(_book_name(b))}</a></li>' for b in books) + "</ul>"
    card = f"<h2>The Tile Board</h2><p>Add a card: <strong>{w['card']}</strong>, with the passage and today’s date. Pencil a line to another card only if the child sees one.</p>" if w["card"] else ""
    note = f'<p class="note">{w["note"]}</p>' if w["note"] else ""
    body = f"""<section class="page-head">
  <div class="wrap narrow">
    {_crumbs(u)}
    <p class="eyebrow">Week {n} · {dates(n)} · {esc(season)}</p>
    <h1>{esc(w['title'])}</h1>
    <p class="lead">{esc(unit_label(u))}: {u['lead']}</p>
  </div>
</section>

<section class="section">
  <div class="wrap narrow">
    <div class="prose">
      <h2>Session A · the reading</h2>
      <p>About 55 minutes. Open and read aloud before any framing: no introduction, no “today we’re looking at”. Scripture first, then the Father.</p>
      {_read_list(n)}
      <h2>Session B · the argument</h2>
      <p>About 35 minutes, on another day. Never both in one sitting.</p>
      {_b_list(n)}
      {card}
      {book_html}
      {note}
    </div>
  </div>
</section>
"""
    prev_html = f'<p><span class="map-nav-label">Week before</span> <a href="{week_path(n - 1)}">Week {n - 1} · {esc(WEEKS[n - 1]["title"])}</a></p>' if n > 1 else ""
    next_html = f'<p><span class="map-nav-label">Week after</span> <a href="{week_path(n + 1)}">Week {n + 1} · {esc(WEEKS[n + 1]["title"])}</a></p>' if n + 1 in WEEKS else ""
    body += _nav(prev_html, next_html, f'<p><span class="map-nav-label">The unit</span> <a href="{unit_path(u)}">{esc(unit_label(u))}</a></p>')
    meta = {"title": f"Week {n}: {w['title']} · Reading Backwards from the Pascha",
            "crumb": f"Week {n}",
            "description": f"Week {n} ({dates(n)}) of Reading Backwards from the Pascha, a year of Scripture read from the Easter Vigil: {unit_label(u)}. What to read aloud, what to argue, and the card for the Tile Board.",
            "path": week_path(n), "nav": "essays", "kind": "pascha-week",
            "summary": f"{dates(n)}. {unit_label(u)}."}
    return meta, body


def _book_name(b):
    x = BOOKS[b]
    return f"{x['author']}, {x['title']}" if x.get("author") else x["title"]


def unit_page(i):
    u = UNITS[i]
    season, span = SEASON_NAME[u["season"]]
    first, last = u["weeks"][0], u["weeks"][-1]
    span_txt = f"Week {first}" if first == last else f"Weeks {first}–{last}"
    rows = "".join(
        f'<tr><td data-label="Week"><a href="{week_path(n)}">Week {n}</a></td><td data-label="Dates">{dates(n)}</td>'
        f'<td data-label="Read aloud">{esc(WEEKS[n]["title"])}: {"; ".join(t for t, _ in WEEKS[n]["A"]) or "the liturgy"}</td></tr>'
        for n in u["weeks"])
    vigil = '<p class="essay-meta">A reading of the Easter Vigil</p>' if u.get("vigil") else ""
    whatfor = f"<h2>What is it for?</h2><p>{u['whatfor']}</p>" if u["whatfor"] else ""
    unans = f"<h2>Unanswerable</h2><p>{u['unanswerable']}</p>" if u["unanswerable"] else ""
    books = []
    for n in u["weeks"]:
        for b in week_books(n):
            if b not in books:
                books.append(b)
    book_html = ("<h2>Books for this unit</h2><ul>" + "".join(
        f'<li><a href="{INDEX}books/#{b}">{esc(_book_name(b))}</a></li>' for b in books) + "</ul>") if books else ""
    body = f"""<section class="page-head">
  <div class="wrap narrow">
    {_crumbs()}
    <p class="eyebrow">{esc(season)} · {span_txt}</p>
    <h1>{esc(u['title'])}</h1>
    <p class="lead">{u['lead']}</p>
    <p class="essay-meta">The text at the centre: {esc(u['spine'])}</p>
    {vigil}
  </div>
</section>

<section class="section">
  <div class="wrap narrow">
    <div class="prose">
      <h2>Why it is here</h2>
      <p>{u['why']}</p>
      {whatfor}
      {unans}
      <h2>The weeks</h2>
      <table class="deadlines curriculum-table">
        <thead><tr><th>Week</th><th>Dates</th><th>Read aloud</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
      {book_html}
    </div>
  </div>
</section>
"""
    prev_u = UNITS[i - 1] if i > 0 else None
    next_u = UNITS[i + 1] if i + 1 < len(UNITS) else None
    prev_html = f'<p><span class="map-nav-label">Before it</span> <a href="{unit_path(prev_u)}">{esc(unit_label(prev_u))}</a></p>' if prev_u else ""
    next_html = f'<p><span class="map-nav-label">After it</span> <a href="{unit_path(next_u)}">{esc(unit_label(next_u))}</a></p>' if next_u else ""
    body += _nav(prev_html, next_html)
    meta = {"title": f"{u['title']} · Reading Backwards from the Pascha",
            "crumb": u["title"],
            "description": f"{unit_label(u)} of Reading Backwards from the Pascha, a year of Scripture read from the Easter Vigil. {html.unescape(_strip(u['lead']))}",
            "path": unit_path(u), "nav": "essays", "kind": "pascha-unit", "summary": _strip(u["lead"])}
    return meta, body


def _strip(s):
    import re
    return re.sub(r"<[^>]+>", "", s)


def books_page():
    groups = []
    for g in dict.fromkeys(b["group"] for b in BOOKS.values()):
        items = []
        for key, b in BOOKS.items():
            if b["group"] != g:
                continue
            name = f"{esc(b['author'])}, <em>{esc(b['title'])}</em>" if b.get("author") else f"<em>{esc(b['title'])}</em>"
            if b.get("free"):
                name = f'<a href="{b["free"]}">{name}</a>'
            detail = f". {b['detail']}" if b.get("detail") else ""
            note = f" {b['note']}" if b.get("note") else ""
            ws = book_weeks(key)
            used = ""
            if ws and key != "bible":
                used = '<br><span class="field-also">Read in ' + ", ".join(f'<a href="{week_path(n)}">week {n}</a>' for n in ws) + "</span>"
            elif key == "bible":
                used = '<br><span class="field-also">Every week</span>'
            items.append(f'<li id="{key}">{name}{detail}.{note}{used}</li>')
        groups.append(f"<h2>{esc(g)}</h2><ul>{''.join(items)}</ul>")
    body = f"""<section class="page-head">
  <div class="wrap narrow">
    {_crumbs()}
    <p class="eyebrow">The books</p>
    <h1>What to buy, and what is free</h1>
    <p class="lead">A Catholic Bible, five cheap paperbacks, two more in print, and the rest free online. Each book lists the weeks that read from it.</p>
  </div>
</section>

<section class="section">
  <div class="wrap narrow">
    <div class="prose">
      {''.join(groups)}
    </div>
  </div>
</section>
"""
    body += _nav("", "")
    meta = {"title": "The books · Reading Backwards from the Pascha", "crumb": "The books",
            "description": "The books for Reading Backwards from the Pascha, a year of Scripture read from the Easter Vigil: a Catholic Bible, the Popular Patristics paperbacks, and the free texts, each with the weeks that use it.",
            "path": f"{INDEX}books/", "nav": "essays", "kind": "pascha-books",
            "summary": "A Catholic Bible, the Popular Patristics paperbacks, and the free texts, with the weeks that read them."}
    return meta, body


def year_section():
    """The year on the index: season by season, each unit with its weeks."""
    out = []
    for s, name, span in SEASONS:
        units = [u for u in UNITS if u["season"] == s]
        cards = []
        for u in units:
            first, last = u["weeks"][0], u["weeks"][-1]
            wk = f"week {first}" if first == last else f"weeks {first}–{last}"
            weeks = " · ".join(f'<a href="{week_path(n)}">{n}</a>' for n in u["weeks"])
            cards.append(f"""      <li>
        <p class="reg">{esc(unit_label(u).split(' · ')[0]) if u['n'] else esc(name)} · {wk}</p>
        <h2><a href="{unit_path(u)}">{esc(u['title'])}</a></h2>
        <p>{u['lead']}</p>
        <p class="field-also">{esc(u['spine'])} · weeks {weeks}</p>
      </li>""")
        out.append(f"""    <h2 class="off-map-head">{esc(name)} <span class="reg-inline">{esc(span)}</span></h2>
    <ul class="essay-list">
{chr(10).join(cards)}
    </ul>""")
    return "\n".join(out)


def calendar_section():
    rows = "".join(
        f'<tr><td data-label="Week"><a href="{week_path(n)}">{n}</a></td><td data-label="Dates">{dates(n)}</td>'
        f'<td data-label="Unit"><a href="{unit_path(BY_UNIT[WEEKS[n]["unit"]])}">{esc(BY_UNIT[WEEKS[n]["unit"]]["title"])}</a>: {esc(WEEKS[n]["title"])}</td></tr>'
        for n in sorted(WEEKS))
    return f"""<table class="deadlines curriculum-table">
        <thead><tr><th>Week</th><th>Dates</th><th>Unit and week</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>"""


def deferred_section():
    return "<ul>" + "".join(f"<li><strong>{esc(a)}</strong>: {esc(b)}</li>" for a, b in DEFERRED) + "</ul>"


def pages():
    check()
    out = [unit_page(i) for i in range(len(UNITS))]
    out += [week_page(n) for n in sorted(WEEKS)]
    out.append(books_page())
    return out
