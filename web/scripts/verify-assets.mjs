// After `next build`, prove every brand asset in out/assets is byte-identical to the brand repo source.
import { readdirSync, statSync, readFileSync, existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join, dirname, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const web = join(dirname(fileURLToPath(import.meta.url)), '..');
const src = join(web, '..', 'identity', 'assets');
const out = join(web, 'out', 'assets');

const walk = (d) => readdirSync(d).flatMap((f) => (statSync(join(d, f)).isDirectory() ? walk(join(d, f)) : [join(d, f)]));
const sha = (p) => createHash('sha256').update(readFileSync(p)).digest('hex');

let bad = 0;
const files = walk(src);
for (const f of files) {
  const rel = relative(src, f), o = join(out, rel);
  if (!existsSync(o)) { console.error(`missing  ${rel}`); bad++; continue; }
  if (sha(f) !== sha(o)) { console.error(`changed  ${rel}`); bad++; }
}
if (bad) { console.error(`verify-assets: ${bad} of ${files.length} assets differ from the brand repo`); process.exit(1); }
console.log(`verify-assets: all ${files.length} assets byte-identical to identity/assets`);
