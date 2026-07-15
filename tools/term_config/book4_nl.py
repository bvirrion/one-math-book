"""Book 4 -- nl. Curation only; the rules live in tools/termlink/.

The traps are Dutch, not the English or French ones. Pattern: book3_nl.py
(phrase NOT_A_TERM, solid compounds in EXTRA) + book4_fr.py / book4_en.py
parity (drop result-names and ambiguous bare words English never links).

tools/term_config/lang_nl.py sets DERIVE = False and WORD_TAIL = (?:e?[ns])?,
so compounds and many adjectives must be declared by hand in EXTRA.
"""

# "een stelling is geen begrip": default NOT_A_TERM is English, so Dutch
# "stelling van X" / "formule van Y" slip through. Use PHRASE forms only --
# bare "stelling"/"regel" would substring-match solid compounds.
NOT_A_TERM = ("stelling van", "formule van", "ongelijkheid van", "regel van",
              "wet van", "wetten van", "lemma van", "identiteit van",
              "criterium van", "principe van", "paradox van")

# Soft: still linked inside the chapter that defines them.
STOP = {
    # ordinary language far more often than the defined notion
    "orde",            # "in orde", "sommatievolgorde"; group order still via phrases
    "equivalent",      # "de drie voorwaarden zijn equivalent"
    "algebra",         # "lineaire algebra", "de algebra is mechanisch"
    "convergeert",     # defined for improper integrals; series uses would land there
    "absoluut",        # "absoluut convergent" series vs ordinary "absoluut"
    # sense changes by chapter / ordinary language
    "alternerend",     # form (ch.2) vs series
    "signatuur",       # permutation (ch.1) vs quadratic form (ch.12); EN never links bare
    "exact",           # exact form vs "exacte waarde"
    "lengte",          # arc length vs ordinary length / cycle length
    "wet",             # law of RV vs ordinary "wet"
    "open",            # open set -- over-links ordinary Dutch "open"
    "duale",           # "duale basis" is the phrase; bare "duale" is noisy
    "affien",          # adjective on many nouns; phrases keep the link
    "cyclisch",        # cyclic group vs cyclic order / cyclic product
    "congruentie",     # matrix congruence vs ordinary congruence
    "normaal",         # normal convergence vs normal endomorphism / principal normal
    "continu",         # ordinary adjective; chapter-local link still allowed (STOP is soft)
    "verdeling",       # ordinary "verdeling" + law of RV
    "spectrum",
    "potentiaal",
    "uniform",         # uniform convergence via the longer phrase
    "gesloten",        # closed form / closed set / closed arc — too mixed
}

# Never linked anywhere (hard). Result-names that reach via \emph{}\index{}
# bypass NOT_A_TERM; English drops the same notions (see book4_en.py DROP).
DROP = {
    "Gibbs-fenomeen",
    "stelling van Korovkin",
    "formule van Jacobi",
    "limietformule van Gauss",
    "ongelijkheid van Hadamard",
    "min-max-stelling van Courant--Fischer",
    "storingsongelijkheden van Weyl",
    "scheidings- en vergelijkingsstellingen van Sturm",
    "Chinese reststelling",          # no " van " -> not filtered by NOT_A_TERM
    "totientfunctie van Euler",      # EN never cross-links
    "isoperimetrische ongelijkheid",
    "polarisatie-identiteit",
    "polarisatie",
    "Hessematrice",                  # harvest lands on Taylor thm; EN never links Hessian
    "puntsgewijs",                   # adverb; "puntsgewijze convergentie" keeps link
}

# Manual term -> label. Solid compounds + weekend-problem notions EN links +
# forms the harvest misses or pins wrong.
EXTRA = {
    # plurals / compounds
    "quotiëntringen":               "def:b2:structures:quotientring",
    "aftelbare verzamelingen":      "def:b2:structures:countable",
    "Fourierreeks":                 "def:b2:fourier:coefficients",
    "Fourierreeksen":               "def:b2:fourier:coefficients",
    "Dirichlet-kern":               "lem:b2:fourier:kernel",
    "Cesàro-sommeerbaar":           "thm:b2:series:abel",
    "Abel-sommeerbaar":             "thm:b2:series:abel",
    "Dunford-ontbinding":           "thm:b2:reduction:dunford",
    "Gauss-reductie":               "thm:b2:quadratic:gauss",
    "oppervlakte":                  "def:b2:surfaces:area",
    "elementair gebied":            "def:b2:multint:domain",
    "elementaire gebieden":         "def:b2:multint:domain",
    "Catalan-getallen":             "ex:b2:powerseries:catalan",
    "Catalangetallen":              "ex:b2:powerseries:catalan",
    "symmetrische bilineaire vorm": "def:b2:quadratic:def",
    "matrixexponentieel":           "ex:b2:nvs:matrixexp",
    "matrixexponentiaal":           "ex:b2:nvs:matrixexp",
    # EN targets that need explicit Dutch terms
    "voorwaardelijke waarschijnlijkheid": "def:b2:proba:conditional",
    "geparametriseerd oppervlak":   "def:b2:surfaces:param",
    "geparametriseerde oppervlakken": "def:b2:surfaces:param",
    "parameterintegraal":           "thm:b2:integration:continuity",
    "parameterintegralen":          "thm:b2:integration:continuity",
    "Bernsteinveeltermen":          "thm:b2:funcseq:weierstrass",
    "Beta-functie":                 "pb:b2:integration:1",
    "vertakkingsproces":            "pb:b2:genfun:1",
    "Rayleigh-quotiënt":            "pb:b2:hermitian:1",
    "Rayleigh-quotiënten":          "pb:b2:hermitian:1",
    "polaire ontbinding":           "pb:b2:quadratic:1",
    "Cholesky-factorisatie":        "pb:b2:quadratic:1",
    "resonantie":                   "pb:b2:diffeq:1",
    "toevalswandeling":             "pb:b2:proba:1",
    "eenvoudige toevalswandeling":  "pb:b2:proba:1",
    "kwadriek":                     "pb:b2:surfaces:1",
    "kwadrieken":                   "pb:b2:surfaces:1",
    "omhullende":                   "pb:b2:curves:1",
    "omhullenden":                  "pb:b2:curves:1",
    "astroïde":                     "pb:b2:curves:1",
    "nefroïde":                     "pb:b2:curves:1",
    "formule van Green":            "pb:b2:multint:1",
}

NO_CAPITAL = set()

DERIVED = {}

PRIMARY_OK = set()

AMBIG_POLICY = "drop"          # university convention (books 3, 4, 5)

# Fixed Dutch phrases where a defined word carries another sense.
# Spaces as \s+; never consume "$".
EXTRA_PROTECT = [
    # closed form / expression (not closed 1-form of ch. 20)
    r'gesloten\s+vorm', r'gesloten\s+uitdrukking(?:en)?',
    r'gesloten\s+formule', r'in\s+gesloten',
    # uniform law / uniform continuity (not uniform convergence)
    r'uniform\s+(?:verdeeld|gekozen|toevallig|continu)',
    r'uniform\)',
    # differential as subject adjective
    r'differentiaal\s*(?:rekening|vergelijking(?:en)?|meetkunde|systeem)',
    # independent of $n$
    r'onafhankelijk(?=\s+van\s+\$)',
    # convex function vs convex set
    r'convex\s+(?:functie|functies|kromme)',
    # open problem
    r'open\s+probleem', r'open\s+de\s+',
    # law of large numbers
    r'(?:sterke|zwakke)\s+wet',
    r'wet\s+van\s+de\s+grote\s+aantallen',
    r'wet\s+van\s+zeldzame\s+gebeurtenissen',
    # cyclic invariance of the trace
    r'cyclische?\s+invariantie',
    # order / reading order
    r'orde\s+relaties', r'leesvolgorde', r'sommatievolgorde',
]
