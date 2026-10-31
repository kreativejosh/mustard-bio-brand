// usage: node drive.js jobs.json   jobs: [{s,v,w,h,t,exp,out,lib, frames?:{n,fps,start}}]
const { chromium } = require('playwright'); const fs=require('fs'); const path=require('path');
(async()=>{const jobs=JSON.parse(fs.readFileSync(process.argv[2]));
const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
for(const j of jobs){const p=await b.newPage({viewport:{width:j.w||1600,height:j.h||1200}});p.on('pageerror',e=>console.log('E',j.s,e.message));
 const qs=new URLSearchParams(Object.entries(j).filter(([k])=>!['out','frames'].includes(k))).toString();
 const t0=Date.now(); try{await p.goto('http://localhost:8123/render.html?'+qs); await p.waitForFunction(()=>window.__ready,{timeout:120000});}catch(e){console.log('FAIL',j.out);await p.close();continue;}
 if(j.frames){fs.mkdirSync(j.out,{recursive:true});const {n,fps,start=0}=j.frames;for(let i=0;i<n;i++){const d=await p.evaluate(t=>window.__frame(t),start+i/fps);fs.writeFileSync(path.join(j.out,`f${String(i).padStart(4,'0')}.png`),Buffer.from(d.split(',')[1],'base64'));}}
 else{const d=await p.evaluate(t=>window.__frame(t),+(j.t??1.2));fs.writeFileSync(j.out,Buffer.from(d.split(',')[1],'base64'));}
 console.log('ok',j.out,((Date.now()-t0)/1000).toFixed(1)+'s');await p.close();}
await b.close();})();
