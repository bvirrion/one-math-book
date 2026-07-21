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


def _newcommands(text):
    out = {}
    for m in re.finditer(
            r"\\(?:re)?newcommand\{\\([A-Za-z]+)\}\{(.*)\}", text):
        out[m.group(1)] = m.group(2)
    return out


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
            self.names[kind] = cmds[key]
        self.proof = cmds["omnameProof"]
        self.solution_of = cmds["omsolutionof"]
        self.admitted = cmds["omadmittedtext"]
        # plural cref names (\omname<Kind>s) for multi-label \cref
        self.plurals = {}
        for kind, macro in KIND_TO_NAME_MACRO.items():
            plural = cmds.get(f"omname{macro}s")
            if plural:
                self.plurals[kind] = plural
        # list conjunction — not in the lang files (cleveref supplies it
        # in LaTeX); extend here when a new language is added
        self.and_word = {"en": "and", "fr": "et", "nl": "en"}[lang]
        # \st -> its \text{...} body, fed to KaTeX as a macro
        m = re.search(r"\\newcommand\{\\st\}\{(.*)\}", text)
        if not m:
            raise ParseError(f"{path}: missing \\st")
        self.st_macro = m.group(1)

    def cref_text(self, kind, number):
        """cleveref is loaded with [capitalize]: always 'Theorem 1.4'."""
        return f"{self.names[kind]} {number}"
