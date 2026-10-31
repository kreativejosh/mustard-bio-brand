import { Illo, IlloGrid, IconSet, BigIcon } from '@/components/brand-static';

export default function SectionIcons() {
  return (
    <section className="sec" id="icons" data-name="Iconography">
  <div className="head">
    <div className="t"><span className="tag">06 Iconography</span></div>
    <div className="t">
      <h2 className="d-2">Hairline geometry. <span className="mute">Drawn, not decorated.</span></h2>
      <p className="lead">Two tiers, one hairline style. Illustrative icons are generative 1&nbsp;px line constructions drawn on a 114 grid and used large on feature cards. Interface icons are a 24&nbsp;px set at 1.25&nbsp;px stroke with round joins.</p>
    </div>
  </div>
  <div className="usp">
    <div style={{background: 'var(--mint)'}}><Illo kind="dose" stroke="#222F30" /><div><h3 className="h-2" style={{marginBottom: '12px'}}>Commercial manufacturing</h3><p>Produce medicines for pharmaceutical companies and brands through contract and white-label manufacturing.</p></div></div>
    <div style={{background: 'var(--charcoal)', color: 'var(--white)'}}><Illo kind="capsules" stroke="#fff" /><div><h3 className="h-2" style={{marginBottom: '12px'}}>Technology development</h3><p>Deploy, test, and continuously improve manufacturing software and automation systems in real-world production environments.</p></div></div>
    <div style={{background: 'var(--stone)'}}><Illo kind="network" stroke="#222F30" /><div><h3 className="h-2" style={{marginBottom: '12px'}}>Intelligence layer</h3><p>A foundational intelligence infrastructure for pharmaceutical manufacturing globally.</p></div></div>
  </div>
  <div className="sub"><h3>Illustrative set · 114 grid · 1 px</h3><span className="lab">Generated from the scale, the capsule and the lattice</span></div>
  <IlloGrid />
  <div className="sub"><h3>Interface set · 24 px · 1.25 stroke</h3><span className="lab">currentColor · hover to see the mint state</span></div>
  <IconSet />
  <div className="grid g3" style={{marginTop: '28px'}}>
    <div className="tile" style={{padding: '22px', display: 'flex', gap: '22px', alignItems: 'center'}}><div className="grid24" style={{width: '120px', height: '120px', flex: 'none', borderRadius: '6px', backgroundColor: 'var(--white)', display: 'grid', placeItems: 'center'}}><BigIcon /></div><p className="body" style={{fontSize: '15px'}}>2&nbsp;px safe area. Shapes sit on whole or half pixels. Round caps and joins.</p></div>
    <div className="rule-c"><span className="do">Do</span><p>Pair icons with a mono label. Inherit text colour. Use the mint tile for selected and hover states.</p></div>
    <div className="rule-c"><span className="dont">Don&apos;t</span><p>Fill icons, mix stroke weights, or colour the stroke lime on white (it fails 3:1 for graphics).</p></div>
  </div>
</section>
  );
}
