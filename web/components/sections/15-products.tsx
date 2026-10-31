
export default function SectionProducts() {
  return (
    <section className="sec" id="products" data-name="Products">
  <div className="head">
    <div className="t"><span className="tag">15 Products</span></div>
    <div className="t">
      <h2 className="d-2">Partner brand first, <span className="mute">Mustard Bio as the maker.</span></h2>
      <p className="lead">Mustard Bio produces medicines for pharmaceutical companies and brands through contract and white-label manufacturing. Packs lead with the partner&apos;s brand. Mustard Bio appears in the charcoal manufacturer band, with the scale rule as the product&apos;s measurement cue.</p>
    </div>
  </div>
  <figure className="fig"><img src="/assets/render/asset-pack.jpg" alt="Cartons and blister packs" loading="lazy" /><figcaption><b>Carton &amp; blister</b><span>Rendered in Blender Cycles · all product text is placeholder</span></figcaption></figure>
  <div className="grid g3" style={{marginTop: '20px'}}>
    <figure className="fig span2"><img src="/assets/art/carton-front.jpg" alt="Carton front artwork" className="paper" loading="lazy" /><figcaption><b>Carton front</b><span>Partner zone · manufacturer band</span></figcaption></figure>
    <div className="rules" style={{gridTemplateColumns: '1fr', alignContent: 'start'}}>
      <div className="rule-c"><span className="lab k">Partner zone</span><p>Top 80% of the front panel. Partner brand, product name, strength, count.</p></div>
      <div className="rule-c"><span className="lab k">Manufacturer band</span><p>Charcoal band, 15% of panel height. “Manufactured by” in mono caps + reverse lockup.</p></div>
      <div className="rule-c"><span className="lab k">Batch panel</span><p>Plex Mono for batch, manufacture and expiry dates. Lime base strip on side panels.</p></div>
    </div>
  </div>
</section>
  );
}
