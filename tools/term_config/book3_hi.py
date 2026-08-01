"""Book 3 -- hi. Curation only; the rules live in tools/termlink/.

University Year 1: AMBIG_POLICY drop (no spiral nearest-preceding).

Curated against ``book3_en.py`` entry by entry: the Hindi edition must link the
same *targets* as English, so every English STOP/DROP/EXTRA was checked against
the word the Hindi text actually uses, and the Hindi-only traps were added.

Hindi has no letter case, so ``NO_CAPITAL`` cannot separate an imperative from a
noun (English needs it for "Set", "Map", "Group"); the Hindi verbs are different
words (``रखिए``, ``भेजिए``, ``समूहबद्ध कीजिए``) and no such split is needed.

``lang_hi.py`` sets ``WORD_TAIL = ''`` and ``DERIVE = False``: no inflected form
is generated, so the oblique plurals the book uses constantly (``बहुपदों``,
``समुच्चयों``, ``फलनों``, ``प्रमेयों``) are simply unreachable.  That, not
curation, is the whole of the residual gap against English; see
``translation_scores/book_3/hi/translation_score.md``.
"""

# Result heads: index-only harvests whose head is a result name, not a notion.
# The book writes असमिका (not असमानता) for *inequality* and कसौटी for *test*;
# both spellings are kept so a future chapter cannot slip a result name through.
NOT_A_TERM = ("प्रमेय", "उपप्रमेय", "असमानता", "असमिका", "सूत्र", "मानदंड",
              "सिद्धांत", "सर्वसमिका", "नियम", "नियम की", "विरोधाभास",
              "समस्या")

# Soft: still linked inside the chapter that defines the term.
STOP = {
    "पहला", "पहली",
    "परिमित",          # "परिमित योग/कुल/सम्मिलन" is not the finite *set* of ch. 2
    "तर्क",            # "यही तर्क दिखाता है" -- not the argument of a complex number
    "एकक",             # "एकक सदिश/वृत्त/अंतराल" vs the unit of a ring
    "सममिति",          # "सममिति से" -- not the linear involution of ch. 20
    "संयुग्मी",        # ch. 3 complex conjugate vs the conjugate expression of
                       # ch. 11 vs conjugating a matrix in ch. 21/22 -- English
                       # STOPs *conjugate* for exactly these three senses
    "प्रवणता",         # ch. 25 defines the *gradient*; the same Hindi word is the
                       # *slope* of a one-variable graph in ch. 4, 11, 14 and 24.
                       # English keeps them apart lexically (gradient / slope) and
                       # links def:b1:multivar:partial in ch. 25 only, which is
                       # exactly what STOP reproduces here.
}

# Never linked anywhere.  Deliberately NOT seeded from STOP: the stub this
# replaced wrote `DROP = set(STOP)`, which turned every soft stop into a hard one
# and threw away the chapter-local links STOP exists to keep.
DROP = {
    # --- ordinary Hindi in this register / a second technical sense ---
    "क्रम",            # "उलटे क्रम में", "क्रम से", and the *order of a group*
                       # (ch. 7) -- English links only the order *relation*
    "प्रत्यक्ष",       # bare "direct": a direct isometry (ch. 23) is not the
                       # direct sum of ch. 18; "प्रत्यक्ष योग" survives
    "क्रांतिक",        # bare adjective; "क्रांतिक बिंदु" survives
    "बीजीय", "अबीजीय",  # bare adjectives ("बीजीय संरचना/युक्ति"); the compounds
                        # "बीजीय संख्या" / "अबीजीय संख्या" survive
    "सदृश",            # "सदृश संगणना" -- keep only "सदृश आव्यूह", which English
                       # harvests but never uses, so it is dropped too (below)

    # --- names of results: the point is to link definitions, not theorems.
    # NOT_A_TERM only filters index-only harvests; these arrive through
    # \emph{...}\index{...} and have to be dropped by hand, exactly as the
    # English config drops their twins.
    "कुमर की प्रमेय",           # Kummer's theorem
    "लजांद्र का सूत्र",          # Legendre's formula
    "डी मॉर्गन के नियम",        # De Morgan's laws
    "टॉलेमी असमिका",            # Ptolemy's inequality
    "लिउविल असमिका",            # Liouville inequality
    "एकांतरित श्रेणी का आकलन",   # alternating series estimate
    "फलनीय समीकरण",             # functional equation
    "कोशी का फलनीय समीकरण",      # Cauchy's functional equation

    # --- target parity with English.  Each of these is a correct-sense Hindi
    # link, but English never links the target (the English prose writes the
    # symbol where Hindi spells the name out), so linking it here would give the
    # Hindi edition a target the English edition does not have.
    "लघुत्तम समापवर्त्य",        # least common multiple: EN writes \lcm
    "कोणांक",                   # the argument of a complex number; EN DROPs
                                # *argument* outright
    "संयोजन-नियम",              # composition law
    "सम्मिश्र निर्देशांक",       # complex coordinates
    "त्रिभुज असमिका",           # triangle inequality (a result name besides)
    "समकाल वक्र",               # tautochrone
    "तुल्य आव्यूह", "सदृश आव्यूह",  # similar matrices
}

# Terms the harvester misses.
EXTRA = {
    # The definitions emphasise a compound ("\emph{$x_0 \in I$ पर संतत}",
    # "\emph{$x_0 \in I$ पर अवकलनीय}"), so the bare adjective -- the form the
    # rest of the book actually uses -- is never harvested.  English restores
    # "continuous"/"continuously"/"differentiable" for the same reason.
    "संतत":      "def:b1:continuity:continuous",
    "अवकलनीय":   "def:b1:derivative:def",
    # Hyphenated compound: the index-only harvest requires a space in the term,
    # so a solid or hyphenated Hindi compound is never seen (the gotcha
    # documented for Dutch in CLAUDE.md).  English harvests "cofactor expansion".
    "सहगुणनखंड-प्रसार": "thm:b1:det:cofactor",
    # NOT_A_TERM's bare "नियम" (Hindi says *niyam* for both *rule* and *law*)
    # eats the tower law, which English keeps because its NOT_A_TERM lists the
    # phrase "law of" rather than the bare noun.
    "मीनार नियम": "pb:b1:findim:1",
    # \index{ऑयलर का अचर} sits in exercise 12, *before* the weekend problem that
    # defines gamma, so the nearest preceding statement is an unrelated
    # telescoping example.  Point it at the problem, as English does.
    "ऑयलर का अचर": "pb:b1:series:1",
}

# Devanagari has no letter case: an imperative cannot be told from a noun by its
# first letter, and the Hindi imperatives are different words anyway.
NO_CAPITAL = set()

# lang_hi.py has DERIVE = False, so nothing is generated from a stem.
DERIVED = {}

PRIMARY_OK = set()

AMBIG_POLICY = "drop"

MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 40

# Fixed Hindi phrases that contain a linkable word in another sense.  Every "$"
# is matched by a lookahead only, never consumed: a protect pattern that eats the
# opening $ of a formula inverts inline-math masking for the rest of the file.
EXTRA_PROTECT = [
    r'से\s+स्वतंत्र',            # "$\theta$ से स्वतंत्र" = independent *of*,
                                 # not a free family
    # *bijection*, the noun.  English writes it as one unharvested word and
    # therefore never links it (95 occurrences, 0 links); Hindi builds it out of
    # the adjective, so without this the same 82 sites would link in Hindi and
    # not in English.  The adjective "एकैकी आच्छादक" is a harvested term of its
    # own and still links (42, against English's 41 "bijective").
    r'एकैकी\s+आच्छादन',
    r'स्वतंत्र\s+चर',            # independent variable
    r'रैखिक\s+बीजगणित',          # linear algebra (EN protects the same phrase)
    r'रैखिक\s+संचय',             # linear combination
    r'रैखिक\s+व्यंजक',           # linear expression
    r'उच्चतम\s+घात',             # "highest degree", not a supremum
    r'संवृत\s+रूप',              # "closed form", not a closed set
    r'मुक्त\s+पतन',              # free fall (physics), not a free family
]
