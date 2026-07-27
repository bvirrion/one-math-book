"""Book 2 -- es. Curation only; the rules live in tools/termlink/.

Spanish bodies use raw UTF-8 accents. School book: nearest-preceding policy.
Aligned with book2_fr STOP ideas (ordinary language vs defined notions).
"""

NOT_A_TERM = ("teorema", "lema", "desigualdad", "fórmula", "criterio",
              "principio", "identidad", "regla", "ley de", "ley de los",
              "paradoja", "problema")

STOP = {
    # ordinal / ordinary language
    "primero",
    "primera",
    # sum of anything (vector sum is phrase-linked in chapter)
    "suma",
    # "par" as pair vs función par (chapter-local links still work)
    "par",
    # arithmetic/geometric as ordinary adjectives outside sequences
    "aritmética",
    "geométrica",
    "aritmético",
    "geométrico",
    # linear combination sense outside combinatorics
    "combinación",
    # coordinate "ordenada" vs ordered list
    "ordenada",
    "ordenado",
    # ordinary emphasis
    "todas",
    "estrictamente",
    "simultáneamente",
    # plane geometry "media" as half vs statistical mean is handled by
    # chapter locality; bare "media" still needs care in geometry chapters
}

NO_CAPITAL = {
    "desarrollar",
    "factorizar",
    "calcular",
    "demostrar",
    "mostrar",
    "completar",
}

EXTRA = {}
DROP = set()
DERIVED = {
    "continua": ["continuo", "continuas", "continuos"],
    "permutación": ["permutaciones"],
    "distribución normal": ["distribuciones normales"],
}
PRIMARY_OK = set()
AMBIG_POLICY = "nearest-preceding"
MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 40

EXTRA_PROTECT = [
    r'\bra[ií]ces?\s+cuadradas?\b',
    r'\bra[ií]ces?\s+cúbicas?\b',
    # "muestra/muestran" is both the noun (sample) and the verb (shows).
    # Protect the verb readings only; the two lookbehinds keep the genuine
    # noun in "la muestra que ..." / "una muestra que ..." linkable.
    r'(?<![Ll]a )(?<!una )(?<!ada )[Mm]uestran?'
    r'(?:\s+(?:que|qué|cómo|lo|entonces|a la|un|una|cada|el|la|los|las)\b'
    r'|\s+\\emph)',
    # "divide" is the arithmetic term, but also the ordinary verb
    r'\bdivide\s+el\s+riesgo\b',
    # "un continuo de valores" is the noun, not the continuity property
    r'\bcontinuo\s+de\s+valores\b',
]
