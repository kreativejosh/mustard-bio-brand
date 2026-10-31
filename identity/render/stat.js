const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();
const ctx=await b.newContext({viewport:{width:1800,height:1400},deviceScaleFactor:300/96});const p=await ctx.newPage();
p.on('console',m=>m.type()=='error'&&console.log('C',m.text()));
await p.goto('http://localhost:8123/stationery.html',{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(500);
const items=await p.$$eval('.ab',a=>a.map(e=>({id:e.id,trim:e.dataset.trim,w:e.style.width,h:e.style.height})));
for(const it of items){await (await p.$('#'+it.id+' .trim')).screenshot({path:`stat/${it.id}.png`});}
console.log('png',items.length);
// PDFs at bleed size, one per item
const q=await (await b.newContext()).newPage();
await q.goto('http://localhost:8123/stationery.html',{waitUntil:'networkidle'});await q.evaluate(()=>document.fonts.ready);
const html=await q.content();
for(const it of items){ if(it.trim.startsWith('px')) continue;
  await q.setContent(html.replace('<head>','<head><base href="http://localhost:8123/">'),{waitUntil:'networkidle'});
  await q.evaluate(id=>{document.body.classList.add('solo');document.querySelectorAll('.ab').forEach(e=>{if(e.id!==id)e.remove()})},it.id);
  await q.evaluate(()=>document.fonts.ready);
  await q.pdf({path:`stat/${it.id}.pdf`,width:it.w,height:it.h,printBackground:true,pageRanges:'1'});}
console.log(items.map(i=>i.id+' '+i.trim).join('\n'));await b.close();})();
