"""Book 5 -- pt. University Year 3: AMBIG_POLICY drop."""

NOT_A_TERM = ("teorema", "lema", "desigualdade", "fórmula", "critério",
              "princípio", "identidade", "regra", "lei de", "paradoxo",
              "problema")

STOP = {
    "primeiro", "primeira",
    "finito", "finita",
    "argumento",
    "unitário", "unitária",
    "simetria",
    "ordem",
    "equivalente",
    "álgebra",
    "converge",
    "regular",
    "equivalência",
    "fechado", "fechada",
    "aberto", "aberta",
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
