"""Book 4 (University Year 2) — Arabic term configuration.

Curated, NOT a translation of book4_en.py: the English config's STOP/DROP
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
    python3 tools/link_defined_terms.py --book 4 --lang ar --unwrap --apply
    python3 tools/link_defined_terms.py --book 4 --lang ar --apply
"""

# Result-names: words that head a STATEMENT, never a defined term. The
# defaults in link_defined_terms.py are English, so without this list every
# "مبرهنة فيثاغورس" would try to become a term.
NOT_A_TERM = ("مبرهنة", "قضية", "نتيجة", "متراجحة", "صيغة", "محك",
              "مبدأ", "متطابقة", "قانون", "قاعدة", "مفارقة", "مسألة",
              "خاصية", "علاقة")
# "معيار" is NOT here on purpose: in this book it is the translation of
# "norm" (def:b2:nvs:norm), a genuine defined term; "criterion" is "محك".

STOP = set()          # ordinary language in this book; still links in its own chapter

# Words the harvest picks up from an \emph{} but which Arabic also uses in a
# completely different, far more frequent sense. Each was verified to produce
# wrong-sense links before being listed here; where the true term survives in
# a longer phrase, that phrase is kept (or added to EXTRA).
DROP = {
    # "رتبة" is the order of a group element in ch01, but "من الرتبة الثانية"
    # (order of a derivative / of an expansion) runs through the whole book.
    "رتبة",
    # "دورية" is "cyclic" in ch01 and "periodic" everywhere after ch14.
    "دورية",
    # "دورة" is a cycle of a permutation in ch01, a full turn in ch16/18/19.
    "دورة",
    # "التوافق" is congruence of quadratic forms in ch12, plain "agreement"
    # in ch18.
    "التوافق",
    # "مرافق" is the adjoint u^* in ch12/13, but also the algebraic cofactor
    # (ch15), a subordinate norm (ch15) and a conjugate pair (ch16).
    "مرافق",
    # "جبر" is the algebra structure of ch01, but "الجبر الخطي" (linear
    # algebra) and "جبر سيغما" are what the word almost always means.
    "جبر",
    # "بانتظام" is uniform convergence in ch10, but also "uniformly at
    # random" in ch21-23 and "uniformly continuous" throughout.
    "بانتظام",
    # "يتقارب" is a verb ("converges"), harvested from the improper-integral
    # definition; it fires on every series and sequence in the book.
    "يتقارب",
    # "مغلقة"/"تامة" are the closed/exact differential forms of ch20, but also
    # closed sets and curves, and "strict"/"complete" in ordinary prose.
    "مغلقة",
    "تامة",
    # "محدبة" alone is any convex function; the convex SET keeps its link
    # through EXTRA below.
    "محدبة",
    # "مستقلين" is independence of events in ch21 and linear independence
    # everywhere before it.
    "مستقلين",
    # "متكافئين" is equivalence of norms in ch05 and plain equivalence after.
    "متكافئين",
    # "الإشارة" is the signature of a permutation in ch01 and the sign of a
    # number in most other chapters.
    "الإشارة",
    # "طوله" is the arc length of ch18 but also the length of a run (ch21).
    "طوله",
    # --- Named RESULTS, not notions. book4_en.py DROPs the English originals
    # (Gauss's limit formula, Korovkin's theorem, Hadamard's inequality,
    # Courant--Fischer, Weyl's inequalities, Jacobi's formula, Sturm's
    # theorems, Chernoff bound, concentration inequalities, Gibbs phenomenon,
    # Euler's function, centerpoint, signature); dropped here for target
    # parity with English.
    "بصيغة غاوس الحدّية",
    "مبرهنة كوروفكين",
    "متراجحة هادامار",
    "مبرهنة الأصغرية العظمى عند كوران--فيشر",
    "متراجحات فايل في الاضطراب",
    "صيغة جاكوبي",
    "مبرهنتي شتورم في الفصل والمقارنة",
    "حصر تشيرنوف",
    "متراجحات التركيز",
    "ظاهرة غيبس",
    "دالة أويلر",
    "نقطة المركز",
    "توقيع",
    # The Hessian matrix: English harvests it too but does not link it
    # (book4_en.py stoplists "Hessian matrix"); dropped for target parity.
    "مصفوفة هس",
    # Arabic spells the matrix exponential with and without the shadda, and
    # the two spellings harvested different targets; keep the definition in
    # ch05 (ex:b2:nvs:matrixexp), which is the one English links.
    "الأسي المصفوفي",
}

EXTRA = {
    # rescued from DROP: the convex SET is a genuine defined object.
    "مجموعة محدبة": "def:b2:affine:convex",
    "المجموعات المحدبة": "def:b2:affine:convex",
    # Broken plurals the harvest cannot reach (WORD_TAIL is empty and
    # DERIVE is off in lang_ar.py — see the docstring).
    "حلقات القسمة": "def:b2:structures:quotientring",
    "السطوح الموسّمة": "def:b2:surfaces:param",
    "الأقواس الموسّمة": "def:b2:curves:arc",
    "الأقواس الهندسية": "def:b2:curves:reparam",
    "الفضاءات المترية": "def:b2:metric:def",
    "الفضاءات الأفينية": "def:b2:affine:def",
    "المتغيرات العشوائية": "def:b2:randomvar:law",
    "الصور التربيعية": "def:b2:quadratic:def",
    "الصور التفاضلية": "def:b2:multint:lineint",
    "القيم الذاتية": "def:b2:reduction:eigen",
    # "vector" is متجهة series-wide (arabic_style_card.md §4), so the broken
    # plural to declare is المتجهات, not the old الأشعة.
    "المتجهات الذاتية": "def:b2:reduction:eigen",
    "الفضاءات الذاتية": "def:b2:reduction:eigen",
    "الفضاءات المعيارية": "def:b2:nvs:norm",
}
EXTRA_PROTECT = ()    # regexes for phrases where a defined word means something else
DERIVED = {}          # declared plurals and variants (see the note above)
PRIMARY_OK = set()
NO_CAPITAL = set()    # inert in a caseless script; use EXTRA_PROTECT instead

AMBIG_POLICY = "drop"
MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 40
