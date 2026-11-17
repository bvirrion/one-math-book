"""Simplified Chinese morphology.

Chinese has no inflection, no capitals and no spaces between words, so a term
is matched as its run of characters with the CJK boundary of
termlink/morphology.py (CJK = True): it must not start or end inside a Latin
word, a number or a macro name, and may break across one source line. A
one-character term sits inside too many compounds (域 in 定义域, 环 in 环境) and
is never linked; declare a safe one in a book config's EXTRA if needed.
"""
CJK = True
CJK_MIN_CHARS = 2
WORD_TAIL = r''
TAIL_ON_EVERY_WORD = False
HEAD = r''
DERIVE = False
