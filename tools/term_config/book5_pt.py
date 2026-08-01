"""Book 5 -- pt. Curation only; the rules live in tools/termlink/.

University Year 3: AMBIG_POLICY drop (no spiral nearest-preceding). At this
level a word two chapters define with different meanings is a genuine
ambiguity, not a re-definition of the same notion, and a wrong link costs the
reader more than a missing one; the harvest still links such a word inside the
chapter that pins it down (the `local` mechanism), which is exactly what
English does.

Curated against the English link targets (parity gate): the set of \\omterm
first arguments used in parts/bachelor-3/pt must coincide with the set used in
parts/bachelor-3, and each Portuguese term must reach the same definition as
its English counterpart. Do not edit book5_en.py (golden fixture).

Three Portuguese-specific jobs, on top of mirroring book5_en's STOP:

* lang_pt sets TAIL_ON_EVERY_WORD = True (since 2026-08-01) and DERIVE = False,
  so regular agreed plurals of a phrase are generated ("espaco compacto" ->
  "espacos compactos") but nothing else is. What still has to be declared in
  EXTRA is what the "(?:e?s)?"-per-word rule cannot spell: irregular plurals
  (-ao/-oes, -al/-ais, -vel/-veis, anel/aneis), gender variants
  ("continuo"/"continua" -- WORD_TAIL covers number, never gender), and the
  abstract nouns English reaches through DERIVED ("continuity", "holomorphy",
  ...). 42 entries that the flag had made necessary, or that were plain dead
  weight, were deleted when it flipped.
* Portuguese homographs English keeps apart: "módulo" is both \\emph{module}
  and \\emph{modulus}, "grau" both the degree of an extension and the degree of
  a polynomial, "base" both a basis of a topology and a basis of a vector
  space, "simples" both a simple group and a simple function. They go to STOP,
  which still links them inside the chapter that defines them.
* "índice de rotação" translates both English index entries -- "index of a
  path" (ch. 16) and "winding number" (ch. 21) -- so it is ambiguous in
  Portuguese where English was not. Left to the `local` rule, which reproduces
  the English behaviour: the phrase links to def:b3:forms:winding inside the
  differential-forms chapter and to def:b3:holomorphic:index inside the
  holomorphic-functions one.

Two EXTRA_PROTECT rules, both learned the hard way elsewhere in the series:

* Never consume a `$`. The protect list is one alternation scanned left to
  right, so a pattern that eats an opening dollar leaves the inline-math rule
  pairing the closing one with the next formula's opening dollar, and every
  span after it is masked inside out -- silently, with no error and a collapsed
  link count. Match a trailing `$` with a lookahead `(?=\\$)`, never a literal.
* Never write a literal space. The list is compiled with re.S and LaTeX source
  wraps lines, so a literal space stops matching the moment the phrase
  straddles a line break -- latently, after any prose rewrap. Write `\\s+`.
"""

NOT_A_TERM = ("teorema", "lema", "desigualdade", "fórmula", "critério",
              "princípio", "identidade", "regra", "lei de", "paradoxo",
              "problema")

# Portuguese mirror of book5_en.STOP: ordinary words, or words whose sense
# changes by chapter. Soft: still linked inside the defining chapter.
STOP = {
    # book5_en: at, all, some, total, shape, section, direct, simple, stable,
    # equivalent, integer, index, law, generated, converges, events, a.e.,
    # dense, normal, maximal, principal, radical, content, characteristic,
    # invariant, bounded, action, basis, degree, free, Euclidean, separable,
    # closed, exact, compact, prime, irreducible, primitive, product,
    # quotient, subspace, path, boundary, interior
    "total", "totais",
    "forma", "formas",
    "seção", "seções",
    "direto", "direta", "diretos", "diretas",
    "simples",
    "estável", "estáveis",
    "equivalente", "equivalentes", "equivalência",
    "inteiro", "inteira", "inteiros", "inteiras",
    "índice", "índices",
    "lei", "leis",
    "gerado", "gerada", "gerados", "geradas",
    "converge",
    "evento", "eventos",
    "quase em toda parte",
    "denso", "densa", "densos", "densas",
    "normal", "normais",
    "maximal", "maximais",
    "principal", "principais",
    "radical", "radicais",
    "conteúdo", "conteúdos",
    "característica", "característico", "características",
    "invariante", "invariantes",
    "limitado", "limitada", "limitados", "limitadas",
    "ação", "ações",
    "base", "bases",
    "grau", "graus",
    "livre", "livres",
    "euclidiano", "euclidiana", "euclidianos", "euclidianas",
    "separável", "separáveis",
    "fechado", "fechada", "fechados", "fechadas",
    "exato", "exata", "exatos", "exatas",
    "compacto", "compacta", "compactos", "compactas",
    "primo", "prima", "primos", "primas",
    "irredutível", "irredutíveis",
    "primitivo", "primitiva", "primitivos", "primitivas",
    "produto", "produtos",
    "quociente", "quocientes",
    "subespaço", "subespaços",
    "caminho", "caminhos",
    "bordo", "bordos",
    "interior", "interiores",
    # Portuguese homographs English never has to arbitrate
    "módulo", "módulos",          # module vs. modulus
    "argumento", "argumentos",    # argument of a complex number vs. proof
    "unitário", "unitária",       # unit vector vs. unital ring
    "simetria", "simetrias",
    "ordem", "ordens",
    "álgebra", "álgebras",
    "regular", "regulares",
    "primeiro", "primeira",
    "finito", "finita", "finitos", "finitas",
    "integral", "integrais",
    "norma", "normas",
}

# overloaded words whose first sense dominates the book, so they may be linked
# outside the chapter that pins them down (book5_en.PRIMARY_OK)
PRIMARY_OK = {
    "compacto", "compacta", "compactos", "compactas",
    "fechado", "fechada", "fechados", "fechadas",
    "caminho", "caminhos",
    "bordo", "bordos",
    "interior", "interiores",
    "irredutível", "irredutíveis",
}

# Harvested terms English never cross-links (parity gate): Portuguese \index
# entries that name a *result* rather than a notion, or that English writes as
# a phrase its own NOT_A_TERM filter refuses.
DROP = {
    "régua e compasso",                      # cor:b3:galois:impossible
    "quíntica, insolubilidade",              # cor:b3:galois:quintic
    "grupo abeliano, estrutura",             # cor:b3:modules:abelian
    "espaços de sequências $\\ell^p$",       # def:b3:banach:lp
    "convergência em distribuição",          # def:b3:clt:cid
    "polinômio ciclotômico",                 # def:b3:galois:cyclotomic
    "espaço $L^p$",                          # def:b3:lp:space
    "$\\sigma$-álgebra de Borel",            # def:b3:measure:borel
    "% $\\sigma$-álgebra de Borel",
    "$\\lambda$-sistema",                    # def:b3:measure:dynkin
    "$\\pi$-sistema",
    "$\\sigma$-álgebra",                     # def:b3:measure:sigmaalgebra
    "convergência de variáveis aleatórias",  # def:b3:probability:modes
    "medida de Lebesgue em $\\R^d$",         # def:b3:product:lebesgue
    "$\\sigma$-álgebra produto",             # def:b3:product:sigma
    "gaussiana, transformada de Fourier",    # ex:b3:fouriertransform:gaussian
    "lei gaussiana",                         # ex:b3:probability:laws
    "máximo divisor comum",                  # lem:b3:rings:bezout
    "ortonormalização de Gram--Schmidt",     # prop:b3:hilbert:gramschmidt
    "raio numérico",                         # prop:b3:spectral:sanorm
    "duais dos espaços de sequências",       # thm:b3:banach:duals
    "série de Fourier, divergência",         # thm:b3:banach:fourierdiverge
    "função característica, injetividade",   # thm:b3:clt:injectivity
    "$\\dd^2 = 0$",                          # thm:b3:forms:dsquare
    "$p$-grupo",                             # thm:b3:groups:pfixed
    "teorema de Morera",                     # thm:b3:holomorphic:weierstrassconv
    "integrais com parâmetro",               # thm:b3:lebesgue:paramcont
    "regularidade da medida de Lebesgue",    # thm:b3:measure:regularity
    "conjunto não mensurável de Vitali",     # thm:b3:measure:vitali
    "sequências independentes, existência",  # thm:b3:probability:existence
    "lei dos grandes números (forte)",       # thm:b3:probability:slln
    "lei dos grandes números (fraca)",       # thm:b3:probability:wlln
    "função Beta",                           # thm:b3:product:ballvolume
    "medida imagem",
    "volume da bola unitária",
    "mudança linear de variáveis",           # thm:b3:product:linearchange
    "lema do tubo",                          # thm:b3:topology:tychonoff
}

# What the "(?:e?s)?"-on-every-word rule still cannot spell. Two classes only,
# each entry checked against the rule rather than assumed:
#
#   * irregular plurals -- "-ão/-ões" (representação, função, aplicação,
#     extensão, solução), "-al/-ais" (ideal, normal, maximal, dual,
#     diferencial), "-vel/-veis" (irredutível, solúvel, variável, mensurável,
#     integrável, derivável), "anel/anéis". The rule would ask for
#     "representaçãos", "normales", "irredutívels": never written, never
#     matched. (Regular "-r/-res" IS generated -- "operador" + "es" -- so
#     "operadores" is not declared here.)
#   * gender variants -- WORD_TAIL covers number, never gender, so a term
#     harvested as "contínua" is unreachable as "contínuo"/"contínuos", and the
#     abstract noun ("continuidade") is not a suffix of either.
EXTRA = {
    # -- irregular plurals, alone or inside a phrase --
    "representações": "def:b3:representations:rep",
    "ideais": "def:b3:rings:ideal",
    "anéis quocientes": "def:b3:rings:ideal",
    "elementos irredutíveis": "def:b3:rings:divisibility",
    "soluções maximais": "thm:b3:ode:maximal",
    "extensões de Galois": "def:b3:galois:galois",
    "solúveis por radicais": "def:b3:galois:radical",
    "reflexivo": "rem:b3:banach:bidual",
    "reflexiva": "rem:b3:banach:bidual",
    "reflexivas": "rem:b3:banach:bidual",
    "gaussiana": "def:b3:clt:gaussianvector",
    "espaços duais": "def:b3:banach:operator",
    "formas diferenciais": "def:b3:forms:diffform",
    "funções holomorfas": "def:b3:holomorphic:holo",
    "funções harmônicas": "prop:b3:conformal:harmonicholo",
    "funções mensuráveis": "def:b3:lebesgue:measurable",
    "funções integráveis": "def:b3:lebesgue:l1",
    "funções meromorfas": "def:b3:residues:singularities",
    "funções simples": "def:b3:lebesgue:simple",
    "funções características": "def:b3:clt:cf",
    "grupos solúveis": "def:b3:groups:derived",
    "ideais primos": "def:b3:rings:primemaximal",
    "ideais maximais": "def:b3:rings:primemaximal",
    "representações irredutíveis": "def:b3:representations:rep",
    "subgrupos normais": "def:b3:groups:normal",
    "variáveis aleatórias": "def:b3:probability:space",
    "aplicações conformes": "def:b3:conformal:conformal",
    "aplicações contínuas": "def:b3:topology:continuity",
    # -- structural terms English links but the harvest misses --
    "bordo de uma subvariedade": "def:b3:forms:boundary",
    "funções em parte alguma deriváveis": "thm:b3:complete:nowherediff",
    # -- continuity / homeomorphism --
    "contínuo": "def:b3:topology:continuity",
    "contínuos": "def:b3:topology:continuity",
    "continuidade": "def:b3:topology:continuity",
    "continuamente": "def:b3:topology:continuity",
    "homeomorfo": "def:b3:topology:continuity",
    "homeomorfa": "def:b3:topology:continuity",
    "homeomorfos": "def:b3:topology:continuity",
    "homeomorfas": "def:b3:topology:continuity",
    # -- compactness / completeness / connectedness --
    "compacidade": "def:b3:topology:compact",
    "completa": "def:b3:complete:complete",
    "completas": "def:b3:complete:complete",
    "completude": "def:b3:complete:complete",
    "conexa": "def:b3:topology:connected",
    "conexas": "def:b3:topology:connected",
    "conexidade": "def:b3:topology:connected",
    "conexa por caminhos": "def:b3:topology:pathconnected",
    "conexas por caminhos": "def:b3:topology:pathconnected",
    "equicontínuo": "def:b3:complete:equicontinuous",
    "simplesmente conexa": "def:b3:conformal:simplyconnected",
    "simplesmente conexas": "def:b3:conformal:simplyconnected",
    # -- measure and integration --
    "mensuráveis": "def:b3:lebesgue:measurable",
    "mensurabilidade": "def:b3:lebesgue:measurable",
    "integráveis": "def:b3:lebesgue:l1",
    "integrabilidade": "def:b3:lebesgue:l1",
    # -- complex analysis --
    "holomorfo": "def:b3:holomorphic:holo",
    "holomorfos": "def:b3:holomorphic:holo",
    "holomorfia": "def:b3:holomorphic:holo",
    "holomorficamente": "def:b3:holomorphic:holo",
    "meromorfo": "def:b3:residues:singularities",
    "meromorfos": "def:b3:residues:singularities",
    "conformemente": "def:b3:conformal:conformal",
    # -- algebra --
    "algébrica": "def:b3:galois:algebraic",
    "algébricas": "def:b3:galois:algebraic",
    "algebricamente": "def:b3:galois:algebraic",
    "perfeito": "prop:b3:galois:perfect",
    "perfeita": "prop:b3:galois:perfect",
    "perfeitas": "prop:b3:galois:perfect",
    "solúveis": "def:b3:groups:derived",
    "solubilidade": "def:b3:groups:derived",
    "caracteres": "def:b3:representations:character",
    "topológico": "def:b3:topology:topology",
    "topológica": "def:b3:topology:topology",
    "topológicos": "def:b3:topology:topology",
    "topológicas": "def:b3:topology:topology",
    "noetheriana": "def:b3:rings:noetherian",
    "construtíveis": "def:b3:galois:constructible",
    # -- operators and probability --
    "autoadjunta": "def:b3:spectral:selfadjoint",
    "autoadjuntas": "def:b3:spectral:selfadjoint",
    "autoadjunção": "def:b3:spectral:selfadjoint",
    "gaussianas": "def:b3:clt:gaussianvector",
    "independente": "def:b3:probability:independence",
    "orientável": "def:b3:forms:orientation",
    "orientáveis": "def:b3:forms:orientation",
    "orientabilidade": "def:b3:forms:orientation",
}

NO_CAPITAL = set()
DERIVED = {}
AMBIG_POLICY = "drop"
MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 40
# "por completo" is the adverb "entirely", not the adjective "complete".
# No literal space, no consumed `$` -- see the module docstring.
EXTRA_PROTECT = [r'por\s+completo']
