"""Book 1 (Grades 1-9) — Arabic term configuration.

Curated, NOT a translation of book1_en.py: the English config's STOP/DROP
lists key on English words that do not exist here, and Arabic raises traps of
its own. Seeded by the orchestrator with the parts that are language-wide;
the book agent owns everything below and should grow it while translating.

Arabic traps to expect (see arabic_style_card.md §4):

  * Proclitics. The article ال and the one-letter particles و ف ب ك ل attach
    to the front of the word, and inside a noun phrase every word carries
    them. tools/term_config/lang_ar.py handles that in HEAD; the cost is that
    a short term can now match with a leading particle it never meant, so
    watch for wrong-sense links and hand-DROP them.
  * Broken plurals. Arabic pluralises by internal vowel change (دالة/دوال،
    حد/حدود), which no suffix rule reaches. lang_ar.py sets WORD_TAIL = ''
    and DERIVE = False on purpose, so every plural a chapter actually uses
    must be declared here, in DERIVED or EXTRA, term by term.
  * NO_CAPITAL is structurally inert: Arabic has no letter case, so nothing
    keys on it. Where the English config used it to separate a unit from the
    physicist it is named after, use EXTRA_PROTECT instead.

Regenerate after editing:
    python3 tools/link_defined_terms.py --book 1 --lang ar --unwrap --apply
    python3 tools/link_defined_terms.py --book 1 --lang ar --apply
"""

# Result-names: words that head a STATEMENT, never a defined term. The
# defaults in link_defined_terms.py are English, so without this list every
# "مبرهنة فيثاغورس" would try to become a term.
NOT_A_TERM = ("مبرهنة", "قضية", "نتيجة", "متراجحة", "صيغة", "معيار",
              "مبدأ", "متطابقة", "قانون", "قاعدة", "مفارقة", "مسألة",
              "خاصية", "علاقة")

# ---------------------------------------------------------------------------
# STOP -- ordinary language in this book; a stoplisted word still links inside
# the chapter that DEFINES it (that is what SOFT below keeps), so the list is
# read together with DROP.
#
# The five pieces of geometric furniture are the Arabic counterpart of the
# English config's square/triangle/rectangle/circle/angle decision: they are
# genuine definitions, but by grade 5 they are the furniture of every
# geometry sentence (مستطيل 37 hits, مربع 31, مثلث 27, دائرة 19 before this
# list), and linking each one turns whole exercise sections blue. The
# compounds a pupil can really forget keep their links: زاوية قائمة،
# مثلث قائم، محور تماثل، نصف قطر.
# ---------------------------------------------------------------------------
STOP = {
    # geometric furniture
    "مربع", "مثلث", "مستطيل", "دائرة", "زاوية",
    # ordinary words that happen to be defined terms
    "نصف",      # "نصف ساعة", "نصف الطريق" -- the fraction sense is a minority
    "ربع",      # same, plus "ربع ساعة"
    "وجه",      # "وجه المجسّم" vs "وجها القسمة", "الوجه الآخر"
    "رأس",      # vertex vs "رأس الساعة", "على رأس"
    "حرف",      # edge of a solid vs "حرف الكوس", "حرف اللام"
    "صندوق",    # the solid vs the everyday box of every word problem
    "كرة",      # the sphere vs the marbles of grades 1-3
    "عشرة",     # the bundle of ten vs the numeral in every other sentence
    "وحدة",     # the unit place vs "وحدة القياس", "وحدة نقدية"
    "قاسم",     # divisor vs the verb form
    "تصميم",    # net of a solid vs "تصميم" in the ordinary sense
    "فئات",     # the classes of three digits vs "فئة نقدية" (banknotes)
    "متوسط",    # the triangle median (pb:g8:midpoints:1) vs the everyday
                # "average" of grades 8-9: one string, two senses, and the
                # average sense is the common one outside its own chapter
    # the unit, not the notion: English does not link "centimetre" either, and
    # linking it made every measurement exercise of grades 1-5 blue.
    "سنتيمتر", "بالسنتيمتر", "سنتيمترات",
}
# The harvest registers both the \emph display (usually definite, المربع) and
# the \index key (indefinite, مربع) as separate terms, so every word above is
# repeated here with its article. Arabic's HEAD pattern cannot merge the two:
# ال is part of the string when the display itself carries it.
STOP |= {"ال" + w for w in STOP}

# STOP is deliberately *soft*: a stoplisted word is still linked inside the
# chapter that defines it. These are the words for which that is exactly
# right -- inside their own chapter every occurrence really is the term.
SOFT = {
    "وجه", "حرف", "رأس",   # parts/grade-5/07, all uses are the solid's
    "فئات",                # parts/grade-4/01, all uses are the digit groups
    "تصميم",               # parts/grade-5/07, all uses are the net
    "متوسط",              # parts/grade-8/06, all uses are the triangle median
}
SOFT |= {"ال" + w for w in SOFT}

# DROP is the hard version: never a link anywhere.
DROP = (set(STOP) - SOFT) | {
    # \emph{قيمة الرقم تتوقف على مرتبته}\index{قيمة مكانية} in
    # parts/grade-6/01: the sentence is not a term (the term is القيمة المكانية).
    "قيمة الرقم تتوقف على مرتبته",
}

# ---------------------------------------------------------------------------
# EXTRA -- manual term -> label, for what the harvest cannot reach.
# ---------------------------------------------------------------------------
EXTRA = {
    # "السلّم" is harvested from the grade-6 weekend problem, but the term is
    # defined in grade 7 (as in English): point it there, and the grade-6 uses
    # fall away by themselves (a link never precedes its definition).
    "السلّم": "def:g7:prop:scale",
    # remainder: the display "الباقي" sits inside the grade-6 Euclidean-division
    # theorem, but the notion is the grade-3 one English links to.
    "الباقي": "def:g3:division:remainder",
    "باقي": "def:g3:division:remainder",
    # difference / quotient: the Arabic grade-6 vocabulary example re-displays
    # both, but English links them to their first appearance.
    "فرق": "ex:g1:subtraction:difference",
    "خارج قسمة": "def:g3:division:remainder",
    # the active participle of "parallel": the harvest only reaches the dual
    # متوازيان, which is ambiguous (grade 4 and grade 6) and so never linked.
    "الموازي": "def:g6:lines:perp",
    "الموازيان": "def:g6:lines:perp",
    "الموازيَين": "def:g6:lines:perp",
    "موازٍ": "def:g6:lines:perp",
    "موازيًا": "def:g6:lines:perp",
}

# ---------------------------------------------------------------------------
# EXTRA_PROTECT -- regexes for a fixed phrase in which a defined word carries
# another sense. Arabic needs these for the proclitic clusters that HEAD
# happily swallows.
# ---------------------------------------------------------------------------
EXTRA_PROTECT = (
    r"في المجموع",        # "in all", not the arithmetic sum
    r"المجموع الكلي",
    r"نصف ساعة", r"ربع ساعة", r"نصف الطريق",
    r"الورق المربّعات",   # grid paper, not the square
    r"المجموع الكلي للحدّ",
    r"مجموع أرقام",       # digit sum: a different notion, defined in grade 5
    r"مجموع الأرقام",
    r"الفرق بين الوقتين",
    # a ladder and a scale are the same word in Arabic (سلّم): grade-9's
    # trigonometry chapter leans a ladder against a wall, not a map scale.
    r"سلّم\s+طوله", r"بين\s+السلّم\s+والأرض", r"مسألة\s+السلّم",
    r"سلّم،\s+لا\s+درج",
    # "الباقي" as ordinary language ("the rest"), not the division remainder
    r"الباقي\s+\$?\\frac", r"الباقي\s+إلى\s+قسمين", r"الباقي؛\s+واُرسم",
)

# ---------------------------------------------------------------------------
# DERIVED -- Arabic pluralises by internal vowel change, and lang_ar.py sets
# WORD_TAIL = '' and DERIVE = False on purpose, so every plural the book
# actually uses is declared here, term by term.
# ---------------------------------------------------------------------------
DERIVED = {
    "مضاعف": ["مضاعفات"],
    "قاسم": ["قواسم"],
    "كسر": ["كسور"],
    "جداء": ["جداءات"],
    "مضلع": ["مضلعات"],
    "مكعب": ["مكعبات"],
    "أسطوانة": ["أسطوانات"],
    "هرم": ["أهرام"],
    "مجسم": ["مجسّم", "مجسّمات", "مجسمات"],
    "محور تماثل": ["محاور تماثل", "محاور التماثل"],
    "نصف قطر": ["أنصاف أقطار"],
    "زاوية قائمة": ["زوايا قائمة"],
    "عدد زوجي": ["أعداد زوجية", "الأعداد الزوجية"],
    "عدد فردي": ["أعداد فردية", "الأعداد الفردية"],
    "عدد عشري": ["أعداد عشرية", "الأعداد العشرية"],
    "أعداد مثلثية": ["الأعداد المثلثية"],
    "خارج القسمة": ["خوارج القسمة"],
    # grades 6-9: broken plurals and the bound forms the chapters really use
    "الأُسّ": ["الأُسُس", "أُسُس", "أُسّ", "أُسًّا", "أُسّه", "أُسّيه",
              "الأُسّان", "أُسّان"],
    "العدد الأولي": ["الأعداد الأولية", "أعداد أولية"],
    "المعادلة": ["المعادلات", "معادلات", "معادلتان", "معادلتين", "معادلاتها"],
    "الجذر التربيعي": ["الجذور التربيعية", "جذور تربيعية"],
    "الدالة الخطية": ["الدوال الخطية", "دوال خطية", "دالّتان خطيّتان"],
    "الدالة التآلفية": ["الدوال التآلفية", "دوال تآلفية"],
    "المخروط": ["المخاريط", "مخاريط", "مخروطين", "مخروطان"],
    "الموشور": ["المواشير", "مواشير"],
    "القطعة": ["القطع", "قطعتان", "قطعتين"],
    "المستقيم": ["المستقيمات", "مستقيمات", "مستقيمان", "مستقيمين"],
    "المتوسّط": ["المتوسّطات", "متوسّط", "متوسّطها", "بمتوسّطها"],
    "وسيط": ["الوسيط", "الوسطاء", "وسيطها", "ووسيطها"],
    "مدى": ["المدى", "مداها"],
    "قابل للقسمة": ["قابلة للقسمة", "قابلًا للقسمة", "قابلان للقسمة",
                    "قابلية القسمة", "قابليّة القسمة"],
    "متوسط مرجح": ["المتوسط المرجّح", "متوسط مرجّح", "المتوسّط المرجّح"],
    "احتمال": ["اِحتمال", "الاِحتمال", "الاحتمال", "اِحتمالات",
               "الاِحتمالات", "اِحتمالًا", "اِحتماله"],
}

PRIMARY_OK = set()
NO_CAPITAL = set()    # inert in a caseless script; use EXTRA_PROTECT instead

AMBIG_POLICY = "nearest-preceding"
MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 40
