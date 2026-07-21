"""Spanish morphology.

Spanish plurals are typically -s or -es. Compounds are usually open or
hyphenated rather than solid, so the English-style DERIVE suffixes are off;
declare irregular variants term by term in EXTRA when needed.
"""
WORD_TAIL = r'(?:e?s)?'
TAIL_ON_EVERY_WORD = False
HEAD = r'(?:[^\W\d_]+-)?'
DERIVE = False
