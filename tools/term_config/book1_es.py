"""Book 1 -- es. Curation only; the rules live in tools/termlink/.

The Spanish bodies (parts/grade-1..9/es) write their accents as raw UTF-8.
School book: spiral curriculum, AMBIG_POLICY nearest-preceding.
"""

NOT_A_TERM = ("teorema", "lema", "desigualdad", "fórmula", "criterio",
              "principio", "identidad", "regla", "ley de", "paradoja",
              "problema")

# Ordinary Spanish, or a word whose sense in the book is not the definition's.
STOP = {
    "recta",       # geometric line vs "to the right"
    "opuesto", "opuestos",
    "clases",
    "escala",      # map scale vs ladder
    "ángulo", "triángulo", "rectángulo", "círculo", "cuadrado",
}

NO_CAPITAL = {"redondear"}

EXTRA = {}
SOFT = {
    "escala",
    "clases",
}
DROP = (set(STOP) - SOFT)

DERIVED = {}
PRIMARY_OK = set()
AMBIG_POLICY = "nearest-preceding"
MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 40

EXTRA_PROTECT = [
    r'\breste\s+(?:[0-9$]|de\s+la|aún|todavía)\b',
    r'\bescala\s+de\s+[0-9]',
]
