"""Copy finished renders into identity/assets/render as JPGs (consumed by web/ via npm run sync).
hd/*.png   -> render/<name>.jpg at full resolution (no downscaling)
hd8/stat-*.png (8K stationery mockups) -> render/8k/<name>.jpg at full 7680 px, plus render/<name>.jpg at 2400 px for the page."""
import glob, os
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, '..', 'assets', 'render')
J = dict(quality=92, optimize=True, progressive=True, subsampling=0)
def fresh(out, src): return os.path.exists(out) and os.path.getmtime(out) > os.path.getmtime(src)
for f in sorted(glob.glob(os.path.join(HERE, 'hd', '*.png'))):
    out = os.path.join(D, os.path.basename(f)[:-4] + '.jpg')
    if fresh(out, f) or os.path.exists(os.path.join(HERE, 'hd8', os.path.basename(f))): continue
    Image.open(f).convert('RGB').save(out, **J); print('wrote', os.path.basename(out))
os.makedirs(os.path.join(D, '8k'), exist_ok=True)
for f in sorted(glob.glob(os.path.join(HERE, 'hd8', 'stat-*.png'))):
    n = os.path.basename(f)[:-4]; big = os.path.join(D, '8k', n + '.jpg')
    if fresh(big, f): continue
    im = Image.open(f).convert('RGB'); im.save(big, **J)
    s = 2400 / im.width; im.resize((2400, round(im.height * s)), Image.LANCZOS).save(os.path.join(D, n + '.jpg'), **J)
    print('wrote 8k', n, im.size)
