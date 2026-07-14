"""Book 2 -- fr. Curation only; the rules live in tools/termlink/.

The French bodies (parts/grade-10..12/fr) write their accents as raw UTF-8, so
the terms below are spelled the same way.
"""

# "un theoreme n'est pas une notion": the French translation of the default
# NOT_A_TERM keywords, which are English and therefore let "formule de Bayes",
# "lemme de Gauss", "loi des grands nombres" through.
NOT_A_TERM = ("théorème", "lemme", "inégalité", "formule", "critère",
              "principe", "identité", "règle", "loi de", "loi des",
              "paradoxe", "problème")

# Ordinary French, or a word whose sense in the book is not the definition's.
STOP = {
    # "premier terme", "premier quartile", "la première étape": the ordinal.
    # "nombre premier" and "premiers entre eux" survive as phrases.
    "premier",
    # harvested from the sum of two *vectors*; used for the sum of anything
    "somme",
    # "une paire de dés", "des paires de vecteurs", "une paire d'équations":
    # the noun. The adjective (fonction paire) keeps its links inside the
    # chapter that defines it, which is where it is used.
    "paire",
    # the sequence senses ("suite arithmétique / géométrique") are kept as
    # phrases; the bare adjectives mean number theory and geometry
    "arithmétique", "géométrique",
    # ordinary emphasis inside definitions
    "toutes", "strictement", "simultanément",
    # outside the combinatorics chapter, "combinaison" is a linear / integer
    # combination (Bezout, vecteurs coplanaires)
    "combinaison",
    # the adjective ("une liste ordonnée", "un $k$-uplet est une liste
    # ordonnée") drowns the noun (l'ordonnée d'un point). The noun keeps its
    # links in the coordinate-geometry chapter, and "ordonnée à l'origine"
    # survives as a phrase.
    "ordonnée",
}
# NB a STOPped word is still linked inside the chapter that defines it (the
# shared rule keeps chapter-local senses): "paire", "arithmétique",
# "géométrique", "premier", "ordonnée" are right there and wrong elsewhere.

# French exercises give their instructions in the infinitive, capitalised at the
# start of the item: "Développer et réduire", "Factoriser le trinôme". Those are
# imperatives, not uses of the notion; mid-sentence the word is linked.
NO_CAPITAL = {"développer", "factoriser"}

EXTRA = {
    # -al/-aux and the feminine forms are not reachable from the harvested
    # plural, so they are declared here.
    "orthogonal": "def:g11:scal:orthogonal",
    "orthogonale": "def:g11:scal:orthogonal",     # + orthogonales
    "vecteurs normaux": "def:g12:space:normal",
    "repère orthonormé": "def:g10:coordgeom:system",   # the other spelling of
                                                       # "repère orthonormal"
    "colinéaire": "def:g11:vect:collinear",       # singular; the plural is
                                                  # harvested and spiral-linked
}

DROP = {
    "(Théorème des gendarmes)",  # a result, not a term
    "Développer",                # duplicate of "développer"
}

DERIVED = {}
PRIMARY_OK = set()
AMBIG_POLICY = "nearest-preceding"   # a spiral curriculum re-defines its terms
MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 40

# Spans no link may touch. (Headings are masked by the shared rule.)
EXTRA_PROTECT = [
    # "loi" = distribution nearly everywhere, but these three are laws
    r'\blois?\s+des\s+(?:cosinus|grands\s+nombres)\b',
    r'\bloi\s+de\s+la\s+racine\b',
    # "racine carrée" is not a root of a polynomial
    r'\b[Rr]acines?\s+carrées?\b',
    r'\b[Rr]acines?\s+cubiques?\b',
    # the past participle of "étendre", not the statistical range
    r'\bétendue?s?\s+à\b',
    # "les termes du milieu" = the middle terms, not the midpoint of a segment
    r'\btermes\s+du\s+milieu\b',
]
