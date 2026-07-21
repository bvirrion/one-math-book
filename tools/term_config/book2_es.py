"""Book 2 -- es. Curation only; the rules live in tools/termlink/.

The Spanish bodies (parts/grade-10..12/es) write their accents as raw UTF-8, so
the terms below are spelled the same way.
"""

# Spanish translation of the default NOT_A_TERM keywords (English defaults
# would let Spanish result-names through and over-link).
NOT_A_TERM = ("teorema", "lema", "desigualdad", "fórmula", "criterio",
              "principio", "identidad", "regla", "ley de", "ley de los",
              "paradoja", "problema")

STOP = {
    # ordinary language harvested from definitions
    "suma",
    "par",
    "combinación",
    "todas",
    "estrictamente",
    "simultáneamente",
    "ordenado",
    "ordenada",
    "primero",
    "primera",
}

NO_CAPITAL = {
    "desarrollar",
    "factorizar",
}

EXTRA = {}
DROP = set()
DERIVED = {}
PRIMARY_OK = set()
AMBIG_POLICY = "nearest-preceding"
MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 40

EXTRA_PROTECT = [
    r'\bra[ií]ces?\s+cuadradas?\b',
    r'\bra[ií]ces?\s+cúbicas?\b',
]
