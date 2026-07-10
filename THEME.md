# One Course — shared theme

This book is part of the **One Course** product family (one-course.com). The
title page carries the shared brand; this file documents it so the website,
apps, videos and future books stay consistent. The LaTeX implementation lives
in `styles/onemath.sty` (colors and the `\ocRosette`/`\ocQuadLine` macros) and
`frontmatter/titlepage.tex` (the cover layout, chosen from mockup 81).

## Palette

The brand is built on four bright colors (the "quad") used together, plus ink
and tints for light grounds.

| role | name | hex |
|---|---|---|
| quad — mint | `ocMint` | `#06D6A0` |
| quad — yellow | `ocYellow` | `#FFD166` |
| quad — red | `ocRed` | `#EF476F` |
| quad — blue | `ocBlue` | `#118AB2` |
| text ink | `ocInk` | `#1F2430` |
| titles / accents | `ocDarkBlue` | `ocBlue` darkened 20% toward black (≈ `#0E6E8E`) |
| pale ground | `ocPaleBlue` | `ocBlue` at 14% over white (≈ `#DEEDF3`) |

Rules of thumb:

- Grounds are light: white or `ocPaleBlue`. Dark backgrounds are off-brand.
- The four quad colors appear **together**, in the fixed order
  mint → yellow → red → blue, never as isolated single accents.
- Body text is `ocInk` on light grounds; big titles are `ocDarkBlue`.

## The rosette logo

A circle of four quadrant wedges — mint on top, yellow on the left, red at
the bottom, blue on the right — separated by white diagonal cuts, around a
white core circle (58% of the radius) holding a bold serif **1** in
`ocDarkBlue`. The diagonal cut width scales with the radius (≈ 1.4 pt per cm
of radius in print).

- LaTeX: `\ocRosette{x}{y}{R}{pt}` (center, radius in cm, size of the "1").
- Keep it on white or a pale ground so the white cuts and core read.
- Minimum size: the "1" must stay comfortably legible (favicon-size versions
  can drop the "1" and keep only the four wedges).

## The wordmark

`ONE-COURSE.COM` (on book covers, where it doubles as the pointer to the
site) or `ONE-COURSE` (inside apps and videos where the context is already
the product), set in bold sans-serif capitals, heavily letterspaced
(LaTeX: `\textls[210]{...}` with `lmodern` sans), in `ocInk`.

## The quad line

A slim horizontal bar split into four equal segments, one per quad color, in
brand order. Used as a page-width rule under bands and as a short centered
separator. LaTeX: `\ocQuadLine{x0}{x1}{y}{h}`.

## Cover layout (chosen design, mockup 81)

White A4 page, coordinates in cm from the bottom-left corner:

- pale blue-gray (`ocPaleBlue`) header band from y = 24.6 to the top edge,
  with a page-width quad line (h = 0.24) directly under it;
- rosette (R = 2.4) centered horizontally, astride the band's lower edge;
- wordmark centered at y = 20.6;
- title block: 40 pt bold `ocDarkBlue` title (y = 16.4), italic subtitle,
  one-line scope text; short centered quad line under it (x 6.6–14.4);
- credits block near y = 6, then version and date;
- full-width quad bottom band (h = 1.0).

Future books in the family keep this layout and swap the title block; the
header band tint may eventually vary by subject, keeping everything else.

## Typography

- Titles and body in the book's serif (Latin Modern).
- Brand elements (wordmark) in bold sans (Latin Modern Sans), letterspaced.
- On the web, close equivalents work: any humanist serif for text, a
  geometric/neutral sans (letterspaced, bold, uppercase) for the wordmark.
