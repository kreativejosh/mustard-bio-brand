import { Illo } from '@/components/brand-static';

export default function SectionMarketing() {
  return (
    <section className="sec" id="marketing" data-name="Marketing">
  <div className="head">
    <div className="t"><span className="tag">12 Marketing</span></div>
    <div className="t">
      <h2 className="d-2">Out of home, print, <span className="mute">social and slides.</span></h2>
      <p className="lead">Every headline is lifted from the brief or the logo line. The sage second half carries the brand&apos;s headline rhythm into print.</p>
    </div>
  </div>
  <figure className="fig"><img src="/assets/render/billboard.jpg" alt="Billboard with floodlights" loading="lazy" /><figcaption><b>Billboard · 48 sheet</b><span>Blender Cycles · floodlights bolted to the frame</span></figcaption></figure>
  <div className="grid g3" style={{marginTop: '20px'}}>
    <figure className="fig"><img src="/assets/art/flyer.jpg" alt="A4 flyer" className="paper" loading="lazy" /><figcaption><b>Flyer</b><span>A4</span></figcaption></figure>
    <figure className="fig"><img src="/assets/art/poster.jpg" alt="Vision poster" className="paper" loading="lazy" /><figcaption><b>Poster</b><span>2:3 · facility &amp; events</span></figcaption></figure>
    <figure className="fig"><img src="/assets/art/notebook.jpg" alt="Notebook cover" className="paper" loading="lazy" /><figcaption><b>Notebook cover</b><span>A5</span></figcaption></figure>
  </div>
  <div className="sub"><h3>Social</h3><span className="lab">4:5 · LinkedIn and Instagram</span></div>
  <div className="grid g3">
    <div className="social" style={{background: 'var(--charcoal)', color: 'var(--white)'}}><img className="bg" src="/assets/3d/blob-deep.jpg" alt="" /><span className="tag d" style={{alignSelf: 'flex-start'}}>Mustard Bio</span><h4>Measured,<br /><span style={{color: 'var(--mint)'}}>not guessed.</span></h4></div>
    <div className="social" style={{background: 'var(--mint)'}}><span className="tag w" style={{alignSelf: 'flex-start'}}>01 Commercial manufacturing</span><Illo kind="dose" stroke="#222F30" style={{ width: '34%', alignSelf: 'flex-end' }} /><h4>Medicines for pharmaceutical companies and brands, <span style={{color: 'var(--deepsea)'}}>through contract and white-label manufacturing.</span></h4></div>
    <div className="social" style={{background: 'var(--offwhite)'}}><img className="bg" src="/assets/3d/mark-glass-light.jpg" alt="" style={{height: '62%', top: 'auto', bottom: '0'}} /><span className="tag w" style={{alignSelf: 'flex-start'}}>02 Technology development</span><h4 style={{marginTop: 'auto', marginBottom: 'auto', alignSelf: 'flex-start', position: 'absolute', top: '22%', left: '7%', right: '7%'}}>Software and automation, <span className="mute">tested in real-world production.</span></h4></div>
  </div>
  <div className="grid g2" style={{marginTop: '20px'}}>
    <div className="slide"><div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}><img src="/assets/logo/primary-charcoal.svg" alt="" style={{width: '30%'}} /><span className="lab">01</span></div><h4 style={{fontSize: 'clamp(22px,3vw,44px)', letterSpacing: '-.03em', lineHeight: '1.04', maxWidth: '16ch'}}>The intelligence layer for the <span className="mute">pharmaceutical factories of the future.</span></h4><span className="lab">Presentation · title slide</span></div>
    <div className="slide" style={{background: 'var(--charcoal)', color: 'var(--white)', padding: '0'}}><img src="/assets/3d/flow-dark.jpg" alt="" style={{position: 'absolute', inset: '0', width: '100%', height: '100%', objectFit: 'cover'}} /><div style={{position: 'relative', padding: '5%', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', height: '100%'}}><span className="tag d" style={{alignSelf: 'flex-start'}}>Mission</span><h4 style={{fontSize: 'clamp(18px,2.2vw,32px)', letterSpacing: '-.025em', lineHeight: '1.12', maxWidth: '24ch'}}>Faster, more efficient, reliable, and cost-effective <span style={{color: 'var(--mint)'}}>pharmaceutical production.</span></h4><span className="lab" style={{color: 'var(--sage)'}}>Presentation · section slide</span></div></div>
  </div>
</section>
  );
}
