'use client';
// Left system nav (desktop) and section picker (phone). Highlights the section in view.
import { useEffect, useState } from 'react';
import { NAV } from '@/lib/brand';

function useActiveSection() {
  const [active, setActive] = useState('overview');
  useEffect(() => {
    const io = new IntersectionObserver(
      (es) => es.forEach((e) => { if (e.isIntersecting) setActive(e.target.id); }),
      { rootMargin: '-40% 0px -55% 0px' },
    );
    document.querySelectorAll('main .sec').forEach((s) => io.observe(s));
    return () => io.disconnect();
  }, []);
  return active;
}

export function Sidebar() {
  const active = useActiveSection();
  let n = 0;
  return (
    <aside className="side">
      <a className="brand" href="#overview"><img src="/assets/logo/primary-charcoal.svg" alt="Mustard Bio" /></a>
      <nav>
        {NAV.map((g) => (
          <div className="grp" key={g.group}>
            <span>{g.group}</span>
            {g.items.map(([id, label]) => {
              n += 1;
              return <a key={id} href={`#${id}`} className={active === id ? 'on' : undefined}><i>{String(n).padStart(2, '0')}</i>{label}</a>;
            })}
          </div>
        ))}
      </nav>
      <div className="meta">Brand identity v1.2<br />31 Oct 2026</div>
    </aside>
  );
}

export function MobileBar() {
  const active = useActiveSection();
  return (
    <div className="mbar">
      <img src="/assets/logo/primary-charcoal.svg" alt="Mustard Bio" />
      <label htmlFor="jump" className="lab" style={{ position: 'absolute', left: '-9999px' }}>Jump to section</label>
      <select id="jump" value={active} onChange={(e) => document.getElementById(e.target.value)?.scrollIntoView()}>
        {NAV.flatMap((g) => g.items).map(([id, label]) => <option key={id} value={id}>{label}</option>)}
      </select>
    </div>
  );
}
