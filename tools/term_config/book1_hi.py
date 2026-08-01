"""Book 1 -- hi (standard technical Hindi). Curation only; rules in tools/termlink/.

The Hindi bodies (parts/grade-1..9/hi) are UTF-8 Devanagari. School book:
spiral curriculum, so AMBIG_POLICY is "nearest-preceding" -- a term redefined
in grade 4 and again in grade 6 links to whichever definition the reader has
already met.

The Hindi traps are neither the English nor the Portuguese ones:

* Hindi is agglutinative at the postposition boundary: the same noun appears as
  "वर्ग", "वर्ग का", "वर्गों", "वर्गाकार". tools/term_config/lang_hi.py sets
  WORD_TAIL = '' and DERIVE = False on purpose (there is no -s plural to bolt
  on), so oblique/plural forms have to be declared in DERIVED when they matter.
* "जाल" is the net of a solid (def:g5:solids:net) *and* the grid of grid paper,
  which the primary grades use on nearly every page ("जाल वाला काग़ज़",
  "जाल पर", "सौ का जाल"). It is therefore SOFT-stopped: linked only inside
  parts/grade-5/07, where every occurrence is a net.
* "अंश" would be both the numerator of a fraction and the degree of an angle.
  The translation avoids the collision at the source: angles are measured in
  "डिग्री" throughout (grade 6), so "अंश" is unambiguously the numerator.
* "आधा"/"चौथाई" behave exactly like English half/quarter: they are ordinary
  language ("आधा घंटा", "चौथाई घुमाव") but the book defines them, and the
  English config keeps them linked, so we do too.
* The geometry furniture -- वर्ग, त्रिभुज, आयत, वृत्त, कोण -- is dropped for
  the same reason the English config drops square/triangle/rectangle/circle/
  angle: they occur in nearly every sentence of every geometry chapter and
  linking each one turns the exercises solid blue. The compounds a child can
  really forget keep their links (समकोण, समकोण त्रिभुज, समद्विबाहु त्रिभुज,
  समबाहु त्रिभुज, वर्गमूल, सममिति अक्ष).
* "रेखा" (line) is dropped like English "line": "संख्या रेखा" (the number
  line) and "एक ही रेखा पर" are far more common than the geometric object of
  def:g6:lines:objects.
"""

NOT_A_TERM = ("प्रमेय", "उपप्रमेय", "प्रतिज्ञप्ति", "असमिका", "सूत्र",
              "कसौटी", "सिद्धांत", "सर्वसमिका", "नियम", "का नियम",
              "विरोधाभास", "समस्या")

# Never linked: in this book these words are ordinary Hindi far more often
# than they are the defined term.
STOP = {
    # "संख्या रेखा", "एक ही रेखा पर", "रेखा पर चलो": the geometric line of
    # def:g6:lines:objects is a minority of the uses, and the number line is a
    # different object. "रेखाखंड" keeps its own link.
    "रेखा",
    # the net of a solid AND the grid of grid paper (see the module docstring).
    "जाल",
    # def:g4:numbers:classes is the group of three digits; but the word
    # "समूह" is the everyday word for any group in division and multiplication.
    "समूह",
    # THE Hindi homonym of this book: "हर" is the denominator of a fraction
    # (def:g4:fractions:def) and also the ordinary determiner *every*
    # ("हर आयत", "हर बार", "हर एक"). The two cannot be told apart by a regex,
    # and *every* is the commoner of the two by four to one -- even inside
    # parts/grade-4/04, the chapter that defines the denominator. So it is
    # hard-DROPped: def:g4:fractions:def stays reachable through "अंश".
    "हर",
    # ---- the furniture ---------------------------------------------------
    # Real definitions (a child meets them in grades 1-6) but by the time they
    # are used they are the everyday furniture of the page.
    "वर्ग", "त्रिभुज", "आयत", "वृत्त", "कोण",
    # geometry owns this word: "आमने-सामने की भुजाएँ", "विपरीत दिशा". The
    # opposite of a relative number keeps its link through "विपरीत संख्या".
    "विपरीत",
}

# Linked mid-sentence, not sentence-initially: "गोल करना" and "फैलाना" open an
# instruction in an exercise stem, they are not uses of the noun.
NO_CAPITAL = set()

# Manual {term: label}; overrides every rule. Deliberately small: the harvest
# already reaches almost everything through \emph{}\index{} pairs.
EXTRA = {
    "अंक-समूहों": "def:g4:numbers:classes",
    "सम संख्याएँ": "def:g3:numbers:evenodd",
    "विषम संख्याएँ": "def:g3:numbers:evenodd",
    "समांतर रेखाएँ": "def:g6:lines:perp",
    "लंब रेखाएँ": "def:g6:lines:perp",
}

# STOP is deliberately *soft*: a stoplisted word is kept out of the global
# vocabulary but still links inside the chapter that defines it. These are the
# words that are ordinary language everywhere *except* in their own chapter:
SOFT = {
    "जाल",      # parts/grade-5/07: every occurrence there is a net
    "समूह",     # parts/grade-4/01: the groups of three digits
}

DROP = (set(STOP) - SOFT) | {
    # \emph{किसी अंक का मान उसके स्थान पर निर्भर करता है}\index{स्थानीय मान}
    # in parts/grade-6/hi/01: the sentence is not a term (the term is
    # "स्थानीय मान", harvested from the index key). Same defect the EN, FR and
    # PT configs drop by name.
    "किसी अंक का मान उसके स्थान पर निर्भर करता है",
}

# lang_hi.py sets DERIVE = False and WORD_TAIL = '' (Hindi has no -s plural to
# append), so the oblique and plural forms that actually occur in the prose are
# declared here, term by term. Only forms that really appear are listed: a
# declaration whose base is ambiguity-resolved is silently inert (DERIVED only
# extends the *unambiguous* map), so nothing is added "just in case".
DERIVED = {
    "भिन्न": ["भिन्नें", "भिन्नों"],
    "गुणज": ["गुणजों"],
    "भाजक": ["भाजकों"],
    "बहुभुज": ["बहुभुजों"],
    "चतुर्भुज": ["चतुर्भुजों"],
    "रेखाखंड": ["रेखाखंडों"],
    "शीर्ष": ["शीर्षों"],
    "किनारा": ["किनारे", "किनारों"],
    "फलक": ["फलकों"],
    "घन": ["घनों"],
    "घनाभ": ["घनाभों"],
    "ठोस": ["ठोसों"],
    "पिरामिड": ["पिरामिडों"],
    "बेलन": ["बेलनों"],
    "समचतुर्भुज": ["समचतुर्भुजों"],
    "सममिति अक्ष": ["सममिति अक्षों"],
    "लंब समद्विभाजक": ["लंब समद्विभाजकों"],
    "दशमलव संख्या": ["दशमलव संख्याएँ", "दशमलव संख्याओं"],
    "सापेक्ष संख्या": ["सापेक्ष संख्याएँ", "सापेक्ष संख्याओं"],
    "विपरीत संख्या": ["विपरीत संख्याएँ", "विपरीत संख्याओं"],
    "सम संख्या": ["सम संख्याएँ", "सम संख्याओं"],
    "विषम संख्या": ["विषम संख्याएँ", "विषम संख्याओं"],
    "त्रिज्या": ["त्रिज्याएँ", "त्रिज्याओं"],
    "व्यास": ["व्यासों"],
    "अंक-समूह": ["अंक-समूहों"],
}
PRIMARY_OK = set()
AMBIG_POLICY = "nearest-preceding"   # a spiral curriculum re-defines its terms
MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 40

# Spans no link may enter: the uses where a good term means something else.
# NB: every space here is \s+ -- the sources wrap at 72 columns, and a phrase
# split across two lines slips past a literal space.
# NEVER CONSUME A `$` (see the header of tools/termlink/protect.py): match it
# with a lookahead instead.
EXTRA_PROTECT = [
    # ---- morpheme boundaries: NO LONGER NEEDED --------------------------
    # This list used to carry six regexes (लंब(?=[ा-्]), दोहर, अंतर(?=[ाि्]),
    # शून्येतर, सममिति(?!...), शीर्षाभिमुख) that worked around a bug in
    # tools/termlink/morphology.py: its word-boundary lookarounds used [\w-],
    # and Python's \w is False for every Devanagari matra, virama, nukta and
    # anusvara (category Mn/Mc), so a short term matched *inside* a longer,
    # unrelated word -- "लंब" (perpendicular) inside "लंबाई" (length), "अंतर"
    # (difference) inside "अंतराल" (interval). _BEFORE/_AFTER now exclude the
    # Devanagari sign ranges, so the six regexes were removed on 2026-08-01.
    # Removing them *added* 10 links, all of them correct and whole-word
    # (अक्षीय सममिति, केंद्रीय सममिति, शीर्षाभिमुख कोण): the blunt regexes had
    # been suppressing the genuine multi-word terms as collateral damage.
    # A whole-tree mid-word scan after regeneration finds 0 suspects.
    # ---- senses ---------------------------------------------------------
    # "जाल वाला काग़ज़", "जाल पर", "सौ का जाल": the grid, not the net of a solid
    r'जाल\s+वाल[ेी]\s+काग़ज़',
    r'जाल\s+(?:पर|की|के|में|है|वाले)',
    r'सौ\s+का\s+जाल',
    r'जाल-खान',
    # "आधा"/"चौथाई" in the clock idioms and in "आधे घंटे": a duration, not the
    # arithmetic half of def:g3:division:half
    r'आधा\s+घंटा', r'आधे\s+घंटे', r'साढ़े', r'सवा', r'पौने',
    # prose cross-references to the other books of the series
    r'अगले\s+खंड',
]
