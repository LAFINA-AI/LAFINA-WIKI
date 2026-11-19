# LAFINA Wiki

The LAFINA research wiki and illustrated Android user manual, built with Astro, MDX, React, and Tailwind CSS. The manual keeps the wiki's existing indigo visual identity, document layout, and light/dark themes.

## User manual

- `/user-manual` — searchable guide index.
- `/user-manual/<topic>` — 13 topic guides with 41 numbered steps, step navigation, and screenshot enlargement.
- `/user-manual/full` — complete manual with linked topic/step contents and Print / Save PDF.
- `/manual/LAFINA-User-Manual.pdf` — downloadable 44-page manual with exact page-numbered contents, internal links, and bookmarks.

All 35 unique supplied screenshots are placed beside the relevant instructions. The duplicate original is retained in `screenshots/`. Research pages remain available at their existing routes.

## Local development

Requires Node.js 22.12 or newer.

```powershell
npm ci
npm run dev
```

Open the local URL printed by Astro (normally `http://localhost:4321`).

## Checks and production build

```powershell
npm run check
npm run check:manual
npm run build
npm run preview
```

`build` validates the manual and checked-in PDF before generating the static site. The existing Vercel adapter configuration is preserved. Python is not required to build or host the site.

## Updating the manual

The canonical source is `src/data/manual.json`. Both the website and PDF generator use it. After editing content or screenshot mappings:

```powershell
npm run manual:assets
python -m pip install -r scripts/requirements-manual.txt
npm run manual:pdf
npm run check:manual
```

Render and visually review regenerated PDF pages before delivery. See [the authoring notes and complete screenshot map](docs/MANUAL-CONTENT.md) for provenance, source limits, and the regeneration workflow.

## Project structure

```text
src/components/manual/       Guide steps, toolbar, screenshot dialog, search and print
src/data/manual.json          Shared manual content and screenshot mapping
src/data/navigation.ts        Shared desktop and mobile navigation
src/pages/user-manual/        Index, topic guides, and complete manual
src/pages/*.mdx               Existing research and reference pages
public/manual/                Published screenshots, PDF, checksum metadata
scripts/                      Asset copy, PDF generation, content validation
screenshots/                  Original user-supplied captures
```
