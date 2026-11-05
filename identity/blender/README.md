# Blender (Cycles) renders

Path-traced renders for merchandise, 3D brand assets, packaging, facility and the stationery overview.

```
pip install bpy                       # Blender 5.2 as a Python module
python fetch_polyhaven.py             # CC0 HDRIs, fabric/concrete scans, run inside a folder named ph/
python merch.py tees out.png 1600 1200 160
python assets.py capsule-dark out.png 1600 1200 192
python facility.py corridor out.png 1600 1200 160
```

Scenes: tee3d.py (ghost-mannequin tee, cloth sim; front/back × stone/ink) · tote3d.py (standing tote, window light) · lanyard3d.py (woven lanyard, buckle, slotted cards) · merch.py (bottles, mugs, engraved wristbands) · assets.py (capsule-dark/light, mark-dark/light, flask, tubes, helix, blob, tablets, pack, stationery) · facility.py (facade, corridor).

Inputs: print artwork and decals from `../render/` (`art/`, `decal/`, `stat/`), produced by `artwork.html`, `decals.html`, `stationery.html` via the Playwright scripts there.
Lighting: Poly Haven `studio_small_09` / `kloofendal_48d_partly_cloudy_puresky` plus area lights. View transform: Khronos PBR Neutral (keeps brand colours accurate).

## Stationery at 8K

1. Serve `../render` on :8123, then in `../render`: `node stat8k.js && python3 pdfprep.py stat8k` (8K PNGs, vector PDFs with TrimBox/BleedBox, CMYK copies).
2. `./run_stat8k.sh` renders the seven stationery mockups at 7680 × 5760 using the 8K artwork as textures (also re-renders the report-cover capsule at 4800 px).
3. `python3 to_site.py` publishes `hd8/stat-*.png` to `assets/render/8k/` (full size) and `assets/render/` (2400 px); `python3 ../render/stat_publish.py` publishes the flat files to `assets/stationery/`.
4. `python3 ../render/drive_pack.py <dir>` builds the Google Drive folder (RGB + CMYK PDFs, 8K PNGs, 8K mockups, combined PDF, print spec).
