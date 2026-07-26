"""Book 3 -- nl. Curation only; the rules live in tools/termlink/.

The traps are Dutch, not the English or French ones. Dutch is SPARED the French
"premier" collision (the prime is priemgetal/priem, the ordinal is eerste --
different words), but has its own: "argument" is the argument of a complex number
*and* "hetzelfde argument" (the same reasoning), "direct(e)" is the direct sum
*and* "een directe berekening / een directe isometrie", "eindig(e)" is the finite
set *and* "een eindige som / een eindig aantal", "gelijkvormig" is matrix
similarity *and* ordinary "similar", "algebraïsch" is the algebraic number *and*
"een algebraïsche structuur", "toegevoegde" is the complex conjugate *and* an
adjoint, "symmetrie" is the linear involution *and* "door symmetrie", "gesloten"
is the closed set *and* "in gesloten vorm" (closed form). Each word was read in
context in parts/bachelor-1/nl/ before being kept or dropped.

The other half of the work is the reverse: tools/term_config/lang_nl.py sets
DERIVE = False and WORD_TAIL = (?:e?[ns])?, which spells "", "e", "n", "s", "en",
"es" -- but not the -aar/-baar adjectives nor the compound. So the bare adjective
a definition emphasises through an inline-math compound ("continu in $x_0 \\in
I$", "afleidbaar in $x_0 \\in I$") has to be declared by hand in EXTRA, and Dutch
solid compounds (deelruimte, eenheidswortel) link only where declared.
"""

# "een stelling is geen begrip": the default NOT_A_TERM keywords are English
# ("theorem", "formula", "inequality", "law", ...), so the harvester filters
# "Rolle's theorem" out of the English book but lets the Dutch "stelling van
# Rolle", "formule van Leibniz", "regel van Cramer", "wetten van De Morgan",
# "ongelijkheid van Ptolemaeus" through -- 18 result-names English never links.
# Filtering on the Dutch keywords restores parity.
# NB substring match (`k in d.lower()`): use the "X van Y" PHRASE forms, not the
# bare nouns. Dutch writes its notions as solid compounds -- kettingregel,
# quotiëntcriterium, machtsregels, hoofdstelling van de integraalrekening,
# Riemannsommen -- and a bare "regel"/"criterium"/"stelling" would filter those
# too. A named result is always "stelling/formule/regel/ongelijkheid VAN <name>";
# a compound never contains " van ".
NOT_A_TERM = ("stelling van", "formule van", "ongelijkheid van", "regel van",
              "wet van", "wetten van", "lemma van", "identiteit van",
              "criterium van", "principe van", "paradox van")

# Ordinary Dutch, or a word whose sense here is not the definition's -- but STILL
# linked inside the chapter that pins it down (STOP is soft).
STOP = {
    # ch. 2 = the finite set. Elsewhere "eindige som", "eindige familie", "een
    # eindig aantal punten", "eindige vereniging" -- and "eindige dimensie",
    # "eindigdimensionaal" are terms of their own that keep their links.
    "eindig", "eindige",
    # ch. 3 = the complex conjugate. Also the adjoint / "de toegevoegde
    # matrix" in later chapters -- a different object.
    "toegevoegde", "toegevoegden",
}

# Never linked anywhere.
DROP = {
    # "hetzelfde argument toont", "een diagonaalargument", "compactheids-
    # argumenten" -- the reasoning word, not the argument of a complex number.
    "argument", "argumenten",
    # "een directe berekening", "een directe isometrie" ($\\det = 1$, ch. 23),
    # "direct gevolg". The notion that earns a link is "directe som", a term of
    # its own that wins by being longer.
    "direct", "directe",
    # "door symmetrie", "een symmetrie-argument" -- the register, not the linear
    # involution $s^2 = \\mathrm{id}$ of ch. 20. "symmetrische groep" is a term
    # of its own and keeps its link.
    "symmetrie", "symmetrieën",
    # "een algebraïsche structuur / vorm / berekening" -- not the algebraic
    # number. "algebraïsch getal" is a term of its own.
    "algebraïsch", "algebraïsche",
    # ordinary "similar": "een gelijkvormige berekening", "op gelijkvormige
    # wijze", "zelfgelijkvormigheid". "gelijkvormige matrices" keeps its link.
    "gelijkvormig", "gelijkvormige", "gelijkvormigheid", "gelijkvormigheden",
    # --- names of results reached through \\emph{...}\\index{...}, not definitions.
    # (NOT_A_TERM only filters the index-ONLY path; an \\emph{...}\\index{...}
    # pair bypasses it, so these must be dropped by hand -- as book3_en.py drops
    # "Ptolemy's inequality", "De Morgan's laws", "Cauchy's functional equation".)
    "de formule van Legendre", "formule van Legendre",
    "de stelling van Kummer", "stelling van Kummer",
    "alternerende reeks schatting",
    "functievergelijking van Cauchy", "functievergelijking",
    "ongelijkheid van Ptolemaeus", "stelling van Napoleon",
    "stelling van van Schooten", "wetten van De Morgan",
    "Chinese reststelling",              # "reststelling" has no " van " -> not filtered
    "aanvullingsstelling voor bases",    # a statement title, not a defined term
    # "bewerking" is the binary operation of ch. 7, but far more often the
    # ordinary word ("een bewerking uitvoeren", "elementaire bewerkingen"). Its
    # English twin "law of composition" is specific and never over-links; the
    # bare Dutch word would. Match English: no link.
    "bewerking", "bewerkingen",
}

# Terms the harvester misses, and the forms DERIVE = False never generates.
EXTRA = {
    # the definition emphasises an inline-math compound ("\\emph{continu in $x_0
    # \\in I$}", "\\emph{afleidbaar in $x_0 \\in I$}"), pure math that never
    # matches; the bare adjective is what the other chapters actually write.
    "continu":        "def:b1:continuity:continuous",   # + continue via WORD_TAIL
    "afleidbaar":     "def:b1:derivative:def",
    "afleidbaarheid": "def:b1:derivative:def",
    # \\emph{deelt} and \\index{deelbaarheid} are separated by "het getal $a$
    # (genoteerd $b \\mid a$)", so the verb is never harvested; only the noun is.
    "deelt":     "def:b1:arith:divides",
    "deelbaar":  "def:b1:arith:divides",

    # Dutch solid/hyphenated compounds the harvester's index-only path skips
    # (it requires a SPACE in the term: `" " not in d -> continue`). English
    # links each of these through its spaced term ("Chebyshev polynomials",
    # "Riemann sums", "Gaussian elimination"); Dutch must declare them by hand.
    "Tsjebysjev-veelterm":     "pb:b1:poly:1",
    "Tsjebysjev-veeltermen":   "pb:b1:poly:1",
    "Vandermonde-determinant": "ex:b1:det:vandermonde",
    "Lagrange-interpolatie":   "thm:b1:poly:lagrange",
    "Riemannsom":              "thm:b1:integration:riemann",
    "Riemannsommen":           "thm:b1:integration:riemann",
    "Riemann-reeks":           "thm:b1:series:riemann",
    "quotiëntcriterium":       "thm:b1:series:ratio",
    "priemontbinding":         "thm:b1:arith:fta",
    "cofactorontwikkeling":    "thm:b1:det:cofactor",
    "torenwet":                "pb:b1:findim:1",
    "diëdergroep":             "pb:b1:euclid:1",
    "glijspiegeling":          "pb:b1:euclid:1",
    "Cantorverzameling":       "pb:b1:topology:1",
    "Gauss-eliminatie":        "met:b1:det:gauss",
    "zadelpunt":               "met:b1:multivar:monge",
    "Cauchy-determinant":      "pb:b1:det:1",
    "Hilbert-matrix":          "pb:b1:det:1",
    # the short form "rij-operaties" (5 uses) is what the proofs write; only the
    # full "elementaire rij-operaties" is harvested, and it sits in its own
    # method (a self-link, excluded). English catches it via "row operations".
    "rij-operatie":            "met:b1:matrices:gauss",
    "rij-operaties":           "met:b1:matrices:gauss",
    # the NL rendering of "growth comparison"; used only in ch. 4 (no clash with
    # a growth ODE), harvested from an index-only entry the space rule skips.
    "groeivergelijking":       "prop:b1:functions:powerrules",
    # \\index{Euler's constant} sits before the problem that defines gamma, so
    # the nearest example (odd-telescoping) is the wrong target -- as in
    # book3_en.py, point it at the problem.
    "constante van Euler":     "pb:b1:series:1",

    # ---------------------------------------------------------------- #
    # Coverage parity with EN.                                          #
    # ---------------------------------------------------------------- #
    # Three shared-rule gaps cost the Dutch edition ~440 links that the
    # English edition gets for free. None of them may be fixed in
    # tools/term_config/lang_nl.py (that would silently re-link all five
    # books), so the forms are declared here, each read in context first.
    #
    #   (a) WORD_TAIL = (?:e?[ns])? spells -n/-s/-en/-es but NOT the bare
    #       attributive -e. English links "continuous" in every position;
    #       Dutch loses every "continue functie".
    #   (b) NO_TAIL_END = ("s", ...) in tools/termlink/morphology.py gives a
    #       term ending in -s no tail at all, so "reeks" never matches
    #       "reeksen" and "basis" never matches "bases"; and Dutch plurals
    #       are irregular far more often than English ones (interval ->
    #       intervallen, lichaam -> lichamen, spoor -> sporen, supremum ->
    #       suprema, isometrie -> isometrieën).
    #   (c) the harvester's \\emph leaf test compares the stripped term with
    #       the label leaf, so "orthogonaal" vs leaf "orthogonal" fails and
    #       the term is never harvested at all -- EN 55 links, NL 3.

    # (a) attributive -e adjectives
    "continue":           "def:b1:continuity:continuous",
    "lineaire":           "def:b1:linmaps:def",
    "vrije":              "def:b1:vspaces:free",
    "dichte":             "def:b1:topology:dense",
    "monische":           "def:b1:poly:def",
    "kritieke":           "thm:b1:multivar:critical",
    "complementaire":     "def:b1:vspaces:sum",
    "transcendente":      "pb:b1:logic:1",
    "eindigdimensionale": "def:b1:findim:def",
    "afleidbare":         "def:b1:derivative:def",
    "bijectieve":         "def:b1:logic:inj",
    "injectieve":         "def:b1:logic:inj",
    "surjectieve":        "def:b1:logic:inj",

    # (b) plurals the tail cannot reach
    "reeksen":       "def:b1:series:def",
    "bases":         "def:b1:vspaces:free",
    "intervallen":   "prop:b1:reals:intervals",
    "uitspraken":    "def:b1:logic:statement",
    "integralen":    "thm:b1:integration:def",
    "isometrieën":   "def:b1:euclid:isometry",
    "priemgetallen": "def:b1:arith:prime",
    "lichamen":      "def:b1:structures:field",
    "hypervlakken":  "def:b1:linmaps:forms",
    "sporen":        "def:b1:matrices:transpose",
    "originelen":    "def:b1:logic:map",
    "suprema":       "def:b1:reals:bounds",
    "infima":        "def:b1:reals:bounds",
    "bovengrenzen":  "def:b1:reals:bounds",
    "ondergrenzen":  "def:b1:reals:bounds",
    # the plural phrases too, so that the longest-first rule keeps them on
    # their own theorem instead of dropping them onto "reeksen".
    "alternerende reeksen":   "thm:b1:series:alternating",
    "meetkundige reeksen":    "ex:b1:series:geometric",
    "telescoperende reeksen": "prop:b1:series:first",
    "Riemann-reeksen":        "thm:b1:series:riemann",

    # (c) never harvested: the \\emph leaf test rejects the Dutch spelling
    "orthogonaal":     "def:b1:euclid:orthogonal",
    "orthogonale":     "def:b1:euclid:orthogonal",
    "orthonormale":    "def:b1:euclid:orthogonal",

    # Dutch solid compounds where English uses a spaced index term the
    # harvester accepts ("normal equations", "regression line", "prime
    # divisor"); the index-only path requires a space, so Dutch loses them.
    "normaalvergelijking":   "pb:b1:multivar:1",
    "normaalvergelijkingen": "pb:b1:multivar:1",
    "regressierechte":       "pb:b1:multivar:1",
    "priemdeler":            "def:b1:arith:prime",

    # WRONG-SENSE REPAIR. "inwendige" (the interior of ch. 12) was landing on
    # the nine "inwendige product(en)" of ch. 23/25 -- the inner product, a
    # different object. Declaring the two-word phrase lets longest-first take
    # it to the euclidean definition instead. ("inwendig product", singular
    # attributive, is already harvested and unaffected.)
    "inwendige product":     "def:b1:euclid:def",
    # and the neuter predicative form of the interior itself ("$x_0$ is
    # inwendig aan $I$", "een inwendig punt", "een inwendig extremum"), which
    # WORD_TAIL cannot reach from the harvested "inwendige". The phrase above
    # is longer, so "inwendig product" still wins where it occurs.
    "inwendig":              "def:b1:topology:closure",
}

# Forms deliberately NOT declared, after reading them in context:
#
#   euclidische   -- "euclidische ruimte" (ch. 23) but also "euclidische
#                    deling" (ch. 6/8, six uses), "euclidische norm",
#                    "euclidische meetkunde". Two senses, both live outside
#                    ch. 23; the same call Book 5 made.
#   vrijheid, volledigheid, orthogonaliteit, lineariteit, convexiteit,
#   injectiviteit, surjectiviteit, transcendentie, geslotenheid
#                 -- the -heid/-iteit abstract nouns. English does NOT link
#                    theirs: lang_en.py DERIVE spells -ally/-ously/-ability/
#                    -ely/-ce/-ly but never -ity, and the book contains 0
#                    links on "linearity", "convexity", "injectivity",
#                    "surjectivity", "orthogonality", "completeness". Adding
#                    them in Dutch would put the NL edition ~110 links AHEAD
#                    of EN on those targets. ("continuïteit", "dichtheid",
#                    "afleidbaarheid", "deelbaarheid" stay linked: English
#                    links "continuity", "density", "differentiability",
#                    "divisibility", which are harvested or derived there.)
#   bijectie, injectie, surjectie (and plurals)
#                 -- same reason: EN links only the adjectives
#                    (injective/surjective/bijective), never the nouns
#                    "bijection"/"injection".
#   dicht bij     -- protected below rather than dropped: "dicht" itself is a
#                    good term, only the collocation is ordinary Dutch.

NO_CAPITAL = set()   # Dutch imperatives use the stem ("Ontbind", "Bereken"),
                     # which never collides with the infinitive/adjective terms

DERIVED = {}

PRIMARY_OK = set()

AMBIG_POLICY = "drop"          # the university convention (books 3, 4, 5)

# Fixed Dutch phrases that contain a linkable word in another sense.
# Every space is \s+ (sources wrap at ~72 cols); no pattern may CONSUME a "$"
# (that inverts inline-math masking for the rest of the file).
EXTRA_PROTECT = [
    # "gesloten": the closed set, except "in gesloten vorm" / "een gesloten
    # uitdrukking" (closed form). "gesloten verzameling" keeps its link.
    r'gesloten\s+vorm', r'gesloten\s+uitdrukking(?:en)?',
    r'geen\s+gesloten',
    # WRONG-SENSE REPAIR. "dicht" is the dense subset of ch. 12, but "dicht
    # bij" is ordinary "close to" -- seven links pointed at the wrong notion
    # (ch. 12, 14, 24 and two solutions). English is spared: it writes
    # "close to", not "dense to". Same protection as book5_nl.py.
    r'dicht\s+bij',
]
