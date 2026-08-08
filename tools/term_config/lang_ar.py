"""Arabic morphology.

Arabic differs from every other language in this repo in that the productive
affix is a PREFIX, not a suffix. The definite article ال is written joined to
its noun, and so are the one-letter conjunction/prepositions و ف ب ك ل, in any
combination (ال، وال، بال، كال، فال، لل). A technical term is mentioned in the
definite far more often than not, so without HEAD almost nothing links.

Inside a noun phrase the article repeats on every word ("عدد أولي" is definite
as "العدد الأولي"), which is why HEAD_ON_EVERY_WORD is on. That knob is read
with getattr in tools/termlink/morphology.py and defaults to False, so no other
language's patterns move.

WORD_TAIL is empty and DERIVE is off, following the Hindi decision and for a
stronger reason: Arabic pluralises mostly by internal vowel change (broken
plurals — دالة/دوال، مبرهنة/مبرهنات is the easy case, حد/حدود is not), which no
suffix regex can reach, and a sound-plural tail on its own buys few links while
risking wrong-sense matches. Declare the plurals a book actually uses in that
book's DERIVED or EXTRA, term by term.
"""
WORD_TAIL = r''
TAIL_ON_EVERY_WORD = False
HEAD = r'(?:لل|[وفبك]?ال|[وفبكل])?'
HEAD_ON_EVERY_WORD = True
DERIVE = False
