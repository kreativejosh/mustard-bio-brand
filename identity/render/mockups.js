// Physical mockups: artwork PNGs (art/*.png) wrapped onto modelled objects, lit like a product studio.
import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { C, studioEnv, gradientTex, glass, solid, keyLight, contact } from './scenes.js';

const loader = new THREE.TextureLoader();
const tex = async (name, o = {}) => {
  const t = await loader.loadAsync(`art/${name}.png`); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
  if (o.rot) { t.center.set(0.5, 0.5); t.rotation = o.rot; }
  if (o.repeat) { t.wrapS = THREE.RepeatWrapping; t.repeat.set(o.repeat, 1); }
  if (o.flipX) { t.wrapS = THREE.RepeatWrapping; t.repeat.x = -1; }
  return t;
};
const paper = (map, o = {}) => new THREE.MeshPhysicalMaterial({ map, roughness: o.roughness ?? 0.7, clearcoat: o.clearcoat ?? 0, clearcoatRoughness: 0.3, sheen: o.sheen ?? 0.2, envMapIntensity: o.env ?? 0.7, metalness: o.metalness ?? 0 });

function studio(renderer, bg, { floorColor = C.stone, floor = true, light = [-3, 9, 5], size = 6, intensity = 2.6, floorEnv = 0.35 } = {}) {
  const scene = new THREE.Scene(); scene.environment = studioEnv(renderer);
  scene.background = typeof bg === 'string' ? new THREE.Color(bg) : bg;
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  if (floor) { const f = new THREE.Mesh(new THREE.PlaneGeometry(60, 60), solid(floorColor, { roughness: 0.92, clearcoat: 0, env: floorEnv })); f.rotation.x = -Math.PI / 2; f.receiveShadow = true; scene.add(f); }
  const l = keyLight(scene, light, intensity, size); l.shadow.radius = 6;
  return scene;
}
const cast = o => { o.traverse(m => { if (m.isMesh) { m.castShadow = true; m.receiveShadow = true; } }); return o; };
// box with per-face materials: order +x,-x,+y,-y,+z,-z
const faced = (w, h, d, mats) => new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mats);
const edge = (c = '#ffffff') => solid(c, { roughness: 0.8, clearcoat: 0, env: 0.6 });

export const SCENES = {

  async cards({ renderer, aspect }) {
    const scene = studio(renderer, C.stone, { light: [-4, 10, 3], size: 4 });
    const [f, b] = await Promise.all([tex('card-front'), tex('card-back')]);
    const W = 1.4, H = W * 680 / 1050, T = 0.008;
    const card = (top, col) => cast(faced(W, T, H, [edge(col), edge(col), paper(top, { roughness: 0.55 }), edge(col), edge(col), edge(col)]));
    const mk = (map, col, x, z, ry, y = T / 2) => { const c = card(map, col); c.position.set(x, y, z); c.rotation.y = ry; scene.add(c); return c; };
    mk(b, C.offwhite, 0.75, 0.25, -0.3); mk(f, C.charcoal, -0.35, -0.05, 0.18);
            // stack
    for (let i = 0; i < 6; i++) mk(f, C.charcoal, -1.45, -0.65 - 0, 0.6 + i * 0.012, T / 2 + i * T);
    const cam = new THREE.PerspectiveCamera(30, aspect, 0.1, 100); cam.position.set(0.1, 4.2, 3.4); cam.lookAt(-0.1, 0, 0);
    return { scene, camera: cam };
  },

  async print({ renderer, aspect }) {
    const scene = studio(renderer, C.g2, { floorColor: C.g2, light: [-5, 10, 4], size: 5 });
    const [fl, lh, nb, cf, cb] = await Promise.all([tex('flyer'), tex('letterhead'), tex('notebook'), tex('card-front'), tex('card-back')]);
    const sheet = (map, w, h, x, z, ry, y = 0.002, t = 0.003, col = '#fff') => { const m = cast(faced(w, t, h, [edge(col), edge(col), paper(map), edge(col), edge(col), edge(col)])); m.position.set(x, y, z); m.rotation.y = ry; scene.add(m); return m; };
    sheet(lh, 2.1, 2.1 * 1.414, -1.25, 0.1, 0.12);
    sheet(fl, 2.1, 2.1 * 1.414, 0.85, -0.05, -0.1, 0.006);
    sheet(nb, 1.5, 1.5 * 1240 / 900, 2.75, 0.6, 0.28, 0.04, 0.07, C.charcoal);
    sheet(cf, 0.85, 0.85 * 680 / 1050, -0.2, 1.75, -0.3, 0.012, 0.006, C.charcoal);
    sheet(cb, 0.85, 0.85 * 680 / 1050, 0.55, 1.95, 0.15, 0.012, 0.006, C.offwhite);
    // pen
    const pen = cast(new THREE.Mesh(new THREE.CapsuleGeometry(0.035, 1.3, 8, 24), solid(C.charcoal, { roughness: 0.25, clearcoat: 1 }))); pen.rotation.z = Math.PI / 2; pen.rotation.y = 0.5; pen.position.set(2.4, 0.035, -1.3); scene.add(pen);
    const cam = new THREE.PerspectiveCamera(30, aspect, 0.1, 100); cam.position.set(0.5, 7.8, 3.2); cam.lookAt(0.6, 0, 0.1);
    return { scene, camera: cam };
  },

  async billboard({ renderer, aspect }) {
    const scene = new THREE.Scene(); scene.environment = studioEnv(renderer);
    scene.background = gradientTex([[0, '#b8c6c3'], [0.55, '#e6ebe7'], [1, '#f4f4f0']], { angle: 90 });
    renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    const ground = new THREE.Mesh(new THREE.PlaneGeometry(200, 200), solid('#a9ae9f', { roughness: 1, clearcoat: 0, env: 0.3 })); ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; scene.add(ground);
    const sun = keyLight(scene, [12, 18, 14], 3, 14); sun.shadow.radius = 3;
    const art = await tex('billboard');
    const g = new THREE.Group(); scene.add(g);
    const W = 9, H = 3;
    const frame = cast(new THREE.Mesh(new RoundedBoxGeometry(W + 0.24, H + 0.24, 0.3, 3, 0.04), solid('#2a3536', { roughness: 0.5 }))); g.add(frame);
    const face = new THREE.Mesh(new THREE.PlaneGeometry(W, H), new THREE.MeshPhysicalMaterial({ map: art, roughness: 0.5, envMapIntensity: 0.4 })); face.position.z = 0.152; g.add(face);
    [-2.6, 2.6].forEach(x => { const p = cast(new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.2, 5, 24), solid('#5d6766', { roughness: 0.5, metalness: 0.6 }))); p.position.set(x, -H / 2 - 2.5, -0.3); g.add(p); });
    const cat = cast(new THREE.Mesh(new THREE.BoxGeometry(W, 0.06, 0.8), solid('#5d6766', { metalness: 0.6, roughness: 0.4 }))); cat.position.set(0, -H / 2 - 0.15, 0.35); g.add(cat);
    for (let i = 0; i < 4; i++) { const lmp = cast(new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.08, 0.16), solid(C.charcoal))); lmp.position.set(-3.4 + i * 2.27, H / 2 + 0.35, 0.6); g.add(lmp); const arm = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.04, 0.7), solid(C.charcoal)); arm.position.set(-3.4 + i * 2.27, H / 2 + 0.33, 0.3); g.add(arm); }
    g.position.y = H / 2 + 5.1; g.rotation.y = -0.38;
    // low hedges for scale
    for (let i = 0; i < 26; i++) { const b = cast(new THREE.Mesh(new THREE.SphereGeometry(0.6 + Math.random() * 0.5, 16, 12), solid(['#7c8c6e', '#6b7c60', '#8a9a7a'][i % 3], { roughness: 1, clearcoat: 0, env: 0.4 }))); b.scale.y = 0.7; b.position.set(-14 + i * 1.1 + Math.random(), 0.3, -3 - Math.random() * 2); scene.add(b); }
    const cam = new THREE.PerspectiveCamera(32, aspect, 0.1, 300); cam.position.set(-3.5, 1.7, 15.5); cam.lookAt(0.3, 5.6, 0);
    return { scene, camera: cam };
  },

  async bottles({ renderer, aspect }) {
    const scene = studio(renderer, gradientTex([[0, '#ffffff'], [0.6, C.stone], [1, C.sage]], { type: 'radial', cx: 0.5, cy: 0.35, r: 0.9 }), { floorColor: C.stone, light: [-4, 9, 6], size: 4 });
    const [dk, lt] = await Promise.all([tex('bottle-wrap'), tex('bottle-wrap-light')]);
    const r = 0.38, h = 2.2;
    const prof = []; // body profile with rounded base & shoulder; v along profile
    for (let i = 0; i <= 6; i++) { const a = -Math.PI / 2 + (i / 6) * Math.PI / 2; prof.push(new THREE.Vector2(r - 0.06 + Math.cos(a) * 0.06, 0.06 + Math.sin(a) * 0.06)); }
    prof.push(new THREE.Vector2(r, h - 0.25));
    for (let i = 1; i <= 8; i++) { const a = (i / 8) * Math.PI / 2; prof.push(new THREE.Vector2(0.24 + (r - 0.24) * Math.cos(a), h - 0.25 + 0.2 * Math.sin(a))); }
    prof.push(new THREE.Vector2(0.24, h));
    const bottle = (map, capCol, x, z, ry) => {
      const g = new THREE.Group();
      const lg = new THREE.LatheGeometry(prof, 96); { const P = lg.attributes.position, U = lg.attributes.uv; for (let i = 0; i < P.count; i++) U.setY(i, P.getY(i) / h); }
      const body = new THREE.Mesh(lg, new THREE.MeshPhysicalMaterial({ map, roughness: 0.42, metalness: 0.15, clearcoat: 0.5, clearcoatRoughness: 0.35, envMapIntensity: 0.9 }));
      g.add(body);
      const neck = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.25, 0.1, 64), solid('#c7cccb', { metalness: 1, roughness: 0.25 })); neck.position.y = h + 0.05; g.add(neck);
      const cap = new THREE.Mesh(new THREE.CylinderGeometry(0.27, 0.27, 0.34, 64), solid(capCol, { roughness: 0.5, clearcoat: 0.3 })); cap.position.y = h + 0.27; g.add(cap);
      const loop = new THREE.Mesh(new THREE.TorusGeometry(0.15, 0.04, 16, 48), solid(capCol, { roughness: 0.5 })); loop.position.y = h + 0.55; g.add(loop);
      g.position.set(x, 0, z); g.rotation.y = ry; scene.add(cast(g)); return g;
    };
    bottle(dk, C.lime, -0.55, 0, Math.PI + 0.12);
    bottle(lt, C.charcoal, 0.6, 0.45, Math.PI - 0.12);
    const cam = new THREE.PerspectiveCamera(30, aspect, 0.1, 100); cam.position.set(0, 2.2, 7.4); cam.lookAt(0, 1.25, 0);
    return { scene, camera: cam };
  },

  async bands({ renderer, aspect }) {
    const scene = studio(renderer, C.offwhite, { floorColor: C.offwhite, light: [-3, 10, 4], size: 3 });
    const [lm, ik] = await Promise.all([tex('band-lime'), tex('band-ink')]);
    [lm, ik].forEach(t => { t.wrapS = THREE.RepeatWrapping; });
    const R = 0.62, w = 0.2, th = 0.05;
    const prof = []; // rounded rect cross-section
    const pts = [[R, -w / 2], [R + th, -w / 2], [R + th, w / 2], [R, w / 2]];
    for (let i = 0; i <= 10; i++) { const t = i / 10; prof.push(new THREE.Vector2(R + th, -w / 2 + w * t)); }
    const outer = new THREE.LatheGeometry(prof, 128);
    const band = (map, col, x, z, rx, ry, y) => {
      const g = new THREE.Group();
      const o = new THREE.Mesh(outer, new THREE.MeshPhysicalMaterial({ map, roughness: 0.6, sheen: 0.6, sheenColor: new THREE.Color('#ffffff'), envMapIntensity: 0.6 }));
      const inner = new THREE.Mesh(new THREE.CylinderGeometry(R, R, w, 128, 1, true), new THREE.MeshPhysicalMaterial({ color: col, roughness: 0.7, side: THREE.BackSide, envMapIntensity: 0.6 }));
      const lip = (yy) => { const m = new THREE.Mesh(new THREE.RingGeometry(R, R + th, 128), new THREE.MeshPhysicalMaterial({ color: col, roughness: 0.65, side: THREE.DoubleSide, envMapIntensity: 0.6 })); m.rotation.x = -Math.PI / 2; m.position.y = yy; return m; };
      g.add(o, inner, lip(w / 2), lip(-w / 2));
      g.position.set(x, y, z); g.rotation.set(rx, ry, 0); scene.add(cast(g)); return g;
    };
    band(lm, C.lime, -0.55, 0.1, 0, 0, w / 2);
    band(ik, C.charcoal, 0.75, -0.2, 0.18, 0.6, R * 0.95);
    band(lm, C.lime, 0.95, 0.85, 0, 1.2, w / 2);
    const cam = new THREE.PerspectiveCamera(30, aspect, 0.1, 100); cam.position.set(0, 3.6, 4.2); cam.lookAt(0.15, 0.2, 0.1);
    return { scene, camera: cam };
  },

  async pack({ renderer, aspect }) {
    const scene = studio(renderer, gradientTex([[0, '#ffffff'], [0.7, C.offwhite], [1, C.g2]], { type: 'radial', cx: 0.5, cy: 0.3, r: 0.9 }), { floorColor: C.offwhite, light: [-4, 9, 7], size: 4 });
    const [fr, sd, en, tp, foil] = await Promise.all([tex('carton-front'), tex('carton-side'), tex('carton-end', { rot: Math.PI / 2 }), tex('carton-top'), tex('blister-foil')]);
    const W = 2.0, H = 1.24, D = 0.48;
    const box = cast(faced(W, H, D, [paper(en, { roughness: 0.4, clearcoat: 0.4 }), paper(en, { roughness: 0.4, clearcoat: 0.4 }), paper(sd, { roughness: 0.4, clearcoat: 0.4 }), edge(), paper(fr, { roughness: 0.4, clearcoat: 0.4 }), paper(tp, { roughness: 0.4, clearcoat: 0.4 })]));
    box.position.set(-0.35, H / 2, -0.3); box.rotation.y = 0.32; scene.add(box);
    // second carton lying flat behind
    const box2 = cast(faced(W, H, D, [paper(en), paper(en), paper(sd), edge(), paper(fr), paper(tp)])); box2.rotation.set(-Math.PI / 2, 0, -0.5); box2.position.set(1.15, D / 2, -1.1); scene.add(box2);
    // blister
    const bl = new THREE.Group();
    const plate = cast(new THREE.Mesh(new RoundedBoxGeometry(1.9, 0.02, 0.92, 2, 0.008), new THREE.MeshPhysicalMaterial({ color: '#d9dedc', metalness: 0.9, roughness: 0.28, envMapIntensity: 1.2 }))); bl.add(plate);
    const bub = glass({ thickness: 0.04, roughness: 0.08, side: THREE.DoubleSide });
    const tabG = new THREE.CylinderGeometry(0.14, 0.14, 0.07, 48);
    for (let r = 0; r < 2; r++) for (let c = 0; c < 5; c++) {
      const x = -0.72 + c * 0.36, z = -0.2 + r * 0.4;
      const b = new THREE.Mesh(new THREE.SphereGeometry(0.17, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2), bub); b.scale.y = 0.55; b.position.set(x, 0.01, z); bl.add(b);
      const t = cast(new THREE.Mesh(tabG, solid(r === 1 && c === 4 ? C.offwhite : '#ffffff', { roughness: 0.6, clearcoat: 0.1 }))); t.position.set(x, 0.045, z); if (!(r === 1 && c === 4)) bl.add(t);
    }
    bl.position.set(0.55, 0.012, 0.85); bl.rotation.y = -0.25; scene.add(bl);
    // flipped blister showing printed foil
    const back = cast(faced(1.9, 0.02, 0.92, [edge('#cfd4d2'), edge('#cfd4d2'), paper(foil, { metalness: 0.6, roughness: 0.3, env: 1 }), edge(), edge('#cfd4d2'), edge('#cfd4d2')]));
    back.position.set(-1.5, 0.012, 1.0); back.rotation.y = 0.35; scene.add(back);
    const loose = [[1.8, 1.55], [1.55, 1.75], [-0.4, 1.55]];
    loose.forEach(([x, z]) => { const t = cast(new THREE.Mesh(tabG, solid('#ffffff', { roughness: 0.6 }))); t.position.set(x, 0.035, z); scene.add(t); });
    const cam = new THREE.PerspectiveCamera(30, aspect, 0.1, 100); cam.position.set(0.4, 3.6, 6.2); cam.lookAt(0, 0.45, 0.2);
    return { scene, camera: cam };
  },

  async badge({ renderer, aspect }) {
    const scene = studio(renderer, C.stone, { floorColor: C.stone, light: [-3, 10, 5], size: 3 });
    const [bd, strap] = await Promise.all([tex('badge'), tex('band-lime')]);
    strap.wrapS = THREE.RepeatWrapping;
    const W = 0.86, H = W * 1000 / 640;
    const card = cast(faced(W, 0.01, H, [edge(), edge(), paper(bd, { roughness: 0.3, clearcoat: 0.8 }), edge(), edge(), edge()])); card.position.set(0.2, 0.012, 0.25); card.rotation.y = -0.18; scene.add(card);
    // holder clip
    const clip = cast(new THREE.Mesh(new RoundedBoxGeometry(0.22, 0.03, 0.12, 2, 0.01), solid('#cfd4d2', { metalness: 0.9, roughness: 0.25 }))); clip.position.set(0.2 + Math.sin(-0.18) * -H / 2 * 0.0 + 0.11, 0.03, 0.25 - H / 2 - 0.02); scene.add(clip);
    // lanyard ribbon: flat strip following a loose curve on the floor
    const curve = new THREE.CatmullRomCurve3([[0.3, 0.02, -0.55], [0.6, 0.02, -1.2], [0.2, 0.02, -1.9], [-0.9, 0.02, -1.8], [-1.4, 0.02, -0.9], [-1.1, 0.02, 0.2], [-0.7, 0.02, 0.6], [-0.1, 0.02, -0.5]].map(p => new THREE.Vector3(...p)));
    const N = 300, wd = 0.11, pos = [], uv = [], idx = [];
    for (let i = 0; i <= N; i++) { const t = i / N, p = curve.getPointAt(t), tg = curve.getTangentAt(t); const n = new THREE.Vector3(-tg.z, 0, tg.x).normalize().multiplyScalar(wd / 2);
      pos.push(p.x + n.x, p.y + 0.002 * Math.sin(i), p.z + n.z, p.x - n.x, p.y, p.z - n.z); uv.push(t * 6, 1, t * 6, 0); if (i < N) { const a = i * 2; idx.push(a, a + 1, a + 2, a + 1, a + 3, a + 2); } }
    const rg = new THREE.BufferGeometry(); rg.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); rg.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2)); rg.setIndex(idx); rg.computeVertexNormals();
    const rib = new THREE.Mesh(rg, new THREE.MeshPhysicalMaterial({ map: strap, roughness: 0.7, sheen: 0.5, side: THREE.DoubleSide, envMapIntensity: 0.6 })); rib.receiveShadow = true; scene.add(rib);
    const cam = new THREE.PerspectiveCamera(30, aspect, 0.1, 100); cam.position.set(-0.2, 4.6, 1.9); cam.lookAt(-0.2, 0, -0.45);
    return { scene, camera: cam };
  },

  async facade({ renderer, aspect }) {
    const scene = new THREE.Scene(); scene.environment = studioEnv(renderer);
    scene.background = gradientTex([[0, '#aebdba'], [0.6, '#dfe5e1'], [1, '#f2f2ee']], { angle: 90 });
    renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    const ground = new THREE.Mesh(new THREE.PlaneGeometry(300, 300), solid('#b9bcb3', { roughness: 1, clearcoat: 0, env: 0.3 })); ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; scene.add(ground);
    const sun = keyLight(scene, [-20, 25, 18], 3.2, 20); sun.shadow.radius = 2;
    const sign = await tex('facade-sign');
    const b = new THREE.Group(); scene.add(b);
    const L = 30, Hh = 8, D = 14;
    const shell = cast(new THREE.Mesh(new THREE.BoxGeometry(L, Hh, D), solid('#e9ebe7', { roughness: 0.8, clearcoat: 0 }))); shell.position.y = Hh / 2; b.add(shell);
    // ribbed charcoal cladding on upper band
    const rib = solid(C.charcoal, { roughness: 0.55, metalness: 0.3 });
    for (let i = 0; i < 150; i++) { const r = cast(new THREE.Mesh(new THREE.BoxGeometry(0.1, 4.6, 0.18), rib)); r.position.set(-L / 2 + 0.1 + i * (L / 150), Hh - 2.3, D / 2 + 0.09); b.add(r); }
    const back = new THREE.Mesh(new THREE.PlaneGeometry(L, 4.6), solid('#1a2324', { roughness: 0.8 })); back.position.set(0, Hh - 2.3, D / 2 + 0.005); b.add(back);
    // glazing
    const glz = new THREE.Mesh(new THREE.PlaneGeometry(L - 6, 3.0), new THREE.MeshPhysicalMaterial({ color: '#3b4b4c', metalness: 0.2, roughness: 0.05, envMapIntensity: 1.6 })); glz.position.set(3, 1.6, D / 2 + 0.01); b.add(glz);
    for (let i = 0; i <= 12; i++) { const m = new THREE.Mesh(new THREE.BoxGeometry(0.08, 3.1, 0.08), solid('#c7cccb', { metalness: 0.8 })); m.position.set(3 - (L - 6) / 2 + i * (L - 6) / 12, 1.6, D / 2 + 0.05); b.add(m); }
    // lime soffit band
    const soff = new THREE.Mesh(new THREE.BoxGeometry(L, 0.2, 0.3), solid(C.lime, { roughness: 0.5 })); soff.position.set(0, 3.3, D / 2 + 0.15); b.add(soff);
    // sign panel
    const sp = cast(new THREE.Mesh(new THREE.BoxGeometry(12, 2.6, 0.2), [solid(C.charcoal), solid(C.charcoal), solid(C.charcoal), solid(C.charcoal), new THREE.MeshPhysicalMaterial({ map: sign, roughness: 0.5, emissive: '#ffffff', emissiveMap: sign, emissiveIntensity: 0.12 }), solid(C.charcoal)])); sp.position.set(-6.5, Hh - 2.3, D / 2 + 0.3); b.add(sp);
    // entrance canopy
    const can = cast(new THREE.Mesh(new THREE.BoxGeometry(6, 0.25, 3), solid(C.charcoal))); can.position.set(-11.5, 3.4, D / 2 + 1.5); b.add(can);
    b.rotation.y = 0.5;
    // trees
    for (let i = 0; i < 7; i++) { const t = cast(new THREE.Mesh(new THREE.SphereGeometry(1.4, 16, 12), solid(['#7c8c6e', '#6b7c60'][i % 2], { roughness: 1, clearcoat: 0, env: 0.4 }))); t.scale.y = 1.3; t.position.set(-24 + i * 7.5, 2.4, 22 - i * 3.2); scene.add(t); const tr = cast(new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.15, 1.6, 8), solid('#5a5148'))); tr.position.set(-24 + i * 7.5, 0.8, 22 - i * 3.2); scene.add(tr); }
    const cam = new THREE.PerspectiveCamera(34, aspect, 0.1, 400); cam.position.set(-14, 2.2, 32); cam.lookAt(-3, 5, 0);
    return { scene, camera: cam };
  },

  async corridor({ renderer, aspect }) {
    const scene = new THREE.Scene(); scene.environment = studioEnv(renderer); scene.background = new THREE.Color('#f2f3f0');
    renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    const wf = await tex('wayfinding');
    const floor = new THREE.Mesh(new THREE.PlaneGeometry(40, 40), new THREE.MeshPhysicalMaterial({ color: '#cfd3c4', roughness: 0.25, clearcoat: 0.8, clearcoatRoughness: 0.2, envMapIntensity: 0.6 })); floor.rotation.x = -Math.PI / 2; floor.receiveShadow = true; scene.add(floor);
    const wall = new THREE.Mesh(new THREE.PlaneGeometry(40, 6), solid('#fbfbf9', { roughness: 0.9, clearcoat: 0, env: 0.6 })); wall.position.set(0, 3, -1); wall.receiveShadow = true; scene.add(wall);
    const wall2 = new THREE.Mesh(new THREE.PlaneGeometry(20, 6), solid('#f4f5f2', { roughness: 0.9, clearcoat: 0, env: 0.6 })); wall2.rotation.y = Math.PI / 2; wall2.position.set(-4.5, 3, 6); scene.add(wall2);
    // skirting in lime line
    const sk = new THREE.Mesh(new THREE.BoxGeometry(40, 0.1, 0.02), solid(C.lime)); sk.position.set(0, 0.05, -0.99); scene.add(sk);
    const ln = new THREE.Mesh(new THREE.PlaneGeometry(40, 0.08), solid(C.lime, { roughness: 0.4 })); ln.rotation.x = -Math.PI / 2; ln.position.set(0, 0.002, 0.6); scene.add(ln);
    const sg = cast(new THREE.Mesh(new RoundedBoxGeometry(0.9, 1.2, 0.04, 2, 0.01), [solid('#fff'), solid('#fff'), solid('#fff'), solid('#fff'), new THREE.MeshPhysicalMaterial({ map: wf, roughness: 0.4, clearcoat: 0.6 }), solid('#fff')]));
    sg.position.set(0.4, 1.75, -0.97); scene.add(sg);
    // cleanroom door with vision panel
    const door = cast(new THREE.Mesh(new THREE.BoxGeometry(1.4, 2.4, 0.08), solid('#e6e9e6', { roughness: 0.4, clearcoat: 0.6 }))); door.position.set(2.4, 1.2, -0.96); scene.add(door);
    const vp = new THREE.Mesh(new THREE.PlaneGeometry(0.5, 0.7), new THREE.MeshPhysicalMaterial({ color: '#53615f', roughness: 0.05, metalness: 0.3 })); vp.position.set(2.4, 1.55, -0.91); scene.add(vp);
    const plate = new THREE.Mesh(new THREE.PlaneGeometry(0.5, 0.14), solid(C.charcoal)); plate.position.set(2.4, 2.05, -0.91); scene.add(plate);
    const bar = cast(new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 0.4, 16), solid('#c7cccb', { metalness: 1, roughness: 0.2 }))); bar.rotation.z = Math.PI / 2; bar.position.set(1.95, 1.05, -0.86); scene.add(bar);
    keyLight(scene, [3, 7, 6], 1.6, 6);
    const cl = new THREE.RectAreaLight ? null : null;
    const cam = new THREE.PerspectiveCamera(36, aspect, 0.1, 100); cam.position.set(-0.9, 1.6, 2.7); cam.lookAt(1.0, 1.5, -1);
    return { scene, camera: cam };
  },

  async mug({ renderer, aspect }) {
    const scene = studio(renderer, gradientTex([[0, '#ffffff'], [1, C.stone]], { type: 'radial', cx: 0.5, cy: 0.35, r: 0.9 }), { floorColor: C.stone, light: [-4, 8, 6], size: 3 });
    const wrap = await tex('mug-wrap');
    const mug = (x, z, ry, col) => {
      const g = new THREE.Group();
      const body = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.5, 1.0, 96, 1, true), new THREE.MeshPhysicalMaterial({ map: col ? null : wrap, color: col || '#ffffff', roughness: 0.2, clearcoat: 1, envMapIntensity: 0.9 }));
      const inside = new THREE.Mesh(new THREE.CylinderGeometry(0.46, 0.46, 0.98, 96, 1, true), solid(col ? C.lime : C.charcoal, { roughness: 0.2, clearcoat: 1 })); inside.material.side = THREE.BackSide;
      const rim = new THREE.Mesh(new THREE.RingGeometry(0.46, 0.5, 96), solid(col || '#ffffff', { roughness: 0.2, clearcoat: 1 })); rim.rotation.x = -Math.PI / 2; rim.position.y = 0.5;
      const base = new THREE.Mesh(new THREE.CircleGeometry(0.47, 64), solid(col ? C.lime : C.charcoal)); base.rotation.x = -Math.PI / 2; base.position.y = -0.47;
      const handle = new THREE.Mesh(new THREE.TorusGeometry(0.26, 0.055, 24, 64, Math.PI * 1.15), solid(col || '#ffffff', { roughness: 0.2, clearcoat: 1 })); handle.rotation.z = -Math.PI * 0.575; handle.position.set(0.5, 0, 0);
      g.add(body, inside, rim, base, handle); g.position.set(x, 0.5, z); g.rotation.y = ry; scene.add(cast(g));
    };
    mug(-0.6, 0, Math.PI / 2 - 0.12); mug(0.75, -0.5, 2.6, C.charcoal);
    const cam = new THREE.PerspectiveCamera(30, aspect, 0.1, 100); cam.position.set(0, 2.2, 5.6); cam.lookAt(0.05, 0.45, 0);
    return { scene, camera: cam };
  },
};
