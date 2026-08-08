"""Book 5 (University Year 3) — Arabic term configuration.

Curated, NOT a translation of book5_en.py: the English config's STOP/DROP
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
    python3 tools/link_defined_terms.py --book 5 --lang ar --unwrap --apply
    python3 tools/link_defined_terms.py --book 5 --lang ar --apply
"""

# Result-names: words that head a STATEMENT, never a defined term. The
# defaults in link_defined_terms.py are English, so without this list every
# "مبرهنة فيثاغورس" would try to become a term.
# "محك" (criterion) heads a statement; "معيار" is the *norm* and is a
# defined term (\index{معيار مؤثر}), so it must NOT be listed here.
NOT_A_TERM = ("مبرهنة", "قضية", "نتيجة", "متراجحة", "صيغة", "محك",
              "مبدأ", "متطابقة", "قانون", "قاعدة", "مفارقة", "مسألة",
              "خاصية", "علاقة")

STOP = {
    # ---- ordinary Arabic, or a sense that changes from chapter to chapter.
    # STOP still links the word inside the chapter that defines it, so nothing
    # is lost where the term is actually being introduced. The list mirrors
    # book5_en.py's decisions (simple, dense, normal, maximal, radical,
    # content, action, basis, degree, free, Euclidean, separable, closed,
    # exact, prime, path, boundary, interior, a.e.) plus the traps that are
    # Arabic-only.
    "بسيطة",            # simple group / simple pole / simple function
    "كثيفة",            # dense set / "كثيفة" as plain "thick, abundant"
    "ناظمية",           # normal subgroup / Smith normal form / normal family
    "أعظميًا",          # maximal ideal / "أعظمي" = greatest, everywhere
    "جذريًّا",          # radical extension / "جذريًّا" = radically
    "محتوى",            # content of a polynomial / "محتوى" = contents
    "فعل",              # group action / "فعل" = act, verb
    "حرًّا",            # free module / "حرًّا" = freely
    "إقليدية",          # Euclidean ring / Euclidean norm, distance, geometry
    "قابلًا للفصل",     # separable polynomial / separable Hilbert space
    "مغلقة",            # closed form (ch. 21) vs closed set (ch. 6 onwards)
    "تامة",             # exact form (ch. 21) vs complete/whole, constantly
    "تامًّا",           # complete metric space vs the adverb "completely"
    "أولي",             # prime element / "أولي" = initial, primary
    "أوليًا",
    "مسار",             # path in a topological space / contour, trajectory
    "الحافة",           # boundary of a manifold / edge, border, generally
    "الداخل",           # interior of a set / "الداخل" = the inside, within
    "الأساس",           # basis of a topology / basis of a space, base of a
                        # numeral system, "الأساس" = the foundation
    "الدرجة",           # degree of a field extension / degree of a polynomial,
                        # of a matrix, of a differential equation -- the single
                        # worst offender in this book
    "كاملة",            # perfect field (ch. 4) / "كاملة" = complete, entire
    "مركز",             # centre of a group / centre of a circle, of a disc
    "طابع",             # character of a representation / "طابع" = stamp,
                        # timbre, quality
    "مدار",             # orbit of a group action / orbit of a flow (ch. 19)
    "متكاملة",          # comaximal ideals / "متكاملة" = complementary, whole
    "الباقي",           # residue at a pole / "الباقي" = the rest, the remainder
    "الدليل",           # index of a path / "الدليل" = subscript, index set
    "غاوسية",           # Gaussian vector (ch. 23) / the Gaussian function,
                        # everywhere from ch. 11 on
    "التواء",           # torsion of a module / skewness of a law (ch. 23)
    "الالتوائي",
    "في كل مكان تقريبًا",   # "a.e." -- book5_en.py stops it for the same reason
    "في كل مكان تقريبا",
}

DROP = set()          # never a link anywhere

EXTRA = {}            # term -> label, for what the harvest cannot reach

# Spans no link may touch. Arabic-specific: HEAD lets the one-letter particles
# ب ف ل ك و attach to a term, which is what makes "الجوار / جوار" (a topological
# neighbourhood, ch. 6) collide with the ordinary preposition "بجوار / في جوار"
# = "near", used on nearly every page of the analysis chapters.
EXTRA_PROTECT = (
    r'بجوار',
    r'في\s+جوار',
)

DERIVED = {}          # declared plurals and variants (see the note above): the
                      # plurals this book actually uses are already harvested
                      # as their own \index entries ("دوال أصناف",
                      # "مؤثرات هيلبرت--شميدت", "عوامل صامدة", "قواسم أولية"),
                      # so nothing has to be declared by hand here.

PRIMARY_OK = set()
NO_CAPITAL = set()    # inert in a caseless script; use EXTRA_PROTECT instead

AMBIG_POLICY = "drop"
MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 40
