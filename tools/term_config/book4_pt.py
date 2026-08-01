"""Book 4 (University Year 2) -- Brazilian Portuguese. Curation only; the
rules live in tools/termlink/.

Curated against the English link targets (the parity gate): the set of
`\\omterm` targets under parts/bachelor-2/pt must equal the English set, and a
term must reach the same definition it reaches in English.

Two Portuguese facts drive most of the table below.

  * tools/term_config/lang_pt.py sets TAIL_ON_EVERY_WORD = False, so the
    plural of a noun PHRASE is never generated ("forma quadrática" would match
    "forma quadráticas", never "formas quadráticas"). Every phrase plural the
    book uses therefore has to be declared in DERIVED. That is the single
    largest block below; it is mechanical, not judgemental.
  * Portuguese adjectives agree in gender and number and nominalise in
    -idade / -ude / -ência. The shared morphology generates only the -s/-es
    tail on the last word, so the feminine, the feminine plural and the
    abstract noun are declared term by term.

AMBIG_POLICY is "drop", as in book4_en.py and in books 3 and 5: at this level
a word defined twice with no phrase to separate the senses is better left
unlinked than sent to a coin-flip definition.
"""

# The default NOT_A_TERM keywords are English, so the harvester filters
# "Parseval's theorem" out of the English book but would let the Portuguese
# "identidade de Parseval", "regra da cadeia", "teorema espectral",
# "desigualdade de Bessel" through -- result-names English never links.
# Filtering on the Portuguese heads restores parity. Bare "lei" is NOT listed
# (it is the distribution/law DEFINITION, def:b2:randomvar:law); only the
# phrase "lei de" is filtered.
NOT_A_TERM = ("teorema", "lema", "desigualdade", "fórmula", "critério",
              "princípio", "identidade", "regra", "lei de", "paradoxo",
              "problema",
              # English heads as well: the harvester falls back to the
              # emphases the English twin accepted, so English result-names
              # can leak into the Portuguese term list.
              "theorem", "lemma", "inequality", "formula", "criterion",
              "principle", "identity", "rule", "law of", "paradox")

# Soft: a stoplisted word is still linked inside the chapter that defines it.
# One-for-one with book4_en.py's STOP.
STOP = {
    "ordem", "ordens",              # "em ordem", "ordem de soma", "de ordem 2"
    "equivalente", "equivalentes",  # only NORMS are defined equivalent
    "álgebra", "álgebras",          # "álgebra linear" >> $K$-álgebra
    "converge", "convergem",        # defined for improper integrals (ch. 9)
    "alternado", "alternada",       # alternating form (ch. 2) vs series (ch. 7)
    "alternados", "alternadas",
    "assinatura",                   # of a permutation (ch. 1) vs of a form (ch. 12)
    "exato", "exata", "exatos", "exatas",  # "forma exata" (ch. 20) vs "o valor exato"
    "regular", "regulares",         # regular point/arc (ch. 18) vs surface (ch. 19)
    "equivalência",                 # equivalence relation (ch. 1) vs of norms (ch. 5)
}

# Hard: never a link anywhere.
DROP = {
    # Named RESULTS, not notions. English filters them through NOT_A_TERM or
    # drops them by hand; in Portuguese several reach the harvester through an
    # \emph{...}\index{...} pair whose head NOT_A_TERM does not catch.
    "fórmula-limite de Gauss",                       # ch. 9 problem
    "teorema de Korovkin",                           # ch. 10 problem
    "desigualdade de Hadamard",                      # ch. 12 problem
    "teorema mín-máx de Courant--Fischer",           # ch. 13 problem
    "desigualdades de perturbação de Weyl",
    "fórmula de Jacobi",                             # ch. 15 problem
    "cota de Chernoff", "desigualdades de concentração",   # ch. 22 problem
    "fenômeno de Gibbs",     # named in a figure caption, explained elsewhere
    "ponto central",         # pb:b2:affine:1 -- EN "centerpoint" is not harvested
    "função totiente de Euler",   # prop:b2:structures:cyclic -- EN does not link it
    # English strings inherited from the twin's accepted emphases; they are
    # result-names, and English does not link them either.
    "Euler's theorem", "Jensen's inequality", "Stirling's formula",
    "spectral theorem",
    # English never links the bare adjoint: it is introduced in ch. 12
    # (Euclidean) AND in ch. 13 (Hermitian), so English drops it as ambiguous.
    # The Portuguese ch. 13 definition writes "adjunto" without an \index,
    # which slips past the ambiguity test; drop it by hand to stay in step.
    "adjunto",
    # English hard-drops bare "closed" (ch. 20 alone has "closed form",
    # "closed arc", "closed disk"). The Portuguese ch. 20 definition
    # emphasises the bare adjective "fechada", which the harvester picks
    # up; the PHRASE "forma fechada" survives and carries the links.
    "fechada", "fechado", "fechadas", "fechados",
    # adverbs whose ordinary-Portuguese sense is the only one used
    "simetricamente", "ciclicamente",
}

# Portuguese derivations the shared morphology cannot generate. Since
# 2026-08-01 lang_pt.py sets TAIL_ON_EVERY_WORD = True, so the *regular* plural
# of a noun phrase is generated ("forma quadrática" -> "formas quadráticas",
# "espaço métrico compacto" -> "espaços métricos compactos"), and the tail is
# optional per word, so head-only plurals work too ("espaço de Banach" ->
# "espaços de Banach"). 84 hand-declared regular plurals were therefore removed
# from this table on that date. What remains is what the tail `(?:e?s)?` on each
# word genuinely cannot reach:
#
#   * GENDER. The tail is a plural, never a feminine: "contínua" cannot reach
#     "contínuo", "hermitiano" cannot reach "hermitiana". This is the shared,
#     documented limitation (see lang_pt.py) and the largest block below.
#   * NOMINALISATIONS in -idade / -ude / -ência, which English spells -ness or
#     -ity: compacidade, completude, conexidade, continuidade, independência.
#   * IRREGULAR plurals: -ão -> -ões (torção -> torções), -l -> -is (ideal ->
#     ideais, enumerável -> enumeráveis, minimal -> minimais), -m -> -ns
#     (afim -> afins), and the fully irregular anel -> anéis.
#   * SINGULARS of terms the harvester picked up in the plural (integrais de
#     Wallis -> integral de Wallis): the tail only ever adds letters.
#
# A form is listed only if it really occurs in the book.
DERIVED = {
    # --- adjective families: feminine, and the abstract noun ---------------
    "contínua":         ["contínuo", "contínuos",
                         "continuidade", "continuamente"],
    "lipschitziana":    ["lipschitziano", "lipschitzianos"],
    "compacto":         ["compacta", "compactas", "compacidade"],
    "completo":         ["completa", "completas", "completude"],
    "conexo":           ["conexa", "conexas", "conexidade"],
    "aberto":           ["aberta", "abertas",
                         # solid compound: HEAD only reaches hyphenated ones
                         "semiaberto", "semiabertos"],
    "convexa":          ["convexo", "convexos"],
    "analítica":        ["analítico", "analíticos"],
    "hermitiano":       ["hermitiana", "hermitianas"],
    "simétrico":        ["simétrica", "simétricas"],
    "cíclico":          ["cíclica", "cíclicas"],
    "gerado":           ["gerada", "geradas"],
    "transposta":       ["transposto"],
    "independentes":    ["independente", "independência"],
    "equipotentes":     ["equipotente"],
    "pontualmente":     ["pontual", "pontuais"],
    # --- irregular plurals: -l -> -is (adjectives in -ável, nouns in -al) ---
    "enumerável":       ["enumeráveis", "enumerabilidade"],
    "somável":          ["somáveis", "somabilidade"],
    "diagonalizável":   ["diagonalizáveis", "diagonalizabilidade"],
    "triangularizável": ["triangularizáveis"],
    "diferenciável":    ["diferenciáveis", "diferenciabilidade"],
    "ideal":            ["ideais"],
    "dual":             ["duais"],
    "diferencial":      ["diferenciais"],
    "potencial":        ["potenciais"],
    # --- irregular plurals: -m -> -ns, -ão -> -ões -------------------------
    "afim":             ["afins"],
    "transposição":     ["transposições"],
    "torção":           ["torções"],
    "polarização":      ["polarizações"],
    "distribuição":     ["distribuições"],
    # --- phrases whose plural is irregular in at least one word ------------
    "espaço afim":               ["espaços afins"],
    "espaço dual":               ["espaços duais"],
    "espaço amostral":           ["espaços amostrais"],
    "base dual":                 ["bases duais"],
    "conjunto enumerável":       ["conjuntos enumeráveis"],
    "família somável":           ["famílias somáveis"],
    "probabilidade condicional": ["probabilidades condicionais"],
    "variável aleatória":        ["variáveis aleatórias"],
    "forma diferencial":         ["formas diferenciais"],
    "normal unitária":           ["normais unitárias"],
    "primeira forma fundamental": ["primeiras formas fundamentais"],
    "polinômio minimal":         ["polinômios minimais"],
    "sistema fundamental":       ["sistemas fundamentais"],
    "convergência normal":       ["convergências normais"],
    "convergência pontual":      ["convergências pontuais"],
    "integral imprópria":        ["integrais impróprias"],
    "integral de linha":         ["integrais de linha"],
    "integral com parâmetro":    ["integrais com parâmetro"],
    "exponencial de matriz":     ["exponenciais de matriz"],
    "função analítica":          ["funções analíticas"],
    "função geradora":           ["funções geradoras"],
    "função geradora de probabilidade":
                                 ["funções geradoras de probabilidade"],
    "função comprimento de arco": ["funções comprimento de arco"],
    "aplicação afim":            ["aplicações afins"],
    "aplicação transposta":      ["aplicações transpostas"],
    "anel quociente":            ["anéis quociente", "anéis quocientes"],
    "volume da bola":            ["volumes de bolas"],
    # --- singulars of terms harvested in the plural ------------------------
    "eventos independentes":     ["evento independente"],
    "matrizes congruentes":      ["matriz congruente"],
    "polinômios de Bernstein":   ["polinômio de Bernstein"],
    "números de Catalan":        ["número de Catalan"],
    "integrais de Wallis":       ["integral de Wallis"],
    "coeficientes de Fourier":   ["coeficiente de Fourier"],
    "somas parciais de Fourier": ["soma parcial de Fourier"],
    "normas equivalentes":       ["norma equivalente"],
}

EXTRA = {
    # book4_en.py's own EXTRA: the phrase names the bilinear form of ch. 12,
    # defined a page before the symmetric endomorphism the bare word reaches.
    "forma bilinear simétrica":     "def:b2:quadratic:def",
    # English links the bare "order" (of a group element), the bare "algebra"
    # and the bare "converges"; each is stoplisted, so the link survives only
    # inside the defining chapter. The Portuguese definitions write these
    # words in a shape the harvester does not pick up (def:b2:structures:algebra
    # emphasises "$K$-álgebra"; the order of an element and the convergence of
    # an improper integral are emphasised inside longer phrases), so they are
    # declared here and left in STOP.
    "ordem":     "def:b2:structures:generated",
    "ordens":    "def:b2:structures:generated",
    "álgebra":   "def:b2:structures:algebra",
    # NOT "converge": STOP is honoured for HARVESTED terms only, so an EXTRA
    # entry links in every chapter. English can afford the bare verb because
    # "converges" is stoplisted and therefore stays inside chapter 9; the
    # Portuguese "converge" would follow every series of chapters 10, 11, 14,
    # 20, 21 and 23 to the improper-INTEGRAL definition. The phrase
    # "integral imprópria" carries the target instead.
    # "unitary" (endomorphism / group / matrix) of ch. 13. Portuguese
    # "unitário" also translates "unit" (vetor unitário, disco unitário, ...),
    # so the ordinary sense is excluded wholesale in EXTRA_PROTECT below.
    "unitário":      "def:b2:hermitian:adjoint",
    "unitária":      "def:b2:hermitian:adjoint",
    "autoadjunto":   "def:b2:hermitian:adjoint",
}

NO_CAPITAL = set()
PRIMARY_OK = set()   # no overloaded word here has a dominant first sense
AMBIG_POLICY = "drop"          # the university convention (books 3, 4, 5)
MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 40

# Spans that must not be touched: fixed phrases in which a defined word carries
# another sense. Portuguese puts its adjectives after the noun, so several
# English ambiguities ("closed form", "convex function") become distinguishable
# phrases here; what needs guarding instead is the gender-agreeing adjective
# and the "unitário = unit" collision.
EXTRA_PROTECT = [
    # --- "unitário/unitária" = UNIT, not unitary ---------------------------
    r'(?:vetor|vetores|versor|versores)\s+unitári[oa]s?',
    r'(?:c[íi]rculo|disco|quadrado|cubo|cilindro|intervalo|segmento|passo|raio|custo|'
    r'tempo|volume|comprimento|determinante|elemento)s?\s+unitári[oa]s?',
    r'(?:esfera|bola|caixa|massa|matriz|coluna|linha|face|velocidade|'
    r'tangente|normal|binormal|carga|área|célula)s?\s+unitári[oa]s?',
    r'de\s+velocidade\s+unitária',
    r'unitári[oa]s?\s+ortogonal',
    r'\bunidade\b',
    # --- "simétrico/simétrica" in its ordinary sense -----------------------
    r'(?:evento|eventos|caso|casos|papel|pap[ée]is|argumento|argumentos|'
    r'raiz|ra[íi]zes|situa[çc][ãa]o|figura|imagem|posi[çc][ãa]o)\s+sim[ée]tric[oa]s?',
    r'sim[ée]tric(?:o|a|os|as)\s+(?:em\s+rela[çc][ãa]o|sob\s+)',
    r'diferen[çc]a\s+sim[ée]trica',
    r'(?:fun[çc][ãa]o|fun[çc][õo]es|polin[óo]mios?)\s+sim[ée]tric[oa]s?',
    r'e\s+sim[ée]tricamente',
    # --- "completo/completa" = full/whole, or the verb "completar" ---------
    r'complet(?:e|a|am|ando|ada|ados|adas)\s+(?:o|os|a|as|um|uma|esta|este)\s+quadrad',
    r'(?:teoria|lista|figura|an[áa]lise|demonstra[çc][ãa]o|prova|volta|'
    r'quadro|panorama|cen[áa]rio|enunciado|resultado|conjunto|sistema|'
    r'grafo|c[íi]rculo|onda)\s+complet[oa]s?',
    r'por\s+completo',
    r'isso\s+completa',
    r'completa\s+(?:a|o)\s+(?:demonstra[çc][ãa]o|prova|argumento)',
    # --- "aberto/aberta" as a verb form ------------------------------------
    r'\babre\b', r'\babrir\b', r'\babriu\b',
    r'problema\s+em\s+aberto',
    # --- "lei" as the name of a result, not the law of a random variable ---
    r'lei(?:s)?\s+(?:fraca|forte|dos\s+grandes|dos\s+eventos|locais|local)',
    r'(?:fraca|forte)\}?\s+dos\s+grandes\s+n[úu]meros',
    # --- a convex FUNCTION / curve is not the convex set of ch. 17 ---------
    # --- "diferencial" as an adjective on a subject ------------------------
    r'(?:c[áa]lculo|geometria|sistemas?|equa[çc](?:[ãa]o|[õo]es))\s+diferen(?:cial|ciais)',
    r'se\s+torna\s+diferencial',
    # --- a physical dimension / a path or block length, not arc length -----
    r'(?:dimens[ãa]o|unidade)\s+de\s+comprimento',
    r'(?:caminhos?|sequ[êe]ncias?|blocos?|textos?)\s+de\s+comprimento',
    r'comprimento\s+(?:da\s+sequ[êe]ncia|do\s+bloco)',
    # --- "independente de $n$" = does not depend on $n$ --------------------
    r'independentes?(?=\s+de\s+\$)',
    r'independentemente\s+(?:de|do|da)\b',
    # --- uniform CONTINUITY / a uniform draw, not uniform convergence ------
    r'uniformemente\s+(?:ao\s+acaso|aleat[óo]ri[oa]s?|cont[íi]nuas?|em\b|'
    r'escolhid[oa]s?|distribu[íi]d[oa]s?)',
    r'(?:escolhendo|escolhid[oa]s?|sortead[oa]s?|extra[íi]d[oa]s?)\s+uniformemente',
    r'(?:portas|caixas|brindes|bolas),\s*uniformemente',
    r'(?<=\\pm1\)\$)\s*uniformemente',
    # --- a POINT singularity / a point mass is not a pointwise statement ---
    r'singularidade[s]?\s+pontuais?',
    r'massa\s+pontual',
    # --- "álgebra linear" is the subject, not a $K$-álgebra ----------------
    r'[áa]lgebras?\s+linear(?:es)?',
    r'[áa]lgebra\s+é\s+mec[âa]nica',
    r'[áa]lgebra\s*:',
    r'[áa]lgebra\s+(?:seguinte|polinomial|direta)',
    # --- ordinary "ordem" in the chapter that defines the order of an element
    r'ordem\s+(?:de\s+(?:soma|integra[çc][ãa]o|grandeza|leitura|'
    r'sorteio|percurso|os\s+fatores)|crescente|decrescente|inversa|'
    r'anti-hor[áa]ria|hor[áa]ria|certa|correta)',
    r'(?:rela[çc](?:[ãa]o|[õo]es)|em|nessa|dessa|na|a)\s+ordem\b',
    r'de\s+ordem\s+(?:dois|tr[êe]s|quatro|superior|\d)',
    r'de\s+ordem(?=\s+\$)',
    r'primeira\s+ordem|segunda\s+ordem|quarta\s+ordem',
    r'ordem(?=\s+\$)',
    # --- "converge" is stoplisted but must not eat the series chapter ------
    r'converge(?=\s+(?:absolutamente|uniformemente|normalmente|pontualmente))',
    r'Abel-som[áa]ve(?:l|is)', r'Ces[àa]ro-som[áa]ve(?:l|is)',
    # a singleton, a unit mean, a unit bisector: "unitário" = unit
    r'conjuntos?\s+unitári[oa]s?',
    r'm[ée]dias?\s+unitári[oa]s?',
    r'bissetri(?:z|zes)\s+unitári[oa]s?',
    # A shared plural head with two coordinated singular adjectives ("os
    # polinômios característico e minimal") is correct Portuguese, but the
    # per-word optional tail matches the head plus the FIRST adjective only,
    # producing "polinômios característico" as a link display and leaving
    # "e minimal" outside it. English links neither word here.
    r'polin[ôóo]mios\s+caracter[íi]stico\s+e\s+minimal',
    # --- ordinary Portuguese in the newly visible text ---------------------
    r'formas?\s+fechadas?(?=\s*\\\[)',
    r'envelopes?,\s*um[a]?\s+em\s+cada',
]
