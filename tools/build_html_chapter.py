#!/usr/bin/env python3
"""Convert a book chapter to HTML for the one-course.com online reader.

Usage (from the repo root):

    python3 tools/build_html_chapter.py \
        --chapter parts/grade-10/01-numbers-and-sets.tex \
        --chapter-number 1 \
        --book math-2 \
        --languages en,fr,nl \
        --out ../../saas/resources/onecourse/chapters \
        --svg-out ../../saas/public/images/onecourse/chapters

Without --out/--svg-out everything lands under build/html/ (never commit
build output in this repo). The converter is strict by design: any LaTeX
construct it does not know raises an error instead of being dropped, and
all language editions must have the same environment/label structure.

Requires: node with `npm install` done in tools/htmlbook/ (KaTeX), and
pdflatex + dvisvgm (or pdftocairo) for the figures.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from htmlbook import lexer, model  # noqa: E402
from htmlbook.emit_html import Emitter, plaintext, slugify, substitute_math  # noqa: E402
from htmlbook.model import anchor_for  # noqa: E402
from htmlbook.langstrings import LangStrings  # noqa: E402
from htmlbook.tikz2svg import FigureBuilder  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
HTMLBOOK_DIR = Path(__file__).resolve().parent / "htmlbook"

# KaTeX equivalents of the math macros in styles/onemath.sty (567-614).
# \st is language-dependent and added per language below.
KATEX_MACROS = {
    "\\N": "\\mathbb{N}",
    "\\Z": "\\mathbb{Z}",
    "\\Q": "\\mathbb{Q}",
    "\\R": "\\mathbb{R}",
    "\\C": "\\mathbb{C}",
    "\\abs": "\\left\\lvert#1\\right\\rvert",
    "\\norm": "\\left\\lVert#1\\right\\rVert",
    "\\floor": "\\left\\lfloor#1\\right\\rfloor",
    "\\intcc": "\\left[#1,\\,#2\\right]",
    "\\intoo": "\\left(#1,\\,#2\\right)",
    "\\intco": "\\left[#1,\\,#2\\right)",
    "\\intoc": "\\left(#1,\\,#2\\right]",
    "\\intint": "[\\![#1,\\,#2]\\!]",
    "\\vertiii": ("\\left\\vert\\kern-0.3ex\\left\\vert\\kern-0.3ex"
                  "\\left\\vert#1\\right\\vert\\kern-0.3ex\\right\\vert"
                  "\\kern-0.3ex\\right\\vert"),
    "\\dd": "\\mathop{}\\!\\mathrm{d}",
    "\\eu": "\\mathrm{e}",
    "\\iu": "\\mathrm{i}",
    "\\vect": "\\overrightarrow{#1}",
    "\\scal": "\\vect{#1}\\cdot\\vect{#2}",
    "\\conj": "\\overline{#1}",
    "\\Rea": "\\operatorname{Re}",
    "\\Ima": "\\operatorname{Im}",
    "\\Arg": "\\operatorname{arg}",
    "\\P": "\\mathbb{P}",
    "\\E": "\\mathbb{E}",
    "\\V": "\\mathbb{V}",
    "\\pcond": "\\P_{#1}\\!\\left(#2\\right)",
    "\\lcm": "\\operatorname{lcm}",
}


def chapter_paths(chapter, lang):
    """EN canonical parts/<year>/NN-slug.tex; other languages in a
    parts/<year>/<lang>/ subdirectory, solutions likewise. No fallback to
    English here: the website only publishes finished translations."""
    chapter = Path(chapter)
    year_dir, name = chapter.parent, chapter.name
    if lang == "en":
        body = year_dir / name
        sols = year_dir / "solutions" / name
    else:
        body = year_dir / lang / name
        sols = year_dir / "solutions" / lang / name
    for p in (body, sols):
        if not p.exists():
            sys.exit(f"error: missing source file {p}")
    return body, sols


def render_math(segments, macros):
    """Batch-render formulas with KaTeX via node."""
    if not segments:
        return []
    payload = json.dumps({
        "macros": macros,
        "segments": [{"tex": t, "display": d} for t, d in segments],
    })
    res = subprocess.run(
        ["node", "katex_render.mjs"], cwd=HTMLBOOK_DIR, input=payload,
        capture_output=True, text=True)
    if res.returncode != 0:
        sys.exit(f"error: KaTeX rendering failed:\n{res.stderr}")
    return json.loads(res.stdout)


def katex_version():
    pkg = HTMLBOOK_DIR / "node_modules" / "katex" / "package.json"
    if not pkg.exists():
        sys.exit("error: run `npm install` in tools/htmlbook/ first")
    return json.loads(pkg.read_text())["version"]


def first_paragraph_text(blocks, limit=160):
    for b in blocks:
        if b["t"] == "para":
            text = plaintext(b["inl"]).strip()
            if len(text) <= limit:
                return text
            cut = text[:limit].rsplit(" ", 1)[0]
            return cut.rstrip(",;:") + "…"
    return ""


def collect_figures(blocks, out):
    for b in blocks:
        if b["t"] == "figure":
            out.append(b["tikz"])
        elif b["t"] == "env":
            collect_figures(b["body"], out)
        elif b["t"] == "list":
            for item in b["items"]:
                collect_figures(item, out)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--chapter", required=True,
                    help="EN chapter file, e.g. parts/grade-10/01-….tex")
    ap.add_argument("--chapter-number", type=int, required=True)
    ap.add_argument("--book", default="math-2",
                    help="book key used in URLs and the manifest")
    ap.add_argument("--languages", default="en,fr,nl")
    ap.add_argument("--out", default=str(REPO_ROOT / "build" / "html"),
                    help="fragment + manifest output directory")
    ap.add_argument("--svg-out",
                    default=str(REPO_ROOT / "build" / "html" / "images"),
                    help="figure SVG output directory (book/chapter "
                         "subdirectories are created inside)")
    ap.add_argument("--svg-url-prefix", default="/images/onecourse/chapters",
                    help="public URL prefix the <img> tags point at")
    args = ap.parse_args()

    langs = [lang.strip() for lang in args.languages.split(",")]
    out_dir = Path(args.out)
    version = katex_version()

    # ---- parse every language ------------------------------------------
    editions = {}
    for lang in langs:
        body_path, sols_path = chapter_paths(args.chapter, lang)
        title, ch_label, blocks = lexer.parse_chapter(body_path)
        solutions = lexer.parse_solutions(sols_path)
        labels = model.number_chapter(blocks, args.chapter_number)
        model.resume_list_starts(blocks)
        editions[lang] = {
            "title": title, "label": ch_label, "blocks": blocks,
            "solutions": solutions, "labels": labels,
            "strings": LangStrings(REPO_ROOT, lang),
        }
        print(f"[{lang}] parsed {body_path.name}: "
              f"{len(labels)} labels, {len(solutions)} solutions")

    # ---- structural parity across languages ----------------------------
    model.check_parity({lang: model.structure_signature(e["blocks"])
                        for lang, e in editions.items()})
    ch_key = editions[langs[0]]["label"].split(":", 1)[1].replace(":", "-")

    # ---- cross-chapter references --------------------------------------
    # Labels of OTHER already-published chapters (from the existing
    # manifest) resolve to links into their pages; the URL scheme mirrors
    # the website routes: /books/{subject}/{n}/{lang}/chapter/{slug}.
    manifest_path = out_dir / "manifest.json"
    manifest = {"katex_version": version, "books": {}}
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["katex_version"] = version
    subject, book_number = args.book.rsplit("-", 1)

    def externals_for(lang):
        externals = {}
        for other in manifest["books"].get(args.book, {}).get("chapters", []):
            if other["key"] == ch_key:
                continue
            edition = (other["languages"].get(lang)
                       or other["languages"].get("en"))
            if not edition:
                continue
            page = (f"/books/{subject}/{book_number}/"
                    f"{lang if lang in other['languages'] else 'en'}"
                    f"/chapter/{edition['slug']}")
            for label, info in other.get("labels", {}).items():
                externals[label] = {"kind": info["kind"],
                                    "number": info["number"],
                                    "href": f"{page}#{anchor_for(label)}"}
        return externals

    # ---- figures (deduped by content hash across languages) ------------
    svg_dir = Path(args.svg_out) / args.book / ch_key
    builder = FigureBuilder(svg_dir, f"{args.svg_url_prefix}/{args.book}/"
                                     f"{ch_key}")
    figures = {}
    for lang in langs:
        tikzs = []
        collect_figures(editions[lang]["blocks"], tikzs)
        for tikz in tikzs:
            figures[tikz] = builder.figure_info(tikz)
    print(f"figures: {len(set(f['file'] for f in figures.values()))} SVG(s) "
          f"for {len(figures)} tikzpicture(s)")

    # ---- emit + render per language ------------------------------------
    manifest_langs = {}
    for lang in langs:
        e = editions[lang]
        emitter = Emitter(e["strings"], e["labels"], e["solutions"],
                          figures, args.chapter_number,
                          externals=externals_for(lang))
        html_body = emitter.blocks(e["blocks"])
        macros = dict(KATEX_MACROS, **{"\\st": e["strings"].st_macro})
        rendered = render_math(emitter.math, macros)
        html_body = substitute_math(html_body, rendered)

        title_text = plaintext(e["title"]).strip()
        slug = f"{args.chapter_number}-{slugify(title_text)}"
        rel = f"{args.book}/{lang}/{ch_key}.html"
        frag_path = out_dir / rel
        frag_path.parent.mkdir(parents=True, exist_ok=True)
        frag_path.write_text(html_body + "\n", encoding="utf-8")

        headings = [plaintext(b["inl"]).strip()
                    for b in e["blocks"] if b["t"] == "section"]
        manifest_langs[lang] = {
            "slug": slug,
            "title": title_text,
            "description_fallback": first_paragraph_text(e["blocks"]),
            "headings": headings,
            "fragment": rel,
        }
        print(f"[{lang}] wrote {frag_path} "
              f"({len(emitter.math)} formulas rendered)")

    # ---- manifest (merged, so future chapters/books accumulate) --------
    kinds = [info["kind"]
             for info in editions[langs[0]]["labels"].values()]
    entry = {
        "key": ch_key,
        "number": args.chapter_number,
        "languages": manifest_langs,
        "exercise_count": kinds.count("exercise"),
        "problem_count": kinds.count("problem"),
        "figures": sorted(set(f["file"] for f in figures.values())),
        # language-independent label map (numbers match across editions),
        # used to resolve cross-chapter \cref/\omterm on later runs
        "labels": {label: {"kind": info["kind"], "number": info["number"]}
                   for label, info in editions[langs[0]]["labels"].items()},
    }
    book = manifest["books"].setdefault(args.book, {"chapters": []})
    book["chapters"] = [c for c in book["chapters"] if c["key"] != ch_key]
    book["chapters"].append(entry)
    book["chapters"].sort(key=lambda c: c["number"])
    manifest_path.write_text(json.dumps(manifest, indent=2,
                                        ensure_ascii=False) + "\n",
                             encoding="utf-8")
    print(f"manifest: {manifest_path}")


if __name__ == "__main__":
    main()
