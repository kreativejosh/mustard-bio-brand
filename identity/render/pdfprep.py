"""Finish stationery print PDFs from stat8k.js: set TrimBox/BleedBox (3 mm bleed) and write a CMYK copy.
Usage: python3 pdfprep.py stat8k  ->  stat8k/<id>.pdf (RGB, digital/print) and stat8k/<id>-cmyk.pdf (press)."""
import sys, os, glob, subprocess, pikepdf
MM = 72 / 25.4
d = sys.argv[1]
for f in sorted(glob.glob(os.path.join(d, '*.pdf'))):
    if f.endswith('-cmyk.pdf'): continue
    with pikepdf.open(f, allow_overwriting_input=True) as pdf:
        for pg in pdf.pages:
            x0, y0, x1, y1 = [float(v) for v in pg.MediaBox]
            b = 3 * MM
            pg.BleedBox = pikepdf.Array([x0, y0, x1, y1])
            pg.TrimBox = pikepdf.Array([x0 + b, y0 + b, x1 - b, y1 - b])
        pdf.docinfo['/Title'] = 'Mustard Bio · ' + os.path.basename(f)[:-4].replace('-', ' ')
        pdf.docinfo['/Author'] = 'Mustard Bio'
        pdf.save(f)
    out = f[:-4] + '-cmyk.pdf'
    subprocess.run(['gs', '-q', '-dNOPAUSE', '-dBATCH', '-dSAFER', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.6',
                    '-sColorConversionStrategy=CMYK', '-sProcessColorModel=DeviceCMYK', '-dPDFSETTINGS=/prepress',
                    '-dPreserveTrimBox=true', '-dDownsampleColorImages=false', '-dDownsampleGrayImages=false',
                    '-dAutoFilterColorImages=true',  # prepress: photos at maximum JPEG quality, flat art lossless
                   
                    '-o', out, f], check=True)
    print('ok', os.path.basename(f), os.path.basename(out))
