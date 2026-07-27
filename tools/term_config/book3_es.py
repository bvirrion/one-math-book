"""Book 3 -- es. Curation only; the rules live in tools/termlink/.

Every key is optional: anything left out falls back to the defaults in
tools/link_defined_terms.py.

Spanish avoids the worst French trap -- "primo" is only the prime, never the
ordinal -- but it brings its own. tools/term_config/lang_es.py sets
DERIVE = False and WORD_TAIL = (?:e?s)?, which spells "", "s" and "es" but
*not* the feminine "a"/"as" and no derived noun. So every definition whose
head word is an adjective loses half its forms unless they are declared:
continuo/continua, convexo/convexidad, inyectiva/inyectivo/inyectividad/
inyeccion, and so on. And the definitions that emphasise a compound with
inline math -- \\emph{continua en $x_0 \\in I$}, \\emph{derivable en $x_0 \\in
I$} -- are harvested in a form that can never match running prose, so the
bare adjective has to be added by hand.

The reference is the English tree: the set of \\omterm *targets* must be the
same in both, a term must link to the same definition, and a result name that
English leaves unlinked ("Kummer's theorem", "Ptolemy's inequality") must stay
unlinked here. Each word below was read in context in parts/bachelor-1/es/
before being kept or dropped.
"""

# Heads that name a *result*, not a notion: "teorema de ...", "regla de ...".
NOT_A_TERM = ("teorema", "lema", "desigualdad", "fórmula",
              "principio", "identidad", "regla", "ley de", "leyes de",
              "paradoja", "estimación", "conjetura")

# Kept out of the book-wide vocabulary, but STILL linked inside the chapter
# that defines them (STOP is soft): each of these is the notion in its own
# chapter and ordinary Spanish everywhere else.
STOP = {
    # ch. 2 = the finite set; elsewhere "un número finito de puntos", "una
    # unión finita". "conjunto finito" and "dimensión finita" are terms of
    # their own.
    "finito", "finita",
    # ch. 8 = the monic polynomial; from ch. 23 on it is a *unit* vector.
    "unitario", "unitaria",
    # ch. 20 = the linear involution; from ch. 23 on plane geometry ("ejes de
    # simetría") and from ch. 25 the register ("por simetría").
    "simetría",
}

# Never linked anywhere.
DROP = {
    # Result names that reach the harvest through \emph{}\index{} and so
    # bypass NOT_A_TERM. English leaves every one of them unlinked.
    "teorema de Kummer",
    "fórmula de Legendre",
    "desigualdad de Ptolomeo",
    "estimación de las series alternadas",
    "leyes de De Morgan",
    "ecuación funcional",
    "ecuación funcional de Cauchy",
    # harvested from "suma directa", but "isometría directa" (ch. 23, $\det =
    # 1$), "una consecuencia directa", "un estudio directo" are the ordinary
    # adjective. "suma directa" is a term of its own and wins by being longer.
    "directa", "directo",
    # harvested from "matrices equivalentes", but "las afirmaciones siguientes
    # son equivalentes" is the commonest sentence in the book.
    "equivalentes",
    # likewise from "matrices semejantes": "triángulos semejantes", "un
    # razonamiento semejante".
    "semejantes",
    # harvested from "número algebraico" (weekend problem of ch. 1), but almost
    # every use is the ordinary adjective: "una estructura algebraica", "la
    # forma algebraica" of a complex number, "un cálculo algebraico".
    "algebraico",
    # likewise "trascendente": English links only "transcendental number".
    "trascendente",
    # harvested from "punto crítico"; English links only the compound.
    "crítico",
    # ch. 3 defines \emph{argumento}\index{argumento} (of a complex number),
    # which English does not harvest at all. STOP would be too soft: the
    # register use lives inside ch. 3 itself ("el mismo argumento, hecho
    # dentro de $\mathbb U_n$"), so the word has to go entirely.
    "argumento",
}

# Terms the harvester cannot see, and the Spanish variants DERIVE = False will
# never generate.
EXTRA = {
    # the definition emphasises "derivable en $x_0 \in I$", pure inline math,
    # so the bare adjective -- what the other twelve chapters write -- is never
    # harvested at all.
    "derivable":      "def:b1:derivative:def",
    "derivabilidad":  "def:b1:derivative:def",
    # def:b1:euclid:orthogonal is harvested only through "complemento
    # ortogonal" / "familia ortonormal"; the bare adjective carries the notion
    # in chapters 23--25 (English links "orthogonal" and "orthogonally").
    "ortogonal":      "def:b1:euclid:orthogonal",
    "ortogonalidad":  "def:b1:euclid:orthogonal",
    "ortogonalmente": "def:b1:euclid:orthogonal",
    # \emph{traspuesta} shares its definition with \index{traza}; only the
    # trace survives the harvest.
    "traspuesta":     "def:b1:matrices:transpose",
    "trasposición":   "def:b1:matrices:transpose",
    # NOT_A_TERM eats "criterio de ..."; this one names a notion the book uses
    # as a noun, exactly like English "ratio test".
    "criterio del cociente": "thm:b1:series:ratio",
    # "ley de" is a result head, but the tower law is quoted as an object.
    "ley de la torre": "pb:b1:findim:1",
    # def:b1:logic:equiv is harvested through "relación de equivalencia" only.
    "clase de equivalencia": "def:b1:logic:equiv",
    # six words: past MAX_TERM_WORDS for the harvest, and English links it.
    "ecuación diferencial lineal de primer orden": "def:b1:diffeq:linear1",
    # \index{constante de Euler} occurs twice (the exercise of ch. 17 and the
    # weekend problem); English resolves it to the problem, and so must the
    # Spanish, or the same words would point at two different places.
    "constante de Euler": "pb:b1:series:1",

    # ---------------------------------------------------------------- plurals
    # lang_es.py now sets TAIL_ON_EVERY_WORD = True (as lang_fr.py always has),
    # so the regular agreed plural of a compound -- "curvas parametrizadas",
    # "aplicaciones lineales", "puntos críticos" -- is generated and no longer
    # needs declaring. What remains below are the forms the plural tail cannot
    # reach: irregular plurals ("raíz" -> "raíces", "afín" -> "afines"),
    # gender changes and the -idad/-itud nominalisations. Only the forms that
    # really occur in parts/bachelor-1/es/ are listed.
    "funciones escalonadas":   "def:b1:integration:step",
    "puntos críticos":         "thm:b1:multivar:critical",
    "puntos de retroceso":     "ex:b1:curves:astroid",
    "números trascendentes":   "pb:b1:logic:1",
    "números algebraicos":     "pb:b1:logic:1",
    "espacios vectoriales":    "def:b1:vspaces:def",
    "aplicaciones lineales":   "def:b1:linmaps:def",
    "coeficientes binomiales": "def:b1:counting:objects",
    "partes enteras":          "thm:b1:reals:floor",
    "sumas directas":          "def:b1:vspaces:sum",
    "cotas superiores":        "def:b1:reals:bounds",
    "derivadas parciales":     "def:b1:multivar:partial",
    "fracciones racionales":   "def:b1:fractions:field",
    "integraciones por partes": "thm:b1:integration:parts",
    "curvas parametrizadas":   "def:b1:curves:def",
    "curvas polares":          "def:b1:curves:polar",
    "productos escalares":     "def:b1:euclid:def",
    "puntos de silla":         "met:b1:multivar:monge",
    "sistemas lineales":       "def:b1:det:system",
    "cambios de variable":     "thm:b1:integration:parts",
    "clases de equivalencia":  "def:b1:logic:equiv",
    "dominios de integridad":  "def:b1:structures:field",
    "espacios euclídeos":      "def:b1:euclid:def",
    "formas lineales":         "def:b1:linmaps:forms",
    "leyes de composición":    "def:b1:structures:law",
    "números primos":          "def:b1:arith:prime",
    "conjuntos abiertos":      "def:b1:topology:open",
    "conjuntos cerrados":      "def:b1:topology:closed",
    "conjuntos finitos":       "def:b1:counting:card",
    "familias libres":         "def:b1:vspaces:free",
    "números irracionales":    "pb:b1:findim:1",
    "rectas de regresión":     "pb:b1:multivar:1",
    "reflexiones deslizantes": "pb:b1:euclid:1",
    "relaciones de equivalencia": "def:b1:logic:equiv",
    "series geométricas":      "ex:b1:series:geometric",
    "sucesiones recurrentes":  "met:b1:seq:recurrent",
}

# Linked mid-sentence, never sentence-initially: "Aplicación." opens a
# paragraph that *applies* a theorem -- it is not the map of def:b1:logic:map.
NO_CAPITAL = {"aplicación"}

# WORD_TAIL spells "", "s", "es" -- never the feminine "a"/"as", never a
# derived noun. These are the forms that really occur in the book.
DERIVED = {
    "continuidad":    ["continuo", "continua"],
    "convexa":        ["convexo", "convexidad"],
    "inyectiva":      ["inyectivo", "inyectividad", "inyección"],
    "sobreyectiva":   ["sobreyectivo", "sobreyectividad", "sobreyección"],
    "biyectiva":      ["biyectivo", "biyectividad", "biyección"],
    "divide":         ["dividen"],
    "suplementarios": ["suplementario"],
    "conjugado":      ["conjugada"],
    "denso":          ["densa"],
    "abierto":        ["abierta"],
    "cerrado":        ["cerrada"],
}

PRIMARY_OK = set()

AMBIG_POLICY = "drop"          # the university convention (books 3, 4, 5)

MAX_TERM_WORDS = 8
MAX_TERM_CHARS = 60

# Spans no link may enter: the uses where a good term means something else.
# NB every space is \s+ -- the sources wrap at 72 columns, and a phrase split
# across two lines ("cuerpo\nno numerable") slips past a literal space and the
# link lands anyway. And no pattern may CONSUME a "$": that inverts inline-math
# masking for the rest of the file.
EXTRA_PROTECT = [
    # "lineal": the linear map, except in these two fixed compounds, which name
    # something else. "aplicación/forma/sistema/recurrencia lineal" are terms
    # of their own and win by being longer.
    r'álgebra\s+lineal', r'combinaci(?:ón|ones)\s+lineal(?:es)?',
    # "aplicación": the map, except where it means a *use* of a theorem.
    r'ejercicios?\s+de\s+aplicación', r'única\s+aplicación\s+de',
    # "módulo": the modulus of a complex number, except the modulus of
    # continuity of ch. 13, which is a different object.
    r'módulo\s+de\s+(?:continuidad|oscilación)',
    # "cuerpo": the field, once out of 52 the Cantor set's ambient line.
    r'cuerpo\s+no\s+numerable',
    # "integral": the integral, except "la forma integral" (of Taylor's
    # remainder), where it is an adjective.
    r'forma\s+integral',
    # "conjunto": the set, except "en su conjunto" (as a whole).
    r'en\s+su\s+conjunto',
    # "imagen": the image of a map, except the picture of ch. 24--25.
    r'una\s+imagen\s+completa', r'en\s+una\s+imagen',
    # "interior": the topological interior -- "el interior $\mathring A$", "de
    # interior vacío", "un punto interior a $I$". "en el interior de la / del
    # ..." is the ordinary preposition (rolling inside a circle, inside a
    # parenthesis); no "$" is consumed.
    r'(?:en|al|del)\s+interior\s+d(?:el|e\s+la|e\s+los|e\s+las|e\s+un)\b',
    r'lazos?\s+interiores?', r'desarrollo\s+interior',
    # "base": the basis of a vector space, except a numeration base ("en base
    # $b$", "base diez") -- lookahead only, the "$" is never consumed.
    r'base\s+(?=\$)', r'bases?\s+(?:diez|dos|decimal(?:es)?|binaria)',
    # "continuo": the continuous function, except the register "de forma
    # continua".
    r'de\s+(?:forma|manera)\s+continua',
]
