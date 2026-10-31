import { Sparkline } from '@/components/brand-static';

export default function SectionFacility() {
  return (
    <section className="sec" id="facility" data-name="Facility">
  <div className="head">
    <div className="t"><span className="tag">14 Facility</span></div>
    <div className="t">
      <h2 className="d-2">Technology-enabled factories, <span className="mute">signed like instruments.</span></h2>
      <p className="lead">Outside, a charcoal ribbed band carries the reverse logo. Inside, white walls, sage floors and lime guide lines. Equipment carries the mark etched into steel; software carries it in the UI. Zone names below are examples.</p>
    </div>
  </div>
  <figure className="fig"><img src="/assets/render/facility-facade.jpg" alt="Factory exterior with illuminated sign" loading="lazy" /><figcaption><b>Building exterior</b><span>Blender Cycles · real sky · ribbed cladding · lime soffit · illuminated sign</span></figcaption></figure>
  <div className="grid g2" style={{marginTop: '20px'}}>
    <figure className="fig"><img src="/assets/render/facility-corridor.jpg" alt="Cleanroom corridor with wayfinding directory" loading="lazy" /><figcaption><b>Cleanroom corridor</b><span>Wall directory · epoxy floor · lime guide line</span></figcaption></figure>
    <figure className="fig"><img src="/assets/art/wayfinding.jpg" alt="Wayfinding sign artwork" className="paper" style={{maxHeight: '100%', objectFit: 'contain', background: 'var(--offwhite)'}} loading="lazy" /><figcaption><b>Directory artwork</b><span>600 × 800 mm</span></figcaption></figure>
    <figure className="fig"><div className="steel"><span className="bolt" style={{left: '20px', top: '20px'}}></span><span className="bolt" style={{right: '20px', top: '20px'}}></span><span className="bolt" style={{left: '20px', bottom: '20px'}}></span><span className="bolt" style={{right: '20px', bottom: '20px'}}></span><div className="etch"><img src="/assets/logo/primary-black.svg" alt="Etched logo" /><div className="lab"><span>Line 00</span><span>Equipment ID 0000</span><span>S/N 0000</span></div></div></div><figcaption><b>Equipment plate</b><span>Laser etch on brushed stainless</span></figcaption></figure>
  </div>
  <div className="sub"><h3>Line control software</h3><span className="lab">Example data</span></div>
  <div className="screen">
    <div className="ui-app">
      <div className="row"><img src="/assets/logo/primary-white-dose.svg" alt="" style={{height: '22px'}} /><div style={{display: 'flex', gap: '10px', flexWrap: 'wrap'}}><span className="chip">Running</span><span className="lab">Line 00 · Batch MB-0000-00</span></div></div>
      <div className="kpis">
        <div className="k"><span className="lab">Output</span><b className="num">4,820</b><span className="lab">units / h</span></div>
        <div className="k"><span className="lab">Weight RSD</span><b className="num">0.42%</b><span className="lab">limit 2.0%</span></div>
        <div className="k"><span className="lab">In spec</span><b className="num">99.6%</b><span className="lab">last 60 min</span></div>
        <div className="k"><span className="lab">Elapsed</span><b className="num">03:12:47</b><span className="lab">of 08:00:00</span></div>
      </div>
      <div className="k" style={{gap: '12px'}}><div className="row"><span className="lab">Tablet weight · mg</span><span className="lab">target 000 ±0</span></div><Sparkline /></div>
    </div>
  </div>
</section>
  );
}
