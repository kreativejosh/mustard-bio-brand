"""Build the Google Drive hand-off folder for stationery from the brand asset store.
Usage: python3 drive_pack.py <out dir>   (reads ../assets/stationery/print and ../assets/render/8k)
Writes:  Mustard Bio Stationery/
           Mustard Bio Stationery - all items.pdf      every item, one per page (RGB)
           Print spec.pdf                              sizes, bleed, colours, which file to use
           01 Print PDF (RGB)/   02 Press PDF (CMYK)/   03 PNG 8K/   04 Mockups 8K/"""
import os, sys, shutil, subprocess, html, pikepdf
HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HERE, '..', 'assets')
ITEMS = [  # id, name, finished size
    ('business-card-front', 'Business card front', '85 x 55 mm'), ('business-card-back', 'Business card back', '85 x 55 mm'),
    ('letterhead', 'Letterhead', 'A4 210 x 297 mm'), ('continuation-sheet', 'Continuation sheet', 'A4 210 x 297 mm'),
    ('compliments-slip', 'Compliments slip', '210 x 99 mm'), ('envelope-dl', 'DL envelope', '220 x 110 mm'),
    ('envelope-c4', 'C4 envelope', '324 x 229 mm'), ('presentation-folder', 'Presentation folder outer spread', '440 x 310 mm'),
    ('report-cover', 'Report cover', 'A4 210 x 297 mm'), ('document-template', 'Document template', 'A4 210 x 297 mm'),
    ('invoice', 'Invoice', 'A4 210 x 297 mm'), ('notepad', 'Notepad', 'A5 148 x 210 mm'), ('notebook-cover', 'Notebook cover', 'A5 148 x 210 mm'),
    ('staff-id-front', 'Staff ID front', 'CR80 54 x 86 mm'), ('staff-id-back', 'Staff ID back', 'CR80 54 x 86 mm'),
    ('visitor-pass', 'Visitor pass', 'CR80 54 x 86 mm'), ('sticker-sheet', 'Sticker sheet', 'A6 105 x 148 mm'),
]
MOCKS = [('stat-cards', 'Business cards'), ('stat-letter', 'Letterhead and continuation sheet'), ('stat-finance', 'Invoice and document template'),
         ('stat-report', 'Report cover, notebook and notepad'), ('stat-post', 'Compliments slip and envelopes'),
         ('stat-id', 'ID cards and sticker sheet'), ('stat-folder', 'Presentation folder')]

out = os.path.join(sys.argv[1], 'Mustard Bio Stationery'); shutil.rmtree(out, ignore_errors=True)
d = {k: os.path.join(out, k) for k in ('01 Print PDF (RGB)', '02 Press PDF (CMYK)', '03 PNG 8K', '04 Mockups 8K')}
for p in d.values(): os.makedirs(p)
P = os.path.join(A, 'stationery', 'print')
for i, (sid, name, size) in enumerate(ITEMS, 1):
    base = f'{i:02d} Mustard Bio - {name} - {size}'
    shutil.copyfile(os.path.join(P, sid + '.pdf'), os.path.join(d['01 Print PDF (RGB)'], base + '.pdf'))
    shutil.copyfile(os.path.join(P, sid + '-cmyk.pdf'), os.path.join(d['02 Press PDF (CMYK)'], base + ' - CMYK.pdf'))
    shutil.copyfile(os.path.join(P, sid + '.png'), os.path.join(d['03 PNG 8K'], base + '.png'))
shutil.copyfile(os.path.join(P, 'email-signature.png'), os.path.join(d['03 PNG 8K'], '18 Mustard Bio - Email signature.png'))
for i, (mid, name) in enumerate(MOCKS, 1):
    shutil.copyfile(os.path.join(A, 'render', '8k', mid + '.jpg'), os.path.join(d['04 Mockups 8K'], f'{i:02d} Mustard Bio - {name} - mockup 8K.jpg'))

# all items in one PDF
allpdf = pikepdf.new()
for sid, _, _ in ITEMS:
    with pikepdf.open(os.path.join(P, sid + '.pdf')) as src: allpdf.pages.extend(src.pages)
allpdf.docinfo['/Title'] = 'Mustard Bio stationery'; allpdf.save(os.path.join(out, 'Mustard Bio Stationery - all items.pdf'))

# print spec sheet (HTML -> PDF with the brand fonts)
fonts = os.path.abspath(os.path.join(HERE, '..', '..', 'source', 'fonts'))
rows = ''.join(f'<tr><td>{i:02d}</td><td>{html.escape(n)}</td><td>{html.escape(s)}</td></tr>' for i, (_, n, s) in enumerate(ITEMS, 1))
ff = ''.join(f'@font-face{{font-family:"P{f}";font-weight:{w};src:url("file://{fonts}/ibm-plex-{f}-latin-{w}-normal.woff")}}' for f in ('sans', 'mono') for w in (400, 500))
doc = f'''<!doctype html><meta charset="utf-8"><style>{ff}
@page{{size:A4;margin:18mm 20mm}}body{{font:400 10pt/1.5 "Psans";color:#222F30;-webkit-print-color-adjust:exact}}
h1{{font-weight:400;font-size:24pt;letter-spacing:-.02em;margin:0 0 2mm}}h2{{font:500 8pt "Pmono";letter-spacing:.06em;text-transform:uppercase;margin:9mm 0 2.5mm;color:#33494A}}
.k{{font:500 8pt "Pmono";letter-spacing:.06em;text-transform:uppercase;color:#33494A}}table{{border-collapse:collapse;width:100%}}
td,th{{text-align:left;padding:1.6mm 2mm 1.6mm 0;border-bottom:.25pt solid #C9CBBE;vertical-align:top}}th{{font:500 7.5pt "Pmono";letter-spacing:.06em;text-transform:uppercase;color:#33494A;border-bottom:.6pt solid #222F30}}
.sw{{display:inline-block;width:3.2mm;height:3.2mm;border-radius:.6mm;vertical-align:-.5mm;margin-right:2mm;border:.25pt solid #C9CBBE}}
.bar{{height:2mm;background:#A7E26E;width:24mm;margin:0 0 6mm}}</style>
<div class="bar"></div><h1>Stationery print spec</h1><div class="k">Mustard Bio · stationery set · 17 items + email signature</div>
<h2>Which file to use</h2><table><tr><th>Folder</th><th>Use for</th></tr>
<tr><td>01 Print PDF (RGB)</td><td>Office and digital printing, sharing on screen. Vector artwork, fonts embedded, 3 mm bleed with TrimBox and BleedBox set.</td></tr>
<tr><td>02 Press PDF (CMYK)</td><td>Commercial offset or digital press. Same artwork converted to CMYK; ask the printer for a hard proof, as lime #A7E26E and mint #CEF79E sit at the edge of the CMYK gamut.</td></tr>
<tr><td>03 PNG 8K</td><td>Screens, slides and web. Finished (trim) size, long edge 7680 px.</td></tr>
<tr><td>04 Mockups 8K</td><td>Presentations and showcases. Path-traced paper mockups, 7680 x 5760 px.</td></tr>
<tr><td>All items PDF</td><td>Review the whole set in one file (RGB, one item per page).</td></tr></table>
<h2>Items</h2><table><tr><th>No.</th><th>Item</th><th>Finished size</th></tr>{rows}<tr><td>18</td><td>Email signature</td><td>600 x 150 px (PNG only)</td></tr></table>
<h2>Print rules</h2><table>
<tr><td>Bleed</td><td>3 mm on every side, included in every PDF. Trim to the TrimBox.</td></tr>
<tr><td>Safe area</td><td>Keep text 5 mm inside the trim.</td></tr>
<tr><td>Type</td><td>IBM Plex Sans and IBM Plex Mono (SIL Open Font License), embedded.</td></tr>
<tr><td>Colour</td><td><span class="sw" style="background:#222F30"></span>Charcoal #222F30 &nbsp; <span class="sw" style="background:#F7F7F5"></span>Off-white #F7F7F5 &nbsp; <span class="sw" style="background:#A7E26E"></span>Lime #A7E26E &nbsp; <span class="sw" style="background:#CEF79E"></span>Mint #CEF79E</td></tr>
<tr><td>Placeholders</td><td>Names, addresses, numbers and amounts are placeholders; replace before printing.</td></tr></table>'''
tmp = os.path.join(out, '.spec.html'); open(tmp, 'w').write(doc)
js = f"const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://{tmp}');await p.evaluate(()=>document.fonts.ready);await p.pdf({{path:{os.path.join(out, 'Print spec.pdf')!r},preferCSSPageSize:true,printBackground:true}});await b.close();}})();"
subprocess.run(['node', '-e', js], check=True, cwd=HERE); os.remove(tmp)
print('built', out)
