"""Book 1 -- es. Curation only; the rules live in tools/termlink/.

The Spanish bodies (parts/grade-1..9/es) write their accents as raw UTF-8.
School book: spiral curriculum, AMBIG_POLICY nearest-preceding.

The Spanish traps are not the English ones, and only partly the French ones.
"media" is both the statistical mean and the feminine of "medio" ("media
hora", "media vuelta", "media esfera"); "resto" is both the remainder of a
division and "the rest" of anything; "cara" is both a face of a solid and
heads of a coin; "par" is both "even" and "a pair of"; "divide" is both the
arithmetic relation ("$b$ divide a $a$") and the imperative that opens half
the exercises ("divide entre $75$"). "escala", by contrast, is *less*
ambiguous than French "échelle": the ladder leaning against the wall is an
"escalera" here, so only the map/model sense is left.
"""

NOT_A_TERM = ("teorema", "lema", "desigualdad", "fórmula", "criterio",
              "principio", "identidad", "regla", "ley de", "paradoja",
              "problema")

# Ordinary Spanish, or a word whose sense in the book is not the definition's.
STOP = {
    "recta",       # geometric line vs. "la recta numérica" furniture
    "opuesto", "opuestos",
    "clases",
    "escala",      # map scale
    # the statistical range; "el recorrido" is also the route itself
    # ("dos tercios del recorrido", "queda la mitad del recorrido"), which is
    # the majority of the uses outside the statistics chapter.
    "recorrido",
    "ángulo", "triángulo", "rectángulo", "círculo", "cuadrado",
    # the same furniture: English stoplists "circle", and Spanish splits it
    # into "círculo" (the disk) and "circunferencia" (the line). Both are on
    # every page of every geometry chapter; "circunferencia circunscrita"
    # keeps its own link.
    "circunferencia",
}

# Linked mid-sentence, not sentence-initially: "Redondea $8.276$ a la unidad"
# and "Desarrolla y reduce" are instructions, not uses of the noun.
# "Divide por el primo más pequeño" and "Divide entre $6$" open a method step;
# the relation "$b$ divide a $a$" is the term and always sits mid-sentence.
NO_CAPITAL = {"redondear", "desarrollar", "divide"}

EXTRA = {}
SOFT = {
    "escala",
    "clases",
    "recorrido",   # parts/grade-9/09: every use there is the statistical range
}
DROP = (set(STOP) - SOFT)

# tools/term_config/lang_es.py appends the plural -s/-es to the LAST word only
# ("número primos"), which is not how a Spanish noun phrase pluralises: the
# head noun inflects too. Declare the plurals of the multi-word terms here, or
# the book links "triángulo rectángulo" and never "triángulos rectángulos".
DERIVED = {
    "función lineal": ["funciones lineales"],
    "función afín": ["funciones afines"],
    "raíz cuadrada": ["raíces cuadradas"],
    "expresión literal": ["expresiones literales"],
}
PRIMARY_OK = set()
AMBIG_POLICY = "nearest-preceding"
MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 40

# Spans no link may enter: the uses where a good term means something else.
# Every space is \s+ -- the sources wrap at 72 columns and a phrase split
# across two lines ("media\nhora") slips past a literal space.
EXTRA_PROTECT = [
    # "reste": the imperative, not the noun
    r'\breste\s+(?:[0-9$]|de\s+la|aún|todavía)\b',
    r'\bescala\s+de\s+[0-9]',

    # "media": the feminine of "medio", not the mean
    r'\bhora\s+y\s+media\b',
    r'\b[Mm]edias?\s+(?:vuelta|altura|esfera|hora|manzana|naranja|docena'
    r'|tableta|casilla|luna)\w*',
    r'\bparalela\s+media\b',
    r'\bcm\s+media\s+hora\b',

    # "resto": "the rest", not the remainder
    r'\bresto\s+(?:del|de\s+l|vien)',
    r'(?:hace|damos|da)\s+el\s+resto\b',

    # "par": "a pair of", not "even"; "pares": the verb "parar"
    r'\bpares?\s+de\b',
    r'\bte\s+pares\b',

    # "cara": heads of a coin, not a face of a solid
    r'(?:sacar|obtener|salir|sale|con|de)\s+cara\b(?!s)',
    r'\b[Cc]ara\s+(?:y|o|\\emph\{[yo]\})\b',
    r'\bcara\s+o\s+cruz\b',

    # "divide": the imperative that opens half the exercises. The relation
    # -- "$b$ divide a $a$", "ningún $p_i$ divide a $N$" -- keeps its link.
    r'[Dd]ivide\s+(?:entre|todo|el|la|los|las|cada|primero|antes)\b',
    r'\\item\s+divide\b',
    r'[Dd]ivide\s+numerador',
    r'[Dd]ivide\s*\.',
    r'[Ss]e\s+divide[ns]?\b',
    r'[Dd]ivídelo\b',

    # "desarrollo": the algebraic expansion, not the net of a solid
    r'[Tt]res\s+desarrollos\s+aparecen',
    r'término\s+del\s+desarrollo',
    r'practica\s+el\s+desarrollo',

    # hyphenated compounds: lang_es lets a link swallow the whole compound,
    # and "la ley del cuadrado-cubo" is not the solid, nor is the ratio
    # "superficie-volumen" the volume of anything.
    r'cuadrado-cubo',
    r'superficie-volumen',

    # "cubo": the unit of volume and the operation, not the solid
    r'(?:metros?|decímetros?|centímetros?|milímetros?)\s+cúbicos?',
    r'\bal\s+cubo\b',
]
