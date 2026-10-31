# Mustard Bio brand identity site

Next.js (App Router, static export) version of the Mustard Bio brand identity and design system.

```bash
npm install
npm run dev      # syncs brand assets, then starts http://localhost:3000
npm run build    # syncs, builds the static site into out/, verifies assets
```

## Where things live

| Path | What |
|---|---|
| `app/` | Layout (IBM Plex via `next/font`), page, global styles (`globals.css`) |
| `components/sections/` | One component per section, `01-overview` to `16-files` |
| `components/` | Nav, lightbox, motion demos, live WebGL (hero shader, 3D viewer), server-rendered brand blocks |
| `lib/brand.ts` | Colours, contrast maths, icon set, generative illustrations, easing curves, nav |

## Assets: one source of truth

Brand assets are produced and improved in the brand repo, never in this app:

- `../identity/assets/` → copied to `public/assets/` by `npm run sync` (runs automatically before `dev` and `build`)
- `../identity/render/scenes.js` → copied to `lib/generated/scenes.js` (the Three.js scene library)

Both destinations are git-ignored. Files are copied byte for byte, images are served with `images: { unoptimized: true }` and plain `<img>` tags, and `postbuild` runs `scripts/verify-assets.mjs`, which fails the build if any file in `out/assets` differs from `../identity/assets` by SHA-256. Improving an asset is: update it in `identity/assets`, run `npm run build`, commit.

## Deploying

`out/` is a plain static site. `npm start` previews it locally.

**Vercel** (ignore the multi-service suggestion: `source/` is the local logo build tool, not a service). Either:

- On the import screen, choose **Import single project** next to `web` (Next.js). Root Directory becomes `web`; keep "Include files outside the root directory in the Build Step" enabled, because the build reads `../identity/assets`.
- Or keep Root Directory at `./` and set Application Preset to **Other**; the repo-root `vercel.json` then installs and builds inside `web/` and serves `web/out`.
