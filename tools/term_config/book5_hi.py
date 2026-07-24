"""Book 5 -- hi. Curation only; the rules live in tools/termlink/.

University Year 3: AMBIG_POLICY drop (no spiral nearest-preceding).
Note: book5_en.py is FROZEN for the EN golden test — do not change it.
"""

NOT_A_TERM = ("प्रमेय", "उपप्रमेय", "असमानता", "सूत्र", "मानदंड",
              "सिद्धांत", "सर्वसमिका", "नियम", "नियम की", "विरोधाभास",
              "समस्या", "लेम्मा", "प्रमेयिका")

STOP = {
    "पहला", "पहली",
    "परिमित",
    "तर्क",
    "एकक",
    "सममिति",
    "सीमा",  # overloaded (boundary vs limit); use EXTRA phrases
}

# Surface forms that EN links and the Hindi harvest otherwise misses
# (math inside \emph, multi-line index keys, or AMBIG drop).
EXTRA = {
    "मॉड्यूल": "def:b3:modules:module",
    "सिलो उपसमूह": "def:b3:groups:sylow",
    "सिलो": "def:b3:groups:sylow",
    "स्वयं सहायक": "def:b3:spectral:selfadjoint",
    "स्वयं adjoint": "def:b3:spectral:selfadjoint",
    "आत्म adjointness": "def:b3:spectral:selfadjoint",
    "स्थानीय स्तर पर लिप्सचिट्ज़": "def:b3:ode:lipschitz",
    "स्थानीय रूप से लिप्सचिट्ज़": "def:b3:ode:lipschitz",
    "लेबेस्गे बाहरी माप": "def:b3:measure:lebesgueouter",
    "लेबेस्गे माप": "def:b3:measure:lebesgueouter",
    "लेब्सेग माप": "def:b3:measure:lebesgueouter",
    "स्पर्शरेखा अंतरिक्ष": "def:b3:submanifolds:tangent",
    "स्पर्शरेखा स्थान": "def:b3:submanifolds:tangent",
    "प्रत्यावर्ती रूप": "def:b3:forms:alternating",
    "वैकल्पिक रूप": "def:b3:forms:alternating",
    "विभेदक रूप": "def:b3:forms:diffform",
    "अवकल रूप": "def:b3:forms:diffform",
    "सीमा के साथ सबमैनिफोल्ड": "def:b3:forms:boundary",
    "सीमा चार्ट": "def:b3:forms:boundary",
    "हिल्बर्ट--श्मिट": "ex:b3:spectral:examples",
    "हिल्बर्ट--श्मिट ऑपरेटर": "ex:b3:spectral:examples",
    "न्यूमैन श्रृंखला": "prop:b3:banach:neumann",
    "न्यूमैन": "prop:b3:banach:neumann",
    "ऑर्थोगोनल बहुपद": "pb:b3:hilbert:1",
    "ओर्थोगोनल बहुपद": "pb:b3:hilbert:1",
    "लम्बकोणीय बहुपद": "pb:b3:hilbert:1",
    "पॉइसन कर्नेल": "thm:b3:conformal:poisson",
    "पॉइसन अष्ठि": "thm:b3:conformal:poisson",
    "रैखिकरण द्वारा स्थिरता": "thm:b3:ode:linearization",
    "रैखिकीकरण द्वारा स्थिरता": "thm:b3:ode:linearization",
    "रैखिककरण द्वारा स्थिरता": "thm:b3:ode:linearization",
    "कहीं भी अवकलनीय नहीं": "thm:b3:complete:nowherediff",
    "कहीं भी भिन्न नहीं": "thm:b3:complete:nowherediff",
}

# HI-only result-name links EN does not make (lemma names via \emph/\index).
DROP = set(STOP) | {
    "गॉस की लेम्मा",
    "गॉस की प्रमेयिका",
    "फ़तौ की लेम्मा",
    "फतौ की लेम्मा",
    "बोरेल--कैंटेली लेम्मास",
    "बोरेल--कैंटेली",
    "शूर की लेम्मा",
    "ज़ोर्न की लेम्मा",
    "ज़ोर्न",
    "लेयर केक",
    "परत केक",
    "परत केक फार्मूला",
    "परतों वाला केक",
    "layer cake",
    "परत",  # over-linked to layercake; EN uses cref for the formula
}

NO_CAPITAL = set()
DERIVED = {}
PRIMARY_OK = set()
AMBIG_POLICY = "drop"
MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 40
EXTRA_PROTECT = []
