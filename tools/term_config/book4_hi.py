"""Book 4 (University Year 2) -- Hindi. Curation only; the rules live in
tools/termlink/.

Curated against the English link targets (the parity gate): the set of
`\\omterm` targets under parts/bachelor-2/hi must equal the English set, and a
term must reach the same definition it reaches in English.

Three Hindi facts drive the table below.

  * tools/term_config/lang_hi.py sets DERIVE = False and WORD_TAIL = '', so no
    inflected form is generated. Hindi marks the oblique plural with a matra
    (-ों / -ओं / -एँ) and derives adjectives with -ीय; since a matra is not a
    Python ``\\w`` character, a word boundary falls *between* the stem and its
    matra, so "चक्रों", "वर्णक्रमीय", "मानों" are matched on their stem
    automatically. That is convenient, and it is also the source of the two
    problems below.
  * The same missing boundary makes a defined term match as the PREFIX of an
    unrelated word: "चक्र" (cycle) inside "चक्रिका" (disk), "पूर्ण"
    (complete) inside "पूर्णांक" (integer), "सममित" (symmetric) inside
    "सममिति" (symmetry), "संतत" (continuous) inside "संतति" (progeny). It
    also makes a term match as the SUFFIX of a prefixed word: "प्रतिसममित"
    (antisymmetric) is cut after "प्रति". Every such word is listed in
    EXTRA_PROTECT; no morphological rule separates them, because the
    collision is orthographic, not grammatical.
  * HEAD = r'(?:[^\\W\\d_]+-)?' lets a hyphenated compound carry a link
    ("विषम-हर्मीशियन", "पूर्व-द्वैत", "अर्ध-विवृत", matching the English
    "skew-hermitian", "pre-dual", "half-open"). The prefix it captures is
    truncated at the first matra, which is cosmetic only -- the visible text
    is unchanged. Compounds whose head changes the SENSE ("आबेल-योग्य" =
    Abel-summable, not a summable family; "वृत्त-जनित" = circle-generated,
    not a generated subgroup) are protected by hand, exactly as book4_en.py
    protects `Abel-summable` and `circle-generated`.

AMBIG_POLICY is "drop", as in book4_en.py and in books 3 and 5.
"""

# The default NOT_A_TERM keywords are English. Hindi puts the head noun LAST
# ("कोरोवकिन की प्रमेय", not "theorem of Korovkin"), so a head filter cannot
# catch a Hindi result-name at all; the named results are listed in DROP
# below instead. The English strings are kept because the harvester falls
# back to the emphases the English twin accepted.
NOT_A_TERM = ("प्रमेय", "प्रमेयिका", "असमिका", "सूत्र", "कसौटी",
              "सिद्धांत", "सर्वसमिका", "विरोधाभास", "समस्या", "परिबंध",
              "theorem", "lemma", "inequality", "formula", "criterion",
              "principle", "identity", "rule", "law of", "paradox")

# Soft: a stoplisted word is still linked inside the chapter that defines it.
# One-for-one with book4_en.py's STOP.
STOP = {
    # ordinary Hindi far more often than the defined notion. "कोटि" is the
    # book's word for the order of a group element (ch. 1) AND for the order
    # of a derivative, of a Taylor expansion, of an ODE, and for the rank of
    # a matrix -- exactly the spread that makes English stoplist "order".
    "कोटि",
    # only NORMS are defined equivalent (ch. 5); "तुल्य" is the ordinary word
    # for "equivalent" everywhere else, and heads the equivalence relation
    # of ch. 1.
    "तुल्य",
    # "बीजगणित" is overwhelmingly "रैखिक बीजगणित" (linear algebra, the
    # subject) rather than the $K$-algebra of ch. 1.
    "बीजगणित",
    # defined for improper integrals (ch. 9); every series of chapters 7,
    # 10, 11, 14, 20, 21, 23 would otherwise land there.
    "अभिसरित",
    # alternating form (ch. 2) vs alternating series (ch. 7, 11)
    "एकांतर",
    # exact form (ch. 20) vs "the exact value/rate/exponent" (ch. 21--23)
    "यथातथ",
}

# Hard: never a link anywhere.
DROP = {
    # --- ordinary Hindi that happens to be a defined word -----------------
    # "चिह्न" is the signature of a permutation (ch. 1) AND the everyday word
    # for "sign" (sign of a coefficient, sign table, sign change, integral
    # sign, Descartes' rule of signs). English stoplists "signature"; in
    # Hindi even the defining chapter mixes the senses, so it must go.
    "चिह्न",
    # the signature of a quadratic form (ch. 12). English links neither
    # sense, so linking this one would break target parity.
    "चिह्नांक",
    # "संवृत" is "closed" in every sense: closed set (ch. 4), closed curve
    # (ch. 18, 21), closed interval, closed form (ch. 20). English hard-drops
    # bare "closed" for the same reason; the phrases "संवृत रूप" and
    # "यथातथ" carry def:b2:multint:exact.
    "संवृत",
    # --- named RESULTS, not notions (mirrors book4_en.py's DROP) ----------
    "गाउस का सीमा-सूत्र",                    # ch. 9 problem
    "कोरोवकिन की प्रमेय",                    # ch. 10 problem
    "आदामार की असमिका",                      # ch. 12 problem
    "कूराँ--फिशर न्यूनतम-अधिकतम प्रमेय",     # ch. 13 problem
    "वाइल की असमिका",
    "याकोबी सूत्र",                          # ch. 15 problem
    "स्टुर्म की पृथक्करण तथा तुलना प्रमेय",  # ch. 16 problem
    "समपरिमापी असमिका",                      # ch. 20 problem
    "हॉफडिंग असमिका", "चेर्नोफ़ परिबंध",
    "संकेंद्रण असमिकाएँ",                    # ch. 22 problem
    "गिब्स परिघटना",                         # named in a figure caption
    # prop:b2:structures:cyclic -- English does not link Euler's totient
    "ऑयलर फलन",
    # pb:b2:affine:1 -- English "centerpoint" is not harvested
    "केंद्रबिंदु",
}

# lang_hi.py generates no derived forms at all, and none are needed: the
# oblique plural and the -ीय adjective are already reached on the stem (see
# the module docstring).
DERIVED = {}

EXTRA = {
    # book4_en.py's own EXTRA: the phrase names the bilinear form of ch. 12,
    # defined a page before the symmetric endomorphism the bare word reaches.
    "सममित द्विरैखिक रूप": "def:b2:quadratic:def",
    # thm:b2:nvs:finitedim. English harvests it from
    # \index{equivalence of norms}; the Hindi \index key is
    # "मानदंडों की तुल्यता", whose head is a nominalisation the harvester
    # cannot reach from the stoplisted "तुल्य".
    "मानदंडों की तुल्यता": "thm:b2:nvs:finitedim",
}

NO_CAPITAL = set()     # Devanagari has no case
PRIMARY_OK = set()     # no overloaded word here has a dominant first sense
AMBIG_POLICY = "drop"  # the university convention (books 3, 4, 5)
MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 40

# Spans that must not be touched.
EXTRA_PROTECT = [
    # --- a defined term is the orthographic PREFIX of a different word ----
    r'चक्रिका',            # disk, not a cycle
    r'चक्रीयता',           # cyclicity: the linkable term is "चक्रीय"
    r'पूर्णांक',           # integer, not a complete space
    r'सूचनापूर्ण',         # informative
    r'सममिति',             # symmetry (also सममितियाँ), not a symmetric map
    r'संतति',              # offspring / total progeny (ch. 23), not continuity
    r'मानदंडित',           # "normed": English does not link the adjective
    r'तुल्याकारिता',       # isomorphism, not equivalence of norms
    r'परिवर्तित',          # changed, not the transpose
    r'अवकलित',             # differentiated, not the differential
    r'बीजगणितीय',          # algebraic, not a $K$-algebra
    r'चिह्नित',            # marked
    r'अंगुलिचिह्न',        # fingerprint
    r'परिघटना',            # phenomenon, not a probabilistic event
    # --- a defined term is the SUFFIX of a prefixed word ------------------
    r'प्रतिसममित',         # antisymmetric
    # --- hyphenated compounds whose head changes the sense ----------------
    r'आबेल-योग्य',         # Abel-summable, not a summable family
    r'चेज़ारो-योग्य',      # Cesaro-summable
    r'वृत्त-जनित',         # circle-generated
    r'समाकल-चिह्न',        # the integral sign
    r'परिष्करण-चक्र',      # a refinement cycle, not a permutation cycle
    # --- "पूर्ण" = total / perfect / whole, not a complete metric space ---
    r'पूर्ण\s+प्रायिकता',      # total probability
    r'पूर्ण\s+परिबद्धता',      # total boundedness
    r'पूर्ण\s+वर्ग',           # perfect square
    r'पूर्ण\s+विलोपन',         # total extinction
    r'पूर्ण\s+एकांतरण',        # perfect alternation
    r'पूर्ण\s+संतति',          # total progeny
    r'पूर्ण\s+मंच',            # "the complete stage" of a problem
    r'पूर्ण\s+द्विभाजन',       # a clean dichotomy
    r'पूर्ण\s+फेरे',           # a full turn
    # --- "सममित" in its ordinary sense; "symmetrically" is dropped in EN --
    r'सममित\s+रूप\s+से',
    r'सममित\s+(?:घटना|स्थिति|सूचकांक|आंशिक|भाग)',
    # --- "नियम" as the name of a RESULT, not the law of a random variable -
    r'शृंखला\s+नियम',                       # chain rule
    r'बृहत्\s+संख्याओं\s+(?:का|के)\s+\S*\s*नियम',
    r'(?:दुर्बल|प्रबल|स्थानीय|सीमा)\s+नियम',
    r'परावर्तन\s+(?:का|के)\s+नियम',         # law of reflection
    r'विभाग\s+नियम',                        # quotient rule
    r'क्रामर\s+(?:का|के)\s+नियम',           # Cramer's rule
    r'चिह्न-नियम',                          # Descartes' rule of signs
    r'अंगूठे\s+का\s+नियम',                  # rule of thumb
    r'रोकन',                                # "stopping rules"
    r'नियम\s+कृपापूर्वक',                   # "the limit law mercifully..."
    # --- "अवकल" as an adjective on a subject, not the differential of a map
    r'अवकल\s+(?:समीकरण|कलन|ज्यामिति|निकाय|समाकृतिकता|समाकृतिकताएँ)',
    # --- a convex FUNCTION / curve is not the convex set of ch. 17 --------
    r'उत्तल\s+(?:फलन|वक्र|संचय|संचयों)',
    # --- a run length / a text length, not arc length ---------------------
    r'कतार\s+की\s+लंबाई',
    r'किसी\s+भी\s+लंबाई',
]
