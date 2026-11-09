# Mustard Bio brand repo — notes for Claude

- Read `brief/brief.md` and `docs/logo-reference.md` first.
- The logo is fixed. Do not redraw or re-space it; use the SVGs in `logo/svg/` or regenerate with `source/build_logo.py`. The capsule o is artwork, not a typed character.
- Colour is defined in `design-system/tokens.css` (charcoal #222F30, off-white #F7F7F5, lime #A7E26E dose, mint #CEF79E). Logo stays geometry-identical; only its fill changes (lime dose on dark grounds only).
- Brand identity site: Next.js app in `web/` (sections in `web/components/sections/`, data in `web/lib/brand.ts`). It serves brand assets from `identity/assets/`, synced byte for byte by `npm run sync` (runs before `dev`/`build`; `postbuild` verifies checksums). Never edit `web/public/assets` or `web/lib/generated` (generated, git-ignored), and keep `images.unoptimized` so renders are never recompressed.
- Asset pipeline: Blender scenes in `identity/blender/` (render to `hd/`, then `to_site.py` copies to `identity/assets/render/`), print artwork and decals in `identity/render/` (Playwright exports), Three.js scene library at `identity/render/scenes.js`.
- Stationery is exported at 8K (long edge 7680 px) with vector PDFs (RGB + CMYK, 3 mm bleed): see "Stationery at 8K" in `identity/blender/README.md`. Secondary text on light paper must stay ≥ 4.5:1 (use `--t2`/`--t3`/`--mute` in `stationery.html`, never sage on light grounds).
- Marketing website: Next.js app in `site/` (Home, Manufacturing, Technology, About with Vision). Copy is verbatim from `brief/website-copy.md` via `site/lib/copy.ts`; never reword or add claims. Assets synced from `identity/assets` like `web/`.
- Never describe Mustard Bio beyond `brief/brief.md` and `brief/website-copy.md`. Older logo-phase mockups in `logo/images/` contain an invented location and product name; do not reuse them.
- Typeface already in use: IBM Plex Sans (wordmark), IBM Plex Mono (labels/technical). Both SIL OFL, files in `source/fonts/`.
- Audience and context: pharmaceutical manufacturing (GMP facilities, regulators, pharma brand partners) plus manufacturing software. The identity must work on cartons and labels at small sizes, etched/printed on stainless equipment, and in software UIs.
- Next phase: brand identity and design system. Suggested home: `identity/` for guidelines, `design-system/` for tokens and components.
