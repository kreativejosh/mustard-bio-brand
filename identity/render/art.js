const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const p=await (await b.newContext({viewport:{width:3200,height:2000},deviceScaleFactor:3})).newPage();
p.on('console',m=>m.type()=='error'&&console.log('C',m.text()));
await p.goto('http://localhost:8123/artwork.html',{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(800);
const ids=await p.$$eval('.ab',a=>a.map(e=>e.id));
for(const id of ids){await (await p.$('#'+id)).screenshot({path:`art/${id}.png`});}
console.log(ids.join(' '));
console.log(await p.evaluate(()=>[...document.fonts].filter(f=>f.status=='loaded').map(f=>f.family+f.weight).join(',')));
await b.close();})();
