// After `next build`, prove every shipped brand asset is byte-identical to the brand repo source.
import { readFileSync, existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
const site = join(dirname(fileURLToPath(import.meta.url)), '..');
const src = join(site, '..', 'identity', 'assets'), out = join(site, 'out', 'assets');
const FILES = readFileSync(join(site, 'scripts', 'sync-assets.mjs'), 'utf8').match(/'[a-z0-9]+\/[^']+\.(svg|jpg|png|mp4)'/g).map((s) => s.slice(1, -1));
const sha = (p) => createHash('sha256').update(readFileSync(p)).digest('hex');
let bad = 0;
for (const f of FILES) { const o = join(out, f); if (!existsSync(o) || sha(o) !== sha(join(src, f))) { console.error('differs', f); bad++; } }
if (bad) process.exit(1);
console.log(`verify-assets: all ${FILES.length} assets byte-identical to identity/assets`);
