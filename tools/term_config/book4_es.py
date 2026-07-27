"""Book 4 (University Year 2) -- Spanish. Curation only; the rules live in
tools/termlink/.

Curated against the English link targets (the parity gate): the set of
`\\omterm` targets under parts/bachelor-2/es must equal the English set, and a
term must reach the same definition it reaches in English.

Two Spanish facts drive most of the table below.

  * tools/term_config/lang_es.py now sets TAIL_ON_EVERY_WORD = True (as
    lang_fr.py always has), so the regular agreed plural of a noun phrase
    ("forma cuadrática" -> "formas cuadráticas") is generated. Only the
    irregular plurals ("función generatriz" -> "funciones generatrices",
    "matriz" -> "matrices", "afín" -> "afines"), the feminines and the
    -idad/-itud nominalisations still need declaring in DERIVED.
  * the harvester used to accept a bare \\emph inside a definition only when it
    agreed with the definition's own English label leaf (def:...:eigen <->
    "eigenvector"), which no translation can match. It now defers to the
    emphases the English twin accepted, so those terms are harvested directly;
    the EXTRA entries below are kept only where they still add a form.
"""

# The default NOT_A_TERM keywords are English ("theorem", "lemma", ...), so the
# harvester filters "Parseval's theorem" out of the English book but would let
# the Spanish "identidad de Parseval", "regla de la cadena", "teorema
# espectral", "desigualdad de Bessel" through -- result-names English never
# links. Filtering on the Spanish heads restores parity. Bare "ley" is NOT
# listed (it is the distribution/law DEFINITION, def:b2:randomvar:law); only
# the phrase "ley de" is filtered.
NOT_A_TERM = ("teorema", "lema", "desigualdad", "fórmula", "criterio",
              "principio", "identidad", "regla", "ley de", "paradoja",
              "problema")

# Soft: a stoplisted word is still linked inside the chapter that defines it.
# One-for-one with book4_en.py's STOP.
STOP = {
    "orden",                       # "en orden de", "orden de sumación"
    "equivalente", "equivalentes",  # only NORMS are defined equivalent
    "álgebra",                     # "álgebra lineal" >> $K$-álgebra
    "converge",                    # defined for improper integrals (ch. 9)
    "alternado", "alternada",      # alternating form (ch. 2) vs series (ch. 7)
    "signatura",                   # of a permutation (ch. 1) vs of a form (ch. 12)
    "exacto", "exacta",            # "forma exacta" (ch. 20) vs "el valor exacto"
    "regular", "regulares",        # regular point/arc (ch. 18) vs surface (ch. 19)
    "equivalencia",                # equivalence relation (ch. 1) vs of norms (ch. 5)
}

# Hard: never a link anywhere.
DROP = {
    # Named RESULTS, not notions. English filters them through NOT_A_TERM or
    # drops them by hand; in Spanish each reaches the harvester through an
    # \emph{...}\index{...} pair, which bypasses NOT_A_TERM.
    "fórmula límite de Gauss",                      # ch. 9 problem
    "teorema de Korovkin",                          # ch. 10 problem
    "desigualdad de Hadamard",                      # ch. 12 problem
    "teorema mín-máx de Courant--Fischer",          # ch. 13 problem
    "desigualdades de perturbación de Weyl",
    "fórmula de Jacobi",                            # ch. 15 problem
    "cota de Chernoff", "desigualdades de concentración",   # ch. 22 problem
    "fenómeno de Gibbs",     # named in a figure caption, explained elsewhere
    "punto central",         # pb:b2:affine:1 -- EN "centerpoint" is not harvested
    # English never links the bare adjoint: it is introduced in ch. 12 (Euclidean)
    # AND in ch. 13 (Hermitian), so English drops it as ambiguous. The Spanish
    # ch. 13 definition writes "adjunto" without an \index, which slips past the
    # ambiguity test; drop it by hand to keep the two books in step.
    "adjunto",
    # STOP would still link these in the chapter that defines them; there even
    # that chapter mixes the senses. Their PHRASES survive ("forma cerrada",
    # "conjunto convexo", "envoltura convexa").
    "cerrado", "cerrada",     # ch. 20 alone: forma cerrada, arco cerrado, disco cerrado
    "convexidad",             # of a SET (ch. 17) vs of a FUNCTION (Jensen, ch. 8)
    # adverbs whose ordinary-Spanish sense is the only one used
    "simétricamente", "cíclicamente",
}

# Spanish derivations the shared morphology does not generate: feminine
# agreement, the -idad/-itud nominalisations English spells -ness / -ity, and
# the irregular plurals the regular -s/-es tail cannot reach. Regular phrase
# plurals are generated now that TAIL_ON_EVERY_WORD is True and are no longer
# listed. A form is kept only if it really occurs in the book.
DERIVED = {
    # --- adjectives: feminine, plural, and the abstract noun -----------------
    "abierto":       ["abierta", "abiertas"],
    "compacto":      ["compacta", "compactas", "compacidad"],
    # NOT the feminine: every "completa/completas" in the book is either the
    # verb ("esto completa la demostración") or ordinary "full" ("la teoría
    # completa", "onda completa"). The complete objects here are all masculine
    # (espacio, subconjunto, cuerpo).
    "completo":      ["completitud"],
    "conexo":        ["conexa", "conexas", "conexidad"],
    "convexo":       ["convexa", "convexas"],
    "continua":      ["continuo", "continuos", "continuidad"],
    "lipschitziana": ["lipschitziano", "lipschitzianos"],
    "analítica":     ["analítico", "analíticos", "analíticamente"],
    "simétrico":     ["simétrica", "simétricas"],
    "hermítico":     ["hermítica", "hermíticas"],
    "unitario":      ["unitaria", "unitarias"],
    "cíclico":       ["cíclica", "cíclicas"],
    "afín":          ["afines"],
    "traspuesta":    ["traspuesto", "traspuestas"],
    "diferenciable": ["diferenciabilidad"],
    "diagonalizable": ["diagonalizabilidad"],
    "sumable":       ["sumabilidad"],
    "numerable":     ["numerabilidad"],
    "independientes": ["independiente", "independencia"],
    "equipotentes":  ["equipotente"],
    # English links the adjective "pointwise" as well as the adverb; Spanish
    # splits them into "puntualmente" (harvested) and "puntual/puntuales".
    "puntualmente":  ["puntual", "puntuales"],
    # --- phrase plurals (and the singulars of terms harvested plural) --------
    "aplicación afín":        ["aplicaciones afines"],
    "función analítica":      ["funciones analíticas"],
    "función generatriz":     ["funciones generatrices"],
    "función generatriz de probabilidad":
                              ["funciones generatrices de probabilidad"],
    "integrales de Wallis":   ["integral de Wallis"],
    "matriz jacobiana":       ["matrices jacobianas"],
    "transposición":          ["transposiciones"],
    "números de Catalan":     ["número de Catalan"],
    "polinomios de Bernstein": ["polinomio de Bernstein"],
}

EXTRA = {
    # def:b2:reduction:eigen writes "vector propio" and "subespacio propio" as
    # bare \emph{}. English harvests its "eigenvector"/"eigenspace" only because
    # they start with the label leaf "eigen"; the Spanish words cannot.
    "vector propio":        "def:b2:reduction:eigen",
    "vectores propios":     "def:b2:reduction:eigen",
    "subespacio propio":    "def:b2:reduction:eigen",
    "subespacios propios":  "def:b2:reduction:eigen",
    # def:b2:structures:generated writes "generado por" as a bare \emph{};
    # English links its "generated" through the same leaf rule.
    "generado":             "def:b2:structures:generated",
    "generada":             "def:b2:structures:generated",
    "generados":            "def:b2:structures:generated",
    "generadas":            "def:b2:structures:generated",
    # book4_en.py's own EXTRA: the phrase names the bilinear form of ch. 12,
    # defined a page before the symmetric endomorphism the bare word reaches.
    "forma bilineal simétrica":    "def:b2:quadratic:def",
    "formas bilineales simétricas": "def:b2:quadratic:def",
}

NO_CAPITAL = set()
PRIMARY_OK = set()   # no overloaded word here has a dominant first sense
AMBIG_POLICY = "drop"          # the university convention (books 3, 4, 5)
MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 40

# Spans that must not be touched: fixed phrases in which a defined word carries
# another sense. The Spanish list is short because Spanish puts its adjectives
# after the noun, so most English ambiguities ("closed form", "convex
# function") become distinguishable phrases here rather than bare words.
EXTRA_PROTECT = [
    # "ley" as the name of a result, not the law of a random variable
    r'ley(?:es)?\s+(?:débil|fuerte|de\s+los\s+grandes|de\s+los\s+sucesos|locales)',
    r'(?:débil|fuerte)\}?\s+de\s+los\s+grandes\s+números',
    # a convex FUNCTION / curve is not the convex set of ch. 17. Spanish puts
    # the adjective last, so the noun ("funciones convexas") or the copula
    # after a math symbol ("$\varphi$ es convexa") is what marks the sense.
    r'funci(?:[óo]n|ones)\}?\s+convexas?',
    r'curvas?\s+(?:\w+\s+)?convexas?',
    r'convexas?\s+sobre',
    r'(?<=\$)\s+(?:es\s+)?convexa\b',
    # "diferencial" as an adjective on a subject, not the differential of a map
    r'(?:c[áa]lculo|geometr[íi]a|sistemas?|ecuaci[óo]n(?:es)?)\s+diferencial(?:es)?',
    r'se\s+vuelve\s+ahora\s+diferencial',
    # geographic longitude / a physical dimension / a combinatorial length are
    # not the arc length of ch. 18
    r'(?:y\s+en|las)\s+longitudes',
    r'(?:unidad|dimensi[óo]n)\s+de\s+longitud',
    # "independiente de $n$" = does not depend on $n$
    r'independientes?(?=\s+de\s+\$)',
    # uniform CONTINUITY / a uniform draw, not uniform convergence
    r'uniformemente\s+(?:al\s+azar|continuas?|en\b)',
    r'de\s+manera\s+uniforme\s+(?:al\s+azar|en\b)',
    r'uniformemente\s+aleatori[oa]s?',
    r'(?:eligiendo|elegidos?|elegidas?|extrae|extra[íi]d[oa]s?|sorteados?)\s+uniformemente',
    r'(?:distintos|distintas|puertas|cajas),\s*uniformemente',
    r'(?<=\\pm1\)\$)\s*uniformemente',
    # a POINT singularity is not a pointwise statement
    r'singularidad(?:es)?\s+puntual(?:es)?',
    # "álgebra lineal" is the subject, not a $K$-algebra
    r'[áa]lgebras?\s+lineal(?:es)?',
    # ordinary Spanish "orden" in the chapter that defines the order of a group
    # element (a stoplisted word is still linked there)
    r'orden\s+(?:de\s+(?:sumaci[óo]n|los\s+factores|lectura)|creciente|decreciente|inverso)',
    r'relaci(?:[óo]n|ones)\s+de\s+orden',
    # a path/run of length n, not the arc length of ch. 18
    r'(?:caminos?|rachas?)\s+de\s+longitud',
    # the mirrored event of a random walk, not a symmetric endomorphism
    r'sucesos?\s+sim[ée]tricos?',
    # "por completo" = entirely; and the ordinary "full/whole" adjective on a
    # masculine noun (the feminine is excluded from DERIVED altogether)
    r'por\s+completo',
    r'(?:escenario|paquete|an[áa]lisis|conos?|panorama|cuadro)\s+completos?',
    # "unitario" also translates "unit": a unit vector / unit tangent is not a
    # unitary endomorphism, and a "conjunto unitario" is a singleton.
    r'(?:vectores?|tangentes?|bisectrices|bisectriz|conjuntos?)\s+unitarios?',
    r'(?:tangentes?|bisectriz|normales?)\s+unitarias?',
    r'(?:columnas|filas)\s+(?:no\s+)?son\s+unitarias',
    r'\\cap\s+W_k\$\s+unitario',
]
