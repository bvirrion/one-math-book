"""Turning a term into the regex that finds its uses.

English keeps exactly the rule Book 5 was generated with. French and Dutch need
two things English does not:

  * accents in two spellings. parts/grade-1..3/{fr,nl} write them as TeX escapes
    (unit\\'es, \\`a, \\c{c}); parts/grade-4..12/{fr,nl} write them as UTF-8
    (unités). Book 1 spans both, so a term harvested in grade-3 would never match
    in grade-6 unless the pattern accepts either spelling.
  * plurals on every word of a phrase (nombre pair -> nombres pairs), not just
    the last one, or most French phrase uses go unlinked.
"""
import re
import unicodedata

# The accent forms that occur in the escaped trees: \'e \`a \^e \"e \~n \c{c}
COMBINING = {"'": "́", "`": "̀", "^": "̂",
             '"': "̈", "~": "̃"}
CEDILLA = "̧"

# unicode letter -> the TeX spellings of it
TEX_FORMS = {}
for _acc, _comb in COMBINING.items():
    for _base in "aeiouynAEIOUYN":
        _ch = unicodedata.normalize("NFC", _base + _comb)
        if len(_ch) == 1:
            # both spellings occur: quoti\"ent and quoti\"{e}nt
            TEX_FORMS.setdefault(_ch, []).extend(
                ["\\" + _acc + _base, "\\" + _acc + "{" + _base + "}"])
TEX_FORMS["ç"] = ["\\c{c}", "\\c c"]      # ç
TEX_FORMS["Ç"] = ["\\c{C}", "\\c C"]      # Ç

# and the reverse, to read an escaped source term back into plain text
_TEX_RE = re.compile(r'\\([\'`^"~])\{?([a-zA-Z])\}?|\\c\s*\{?([a-zA-Z])\}?')


def to_text(term):
    """A harvested term as plain NFC text, whatever spelling the source used."""
    def sub(m):
        if m.group(3):
            return unicodedata.normalize("NFC", m.group(3) + CEDILLA)
        return unicodedata.normalize("NFC", m.group(2) + COMBINING[m.group(1)])
    return unicodedata.normalize("NFC", _TEX_RE.sub(sub, term))


def _esc(word):
    """Escape a word, accepting either spelling of each accented letter."""
    out = []
    for ch in word:
        forms = TEX_FORMS.get(ch)
        if forms:
            out.append("(?:" + "|".join(re.escape(f) for f in [ch] + forms) + ")")
        else:
            out.append(re.escape(ch))
    return "".join(out)


def _cap(word):
    """[Cc]ercle, accents included."""
    up, low = word[0].upper(), word[0]
    return "(?:" + _esc(up) + "|" + _esc(low) + ")" + _esc(word[1:])


NO_TAIL_END = ("s", "$", "]", ")")

# in the escaped trees a word can be followed by an accent macro belonging to
# the same word ("pair" inside "pair\'e"), which \w does not see
_AFTER = r'(?!(?:[\w-]|\\[\'`^"~]|\\c\s*\{?[a-zA-Z]))'


def pattern(term, lang, langcfg, no_capital=()):
    """Match every use of the term: plural, sentence-initial capital, hyphenated
    prefix ("non-measurable", linked whole). Never split an existing hyphenated
    compound, or "torsion-free" becomes two links."""
    if lang == "en":
        # the exact rule Book 5 was generated with -- do not "improve" it here
        body = re.escape(term).replace(r'\ ', r'\s+')
        if term[:1].isalpha() and term[:1].islower() and term not in no_capital:
            body = "[" + term[0].upper() + term[0] + "]" + body[1:]
        tail = "" if term.endswith(NO_TAIL_END) else r'(?:e?s)?'
        head = r'(?:[A-Za-z]+-)?' if " " not in term else ""
        return re.compile(r'(?<![\w\\@-])(' + head + body + tail + r')(?![\w-])')

    words = to_text(term).split()
    pieces = []
    for i, w in enumerate(words):
        last = i == len(words) - 1
        first = i == 0
        p = _cap(w) if (first and w[:1].isalpha() and w[:1].islower()
                        and term not in no_capital) else _esc(w)
        if (last or langcfg.TAIL_ON_EVERY_WORD) and not w.endswith(NO_TAIL_END):
            p += langcfg.WORD_TAIL
        pieces.append(p)
    body = r'\s+'.join(pieces)
    head = langcfg.HEAD if len(words) == 1 else ""
    return re.compile(r'(?<![\w\\@-])(' + head + body + r')' + _AFTER)


def derive(term, langcfg):
    """Regular derivations, generated here and kept by the caller only if they
    really occur in the book (holomorphic -> holomorphically)."""
    if not langcfg.DERIVE or " " in term or "$" in term:
        return []
    out = []
    if term.endswith("ic"):
        out += [term + "ally"]
    if term.endswith("ous"):
        out += [term[:-3] + "ously"]
    if term.endswith("able"):
        out += [term[:-4] + "ability", term[:-1] + "y"]
    if term.endswith("ible"):
        out += [term[:-4] + "ibility"]
    if term.endswith("ive"):
        out += [term[:-1] + "ely"]
    if term.endswith("ent"):
        out += [term[:-1] + "ce"]
    if term.endswith("al"):
        out += [term + "ly"]
    return out
