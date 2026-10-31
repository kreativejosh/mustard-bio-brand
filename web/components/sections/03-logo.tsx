
export default function SectionLogo() {
  return (
    <section className="sec" id="logo" data-name="Logo">
  <div className="head">
    <div className="t"><span className="tag">03 Logo</span></div>
    <div className="t">
      <h2 className="d-2">A measurement scale that draws an M, <span className="mute">ending in a capsule.</span></h2>
      <p className="lead">Eleven graduations at a fixed pitch. Ticks one to nine sit on two straight lines that meet at the centre. The bold centre graduation is the dose. The wordmark is IBM Plex Sans Regular, and its final o is drawn as a capsule leaning 36.15°.</p>
    </div>
  </div>
  <div className="grid g2">
    <div className="tile lg" style={{background: 'var(--offwhite)'}}><img src="/assets/logo/primary-charcoal.svg" alt="Primary logo in charcoal" /></div>
    <div className="tile lg d"><img src="/assets/logo/primary-white-dose.svg" alt="Reverse logo with lime dose graduation" /></div>
  </div>
  <div className="grid g4" style={{marginTop: '20px'}}>
    <div className="tile lg sq w"><img src="/assets/logo/mark-charcoal.svg" alt="Mark" style={{width: '70%'}} /></div>
    <div className="tile lg sq d"><img src="/assets/logo/mark-white-dose.svg" alt="Mark reverse" style={{width: '70%'}} /></div>
    <div className="tile lg sq" style={{background: 'var(--lime)'}}><img src="/assets/logo/mark-small-charcoal.svg" alt="Small mark" style={{width: '62%'}} /></div>
    <div className="tile lg sq" style={{background: 'var(--stone)'}}><img src="/assets/logo/app-icon.svg" alt="App icon" style={{width: '62%', borderRadius: '22%'}} /></div>
  </div>
  <div className="grid g4" style={{marginTop: '12px'}}>
    <span className="lab">Mark · charcoal</span><span className="lab">Mark · reverse, lime dose</span><span className="lab">Mark S · 7 graduations</span><span className="lab">App icon · favicon</span>
  </div>

  <div className="sub"><h3>Colour on the logo</h3><span className="lab">Recolour only. Geometry untouched.</span></div>
  <div className="rules">
    <div className="rule-c"><span className="lab k">On light grounds</span><p>Entire lockup in Dark Charcoal #222F30. The dose stays charcoal: lime on white is 1.53:1 and disappears.</p></div>
    <div className="rule-c"><span className="lab k">On dark grounds</span><p>Lockup in white with the dose graduation in Fresh Lime #A7E26E (9.06:1 on charcoal). This is the signature version.</p></div>
    <div className="rule-c"><span className="lab k">One colour</span><p>Pure black or pure white for etching, embossing, debossing, single-colour print and fax.</p></div>
    <div className="rule-c"><span className="lab k">On imagery and 3D</span><p>White, with a white base plate (as in the site navigation) when the image behind is busy.</p></div>
  </div>

  <div className="sub"><h3>Clear space and minimum size</h3><span className="lab">x = cap height of the wordmark</span></div>
  <div className="grid g2">
    <div className="clear tile"><div className="box"><img src="/assets/logo/primary-charcoal.svg" alt="Logo with clear space" /></div><span className="lab" style={{position: 'absolute', left: '18px', bottom: '16px'}}>Clear space = 0.5x on all sides</span></div>
    <div className="tile w sizes">
      <div><img src="/assets/logo/primary-charcoal.svg" alt="" style={{width: '240px'}} /><span className="lab">Lockup · min 120 px / 30 mm</span></div>
      <div><img src="/assets/logo/mark-charcoal.svg" alt="" style={{height: '32px', width: 'auto'}} /><span className="lab">Mark · 24 px +</span></div>
      <div><img src="/assets/logo/mark-small-charcoal.svg" alt="" style={{height: '16px', width: 'auto'}} /><span className="lab">Mark S · below 24 px</span></div>
      <p className="body" style={{fontSize: '15px'}}>Under 24&nbsp;px tall the eleven fine graduations fill in. Mark S keeps the M silhouette with seven graduations at a wider pitch (the outer ticks and every other tick from the full mark).</p>
    </div>
  </div>

  <div className="sub"><h3>Misuse</h3><span className="lab">The logo is fixed artwork</span></div>
  <div className="mis">
    <div className="tile w"><img src="/assets/logo/primary-charcoal.svg" alt="" style={{transform: 'scaleX(1.35)'}} /><span className="dont x">Stretch</span></div>
    <div className="tile w"><img src="/assets/logo/primary-charcoal.svg" alt="" style={{transform: 'rotate(-12deg)'}} /><span className="dont x">Rotate</span></div>
    <div className="tile" style={{background: 'var(--lime)'}}><img src="/assets/logo/primary-white.svg" alt="" /><span className="dont x">Low contrast</span></div>
    <div className="tile w"><div style={{display: 'flex', alignItems: 'center', gap: '6%', width: '100%'}}><img src="/assets/logo/mark-charcoal.svg" alt="" style={{width: '26%'}} /><span style={{fontSize: 'clamp(16px,2vw,28px)', whiteSpace: 'nowrap'}}>Mustard Bio</span></div><span className="dont x">Retype the o</span></div>
  </div>
</section>
  );
}
