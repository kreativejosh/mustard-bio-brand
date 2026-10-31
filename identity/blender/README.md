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
