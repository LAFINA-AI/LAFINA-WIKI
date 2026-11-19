# User manual verification

Verified locally on 20 November 2026 using the production Astro build and headless Chrome on Windows.

## Automated checks

- `npm run check`: zero errors, warnings, or hints.
- `npm run check:manual`: 13 chapters, 41 steps, 35 unique screenshots, 44 PDF pages; content, screenshot, and PDF checksums agree.
- `npm run build`: all 30 website routes generated successfully, preserving the Vercel adapter.
- Production HTML link audit: manual links resolve to files or valid HTML IDs, including contents, shared navigation, and previous/next steps.
- Every topic route returns HTTP 200, contains the expected number of steps, and has one main heading.
- PDF download returns HTTP 200 with `application/pdf`.

## Browser flows

- Topic search returns matching chapters, exposes a no-results message, and restores all topics when cleared.
- Screenshot enlargement opens the native modal; Escape closes it and restores focus to its trigger.
- Mobile navigation expands and exposes the topic links.
- Light and dark modes visually inspected after theme transitions settle.
- Manual home, class guide, and full manual have no document overflow at 320, 390, 768, or 1440 CSS pixels.
- Class guide inspected at 200% CSS zoom with no document overflow. This is a CSS zoom check, not a browser or assistive-technology certification.
- All 35 full-manual images load and decode before Print / Save PDF invokes printing.
- No browser page errors observed in the checked flows.

## PDF review

- Standalone PDF: 44 pages, 95 internal links, chapter and step outline bookmarks. All 41 step titles appear on their expected pages.
- All standalone pages rendered with PDFium and visually reviewed in contact sheets; representative cover, contents, screenshot, long-content, and reminder pages inspected at higher resolution.
- Browser Print / Save PDF output: 44 pages, all 35 images present, every page contains text. Representative printed pages visually inspected.
- Original screenshots are retained. The `(1)` duplicate is byte-identical and is not published twice.

## Verification limits

This verifies the documentation website and generated documents. It does not validate Android reminder delivery, microphone recognition, cloud account entitlements, or the correctness of AI answers on a physical phone. No screen-reader or cross-browser certification was performed. First-launch and incoming reminder instructions are source-based and clearly marked because no matching screenshots were supplied.
