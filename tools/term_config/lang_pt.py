"""Brazilian Portuguese morphology.

Portuguese agrees every word of a noun phrase (numero primo -> numeros primos,
funcao continua -> funcoes continuas), as Spanish and French do, so the tail
goes on each word and not only the last. The tail is optional per word, so
head-only plurals still match: "espaco de Banach" -> "espacos de Banach"
pluralises the head and leaves the prepositional tail alone.

This flag was False until 2026-08-01; with the tail on the last word alone the
regex asked for "numero primos" and no plural of a multiword term was ever
generated. Every pt book worked around it by declaring its compound plurals by
hand -- the same workaround the Spanish books carried before their own flag was
corrected (see lang_es.py). Those declarations have been trimmed back to the
genuinely irregular forms.

WORD_TAIL covers the plural only. It does NOT reach gender variants: a term
harvested as "paralelo" is unreachable as "paralela". Book 1 measured ~312
links lost that way and confirmed DERIVED cannot recover them either, because
DERIVED only extends the unambiguous map. Spanish carries the identical
limitation. A residual gap against English is therefore expected here and is
not a defect.

Solid compounds are rarer than in Dutch, so DERIVE is off -- declare irregular
variants ("-ao" -> "-oes", "-al" -> "-ais", "-m" -> "-ns", "-r" -> "-res") term
by term in EXTRA when needed.
"""
WORD_TAIL = r'(?:e?s)?'
TAIL_ON_EVERY_WORD = True
HEAD = r'(?:[^\W\d_]+-)?'
DERIVE = False
