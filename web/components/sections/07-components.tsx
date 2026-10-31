
export default function SectionComponents() {
  return (
    <section className="sec" id="components" data-name="Components">
  <div className="head">
    <div className="t"><span className="tag">07 Components</span></div>
    <div className="t">
      <h2 className="d-2">The Mustard Bio kit, <span className="mute">built from the brand tokens.</span></h2>
      <p className="lead">Split buttons with a slanted mint arrow tile, a lime-square tag, a white nav pill, cut-corner article cards and the full-bleed marquee.</p>
    </div>
  </div>
  <div className="wrap-bg">
    <div style={{display: 'flex', flexWrap: 'wrap', gap: '20px', alignItems: 'center', marginBottom: '28px'}}>
      <a className="btn" href="#components"><span className="l">Work with us</span><span className="r"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6"><path d="M5 12h14M13 6l6 6-6 6" /></svg></span></a>
      <a className="btn lt" href="#components"><span className="l">Discover our systems</span><span className="r"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6"><path d="M5 12h14M13 6l6 6-6 6" /></svg></span></a>
      <span className="tag w">Intelligent manufacturing</span>
      <span className="tag" style={{background: 'var(--white)'}}>Batch MB-0000-00</span>
      <div className="pill"><a href="#components">Company</a><a href="#components">Newsroom</a><a className="on" href="#components">Work with us</a></div>
    </div>
    <div className="grid g3">
      <div className="art"><div style={{display: 'flex', justifyContent: 'space-between', gap: '10px', flexWrap: 'wrap'}}><span className="tag">Systems</span><span className="lab">00 Month 0000</span></div><h4 className="h-2">Article title set in Heading 2, up to three lines</h4><span className="lab k rd">Read article</span><span className="go"><b><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6"><path d="M5 12h14M13 6l6 6-6 6" /></svg></b></span></div>
      <div className="art s"><div style={{display: 'flex', justifyContent: 'space-between', gap: '10px', flexWrap: 'wrap'}}><span className="tag d">Manufacturing</span><span className="lab" style={{color: 'var(--sage)'}}>00 Month 0000</span></div><h4 className="h-2">Deep Sea card variant for secondary stories</h4><span className="lab rd">Read article</span><span className="go" style={{background: 'var(--gray-1)'}}><b><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6"><path d="M5 12h14M13 6l6 6-6 6" /></svg></b></span></div>
      <div className="art d"><div style={{display: 'flex', justifyContent: 'space-between', gap: '10px', flexWrap: 'wrap'}}><span className="tag d">Technology</span><span className="lab" style={{color: 'var(--sage)'}}>00 Month 0000</span></div><h4 className="h-2">Charcoal card variant for lead stories</h4><span className="lab rd">Read article</span><span className="go" style={{background: 'var(--gray-1)'}}><b><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6"><path d="M5 12h14M13 6l6 6-6 6" /></svg></b></span></div>
    </div>
  </div>
  <div className="rules" style={{marginTop: '28px'}}>
    <div className="rule-c"><span className="lab k">Radius</span><p className="num">6 tags · 10 buttons, pills · 16 cards, media · 24 page bands</p></div>
    <div className="rule-c"><span className="lab k">Spacing</span><p className="num">10 · 20 · 30 · 50 · 70 · 90 · 140, the Mustard Bio scale</p></div>
    <div className="rule-c"><span className="lab k">Grid</span><p>12 columns, 48 px outer margin, 20 px gutter. Headings start on column 5.</p></div>
    <div className="rule-c"><span className="lab k">Button</span><p>Label tile + arrow tile, 9 px slant. Hover widens the arrow tile and turns it lime.</p></div>
  </div>
</section>
  );
}
