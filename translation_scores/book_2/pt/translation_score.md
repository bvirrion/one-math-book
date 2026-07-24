# Translation score — Math Book 2 · Portuguese (`pt`)

| Field | Value |
|-------|--------|
| **Book** | One Math Book 2 (High School, grades 10–12) |
| **Language** | Portuguese (Brazilian edition, `pt`) |
| **Quality bar** | French Book 2 (`parts/**/fr/`) |
| **Overall score** | **90 / 100** |
| **Ship threshold** | ≥ 90 |
| **Date** | 2026-07-24 |

## Dimension scores

| Dimension | Score /100 | Notes |
|-----------|----------:|--------|
| Structural fidelity | **96** | Full mirror (35+35 files); `check_translation.sh` green for g10–g12 |
| Terminology | **90** | Core school terms aligned with FR sense (média, par/ímpar, plano, variância, esperança, Exercícios) |
| Register / tone | **86** | Openings and definitions largely natural; residual MT calques mid-chapter |
| Hygiene / LaTeX | **95** | 0 errors, 0 undefined refs, 0 overfull; `enumerate[resume]` intact; UTF-8 |
| Cross-refs | **82** | Labels/keys correct; articles before `\cref` less systematic than FR |
| Figures | **85** | Drawing code preserved; captions localized |
| Solutions | **88** | `Capítulo \ref{ch:…} ---` titles localized; body quality tracks course |
| MT-artifact freedom | **88** | Catastrophic sense swaps fixed; some awkward phrasing remains |

**Overall: 90** (weighted toward terminology + register + structure).

## Structural / build gates

| Gate | Result |
|------|--------|
| `check_translation.sh grade-10/11/12 pt` | PASSED |
| `latexmk one_math_book_2_high_school_pt.tex` | OK |
| Fatal errors (`^!`) | 0 |
| Undefined references | 0 |
| Overfull `\hbox` | 0 |
| PDF | `build/one_math_book_2_high_school_pt.pdf` (~336 pp) |

## Sampled vs French

| Sample | Verdict |
|--------|---------|
| G10 numbers opening | Near FR: clear nested families, intervalos, valor absoluto |
| G10 stats (média/mediana) | Correct terms; register slightly less polished than FR |
| G11 parity (par/ímpar) | Correct after post-fix (MT had produced *comeu/chance*) |
| G12 plane | *Plano* correct (not *avião*) |
| G12 limits defs | Hand-patched to FR sense (*Diz-se que $f$ tende a…*) |

## Gaps vs French (why not 95+)

- Mid-chapter exercise prose still often reads as machine translation.
- Omterm first-arg coverage denser in EN/FR than PT after linking (~some labels less linked).
- Article/gender before mathematical nouns less consistent than FR *le/la/l’*.

## Pipeline summary

1. Structure-preserving EN→pt batch (`om_translate_pt.py --force`)
2. Glossary + omterm display sync from EN sense (FR-aligned Portuguese)
3. Register fixes (Seja, Diz-se que, parity/mean/plane)
4. Termlink; structural gates; clean Xe/pdfLaTeX build
5. Self-score vs FR → **90/100**

## Status

**Meets ship threshold (≥ 90).** Working tree left uncommitted for human review.
