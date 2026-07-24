"""Book 1 -- hi. Curation only; the rules live in tools/termlink/.

Hindi bodies (parts/grade-1..9/hi) use UTF-8 Devanagari.
School book: spiral curriculum, AMBIG_POLICY nearest-preceding.
"""

NOT_A_TERM = ("प्रमेय", "उपप्रमेय", "असमानता", "सूत्र", "मानदंड",
              "सिद्धांत", "सर्वसमिका", "नियम", "नियम की", "विरोधाभास",
              "समस्या")

# Ordinary Hindi, or a word whose sense in the book is not the definition's.
STOP = {
    "सरल",
    "विपरीत",
    "वर्ग",
    "कोण",
    "त्रिभुज",
    "आयत",
    "वृत्त",
    "वर्ग",
}

NO_CAPITAL = set()

EXTRA = {}
SOFT = set()
DROP = (set(STOP) - SOFT)

DERIVED = {}
PRIMARY_OK = set()
AMBIG_POLICY = "nearest-preceding"
MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 40

EXTRA_PROTECT = []
