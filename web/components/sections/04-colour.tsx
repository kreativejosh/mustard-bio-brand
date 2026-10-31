import { Swatches, ContrastPairs } from '@/components/brand-static';

export default function SectionColour() {
  return (
    <section className="sec" id="colour" data-name="Colour">
  <div className="head">
    <div className="t"><span className="tag">04 Colour</span></div>
    <div className="t">
      <h2 className="d-2">Charcoal, off-white and the lime dose, <span className="mute">token by token.</span></h2>
      <p className="lead">Charcoal and off-white carry almost every surface. Lime and mint are small signals: the dose, the arrow tile, the tag square. Sage is for quiet display text and soft grounds.</p>
    </div>
  </div>
  <div className="ratio" aria-label="Proportion of colour use">
    <div style={{flex: '46', background: 'var(--offwhite)', color: 'var(--text-3)'}}>Off White 46%</div>
    <div style={{flex: '26', background: 'var(--charcoal)', color: 'var(--white)'}}>Charcoal 26%</div>
    <div style={{flex: '12', background: 'var(--stone)', color: 'var(--text-3)'}}>Stone 12%</div>
    <div style={{flex: '7', background: 'var(--sage)'}}></div>
    <div style={{flex: '5', background: 'var(--deepsea)'}}></div>
    <div style={{flex: '4', background: 'var(--mint)'}}></div>
    <div style={{flex: '2', background: 'var(--lime)'}}></div>
  </div>
  <Swatches />

  <div className="sub"><h3>Contrast pairs</h3><span className="lab">WCAG 2.1, computed</span></div>
  <ContrastPairs />
  <div className="note" style={{marginTop: '20px'}}>Headlines set their second half in Sage Mist on off-white (1.53:1). Keep that move to display sizes of 48&nbsp;px and up, where the first half carries the meaning. Running text in grey uses Text 2 #5C6B6C (5.56:1 on white).</div>
</section>
  );
}
