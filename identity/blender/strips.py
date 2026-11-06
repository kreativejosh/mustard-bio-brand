"""Render a scene in horizontal strips (each saved on its own, so long 8K renders survive interruptions), then stitch.
Usage: python3 strips.py <script.py> <scene> <out.png> <w> <h> <spp> <n strips> [strip index | stitch]"""
import os, sys, subprocess
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
script, scene, out, w, h, spp, n, which = sys.argv[1:9]
w, h, n = int(w), int(h), int(n)
part = lambda i: f'{out[:-4]}.part{i}.png'
if which == 'stitch':
    im = Image.new('RGB', (w, h))
    for i in range(n):  # strip 0 is the bottom of the frame (Blender border y runs bottom-up)
        p = Image.open(part(i)).convert('RGB'); im.paste(p, (0, h - (i + 1) * h // n))
    im.save(out); [os.remove(part(i)) for i in range(n)]; print('stitched', out)
else:
    i = int(which)
    if os.path.exists(part(i)): print('exists', part(i)); sys.exit()
    env = dict(os.environ, STAT_BORDER=f'0,1,{i / n},{(i + 1) / n}')
    subprocess.run(['python3', script, scene, part(i) + '.tmp.png', str(w), str(h), spp], env=env, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.replace(part(i) + '.tmp.png', part(i)); print('ok', part(i), Image.open(part(i)).size)
