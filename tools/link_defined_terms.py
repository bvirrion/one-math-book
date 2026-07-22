#!/usr/bin/env python3
"""Link defined terms to their definitions.

Wraps a term as \\omterm{def:...}{term} so it links back to the definition that
introduces it. Every occurrence is linked -- course text, exercises, problems and
solutions -- so a reader can always jump from a term to the place it is defined.

    python3 tools/link_defined_terms.py --book 3                  # dry run
    python3 tools/link_defined_terms.py --book 3 --apply          # rewrite
    python3 tools/link_defined_terms.py --book 1 --lang fr --apply
    python3 tools/link_defined_terms.py --book 1 --unwrap --apply # strip links

Run from the repository root. --book is mandatory: a defaulted book is how the
wrong one gets rewritten.

Regenerating: re-running --apply can only ADD links, so removing a term from a
config appears to work (0 new links) while its stale links stay in the sources.
Always --unwrap --apply first, then --apply.

What is linked is decided by two things:
  * the rules, in tools/termlink/ -- shared by every book, do not tune them for
    one book (tools/check_book5_golden.sh will catch you);
  * the vocabulary, in tools/term_config/book<N>_<lang>.py -- one file per book
    and language, and the only file a book's author should need to touch.
"""
import argparse
import collections
import importlib
import re
import sys

sys.path.insert(0, "tools")

from termlink import books, harvest, protect, wrap        # noqa: E402

DEFAULTS = dict(
    STOP=set(), NOT_A_TERM=("theorem", "lemma", "inequality", "formula",
                            "criterion", "principle", "identity", "rule",
                            "law of", "paradox", "problem"),
    DERIVED={}, PRIMARY_OK=set(), AMBIG_POLICY="drop", EXTRA={}, DROP=set(),
    NO_CAPITAL=set(), MAX_TERM_WORDS=None, MAX_TERM_CHARS=None, EXTRA_PROTECT=[],
)


class Config:
    def __init__(self, mod):
        for k, v in DEFAULTS.items():
            setattr(self, k, getattr(mod, k, v))


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--book", type=int, required=True, choices=sorted(books.ENTRY))
    ap.add_argument("--lang", default="en",
                    choices=("en", "fr", "nl", "es", "pt"))
    ap.add_argument("--apply", action="store_true", help="rewrite the sources")
    ap.add_argument("--unwrap", action="store_true",
                    help="strip existing links instead of adding them")
    ap.add_argument("--check", action="store_true",
                    help="regenerate in memory and report any file whose links "
                         "on disk differ; writes nothing, so it is safe to run "
                         "while another book is being generated")
    ap.add_argument("--terms", action="store_true", help="list the linkable terms")
    args = ap.parse_args()

    if args.lang not in books.LANGS[args.book]:
        ap.error("book %d has no %s edition" % (args.book, args.lang))

    fs = books.files(args.book, args.lang)
    if not fs:
        ap.error("no sources found for book %d (%s)" % (args.book, args.lang))

    if args.unwrap:
        stripped = 0
        for path, _, _ in fs:
            s = open(path, encoding="utf8").read()
            out = wrap.unwrap(s)
            stripped += len(wrap.OMTERM.findall(s))
            if args.apply and out != s:
                open(path, "w", encoding="utf8").write(out)
        print("links %s: %d across %d files"
              % ("removed" if args.apply else "to remove", stripped, len(fs)))
        return

    cfg = Config(importlib.import_module(
        "term_config.book%d_%s" % (args.book, args.lang)))
    langcfg = importlib.import_module("term_config.lang_%s" % args.lang)

    # --check regenerates from the unwrapped sources without writing anything,
    # so it can run while another book is being generated.
    disk = {path: harvest.read(path) for path, _, _ in fs} if args.check else {}
    load = (lambda p: wrap.unwrap(disk[p])) if args.check else harvest.read

    terms, def_seq, local, primary, nearest, stats = harvest.harvest(
        fs, cfg, args.lang, langcfg, load)
    mask = protect.masker(cfg.EXTRA_PROTECT)

    total = collections.Counter()
    by_prefix = collections.Counter()
    stale = []
    for path, seq, is_sol in fs:
        s, labs = wrap.wrap_file(path, seq, is_sol, terms, def_seq, local,
                                 primary, nearest, mask, args.lang, langcfg,
                                 cfg.NO_CAPITAL, load)
        if labs:
            total[path] = len(labs)
            by_prefix.update(lab.split(":", 1)[0] for lab in labs)
        if args.check and s != disk[path]:
            stale.append(path)
        if args.apply:
            open(path, "w", encoding="utf8").write(s)

    if args.terms:
        for t, lab in sorted(terms.items()):
            print("  %-40s -> %s" % (t, lab))
        for t in sorted(nearest):
            print("  %-40s -> %s (nearest preceding)"
                  % (t, ", ".join("%d:%s" % p for p in nearest[t])))

    print("book %d (%s)" % (args.book, args.lang))
    print("terms harvested        : %d" % stats["harvested"])
    print("dropped (defined twice): %d" % stats["ambiguous"])
    print("dropped (stoplist)     : %d" % stats["stoplisted"])
    print("LINKABLE TERMS         : %d" % stats["linkable"])
    if nearest:
        print("chapter-local terms    : %d" % len(nearest))
    print("links %s: %d across %d files"
          % ("inserted" if args.apply else "to insert", sum(total.values()), len(total)))
    print("by target              : %s"
          % ", ".join("%s %d" % (k, v) for k, v in by_prefix.most_common()))

    if args.check:
        if stale:
            print("STALE: %d file(s) do not match what the config generates:"
                  % len(stale))
            for p in stale:
                print("  %s" % p)
            sys.exit(1)
        print("CHECK: every file matches what the config generates")


if __name__ == "__main__":
    main()
