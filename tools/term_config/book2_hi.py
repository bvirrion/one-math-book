"""Book 2 -- hi (standard technical Hindi). Curation only; the rules live in
tools/termlink/.

The Hindi bodies (parts/grade-10..12/hi) are UTF-8 Devanagari. Devanagari
letters are ``\\w``, so the shared pattern's lookaround already protects every
*solid* compound: वर्गमूल and घनमूल never leak a link on मूल, त्रिभुज and
बहुभुज never leak one on भुज, समकोण and समांतर never leak one on सम. Only
**open** (space- or hyphen-separated) compounds need guarding, and those are
the EXTRA_PROTECT list below.

Four homographs are Hindi-only and drive most of the curation:

  * **कोटि** is the *ordinate* of coordinate geometry **and** the everyday
    "order / rank / kind": परिमाण की कोटि (order of magnitude), प्रथम कोटि का
    समीकरण (first-order equation), एक कोटि के तीन पत्ते (three cards of one
    rank). English keeps *ordinate* and *order* apart; Hindi does not.
  * **प्रसार** is the *expansion* of an algebraic expression **and** the
    *spread* of a data set (English: expanding / spread).
  * **परिमाण** is the *norm* of a vector **and** the *magnitude* of an
    earthquake and the परिमाण की कोटि above.
  * **मापांक** is the *modulus* of a complex number **and** the *modulus n*
    of the arithmetic chapter -- exactly the trap Portuguese hits with
    "módulo", and here it bites harder because the arithmetic chapter comes
    directly after the complex-numbers one.

The first three are handled by the soft STOP (which keeps them linked inside
the chapter that defines them, where the sense is right); the fourth by phrase
guards, so the genuine complex-modulus links survive.

Known, accepted gap: Hindi inflects the oblique plural (पूर्णांक ->
पूर्णांकों, वास्तविक संख्या -> वास्तविक संख्याओं) and lang_hi.py deliberately
carries no WORD_TAIL, so those forms reach the linker only when the sources
happen to define them too. The commonest ones are declared in EXTRA below;
the long tail is left unlinked rather than risk a blanket suffix rule that
would also match unrelated words.
"""

# "एक प्रमेय कोई धारणा नहीं है": the Hindi counterpart of the default
# NOT_A_TERM keywords, which are English and therefore let पास्कल का नियम,
# ब्येनेमे--चेबिशेव असमिका and मार्कोव असमिका through as if they were notions.
NOT_A_TERM = ("प्रमेय", "प्रमेयिका", "उपप्रमेय", "प्रतिज्ञप्ति",
              "असमिका", "असमानता", "सूत्र", "कसौटी", "मानदंड",
              "सिद्धांत", "सर्वसमिका", "विरोधाभास", "भ्रांति",
              "समस्या", "विधि", "पद्धति", "योजना",
              "नियम", "नियम की", "नियम के", "कलनविधि")

# Ordinary Hindi, or a word whose sense in most of the book is not the
# definition's. STOP is SOFT: a stoplisted word is still linked inside the
# chapter that defines it -- which is exactly what these entries want.
STOP = {
    # the ordinate of a point (grade 10) against "order / rank / kind"
    # everywhere else: परिमाण की कोटि, प्रथम कोटि, एक कोटि के तीन पत्ते
    "कोटि",
    # expanding an expression (grade 10) against the *spread* of a data set
    # (grades 10--12) and दशमलव प्रसार
    "प्रसार",
    # the norm of a vector (grade 11) against भूकंप का परिमाण and
    # परिमाण की कोटि
    "परिमाण",
    # parity (grade 11) against the ordinary "even / odd number", exactly as
    # English keeps "even" and "odd" chapter-local
    "सम", "विषम",
    # the arrangement of k elements (grade 12) against अक्षर-विन्यास
    "विन्यास",
    # "बराबर", "अचर", "एक साथ": ordinary emphasis inside definitions
    "बराबर", "अचर", "एक साथ", "सभी", "क्रमित", "पहला", "पहली",
    # "combination" of k elements against a linear/integer combination
    # (Bézout, coplanar vectors) and निवेश-संचय
    "संचय", "संयोजन",
    # the "युग्म" of a definition is any ordered pair in most chapters
    "युग्म", "योग",
}

NO_CAPITAL = set()

# Hindi oblique plurals that occur often enough to be worth declaring, plus
# the two display spellings the sources alternate between.
EXTRA = {
    # -- oblique plurals of single-word terms ------------------------------
    "अंतरालों": "def:g10:numbers:interval",
    "फलनों": "def:g10:functions:function",
    "सदिशों": "def:g10:vectors:vector",
    "समीकरणों": "def:g10:algebra:equation",
    "अभाज्यों": "def:g12:arith:prime",
    "आव्यूहों": "def:g12:matrix:matrix",
    "अनुक्रमों": "def:g11:seq:sequence",
    "प्रायिकताओं": "def:g10:proba:distribution",
    "घटनाओं": "def:g10:proba:events",
    "चतुर्थकों": "def:g10:stats:quartiles",
    "निर्देशांकों": "def:g10:coordgeom:system",
    "मूलों": "def:g11:quad:discriminant",
    "लघुगणकों": "def:g12:exp:ln",
    "प्रतिबिंबों": "def:g10:functions:function",
    "समाकलों": "def:g12:integ:area",
    "अवकलजों": "def:g12:deriv:derivative",
    "प्रतिअवकलजों": "def:g12:integ:primitive",
    "सारणिकों": "def:g11:vect:det",
    "प्रांतों": "def:g11:func:function",
    "सम्मिलनों": "def:g10:numbers:interunion",
    "प्रतिदर्शों": "def:g10:proba:sample",
    "गुणजों": "def:g12:arith:divides",
    "घनत्वों": "def:g12:contdist:density",
    "बंटनों": "def:g11:prob:rv",
    "वृक्षों": "met:g10:proba:tree",
    "आलेखों": "def:g10:functions:graph",
    "गुणनखंडनों": "def:g10:algebra:expand",
    "कोणांकों": "def:g12:complex:argument",
    "मापांकों": "def:g12:complex:modulus",
    "z-मानों": "pb:g11:stat:1",
    "विन्यासों": "def:g12:comb:tuples",
    "माध्यों": "def:g10:stats:mean",
    "परिमाणों": "def:g11:scal:dot",
    # -- the two result names English links (its NOT_A_TERM has no "rule" /
    # "algorithm"); NOT_A_TERM above drops every other नियम / कलनविधि, as
    # English drops "law of cosines", "chain rule", "law of large numbers"
    "पास्कल का नियम": "prop:g12:comb:identities",
    "यूक्लिड की कलनविधि": "prop:g12:arith:euclidalgo",
    # -- feminine plurals in -एँ: the term itself cannot reach them, because
    # एँ opens with a letter and the shared lookahead is (?![\w-])
    "घटनाएँ": "def:g10:proba:events",
    "प्रायिकताएँ": "def:g10:proba:distribution",
    "वास्तविक संख्याएँ": "def:g10:numbers:sets",
    "परिमेय संख्याएँ": "def:g10:numbers:sets",
    "अपरिमेय संख्याएँ": "ex:g10:numbers:classify",
    "सम्मिश्र संख्याएँ": "def:g12:complex:def",
    "स्पर्श रेखाएँ": "def:g11:deriv:tangent",
    # -- oblique plurals of phrase terms -----------------------------------
    "वर्धमान फलनों": "def:g11:func:monotone",
    "आधार फलनों": "def:g11:func:reference",
    "विषम फलनों": "def:g11:func:parity",
    "एकघात फलनों": "def:g10:reffunc:affine",
    "प्रसामान्य बंटनों": "def:g12:contdist:normal",
    "संबद्ध कोणों": "prop:g11:trigo:associated",
    "यादृच्छिक चरों": "def:g12:randvar:rv",
    "बीजगणितीय रूपों": "def:g12:complex:def",
    "अवकल समीकरणों": "def:g12:diffeq:ode",
    "मानक विचलनों": "def:g11:stat:variance",
    "गुणोत्तर अनुक्रमों": "def:g11:seq:geometric",
    "बर्नूली परीक्षणों": "def:g11:binom:bernoulli",
    "औसत परिवर्तन दरों": "def:g11:deriv:rate",
}

DROP = set()
DERIVED = {}
PRIMARY_OK = set()

# School book: the spiral curriculum re-defines a term year after year, so a
# use is linked to the definition the reader has most recently met.
AMBIG_POLICY = "nearest-preceding"

MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 40

# Never consume a `$` (see tools/termlink/protect.py): every math-adjacent
# guard below ends in a lookahead.
EXTRA_PROTECT = [
    # =====================================================================
    # Devanagari word boundaries.  The shared pattern brackets a term with
    # (?<![\w\\@-]) ... (?![\w-]), and Python's \w is false for every
    # Devanagari matra, virama and anusvara (they are Mc/Mn, not alnum).  A
    # term therefore matches inside a longer orthographic word whenever the
    # boundary falls on a vowel sign: भुज (abscissa) inside भुजा (side),
    # ज्या (sine) inside त्रिज्या (radius), माध्य (mean) inside माध्यिका
    # (median), सम (even) inside समुच्चय (set) -- a wrong link, and a link
    # that splits a consonant cluster in two boxes, which XeLaTeX renders
    # with a dotted circle.  Every group below closes one such hole; the
    # request to fix the lookaround once, for every Indic edition, is in
    # translation_scores/book_2/hi/translation_score.md.
    # =====================================================================
    # ---- भुज (abscissa) inside the polygons and inside भुजा (side) -------
    r'(?<!पास्कल\s)(?:त्रि|चतुर्|समचतुर्|बहु|षट्|द्वि|पंच|अष्ट)भुज',
    r'भुज[ाीो][ऀ-ॣ]*',
    # ---- ज्या (sine) inside त्रिज्या / परित्रिज्या (radius) --------------
    r'त्रिज्या',
    # ---- घटना (event) inside परिघटना / दुर्घटना -------------------------
    r'(?:परि|दुर्)घटना[ऀ-ॣ]*',
    # ---- सम (even) inside four ordinary words ---------------------------
    r'समुच्चय', r'समाप्त', r'समापन',
    r'(?<!खंडशः\s)समाकलन',      # समाकलन, but not the term खंडशः समाकलन
    r'संपूरक',                  # complementary, not the पूरक of an event
    # ---- stems inside a derived adjective or a different word -----------
    r'मूल[्ी][ऀ-ॣ]*',          # मूल्य (value), मामूली (ordinary)
    r'पूर्णांकित',              # rounded, not "integer"
    r'आलेखित',                  # plotted, not "graph"
    r'लघुगणकीय',                # logarithmic, not "logarithm"
    r'फलन[ीा][ऀ-ॣ]*',          # फलनीय, फलनात्मक
    r'परवलय[ािी][ऀ-ॣ]*',      # परवलयीय, परवलयाकार, अतिपरवलयिक
    r'माध्यिका[एओ][ऀ-ॣ]*',     # माध्यिकाएँ / माध्यिकाओं: the term itself
                                # cannot match (एँ, ओं start with a letter),
                                # so माध्य would grab the stem
    # माध्यिका inside its own two definitions, where the median link is
    # suppressed and माध्य would take the stem instead
    r'आधे\s+मान\s+माध्यिका', r'विषम\s+हो\s*,?\s*तो\s+माध्यिका',
    # ---- open compounds: the shared HEAD (?:[^\W\d_]+-)? swallows only the
    # tail of the first element when that element ends in a vowel sign
    # (को|र-सदिश, क्|रमचय-संचय), so the whole compound is guarded here ----
    r'[ऀ-ॣ]+-(?:समीकरण|सदिश|संचय|अनुक्रम|गुणनखंडन|सन्निकटन|माध्य|गुणोत्तर'
    r'|मध्यबिंदु|चतुर्थक|फलन|प्रायिकता|अंतराल|मूल)',
    r'(?<!सह)-अभाज्य',          # छद्म-अभाज्य, but सह-अभाज्य is a term
    r'अक्षर-विन्यास', r'दर्पण-प्रतिबिंब',
    # =====================================================================
    # Ordinary-language senses of a defined word (the classic EXTRA_PROTECT)
    # =====================================================================
    # ---- मूल: the root of an equation, against the four open compounds ---
    r'मूल\s+बिंदु',            # the origin of a coordinate system
    r'मूल\s+प्रमेय',           # the fundamental theorem (of calculus/algebra)
    r'मूल\s+सूत्र',            # the "mother formula" of the addition formulas
    r'मूल\s+वक्र',             # the master curve of the similar parabolas
    r'मूल\s+अंतराल',           # the original interval of a dichotomy
    r'मूल\s+प्रतिरूप',
    # ---- सम: parity, against the regular polygons and solids ------------
    r'सम\s+(?:बहुभुज|पंचभुज|षट्भुज|चतुष्फलक|अष्टभुज)',
    # ---- मापांक: the complex modulus, against "modulo n" ----------------
    r'अभाज्य\s+मापांक',
    r'मित्रवत\s+मापांक',
    r'मापांकों?(?=\s*\$)',      # "मापांक $13$": lookahead, never eat the $
    # ---- अंतराल: the mathematical interval, against the gap between buses
    r'माध्य\s+अंतराल',
    r'(?:लंबे|लंबा|लंबी|बड़े|बड़ा|प्रारूपिक|छोटे)\s+अंतरालों?',
    r'अंतरालों?\s+(?:बारी-बारी|की\s+लंबाई)',
    r'गिरते\s+हैं:\s*अंतराल',
]
