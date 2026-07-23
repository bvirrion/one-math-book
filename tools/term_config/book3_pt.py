"""Book 3 -- pt. University Year 1: AMBIG_POLICY drop."""

NOT_A_TERM = ("teorema", "lema", "desigualdade", "fórmula", "critério",
              "princípio", "identidade", "regra", "lei de", "paradoxo",
              "problema")

STOP = {
    "primeiro", "primeira",
    "finito", "finita",
    "argumento",
    "unitário", "unitária",
    "simetria",
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
