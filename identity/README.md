# Mustard Bio — Brand identity v1.0

- `assets/` — the brand asset store: logo variants (SVG), 3D stills, motion loops (MP4), Blender renders, flat print artwork, fonts. The brand identity site in `../web/` serves these byte for byte.
- `blender/` — Blender (Cycles) scenes for merchandise, 3D brand assets, packaging, facility and the stationery overview; see `blender/README.md`.
- `assets/stationery/print/` — 17 print-ready stationery items: 300 dpi PNG at trim size + PDF with 3 mm bleed.
- `render/` — Three.js scene library (`scenes.js`, `mockups.js`), print artwork (`artwork.html`) and the headless render scripts used to produce every image and video.

All company copy comes from `../brief/brief.md`; contact details, product names and figures in mockups are placeholders.

Render pipeline: serve `render/` (with `lib/` = three@0.160.0 build + examples/jsm, `logo/`, `fonts/`, `final/`, `art/`) on :8123, then `node art.js`, `node drive.js jobs.json`, `bash encode.sh`.

## Workflow: improving an asset

1. Render or export into `identity/` (for example `python blender/merch.py ...` writes to `blender/hd/`, then `python blender/to_site.py` copies it to `assets/render/` at full resolution).
2. `cd ../web && npm run build` syncs `identity/assets` into the site and checks that every file is byte-identical to the source.
3. Commit `identity/assets` and push. The site never stores its own copy: `web/public/assets` is generated and git-ignored.
