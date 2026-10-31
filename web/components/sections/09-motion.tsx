import { Curves, LogoBuild, RevealDemo } from '@/components/motion';

export default function SectionMotion() {
  return (
    <section className="sec" id="motion" data-name="Motion">
  <div className="head">
    <div className="t"><span className="tag">09 Motion</span></div>
    <div className="t">
      <h2 className="d-2">Slow, exponential, <span className="mute">settling like a measured pour.</span></h2>
      <p className="lead">One easing curve, cubic-bezier(.16, 1, .3, 1), drives everything. Things arrive fast and settle long. Ambient 3D loops drift slowly behind the content, and every animation has a reduced-motion fallback.</p>
    </div>
  </div>
  <Curves />
  <div className="grid g2" style={{marginTop: '20px'}}>
    <LogoBuild />
    <RevealDemo />
    <div className="stage"><div className="loader" aria-label="Loading"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div><span className="lab" style={{position: 'absolute', left: '16px', top: '16px'}}>Loader · graduations</span></div>
    <div className="stage" style={{background: 'var(--stone)'}}><a className="btn" href="#motion"><span className="l">Hover me</span><span className="r"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6"><path d="M5 12h14M13 6l6 6-6 6" /></svg></span></a><span className="lab" style={{position: 'absolute', left: '16px', top: '16px'}}>Button · 400 ms</span></div>
  </div>
  <div className="sub"><h3>3D motion loops</h3><span className="lab">1280 × 720 · 24 fps · H.264 · seamless</span></div>
  <div className="grid g3" id="videos">
    <figure className="fig span2"><video src="/assets/motion/capsule.mp4" poster="/assets/motion/capsule.jpg" muted loop playsInline autoPlay preload="metadata"></video><figcaption><b>Capsule turn</b><span>10 s loop</span></figcaption></figure>
    <figure className="fig"><video src="/assets/motion/markbuild.mp4" poster="/assets/motion/markbuild.jpg" muted loop playsInline autoPlay preload="metadata"></video><figcaption><b>Glass mark build</b><span>5 s</span></figcaption></figure>
    <figure className="fig"><video src="/assets/motion/flow.mp4" poster="/assets/motion/flow.jpg" muted loop playsInline autoPlay preload="metadata"></video><figcaption><b>Flow</b><span>10 s loop</span></figcaption></figure>
    <figure className="fig"><video src="/assets/motion/blob.mp4" poster="/assets/motion/blob.jpg" muted loop playsInline autoPlay preload="metadata"></video><figcaption><b>Metaball</b><span>8 s loop</span></figcaption></figure>
    <figure className="fig"><video src="/assets/motion/helix.mp4" poster="/assets/motion/helix.jpg" muted loop playsInline autoPlay preload="metadata"></video><figcaption><b>Molecule chain</b><span>12 s loop</span></figcaption></figure>
    <figure className="fig span2"><video src="/assets/motion/tubes.mp4" poster="/assets/motion/tubes.jpg" muted loop playsInline autoPlay preload="metadata"></video><figcaption><b>Test tubes</b><span>6 s loop</span></figcaption></figure>
  </div>
  <div className="rules" style={{marginTop: '28px'}}>
    <div className="rule-c"><span className="lab k">Ambient</span><p>3D loops rotate at most one turn per 10 s. Never cut; loops crossfade.</p></div>
    <div className="rule-c"><span className="lab k">Marquee</span><p>One marquee per page, display size, 40 s per cycle, linear.</p></div>
    <div className="rule-c"><span className="lab k">Reduced motion</span><p>Loops show their poster frame. Reveals and builds jump to the end state.</p></div>
  </div>
</section>
  );
}
