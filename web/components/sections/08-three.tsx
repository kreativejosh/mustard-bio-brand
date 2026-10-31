import { Viewer3D } from '@/components/three';

export default function SectionThree() {
  return (
    <section className="sec" id="three" data-name="3D assets">
  <div className="head">
    <div className="t"><span className="tag">08 3D assets</span></div>
    <div className="t">
      <h2 className="d-2">Clear lab glass, <span className="mute">lit like a product studio.</span></h2>
      <p className="lead">The Mustard Bio 3D language: clear lab glass, frosted lime for the dose, glossy charcoal for structure, soft studio light. Stills are path-traced in Blender Cycles, so glass refracts, liquids absorb light and shadows fall softly. The live viewer below is the real-time version for web use; drag to turn the models.</p>
    </div>
  </div>
  <Viewer3D />
  <div className="grid g3" style={{marginTop: '20px'}}>
    <figure className="fig span2"><img src="/assets/render/asset-capsule-dark.jpg" alt="Glass capsule with granules, lime frosted half" loading="lazy" /><figcaption><b>Dose capsule</b><span>Hero asset · leans 36.15°</span></figcaption></figure>
    <figure className="fig"><img src="/assets/render/asset-capsule-light.jpg" alt="Glass capsule on light ground" loading="lazy" /><figcaption><b>Dose capsule</b><span>Light</span></figcaption></figure>
    <figure className="fig"><img src="/assets/render/asset-mark-dark.jpg" alt="Logo mark as glass graduations" loading="lazy" /><figcaption><b>Glass mark</b><span>Dark</span></figcaption></figure>
    <figure className="fig"><img src="/assets/render/asset-mark-light.jpg" alt="Logo mark as glass on light" loading="lazy" /><figcaption><b>Glass mark</b><span>Light</span></figcaption></figure>
    <figure className="fig"><img src="/assets/render/asset-helix.jpg" alt="Glass molecule chain" loading="lazy" /><figcaption><b>Molecule chain</b><span>Glass spheres</span></figcaption></figure>
    <figure className="fig"><img src="/assets/render/asset-flask.jpg" alt="Graduated Erlenmeyer flask" loading="lazy" /><figcaption><b>Graduated flask</b><span>Scale printed on glass</span></figcaption></figure>
    <figure className="fig"><img src="/assets/render/asset-tubes.jpg" alt="Test tubes in a charcoal rack" loading="lazy" /><figcaption><b>Test tubes</b><span>Spot-lit</span></figcaption></figure>
    <figure className="fig"><img src="/assets/render/asset-blob.jpg" alt="Mint glass metaball" loading="lazy" /><figcaption><b>Metaball</b><span>Thin-film glass</span></figcaption></figure>
    <figure className="fig span2"><img src="/assets/render/asset-tablets.jpg" alt="Capsules and scored tablets" loading="lazy" /><figcaption><b>Dose field</b><span>Top-down</span></figcaption></figure>
    <figure className="fig"><img src="/assets/3d/flow-light.jpg" alt="Light flowing abstract" loading="lazy" /><figcaption><b>Flow</b><span>Hero ground · light</span></figcaption></figure>
    <figure className="fig span2"><img src="/assets/3d/flow-wide.jpg" alt="Flowing green glass abstract" loading="lazy" /><figcaption><b>Flow</b><span>Wide hero ground</span></figcaption></figure>
  </div>
  <div className="sub"><h3>Material and scene rules</h3><span className="lab">Blender Cycles · Principled BSDF</span></div>
  <div className="rules">
    <div className="rule-c"><span className="lab k">Glass</span><p>Transmission 1, roughness 0.02–0.05, IOR 1.5, clearcoat 1, attenuation tint #DFF3E6. Thin walls on vessels, thick on solids.</p></div>
    <div className="rule-c"><span className="lab k">Frosted dose</span><p>Fresh Lime, transmission 0.7–0.85, roughness 0.22–0.35. Only one frosted lime object per frame.</p></div>
    <div className="rule-c"><span className="lab k">Light</span><p>Poly Haven studio HDRI at low strength plus a large soft key, a rim strip and a backdrop wash. Khronos PBR Neutral view transform keeps brand colours true.</p></div>
    <div className="rule-c"><span className="lab k">Ground</span><p>Radial gradient sweeps: White → Stone → Sage on light; Deep Sea → Charcoal on dark. Film grain 2.5%.</p></div>
  </div>
</section>
  );
}
