"""Hindi morphology.

Hindi does not use Latin-style -s plurals. Compounds are open (space-
separated) or sometimes hyphenated. Disable English-style DERIVE suffixes;
declare irregular variants term by term in EXTRA when needed.
"""
WORD_TAIL = r''
TAIL_ON_EVERY_WORD = False
HEAD = r'(?:[^\W\d_]+-)?'
DERIVE = False
