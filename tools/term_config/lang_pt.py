"""Brazilian Portuguese morphology.

Portuguese plurals are typically -s or -es. Open compounds are common;
solid compounds are rarer than in Dutch, so DERIVE is off — declare
irregular variants term by term in EXTRA when needed.
"""
WORD_TAIL = r'(?:e?s)?'
TAIL_ON_EVERY_WORD = False
HEAD = r'(?:[^\W\d_]+-)?'
DERIVE = False
