"""Book 3 -- pt (Brazilian Portuguese). Curation only; the rules live in
tools/termlink/.

Every key is optional: anything left out falls back to the defaults in
tools/link_defined_terms.py.

The reference is the English tree: the set of \\omterm *targets* must be the
same in both, a term must link to the same definition, and a result name that
English leaves unlinked ("teorema de Kummer", "desigualdade de Ptolomeu") must
stay unlinked here. Each word below was read in context in
parts/bachelor-1/pt/ before being kept or dropped.

Portuguese avoids the worst French trap -- "primo" is only the prime, never the
ordinal, and "simetria"/"argumento" are never harvested at all -- but it brings
two of its own.

1. tools/term_config/lang_pt.py sets DERIVE = False and
   WORD_TAIL = (?:e?s)?, which spells "", "s" and "es" but *not* the feminine
   "a"/"as", not the -al -> -ais plural ("ortogonal" -> "ortogonais") and no
   derived noun. So every definition whose head word is an adjective loses half
   its forms unless they are declared in DERIVED, and the definitions that
   emphasise a compound with inline math -- \\emph{contínua em $x_0 \\in I$},
   \\emph{derivável em $x_0 \\in I$} -- are harvested in a form that can never
   match running prose, so the bare adjective has to be added by hand.

2. lang_pt.py set TAIL_ON_EVERY_WORD = False until 2026-08-01, so no *agreed*
   plural of a multiword term was ever generated and all 36 that occur in this
   book had to be declared by hand. The flag is now True, and the 26 whose
   plural (?:e?s)? can spell on every word have been deleted. What remains
   below are the 10 the tail still cannot reach, all irregular in the first
   word, the second, or both:
     -ão -> -ões   aplicação, fração, função, integração, reflexão, relação
     -al -> -ais   vetorial, racional, irracional, binomial
     -vel -> -veis enumerável
   Note "aplicações lineares" is irregular in the head (-ão) and regular in the
   tail (linear -> lineares), and "funções escada" is irregular in the head
   with an invariable apposition: both still need declaring.
"""

# Heads that name a *result*, not a notion: "teorema de ...", "regra de ...".
NOT_A_TERM = ("teorema", "lema", "desigualdade", "fórmula", "critério",
              "princípio", "identidade", "regra", "paradoxo", "problema",
              "estimativa", "conjectura")

# Kept out of the book-wide vocabulary, but STILL linked inside the chapter
# that defines them (STOP is soft): each of these is the notion in its own
# chapter and ordinary Portuguese everywhere else.
STOP = {
    # ch. 3 = the complex conjugate; ch. 11 "multiplique pelo conjugado" (the
    # conjugate expression), ch. 19 the algebraic conjugates, ch. 23
    # conjugating an isometry by a translation. English STOPs "conjugate".
    "conjugado",
    # ch. 5 defines it for a linear ODE; ch. 21 uses the same words for a
    # matrix, which is a different object. English STOPs it too.
    "polinômio característico",
    # ch. 2 = the finite set; everywhere else the ordinary adjective ("um
    # número finito de pontos", "uma união finita", "somas finitas"). The
    # compounds that matter -- "conjunto finito", "dimensão finita" -- are
    # terms of their own and win by being longer. English STOPs "finite".
    "finito", "finita",
}

# Never linked anywhere.
DROP = {
    # --- bare adjectives harvested from a compound; English links only the
    # compound, which is longer and wins on its own.
    # "número algébrico" (weekend problem of ch. 1) leaks "algébrico", but
    # almost every use is the ordinary adjective: "uma estrutura algébrica",
    # "a forma algébrica" of a complex number, "um cálculo algébrico",
    # "comprimentos algébricos" (ch. 24).
    "algébrico",
    # likewise "transcendente": English links only "transcendental number".
    "transcendente",
    # harvested from "ponto crítico"; English links only the compound.
    "crítico",
    # harvested from "soma direta", but "isometria direta" (ch. 23, $\det = 1$),
    # "uma consequência direta", "o sentido direto" are the ordinary adjective.
    "direta",
    # harvested from "matrizes equivalentes", but "as afirmações seguintes são
    # equivalentes" is the commonest sentence in the book.
    "equivalentes",
    # likewise from "matrizes semelhantes": "um raciocínio semelhante".
    "semelhantes",
    # English DROPs the verb "beats"; the Portuguese noun reaches the harvest
    # through \emph{batimentos}\index{batimentos} in ch. 5. pb:b1:diffeq:1
    # keeps its link through "fator de qualidade", exactly as in English.
    "batimentos",
    # ch. 3 defines \emph{argumento}\index{argumento} (of a complex number),
    # but from ch. 4 on the word is pure register: "o mesmo argumento", "um
    # argumento de dimensão", "o argumento diagonal", "argumentos de
    # compacidade". 72 of its uses, against a handful of complex arguments.
    # English DROPs "argument" for exactly this reason.
    "argumento",
    # ch. 20 defines the linear involution \emph{simetria}; from ch. 23 on it
    # is plane geometry ("eixos de simetria", "simetria central") and from
    # ch. 25 the register ("por simetria", "verificação de simetria").
    # English DROPs "symmetry".
    "simetria",

    # --- names of results: the point is to link definitions, not theorems.
    # (NOT_A_TERM only filters index-only harvests; these came in through
    # \emph{...}\index{...} and have to be dropped by hand. English drops the
    # same seven.)
    "teorema de Kummer",
    "fórmula de Legendre",
    "leis de De Morgan",
    "desigualdade de Ptolomeu",
    "estimativa das séries alternadas",
    "equação funcional",
    "equação funcional de Cauchy",
}

# Terms the harvester cannot see, and the Portuguese variants DERIVE = False
# will never generate.
EXTRA = {
    # the definition emphasises the compound -- \emph{contínua em $x_0 \in I$},
    # \emph{derivável em $x_0 \in I$} -- whose pattern is pure inline math and
    # therefore never matches running prose. The bare adjective is what the
    # other twelve chapters actually write.
    "contínuo":        "def:b1:continuity:continuous",
    "contínua":        "def:b1:continuity:continuous",
    "continuamente":   "def:b1:continuity:continuous",
    "derivável":       "def:b1:derivative:def",
    "derivabilidade":  "def:b1:derivative:def",
    # NOT_A_TERM eats "critério de ..."; this one names a notion the book uses
    # as a noun, exactly like English "ratio test".
    "critério da razão": "thm:b1:series:ratio",
    # \index{constante de Euler} occurs twice (exercise 12 of ch. 17 and the
    # weekend problem); the nearest preceding statement is an unrelated
    # telescoping example. English resolves it to the problem, and so must the
    # Portuguese, or the same words would point at two different places.
    "constante de Euler": "pb:b1:series:1",
    # six and eight words: past MAX_TERM_WORDS for the harvest, and English
    # links both.
    "equação diferencial linear de primeira ordem": "def:b1:diffeq:linear1",
    "equação linear de segunda ordem com coeficientes constantes":
        "def:b1:diffeq:linear2",

    # --------------------------------------------- irregular plural compounds
    # With TAIL_ON_EVERY_WORD = True the regular agreed plural of a compound
    # ("números primos", "somas diretas", "curvas polares") is generated and no
    # longer needs declaring; 26 such entries were deleted on 2026-08-01. These
    # 10 remain because (?:e?s)? cannot spell -ão -> -ões, -al -> -ais or
    # -vel -> -veis. Only forms that really occur in parts/bachelor-1/pt/ are
    # listed, and each was verified by counting occurrences against links.
    "espaços vetoriais":        "def:b1:vspaces:def",
    "aplicações lineares":      "def:b1:linmaps:def",
    "números irracionais":      "pb:b1:findim:1",
    "conjuntos enumeráveis":    "pb:b1:logic:1",
    "frações racionais":        "def:b1:fractions:field",
    "relações de equivalência": "def:b1:logic:equiv",
    "coeficientes binomiais":   "def:b1:counting:objects",
    "funções escada":           "def:b1:integration:step",
    "reflexões deslizantes":    "pb:b1:euclid:1",
    "integrações por partes":   "thm:b1:integration:parts",
}

# Linked mid-sentence, never sentence-initially: "Aplicações" opens the section
# that *applies* a theorem -- it is not the map of def:b1:logic:map.
NO_CAPITAL = {"aplicação"}

# WORD_TAIL spells "", "s", "es" -- never the feminine "a"/"as", never the
# -al -> -ais plural, never a derived noun. These are the forms that really
# occur in the book.
DERIVED = {
    "ortogonal":     ["ortogonais", "ortogonalmente"],
    "ortonormal":    ["ortonormais"],
    "aberto":        ["aberta", "abertas"],
    "fechado":       ["fechada", "fechadas"],
    "denso":         ["densa", "densas"],
    "convexa":       ["convexo", "convexos", "convexidade"],
    # only the adjective, as in English: "injeção"/"bijeção"/"injetividade"
    # are ordinary nouns of the register ("uma bijeção de $G$ sobre si
    # mesmo"), and English leaves "injection"/"bijection"/"injectivity"
    # unlinked.
    "injetiva":      ["injetivo"],
    "sobrejetiva":   ["sobrejetivo"],
    "bijetiva":      ["bijetivo"],
    "mônico":        ["mônica", "mônicos", "mônicas"],
    "suplementares": ["suplementar"],
    "conjugado":     ["conjugada", "conjugadas"],
    "divide":        ["dividem"],
    "linear":        ["lineares"],
}

PRIMARY_OK = set()

# The university convention (books 3, 4, 5): a word defined twice earns no
# book-wide link. "posto" is def:b1:findim:rank in ch. 19 and
# def:b1:linmaps:rank in ch. 20, and no first sense dominates -- exactly as in
# English, where "rank" is dropped for the same reason. Under this policy the
# word still links inside each defining chapter, so both targets survive in
# both trees and the two target sets match.
AMBIG_POLICY = "drop"

MAX_TERM_WORDS = 8
MAX_TERM_CHARS = 60

# Spans no link may enter: the uses where a good term means something else.
# NB every space is \s+ -- the sources wrap at 72 columns, and a phrase split
# across two lines ("corpo\nnão enumerável") slips past a literal space and the
# link lands anyway. And no pattern may CONSUME a "$": that inverts inline-math
# masking for the rest of the file (it cost Book 3 a thousand links in English).
EXTRA_PROTECT = [
    # "linear": the linear map, except in these two fixed compounds, which name
    # something else. "aplicação/forma/sistema/recorrência linear" are terms of
    # their own and win by being longer.
    r'álgebra\s+linear', r'combinaç(?:ão|ões)\s+linear(?:es)?',
    # "aplicação": the map, except where it means a *use* of a theorem.
    r'exercícios?\s+de\s+aplicação',
    r'[Aa]plicaç(?:ão|ões)\s+d[eo]s?\s+teorema',
    # "módulo": the modulus of a complex number, except the modulus of
    # continuity of ch. 13, which is a different object.
    r'módulo\s+de\s+(?:continuidade|oscilação)',
    # and, unlike English, Portuguese spells "modulo" and "modulus" the same
    # way: "reduza $X^n$ módulo $D$", "módulo $\pi$", "módulo $n$". The
    # congruence sense is always followed by a formula and the modulus sense
    # never is ("o módulo de $z$", "o módulo é ..."), so a LOOKAHEAD on the
    # opening $ separates them without consuming it.
    r'módulo\s+(?=\$)',
    # "corpo": the field, once out of fifty-odd the ambient line of the Cantor
    # set.
    r'corpo\s+não\s+enumerável',
    # "integral": the integral, except "a forma integral" and "o resto
    # integral" (of Taylor's remainder), where it is an adjective.
    r'forma\s+integral', r'resto\s+integral',
    # "base": the basis of a vector space, except a numeration base ("base
    # $b$", "base $10$", "base dez") -- the "$" is a LOOKAHEAD, never consumed,
    # and the vector bases of this book are always written $\mathcal B$,
    # $(e_i)$, $(1, X, X^2)$, which this pattern does not touch.
    r'[Bb]ases?\s+(?=\$(?:[0-9]+|[abpq])\$)',
    r'[Bb]ases?\s+(?:dez|dois|decimal(?:is)?|binária)',
    # "interior": the topological interior -- "o interior $\mathring A$", "de
    # interior vazio", "um ponto interior a $I$". "no interior de ..." is the
    # ordinary preposition (a point deep inside an interval of convergence).
    r'(?:no|ao|do)\s+interior\s+d(?:o|a|os|as|e\s+um)\b',
    # "livre": the free family, except free fall (ch. 24) -- the physics, not
    # the linear algebra.
    r'queda\s+livre',
]
