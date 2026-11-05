
// [file id, name, finished size]; files come from identity/render/stat8k.js + pdfprep.py
const ITEMS: [string, string, string][] = [
  ['business-card-front', 'Business card · front', '85 × 55 mm'],
  ['business-card-back', 'Business card · back', '85 × 55 mm'],
  ['letterhead', 'Letterhead', 'A4 · 210 × 297 mm'],
  ['continuation-sheet', 'Continuation sheet', 'A4 · 210 × 297 mm'],
  ['compliments-slip', 'Compliments slip', '210 × 99 mm'],
  ['envelope-dl', 'DL envelope', '220 × 110 mm'],
  ['envelope-c4', 'C4 envelope', '324 × 229 mm'],
  ['presentation-folder', 'Presentation folder · outer', '440 × 310 mm spread'],
  ['report-cover', 'Report cover', 'A4 · 210 × 297 mm'],
  ['document-template', 'Document template', 'A4 · 210 × 297 mm'],
  ['invoice', 'Invoice', 'A4 · 210 × 297 mm'],
  ['notepad', 'Notepad', 'A5 · 148 × 210 mm'],
  ['notebook-cover', 'Notebook cover', 'A5 · 148 × 210 mm'],
  ['staff-id-front', 'Staff ID · front', 'CR80 · 54 × 86 mm'],
  ['staff-id-back', 'Staff ID · back', 'CR80 · 54 × 86 mm'],
  ['visitor-pass', 'Visitor pass', 'CR80 · 54 × 86 mm'],
  ['sticker-sheet', 'Sticker sheet', 'A6 · 105 × 148 mm'],
];

export default function SectionStationery() {
  return (
    <section className="sec" id="stationery" data-name="Stationery">
  <div className="head">
    <div className="t"><span className="tag">11 Stationery</span></div>
    <div className="t">
      <h2 className="d-2">Seventeen print items, <span className="mute">each set square and ready to export.</span></h2>
      <p className="lead">Click any image to view it full size. Every item is built at its true trim size. Each comes as a vector PDF with 3 mm bleed and trim and bleed boxes set in the file (RGB for screen and office printing, CMYK for press) and an 8K PNG of the finished size. Zoom in as far as you like: type stays sharp. Names, addresses, numbers and amounts are placeholders.</p>
    </div>
  </div>
  <div className="grid g2">
    <figure className="fig mock-lg"><img src="/assets/render/stat-cards.jpg" data-full="/assets/render/8k/stat-cards.jpg" alt="Business cards, front and back" loading="lazy" /><figcaption><b>Business cards</b><span>Front · back · Blender Cycles</span></figcaption></figure>
    <figure className="fig"><img src="/assets/render/stat-letter.jpg" data-full="/assets/render/8k/stat-letter.jpg" alt="Letterhead and continuation sheet" loading="lazy" /><figcaption><b>Letterhead &amp; continuation</b><span>A4</span></figcaption></figure>
    <figure className="fig"><img src="/assets/render/stat-finance.jpg" data-full="/assets/render/8k/stat-finance.jpg" alt="Invoice and document template" loading="lazy" /><figcaption><b>Invoice &amp; document template</b><span>A4</span></figcaption></figure>
    <figure className="fig"><img src="/assets/render/stat-report.jpg" data-full="/assets/render/8k/stat-report.jpg" alt="Report cover, notebook and notepad" loading="lazy" /><figcaption><b>Report cover, notebook, notepad</b><span>A4 · A5</span></figcaption></figure>
    <figure className="fig"><img src="/assets/render/stat-post.jpg" data-full="/assets/render/8k/stat-post.jpg" alt="Compliments slip and envelopes" loading="lazy" /><figcaption><b>Compliments slip &amp; envelopes</b><span>DL · C4</span></figcaption></figure>
    <figure className="fig"><img src="/assets/render/stat-id.jpg" data-full="/assets/render/8k/stat-id.jpg" alt="Staff ID, visitor pass and stickers" loading="lazy" /><figcaption><b>ID cards &amp; stickers</b><span>CR80 · A6</span></figcaption></figure>
    <figure className="fig"><img src="/assets/render/stat-folder.jpg" data-full="/assets/render/8k/stat-folder.jpg" alt="Presentation folder outer spread" loading="lazy" /><figcaption><b>Presentation folder</b><span>440 × 310 mm spread</span></figcaption></figure>
  </div>
  <div className="st-grid" style={{marginTop: '20px'}}>{ITEMS.map(([id, name, size]) => (
    <figure className="st" key={id}><div className="st-img"><img src={`/assets/stationery/preview/${id}.jpg`} data-full={`/assets/stationery/print/${id}.png`} alt={name} loading="lazy" /></div><figcaption><b>{name}</b><span>{size}</span><span className="dl"><a href={`/assets/stationery/print/${id}.pdf`} download>PDF</a><a href={`/assets/stationery/print/${id}-cmyk.pdf`} download>PDF CMYK</a><a href={`/assets/stationery/print/${id}.png`} download>PNG 8K</a></span></figcaption></figure>
  ))}</div>
  <div className="sub"><h3>Email signature</h3><span className="lab">HTML, 600 px max · <a href="/assets/stationery/print/email-signature.png" download>PNG</a></span></div>
  <div className="sig">
    <img src="/assets/logo/mark-charcoal.svg" alt="" style={{width: '64px'}} />
    <div className="r"><b style={{fontWeight: '500', color: 'var(--text)', fontSize: '17px'}}>Firstname Lastname</b><span className="lab">Job title</span><span>name@company-domain · +000 000 000 0000</span><span style={{color: 'var(--text-3)', fontSize: '13px'}}>The intelligence layer for the pharmaceutical factories of the future.</span></div>
  </div>
  <div className="note" style={{marginTop: '20px'}}>Download each item above, or find every file in the brand repository at <code style={{fontFamily: 'var(--mono)', fontSize: '.92em'}}>identity/assets/stationery/print/</code>. Print PDFs include 3 mm bleed on every side with TrimBox and BleedBox set, fonts embedded; keep text 5 mm inside the trim. Send the CMYK PDF to press and ask for a hard proof: lime and mint sit at the edge of the CMYK gamut.</div>
</section>
  );
}
