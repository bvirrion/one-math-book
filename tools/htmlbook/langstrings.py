"""Read the localized UI strings the converter needs from styles/lang/*.tex.

The lang files are flat \\newcommand definitions, so a regex read keeps the
website strings automatically in sync with the book: a renamed environment
title changes the HTML on the next converter run.
"""

import re
from pathlib import Path

from .lexer import ParseError

# \omname<Key> used for statement box titles and \cref names.
KIND_TO_NAME_MACRO = {
    "definition": "Definition",
    "theorem": "Theorem",
    "proposition": "Proposition",
    "lemma": "Lemma",
    "corollary": "Corollary",
    "method": "Method",
    "example": "Example",
    "notation": "Notation",
    "remark": "Remark",
    "exercise": "Exercise",
    "problem": "Problem",
    "chapter": "Chapter",
}

# \st is language-dependent and may appear inside math.
ST_TEXT = "st"

# Arabic back-references are definite (onemath.sty overrides the \crefname
# declarations with these) while box headings stay indefinite
# (styles/lang/ar.tex). Keep byte-identical to the sty's \ifom@arabic block.
AR_CREF_NAMES = {
    "definition": "التعريف", "theorem": "المبرهنة",
    "proposition": "القضية", "lemma": "المبرهنة المساعدة",
    "corollary": "النتيجة", "method": "الطريقة", "example": "المثال",
    "notation": "الترميز", "remark": "الملاحظة", "chapter": "الفصل",
    "exercise": "التمرين", "problem": "المسألة",
    "figure": "الشكل", "equation": "المعادلة", "section": "القسم",
}
AR_CREF_PLURALS = {
    "definition": "التعريفات", "theorem": "المبرهنات",
    "proposition": "القضايا", "lemma": "المبرهنات المساعدة",
    "corollary": "النتائج", "method": "الطرائق", "example": "الأمثلة",
    "notation": "الترميزات", "remark": "الملاحظات", "chapter": "الفصول",
    "exercise": "التمارين", "problem": "المسائل",
    "figure": "الأشكال", "equation": "المعادلات", "section": "الأقسام",
}


QUANT_NAMES = {
    "interviewq": ("Interview question", "Interview questions"),
    "listing": ("Listing", "Listings"),
    "table": ("Table", "Tables"),
    "dated": ("Box", "Boxes"),
    "strategyfile": ("Strategy file", "Strategy files"),
    "predictorcard": ("Predictor card", "Predictor cards"),
}


def _newcommands(text):
    out = {}
    for m in re.finditer(
            r"\\(?:re)?newcommand\{\\([A-Za-z]+)\}\{(.*)\}", text):
        out[m.group(1)] = m.group(2)
    return out


def _typo(s):
    """LaTeX typography in lang strings (e.g. hi \\omsolutionof 'हल ---')
    must reach the HTML as real punctuation, like titles do in the toc."""
    return s.replace("---", "\u2014").replace("--", "\u2013").replace("~", " ")


class LangStrings:
    def __init__(self, repo_root, lang):
        path = Path(repo_root) / "styles" / "lang" / f"{lang}.tex"
        text = path.read_text(encoding="utf-8")
        cmds = _newcommands(text)
        self.lang = lang
        self.names = {}
        for kind, macro in KIND_TO_NAME_MACRO.items():
            key = f"omname{macro}"
            if key not in cmds:
                raise ParseError(f"{path}: missing \\{key}")
            self.names[kind] = _typo(cmds[key])
        self.proof = _typo(cmds["omnameProof"])
        self.solution_of = _typo(cmds["omsolutionof"])
        self.admitted = _typo(cmds["omadmittedtext"])
        # plural cref names (\omname<Kind>s) for multi-label \cref
        self.plurals = {}
        for kind, macro in KIND_TO_NAME_MACRO.items():
            plural = cmds.get(f"omname{macro}s")
            if plural:
                self.plurals[kind] = _typo(plural)
        # siunitx range/list words (\sisetup in the lang file; English
        # has none and keeps the siunitx defaults)
        self.si_phrases = {"range": " to ", "pair": " and ",
                           "final": " and "}
        for key, option in (("range", "range-phrase"),
                            ("pair", "list-pair-separator"),
                            ("final", "list-final-separator")):
            m = re.search(option + r"\s*=\s*\{\\text\{([^{}]*)\}\}", text)
            if m:
                word = m.group(1)
                if re.search("[\u0590-\u08ff]", word):
                    # RTL word inside the LTR math island: isolate it
                    # (RLI … PDI), else the bidi algorithm reorders the
                    # numbers around it — print sets "20 إلى 60" LTR
                    word = re.sub(r"(\S(?:.*\S)?)", "\u2067\\1\u2069", word)
                self.si_phrases[key] = word
        # list conjunction — not in the lang files (cleveref supplies it
        # in LaTeX); extend here when a new language is added
        self.and_word = {"en": "and", "fr": "et", "nl": "en",
                         "es": "y", "pt": "e", "hi": "और",
                         "ar": "و", "id": "dan"}[lang]
        # figure cref names come from babel in print, not the lang files
        self.names["figure"] = {"en": "Figure", "fr": "Figure",
                                "nl": "Figuur", "es": "Figura",
                                "pt": "Figura", "hi": "आकृति",
                                "ar": "شكل", "id": "Gambar"}[lang]
        self.plurals["figure"] = {"en": "Figures", "fr": "Figures",
                                  "nl": "Figuren", "es": "Figuras",
                                  "pt": "Figuras", "hi": "आकृतियाँ",
                                  "ar": "أشكال", "id": "Gambar"}[lang]
        self.names["equation"] = {"en": "Equation", "fr": "Équation",
                                  "nl": "Vergelijking",
                                  "es": "Ecuación", "pt": "Equação",
                                  "hi": "समीकरण", "ar": "معادلة",
                                  "id": "Persamaan"}[lang]
        self.names["section"] = {"en": "Section", "fr": "Section",
                                 "nl": "Sectie", "es": "Sección",
                                 "pt": "Seção", "hi": "अनुभाग",
                                 "ar": "قسم", "id": "Bagian"}[lang]
        self.plurals["section"] = {"en": "Sections", "fr": "Sections",
                                   "nl": "Secties",
                                   "es": "Secciones", "pt": "Seções",
                                   "hi": "अनुभाग", "ar": "أقسام",
                                   "id": "Bagian"}[lang]
        self.plurals["equation"] = {"en": "Equations", "fr": "Équations",
                                    "nl": "Vergelijkingen",
                                    "es": "Ecuaciones", "pt": "Equações",
                                    "hi": "समीकरण", "ar": "معادلات",
                                    "id": "Persamaan"}[lang]
        # Quant-book kinds: styles/onequant.sty hard-codes their English
        # names (\crefname, tcolorbox titles) whatever the book language.
        for kind, (name, plural) in QUANT_NAMES.items():
            self.names[kind] = name
            self.plurals[kind] = plural
        self.iq_lookfor = "What the interviewer is looking for:"
        self.sources_head = "Sources and further reading"
        self.as_of = "As of"
        # Back-reference (\cref) names: same as the headings except in
        # Arabic, where cleveref prints the definite forms. The list
        # separators mirror cleveref's conjunctions: Arabic و is a bound
        # prefix (space before, none after), the middle separator is the
        # Arabic comma (onemath.sty's \crefpairconjunction overrides).
        self.cref_names = dict(self.names)
        self.cref_plurals = dict(self.plurals)
        if lang == "ar":
            self.cref_names.update(AR_CREF_NAMES)
            self.cref_plurals.update(AR_CREF_PLURALS)
            self.and_sep = " و"
            self.list_sep = "، "
        else:
            self.and_sep = f" {self.and_word} "
            self.list_sep = ", "
        # \st -> its \text{...} body, fed to KaTeX as a macro
        m = re.search(r"\\newcommand\{\\st\}\{(.*)\}", text)
        if not m:
            raise ParseError(f"{path}: missing \\st")
        self.st_macro = m.group(1)

    def cref_text(self, kind, number):
        """cleveref is loaded with [capitalize]: always 'Theorem 1.4'."""
        return f"{self.cref_names[kind]} {number}"
