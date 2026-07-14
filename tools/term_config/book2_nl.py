"""Book 2 -- nl. Curation only; the rules live in tools/termlink/.

The Dutch bodies (parts/grade-10..12/nl) write their accents as raw UTF-8, so
the terms below are spelled the same way. Dutch writes its compounds solid
(vierkantswortel, priemgetal) and the shared rule refuses to link a component
inside a compound, so Dutch coverage is thinner than English by construction --
and safer: "wortel" never lands inside "vierkantswortel".
"""

# "een stelling is geen begrip": the Dutch translation of the default
# NOT_A_TERM keywords, which are English and therefore let "formule van Bayes",
# "ongelijkheid van Markov", "wet van de grote aantallen" through.
NOT_A_TERM = ("stelling", "lemma", "ongelijkheid", "formule", "criterium",
              "principe", "identiteit", "regel", "wet van", "paradox",
              "probleem")

# Ordinary Dutch, or a word whose sense in the book is not the definition's.
STOP = {
    # parity of an integer ("als $N$ even is") and the adverb ("even groot").
    # The harvested sense is the parity of a *function*; "even functie" and
    # "oneven functie" survive as phrases.
    "even", "oneven",
    # harvested from the sum of two *vectors*; used for the sum of anything
    "som",
    # outside the combinatorics chapter, "combinatie" is a linear combination
    "combinatie",
    # ordinary emphasis inside definitions
    "alle", "strikt", "tegelijk",
}
# NB a STOPped word is still linked inside the chapter that defines it (the
# shared rule keeps chapter-local senses), which is what we want: "even" and
# "oneven" are right in the parity chapter and wrong everywhere else.

NO_CAPITAL = set()    # Dutch instructions use the stem ("Ontbind", "Ontwikkel",
                      # "Bereken"), which never matches the infinitive terms
                      # "ontbinden" / "ontwikkelen" -- no imperative collides

EXTRA = {
    # the inflected adjective (-aal -> -ale) is not reachable from the
    # harvested base form
    "orthogonale": "def:g11:scal:orthogonal",
    "orthonormale": "def:g10:coordgeom:system",
}

DROP = {
    "(Insluitstelling)",   # a result, not a term
    "Ontwikkelen",         # duplicate of "ontwikkelen"
}

DERIVED = {}
PRIMARY_OK = set()
AMBIG_POLICY = "nearest-preceding"   # a spiral curriculum re-defines its terms
MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 40

# Spans no link may touch. (Headings are masked by the shared rule.)
EXTRA_PROTECT = [
    # "rij" is the Dutch for a sequence AND for a row, and this book uses both:
    # a matrix ("$m$ rijen en $n$ kolommen", "de ingang in rij $i$, kolom $j$"),
    # the rows of Pascal's triangle, the row of a probability table, and the
    # rows of seats in the theatre exercise. The sequence sense is far too
    # central to drop, so the row sense is masked by its context instead.
    # The windows are wide enough to survive an \omterm wrapper sitting between
    # the word and its context, so a re-run without --unwrap stays a no-op.
    r'\brij(?:en)?\b(?=[^.]{0,70}(?:kolom|stoelen|theater'
    r'|driehoek\s+van\s+Pascal|permutaties))',
    r'\brij(?:en)?\b(?=\s*\$[0-9n][^$]*\$)',  # "rij $n$", "rij $5$", "rijen $n =
                                              # 0$": a row is numbered, a
                                              # sequence is always "rij $(u_n)$"
    r'\brij\s+voor\s+rij\b',                  # "row by row"
    r'\bper\s+rij\b',
    r'\brij\s+van\s+kansen\b',
    r'(?<=uit tot )rij\b',                    # "tot rij $7$" of Pascal
    # "vergelijking" is an equation -- but it is also the ordinary word for a
    # comparison, and Dutch uses both senses in this book
    r'[Vv]ergelijking(?:en)?\s+van\s+(?:beelden|argumenten|integralen)\b',
    r'\bVergelijking\s+volgt\b',
    # "het risico deelt" = shares/divides the risk, not "a divides b"
    r'\bdeelt\s+het\s+risico\b',
]
