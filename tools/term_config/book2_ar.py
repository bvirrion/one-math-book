"""Book 2 (Grades 10-12) — Arabic term configuration.

Curated, NOT a translation of book2_en.py: the English config's STOP/DROP
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
    python3 tools/link_defined_terms.py --book 2 --lang ar --unwrap --apply
    python3 tools/link_defined_terms.py --book 2 --lang ar --apply
"""

# Result-names: words that head a STATEMENT, never a defined term. The
# defaults in link_defined_terms.py are English, so without this list every
# "مبرهنة فيثاغورس" would try to become a term.
NOT_A_TERM = ("مبرهنة", "قضية", "نتيجة", "متراجحة", "صيغة", "محك",
              "مبدأ", "متطابقة", "قانون", "قاعدة", "مفارقة", "مسألة",
              "خاصية", "علاقة", "مساواة")

STOP = {
    # ordinary language outside its own chapter; still links where defined.
    "المجموع", "مجموع",          # 'sum' is everyday Arabic (EN never links it)
    # صورة is the mathematical *image* of a function, but it is also the
    # ordinary word for FORM ("على الصورة الجبرية/الأسية/المختزلة"), for the
    # HEADS of a coin, for a FACE card, and -- with the ب proclitic -- for the
    # adverbial "بصورة ساحقة". Sampling every link showed almost none meant
    # the image, so the word is stopped everywhere but its own chapter.
    "صورة", "صور",
}
STOP |= {"ال" + w for w in STOP}   # the harvest sees bare and definite as two terms

DROP = {
    # bare \index{} inside a theorem: English skips it (no space in
    # "memorylessness"), Arabic would harvest it and out-link the twin.
    "انعدام الذاكرة",
}

EXTRA = {
    # Broken plurals and derived forms the suffix-free Arabic rules cannot reach.
    "تبديلات": "def:g12:comb:permutation",   # plural of تبديلة
    "عاملية": "prop:g12:comb:tuples",        # "الصيغة العاملية" = factorial formula
    "متوسط": "def:g10:stats:mean",           # the definition emphasises المتوسط الحسابي
    # Sense-fixing: المحدد always means the 2x2 determinant of grade 11,
    # never the matrix proposition that recomputes it.
    "المحدد": "def:g11:vect:det",
    # Continuity: the definition emphasises the compound ("\emph{متصلة عند
    # $a$}"), so the bare adjective -- the form the rest of grade 12 actually
    # uses, ~45 times -- is never harvested. Same entry, same reason, as
    # book3_ar.py's "متصلة"; it is what keeps the school->university seam
    # clickable in both volumes. Safe here: every متصلة in Books 1-2 is the
    # analytic sense (the graph-theory "connected" of ch. 11 is وصلات/اتصالات).
    "متصلة": "def:g12:limcont:continuity",
}
EXTRA_PROTECT = ()    # regexes for phrases where a defined word means something else
DERIVED = {}          # declared plurals and variants (see the note above)
PRIMARY_OK = set()
NO_CAPITAL = set()    # inert in a caseless script; use EXTRA_PROTECT instead

AMBIG_POLICY = "nearest-preceding"
MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 40
