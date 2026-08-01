"""Book 5 (University Year 3) -- Hindi. Curation only; the rules live in
tools/termlink/.

The design principle here is *mirror English, word for word*. book5_en.py is
frozen and almost empty: it stops the ordinary English words and the words
whose sense changes by chapter, marks six of them as "first sense dominates",
and lets the harvest do everything else. A Hindi config that stops a different
set of words produces a different link layer, and the reader of the Hindi
edition then meets links the English reader does not (and misses links the
English reader gets). So every entry of STOP below is the Hindi rendering of an
entry of ``book5_en.STOP``, and PRIMARY_OK is the Hindi rendering of
``book5_en.PRIMARY_OK``, item for item.

What cannot be mirrored is spelling: Hindi has no ``-s`` plural for
``morphology.derive`` to append (``lang_hi.WORD_TAIL`` is empty and ``DERIVE``
is off), so every surface form a Hindi sentence actually uses -- the oblique
plural *अवकल रूपों*, the shortened *इकाई विभाजन* against the index key
*इकाई का विभाजन* -- has to be declared by hand in EXTRA. That, and the two
homographs Hindi has where English has two different words, is the whole
content of this file.

AMBIG_POLICY = "drop": at third-year level a word two chapters define
differently is a genuine ambiguity, not a spiral re-definition, and a wrong
link costs more than a missing one. The ``local`` mechanism still links such a
word inside the chapter that pins it down -- exactly what English does.
"""

# A result is not a term: "बेयर की प्रमेय" must not become a link. These are the
# heads of book5_en.NOT_A_TERM in the forms styles/lang/hi.tex fixes for the
# statement environments (प्रमेय / प्रमेयिका / उपप्रमेय / प्रतिज्ञप्ति).
#
# Note on "नियम" (both *rule* and *law*): English blocks bare "rule" but only
# the phrase "law of", because *tower law* and *zero--one law* ARE names it
# links. Hindi cannot draw that line lexically -- मीनार नियम and शून्य--एक नियम
# are spelled with the same word as any चेन नियम -- so bare "नियम" is
# deliberately NOT listed here (listing it costs two targets English has); it
# is stoplisted instead, which is soft, and the Hindi rule-names that then slip
# through the index harvest are named in DROP.
NOT_A_TERM = ("प्रमेय",        # theorem (also catches प्रमेयिका, उपप्रमेय)
              "प्रतिज्ञप्ति",  # proposition
              "असमिका",        # inequality
              "सूत्र",          # formula
              "कसौटी",         # criterion
              "सिद्धांत",       # principle
              "सर्वसमिका",      # identity
              "विरोधाभास",      # paradox
              "समस्या")        # problem

# Single words that are ordinary Hindi, or whose sense changes by chapter.
# Their disambiguated phrases -- संहत संकारक, संवृत रूप, अभाज्य आदर्श -- survive,
# because those come from the \index entries. STOP is SOFT on purpose: a
# stoplisted word is still linked inside the chapter that defines it, which is
# what lets संहत point at the space in ch. 6 and at the operator in ch. 15.
#
# Each line names the book5_en.STOP entry it mirrors.
STOP = {
    "प्रत्यक्ष",      # direct     (प्रत्यक्ष गुणन / a direct parametrization)
    "सरल",           # simple     (simple group / simple function / "plain")
    "स्थायी",         # stable     (Lyapunov stable / a stationary vector)
    "तुल्य",          # equivalent
    "पूर्णांक",       # integer
    "सूचकांक",        # index      (winding index / an index of summation)
    "नियम",          # law        (see the NOT_A_TERM note above)
    "जनित",          # generated
    "अभिसरित",       # converges
    "घटना",          # events
    "घटनाएँ",
    "लगभग सर्वत्र",   # a.e.
    "सघन",           # dense
    "प्रसामान्य",     # normal     (normal subgroup / the normal distribution)
    "महत्तम",         # maximal    (maximal ideal / महत्तम समापवर्तक / "greatest")
    "मुख्य",          # principal
    "मूलक",          # radical
    "अंतर्वस्तु",     # content
    "अभिलक्षणिक",     # characteristic
    "अपरिवर्ती",      # invariant
    "परिबद्ध",        # bounded
    "क्रिया",         # action     (group action / an ordinary "operation")
    "आधार",          # basis      (basis of a topology / of a space / base $b$)
    "घात",           # degree     (degree of an extension / an exponent)
    "मुक्त",          # free       (free module / "free of", "rid of")
    "यूक्लिडीय",      # Euclidean  (Euclidean domain / the Euclidean norm)
    "वियोज्य",        # separable  (separable extension / separable space)
    "संवृत",          # closed     -> PRIMARY_OK
    "यथार्थ",         # exact
    "संहत",          # compact    -> PRIMARY_OK
    "अभाज्य",         # prime
    "अखंडनीय",        # irreducible -> PRIMARY_OK
    "आदिम",          # primitive
    "गुणन",          # product
    "गुणनफल",
    "भागफल",         # quotient
    "उपसमष्टि",       # subspace
    "पथ",            # path       -> PRIMARY_OK
    "परिसीमा",        # boundary   -> PRIMARY_OK
    "अंतःभाग",        # interior   -> PRIMARY_OK
    # Two homographs Hindi has where English has two distinct words. Both are
    # soft, so each is still linked inside the chapter that defines it.
    "सीमा",          # limit AND boundary: the book writes परिसीमा for the
                     # boundary, but plain सीमा is the ordinary word for a limit
                     # and for केंद्रीय सीमा प्रमेय
}

# Overloaded words whose first sense dominates the book, so they may be linked
# outside the chapter that pins them down. book5_en.PRIMARY_OK item for item:
# compact, closed, path, boundary, interior, irreducible.
PRIMARY_OK = {"संहत", "संवृत", "पथ", "परिसीमा", "अंतःभाग", "अखंडनीय"}

# Surface forms the Hindi text really uses and the harvest cannot reach.
# Hindi has no productive plural suffix for morphology.derive to append, so
# oblique plurals and the short forms prose prefers over the index key have to
# be spelled out. Each entry names the English link it restores.
EXTRA = {
    # oblique plural -ओं; English gets "differential forms" from WORD_TAIL
    "अवकल रूपों": "def:b3:forms:diffform",
    "अवकल रूप": "def:b3:forms:diffform",
    # the index key is इकाई का विभाजन; every use in prose drops the का
    # (EN: "partition of unity", 5 links)
    "इकाई विभाजन": "lem:b3:forms:partition",
    # EN links bare "flow" (5 links); bare प्रवाह is also fluid flow in ch. 18
    # and heat flow in ch. 14, so only the unambiguous phrase is declared
    "प्रवाह प्रतिचित्रण": "ex:b3:ode:planeclassification",
    # oblique plural again: EN "elementary divisors" (7)
    "प्रारंभिक भाजकों": "thm:b3:modules:structure",
    # EN "torsion-free" (13); Hindi negates with a hyphenated suffix, which
    # ends the word for the boundary rule, so मरोड़ never reaches it
    "मरोड़-मुक्त": "def:b3:modules:torsion",

    # --- the abstract nouns English gets free from book5_en.DERIVED ----------
    # English derives continuity from continuous, solvability from solvable,
    # and so on; Hindi forms them by a different stem (संतत -> सांतत्य), which
    # no suffix rule reaches. Counts in brackets are the English link counts
    # the entry restores.
    "सांतत्य": "def:b3:topology:continuity",        # continuity [173]
    "समसांतत्य": "def:b3:complete:equicontinuous",   # equicontinuity
    "पथ-संबद्धता": "def:b3:topology:pathconnected",  # path-connectedness
    "संबद्धता": "def:b3:topology:connected",        # connectedness [20]
    "पूर्णता": "def:b3:complete:complete",          # completeness [21]
    "मापनीयता": "def:b3:lebesgue:measurable",       # measurability
    "समाकलनीयता": "def:b3:lebesgue:l1",             # integrability
    "समविश्लेषिकता": "def:b3:holomorphic:holo",      # holomorphy
    "विलेयता": "def:b3:groups:derived",             # solvability [9]
    "स्वसंलग्नता": "def:b3:spectral:selfadjoint",    # self-adjointness
    "अभिविन्यासनीय": "def:b3:forms:orientation",     # orientable
}

# Harvested Hindi terms that name a *result* rather than a notion, or that
# English refuses through its own NOT_A_TERM. Each carries, in a comment, the
# target it would have reached, so the parity argument is auditable line by
# line.
#
# This is the hard list, and it is NOT `set(STOP)`: the previous version of this
# file wrote `DROP = set(STOP)`, which hard-dropped every stoplisted word
# everywhere and destroyed the soft, chapter-local linking that STOP exists to
# provide.
DROP = {
    "महत्तम समापवर्तक",   # -> lem:b3:rings:bezout; English does not link the gcd
}

NO_CAPITAL = set()   # Devanagari has no letter case: nothing to key on
DERIVED = {}         # lang_hi.DERIVE is off; variants are declared in EXTRA
AMBIG_POLICY = "drop"
MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 40

# A defined word carrying another sense inside a fixed phrase. Audited against
# the four silent-failure rules: none of these consumes a `$` (a pattern that
# eats an opening dollar leaves the inline-math rule pairing the closing one
# with the next formula's opening dollar, masking every later span inside out);
# none contains a literal space, so each still matches across a line break (the
# list is compiled with re.S); each was checked on unwrapped source; and each
# was verified live by a moved link count, which is the only check that
# distinguishes a working pattern from one that matches nothing.
EXTRA_PROTECT = [
    # पूर्ण = *complete* (ch. 7) but also plain *full*: "पूर्ण (पारस्परिक)
    # स्वातंत्र्य" is English's "full mutual independence", which links only
    # *independence*. 6 occurrences, in ch. 22 and its solutions.
    #
    # A fifth rule, learned here: the pattern must be IDEMPOTENT under its own
    # output. The narrower `पूर्ण(?=\s+...स्वातंत्र्य)` -- a lookahead, so that
    # only पूर्ण is masked and English's स्वातंत्र्य link survives -- stops
    # matching the moment स्वातंत्र्य is wrapped, so a second `--apply` inserted
    # 6 links a `--check` then reported as stale. Consuming the whole phrase
    # costs 6 correct स्वातंत्र्य links to buy back 6 wrong पूर्ण ones, and it is
    # stable: measured 4125 links with EXTRA_PROTECT empty against 4113 with
    # this pattern -- the 12 being 6 wrong पूर्ण links and the 6 correct
    # स्वातंत्र्य links that go with them.
    r'पूर्ण\s+(?:\(?पारस्परिक\)?\s+)?स्वातंत्र्य',
]

# Verified idempotent: --unwrap --apply, then --apply inserts 0, then --check
# reports every file matching what the config generates.
