'use client';
// Live WebGL: the hero flow shader and the drag-to-rotate 3D asset viewer.
// Scenes come from the brand repo's scene library (identity/render/scenes.js), synced into lib/generated/.
import { useEffect, useRef, useState } from 'react';

const reduceMotion = () => typeof window !== 'undefined' && matchMedia('(prefers-reduced-motion: reduce)').matches;

export function HeroCanvas() {
  const ref = useRef<HTMLCanvasElement>(null);
  useEffect(() => {
    let raf = 0, alive = true, cleanup = () => {};
    (async () => {
      const THREE = await import('three');
      const SCENES: any = (await import('@/lib/generated/scenes.js')).SCENES; // untyped JS from the brand repo
      const cv = ref.current; if (!cv || !alive) return;
      const r = new THREE.WebGLRenderer({ canvas: cv, antialias: false });
      r.setPixelRatio(Math.min(devicePixelRatio, 1.5)); r.outputColorSpace = THREE.SRGBColorSpace;
      let S: any;
      const size = () => { const b = cv.parentElement!.getBoundingClientRect(); r.setSize(b.width, b.height, false); S = SCENES.flow({ aspect: b.width / b.height }); };
      size(); addEventListener('resize', size);
      let vis = true; const io = new IntersectionObserver((e) => { vis = e[0].isIntersecting; }); io.observe(cv);
      const reduce = reduceMotion(); const t0 = performance.now();
      const loop = () => { if (vis) { S.update(reduce ? 3 : 3 + (performance.now() - t0) / 1000); r.render(S.scene, S.camera); } if (!reduce && alive) raf = requestAnimationFrame(loop); };
      loop();
      cleanup = () => { removeEventListener('resize', size); io.disconnect(); r.dispose(); };
    })();
    return () => { alive = false; cancelAnimationFrame(raf); cleanup(); };
  }, []);
  return <canvas ref={ref} aria-hidden="true" />;
}

const MODELS: [scene: string, label: string, variant: string | null][] = [
  ['capsule', 'Capsule', 'dark'], ['mark', 'Glass mark', null], ['helix', 'Molecule', null], ['blob', 'Metaball', 'lime'], ['tubes', 'Test tubes', null], ['flask', 'Flask', null],
];

export function Viewer3D() {
  const ref = useRef<HTMLCanvasElement>(null);
  const [cur, setCur] = useState(0);
  const api = useRef<{ build: (i: number) => void } | null>(null);
  useEffect(() => {
    let raf = 0, alive = true, cleanup = () => {};
    (async () => {
      const THREE = await import('three');
      const SCENES: any = (await import('@/lib/generated/scenes.js')).SCENES; // untyped JS from the brand repo
      const cv = ref.current; if (!cv || !alive) return;
      const r = new THREE.WebGLRenderer({ canvas: cv, antialias: true });
      r.setPixelRatio(Math.min(devicePixelRatio, 1.5)); r.toneMapping = THREE.ACESFilmicToneMapping; r.outputColorSpace = THREE.SRGBColorSpace;
      let S: any = null, idx = 0, drag: number[] | null = null, rotY = 0, rotX = 0, vis = false; const t0 = performance.now();
      const build = (i: number) => {
        idx = i; const b = cv.getBoundingClientRect(); r.setSize(b.width, b.height, false);
        S = SCENES[MODELS[i][0]]({ renderer: r, aspect: b.width / b.height, variant: MODELS[i][2] }); rotY = rotX = 0;
      };
      api.current = { build };
      const down = (e: PointerEvent) => { drag = [e.clientX, e.clientY, rotY, rotX]; cv.setPointerCapture(e.pointerId); cv.style.cursor = 'grabbing'; };
      const move = (e: PointerEvent) => { if (drag) { rotY = drag[2] + (e.clientX - drag[0]) * 0.01; rotX = Math.max(-0.6, Math.min(0.6, drag[3] + (e.clientY - drag[1]) * 0.006)); } };
      const up = () => { drag = null; cv.style.cursor = 'grab'; };
      const resize = () => { if (S) build(idx); };
      cv.addEventListener('pointerdown', down); cv.addEventListener('pointermove', move); cv.addEventListener('pointerup', up); addEventListener('resize', resize);
      const io = new IntersectionObserver((e) => { vis = e[0].isIntersecting; if (vis && !S) build(0); }); io.observe(cv);
      const reduce = reduceMotion();
      const loop = () => {
        if (vis && S) { S.update?.(reduce ? 1.2 : (performance.now() - t0) / 1000); S.scene.rotation.y = rotY; S.scene.rotation.x = rotX; r.render(S.scene, S.camera); }
        if (alive) raf = requestAnimationFrame(loop);
      };
      loop();
      cleanup = () => { cv.removeEventListener('pointerdown', down); cv.removeEventListener('pointermove', move); cv.removeEventListener('pointerup', up); removeEventListener('resize', resize); io.disconnect(); r.dispose(); };
    })();
    return () => { alive = false; cancelAnimationFrame(raf); cleanup(); };
  }, []);
  return (
    <div className="viewer">
      <canvas ref={ref} aria-label="Interactive 3D asset viewer" />
      <span className="tag w hint">Live · drag to rotate</span>
      <div className="ui">
        {MODELS.map((m, i) => (
          <button key={m[0]} className={`mini${cur === i ? ' on' : ''}`} onClick={() => { setCur(i); api.current?.build(i); }}>{m[1]}</button>
        ))}
      </div>
    </div>
  );
}
