"""Book 2 -- hi. Curation only; the rules live in tools/termlink/.

Hindi bodies (parts/grade-10..12/hi) use UTF-8 Devanagari.
School book: spiral curriculum, AMBIG_POLICY nearest-preceding.
"""

NOT_A_TERM = ("प्रमेय", "उपप्रमेय", "असमानता", "सूत्र", "मानदंड",
              "सिद्धांत", "सर्वसमिका", "नियम", "नियम की", "नियम के",
              "विरोधाभास", "समस्या")

STOP = {
    "योग",
    "युग्म",
    "संयोजन",
    "सभी",
    "कठोरता से",
    "एक साथ",
    "क्रमित",
    "पहला",
    "पहली",
}

NO_CAPITAL = set()

EXTRA = {}
DROP = set()
DERIVED = {}
PRIMARY_OK = set()
AMBIG_POLICY = "nearest-preceding"
MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 40

EXTRA_PROTECT = []
