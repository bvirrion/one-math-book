"""Book 1 -- pt (Brazilian Portuguese). Curation only; rules in tools/termlink/.

The Portuguese bodies (parts/grade-1..9/pt) write their accents as raw UTF-8.
School book: spiral curriculum, AMBIG_POLICY nearest-preceding.
"""

NOT_A_TERM = ("teorema", "lema", "desigualdade", "fórmula", "critério",
              "princípio", "identidade", "regra", "lei de", "paradoxo",
              "problema")

# Ordinary Portuguese, or a word whose sense in the book is not the definition's.
STOP = {
    "reta",        # geometric line vs "straight"
    "oposto", "opostos",
    "classes",
    "escala",      # map scale vs ladder
    "ângulo", "triângulo", "retângulo", "círculo", "quadrado",
}

NO_CAPITAL = {"arredondar"}

EXTRA = {
    # Portuguese forms that the harvest may miss or under-link
    "classes": "def:g4:numbers:classes",
    "equação": "def:g8:equations:def",
    "equações": "def:g8:equations:def",
    "expoente": "def:g8:powers:def",
    "expoentes": "def:g8:powers:def",
    "potência": "def:g8:powers:def",
    "potências": "def:g8:powers:def",
    "média ponderada": "def:g8:speed:average",
    "médias ponderadas": "def:g8:speed:average",
    "números primos": "def:g9:arith:prime",
    "número primo": "def:g9:arith:prime",
    "primo": "def:g9:arith:prime",
    "primos": "def:g9:arith:prime",
    "fator de escala": "def:g9:thales:scaling",
    "fatores de escala": "def:g9:thales:scaling",
    "inclinação": "prop:g9:linfunc:affinegraph",
    "inclinações": "prop:g9:linfunc:affinegraph",
    "declive": "prop:g9:linfunc:affinegraph",
    "declives": "prop:g9:linfunc:affinegraph",
    "tabela de proporcionalidade": "def:g7:prop:table",
    "tabelas de proporcionalidade": "def:g7:prop:table",
    "proporcionalidade": "def:g7:prop:table",
    "números triangulares": "pb:g6:wholes:1",
    "média geométrica": "pb:g8:cosine:1",
    "média harmônica": "pb:g8:speed:1",
    "arredondar": "def:g4:numbers:round",
    "arredonde": "def:g4:numbers:round",
    "arredondado": "def:g4:numbers:round",
    "arredondada": "def:g4:numbers:round",
    "arredondados": "def:g4:numbers:round",
    "arredondadas": "def:g4:numbers:round",
    "arredondando": "def:g4:numbers:round",
}

SOFT = {
    "escala",
    "classes",
}
DROP = (set(STOP) - SOFT)

DERIVED = {}
PRIMARY_OK = set()
AMBIG_POLICY = "nearest-preceding"
MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 40

EXTRA_PROTECT = [
    r'\bresto\s+(?:[0-9$]|da\s|ainda)\b',
    r'\bescala\s+de\s+[0-9]',
]
