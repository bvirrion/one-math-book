"""French morphology.

French pluralises every word of a phrase (nombre pair -> nombres pairs), so the
tail goes on each word, not only the last. The English suffix derivations
(-ic -> -ically, -able -> -ability) mean nothing here and are off; real variants
(egal/egaux, entier/entiere) are declared term by term in EXTRA.
"""
WORD_TAIL = r'(?:e?s)?'
TAIL_ON_EVERY_WORD = True
HEAD = r'(?:[^\W\d_]+-)?'
DERIVE = False
