
export default function SectionFiles() {
  return (
    <section className="sec" id="files" data-name="Files">
  <div className="head">
    <div className="t"><span className="tag">16 Files</span></div>
    <div className="t">
      <h2 className="d-2">Where everything lives.</h2>
      <p className="lead">All source files sit in the brand repository under <code style={{fontFamily: 'var(--mono)', fontSize: '.9em'}}>identity/assets/</code>.</p>
    </div>
  </div>
  <div className="tw"><table>
    <thead><tr><th>Folder</th><th>Contents</th><th>Formats</th></tr></thead>
    <tbody>
      <tr><td>logo/</td><td className="wrap">Primary charcoal, white, white with lime dose, black; mark, Mark S, wordmark, app icon</td><td>SVG</td></tr>
      <tr><td>3d/</td><td className="wrap">Capsule, glass mark, molecule chain, metaballs, test tubes, flask, tablets, flow grounds</td><td>JPG 1600 px</td></tr>
      <tr><td>motion/</td><td className="wrap">Capsule, glass mark build, flow, metaball, molecule chain, test tubes</td><td>MP4 720p + poster</td></tr>
      <tr><td>render/</td><td className="wrap">Blender Cycles renders: merchandise, 3D brand assets, packaging, facility, stationery overview</td><td>JPG 2400 px</td></tr>
      <tr><td>stationery/print/</td><td className="wrap">17 stationery items at trim size plus email signature</td><td>PNG 300 dpi + PDF with 3 mm bleed</td></tr>
            <tr><td>art/</td><td className="wrap">Flat print artwork for cards, flyer, poster, letterhead, badge, wayfinding, carton, notebook</td><td>JPG</td></tr>
      <tr><td>fonts/</td><td className="wrap">IBM Plex Sans and Mono, SIL Open Font License</td><td>WOFF</td></tr>
    </tbody></table></div>
</section>
  );
}
