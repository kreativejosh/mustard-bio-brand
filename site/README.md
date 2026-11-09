# Mustard Bio website

Marketing site: Home, Manufacturing, Technology, About (Vision is a section of About). Next.js static export.

- Copy: `lib/copy.ts`, verbatim from `../brief/website-copy.md`. Do not reword.
- Brand: tokens from `../design-system/tokens.css`, IBM Plex via next/font, assets synced byte for byte from `../identity/assets` (`npm run sync`, listed in `scripts/sync-assets.mjs`; `postbuild` verifies checksums). The hero shader is the `flow` scene from `../identity/render/scenes.js`.
- Contact form: set `NEXT_PUBLIC_CONTACT_ENDPOINT` (form service that accepts JSON POST) or `NEXT_PUBLIC_CONTACT_EMAIL` (opens the visitor's mail app) at build time.

```bash
npm ci
npm run dev      # http://localhost:3000
npm run build    # static site in out/
```

Deploy on Vercel as its own project: Root Directory `site`, framework Next.js, and keep "Include files outside the root directory" on (the build reads `../identity`).
