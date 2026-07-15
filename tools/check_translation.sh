#!/bin/bash
# Structural gate for a translated edition.
#
#   bash tools/check_translation.sh bachelor-3 fr     # one year, one language
#   bash tools/check_translation.sh                   # every year x {fr,nl}
#
# A clean pdflatex build proves almost nothing about a translation: \ominput
# silently falls back to the English body when a translated file is missing,
# and \omstr expands to nothing when a lang key is missing. Both failures
# build green. So completeness and structure are checked here, against the
# English source, file by file.
#
# Needs bash (process substitution), not sh.
cd "$(dirname "$0")/.." || exit 2

fail=0
bad() { fail=1; printf '  FAIL  %-44s %s\n' "$1" "$2"; }

check_year_lang() {
  local year=$1 lang=$2
  local dir="parts/$year" tdir="parts/$year/$lang"
  local sdir="parts/$year/solutions" tsdir="parts/$year/solutions/$lang"

  echo "== $year / $lang =="

  if [ ! -d "$tdir" ]; then
    bad "$year/$lang" "no translation directory"
    return
  fi

  # ---- 1. Completeness. The check a green build will NOT give you. --------
  for f in "$dir"/[0-9]*.tex; do
    b=$(basename "$f")
    [ -f "$tdir/$b" ]  || bad "chapter missing"   "$tdir/$b"
    [ -f "$tsdir/$b" ] || bad "solutions missing" "$tsdir/$b"
  done
  for f in "$tdir"/[0-9]*.tex; do
    [ -e "$f" ] || continue
    b=$(basename "$f")
    [ -f "$dir/$b" ] || bad "extra chapter, no English twin" "$tdir/$b"
  done

  # ---- 2..4. Per-file structure, against the English original. ------------
  for f in "$dir"/[0-9]*.tex; do
    b=$(basename "$f")
    local t="$tdir/$b" ts="$tsdir/$b"
    [ -f "$t" ] || continue

    # 2. Labels: identical set, identical order. Never translated.
    if ! diff -q <(grep -o 'label{[^}]*}' "$f") \
                 <(grep -o 'label{[^}]*}' "$t") >/dev/null 2>&1; then
      bad "labels differ from English" "$b"
      diff <(grep -o 'label{[^}]*}' "$f") <(grep -o 'label{[^}]*}' "$t") \
        | head -6 | sed 's/^/          /'
    fi

    # 3. Exercise/problem <-> solution parity (the CLAUDE.md invariant).
    if [ -f "$ts" ]; then
      if ! diff -q \
          <(grep -o 'label{\(exo\|pb\):[^}]*}' "$t" | sed 's/label{//;s/}//') \
          <(grep -o 'begin{solution}{[^}]*}'   "$ts" | sed 's/begin{solution}{//;s/}//') \
          >/dev/null 2>&1; then
        bad "exercise/solution keys mismatch" "$b"
      fi
    fi

    # 4. Environment and figure census must equal English: nothing dropped,
    #    nothing invented, figures preserved.
    for env in definition theorem proposition lemma corollary example remark \
               method notation exercise problem proof tikzpicture omfigure; do
      ne=$(grep -c "begin{$env}" "$f")
      nt=$(grep -c "begin{$env}" "$t")
      [ "$ne" = "$nt" ] || bad "$env count ${ne}->${nt}" "$b"
      if [ -f "$ts" ]; then
        se=$(grep -c "begin{$env}" "$sdir/$b")
        st=$(grep -c "begin{$env}" "$ts")
        [ "$se" = "$st" ] || bad "$env count ${se}->${st} (solutions)" "$b"
      fi
    done
  done

  # ---- 5. Hygiene. -------------------------------------------------------
  if grep -rqn 'end{[a-z]*>' "$tdir" "$tsdir" 2>/dev/null; then
    bad "\\end{...> typo class" "$year/$lang"
  fi
  # "samples at={1,...,16}" is pgfplots syntax, not drafty prose.
  if grep -rn '\.\.\.' "$tdir" "$tsdir" 2>/dev/null \
       | grep -qv '\\dots\|\\ldots\|\\cdots\|\\foreach\|samples at'; then
    bad "drafty ... in prose (use \\dots)" "$year/$lang"
  fi
  dup=$(grep -rho 'label{[^}]*}' "$tdir" "$tsdir" 2>/dev/null | sort | uniq -d)
  [ -z "$dup" ] || bad "duplicate labels" "$(echo "$dup" | head -3 | tr '\n' ' ')"

  # ---- 6. Encoding: UTF-8, and no TeX accent escapes (\'e, \`a).
  #         Books 1/2 mixed the two and it cost their term configs a double
  #         spelling of every accented word. Do not repeat it here.
  if grep -rqn "\\\\['\`^\"]{\?[aeiouAEIOU]" "$tdir" "$tsdir" 2>/dev/null; then
    bad "TeX accent escapes (use UTF-8)" "$year/$lang"
  fi
}

if [ $# -eq 2 ]; then
  check_year_lang "$1" "$2"
else
  for year in bachelor-1 bachelor-2 bachelor-3; do
    for lang in fr nl; do
      check_year_lang "$year" "$lang"
    done
  done
fi

echo
if [ "$fail" -ne 0 ]; then
  echo "TRANSLATION GATE: FAILED"
  exit 1
fi
echo "TRANSLATION GATE: PASSED"
