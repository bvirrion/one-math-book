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
    # sense changes by chapter / ordinary language
    "alternerend",     # form (ch.2) vs series
    "signatuur",       # permutation (ch.1) vs quadratic form (ch.12); EN never links bare
    "exact",           # exact form vs "exacte waarde"
    "wet",             # law of RV vs ordinary "wet"; EN protects "(strong|weak) law"
    "affien",          # bare adjective; the "affiene ..." forms are in EXTRA below
    "cyclisch",        # cyclic group vs cyclic order / cyclic product
    "congruentie",     # matrix congruence vs ordinary congruence
    "normaal",         # normal convergence vs normal endomorphism / principal normal
    "spectrum",
    "potentiaal",
    "uniform",         # bare adverb: already at English's count (NL 47 / EN 43);
                       # the attributive "uniforme" is pinned in EXTRA instead
    "gesloten",        # closed form / closed set / closed arc — too mixed
    # Removed from STOP after a per-target density audit against English, which
    # links all four book-wide (EN: open 80, law/distribution 87, absolutely 52,
    # length 42). Their ordinary-language uses are guarded by the EXTRA_PROTECT
    # look-aheads at the bottom of this file, exactly as book4_en.py guards
    # "paths of length", "run length", "uniformly at random":
    #   open      -- every use in this book is the topological one
    #   verdeling -- always the law of a random variable (chs. 21-23)
    #   absoluut  -- "absolute convergentie" is the notion, and it is the only use
    #   lengte    -- arc length from ch. 18 on; the ch. 21 path lengths are protected
    #   duale     -- the dual space/basis, chs. 2 and 8 only (pinned in EXTRA)
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
    "hessiaan",                      # ditto: EN term is the 2-word "Hessian matrix",
    "hessianen",                     # which never matches; keeps omterm parity with EN
    "puntsgewijs",                   # adverb; "puntsgewijze convergentie" keeps link
}

# Manual term -> label. Solid compounds + weekend-problem notions EN links +
# forms the harvest misses or pins wrong.
EXTRA = {
    # Dutch attributive -e forms and abstract nouns: WORD_TAIL is (?:e?[ns])?,
    # so the bare "-e" adjective and the "-heid/-iteit" noun never match on
    # their own. English gets them from DERIVE (continuity/continuously,
    # compactness, countable) and links them book-wide; declaring them here
    # keeps the Dutch reader's link coverage at the English level.
    "continue":                     "def:b2:metric:continuity",
    "continuïteit":                 "def:b2:metric:continuity",
    "compacte":                     "def:b2:metric:compact",
    "compactheid":                  "def:b2:metric:compact",
    "aftelbare":                    "def:b2:structures:countable",
    "aftelbaarheid":                "def:b2:structures:countable",
    "convexe":                      "def:b2:affine:convex",
    "affiene":                      "def:b2:affine:subspace",
    "affiene deelruimte":           "def:b2:affine:subspace",
    "affiene deelruimten":          "def:b2:affine:subspace",
    "hermitische":                  "def:b2:hermitian:adjoint",
    "unitaire":                     "def:b2:hermitian:adjoint",
    "antihermitisch":               "def:b2:hermitian:adjoint",
    "antihermitische":              "def:b2:hermitian:adjoint",
    "symmetrische":                 "def:b2:quadratic:adjoint",
    "zelftoegevoegd":               "def:b2:quadratic:adjoint",
    "zelftoegevoegde":              "def:b2:quadratic:adjoint",
    "diagonaliseerbare":            "def:b2:reduction:diag",
    "sommeerbare":                  "def:b2:series:summable",
    "sommeerbaarheid":              "def:b2:series:summable",
    "volledigheid":                 "def:b2:metric:complete",
    "samenhang":                    "def:b2:metric:connected",
    "samenhangende":                "def:b2:metric:connected",
    "differentieerbaarheid":        "def:b2:diffcalc:differential",
    "puntsgewijze":                 "def:b2:funcseq:def",
    "uniforme":                     "def:b2:funcseq:def",
    "absolute convergentie":        "def:b2:series:def",
    # the wrapper never links a term before the chapter that defines it, so
    # these two reach only chs. 21-23 (the probabilistic sense) and never the
    # "lineair/affien onafhankelijk" of chs. 1-20 -- the same guard that lets
    # English link "independent" 117 times
    "onafhankelijke":               "def:b2:proba:independence",
    "onafhankelijkheid":            "def:b2:proba:independence",
    "voortgebracht":                "def:b2:structures:generated",
    "voortgebrachte":               "def:b2:structures:generated",
    "barycentra":                   "def:b2:affine:barycenter",
    "oppervlakten":                 "def:b2:surfaces:area",
    "duale":                        "def:b2:linalg:dual",
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
    # uniform law / uniform continuity (not uniform convergence). Look-ahead:
    # the noun after it stays linkable ("uniforme \omterm{...}{verdeling}").
    r'uniform(?:e)?(?=\s+(?:verdeeld|gekozen|toevallig|continu\w*|gewicht\w*|'
    r'maat|kans|letter\w*|rangschikking\w*|steekproe\w+|verdeling\w*|'
    r'som|sommen|dichtheid|oppervlakte\w*))',
    r'uniform\)',
    # arc length (ch. 18) vs the length of a run / of a lattice path (ch. 21) --
    # book4_en.py protects the same three phrases
    r'pad(?:en)?\s+van\s+lengte', r'paden\s+van\s+lengte',
    r'lengte\s+van\s+de\s+reeks', r'tekst\s+van\s+elke\s+lengte',
    # the mirrored event of a random walk, not a symmetric endomorphism
    r'symmetrische?(?=\s+gebeurtenis)',
    # differential as subject adjective
    r'differentiaal\s*(?:rekening|vergelijking(?:en)?|meetkunde|systeem)',
    # independent of $n$
    r'onafhankelijk(?=\s+van\s+\$)',
    # convex function vs convex set (also the attributive "convexe")
    r'convexe?\s+(?:functie|functies|kromme|krommen|afbeelding\w*)',
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
