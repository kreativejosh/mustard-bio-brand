# Mustard Bio website

Marketing site: Home, Manufacturing, Technology, About (Vision is a section of About). Next.js static export.

- Copy: `lib/copy.ts`, verbatim from `../brief/website-copy.md`. Do not reword.
- Brand: tokens from `../design-system/tokens.css`, IBM Plex via next/font, assets synced byte for byte from `../identity/assets` (`npm run sync`, listed in `scripts/sync-assets.mjs`; `postbuild` verifies checksums). The hero shader is the `flow` scene from `../identity/render/scenes.js`.
- Search and AI search (all generated from the verbatim copy, see `lib/seo.ts`):
  - per-page `<title>`, description, canonical URL, Open Graph and Twitter cards; share images at `/og/<page>.png` (`lib/og.tsx`, IBM Plex, rendered at build)
  - schema.org JSON-LD on every page: Organization, WebSite, WebPage/AboutPage, BreadcrumbList (`components/json-ld.tsx`)
  - `/sitemap.xml`, `/robots.txt` (search and AI crawlers allowed), `/manifest.webmanifest`, `/apple-icon.png`
  - `/llms.txt` and `/llms-full.txt` (llmstxt.org): plain-text site map and full page text for AI assistants
  - one `h1` per page, ordered `h2`/`h3`, landmarks (`header`, `nav`, `main`, `footer`), alt text on every image
  - Set `NEXT_PUBLIC_SITE_URL` to the live domain (e.g. `https://example.com`) so canonicals and the sitemap use it; on Vercel it falls back to the project's production domain.
- Contact form: set `NEXT_PUBLIC_CONTACT_ENDPOINT` (form service that accepts JSON POST) or `NEXT_PUBLIC_CONTACT_EMAIL` (opens the visitor's mail app) at build time.

```bash
npm ci
npm run dev      # http://localhost:3000
npm run build    # static site in out/
```

Deploy on Vercel as its own project: Root Directory `site`, framework Next.js, and keep "Include files outside the root directory" on (the build reads `../identity`).
