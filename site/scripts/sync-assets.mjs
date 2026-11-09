// Pull the brand assets this site uses from the brand repo, byte for byte (source of truth: ../identity).
// Runs before `dev` and `build`; only the files listed here are shipped.
import { cpSync, rmSync, mkdirSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const site = join(dirname(fileURLToPath(import.meta.url)), '..');
const assets = join(site, '..', 'identity', 'assets');
export const FILES = [
  'logo/primary-charcoal.svg', 'logo/primary-white-dose.svg', 'logo/mark-charcoal.svg', 'logo/mark-white-dose.svg', 'logo/app-icon.svg',
  'render/facility-facade.jpg', 'render/facility-corridor.jpg', 'render/asset-tablets.jpg', 'render/asset-capsule-dark.jpg',
  'render/asset-capsule-light.jpg', 'render/asset-mark-dark.jpg', 'render/asset-mark-light.jpg', 'render/asset-tubes.jpg', 'render/asset-pack.jpg',
  '3d/flow-dark.jpg', '3d/flow-light.jpg', '3d/blob-deep.jpg',
  'motion/flow.mp4', 'motion/flow.jpg',
];
const out = join(site, 'public', 'assets');
rmSync(out, { recursive: true, force: true });
for (const f of FILES) {
  const s = join(assets, f); if (!existsSync(s)) { console.error(`sync-assets: missing ${s}`); process.exit(1); }
  mkdirSync(dirname(join(out, f)), { recursive: true }); cpSync(s, join(out, f), { preserveTimestamps: true });
}
const gen = join(site, 'lib', 'generated'); rmSync(gen, { recursive: true, force: true }); mkdirSync(gen, { recursive: true });
cpSync(join(site, '..', 'identity', 'render', 'scenes.js'), join(gen, 'scenes.js'));
console.log(`sync-assets: ${FILES.length} brand assets + scene library`);
