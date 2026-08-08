"""Book 3 (University Year 1) — Arabic term configuration.

Curated, NOT a translation of book3_en.py: the English config's STOP/DROP
lists key on English words that do not exist here, and Arabic raises traps of
its own. Where an English decision transfers (a word whose sense moves from
chapter to chapter is usually overloaded in both languages) the Arabic entry
carries the English word in its comment, so the two configs can be compared.

Arabic traps to expect (see arabic_style_card.md §4):

  * Proclitics. The article ال and the one-letter particles و ف ب ك ل attach
    to the front of the word, and inside a noun phrase every word carries
    them. tools/term_config/lang_ar.py handles that in HEAD; the cost is that
    a short term can now match with a leading particle it never meant, so
    watch for wrong-sense links and hand-DROP them. Because a harvested term
    may be definite or indefinite, STOP and DROP are closed below under
    prefixing ال — list a word once, bare, and both forms are covered.
  * Broken plurals. Arabic pluralises by internal vowel change (دالة/دوال،
    حد/حدود), which no suffix rule reaches. lang_ar.py sets WORD_TAIL = ''
    and DERIVE = False on purpose, so every plural a chapter actually uses
    must be declared here, in DERIVED or EXTRA, term by term.
  * NO_CAPITAL is structurally inert: Arabic has no letter case, so nothing
    keys on it. Where the English config used it to separate a unit from the
    physicist it is named after, use EXTRA_PROTECT instead.

Regenerate after editing:
    python3 tools/link_defined_terms.py --book 3 --lang ar --unwrap --apply
    python3 tools/link_defined_terms.py --book 3 --lang ar --apply
"""

# Result-names: words that head a STATEMENT, never a defined term. The
# defaults in link_defined_terms.py are English, so without this list every
# "مبرهنة فيثاغورس" would try to become a term.
NOT_A_TERM = ("مبرهنة", "قضية", "نتيجة", "متراجحة", "صيغة", "معيار",
              "مبدأ", "متطابقة", "قانون", "قاعدة", "مفارقة", "مسألة",
              "خاصية", "علاقة")

# Words whose sense is only safe inside the chapter that pins them down.
# STOP is soft: the term still links where it is introduced.
STOP = {
    "منتهية",          # EN "finite": "مجموع/عائلة/اتحاد منته" and above all
                       # "التزايدات المنتهية" (the MVT) are not the finite SET
                       # of ch. 2. "مجموعة منتهية" keeps the link.
    "مرافق",           # EN "conjugate": complex conjugate (ch. 3) vs "اضرب في
                       # المرافق" (ch. 11) vs conjugating a matrix (ch. 21)
    "كثير الحدود المميز",    # EN "characteristic polynomial": ch. 5 defines it
    "كثير حدودها المميِّز",  # for a linear ODE, ch. 22 for a matrix
    "صورة",            # image of a linear map (ch. 20) vs the ordinary "في
                       # صورة" = "in the form of", "أبسط صورة" = lowest terms,
                       # "صورة" = picture; ~70 uses each way
    "أثر",             # trace of a matrix (ch. 21) vs "الأثر" = the effect,
                       # "بأثر رجعي", "لا أثر هناك"
    "الجزء الصحيح",    # floor (ch. 10) vs the polynomial part of a rational
                       # fraction (ch. 9), which is a different object
    "تجزئة",           # partition of a set (ch. 1) vs the subdivision talk of
                       # ch. 15; "بالتجزئة" is protected below
}
STOP |= {"ال" + w for w in STOP}

# Never linked anywhere.
DROP = {
    # ---- ordinary Arabic in this register (the EN counterpart is dropped
    # for the same reason)
    "طول",             # EN "length": "طول ضلع", "طول المجال", everywhere —
                       # "طول القوس" (arc length) keeps the link
    "داخل",            # interior of a set vs the preposition "داخل $A$" =
                       # inside $A$; the two are indistinguishable in print.
                       # "الغلق" and "حافة" still reach the same definition.
    "تماثل",           # EN "symmetry": "بالتماثل" = by symmetry, not the
                       # linear-map symmetry of ch. 20 ("إسقاط" keeps it)
    "مباشرًا",         # EN "direct": "حسابًا مباشرًا"; "مجموع مباشر" survives
    "حرجة",            # EN "critical": bare adjective; "نقطة حرجة" survives
    "جبريّ", "جبري",   # EN "algebraic": "تلاعب جبري", "بنية جبرية"
    "متسامٍ",          # EN "transcendental": bare adjective; "عدد متسامٍ" and
                       # "عدد متسام" survive
    "متكافئتان",       # "العبارتان متكافئتان" = the two statements are
                       # equivalent, on nearly every page; "مصفوفات متكافئة"
                       # and "متشابهتان" keep the matrix notions

    # ---- names of results: the point is to link definitions, not theorems.
    # NOT_A_TERM only filters the index-only harvest; these arrived through
    # \emph{...}\index{...} and have to be dropped by hand. Mirrors the EN
    # list (Kummer, Legendre, Ptolemy, Cauchy's functional equation,
    # alternating series estimate).
    "صيغ فييت",                 # plural صيغ escapes NOT_A_TERM
    "مبرهنة كومر",
    "صيغة لوجاندر",
    "متراجحة بطليموس",
    "معادلة كوشي الدالية",
    "معادلة دالية",
    "تقدير المتسلسلة المتناوبة",

    # ---- mis-target: \index{عدد أصمّ} sits inside the ch. 19 weekend problem
    # (Dedekind's tower law), so the harvest pins "irrational number" to a
    # statement about field degrees. English links nothing here either.
    "عدد أصمّ", "عدد أصم",
}
DROP |= {"ال" + w for w in DROP}

# Terms the harvest cannot reach.
EXTRA = {
    # the definition emphasises the compound ("\emph{متصلة عند $x_0 \in I$}",
    # "\emph{قابلة للاشتقاق على $I$}"), so the bare adjective — the form the
    # rest of the book actually uses, ~100 times — is never harvested
    "متصلة":            "def:b1:continuity:continuous",
    "قابلة للاشتقاق":   "def:b1:derivative:def",
    # \index{ثابت أويلر} sits in an exercise BEFORE the weekend problem that
    # defines gamma, so the nearest preceding statement is an unrelated
    # telescoping example. Point it at the problem (as book3_en.py does).
    "ثابت أويلر":       "pb:b1:series:1",
    # NOT_A_TERM ("خاصية", "قانون") filters these out of the index-only
    # harvest, but they name definitions the book uses by name afterwards —
    # English links both.
    "خاصية أرخميدس":    "thm:b1:reals:archimedes",
    "قانون البرج":      "pb:b1:findim:1",
    # "coprime" is a three-word phrase in Arabic that inflects for the dual
    # and the plural; the harvest only saw one of the forms the book uses.
    "أولية فيما بينها":     "cor:b1:arith:bezout",
    "أوليّان فيما بينهما":  "cor:b1:arith:bezout",
    "أوليّين فيما بينهما":  "cor:b1:arith:bezout",
}

# Fixed Arabic phrases that contain a linkable word in another sense.
# NB: never consume a `$` (see tools/termlink/protect.py) — the base-of-a
# -numeral-system rule below matches the opening $ with a lookahead.
EXTRA_PROTECT = (
    # HEAD lets ب attach to a term, which makes the topological جوار collide
    # with the ordinary preposition "بجوار / في جوار" = "near" (same trap as
    # book5_ar.py)
    r'بجوار',
    r'في\s+جوار',
    # "الأساس $b$ / $2$ / $10$ / $p$" is the base of a numeral system (ch. 6,
    # 10, 17), not a basis. A basis is always written with a tuple —
    # "الأساس $(e_1, \dots, e_n)$" — so protect only a scalar-looking formula.
    r'(?:ال)?أساس\s+(?=\$(?![(\\]))',
    # EN protects "closed form" for exactly this
    r'صور(?:ة|ةً)\s+مغلقة',
    r'في\s+صورة',
    # "بالتجزئة" (= by parts) is NOT protected: "مكاملة بالتجزئة" is a term of
    # its own and longest-first makes it beat the bare "تجزئة", while STOP
    # keeps the partition sense inside ch. 1, where integration never appears.
    # "عبارةٌ عن" = "is nothing but", not the logical statement of ch. 1
    r'عبارةٌ?\s+عن',
)

DERIVED = {}          # the plurals this book uses are harvested as their own
                      # \index entries (كثيرات حدود تشيبيشيف، دوال زائدية،
                      # مجاميع ريمان، فروق مقسومة، أقطاب), so nothing has to be
                      # declared by hand.

PRIMARY_OK = set()    # as in book3_en.py: نواة / رتبة / ترتيب are each defined
                      # twice and no first sense dominates — AMBIG_POLICY drops
                      # them rather than guessing.

NO_CAPITAL = set()    # inert in a caseless script; use EXTRA_PROTECT instead

AMBIG_POLICY = "drop"
MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 40
