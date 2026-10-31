"""Copy finished high-res renders into identity/assets/render as full-resolution JPGs (no downscaling)."""
import glob, os
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, '..', 'assets', 'render')  # brand asset store, consumed by web/ via npm run sync
for f in sorted(glob.glob(os.path.join(HERE, 'hd', '*.png'))):
    out = os.path.join(D, os.path.basename(f)[:-4] + '.jpg')
    if os.path.exists(out) and os.path.getmtime(out) > os.path.getmtime(f): continue
    Image.open(f).convert('RGB').save(out, quality=92, optimize=True, progressive=True, subsampling=0)
    print('wrote', os.path.basename(out), Image.open(f).size)
