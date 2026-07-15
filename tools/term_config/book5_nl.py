"""Book 5 -- nl. Curation only; the rules live in tools/termlink/.

Phrase NOT_A_TERM only. Solid compounds in EXTRA. Parity with EN targets.
Do not edit book5_en.py (golden fixture).
"""

NOT_A_TERM = ("stelling van", "formule van", "ongelijkheid van", "regel van",
              "wet van", "wetten van", "lemma van", "identiteit van",
              "criterium van", "principe van", "paradox van")

STOP = {
    "equivalent", "algebra", "convergeert", "open", "gesloten",
    "normaal", "continu", "exact", "compact", "basis", "vrij",
    "graad", "wet", "product", "quotiënt",
}

DROP = {
    # EN never links these as standalone targets in the same way
    "liniaal en passer", "liniaal en\npasser",
    "Gaussische", "Gaussischen", "Sub-Gaussische", "niet-Gaussische",
    "standaard-Gaussische", "standaard-Gaussischen",
    "centrale limietstelling",           # thm name; EN links differently
    "gedomineerde convergentiestelling",
    "lemma's van Borel--Cantelli",
}

EXTRA = {
    # EN target parity: compounds / phrases harvest misses
    "klassevergelijking":           "cor:b3:groups:classeq",
    "rand":                         "def:b3:forms:boundary",
    "uitwendig product":            "def:b3:forms:wedge",
    "uitwendige product":           "def:b3:forms:wedge",
    "poolcoördinaten":              "ex:b3:product:polar",
    "Hilbert--Schmidt-operator":    "ex:b3:spectral:examples",
    "topologen-sinus":              "ex:b3:topology:sinecurve",
    "topologen-sinuskromme":        "ex:b3:topology:sinecurve",
    "sinuskromme van de topoloog":  "ex:b3:topology:sinecurve",
    "Neumannreeks":                 "prop:b3:banach:neumann",
    "direct product":               "prop:b3:groups:direct",
    "directe producten":            "prop:b3:groups:direct",
    "Cauchy--Riemannvergelijkingen": "prop:b3:holomorphic:cauchyriemann",
    "Blaschke-factor":              "thm:b3:conformal:autdisc",
    "Poissonkern":                  "thm:b3:conformal:poisson",
    "torenwet":                     "thm:b3:galois:tower",
    "toren van graden":             "thm:b3:galois:tower",
    "Cauchy-schattingen":           "thm:b3:holomorphic:analytic",
    "Lyapunov-functie":             "thm:b3:ode:lyapunov",
    "Lyapunov-functies":            "thm:b3:ode:lyapunov",
    "matrixexponentiaal":           "thm:b3:ode:matrixexp",
    "matrixexponentieel":           "thm:b3:ode:matrixexp",
    "nul-één-wet":                  "thm:b3:probability:zeroone",
    "nul--één-wet":                 "thm:b3:probability:zeroone",
    "productmaat":                  "thm:b3:product:existence",
    "orthogonaliteit van karakters": "thm:b3:representations:orthogonality",
    "orthogonaliteitsrelaties":      "thm:b3:representations:orthogonality",
    "kolomorthogonaliteit":          "thm:b3:representations:orthogonality",

    "Laurentreeks":                 "thm:b3:residues:laurent",
    "orthogonaal complement":       "thm:b3:hilbert:decomposition",
    "orthogonale complement":       "thm:b3:hilbert:decomposition",
}

NO_CAPITAL = set()
DERIVED = {}
PRIMARY_OK = set()
AMBIG_POLICY = "drop"
EXTRA_PROTECT = [
    r'gesloten\s+vorm', r'gesloten\s+uitdrukking(?:en)?',
    r'onafhankelijk(?=\s+van\s+\$)',
]
