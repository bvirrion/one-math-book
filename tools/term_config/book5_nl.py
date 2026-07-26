"""Book 5 -- nl. Curation only; the rules live in tools/termlink/.

Phrase NOT_A_TERM only. Solid compounds in EXTRA. Parity with EN targets.
Do not edit book5_en.py (golden fixture).
"""

NOT_A_TERM = ("stelling van", "formule van", "ongelijkheid van", "regel van",
              "wet van", "wetten van", "lemma van", "identiteit van",
              "criterium van", "principe van", "paradox van")

STOP = {
    "equivalent", "algebra", "convergeert", "open", "gesloten",
    "normaal", "exact", "compact", "basis", "vrij",
    "graad", "wet", "product", "quotiënt",
    # "continu" was stoplisted here by the previous edition; EN does not stop
    # "continuous", and Dutch "continu" has no ordinary sense in this book
    # (it is never the adverb "non-stop"), so it is a global term again.
    # EN stops "simple": nl "enkelvoudig" also reads as a simple zero/pole
    # and inside "enkelvoudig samenhangend", none of them a simple group
    "enkelvoudig",
    # EN stops "index": nl "index" is the group index, the index of a
    # stable law and a summation index, not the winding number
    "index",
    # EN stops "stable": nl "stabiel" also means stable under sums and
    # strictly stable of index alpha, not Lyapunov-stable
    "stabiel",
    # EN stops "content": nl "inhoud" is ordinary language (the content
    # of a problem, of a statement) outside the ring chapter
    "inhoud",
    # EN stops "separable": a separable field extension (ch. 4) and a
    # separable Hilbert/Banach space (ch. 7, 8, 13, 15) are different
    # notions, and the harvest only knows the first
    "separabel",
    # EN stops "maximal": outside the ring chapters nl "maximaal" is the
    # maximal solution of an ODE, the maximum principle, a maximal element
    "maximaal",
}

DROP = {
    # EN never links these as standalone targets in the same way
    "liniaal en passer", "liniaal en\npasser",
    "Gaussische", "Gaussischen", "Sub-Gaussische", "niet-Gaussische",
    "standaard-Gaussische", "standaard-Gaussischen",
    "centrale limietstelling",           # thm name; EN links differently
    "gedomineerde convergentiestelling",
    "lemma's van Borel--Cantelli",
    # "beeldmaat" is introduced inside an exercise; the harvest attaches it
    # to the preceding theorem (the volume of the unit ball) -- wrong sense,
    # and EN links its "pushforward measure" nowhere either
    "beeldmaat",
}

EXTRA = {
    # EN target parity: compounds / phrases harvest misses
    "klassevergelijking":           "cor:b3:groups:classeq",
    "rand":                         "def:b3:forms:boundary",
    "uitwendig product":            "def:b3:forms:wedge",
    "uitwendige product":           "def:b3:forms:wedge",
    "poolcoördinaten":              "ex:b3:product:polar",
    "hilbert-schmidtoperator":      "ex:b3:spectral:examples",
    "hilbert-schmidtoperatoren":    "ex:b3:spectral:examples",
    # EN target parity: solid compounds the index harvest skips (no space)
    "Galoiscorrespondentie":        "thm:b3:galois:fundamental",
    "galoiscorrespondentie":        "thm:b3:galois:fundamental",
    "jordanvorm":                   "thm:b3:modules:jordan",
    "jordanvormen":                 "thm:b3:modules:jordan",
    "rijcompactheid":               "thm:b3:topology:metriccompact",
    # kept linkable after "enkelvoudig" was stoplisted above
    "enkelvoudig samenhangende":    "def:b3:conformal:simplyconnected",
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
    # spellings as used in the nl text (solid/hyphenated compounds)
    "lyapunovfunctie":              "thm:b3:ode:lyapunov",
    "lyapunovfuncties":             "thm:b3:ode:lyapunov",
    "matrixexponentiële":           "thm:b3:ode:matrixexp",
    "nul-een-wet":                  "thm:b3:probability:zeroone",
    "productmaat":                  "thm:b3:product:existence",
    "orthogonaliteit van karakters": "thm:b3:representations:orthogonality",
    "orthogonaliteitsrelaties":      "thm:b3:representations:orthogonality",
    "kolomorthogonaliteit":          "thm:b3:representations:orthogonality",

    "laurentreeks":                 "thm:b3:residues:laurent",
    "laurentreeksen":               "thm:b3:residues:laurent",
    "orthogonaal complement":       "thm:b3:hilbert:decomposition",
    "orthogonale complement":       "thm:b3:hilbert:decomposition",

    # ---------------------------------------------------------------------
    # Coverage parity with EN. The shared Dutch morphology (lang_nl.py,
    # WORD_TAIL = (?:e?[ns])?) matches plurals but never the attributive
    # adjective in -e ("meetbare functie") nor the derived noun in
    # -heid/-iteit ("meetbaarheid"), while English reaches its equivalents
    # through DERIVED (measurable -> measurability). Every form below was
    # read in context first; forms whose sense drifts outside their own
    # chapter are listed in the comment block at the end instead.
    "continue":                     "def:b3:topology:continuity",
    "continuïteit":                 "def:b3:topology:continuity",
    "homeomorf":                    "def:b3:topology:continuity",
    "homeomorfe":                   "def:b3:topology:continuity",
    "compacte":                     "def:b3:topology:compact",
    "compactheid":                  "def:b3:topology:compact",
    "gaussische":                   "def:b3:clt:gaussianvector",
    "volledigheid":                 "def:b3:complete:complete",
    "meetbare":                     "def:b3:lebesgue:measurable",
    "meetbaarheid":                 "def:b3:lebesgue:measurable",
    "samenhangende":                "def:b3:topology:connected",
    "samenhang":                    "def:b3:topology:connected",
    "wegsamenhangende":             "def:b3:topology:pathconnected",
    "holomorfe":                    "def:b3:holomorphic:holo",
    "holomorfie":                   "def:b3:holomorphic:holo",
    "onafhankelijke":               "def:b3:probability:independence",
    "dichte":                       "def:b3:topology:interior",
    "algebraïsche":                 "def:b3:galois:algebraic",
    "banen":                        "def:b3:groups:action",
    "idealen":                      "def:b3:rings:ideal",
    "integreerbare":                "def:b3:lebesgue:l1",
    "integreerbaarheid":            "def:b3:lebesgue:l1",
    "conforme":                     "def:b3:conformal:conformal",
    "torsievrij":                   "def:b3:modules:torsion",
    "maten":                        "def:b3:measure:measure",
    "radicaal":                     "def:b3:galois:radical",
    "radicale":                     "def:b3:galois:radical",
    "oplosbaarheid":                "def:b3:groups:derived",
    "zelftoegevoegde":              "def:b3:spectral:selfadjoint",
    "zelftoegevoegdheid":           "def:b3:spectral:selfadjoint",
    "equicontinue":                 "def:b3:complete:equicontinuous",
    "hausdorffruimte":              "def:b3:topology:hausdorff",
    "randen":                       "def:b3:forms:boundary",
    "magere":                       "rem:b3:complete:meagre",
    # Deliberately NOT declared, because EXTRA is global and these forms
    # carry a second sense outside their own chapter:
    #   "irreducibele" (88 uses) -- irreducible polynomial (ch. 2) vs
    #       irreducible representation (ch. 5); the bare "irreducibel" is
    #       handled per chapter by the overloaded-word rule + PRIMARY_OK.
    #   "normale"      (24) -- normal subgroup vs normal family (Montel)
    #       vs normal distribution.
    #   "euclidische"  (14) -- Euclidean domain vs Euclidean norm/division;
    #       EN stoplists "Euclidean" for exactly this reason.
    #   "perfecte"     (9)  -- perfect field (ch. 4) vs perfect set (ch. 6);
    #       EN links these to the field proposition, which is wrong.
    #   "vrije"        (10) -- "vrij" is stoplisted (free module vs free
    #       variable vs "vrij" as ordinary Dutch).
    #   "volledige"    (66) -- half its uses are the ordinary "full/entire"
    #       (volledige verantwoording, volledige omwenteling, volledige
    #       elliptische integraal); only the derived noun "volledigheid",
    #       which is always the completeness of a space, is declared.
    #   "separabele"/"separabiliteit" -- see the STOP note on "separabel".
}

NO_CAPITAL = set()
DERIVED = {}
# mirrors EN's PRIMARY_OK for the same two words: their first sense dominates
# the book, so they stay linked outside the chapter that pins them down
# ("compact" -> the space, except in ch. 15 where the operator sense wins;
# "irreducibel" -> the ring element, except in ch. 5's representations).
# EN's "closed"/"boundary"/"interior"/"path" are *not* mirrored: Dutch
# "gesloten" is pinned by the closed-forms chapter, so promoting it would
# point every closed set at the differential-forms definition.
PRIMARY_OK = {"compact", "irreducibel"}
AMBIG_POLICY = "drop"
EXTRA_PROTECT = [
    r'gesloten\s+vorm', r'gesloten\s+uitdrukking(?:en)?',
    r'onafhankelijk(?=\s+van\s+\$)',
    r'op\s+maat',        # "op maat" = made to order, not a measure
    r'dicht\s+bij',      # "dicht bij" = close to, not topologically dense
    r'lineair\s+onafhankelijk\w*',   # linear independence, not probabilistic
    r'volledige\s+(?:inhoud|lijst)', # "complete" in the ordinary sense
]
