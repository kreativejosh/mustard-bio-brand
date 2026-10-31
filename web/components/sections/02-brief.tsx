
export default function SectionBrief() {
  return (
    <section className="sec" id="brief" data-name="Brief">
  <div className="head">
    <div className="t"><span className="tag">02 Brief</span></div>
    <div className="t">
      <h2 className="d-2">Mustard Bio is the intelligence layer for the <span className="mute">pharmaceutical factories of the future.</span></h2>
      <p className="lead">This is the text of the comms and marketing brief, unedited. Use it as the only source for describing the company.</p>
    </div>
  </div>
  <div className="brief">
    <div className="tile d"><span className="tag d">Vision</span><p style={{color: 'var(--white)', fontSize: '24px', letterSpacing: '-.015em', lineHeight: '1.3'}}>To become the intelligence layer powering the next generation of pharmaceutical factories worldwide.</p><p>We envision a future where pharmaceutical manufacturing is increasingly autonomous, intelligent, efficient, and accessible, transforming how essential medicines are produced and supplied globally.</p></div>
    <div className="tile"><span className="tag w">Mission</span><p style={{color: 'var(--text)', fontSize: '24px', letterSpacing: '-.015em', lineHeight: '1.3'}}>To develop, validate, and commercialise intelligent manufacturing systems that make pharmaceutical production faster, more efficient, reliable, and cost-effective.</p><p>We are building technology-enabled pharmaceutical factories, beginning in Nigeria, that serve two interconnected purposes:</p>
      <ol><li><b style={{fontWeight: '500', color: 'var(--text)'}}>Commercial manufacturing:</b> Produce medicines for pharmaceutical companies and brands through contract and white-label manufacturing.</li><li><b style={{fontWeight: '500', color: 'var(--text)'}}>Technology development:</b> Deploy, test, and continuously improve manufacturing software and automation systems in real-world production environments, with the goal of commercialising proprietary technology for other manufacturers.</li></ol></div>
    <div className="tile" style={{background: 'var(--mint)'}}><span className="tag w">Long-term ambition</span><p style={{color: 'var(--text)'}}>To establish Mustard Bio&apos;s technology as a foundational intelligence infrastructure for pharmaceutical manufacturing globally, with the potential to extend into other industries.</p></div>
    <div className="tile" style={{background: 'var(--stone)'}}><span className="tag w">Core positioning</span><p style={{color: 'var(--text)', fontSize: '24px', letterSpacing: '-.015em', lineHeight: '1.3'}}>Mustard Bio is the intelligence layer for the pharmaceutical factories of the future.</p></div>
  </div>
  <div className="note" style={{marginTop: '20px'}}>Brand line used with the logo: “Measured, not guessed.” It comes from the logo idea (a measurement scale whose bold centre graduation is the dose), not from the brief.</div>
</section>
  );
}
