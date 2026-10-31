
export default function SectionImagery() {
  return (
    <section className="sec" id="imagery" data-name="Imagery">
  <div className="head">
    <div className="t"><span className="tag">10 Imagery</span></div>
    <div className="t">
      <h2 className="d-2">Real production, <span className="mute">soft light, shallow focus.</span></h2>
      <p className="lead">Photography shows people and equipment at work, close and calm, with the green tint of the 3D world. When a photograph cannot show it, 3D does.</p>
    </div>
  </div>
  <div className="grid g4">
    <div className="tile" style={{padding: '24px', display: 'flex', flexDirection: 'column', gap: '12px', minHeight: '240px'}}><span className="lab k">Subject</span><p className="body" style={{fontSize: '15px'}}>Production lines, control rooms, lab glass, hands on equipment, packaging in progress. Real staff and real facilities only.</p></div>
    <div className="tile" style={{padding: '24px', display: 'flex', flexDirection: 'column', gap: '12px', minHeight: '240px'}}><span className="lab k">Light</span><p className="body" style={{fontSize: '15px'}}>Soft and diffused, from above or the side. Clean whites that do not clip. No hard flash.</p></div>
    <div className="tile" style={{padding: '24px', display: 'flex', flexDirection: 'column', gap: '12px', minHeight: '240px'}}><span className="lab k">Grade</span><p className="body" style={{fontSize: '15px'}}>Slight green-sage cast in the shadows, lifted blacks to Charcoal, saturation −10. Matches the 3D renders.</p></div>
    <div className="tile" style={{padding: '24px', display: 'flex', flexDirection: 'column', gap: '12px', minHeight: '240px'}}><span className="lab k">Avoid</span><p className="body" style={{fontSize: '15px'}}>Stock lab clichés, blue sci-fi overlays, glowing DNA, staged handshakes, people looking at camera.</p></div>
  </div>
  <div className="grid g3" style={{marginTop: '20px'}}>
    <figure className="fig"><img src="/assets/render/asset-tubes.jpg" alt="" loading="lazy" /><figcaption><b>Vessels</b><span>Spot-lit, dark ground</span></figcaption></figure>
    <figure className="fig"><img src="/assets/render/asset-flask.jpg" alt="" loading="lazy" /><figcaption><b>Measurement</b><span>Light ground</span></figcaption></figure>
    <figure className="fig"><img src="/assets/render/asset-tablets.jpg" alt="" loading="lazy" /><figcaption><b>Product</b><span>Top-down</span></figcaption></figure>
  </div>
  <div className="note" style={{marginTop: '20px'}}>AI-generated imagery is not used for people or facilities. 3D renders stand in for anything that cannot yet be photographed.</div>
</section>
  );
}
