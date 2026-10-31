// Server-rendered brand blocks: colour swatches, contrast pairs, icons, illustrations, sparkline.
import type { CSSProperties } from 'react';
import { COLOURS, PAIRS, ICONS, ILLO, ILLO_TILES, contrast, wcagLevel, sparkline, type IlloKind } from '@/lib/brand';

export function Swatches() {
  return (
    <div className="grid g4" style={{ marginTop: '20px' }}>
      {COLOURS.map((c) => (
        <div className="sw" key={c.hex}>
          <div className="c" style={{ background: c.hex, color: c.ink, boxShadow: c.hex === '#F7F7F5' || c.hex === '#EEEEEE' ? 'inset 0 -1px 0 var(--line)' : undefined }}>
            <span>var({c.token})</span>
            <span>{contrast(c.hex, '#FFFFFF').toFixed(2)}:1 / white</span>
          </div>
          <div className="i">
            <b>{c.name}</b>
            <span>HEX {c.hex}</span><span>RGB {c.rgb}</span><span>HSL {c.hsl}</span><span>CMYK {c.cmyk}</span>
            <span style={{ fontFamily: 'var(--sans)', fontSize: '14px', marginTop: '6px' }}>{c.use}</span>
          </div>
        </div>
      ))}
    </div>
  );
}

export function ContrastPairs() {
  return (
    <div className="pairs">
      {PAIRS.map(([fg, bg, label]) => {
        const r = contrast(fg, bg);
        return (
          <div className="pair" key={fg + bg} style={{ background: bg, color: fg, boxShadow: bg === '#FFFFFF' || bg === '#F7F7F5' ? '0 0 0 1px var(--line)' : undefined }}>
            <span className="s">Aa {r.toFixed(2)}</span>
            <span className="m"><span>{label}</span><span>{wcagLevel(r)}</span></span>
          </div>
        );
      })}
    </div>
  );
}

export function IconSet() {
  return (
    <div className="icons">
      {Object.entries(ICONS).map(([name, inner]) => (
        <div className="ic" key={name}>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.25" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" dangerouslySetInnerHTML={{ __html: inner }} />
          <span>{name}</span>
        </div>
      ))}
    </div>
  );
}

export function BigIcon() {
  return <svg viewBox="0 0 24 24" width="120" height="120" fill="none" stroke="#222F30" strokeWidth=".9" strokeLinecap="round" strokeLinejoin="round" dangerouslySetInnerHTML={{ __html: ICONS.capsule }} />;
}

export function Illo({ kind, stroke, style }: { kind: IlloKind; stroke: string; style?: CSSProperties }) {
  return <svg viewBox="0 0 114 114" fill="none" stroke={stroke} strokeWidth="1" strokeMiterlimit="10" aria-hidden="true" style={style} dangerouslySetInnerHTML={{ __html: ILLO[kind]() }} />;
}

export function IlloGrid() {
  return (
    <div className="illo">
      {ILLO_TILES.map(([k, bg, st]) => (
        <div className="tile" key={k} style={{ background: bg }}>
          <Illo kind={k} stroke={st} />
          <span className="lab" style={{ position: 'absolute', left: '12px', bottom: '10px', color: st, opacity: 0.7 }}>{k}</span>
        </div>
      ))}
    </div>
  );
}

export function Sparkline() {
  const s = sparkline();
  return (
    <svg viewBox="0 0 600 140" style={{ width: '100%', height: '140px' }} preserveAspectRatio="none">
      <path d="M0 30H600M0 110H600" stroke="rgba(201,203,190,.25)" strokeDasharray="4 6" />
      <path d={s.area} fill="rgba(167,226,110,.12)" />
      <path d={s.d} fill="none" stroke="#CEF79E" strokeWidth="1.5" vectorEffect="non-scaling-stroke" />
      <circle cx="600" cy={s.last.toFixed(1)} r="4" fill="#A7E26E" />
    </svg>
  );
}
