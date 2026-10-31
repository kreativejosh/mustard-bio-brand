
export default function SectionType() {
  return (
    <section className="sec" id="type" data-name="Typography">
  <div className="head">
    <div className="t"><span className="tag">05 Typography</span></div>
    <div className="t">
      <h2 className="d-2">IBM Plex Sans, set with a light touch: <span className="mute">tight tracking, mono labels.</span></h2>
      <p className="lead">The wordmark is drawn in IBM Plex Sans, so the brand speaks in the same face. Display sizes run at Regular with −3% tracking. Labels, buttons and data are IBM Plex Mono in caps. Both are SIL OFL, free for web, print and apps.</p>
    </div>
  </div>
  <div className="grid g2">
    <div className="tile face"><span className="lab k">Primary · IBM Plex Sans</span><div className="big">Aa</div><span className="lab">Light 300 · Regular 400 · Medium 500</span></div>
    <div className="tile face d"><span className="lab" style={{color: 'var(--sage)'}}>Utility · IBM Plex Mono</span><div className="big" style={{fontFamily: 'var(--mono)', letterSpacing: '-.06em'}}>Aa</div><span className="lab" style={{color: 'var(--sage)'}}>Regular 400 · Medium 500 · caps +5% tracking</span></div>
  </div>
  <div className="sub"><h3>Scale</h3><span className="lab">Desktop sizes, fluid below 1440 px</span></div>
  <div>
    <div className="spec"><span className="lab">Display 1<br />112 / 112 · −3%</span><div className="d-1">Measured, not guessed.</div></div>
    <div className="spec"><span className="lab">Display 2<br />72 / 75 · −3%</span><div className="d-2">Intelligent manufacturing <span className="mute">systems.</span></div></div>
    <div className="spec"><span className="lab">Heading 1<br />48 / 52 · −2.5%</span><div className="h-1">Commercial manufacturing</div></div>
    <div className="spec"><span className="lab">Heading 2<br />32 / 37 · −2%</span><div className="h-2">Technology development</div></div>
    <div className="spec"><span className="lab">Lead<br />22 / 30 · −1%</span><p className="lead" style={{margin: '0'}}>Deploy, test, and continuously improve manufacturing software and automation systems in real-world production environments.</p></div>
    <div className="spec"><span className="lab">Body<br />17 / 25.5 · 0</span><p className="body">Produce medicines for pharmaceutical companies and brands through contract and white-label manufacturing.</p></div>
    <div className="spec"><span className="lab">Label · mono<br />13 / 17 · +5% caps</span><span className="lab k">Batch MB-0000-00 · Line 00</span></div>
  </div>
  <div className="sub"><h3>Character set</h3><span className="lab">Fallback: -apple-system, Segoe UI, Helvetica, Arial</span></div>
  <div className="glyphs">ABCDEFGHIJKLM<br />abcdefghijklm<br /><span style={{fontFamily: 'var(--mono)'}}>0123456789 mg/µL</span></div>
</section>
  );
}
