"""Book 2 -- pt (Brazilian Portuguese). Curation only; the rules live in
tools/termlink/.

The Portuguese bodies (parts/grade-10..12/pt) write their accents as raw UTF-8,
so the terms below are spelled the same way.

Three homographs are Portuguese-only and drive most of the curation:

  * "módulo" is both the absolute value / complex modulus *and* the Latin
    "modulo n" of the arithmetic chapter (English keeps "modulus" and "modulo"
    apart, French keeps "module" and "modulo" apart -- Portuguese does not);
  * "amplitude" is the statistical range *and* the amplitude of an
    oscillation or of a seismic wave;
  * "intervalo" is the mathematical interval *and* the gap between two buses
    in the last chapter's inspection paradox.

Each is handled below, the first two without losing the genuine links (the
protected spans are the wrong-sense phrases only).

Known, accepted gap: "razão" is the ratio of BOTH a progressão aritmética and
a progressão geométrica in Brazilian usage, so the harvest sees one word
defined twice in the same chapter and drops it. English links "common
difference" and "common ratio" separately; Portuguese cannot without inventing
terminology no Brazilian textbook uses.
"""

# "um teorema não é uma noção": the Portuguese translation of the default
# NOT_A_TERM keywords, which are English and therefore let "fórmula de Bayes",
# "lema de Gauss", "lei dos grandes números" through. "lei da" is needed for
# "lei da probabilidade total", which English drops via its own "law of".
NOT_A_TERM = ("teorema", "lema", "desigualdade", "fórmula", "critério",
              "princípio", "identidade", "regra", "lei de", "lei da",
              "lei das", "lei dos", "paradoxo", "problema")

# Ordinary Portuguese, or a word whose sense in the book is not the
# definition's. STOP is SOFT: a stoplisted word is still linked inside the
# chapter that defines it, which is exactly what these entries want.
STOP = {
    # harvested from the sum of two *vectors*; used for the sum of anything
    "soma",
    # "um par de dados", "pares de vetores": the noun. The adjective
    # (função par) keeps its links in the parity chapter.
    "par",
    # same treatment as "par": outside the parity chapter, "ímpar" means an
    # odd *number* (English keeps "odd" chapter-local for the same reason).
    "ímpar",
    # the statistical range in grade 10; the amplitude of an oscillation in
    # grades 11--12. Chapter-local keeps the statistics sense and drops the
    # rest.
    "amplitude",
    # the adjective ("uma lista ordenada", "uma $k$-upla ordenada") drowns the
    # noun (a ordenada de um ponto), which keeps its links in the
    # coordinate-geometry chapter
    "ordenada", "ordenado",
    # ordinary emphasis inside definitions
    "todas", "estritamente", "simultaneamente",
    # outside the combinatorics chapter, a "combinação" is a linear or integer
    # combination (Bézout, vetores coplanares)
    "combinação",
    # the ordinal ("primeiro termo", "primeiro quartil"); "número primo" and
    # "primos entre si" survive as phrases
    "primeiro", "primeira",
}

# Portuguese exercises give their instructions in the imperative
# ("Expanda e reduza", "Fatore o trinômio"), but headings and a few item stems
# use the bare infinitive, capitalised. Those are instructions, not uses of the
# notion; mid-sentence the word is linked.
NO_CAPITAL = {"expandir", "fatorar"}

EXTRA = {
    # gender / number forms the harvest cannot reach from the plural or the
    # feminine it saw in the definition
    "ortogonal": "def:g11:scal:orthogonal",
    "coplanar": "def:g12:space:collinear",
    "colinear": "def:g11:vect:collinear",     # the plural is harvested and
                                              # spiral-linked
    "vetores normais": "def:g12:space:normal",   # -al -> -ais, not WORD_TAIL's
    "invertíveis": "def:g12:matrix:inverse",     # -vel -> -veis
    "sistema ortonormado": "def:g10:coordgeom:system",  # the other spelling
}

DROP = {
    "(Teorema do confronto)",  # a result, not a term
    "Expandir",                # duplicate of "expandir"
}

# `lang_pt.py` sets TAIL_ON_EVERY_WORD = True, so the shared WORD_TAIL
# `(?:e?s)?` already reaches every REGULAR plural, on each word of a compound
# ("número primo" -> "números primos", "contínua" -> "contínuas"). Only two
# things still need declaring:
#
#   * plurals WORD_TAIL cannot spell -- "-ão" -> "-ões", "-al" -> "-ais",
#     "-vel" -> "-veis" (and, elsewhere, "-m" -> "-ns", "-r" -> "-res");
#   * GENDER, which WORD_TAIL does not touch at all: a term harvested as
#     "contínua" is unreachable as "contínuo". The masculine is declared here
#     and its own regular plural then comes free from WORD_TAIL.
DERIVED = {
    # gender only -- "contínuas"/"contínuos" come from WORD_TAIL
    "contínua": ["contínuo"],
    "convexa": ["convexo"],
    "côncava": ["côncavo"],
    "monótona": ["monótono"],
    "limitada": ["limitado"],
    # irregular plurals
    "derivável": ["deriváveis"],      # -vel -> -veis
    "permutação": ["permutações"],    # -ão  -> -ões
    "fatorial": ["fatoriais"],        # -al  -> -ais
    "distribuição normal": ["distribuições normais"],   # both words irregular
    # not a plural at all: English emphasises "frequency" in this definition,
    # Brazilian usage spells the notion "frequência relativa" but writes the
    # bare head in running text. Its plural comes from WORD_TAIL.
    "frequência relativa": ["frequência"],

    # --- irregular plurals of UNAMBIGUOUS terms -------------------------
    # Found by auditing, for every linkable term, the count of its true Brazilian
    # plural in the sources against the count actually linked: WORD_TAIL spells
    # "equaçãos", the language says "equações". Same trap as physics's
    # "ordem de grandeza" (-m -> -ns), and it is worth ~130 links here.
    "equação": ["equações"],                        # -ão -> -ões
    "equação diferencial": ["equações diferenciais"],
    "aproximação": ["aproximações"],
    "interseção": ["interseções"],
    "união": ["uniões"],
    "imagem": ["imagens"],                          # -m  -> -ns
    "pré-imagem": ["pré-imagens"],
    "integral": ["integrais"],                      # -al -> -ais
    "ortonormal": ["ortonormais"],
    "parte real": ["partes reais"],
    "número natural": ["números naturais"],
    "função afim": ["funções afins"],               # -ão -> -ões AND -m -> -ns
    "função quadrática": ["funções quadráticas"],
    "função ímpar": ["funções ímpares"],            # -r  -> -res
}

PRIMARY_OK = set()
AMBIG_POLICY = "nearest-preceding"   # a spiral curriculum re-defines its terms
MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 40

# Spans no link may touch. (Headings and math are masked by the shared rule.)
#
# Four ways a pattern here fails SILENTLY -- no gate catches any of them, so
# every pattern below was checked against all four:
#   1. never consume a `$` (see the header of tools/termlink/protect.py):
#      every math-adjacent pattern below stops at a lookahead;
#   2. never write a literal space -- the list compiles with re.S and LaTeX
#      wraps lines, so `\s+` is used throughout;
#   3. audit on UNWRAPPED source: an already-inserted wrong link hides the
#      evidence of itself;
#   4. a pattern that matches nothing looks exactly like one that works, and a
#      pattern that matches but suppresses nothing is just as useless. Every
#      group below was measured by deleting it and re-running the linker; the
#      wrong-sense links each one actually suppresses are recorded beside it.
#      (Portuguese accent trap: a class standing in for an accented vowel must
#      list every accent the word can carry -- circumflex AND acute. None of
#      the words guarded here takes a circumflex: "módulo", "raiz/raízes",
#      "cúbica" are acute-only, verified against every spelling in the corpus.)
EXTRA_PROTECT = [
    # "raiz quadrada / cúbica" is not a root of a polynomial (suppresses 9)
    r'\b[Rr]a[ií]z(?:es)?\s+quadrad[ao]s?\b',
    r'\b[Rr]a[ií]z(?:es)?\s+c[úu]bicas?\b',

    # --- "módulo": the arithmetic "modulo n", not the absolute value ---
    # "módulo" followed by the modulus is always the Latin adverb; the
    # absolute value and the complex modulus never take an argument this way.
    # (suppresses 50; the bare-digit variant `\s+(?=\d)` was removed -- every
    # modulus in this book is written in math mode, so it matched nothing.)
    r'[Mm][óo]dulos?\s+(?=\$)',
    r'[Mm][óo]dulos?\s+primos?\b',

    # --- "amplitude": NO PATTERN NEEDED ---
    # The oscillation / seismic sense ("amplitude sísmica", "amplitude $R$",
    # "razão das amplitudes", "não depende da amplitude") used to carry five
    # guards here. Measured: deleting all five changes the link count by ZERO,
    # because the soft STOP on "amplitude" already confines the term to the
    # statistics chapter that defines it. Five patterns that matched text and
    # protected nothing -- removed rather than left looking protective.

    # --- "intervalo": the gap between two buses (inspection paradox) ---
    # (suppresses 22)
    r'\b[Ii]ntervalos?\s+(?:médio|longo|longos|típico|grande)\b',
    r'\bde\s+um\s+intervalo\s+inteiro\b',
    r'\bcomprimento\s+do\s+intervalo\s*(?=:)',
    r'\bintervalos\s+alternam\b',
    r'\bintervalos\s+com\s+probabilidade\s+proporcional\b',
    r'\bintervalo\s+em\s+que\s+você\b',
    r'\bintervalo\s+que\s+contém\s+você\b',
    r'\bintervalo\s+que\s+por\s+acaso\b',
    r'\bmetade\s+de\s+um\s+intervalo\b',

    # "no máximo" / "no mínimo" are Portuguese for "at most" / "at least",
    # not the extrema of a function. "no máximo local" is the real thing.
    # (suppresses 27)
    r'\b[Nn]o\s+máximo\b(?!\s+local)',
    r'\b[Nn]o\s+mínimo\b(?!\s+local)',

    # "divide" is the arithmetic term, but also the ordinary verb (suppresses 2)
    r'\bdivide\s+o\s+risco\b',

    # the complementary-angle identity, not the complement of an event (2)
    r'\bidentidade\s+complementar\b',

    # "os dois extremos" = the two extreme cases, not the extrema (suppresses 1)
    r'\bos\s+dois\s+extremos\b',
]
