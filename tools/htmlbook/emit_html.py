"""Emit HTML from the parsed chapter tree.

Math is not rendered here: every formula becomes a \\x00M<i>\\x00
placeholder and is collected in Emitter.math, so the build script can
batch-render all formulas of a chapter in one KaTeX (node) call and
substitute the results afterwards.
"""

import html
import re

from .lexer import STATEMENT_KINDS, ParseError
from .model import anchor_for

# A small TeX -> Unicode map for alt texts and meta descriptions only
# (the real rendering is KaTeX's).
ALT_MAP = {
    "\\N": "ℕ", "\\Z": "ℤ", "\\Q": "ℚ", "\\R": "ℝ", "\\C": "ℂ",
    "\\subset": "⊂", "\\in": "∈", "\\notin": "∉", "\\cap": "∩",
    "\\cup": "∪", "\\leq": "≤", "\\geq": "≥", "\\neq": "≠",
    "\\infty": "∞", "\\pi": "π", "\\sqrt": "√", "\\times": "×",
    "\\dots": "…", "\\ldots": "…", "\\pm": "±",
}


MONTHS = ("January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December")

# \omcode listings: Pygments lexer per file extension (onequant.sty picks the
# listings language the same way; .s is Intel-syntax x86).
LISTING_LEXERS = {
    ".py": "python", ".hpp": "cpp", ".cpp": "cpp", ".h": "cpp",
    ".rs": "rust", ".s": "nasm", ".sql": "sql", ".sv": "systemverilog",
    ".v": "systemverilog", ".xml": "xml", ".xhtml": "html", ".sh": "bash",
    ".json": "json", ".toml": "toml", ".txt": "text", ".csv": "text",
}
# Pygments short token classes kept in the HTML, coarsened to what the
# reader CSS colours (keywords, strings, comments, numbers, a few names).
KEEP_TOKEN_CLASSES = ("nf", "nc", "nb", "nd", "bp")


def _token_class(ttype):
    from pygments.token import STANDARD_TYPES
    while ttype not in STANDARD_TYPES:
        ttype = ttype.parent
    short = STANDARD_TYPES[ttype]
    if short in KEEP_TOKEN_CLASSES:
        return short
    return short[:1] if short[:1] in ("k", "s", "c", "m") else ""


def highlight_lines(code, ext):
    """Syntax-highlighted HTML, one string per source line (a token that
    spans lines is split so every line is a self-contained span run)."""
    from pygments.lexers import get_lexer_by_name
    if ext not in LISTING_LEXERS:
        raise ParseError(f"no listing lexer for {ext!r} files")
    lexer = get_lexer_by_name(LISTING_LEXERS[ext], stripnl=False,
                              ensurenl=False)
    lines = [[]]
    for ttype, value in lexer.get_tokens(code):
        cls = _token_class(ttype)
        for k, part in enumerate(value.split("\n")):
            if k:
                lines.append([])
            if part:
                esc = html.escape(part, quote=False)
                lines[-1].append(f'<span class="{cls}">{esc}</span>'
                                 if cls else esc)
    return ["".join(parts) for parts in lines]


def tex_to_alt(tex):
    """Rough plaintext for a formula, for alt/description use."""
    s = tex
    s = re.sub(r"\\(intcc|intco|intoc|intoo)\{([^{}]*)\}\{([^{}]*)\}",
               lambda m: {"intcc": "[%s, %s]", "intco": "[%s, %s)",
                          "intoc": "(%s, %s]", "intoo": "(%s, %s)"}
               [m.group(1)] % (m.group(2), m.group(3)), s)
    s = re.sub(r"\\abs\{([^{}]*)\}", r"|\1|", s)
    s = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"\1/\2", s)
    s = re.sub(r"\\t?frac(\d)(\d)", r"\1/\2", s)
    for k, v in ALT_MAP.items():
        s = s.replace(k, v)
    s = re.sub(r"\\[a-zA-Z]+", " ", s)
    s = s.replace("{", "").replace("}", "").replace("^", "")
    return re.sub(r"\s+", " ", s).strip()


def plaintext(inlines, refs=None):
    """Visible text of an inline run (titles, headings, meta descriptions).

    `refs` is an optional callable node -> str that spells out \cref /
    \eqref nodes ("Chapter 3", "(2.1)"); the Emitter provides one via
    plain_ref(). Without it references vanish, which leaves residues like
    "appeared in ;" in a meta description — pass it whenever labels are
    resolvable."""
    out = []
    for node in inlines:
        t = node["t"]
        if t == "text":
            out.append(node["s"])
        elif t == "math":
            out.append(tex_to_alt(node["tex"]))
        elif t in ("emph", "bold", "sup", "sub", "code", "span", "u"):
            out.append(plaintext(node["inl"], refs))
        elif t == "term":
            out.append(plaintext(node["inl"], refs))
        elif t == "field":
            out.append(plaintext(node["inl"], refs) + ".")
        elif t in ("cref", "eqref", "ref") and refs is not None:
            out.append(refs(node))
    return "".join(out)


def slugify(text):
    import unicodedata
    s = unicodedata.normalize("NFKD", text)
    s = s.encode("ascii", "ignore").decode("ascii").lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


class Emitter:
    def __init__(self, lang, labels, solutions, figures, chapter_number,
                 externals=None):
        """
        lang       -- LangStrings
        labels     -- label map from model.number_chapter
        solutions  -- sol_key -> blocks (already numbered? no: solutions are
                      bodies only; their exercise numbers come from labels)
        figures    -- tikz source -> {"file","width","height","url"}
        externals  -- labels of OTHER already-published chapters:
                      {label: {"kind","number","href"}} where href is the
                      target chapter page URL + #anchor (this language)
        """
        self.lang = lang
        self.labels = labels
        self.solutions = solutions
        self.figures = figures
        self.chapter_number = chapter_number
        self.externals = externals or {}
        self.math = []          # [(tex, display)]
        self.footnotes = []     # collected footnote bodies (HTML)

    # ------------------------------------------------------------- helpers

    def math_ph(self, tex, display):
        # \cref inside a formula: KaTeX cannot carry a hyperlink, so the
        # localized reference text is substituted in (text, no link)
        tex = re.sub(
            r"\\[cC]ref\{([^{}]*)\}",
            lambda m: "\\text{" + self.lang.cref_text(
                *(lambda i: (i["kind"], i["number"]))(
                    self.resolve(m.group(1), "\\cref in math"))) + "}",
            tex)
        self.math.append((tex, display))
        return f"\x00M{len(self.math) - 1}\x00"

    def plain_ref(self, node):
        """Plain-text rendering of a \cref / \eqref node (no links): the
        `refs` callback of plaintext(), used for the manifest's
        description_fallback and headings."""
        if node["t"] == "eqref":
            info = self.resolve(node["label"], "\\eqref")
            return f"({info['number']})"
        if node["t"] == "ref":
            return self.resolve(node["label"], "\\ref")["number"]
        labels = [re.sub(r"\s+", "", part) for part in node["label"].split(",")]
        infos = [self.resolve(lbl, "\\cref") for lbl in labels]
        if len(infos) == 1:
            return self.lang.cref_text(infos[0]["kind"], infos[0]["number"])
        kinds = {info["kind"] for info in infos}
        if len(kinds) == 1 and self.lang.cref_plurals.get(infos[0]["kind"]):
            parts = [info["number"] for info in infos]
            joined = (self.lang.and_sep.join(parts) if len(parts) == 2
                      else self.lang.list_sep.join(parts[:-1])
                      + self.lang.and_sep + parts[-1])
            return f"{self.lang.cref_plurals[infos[0]['kind']]} {joined}"
        parts = [self.lang.cref_text(info["kind"], info["number"])
                 for info in infos]
        return (self.lang.and_sep.join(parts) if len(parts) == 2
                else self.lang.list_sep.join(parts[:-1])
                + self.lang.and_sep + parts[-1])

    def resolve(self, label, where):
        """A reference target: in this chapter (anchor) or in another
        published chapter (page URL + anchor)."""
        if label in self.labels:
            info = self.labels[label]
            return {**info, "href": f"#{info['anchor']}"}
        if label in self.externals:
            return self.externals[label]
        raise ParseError(
            f"unresolvable reference {label!r} in {where}: this label is "
            "neither in the current chapter nor in a published one")

    # ------------------------------------------------------------- inlines

    def inlines(self, nodes):
        out = []
        for node in nodes:
            t = node["t"]
            if t == "text":
                out.append(html.escape(node["s"], quote=False))
            elif t == "math":
                out.append(self.math_ph(node["tex"],
                                        display=node.get("display", False)))
            elif t == "emph":
                attr = ""
                if node.get("index"):
                    attr = f' data-index="{html.escape(node["index"])}"'
                out.append(f"<em{attr}>{self.inlines(node['inl'])}</em>")
            elif t == "bold":
                out.append(f"<strong>{self.inlines(node['inl'])}</strong>")
            elif t == "code":
                out.append(f"<code>{self.inlines(node['inl'])}</code>")
            elif t == "u":
                out.append(f"<u>{self.inlines(node['inl'])}</u>")
            elif t == "span":
                # a \\multicolumn outside a table cell: just its text
                out.append(self.inlines(node["inl"]))
            elif t == "sup":
                out.append(f"<sup>{self.inlines(node['inl'])}</sup>")
            elif t == "sub":
                out.append(f"<sub>{self.inlines(node['inl'])}</sub>")
            elif t == "sc":
                out.append(f'<span class="om-sc">'
                           f"{self.inlines(node['inl'])}</span>")
            elif t == "footnote":
                self.footnotes.append(self.inlines(node["inl"]))
                n = len(self.footnotes)
                out.append(f'<sup class="om-fnref" id="fnref-{n}">'
                           f'<a href="#fn-{n}">{n}</a></sup>')
            elif t == "term":
                label = node["label"]
                text = self.inlines(node["inl"])
                if label in self.labels:
                    out.append(f'<a class="om-term" href='
                               f'"#{self.labels[label]["anchor"]}">{text}</a>')
                elif label in self.externals:
                    out.append(f'<a class="om-term" href='
                               f'"{self.externals[label]["href"]}">{text}</a>')
                else:
                    # target lives in a chapter not yet published: keep the
                    # link intent in the DOM, resolvable by a later run
                    out.append(f'<span class="om-term-future" data-omterm='
                               f'"{html.escape(label)}">{text}</span>')
            elif t == "eqref":
                info = self.resolve(node["label"], "\\eqref")
                out.append(f'<a class="om-cref" href="{info["href"]}">'
                           f"({info['number']})</a>")
            elif t == "ref":
                # bare \ref: the number alone, linked
                info = self.resolve(node["label"], "\\ref")
                out.append(f'<a class="om-cref" href="{info["href"]}">'
                           f"{info['number']}</a>")
            elif t == "field":
                # \sfield / \bfield lead-in
                out.append(f'<strong class="om-field">'
                           f"{self.inlines(node['inl'])}.</strong>")
            elif t == "cref":
                # labels may be line-wrapped in the source
                labels = [re.sub(r"\s+", "", part)
                          for part in node["label"].split(",")]
                infos = [self.resolve(lbl, "\\cref") for lbl in labels]
                if len(infos) == 1:
                    info = infos[0]
                    text = self.lang.cref_text(info["kind"], info["number"])
                    out.append(f'<a class="om-cref" href="{info["href"]}">'
                               f"{text}</a>")
                else:
                    kinds = {info["kind"] for info in infos}
                    if len(kinds) == 1:
                        # \cref{a,b} same kind: "Chapters 9 and 10"
                        name = self.lang.cref_plurals.get(infos[0]["kind"])
                        if not name:
                            raise ParseError(
                                f"no plural name for {infos[0]['kind']!r}")
                        links = [f'<a class="om-cref" href="{info["href"]}">'
                                 f'{info["number"]}</a>' for info in infos]
                        joined = (self.lang.and_sep.join(links)
                                  if len(links) == 2
                                  else self.lang.list_sep.join(links[:-1])
                                  + self.lang.and_sep + links[-1])
                        out.append(f"{name} {joined}")
                    else:
                        # mixed kinds: each reference spelled out in full
                        links = [
                            f'<a class="om-cref" href="{info["href"]}">'
                            + self.lang.cref_text(info["kind"],
                                                  info["number"])
                            + "</a>" for info in infos]
                        joined = (self.lang.and_sep.join(links)
                                  if len(links) == 2
                                  else self.lang.list_sep.join(links[:-1])
                                  + self.lang.and_sep + links[-1])
                        out.append(joined)
            else:
                raise ParseError(f"emitter: unknown inline {t!r}")
        return "".join(out)

    # -------------------------------------------------------------- blocks

    def blocks(self, nodes):
        out = []
        for node in nodes:
            t = node["t"]
            if t == "para":
                out.append(f"<p>{self.inlines(node['inl'])}</p>")
            elif t == "dmath":
                tex = node["tex"]
                anchor = ""
                if node.get("label"):
                    anchor = f' id="{anchor_for(node["label"])}"'
                    tex += f"\\tag{{{node['number']}}}"
                out.append(f'<div class="om-display"{anchor}>'
                           f"{self.math_ph(tex, display=True)}</div>")
            elif t == "section":
                title = self.inlines(node["inl"])
                if node["star"]:
                    out.append(f"<h2>{title}</h2>")
                else:
                    num = node["number"]
                    sid = f"sec-{num.replace('.', '-')}"
                    out.append(
                        f'<h2 id="{sid}"><span class="om-secnum">{num}'
                        f"</span> {title}</h2>")
            elif t == "subsection":
                title = self.inlines(node["inl"])
                if node["star"]:
                    out.append(f"<h3>{title}</h3>")
                else:
                    num = node["number"]
                    sid = f"sec-{num.replace('.', '-')}"
                    out.append(
                        f'<h3 id="{sid}"><span class="om-secnum">{num}'
                        f"</span> {title}</h3>")
            elif t == "admitted":
                # \admitted: a whole proof reading "Admitted at this level."
                out.append(
                    f'<div class="om-proof"><p>'
                    f'<span class="om-proof-lead">{self.lang.proof}.</span> '
                    f"<em>{self.lang.admitted}</em> "
                    f'<span class="om-qed">∎</span></p></div>')
            elif t == "env":
                out.append(self.env(node))
            elif t == "list":
                out.append(self.list_env(node))
            elif t == "figure":
                out.append(self.figure(node))
            elif t == "table":
                out.append(self.table(node))
            elif t == "centered":
                out.append(f'<p class="om-center">{self.inlines(node["inl"])}</p>')
            elif t == "tables":
                inner = "\n".join(self.table_inner(tbl)
                                  for tbl in node["tables"])
                out.append(f'<div class="om-table-wrap om-table-row">'
                           f"{inner}</div>")
            elif t == "tablefloat":
                out.append(self.table_float(node))
            elif t == "listing":
                out.append(self.listing(node))
            elif t == "lookfor":
                out.append(f'<p class="om-iq-lookfor"><em>'
                           f"{self.lang.iq_lookfor} "
                           f"{self.inlines(node['inl'])}</em></p>")
            else:
                raise ParseError(f"emitter: unknown block {t!r}")
        return "\n".join(out)

    def env(self, node):
        kind = node["kind"]
        if kind in STATEMENT_KINDS:
            return self.statement(node)
        if kind == "proof":
            return self.proof(node)
        if kind == "exercise":
            return self.exercise(node)
        if kind == "problem":
            return self.problem(node)
        if kind == "interviewq":
            return self.exercise(node, css="om-exercise om-iq")
        if kind in ("dated", "strategyfile", "predictorcard",
                    "tutorial", "build"):
            return self.quant_box(node)
        raise ParseError(f"emitter: unexpected environment {kind!r}")

    def quant_box(self, node):
        """Titled boxes of the quant books: "As of September 2026 — …",
        "Strategy file 23.1 — …", "Predictor card 4.2 — …"; tutorial and
        build boxes carry no title bar."""
        kind = node["kind"]
        anchor = f' id="{anchor_for(node["label"])}"' if node["label"] else ""
        body = self.blocks(node["body"])
        if kind in ("tutorial", "build"):
            return (f'<div class="om-box om-{kind}"{anchor}>\n{body}\n'
                    f"</div>")
        if kind == "dated":
            year, month = node["asof"].split("-")
            lead = f"{self.lang.as_of} {MONTHS[int(month) - 1]} {year}"
        else:
            lead = f"{self.lang.names[kind]} {node['number']}"
        head = (f'<p class="om-box-head"><span class="om-box-kind">{lead}'
                f'</span> <span class="om-box-note">— '
                f"{self.inlines(node['title'])}</span></p>")
        return (f'<section class="om-box om-{kind}"{anchor}>\n{head}\n'
                f"{body}\n</section>")

    def listing(self, node):
        """\\omcode: lines first..last of a tested source file, highlighted,
        numbered from `first` as in print, caption below."""
        from pathlib import Path
        path = Path(node["path"])     # relative to the book repo root
        if not path.exists():
            raise ParseError(f"listing source not found: {path}")
        lines = path.read_text(encoding="utf-8").split("\n")
        first, last = node["first"], node["last"]
        if not 1 <= first <= last <= len(lines):
            raise ParseError(f"listing range {first}..{last} outside "
                             f"{path} ({len(lines)} lines)")
        code = "\n".join(lines[first - 1:last])
        hl = highlight_lines(code, path.suffix)
        body = "\n".join(f'<span class="om-line" data-n="{first + k}">'
                         f"{line}</span>" for k, line in enumerate(hl))
        lang = LISTING_LEXERS[path.suffix]
        anchor = f' id="{anchor_for(node["label"])}"' if node["label"] else ""
        # listings in solutions are unnumbered here (print runs one counter
        # across the whole solutions appendix; nothing references them)
        num = (f'<strong>{self.lang.names["listing"]} '
               f"{node['number']}.</strong> " if "number" in node else "")
        caption = (f"{num}{self.inlines(node['caption'])} "
                   f'<span class="om-listing-path">'
                   f"{html.escape(str(path), quote=False)}</span>")
        return (f'<figure class="om-listing"{anchor}>\n'
                f'<pre class="om-code" data-lang="{lang}"><code>{body}'
                f"</code></pre>\n<figcaption>{caption}</figcaption>\n"
                f"</figure>")

    def table_float(self, node):
        tbl = node["table"]
        inner = (self.table_inner(tbl) if tbl["t"] == "table"
                 else "\n".join(self.table_inner(x) for x in tbl["tables"]))
        anchor = f' id="{anchor_for(node["label"])}"' if node["label"] else ""
        caption = self.inlines(node["caption"])
        if node["numbered"]:
            caption = (f'<strong>{self.lang.names["table"]} '
                       f"{node['number']}.</strong> {caption}")
        cap = f"\n<figcaption>{caption}</figcaption>" if caption else ""
        return (f'<figure class="om-figure om-table-float"{anchor}>\n'
                f'<div class="om-table-wrap">{inner}</div>{cap}\n'
                f"</figure>")

    def head(self, node, css_kind):
        num = node["number"]
        name = self.lang.names[node["kind"]]
        note = ""
        if node["title"]:
            note = (f' <span class="om-box-note">'
                    f"({self.inlines(node['title'])})</span>")
        return (f'<p class="om-box-head"><span class="om-box-kind">'
                f"{name} {num}</span>{note}</p>")

    def statement(self, node):
        anchor = f' id="{anchor_for(node["label"])}"' if node["label"] else ""
        body = self.blocks(node["body"])
        return (f'<section class="om-box om-{node["kind"]}"{anchor}>\n'
                f"{self.head(node, node['kind'])}\n{body}\n</section>")

    def proof(self, node):
        lead = (self.inlines(node["title"]) if node["title"]
                else self.lang.proof)
        body = self.blocks(node["body"])
        # inject the lead into the first paragraph, QED after the last block
        lead_html = f'<span class="om-proof-lead">{lead}.</span> '
        if body.startswith("<p>"):
            body = "<p>" + lead_html + body[len("<p>"):]
        else:
            body = f"<p>{lead_html}</p>\n" + body
        qed = '<span class="om-qed">∎</span>'
        if body.endswith("</p>"):
            body = body[:-len("</p>")] + " " + qed + "</p>"
        else:
            body += f'\n<p class="om-qed-line">{qed}</p>'
        return f'<div class="om-proof">\n{body}\n</div>'

    def exercise(self, node, css="om-exercise"):
        label = node["label"]
        anchor = f' id="{anchor_for(label)}"' if label else ""
        num = node["number"]
        name = self.lang.names[node["kind"]]
        parts = [f'<article class="{css}"{anchor}>']
        diff = ""
        if node.get("difficulty"):
            stars = "★" * node["difficulty"]
            diff = (f' <span class="om-difficulty" aria-label='
                    f'"{node["difficulty"]}/3">{stars}</span>')
        note = ""
        if node["title"]:
            note = (f'<p class="om-box-note om-problem-title">'
                    f"{self.inlines(node['title'])}</p>")
        tags = [self.inlines(node[k]) for k in ("roles", "firm")
                if node.get(k)]
        if tags:
            # interview questions: "trader, researcher • market maker"
            diff += (' <span class="om-iq-roles">'
                     + " • ".join(tags) + "</span>")
        parts.append(f'<p class="om-box-head"><span class="om-box-kind">'
                     f"{name} {num}</span>{diff}</p>")
        if note:
            parts.append(note)
        parts.append(self.blocks(node["body"]))
        parts.append(self.solution_details(label, num))
        parts.append("</article>")
        return "\n".join(p for p in parts if p)

    def problem(self, node):
        return self.exercise(node, css="om-exercise om-problem")

    def solution_details(self, label, num):
        if label is None or label not in self.solutions:
            raise ParseError(
                f"no solution found for {label!r} — the book guarantees "
                "exactly one solution per exercise/problem")
        kind = self.labels[label]["kind"]
        cref = self.lang.cref_text(kind, num)
        # "Solution" / "Oplossing": first word of the localized "Solution of"
        summary = self.lang.solution_of.split()[0]
        body = self.blocks(self.solutions[label])
        opening = (f'<p class="om-solution-of"><strong>'
                   f"{self.lang.solution_of} {cref}.</strong></p>")
        return (f'<details class="om-solution" id="sol-{anchor_for(label)}">'
                f"\n<summary>{summary}</summary>\n{opening}\n{body}\n"
                f"</details>")

    def list_env(self, node):
        if node["kind"] == "itemize":
            tag_open, tag_close = "<ul>", "</ul>"
        elif node["kind"] == "steps":
            # tutorial steps: "Step N." markers come from the CSS
            tag_open, tag_close = '<ol class="om-steps">', "</ol>"
        else:
            start = node.get("start", 1)
            attr = f' start="{start}"' if start != 1 else ""
            tag_open, tag_close = f"<ol{attr}>", "</ol>"
        items = []
        for item in node["items"]:
            body = self.blocks(item)
            # single-paragraph items read better without the <p> wrapper
            if body.startswith("<p>") and body.endswith("</p>") \
                    and body.count("<p>") == 1:
                body = body[len("<p>"):-len("</p>")]
            items.append(f"<li>{body}</li>")
        out = tag_open + "\n" + "\n".join(items) + "\n" + tag_close
        if node.get("sources"):
            out = (f'<div class="om-sources">\n<p class="om-sources-head">'
                   f"{self.lang.sources_head}</p>\n{out}\n</div>")
        return out

    def figure(self, node):
        caption = self.inlines(node["caption"])
        alt = plaintext(node["caption"]).strip()
        sublabels = node.get("sublabels") or {}
        widths = node.get("widths") or {}
        parts = []
        for i, src in enumerate(node["tikzs"]):
            fig = self.figures[src]
            if i in widths:
                # minipage sub-figure: its share of the row, no phone floor
                fig = dict(fig, rel_width=widths[i], sub=True)
            img = self.img_tag(fig, alt)
            if i in sublabels or i in widths:
                # a picture with its own sub-caption (leading picture of a
                # grid, or a minipage sub-figure)
                sub = self.inlines(sublabels[i]) if i in sublabels else ""
                img = (f'<figure class="om-subfig">{img}'
                       + (f"<figcaption>{sub}</figcaption>" if sub else "")
                       + "</figure>")
            parts.append(img)
        imgs = "\n".join(parts)
        if node.get("table") is not None:
            tbl = node["table"]
            inner = (self.table_inner(tbl) if tbl["t"] == "table"
                     else "\n".join(self.table_inner(x) for x in tbl["tables"]))
            imgs = f'<div class="om-table-wrap">{inner}</div>'
        grid = ""
        if node.get("grid"):
            rows = []
            for row in node["grid"]:
                cells = "".join(
                    f'<figure class="om-subfig">'
                    f'{self.img_tag(self.figures[c["src"]], plaintext(c["label"]).strip() or alt)}'
                    f'<figcaption>{self.inlines(c["label"])}</figcaption>'
                    "</figure>"
                    for c in row)
                rows.append(f'<div class="om-figure-row">{cells}</div>')
            grid = '\n<div class="om-figure-grid">\n' + "\n".join(rows) \
                + "\n</div>"
        anchor = ""
        if node.get("label"):
            anchor = f' id="{anchor_for(node["label"])}"'
        if node.get("number"):
            caption = (f'<strong>{self.lang.names["figure"]} '
                       f"{node['number']}.</strong> {caption}")
        return (f'<figure class="om-figure"{anchor}>\n'
                f'<div class="om-figure-row">\n{imgs}\n</div>{grid}\n'
                f"<figcaption>{caption}</figcaption>\n</figure>")

    def img_tag(self, fig, alt):
        """Photos keep their print proportion (`width=0.52\\linewidth` →
        width:52%, floored so they stay readable on phones; `height=3.1cm`
        → a CSS height, scaled up since the reader column is wider than
        the printed page); SVG figures size themselves from their
        intrinsic width."""
        style = ""
        if fig.get("rel_width") and fig.get("sub"):
            # side-by-side sub-figures share the row as in print; the
            # phone media query stacks them at full width
            style = f' style="width:{round(fig["rel_width"] * 100)}%"'
        elif fig.get("rel_width"):
            style = f' style="width:{max(50, round(fig["rel_width"] * 100))}%"'
        elif fig.get("height_cm"):
            style = (f' style="height:{round(fig["height_cm"] * 1.5, 2)}cm;'
                     'width:auto"')
        alt = html.escape(alt, quote=True)
        return (f'<img src="{fig["url"]}" alt="{alt}" '
                f'width="{fig["width"]}" height="{fig["height"]}"'
                f'{style} loading="lazy">')

    def table(self, node):
        return ('<div class="om-table-wrap">' + self.table_inner(node)
                + "</div>")

    def table_inner(self, node):
        align = node.get("align")   # booktabs tables only
        rows = []
        if node["header"]:
            cells = self.row_cells("th", node["header"], align)
            rows.append(f"<thead><tr>{cells}</tr></thead>")
        body_rows = []
        for row in node["rows"]:
            cells = self.row_cells("td", row["cells"], align)
            attr = ' class="om-rule"' if row["rule"] else ""
            body_rows.append(f"<tr{attr}>{cells}</tr>")
        rows.append("<tbody>" + "".join(body_rows) + "</tbody>")
        css = "om-table om-booktabs" if node.get("booktabs") else "om-table"
        return f'<table class="{css}">' + "".join(rows) + "</table>"

    def row_cells(self, tag, cells, align):
        if not align:
            return "".join(self.cell(tag, c) for c in cells)
        out, col = [], 0
        for c in cells:
            # booktabs text tables: the colspec's alignment per column
            # (om-l / om-c / om-r); a \multicolumn spans several columns
            span = c[0]["cols"] if len(c) == 1 and c[0]["t"] == "span" else 1
            out.append(self.cell(tag, c, align[col] if col < len(align)
                                 else None))
            col += span
        return "".join(out)

    def cell(self, tag, inl, align=None):
        """One table cell; a lone span node (\\multicolumn) → colspan."""
        cls = f' class="om-{align}"' if align else ""
        if len(inl) == 1 and inl[0]["t"] == "span":
            return (f'<{tag}{cls} colspan="{inl[0]["cols"]}">'
                    f"{self.inlines(inl[0]['inl'])}</{tag}>")
        return f"<{tag}{cls}>{self.inlines(inl)}</{tag}>"


def footnotes_html(emitter):
    """End-of-chapter footnote list with backlinks (empty string if none)."""
    if not emitter.footnotes:
        return ""
    items = "\n".join(
        f'<li id="fn-{i + 1}">{body} '
        f'<a href="#fnref-{i + 1}" class="om-fnback" '
        f'aria-label="Back to text">↩</a></li>'
        for i, body in enumerate(emitter.footnotes))
    return (f'\n<section class="om-footnotes">\n<ol>\n{items}\n</ol>\n'
            f"</section>")


def substitute_math(html_text, rendered):
    """Replace \\x00M<i>\\x00 placeholders with KaTeX output."""
    def repl(m):
        return rendered[int(m.group(1))]
    return re.sub("\x00M(\\d+)\x00", repl, html_text)
