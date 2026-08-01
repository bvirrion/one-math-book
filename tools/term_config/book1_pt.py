"""Book 1 -- pt (Brazilian Portuguese). Curation only; rules in tools/termlink/.

The Portuguese bodies (parts/grade-1..9/pt) write their accents as raw UTF-8.
School book: spiral curriculum, so AMBIG_POLICY is "nearest-preceding" -- a
term re-defined in grade 4 and again in grade 6 links to whichever definition
the reader has already met.

The Brazilian-Portuguese traps are neither the English nor the Spanish ones:

* "par" is both "even" and "a pair" ("os pares de Gauss", "pares de lados
  opostos", "os pares $(30, 15)$ e $(80, 120)$"). Counted in context, the
  pair sense wins outright in grades 5-9, so the bare word is dropped and the
  compound "número par" / "números pares" carries the link -- exactly what the
  English config does with its geometry furniture.
* "média" is *not* the Spanish trap: half an hour is "meia hora" here, so every
  "média" in the book is the statistical mean.
* "cara" is not a face either -- a face of a solid is "face", heads of a coin
  is "cara" -- so "face" needs no masking.
* "divide" is the third-person form, not the imperative (which is "divida"),
  so the relation "$b$ divide $a$" keeps its link; only the geometric sense
  ("a mediana divide o triângulo em dois") is masked.
* "raio" is both the radius and a ray of light; the pinhole-camera and
  shadow passages are full of "raios de sol" and "raios de luz".
* "volume" is both the solid's content and a volume of this series: the prose
  cross-references ("o volume do ensino médio", "os volumes de graduação")
  must never become geometry links.
"""

NOT_A_TERM = ("teorema", "lema", "desigualdade", "fórmula", "critério",
              "princípio", "identidade", "regra", "lei de", "paradoxo",
              "problema")

# Never linked: ordinary Portuguese, or a word this book uses in another sense
# far more often than in the sense its definition gives it.
STOP = {
    # "a reta numérica", "uma linha reta", "em linha reta": the geometric line
    # (def:g6:lines:objects) is a minority of the uses. "retas paralelas" and
    # "retas perpendiculares" keep their own links.
    "reta",
    # geometry owns this word: "os lados opostos do retângulo", "o cateto
    # oposto ao ângulo". The opposite of a relative number is a small minority,
    # and "ângulos opostos pelo vértice" keeps its own link.
    "oposto", "opostos",
    # def:g4:numbers:classes is the group of three digits; grade 7 groups data
    # into (statistical) classes and grade 8 averages two school classes.
    "classes",
    # the scale of a map or model; also the scale of an axis and the verb
    # "mudar a escala". "fator de escala" keeps its link.
    "escala",
    # the edge of a solid, but also "a aresta da régua" and the everyday
    # furniture of the solids chapters.
    "aresta", "arestas",
    # "par" / "pares": the pair sense dominates from grade 5 on (see the
    # module docstring). "número par" / "números pares" carry the link.
    "par", "pares",

    # ---- the furniture ----------------------------------------------------
    # Real definitions (a child meets them in grades 1-6), but by the time they
    # are used they are the everyday furniture of the page: they occur in
    # nearly every sentence of every geometry chapter, and linking each one
    # turns the exercises solid blue. The compounds a child can really forget
    # survive and carry the link: "ângulo reto", "triângulo retângulo",
    # "triângulo isósceles", "triângulo equilátero", "raiz quadrada",
    # "ângulos alternos internos", "ângulos opostos pelo vértice".
    "ângulo", "triângulo", "retângulo", "círculo", "quadrado",
}

# Linked mid-sentence, not sentence-initially: "Arredonde $8.276$ à unidade" and
# "Desenvolva e reduza" open an instruction, they are not uses of the noun;
# "Divide" would only ever start a heading.
NO_CAPITAL = {"arredondar", "desenvolver", "divide"}

# Manual {term: label}; overrides every rule. Kept deliberately small: the
# harvest already reaches almost everything through \emph{}\index{} pairs.
EXTRA = {
    "equação": "def:g8:equations:def",
    "equações": "def:g8:equations:def",
    "fator de escala": "def:g9:thales:scaling",
    "fatores de escala": "def:g9:thales:scaling",
    "tabela de proporcionalidade": "def:g7:prop:table",
    "tabelas de proporcionalidade": "def:g7:prop:table",
    "números triangulares": "pb:g6:wholes:1",
    "média geométrica": "pb:g8:cosine:1",
    "média harmônica": "pb:g8:speed:1",
}

# STOP is deliberately *soft*: a stoplisted word is kept out of the global
# vocabulary but still links inside the chapter that defines it. For most of
# the words above that is not wanted either, so they are hard-dropped as well.
# These are the exceptions -- ordinary language everywhere in the book *except*
# in their own chapter, where every single use is the term:
SOFT = {
    "escala",            # parts/grade-7/05: every use there is the map scale
    "classes",           # parts/grade-4/01: the groups of three digits
    "aresta", "arestas", # parts/grade-5/07: "12 arestas", faces + vértices = arestas + 2
}

DROP = (set(STOP) - SOFT) | {
    # \emph{valor de um algarismo depende da posição dele}\index{valor
    # posicional} in parts/grade-6/pt/01: the sentence is not a term (the term
    # is "valor posicional", which is harvested from the index key).
    "valor de um algarismo depende da posição dele",
}

# Since 2026-08-01 tools/term_config/lang_pt.py sets TAIL_ON_EVERY_WORD = True,
# so the optional tail "(?:e?s)?" goes on EVERY word of a phrase and the regular
# compound plurals are generated for free: "triângulo retângulo" now matches
# "triângulos retângulos", "número par" matches "números pares". This map was 27
# entries under the old flag and is trimmed to the 8 forms the tail genuinely
# cannot build -- -ão/-ões, -al/-ais, -m/-ns, and the accent shift in
# raiz/raízes. Do not re-add a regular plural here: it is dead weight, and a
# declaration whose base is ambiguity-resolved is worse than dead weight (it is
# silently inert -- DERIVED only extends the unambiguous map, which is why the
# old "eixo de simetria" entry had never done anything).
DERIVED = {
    # -z -> -zes with an accent shift the tail cannot make (raizes != raízes)
    "raiz quadrada": ["raízes quadradas"],
    # -ão -> -ões
    "função linear": ["funções lineares"],
    "função afim": ["funções afins"],          # and -m -> -ns in "afim"
    "expressão literal": ["expressões literais"],   # and -al -> -ais
    "seção transversal": ["seções transversais"],   # and -al -> -ais
    "notação científica": ["notações científicas"],
    # -al -> -ais
    "número decimal": ["números decimais"],
    "ponto decimal": ["pontos decimais"],
}
PRIMARY_OK = set()
AMBIG_POLICY = "nearest-preceding"   # a spiral curriculum re-defines its terms
MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 40

# Spans no link may enter: the uses where a good term means something else.
# NB: every space here is \s+ -- the sources wrap at 72 columns, and a phrase
# split across two lines ("metros\ncúbicos") slips past a literal space.
EXTRA_PROTECT = [
    # "volume": the books of this series, not the content of a solid
    r'volumes?\s+d[oe]\s+ensino\s+(?:m(?:é|e)dio|fundamental)',
    r'volumes?\s+de\s+gradua(?:ç|c)(?:ã|a)o',
    r'volumes?\s+d[ao]\s+s(?:é|e)rie',
    r'volumes?\s+do\s+primeiro\s+ano',

    # "raio": a ray of light or of the Sun, not a radius
    r'raios?\s+de\s+(?:sol|Sol|luz)',
    r'raios?\s+(?:paralelos?|de\s+sol)',
    r'raios?\s+dele\s+chegam',
    r'raios?\s+se\s+cruzam',
    r'raio\s+de\s+luz',
    # "Tales é a matemática dos \emph{raios}": rays, not radii. (Exposed only
    # after the two $-consuming patterns below were rewritten with lookaheads
    # -- it had been hidden inside a mis-paired math mask.)
    r'\\emph\{raios\}',

    # "resto": "the rest", not the remainder of a division
    r'[Oo]\s+resto\s+do\s+problema',
    r'[Oo]\s+resto\s+(?:é|e)\s+admitido',
    r'com\s+o\s+resto\b',

    # "divide": the geometric sense ("a mediana divide o triângulo em dois"),
    # not the arithmetic relation "$b$ divide $a$"
    r'divide\s+(?:em\s+dois|ao\s+meio|a\s+folha|as\s+mesmas)',
    # NEVER CONSUME A `$` (see the header of tools/termlink/protect.py): the
    # whole list is one alternation, and a pattern that eats an opening $
    # leaves the inline-math rule pairing the closing $ with the next
    # formula's opening one, masking every span inside out to end of file.
    # Match the trailing $ with a lookahead.
    r'divide\s+(?=\$[A-Z])',
    r'divide\s+o\s+(?:tri(?:â|a)ngulo|quadril(?:á|a)tero|trap(?:é|e)zio)',

    # "cubo": the operation and the unit of volume, not the solid
    r'\ba[o]?\s+cubo\b',
    r'com\s+o\s+cubo\b',        # "os volumes mudam com o cubo" (the power)
    r'(?:metros?|dec(?:í|i)metros?|cent(?:í|i)metros?|mil(?:í|i)metros?)'
    r'\s+c(?:ú|u)bicos?',
    r'quadrado--cubo',

    # "escala": the numeric scale of a map, printed as "escala $1 : 25\,000$"
    r'escala\s+de\s+[0-9]',
    r'escala\s+(?=\$)',        # lookahead: never consume the opening $
]
