// Export every stationery item from stationery.html:
//   stat8k/<id>.png  trim size, long edge 7680 px (8K), for screens and Blender textures
//   stat8k/<id>.pdf  vector print master at bleed size (3 mm each side), fonts embedded
// Serve this folder on :8123 first (python3 -m http.server 8123). Then run pdfprep.py for TrimBox/BleedBox + CMYK.
const { chromium } = require('playwright'); const fs = require('fs');
const URL = 'http://localhost:8123/stationery.html', OUT = 'stat8k', LONG = 7680;
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const b = await chromium.launch();
  const probe = await b.newPage(); await probe.goto(URL, { waitUntil: 'networkidle' }); await probe.evaluate(() => document.fonts.ready);
  const items = await probe.$$eval('.ab', (a) => a.map((e) => { const r = e.querySelector('.trim').getBoundingClientRect(); return { id: e.id, trim: e.dataset.trim, w: e.style.width, h: e.style.height, tw: r.width, th: r.height }; }));
  const html = await probe.content(); await probe.close();
  for (const it of items) {
    const dsf = LONG / Math.max(it.tw, it.th);
    const ctx = await b.newContext({ viewport: { width: 1800, height: 1400 }, deviceScaleFactor: dsf });
    const p = await ctx.newPage(); p.on('console', (m) => m.type() == 'error' && console.log('C', m.text()));
    await p.goto(URL, { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
    await p.evaluate((id) => { document.body.classList.add('solo'); document.querySelectorAll('.ab').forEach((e) => { if (e.id !== id) e.remove(); }); }, it.id);
    await p.waitForTimeout(300);
    await (await p.$('#' + it.id + ' .trim')).screenshot({ path: `${OUT}/${it.id}.png` });
    if (!it.trim.startsWith('px')) {
      await p.emulateMedia({ media: 'print' });
      await p.pdf({ path: `${OUT}/${it.id}.pdf`, width: it.w, height: it.h, printBackground: true, pageRanges: '1' });
    }
    console.log(it.id, it.trim, dsf.toFixed(2)); await ctx.close();
  }
  fs.writeFileSync(`${OUT}/items.json`, JSON.stringify(items, null, 1));
  await b.close();
})();
