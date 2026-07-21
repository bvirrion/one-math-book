#!/usr/bin/env python3
"""Extract a book's full table of contents into the online-reader manifest.

Usage (from the repo root):

    python3 tools/build_html_toc.py \
        --entry one_math_book_2_high_school.tex \
        --book math-2 \
        --languages en,fr,nl \
        --out ../../saas/resources/onecourse/chapters

Reads the entry file's part inputs, each part.tex's ordered \\ominput list,
the (localized) \\chapter{...}\\label{ch:...} first lines and the part
titles from styles/lang/<lang>.tex, and writes a `toc` array under
books.<book> in the existing manifest.json — every chapter of the book,
published online or not, so the website can render the whole book's
navigation with unpublished chapters grayed out.

Strict on purpose: any line this script cannot read exactly (a chapter
title growing a macro, a missing part title, a label mismatch between
languages, a published chapter whose key/number/title disagrees with the
computed toc) aborts the run. Extend the script deliberately; never let it
guess. Run AFTER build_html_chapter.py: the toc is validated against (and
stored next to) the published chapters, and a from-scratch manifest
rebuild drops the toc key until this script runs again.
"""

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

CHAPTER_RE = re.compile(
    r"\\chapter\{([^{}]*)\}\s*\\label\{(ch:[a-z0-9:]+)\}")


def fail(msg):
    sys.exit(f"error: {msg}")


ACCENTS = {"'": "́", "`": "̀", "^": "̂",
           '"': "̈", "~": "̃", "c": "̧", "H": "̋"}


def detex(text, where):
    import unicodedata

    # accents first (\'e, \`{a}, \c{c}, ...) — before quote curling,
    # which would otherwise eat the accent characters
    text = re.sub(
        r"\\(['`^\"~cH])\{?([A-Za-z])\}?",
        lambda m: unicodedata.normalize(
            "NFC", m.group(2) + ACCENTS[m.group(1)]),
        text)
    sup = {"a": "ᵃ", "e": "ᵉ", "r": "ʳ", "n": "ⁿ", "d": "ᵈ", "t": "ᵗ",
           "h": "ʰ", "s": "ˢ", "o": "ᵒ"}

    def superscript(m):
        letters = m.group(1)
        if any(ch not in sup for ch in letters):
            fail(f"{where}: \\textsuperscript{{{letters}}} has no Unicode "
                 "superscript mapping — extend build_html_toc.py")
        return "".join(sup[ch] for ch in letters)

    text = re.sub(r"\\textsuperscript\{([A-Za-z]+)\}", superscript, text)
    text = text.replace("\\oe{}", "œ").replace("\\oe ", "œ")
    text = text.replace("\\,", " ")  # thin space, as the chapter parser
    text = text.replace("---", "—").replace("--", "–").replace("~", " ")
    # same typographic quotes the chapter converter produces
    text = text.replace("``", "“").replace("''", "”")
    text = text.replace("`", "‘").replace("'", "’")
    if "\\" in text or "{" in text or "}" in text:
        fail(f"{where}: title {text!r} contains LaTeX markup — extend "
             "build_html_toc.py deliberately instead of letting it guess")
    return re.sub(r"\s+", " ", text).strip()


def part_dirs(entry_path):
    text = entry_path.read_text(encoding="utf-8")
    dirs = re.findall(r"\\input\{(parts/[a-z0-9-]+)/part\}", text)
    if not dirs:
        fail(f"{entry_path}: no \\input{{parts/<dir>/part}} lines found")
    return dirs


def part_of(part_path):
    """Returns (part_string_key, [chapter file slugs])."""
    text = part_path.read_text(encoding="utf-8")
    m = re.search(r"\\part\{\\omstr\{(part\.[a-z0-9]+)\}\}", text)
    if not m:
        fail(f"{part_path}: no \\part{{\\omstr{{...}}}} line")
    inputs = re.findall(r"\\ominput\{([a-z0-9-]+)\}\{([0-9]{2}-[a-z0-9-]+)\}",
                        text)
    if not inputs:
        fail(f"{part_path}: no \\ominput lines")
    expected_dir = part_path.parent.name
    for grade_dir, _ in inputs:
        if grade_dir != expected_dir:
            fail(f"{part_path}: \\ominput dir {grade_dir!r} does not match "
                 f"the part directory {expected_dir!r}")
    return m.group(1), [slug for _, slug in inputs]


def part_titles(langs):
    """{part_string_key: {lang: raw_title}} from styles/lang/<lang>.tex.
    Raw: de-TeXing happens only for the parts the book actually uses, so
    an exotic macro in an unrelated part title cannot break the build."""
    titles = {}
    for lang in langs:
        path = REPO_ROOT / "styles" / "lang" / f"{lang}.tex"
        text = path.read_text(encoding="utf-8")
        for m in re.finditer(
                r"\\@namedef\{omstr@(part\.[a-z0-9]+)\}\{(.*)\}", text):
            titles.setdefault(m.group(1), {})[lang] = m.group(2)
    return titles


def chapter_title_and_label(grade_dir, slug, lang):
    """(title, label) for one chapter file in one language; EN fallback."""
    path = REPO_ROOT / "parts" / grade_dir / lang / f"{slug}.tex"
    if lang == "en" or not path.exists():
        if lang != "en":
            print(f"notice: {grade_dir}/{lang}/{slug}.tex missing — "
                  "falling back to the English title")
        path = REPO_ROOT / "parts" / grade_dir / f"{slug}.tex"
    if not path.exists():
        fail(f"missing chapter file {path}")
    m = CHAPTER_RE.search(path.read_text(encoding="utf-8"))
    if not m:
        fail(f"{path}: no \\chapter{{...}}\\label{{ch:...}} line matched")
    return detex(m.group(1), str(path)), m.group(2)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--entry", required=True,
                    help="book entry file, e.g. one_math_book_2_high_school.tex")
    ap.add_argument("--book", required=True, help="manifest book key")
    ap.add_argument("--languages", default="en,fr,nl")
    ap.add_argument("--out", required=True,
                    help="directory containing manifest.json")
    args = ap.parse_args()

    langs = [lang.strip() for lang in args.languages.split(",")]
    manifest_path = Path(args.out) / "manifest.json"
    if not manifest_path.exists():
        fail(f"{manifest_path} not found — run build_html_chapter.py first "
             "(the toc is validated against the published chapters)")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    lang_part_titles = part_titles(langs)
    toc = []
    number = 0
    seen_keys = set()

    for part_dir in part_dirs(REPO_ROOT / args.entry):
        part_path = REPO_ROOT / part_dir / "part.tex"
        string_key, slugs = part_of(part_path)
        raw_titles = lang_part_titles.get(string_key)
        if not raw_titles or any(lang not in raw_titles for lang in langs):
            fail(f"part title {string_key!r} missing for some of {langs}")
        titles = {lang: detex(raw, f"styles/lang/{lang}.tex {string_key}")
                  for lang, raw in raw_titles.items() if lang in langs}
        part_key = part_dir.split("/")[-1]

        chapters = []
        for slug in slugs:
            number += 1
            ch_titles, labels = {}, set()
            for lang in langs:
                title, label = chapter_title_and_label(part_key, slug, lang)
                ch_titles[lang] = title
                labels.add(label)
            if len(labels) != 1:
                fail(f"{part_key}/{slug}: \\label differs across languages: "
                     f"{sorted(labels)}")
            key = labels.pop().split(":", 1)[1].replace(":", "-")
            if key in seen_keys:
                fail(f"duplicate chapter key {key!r}")
            seen_keys.add(key)
            chapters.append({"key": key, "number": number,
                             "titles": ch_titles})

        toc.append({"key": part_key, "titles": titles, "chapters": chapters})

    # ---- consistency with the published chapters -----------------------
    by_key = {c["key"]: c for part in toc for c in part["chapters"]}
    for published in manifest["books"].get(args.book, {}).get("chapters", []):
        entry = by_key.get(published["key"])
        if entry is None:
            fail(f"published chapter {published['key']!r} is not in the "
                 "computed toc")
        if entry["number"] != published["number"]:
            fail(f"chapter {published['key']!r}: toc number "
                 f"{entry['number']} != published number "
                 f"{published['number']} — renumbering drift")
        for lang, edition in published["languages"].items():
            if lang in entry["titles"] \
                    and entry["titles"][lang] != edition["title"]:
                fail(f"chapter {published['key']!r} [{lang}]: toc title "
                     f"{entry['titles'][lang]!r} != published title "
                     f"{edition['title']!r}")

    book = manifest["books"].setdefault(args.book, {"chapters": []})
    book["toc"] = toc
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    total = sum(len(p["chapters"]) for p in toc)
    print(f"toc: {len(toc)} parts, {total} chapters, "
          f"{len(langs)} languages -> {manifest_path}")


if __name__ == "__main__":
    main()
