"""Dutch morphology.

Plurals are -en or -s. Dutch writes compounds solid (driehoek), and the word
boundary deliberately refuses to match inside one: linking "hoek" inside
"driehoek" would be wrong. Dutch coverage is therefore thinner than English by
construction -- declare the compounds you want linked in EXTRA instead of
loosening the boundary.
"""
WORD_TAIL = r'(?:e?[ns])?'
TAIL_ON_EVERY_WORD = False
HEAD = r'(?:[^\W\d_]+-)?'
DERIVE = False
