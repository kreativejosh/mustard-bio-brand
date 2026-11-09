'use client';
// Header: logo, page links, partner CTA. Turns solid once you scroll off the hero; a hairline scale rule under it
// fills with reading progress. On small screens the links fold into a full-height menu.
import Link from '@/components/link';
import { usePathname } from 'next/navigation';
import { useEffect, useState } from 'react';
import { NAV, HOME } from '@/lib/copy';
import { Arrow } from './ui';

export function Nav() {
  // Normalised so it also works when pages are served as flat .html files (static preview)
  const seg = (usePathname() || '/').split('/').filter(Boolean).pop()?.replace(/\.html$/, '') || '';
  const path = !seg || seg === 'index' ? '/' : '/' + seg;
  const [solid, setSolid] = useState(false);
  const [open, setOpen] = useState(false);
  const dark = path === '/' || path === '/technology';  // pages whose hero is charcoal
  useEffect(() => {
    const on = () => setSolid(scrollY > 40);
    on(); addEventListener('scroll', on, { passive: true }); return () => removeEventListener('scroll', on);
  }, []);
  useEffect(() => { setOpen(false); }, [path]);
  useEffect(() => { document.body.style.overflow = open ? 'hidden' : ''; }, [open]);
  const onDark = dark && !solid && !open;
  return (
    <header className={`hdr${solid ? ' solid' : ''}${onDark ? ' on-dark' : ''}${open ? ' open' : ''}`}>
      <div className="hdr-in">
        <Link href="/" className="logo" aria-label="Mustard Bio home">
          <img src={onDark ? '/assets/logo/primary-white-dose.svg' : '/assets/logo/primary-charcoal.svg'} alt="Mustard Bio" width={172} height={29} />
        </Link>
        <nav className="links" aria-label="Main">
          {NAV.map((n) => <Link key={n.href} href={n.href} className={path === n.href ? 'on' : undefined} aria-current={path === n.href ? 'page' : undefined}>{n.label}</Link>)}
        </nav>
        <Link href="/about#contact" className="hdr-cta"><span>{HOME.hero.secondary}</span><Arrow /></Link>
        <button className="burger" aria-label={open ? 'Close menu' : 'Open menu'} aria-expanded={open} onClick={() => setOpen((o) => !o)}><span /><span /></button>
      </div>
      <div className="prog" aria-hidden="true"><i /></div>
      <div className="sheet" hidden={!open}>
        {NAV.map((n, i) => <Link key={n.href} href={n.href} className={path === n.href ? 'on' : undefined}><em>0{i + 1}</em>{n.label}</Link>)}
        <Link href="/about#contact" className="sheet-cta">{HOME.hero.secondary}<Arrow /></Link>
      </div>
    </header>
  );
}
