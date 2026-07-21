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


def plaintext(inlines):
    out = []
    for node in inlines:
        t = node["t"]
        if t == "text":
            out.append(node["s"])
        elif t == "math":
            out.append(tex_to_alt(node["tex"]))
        elif t in ("emph", "bold", "sup"):
            out.append(plaintext(node["inl"]))
        elif t == "term":
            out.append(plaintext(node["inl"]))
        elif t == "cref":
            out.append("")  # resolved text needs labels; unused in meta
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
            elif t == "sup":
                out.append(f"<sup>{self.inlines(node['inl'])}</sup>")
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
                        name = self.lang.plurals.get(infos[0]["kind"])
                        if not name:
                            raise ParseError(
                                f"no plural name for {infos[0]['kind']!r}")
                        links = [f'<a class="om-cref" href="{info["href"]}">'
                                 f'{info["number"]}</a>' for info in infos]
                        joined = (f" {self.lang.and_word} ".join(links)
                                  if len(links) == 2
                                  else ", ".join(links[:-1])
                                  + f" {self.lang.and_word} " + links[-1])
                        out.append(f"{name} {joined}")
                    else:
                        # mixed kinds: each reference spelled out in full
                        links = [
                            f'<a class="om-cref" href="{info["href"]}">'
                            + self.lang.cref_text(info["kind"],
                                                  info["number"])
                            + "</a>" for info in infos]
                        joined = (f" {self.lang.and_word} ".join(links)
                                  if len(links) == 2
                                  else ", ".join(links[:-1])
                                  + f" {self.lang.and_word} " + links[-1])
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
            elif t == "tables":
                inner = "\n".join(self.table_inner(tbl)
                                  for tbl in node["tables"])
                out.append(f'<div class="om-table-wrap om-table-row">'
                           f"{inner}</div>")
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
        raise ParseError(f"emitter: unexpected environment {kind!r}")

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
        return tag_open + "\n" + "\n".join(items) + "\n" + tag_close

    def figure(self, node):
        caption = self.inlines(node["caption"])
        alt = html.escape(plaintext(node["caption"]).strip(), quote=True)
        imgs = "\n".join(
            f'<img src="{fig["url"]}" alt="{alt}" '
            f'width="{fig["width"]}" height="{fig["height"]}" loading="lazy">'
            for fig in (self.figures[tikz] for tikz in node["tikzs"]))
        anchor = ""
        if node.get("label"):
            anchor = f' id="{anchor_for(node["label"])}"'
            caption = (f'<strong>{self.lang.names["figure"]} '
                       f"{node['number']}.</strong> {caption}")
        return (f'<figure class="om-figure"{anchor}>\n'
                f'<div class="om-figure-row">\n{imgs}\n</div>\n'
                f"<figcaption>{caption}</figcaption>\n</figure>")

    def table(self, node):
        return ('<div class="om-table-wrap">' + self.table_inner(node)
                + "</div>")

    def table_inner(self, node):
        rows = []
        if node["header"]:
            cells = "".join(f"<th>{self.inlines(c)}</th>"
                            for c in node["header"])
            rows.append(f"<thead><tr>{cells}</tr></thead>")
        body_rows = []
        for row in node["rows"]:
            cells = "".join(f"<td>{self.inlines(c)}</td>"
                            for c in row["cells"])
            attr = ' class="om-rule"' if row["rule"] else ""
            body_rows.append(f"<tr{attr}>{cells}</tr>")
        rows.append("<tbody>" + "".join(body_rows) + "</tbody>")
        return '<table class="om-table">' + "".join(rows) + "</table>"


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
