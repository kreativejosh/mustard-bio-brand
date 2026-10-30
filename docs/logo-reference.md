# Mustard Bio — Logo Reference

**Status:** Chosen 30 Oct 2026. Route 10 "Calibrated" from the 14-route exploration, with one change: the final o is the capsule from route 06.
**Colour:** monochrome until the identity system is defined. Ink `#1C1B19`, paper `#F2F0EA`.

## Idea
A measurement scale whose graduations trace an M. The bold centre graduation is the target value, the dose: medicine that is measured, not guessed. The wordmark ends in the product itself: the o is drawn as a capsule.

Tagline used in presentation: **Measured, not guessed.**

## Construction
Units: font size 200; IBM Plex Sans cap height = 139.6.

### Mark
- 11 graduations at pitch **p = 22**; tick width 6.
- Heights: 60, 128, 116, 104, 92, **80**, 92, 104, 116, 128, 60. Ticks 1–9 sit on two straight lines that meet at the centre, so the scale draws an M.
- Centre tick (index 5) is doubled in weight (width 12): the dose.

### Wordmark
- "Mustard Bi" set in **IBM Plex Sans Regular**, tracking −10/1000.
- **Capsule o:** an outlined ellipse, outer semi-axes **0.2802 cap × 0.5248 cap**, leaning **36.15° to the right**.
  - Stroke **17 units**, the same as IBM Plex Sans Regular's round stroke (≈0.122 cap), so it reads as part of the type.
  - Placed **0.143 cap** after the i; bottom sits **0.0226 cap** below the baseline (normal round overshoot); top reaches ≈0.91 cap.

### Lockup
- Mark height = **1.25 × cap height**, centred vertically on the cap band.
- Gap between mark and wordmark = **0.62 × cap height**.

## Files
| Path | What |
|---|---|
| `logo/svg/mustard-bio-logo-primary.svg` | Full lockup, ink |
| `logo/svg/mustard-bio-logo-black.svg` / `-white.svg` | One-colour versions |
| `logo/svg/mustard-bio-logo-icon.svg` | Calibrated mark alone |
| `logo/svg/mustard-bio-logo-wordmark.svg` | Wordmark alone (with capsule o) |
| `logo/construction/construction.svg` | Construction sheet (outlined text) |
| `logo/construction/construction-figma-editable.svg` | Construction sheet for Figma: live IBM Plex Mono text, grouped layers |
| `logo/construction/construction-8k.png` | Construction sheet, 7680×4320 |
| `logo/images/logo-primary-8k.png`, `logo-reverse-8k.png` | Logo on paper / on ink, 7680×4320 |
| `logo/images/presentation-board-8k.jpg` | Six-panel board, 7680×5120 |
| `logo/images/mockup-*.jpg` | Carton, laser-etched stainless, control screen (8K) |
| `source/build_logo.py` | Regenerates the SVGs from the geometry above |

## Known constraints
- Fine ticks need a minimum size: below ~24 px tall, consider a simplified icon (fewer ticks) — to be defined in the identity system.
- The capsule o is a drawn glyph, not a font character: always use the artwork, never type "o".
