"""Copy finished stationery from stat8k/ (stat8k.js + pdfprep.py) into the brand asset store.
print/<id>.pdf (RGB, 3 mm bleed) · print/<id>-cmyk.pdf (press) · print/<id>.png (8K, trim) · preview/<id>.jpg (2000 px grid preview)."""
import glob, os, shutil, sys
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'stat8k')
D = os.path.join(HERE, '..', 'assets', 'stationery')
for sub in ('print', 'preview'): os.makedirs(os.path.join(D, sub), exist_ok=True)
for f in sorted(glob.glob(os.path.join(SRC, '*.pdf')) + glob.glob(os.path.join(SRC, '*.png'))):
    shutil.copyfile(f, os.path.join(D, 'print', os.path.basename(f)))
for f in sorted(glob.glob(os.path.join(SRC, '*.png'))):
    im = Image.open(f).convert('RGB'); s = 2000 / max(im.size)
    im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS).save(
        os.path.join(D, 'preview', os.path.basename(f)[:-4] + '.jpg'), quality=92, optimize=True, progressive=True, subsampling=0)
    print('published', os.path.basename(f)[:-4])
