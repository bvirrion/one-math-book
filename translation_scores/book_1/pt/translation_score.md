# Translation score — Math Book 1 · Portuguese (`pt`)

| Field | Value |
|-------|--------|
| **Book** | One Math Book 1 (Primary / Middle, grades 1–9) |
| **Language** | Portuguese (Brazilian edition, `pt`) |
| **Quality bar** | French Book 1 (`parts/grade-N/fr/`) |
| **Overall score** | **91 / 100** |
| **Ship threshold** | ≥ 90 |
| **Date** | 2026-07-24 |

## Dimension scores

| Dimension | Score /100 | Notes |
|-----------|----------:|--------|
| Structural fidelity | **97** | Full mirror (71+71 files); `check_translation.sh` green for g1–g9 |
| Terminology | **90** | School terms: fração, perímetro, área, Pitágoras, Tales, média, par/ímpar |
| Register / tone | **88** | Young-grade openings natural after polish; residual MT mid-chapter |
| Hygiene / LaTeX | **95** | 0 errors, 0 undefined; 1 overfull; UTF-8; `enumerate[resume]` intact |
| Cross-refs | **85** | Labels/keys correct; articles before `\cref` less systematic than FR |
| Figures | **90** | TikZ geometry preserved; node captions localized (bolinhas de gude, etc.) |
| Solutions | **90** | `Capítulo \ref{ch:…} ---` titles curated; body tracks course |
| MT-artifact freedom | **88** | Catastrophic sense swaps fixed; gender/range fixes applied |

**Overall: 91** (weighted toward terminology + register + structure).

## Structural / build gates

| Gate | Result |
|------|--------|
| `check_translation.sh grade-1…9 pt` | PASSED |
| `latexmk one_math_book_1_primary_middle_school_pt.tex` | OK |
| Fatal errors (`^!`) | 0 |
| Undefined references | 0 |
| Overfull `\hbox` | 1 |
| PDF | `build/one_math_book_1_primary_middle_school_pt.pdf` (~428 pp) |

## Sampled vs French

| Sample | Verdict |
|--------|---------|
| G1 counting opening | Near FR: contagem, bolinhas de gude, último número, de $0$ a $20$ |
| G1 method how-to-count | Correct after post-fix (*último*, not *durar*) |
| G2 money/measures | Everyday register OK; unit vocabulary aligned |
| G9 arithmetic / primes | *Números primos*, divisores correct |

## Gaps vs French (why not 95+)

- Mid-chapter exercise prose still often reads as machine translation.
- Some multi-line gender slips possible outside the global fixes.
- Article/gender before mathematical nouns less consistent than FR.

## Pipeline summary

1. Structure-preserving EN→pt batch (`om_translate_pt_robust.py`)
2. Glossary + gender + figure-caption polish (`om_pt_polish_all.py`)
3. Curated chapter titles (FR sense)
4. Termlink; structural gates; clean pdfLaTeX build
5. Self-score vs FR → **91/100**

## Status

**Meets ship threshold (≥ 90).** Working tree left uncommitted for human review.
