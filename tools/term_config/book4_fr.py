"""Book 4 -- fr. Curation only; the rules live in tools/termlink/.

Minimal starting point: harvest the French terms, then curate against the
English link targets (the parity gate). tools/term_config/lang_fr.py sets
DERIVE = False and WORD_TAIL = (?:e?s)? -- it spells "", "s", "es" but NOT the
feminine singular "e" nor the -aux/-if masculines -- so every real French
variant is declared by hand in DERIVED/EXTRA (see book3_fr.py).
"""

# The default NOT_A_TERM keywords are English ("theorem", "lemma", "inequality",
# "rule", ...), so the harvester filters "Parseval's theorem" out of the English
# book but lets the French "identité de Parseval", "règle de la chaîne",
# "théorème spectral", "inégalité de Bessel" through -- ~25 result-names English
# never links. Filtering on the French heads restores parity. (Bare "loi" is the
# distribution/law DEFINITION and is kept; no "loi de X" result-name is harvested.
# "identité de polarisation" is filtered here but its target def:b2:quadratic:def
# stays, linked through "forme quadratique".)
NOT_A_TERM = ("théorème", "lemme", "inégalité", "formule", "critère",
              "principe", "identité", "règle", "paradoxe", "problème")

STOP = set()

# French result-names / weekend-problem notions English does NOT link, so they
# must be dropped for parity with the English target set. Each reaches the
# harvester through an \emph{...}\index{...} pair (which bypasses NOT_A_TERM) or
# has no English \emph\index twin at all.
DROP = {
    "phénomène de Gibbs",     # ex:b2:fourier:zetafourodd -- never linked in EN
    "point central",          # pb:b2:affine:1 -- EN "centerpoint" not harvested
    "formule de Jacobi",      # pb:b2:diffcalc:1 -- a named formula (EN filters it)
    "théorème de Korovkin",   # pb:b2:funcseq:1 -- a named theorem (EN filters it)
    "indicatrice d'Euler",    # prop:b2:structures:cyclic -- EN "Euler's totient
                              # function" exists but is never cross-linked
    # bare "signature" is the permutation signature (ch. 1) AND the signature of
    # a quadratic form (ch. 12): ambiguous, and English never links the bare word
    # ("signature of a quadratic form" is a longer, different term).
    "signature",
}

EXTRA = {
    # bare "courbure" is the curvature of the plane Frenet theorem, exactly as EN
    # links bare "curvature" -> thm:b2:curves:frenet2d ("centre/rayon de courbure"
    # are longer and keep their own def:b2:curves:curvature link). The FR harvest
    # drops it as ambiguous; EXTRA forces the English behaviour.
    "courbure":          "thm:b2:curves:frenet2d",
    # the definition writes the singular "anneau quotient" (a self-link, excluded)
    # while the chapter intro writes the plural "anneaux quotients" -- the only
    # cross-occurrence, which the singular term does not match (anneau != anneaux).
    "anneaux quotients": "def:b2:structures:quotientring",
}
NO_CAPITAL = set()
DERIVED = {}
PRIMARY_OK = set()
AMBIG_POLICY = "drop"          # the university convention (books 3, 4, 5)
EXTRA_PROTECT = []
