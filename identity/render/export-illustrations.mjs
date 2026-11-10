// Export the illustration pack (web/lib/brand.ts ILLO, 114 grid, 1 px) as SVG files into identity/assets/illustrations/.
// Run: node --experimental-strip-types identity/render/export-illustrations.mjs
import { mkdirSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
const here = dirname(fileURLToPath(import.meta.url));
const { ILLO } = await import(join(here, '..', '..', 'web', 'lib', 'brand.ts'));
const out = join(here, '..', 'assets', 'illustrations'); mkdirSync(out, { recursive: true });
for (const [name, fn] of Object.entries(ILLO)) {
  // currentColor stroke so the file takes any brand colour; same stroke settings as the brand site (web/components/brand-static.tsx)
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 114 114" fill="none" stroke="currentColor" stroke-width="1" stroke-miterlimit="10"><title>Mustard Bio illustration: ${name}</title>${fn()}</svg>\n`;
  writeFileSync(join(out, `${name}.svg`), svg);
  console.log('wrote', `${name}.svg`);
}
