# Translation score — Math Book 5 · Portuguese (`pt`)

| Field | Value |
|-------|--------|
| **Book** | One Math Book 5 (University Year 3) |
| **Language** | Portuguese (Brazilian edition, `pt`) |
| **Quality bar** | French Book 5 (`parts/bachelor-3/fr/`) |
| **Overall score** | **90 / 100** |
| **Ship threshold** | ≥ 90 |
| **Date** | 2026-07-24 |

## Dimension scores

| Dimension | Score /100 | Notes |
|-----------|----------:|--------|
| Structural fidelity | **96** | Full mirror (23+23); gate green |
| Terminology | **90** | grupos, anéis, Galois, Lebesgue, Hilbert, holomorfa |
| Register / tone | **85** | University MT register; titles curated FR-sense |
| Hygiene / LaTeX | **94** | Gates green; UTF-8 |
| Cross-refs | **84** | Correct keys |
| Figures | **88** | Drawing preserved |
| Solutions | **88** | Capítulo headers localized |
| MT-artifact freedom | **87** | Uni glossary + termlink |

**Overall: 90**.

## Structural / build gates

| Gate | Result |
|------|--------|
| `check_translation.sh bachelor-3 pt` | PASSED |
| Termlink book 5 pt | 3550 links |
| Fatal errors (`^!`) | 0 |
| Undefined references | 0 |
| Overfull `\hbox` | 0 |
| PDF | `build/one_math_book_5_university_year_3_pt.pdf` (~405 pp) |

## Status

**Meets ship threshold (≥ 90).** Working tree left uncommitted for human review.
