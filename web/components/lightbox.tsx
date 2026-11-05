'use client';
// Click any figure image to view it full size; click the image again for 100% zoom. Esc or click outside closes.
// Images can name a larger file in data-full (8K stationery, 8K mockups): the preview shows at once and is
// swapped for the full file as soon as it has loaded, so zooming never shows an upscaled preview.
// Also pauses autoplay loops for people who prefer reduced motion.
import { useEffect, useState } from 'react';

export function Lightbox() {
  const [img, setImg] = useState<{ src: string; full: string; alt: string } | null>(null);
  const [ready, setReady] = useState(false);
  const [zoom, setZoom] = useState(false);
  useEffect(() => {
    const open = (e: MouseEvent) => {
      const t = e.target as HTMLElement;
      if (t instanceof HTMLImageElement && t.matches('.fig img, .st-img img')) {
        const src = t.currentSrc || t.src;
        setImg({ src, full: t.dataset.full || src, alt: t.alt }); setReady(!t.dataset.full); setZoom(false);
      }
    };
    const key = (e: KeyboardEvent) => { if (e.key === 'Escape') setImg(null); };
    document.addEventListener('click', open); addEventListener('keydown', key);
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) document.querySelectorAll('video').forEach((v) => { v.removeAttribute('autoplay'); v.pause(); });
    return () => { document.removeEventListener('click', open); removeEventListener('keydown', key); };
  }, []);
  useEffect(() => {
    if (!img || ready) return;
    let live = true; const pre = new Image();
    pre.onload = () => { if (live) setReady(true); };
    pre.src = img.full;
    return () => { live = false; };
  }, [img, ready]);
  if (!img) return null;
  return (
    <div id="lb" className={zoom ? 'full' : undefined} onClick={() => setImg(null)}>
      <img src={ready ? img.full : img.src} alt={img.alt} decoding="async" onClick={(e) => { e.stopPropagation(); setZoom((z) => !z); }} />
      {!ready && <span className="lab lb-load">Loading full resolution…</span>}
      <button className="mini" type="button">Close</button>
    </div>
  );
}
