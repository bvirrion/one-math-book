"""Book 5 -- fr. Curation only; the rules live in tools/termlink/.

Harvest French terms, then curate against English link targets (parity gate).
Do not edit book5_en.py (golden fixture).
"""

NOT_A_TERM = ("théorème", "lemme", "inégalité", "formule", "critère",
              "principe", "identité", "règle", "paradoxe", "problème")

STOP = set()

# Result-names / weekend notions English never cross-links (parity).
DROP = {
    "convergence en loi",          # EN does not use this bare target as def:b3:clt:cid
    "gaussienne", "gaussiennes", "Gaussienne", "sous-gaussiennes",
    "log-convexe", "log-convexes",
    "rayon numérique",
    "extension cyclotomique",
    "élément primitif",
    "résolubilité par radicaux",
    "intégrales à paramètre",
    "volume de la boule unité",
    "volume de la\nboule unité",
}

EXTRA = {
    # EN links "boundary" -> def:b3:forms:boundary
    "bord": "def:b3:forms:boundary",
    # EN "tower law"
    "loi de la tour": "thm:b3:galois:tower",
    "tour des degrés": "thm:b3:galois:tower",
    # EN "orthogonal complement" -> orthogonal decomposition thm
    "complémentaire orthogonal": "thm:b3:hilbert:decomposition",
    "complémentaires orthogonaux": "thm:b3:hilbert:decomposition",
    "décomposition orthogonale": "thm:b3:hilbert:decomposition",
    "projections orthogonales": "thm:b3:hilbert:decomposition",
}

NO_CAPITAL = set()
DERIVED = {}
PRIMARY_OK = set()
AMBIG_POLICY = "drop"
EXTRA_PROTECT = []
