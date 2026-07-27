"""Spanish morphology.

Spanish plurals are typically -s or -es, and -- like French -- a noun phrase
inflects on every word (numero primo -> numeros primos, forma cuadratica ->
formas cuadraticas), so the tail goes on each word, not only the last. With the
tail on the last word alone the regex asked for "numero primos", and every
plural of a compound term went unlinked; each Spanish book worked around that
by declaring its plurals by hand until the flag was corrected. Compounds are
usually open or hyphenated rather than solid, so the English-style DERIVE
suffixes are off; declare irregular variants term by term in EXTRA when needed.
"""
WORD_TAIL = r'(?:e?s)?'
TAIL_ON_EVERY_WORD = True
HEAD = r'(?:[^\W\d_]+-)?'
DERIVE = False
