'use client';
// Click any figure image to view it full size; click the image again for 100% zoom. Esc or click outside closes.
// Also pauses autoplay loops for people who prefer reduced motion.
import { useEffect, useState } from 'react';

export function Lightbox() {
  const [img, setImg] = useState<{ src: string; alt: string } | null>(null);
  const [full, setFull] = useState(false);
  useEffect(() => {
    const open = (e: MouseEvent) => {
      const t = e.target as HTMLElement;
      if (t instanceof HTMLImageElement && t.matches('.fig img, .st-img img')) { setImg({ src: t.currentSrc || t.src, alt: t.alt }); setFull(false); }
    };
    const key = (e: KeyboardEvent) => { if (e.key === 'Escape') setImg(null); };
    document.addEventListener('click', open); addEventListener('keydown', key);
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) document.querySelectorAll('video').forEach((v) => { v.removeAttribute('autoplay'); v.pause(); });
    return () => { document.removeEventListener('click', open); removeEventListener('keydown', key); };
  }, []);
  if (!img) return null;
  return (
    <div id="lb" className={full ? 'full' : undefined} onClick={() => setImg(null)}>
      <img src={img.src} alt={img.alt} onClick={(e) => { e.stopPropagation(); setFull((f) => !f); }} />
      <button className="mini" type="button">Close</button>
    </div>
  );
}
