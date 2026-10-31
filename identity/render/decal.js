const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const p=await (await b.newContext({viewport:{width:4400,height:2400},deviceScaleFactor:2})).newPage();
await p.goto('http://localhost:8123/decals.html',{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(400);
const ids=await p.$$eval('.d',a=>a.map(e=>e.id));
for(const id of ids) await (await p.$('#'+id)).screenshot({path:`decal/${id}.png`,omitBackground:true});
console.log(ids.join(' '));await b.close();})();
