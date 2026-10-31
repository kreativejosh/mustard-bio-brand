'use client';
// Motion demos: easing curves, logo build, line reveal. All replay on view and on click.
import { useCallback, useEffect, useRef, useState, type CSSProperties } from 'react';
import { CURVES } from '@/lib/brand';

/** Restarts a CSS animation class on an element. */
function useReplay<T extends Element>(cls = 'go') {
  const ref = useRef<T>(null);
  const replay = useCallback(() => {
    const el = ref.current; if (!el) return;
    el.classList.remove(cls); void el.getBoundingClientRect(); el.classList.add(cls);
  }, [cls]);
  return [ref, replay] as const;
}

function useOnView(ref: React.RefObject<Element | null>, cb: () => void, threshold = 0.6) {
  useEffect(() => {
    const el = ref.current; if (!el) return;
    const io = new IntersectionObserver((es) => { if (es[0].isIntersecting) cb(); }, { threshold });
    io.observe(el); return () => io.disconnect();
  }, [ref, cb, threshold]);
}

function Curve({ label, bezier, ms, delay }: { label: string; bezier: string; ms: number; delay: number }) {
  const [ref, replay] = useReplay<HTMLDivElement>('play');
  const [x1, y1, x2, y2] = bezier.split(',').map(Number);
  useEffect(() => {
    const el = ref.current; if (!el) return;
    const io = new IntersectionObserver((es) => { if (es[0].isIntersecting) setTimeout(replay, delay); }, { threshold: 0.5 });
    io.observe(el); return () => io.disconnect();
  }, [ref, replay, delay]);
  return (
    <div ref={ref} className="curve" onClick={replay} style={{ '--e': `cubic-bezier(${bezier})`, '--d': `${ms}ms`, cursor: 'pointer' } as CSSProperties}>
      <svg viewBox="-4 -4 108 108">
        <rect x="0" y="0" width="100" height="100" fill="none" stroke="#E4E3E3" />
        <path d={`M0 100C${x1 * 100} ${100 - y1 * 100} ${x2 * 100} ${100 - y2 * 100} 100 0`} fill="none" stroke="#222F30" strokeWidth="1.5" />
        <circle cx={x1 * 100} cy={100 - y1 * 100} r="2.5" fill="#A7E26E" />
        <circle cx={x2 * 100} cy={100 - y2 * 100} r="2.5" fill="#A7E26E" />
      </svg>
      <div className="track"><span className="dot" /></div>
      <div style={{ display: 'flex', justifyContent: 'space-between', gap: '8px' }}><span className="lab k">{label}</span><span className="lab num">{ms} ms</span></div>
      <span className="lab" style={{ fontSize: '11px' }}>cubic-bezier({bezier})</span>
    </div>
  );
}

export function Curves() {
  return <div className="mo">{CURVES.map(([l, b, ms], i) => <Curve key={l} label={l} bezier={b} ms={ms} delay={i * 150} />)}</div>;
}

type LogoPaths = { ticks: { d: string; delay: number }[]; dose: string; word: string; cap: string };

/** Logo build: real logo paths, graduations rise centre-out, wordmark fades up, capsule o rolls in. */
export function LogoBuild() {
  const [ref, replay] = useReplay<SVGSVGElement>();
  const [paths, setPaths] = useState<LogoPaths | null>(null);
  useEffect(() => {
    fetch('/assets/logo/primary-charcoal.svg').then((r) => r.text()).then((t) => {
      const ps = [...new DOMParser().parseFromString(t, 'image/svg+xml').querySelectorAll('path')].map((p) => p.getAttribute('d') || '');
      const ticks = ps[0].match(/M[^M]+/g) || [];
      const xs = ticks.map((s) => parseFloat(s.slice(1))); const cx = (Math.min(...xs) + Math.max(...xs)) / 2;
      setPaths({ ticks: ticks.map((d) => ({ d, delay: (Math.abs(parseFloat(d.slice(1)) - cx) / 160) * 120 + 80 })), dose: ps[1], word: ps[2], cap: ps[3] });
    });
  }, []);
  useOnView(ref, replay);
  return (
    <div className="stage">
      <svg ref={ref} id="logoAnim" viewBox="-34.010 -200.904 1535.568 256.963" aria-label="Logo build animation">
        {paths && <>
          {paths.ticks.map((t) => <path key={t.d} d={t.d} fill="#222F30" className="t" style={{ animationDelay: `${t.delay}ms` }} />)}
          <path d={paths.dose} fill="#A7E26E" className="t" />
          <path d={paths.word} fill="#222F30" className="w" />
          <path d={paths.cap} fill="#222F30" className="cap" />
        </>}
      </svg>
      <button className="mini replay" onClick={replay}>Replay</button>
      <span className="lab" style={{ position: 'absolute', left: '16px', top: '16px' }}>Logo build · 1.8 s</span>
    </div>
  );
}

export function RevealDemo() {
  const [ref, replay] = useReplay<HTMLDivElement>();
  useOnView(ref, replay);
  return (
    <div ref={ref} className="stage reveal-demo" id="revealDemo" style={{ background: 'var(--charcoal)', color: 'var(--white)' }}>
      <h4><span className="ln"><span>Intelligent</span></span><span className="ln"><span>manufacturing</span></span><span className="ln"><span className="mute">systems.</span></span></h4>
      <span className="dk"><button className="mini replay" onClick={replay}>Replay</button></span>
      <span className="lab" style={{ position: 'absolute', left: '16px', top: '16px', color: 'var(--sage)' }}>Line reveal · 1.2 s, 90 ms stagger</span>
    </div>
  );
}
