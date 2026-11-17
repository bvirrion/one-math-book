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

# Devanagari dependent signs -- matras, virama, nukta, anusvara, candrabindu,
# visarga -- are Unicode category Mn/Cf, so Python's \w is FALSE for every one
# of them. A boundary written as [\w-] therefore LEAKS in Hindi: it happily
# ends a term in the middle of a word, because the next character is a matra
# and not a "word character". Two book agents independently measured the
# damage at ~1250 wrong-sense links: "भुज" (abscissa) matched inside "भुजा"
# (side), "ज्या" inside "त्रिज्या", "सम" (even) inside "समुच्चय", "लंब"
# (perpendicular) inside "लंबाई". The lookbehind leaks the same way, and a
# term starting right after the virama of "क्" split the conjunct across two
# boxes -- which XeLaTeX renders as a dotted circle.
_DEV_MARK = (r'ऀ-ःऺ-़ा-ॏ'
             r'॑-ॗॢॣ‌‍')

# Arabic has the same hole: harakat, sukun, shadda, the superscript alef and
# the Quranic marks are all category Mn, so \w is false for every one of them
# and a boundary written [\w-] happily ends a term on a bare consonant that is
# in fact carrying a vowel sign. Tatweel (U+0640) is Lm and \w already sees it,
# but it is listed here so the class documents the whole joining apparatus.
_ARAB_MARK = ('ً-ٰٟ'
              'ۖ-ۭـ')

_MARKS = _DEV_MARK + _ARAB_MARK

# Keep the hyphen last in each class so it stays literal and does not open a
# range with the codepoint before it.
_BEFORE = r'(?<![\w\\@' + _MARKS + r'-])'

# in the escaped trees a word can be followed by an accent macro belonging to
# the same word ("pair" inside "pair\'e"), which \w does not see
_AFTER = (r'(?!(?:[\w' + _MARKS + r'-]|\\[\'`^"~]|\\c\s*\{?[a-zA-Z]))')


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

    if getattr(langcfg, "CJK", False):
        return _cjk_pattern(term, langcfg)

    words = to_text(term).split()
    pieces = []
    for i, w in enumerate(words):
        last = i == len(words) - 1
        first = i == 0
        p = _cap(w) if (first and w[:1].isalpha() and w[:1].islower()
                        and term not in no_capital) else _esc(w)
        if (last or langcfg.TAIL_ON_EVERY_WORD) and not w.endswith(NO_TAIL_END):
            p += langcfg.WORD_TAIL
        # Arabic attaches its article and its one-letter prepositions to the
        # FRONT of the word, and inside a noun phrase every word takes them
        # ("عدد أولي" -> "العدد الأولي"). Every other language here only ever
        # needs a head on a single word, so this is opt-in per language and
        # the fr/nl/es/pt/hi patterns are unchanged.
        if len(words) > 1 and getattr(langcfg, "HEAD_ON_EVERY_WORD", False):
            p = langcfg.HEAD + p
        pieces.append(p)
    body = r'\s+'.join(pieces)
    head = langcfg.HEAD if len(words) == 1 else ""
    return re.compile(_BEFORE + r'(' + head + body + r')' + _AFTER)


# Chinese (and any other script written without spaces) has no word boundary to
# test: every Han character is \w, so the boundary above would refuse a term
# sitting between two other characters, i.e. nearly every use. In CJK mode the
# boundary only keeps a term from starting or ending inside a LATIN word, a
# number or a macro name. There is no plural, no capital and no attached head.
# xeCJK drops a newline between two Han characters, so a source line may break
# inside a term: allow one line break (and its indentation) between any two
# characters. A one-character term (域, 环, 群, 像) sits inside many compounds
# (定义域, 环境, 群体, 图像) and is never linked unless the language config lowers
# CJK_MIN_CHARS. Opt-in per language: the en/fr/nl/es/pt/hi/ar/id patterns are
# unchanged (tools/check_book5_golden.sh).
_CJK_BEFORE = r'(?<![A-Za-z0-9\\@-])'
_CJK_AFTER = r'(?![A-Za-z0-9-])'


def _cjk_pattern(term, langcfg):
    text = to_text(term)
    if len(re.sub(r"\s", "", text)) < getattr(langcfg, "CJK_MIN_CHARS", 2):
        return re.compile(r"(?!)")
    chars = [c for c in text if not c.isspace()]
    body = r"(?:\n[ \t]*)?".join(_esc(c) for c in chars)
    return re.compile(_CJK_BEFORE + r'(' + body + r')' + _CJK_AFTER)


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
