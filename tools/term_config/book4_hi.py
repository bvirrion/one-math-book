"""Book 4 -- hi. Curation only; the rules live in tools/termlink/.

University Year 2: AMBIG_POLICY drop (no spiral nearest-preceding).
"""

NOT_A_TERM = ("प्रमेय", "उपप्रमेय", "असमानता", "सूत्र", "मानदंड",
              "सिद्धांत", "सर्वसमिका", "नियम", "नियम की", "विरोधाभास",
              "समस्या")

STOP = {
    "पहला", "पहली",
    "परिमित",
    "तर्क",
    "एकक",
    "सममिति",
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
