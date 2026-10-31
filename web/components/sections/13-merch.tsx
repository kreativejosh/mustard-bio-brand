
export default function SectionMerch() {
  return (
    <section className="sec" id="merch" data-name="Merchandise">
  <div className="head">
    <div className="t"><span className="tag">13 Merchandise</span></div>
    <div className="t">
      <h2 className="d-2">Things people carry. <span className="mute">Real materials, one mark each.</span></h2>
      <p className="lead">Rendered in Blender Cycles with cloth-simulated cotton and canvas, powder-coated steel, glazed ceramic and engraved silicone, lit like a product studio. One mark per item, placed where it would be printed, embroidered or debossed. Lime appears as a cap, a glaze or a band.</p>
    </div>
  </div>
  <div className="sub" style={{marginTop: '0'}}><h3>T-shirts</h3><span className="lab">Oversized heavyweight cotton · front and back</span></div>
  <div className="grid g2">
    <figure className="fig"><img src="/assets/render/tee-stone-front.jpg" alt="Stone T-shirt, front" loading="lazy" /><figcaption><b>Front</b><span>Stone · chest mark</span></figcaption></figure>
    <figure className="fig"><img src="/assets/render/tee-stone-back.jpg" alt="Stone T-shirt, back" loading="lazy" /><figcaption><b>Back</b><span>Stone · vertical lockup</span></figcaption></figure>
    <figure className="fig"><img src="/assets/render/tee-ink-front.jpg" alt="Charcoal T-shirt, front" loading="lazy" /><figcaption><b>Front</b><span>Charcoal · mark with lime dose</span></figcaption></figure>
    <figure className="fig"><img src="/assets/render/tee-ink-back.jpg" alt="Charcoal T-shirt, back" loading="lazy" /><figcaption><b>Back</b><span>Charcoal · vertical lockup</span></figcaption></figure>
  </div>
  <div className="sub"><h3>Totes</h3><span className="lab">Cotton canvas · webbing handles · box-X stitching</span></div>
  <div className="grid g2">
    <figure className="fig"><img src="/assets/render/tote-natural.jpg" alt="Natural canvas tote in window light" loading="lazy" /><figcaption><b>Natural</b><span>Charcoal print</span></figcaption></figure>
    <figure className="fig"><img src="/assets/render/tote-ink.jpg" alt="Charcoal canvas tote in window light" loading="lazy" /><figcaption><b>Charcoal</b><span>White print, lime line</span></figcaption></figure>
  </div>
  <div className="sub"><h3>Everyday objects</h3><span className="lab">Blender Cycles</span></div>
  <div className="grid g2">
    <figure className="fig"><img src="/assets/render/merch-bottles.jpg" alt="Charcoal and white insulated bottles" loading="lazy" /><figcaption><b>Water bottles</b><span>750 ml steel · powder coat · knurled cap</span></figcaption></figure>
    <figure className="fig"><img src="/assets/render/merch-mugs.jpg" alt="White glazed and charcoal matte mugs" loading="lazy" /><figcaption><b>Mugs</b><span>Glazed ceramic · lime and charcoal interiors</span></figcaption></figure>
    <figure className="fig mock-lg"><img src="/assets/render/merch-bands.jpg" alt="Silicone wristbands with engraved lettering" loading="lazy" /><figcaption><b>Wristbands</b><span>Silicone · lettering engraved 0.4 mm</span></figcaption></figure>
    <figure className="fig mock-lg"><img src="/assets/render/merch-lanyard.jpg" alt="Woven lanyard with breakaway buckle, staff ID and visitor pass" loading="lazy" /><figcaption><b>Lanyard, staff ID &amp; visitor pass</b><span>Woven polyester · breakaway buckle · CR80 PVC</span></figcaption></figure>
  </div>
</section>
  );
}
