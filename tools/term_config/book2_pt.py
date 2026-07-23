"""Book 2 -- pt (Brazilian Portuguese). Curation only; rules in tools/termlink/.

High school: spiral curriculum, AMBIG_POLICY nearest-preceding.
UTF-8 accents in parts/grade-10..12/pt.
"""

NOT_A_TERM = ("teorema", "lema", "desigualdade", "fórmula", "critério",
              "princípio", "identidade", "regra", "lei de", "lei dos",
              "paradoxo", "problema")

STOP = {
    "soma",
    "par",
    "combinação",
    "todas",
    "estritamente",
    "simultaneamente",
    "ordenado",
    "ordenada",
    "primeiro",
    "primeira",
}

NO_CAPITAL = {
    "desenvolver",
    "fatorar",
}

EXTRA = {}
DROP = set()
DERIVED = {}
PRIMARY_OK = set()
AMBIG_POLICY = "nearest-preceding"
MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 40

EXTRA_PROTECT = [
    r'\bra[ií]zes?\s+quadra(?:da|das)?\b',
    r'\bra[ií]zes?\s+cúbicas?\b',
]
