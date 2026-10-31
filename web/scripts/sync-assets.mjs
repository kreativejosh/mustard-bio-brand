// Pull brand assets from the brand repo into the Next.js app, byte for byte.
// Source of truth: ../identity/assets (written by the render pipeline, e.g. identity/blender/to_site.py)
// and ../identity/render/scenes.js (the Three.js scene library). Runs before `dev` and `build`.
import { cpSync, rmSync, mkdirSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const web = join(dirname(fileURLToPath(import.meta.url)), '..');
const identity = join(web, '..', 'identity');

const copies = [
  [join(identity, 'assets'), join(web, 'public', 'assets')],
  [join(identity, 'render', 'scenes.js'), join(web, 'lib', 'generated', 'scenes.js')],
];

const count = (p) => statSync(p).isDirectory() ? readdirSync(p).reduce((n, f) => n + count(join(p, f)), 0) : 1;

for (const [src, dest] of copies) {
  if (!existsSync(src)) { console.error(`sync-assets: missing source ${src}`); process.exit(1); }
  rmSync(dest, { recursive: true, force: true });   // drop stale files so removed assets disappear too
  mkdirSync(dirname(dest), { recursive: true });
  cpSync(src, dest, { recursive: true, dereference: true, preserveTimestamps: true });
  console.log(`sync-assets: ${count(dest)} file(s) ${src.replace(web + '/', '')} -> ${dest.replace(web + '/', '')}`);
}
