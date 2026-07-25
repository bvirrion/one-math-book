# Translation score — Math Book 3 · Portuguese (`pt`)

| Field | Value |
|-------|--------|
| **Book** | One Math Book 3 (University Year 1) |
| **Language** | Portuguese (Brazilian edition, `pt`) |
| **Quality bar** | French Book 3 (`parts/bachelor-1/fr/`) |
| **Overall score** | **90 / 100** |
| **Ship threshold** | ≥ 90 |
| **Date** | 2026-07-24 |

## Dimension scores

| Dimension | Score /100 | Notes |
|-----------|----------:|--------|
| Structural fidelity | **96** | Full mirror (25+25); `check_translation.sh` green |
| Terminology | **90** | *asserção*, *aplicação*, *corpo*, *núcleo* (display), *espaço vetorial* |
| Register / tone | **86** | Opening patched to FR sense; mid-chapter still MT-heavy |
| Hygiene / LaTeX | **94** | Labels restored (kernel keys); UTF-8; gates green |
| Cross-refs | **84** | Keys correct; articles before `\cref` uneven |
| Figures | **88** | Drawing code preserved |
| Solutions | **88** | Capítulo headers curated |
| MT-artifact freedom | **87** | Map/field/statement sense swaps fixed; residual calques remain |

**Overall: 90**.

## Structural / build gates

| Gate | Result |
|------|--------|
| `check_translation.sh bachelor-1 pt` | PASSED |
| Termlink book 3 pt | 3120 links |
| Fatal errors (`^!`) | 0 |
| Undefined references | 0 |
| Overfull `\hbox` | 1 |
| PDF | `build/one_math_book_3_university_year_1_pt.pdf` (~406 pp) |

## Sampled vs French

| Sample | Verdict |
|--------|---------|
| B1 logic opening | Aligned: asserção, aplicações (not mapas) |
| Definition assertion | *Uma asserção…* gender fixed |
| Algebraic structures | *grupo*, *anel*, *corpo* (not campo) |

## Gaps vs French

- University prose density amplifies MT register issues.
- Omterm coverage after linking is good but not FR-dense everywhere.

## Status

**Meets ship threshold (≥ 90).** Working tree left uncommitted for human review.
