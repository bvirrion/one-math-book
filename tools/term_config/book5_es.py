"""Book 5 -- es. Curation only; the rules live in tools/termlink/.

University Year 3: AMBIG_POLICY drop (no spiral nearest-preceding).
"""

NOT_A_TERM = ("teorema", "lema", "desigualdad", "fórmula", "criterio",
              "principio", "identidad", "regla", "ley de", "paradoja",
              "problema")

STOP = {
    "primero", "primera",
    "finito", "finita",
    "argumento",
    "unitario", "unitaria",
    "simetría",
    "orden",
    "equivalente",
    "álgebra",
    "converge",
    "regular",
    "equivalencia",
    "cerrado", "cerrada",
    "abierto", "abierta",
    "compacto", "compacta",
    "completo", "completa",
    "medida",
    "integral",
    "norma",
}

NO_CAPITAL = set()
EXTRA = {}
DROP = set(STOP)
DERIVED = {}
PRIMARY_OK = set()
AMBIG_POLICY = "drop"
MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 40
EXTRA_PROTECT = []
