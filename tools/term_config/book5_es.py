"""Book 5 -- es. Curation only; the rules live in tools/termlink/.

University Year 3: AMBIG_POLICY drop (no spiral nearest-preceding).

Curated against the English link targets (parity gate): the set of
\\omterm first arguments used in parts/bachelor-3/es must coincide with
the set used in parts/bachelor-3, and each Spanish term must reach the
same definition as its English counterpart. Do not edit book5_en.py
(golden fixture).

Two Spanish-specific jobs, on top of mirroring book5_en's STOP:

* Spanish inflects gender and number on every word of a phrase. lang_es
  now sets TAIL_ON_EVERY_WORD = True, so regular agreed plurals are
  generated; with DERIVE = False the gender changes and the
  nominalisations English reaches through DERIVED ("continuity",
  "holomorphy", ...) still have to be declared here.
* Spanish homographs that English keeps apart: "módulo" is both
  \\emph{module} and \\emph{modulus}, "grado" both \\emph{degree of an
  extension} and \\emph{degree of a polynomial}, "base" both
  \\emph{basis of a topology} and \\emph{basis of a vector space},
  "simple" both \\emph{simple group} and \\emph{simple function}. They go
  to STOP, which still links them inside the chapter that defines them.
"""

NOT_A_TERM = ("teorema", "lema", "desigualdad", "fórmula", "criterio",
              "principio", "identidad", "regla", "ley de", "paradoja",
              "problema")

# Spanish mirror of book5_en.STOP: ordinary words here, or words whose
# sense changes by chapter. Soft: still linked inside the defining chapter.
STOP = {
    # book5_en: total, shape, section, direct, simple, stable, equivalent,
    # integer, index, law, generated, converges, events, a.e., dense,
    # normal, maximal, principal, radical, content, characteristic,
    # invariant, bounded, action, basis, degree, free, Euclidean,
    # separable, closed, exact, compact, prime, irreducible, primitive,
    # product, quotient, subspace, path, boundary, interior
    "total",
    "abierto", "abierta", "abiertos", "abiertas",
    "forma", "formas",
    "sección", "secciones",
    "directo", "directa", "directos", "directas",
    "simple", "simples",
    "estable", "estables",
    "equivalente", "equivalentes", "equivalencia",
    "entero", "entera", "enteros", "enteras",
    "índice", "índices",
    "ley", "leyes",
    "generado", "generada", "generados", "generadas",
    "converge",
    "suceso", "sucesos",
    "en casi todo punto",
    "denso", "densa", "densos", "densas",
    "normal", "normales",
    "maximal", "maximales",
    "principal", "principales",
    "radical", "radicales",
    "contenido", "contenida", "contenidos", "contenidas",
    "característica", "característico", "características",
    "invariante", "invariantes",
    "acotado", "acotada", "acotados", "acotadas",
    "acción", "acciones",
    "base", "bases",
    "grado", "grados",
    "libre", "libres",
    "euclídeo", "euclídea", "euclídeos", "euclídeas",
    "separable", "separables",
    "cerrado", "cerrada", "cerrados", "cerradas",
    "exacto", "exacta", "exactos", "exactas",
    "compacto", "compacta", "compactos", "compactas",
    "primo", "prima", "primos", "primas",
    "irreducible", "irreducibles",
    "primitivo", "primitiva", "primitivos", "primitivas",
    "producto", "productos",
    "cociente", "cocientes",
    "subespacio", "subespacios",
    "camino", "caminos",
    "borde", "bordes",
    "interior", "interiores",
    # Spanish homographs English never has to arbitrate
    "módulo", "módulos",          # module vs. modulus
    "argumento", "argumentos",    # argument of a complex number vs. proof
    "unitario", "unitaria",       # unit vector vs. unital ring
    "simetría",
    "orden", "órdenes",
    "álgebra", "álgebras",
    "regular", "regulares",
    "primero", "primera",
    "finito", "finita", "finitos", "finitas",
    "integral", "integrales",
    "norma", "normas",
}

# overloaded words whose first sense dominates the book, so they may be
# linked outside the chapter that pins them down (book5_en.PRIMARY_OK)
PRIMARY_OK = {
    "compacto", "compacta", "compactos", "compactas",
    "cerrado", "cerrada", "cerrados", "cerradas",
    "camino", "caminos",
    "borde", "bordes",
    "interior", "interiores",
    "irreducible", "irreducibles",
}

# harvested terms English never cross-links (parity gate)
DROP = {
    "máximo común divisor",        # lem:b3:rings:bezout
    "medida imagen",               # thm:b3:product:ballvolume
}

# Phrases and derived forms the Spanish harvest cannot reach: plurals
# inflect every word, adjectives inflect gender, abstract nouns are not
# suffixes of the adjective, and result-names translated with a
# NOT_A_TERM head ("fórmula de los grados") are refused outright.
EXTRA = {
    # -- structural terms English links but the harvest misses --
    "borde": "def:b3:forms:boundary",
    "conjunto abierto": "def:b3:topology:topology",
    "conjuntos abiertos": "def:b3:topology:topology",
    "camino": "def:b3:topology:pathconnected",
    "caminos": "def:b3:topology:pathconnected",
    "funciones características": "def:b3:clt:cf",
    "reflexivo": "rem:b3:banach:bidual",
    "reflexiva": "rem:b3:banach:bidual",
    "reflexivos": "rem:b3:banach:bidual",
    "reflexivas": "rem:b3:banach:bidual",
    "formas diferenciales": "def:b3:forms:diffform",
    "funciones simples": "def:b3:lebesgue:simple",
    "productos directos": "prop:b3:groups:direct",
    "fórmula de los grados": "thm:b3:galois:tower",
    "no derivables en ningún punto": "thm:b3:complete:nowherediff",
    # -- continuity / homeomorphism --
    "continuidad": "def:b3:topology:continuity",
    "continuamente": "def:b3:topology:continuity",
    "continuo": "def:b3:topology:continuity",
    "continuos": "def:b3:topology:continuity",
    "homeomorfo": "def:b3:topology:continuity",
    "homeomorfa": "def:b3:topology:continuity",
    "homeomorfos": "def:b3:topology:continuity",
    "homeomorfas": "def:b3:topology:continuity",
    # -- compactness / completeness / connectedness --
    "compacidad": "def:b3:topology:compact",
    "completo": "def:b3:complete:complete",
    "completa": "def:b3:complete:complete",
    "completos": "def:b3:complete:complete",
    "completas": "def:b3:complete:complete",
    "completitud": "def:b3:complete:complete",
    "conexa": "def:b3:topology:connected",
    "conexas": "def:b3:topology:connected",
    "conexión": "def:b3:topology:connected",
    "conexa por caminos": "def:b3:topology:pathconnected",
    "conexos por caminos": "def:b3:topology:pathconnected",
    "conexas por caminos": "def:b3:topology:pathconnected",
    "equicontinua": "def:b3:complete:equicontinuous",
    "equicontinuas": "def:b3:complete:equicontinuous",
    "equicontinuidad": "def:b3:complete:equicontinuous",
    # -- measure and integration --
    "medibilidad": "def:b3:lebesgue:measurable",
    "integrabilidad": "def:b3:lebesgue:l1",
    # -- complex analysis --
    "holomorfo": "def:b3:holomorphic:holo",
    "holomorfos": "def:b3:holomorphic:holo",
    "holomorfía": "def:b3:holomorphic:holo",
    "holomorfamente": "def:b3:holomorphic:holo",
    "meromorfo": "def:b3:residues:singularities",
    "meromorfos": "def:b3:residues:singularities",
    "conformemente": "def:b3:conformal:conformal",
    # -- algebra --
    "algebraico": "def:b3:galois:algebraic",
    "algebraica": "def:b3:galois:algebraic",
    "algebraicos": "def:b3:galois:algebraic",
    "algebraicas": "def:b3:galois:algebraic",
    "algebraicamente": "def:b3:galois:algebraic",
    "perfecto": "prop:b3:galois:perfect",
    "perfecta": "prop:b3:galois:perfect",
    "perfectos": "prop:b3:galois:perfect",
    "perfectas": "prop:b3:galois:perfect",
    "resoluble": "def:b3:groups:derived",
    "resolubles": "def:b3:groups:derived",
    "resolubilidad": "def:b3:groups:derived",
    "caracteres": "def:b3:representations:character",
    "topológico": "def:b3:topology:topology",
    "topológica": "def:b3:topology:topology",
    "topológicos": "def:b3:topology:topology",
    "topológicas": "def:b3:topology:topology",
    # -- operators and probability --
    "autoadjunta": "def:b3:spectral:selfadjoint",
    "autoadjuntos": "def:b3:spectral:selfadjoint",
    "autoadjuntas": "def:b3:spectral:selfadjoint",
    "autoadjunción": "def:b3:spectral:selfadjoint",
    "gaussiano": "def:b3:clt:gaussianvector",
    "gaussiana": "def:b3:clt:gaussianvector",
    "gaussianos": "def:b3:clt:gaussianvector",
    "gaussianas": "def:b3:clt:gaussianvector",
}

NO_CAPITAL = set()
DERIVED = {}
AMBIG_POLICY = "drop"
MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 40
EXTRA_PROTECT = [r'por\s+completo']
