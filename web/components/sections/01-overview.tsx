import { HeroCanvas } from '@/components/three';

export default function SectionOverview() {
  return (
    <section className="sec" id="overview" data-name="Overview">
  <div className="hero">
    <HeroCanvas />
    <div className="top">
      <img src="/assets/logo/primary-white-dose.svg" alt="Mustard Bio" />
      <div className="pill"><a href="#logo">Logo</a><a href="#colour">Colour</a><a className="on" href="#three">3D &amp; motion</a></div>
    </div>
    <h1>The intelligence layer for the pharmaceutical factories of the future.</h1>
    <div className="bot">
      <p>Brand identity and design system: logo, colour, type, iconography, 3D, motion and applications.</p>
      <a className="btn" href="#brief"><span className="l">Read the brief</span><span className="r"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6"><path d="M5 12h14M13 6l6 6-6 6" /></svg></span></a>
    </div>
  </div>

  <div className="marq" aria-hidden="true"><div>Measured, not guessed — The intelligence layer — Measured, not guessed — The intelligence layer —&nbsp;</div></div>

  <div className="head">
    <div className="t"><span className="tag">How this system works</span></div>
    <div className="t">
      <h2 className="d-2">One fixed logo, a measured visual language, <span className="mute">and a 3D world of glass.</span></h2>
      <p className="lead">Charcoal and off-white grounds, lime for the dose, hairline icons, slow exponential motion and clear lab glass in 3D. Every element follows from the logo idea: medicine that is measured, not guessed. The logo and its typeface (IBM Plex) are fixed.</p>
    </div>
  </div>
  <div className="grid g3">
    <div className="tile" style={{padding: '28px', display: 'flex', flexDirection: 'column', gap: '14px', minHeight: '220px'}}><span className="lab k">Source of copy</span><p className="body">Every description of Mustard Bio on this page comes from the comms and marketing brief. Contact details, product names and figures in mockups are placeholders and are marked as such.</p></div>
    <div className="tile" style={{padding: '28px', display: 'flex', flexDirection: 'column', gap: '14px', minHeight: '220px'}}><span className="lab k">Visual language</span><p className="body">Colour tokens, layout grid, split buttons, lime-square tags, hairline icons and one easing curve, applied the same way in print, product and on screen. In 3D: clear lab glass, glass-sphere chains and metaballs.</p></div>
    <div className="tile" style={{padding: '28px', display: 'flex', flexDirection: 'column', gap: '14px', minHeight: '220px'}}><span className="lab k">What is new here</span><p className="body">Colour applied to the logo, a small-size mark, the scale rule motif, a 24&nbsp;px icon set, path-traced 3D assets and merchandise (Blender Cycles), motion loops, and a 17-item print-ready stationery set.</p></div>
  </div>
</section>
  );
}
