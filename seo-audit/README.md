# Torah Lock — SEO Audit

**Site:** https://torahlock.app
**Repo:** TorahLockMain (static HTML site, hosted on GitHub Pages + Fastly)
**Audited:** 2026-06-09
**Scope:** Homepage, blog hub, 43 blog posts, 3 legal/support pages, robots.txt, sitemap.xml, live HTTP headers, structured data, images, and AI-search readiness.

---

## ✅ Status: IMPLEMENTED (2026-06-09)

All phases below have been implemented in the working tree. See **[`IMPLEMENTATION.md`](IMPLEMENTATION.md)** for the full changelog and verification evidence. Headline: dead App-Store CTA fixed site-wide, 52/52 pages with canonical + OG + Twitter + schema, 0 broken internal links, 102/102 JSON-LD blocks valid, 4 new pages, 2 thin posts expanded, WebP images, `llms.txt`, sitemap regenerated. **Estimated score after: ~89/100.** A few items were deliberately left to you (named author, real ratings, GSC submission) — listed in `IMPLEMENTATION.md`.

The sections below are preserved as the original **diagnosis** (what was found).

---

## TL;DR

Torah Lock has an **unusually strong content foundation** — 43 well-written, original, 1,100–1,900-word articles on Jewish prayer and digital wellness, a complete sitemap, clean semantic HTML, and decent baseline schema. The technical hygiene is good.

But it is **leaking its single most valuable action**: the marketing site contains **zero working links to the App Store**, even though the app is live at `apps.apple.com/app/id6759348814`. Every "Download on the App Store" button points to `href="#"`. This is the #1 fix and it is a 10-minute change.

Beyond that, the gaps are systematic-but-cheap: missing canonicals on all 43 posts, titles that truncate in search results, no social/AI preview images on posts, and schema that under-sells the content to AI engines.

**Overall SEO Health Score: 72 / 100** — "Good foundation, high-ROI fixes available."

---

## Scorecard

| Category | Weight | Score | Notes |
|---|---|---|---|
| Technical SEO | 22% | 78 | Sitemap complete, HTTPS/HTTP2, valid 404. `/index.html` duplicates `/`; no HSTS (host limitation). |
| Content Quality | 23% | 80 | Strong, original, useful. Author = "Organization" (no human E-E-A-T); 2 thin legacy posts. |
| On-Page SEO | 20% | 68 | Good H1/meta discipline, but titles truncate site-wide; dead primary CTA; uneven internal linking. |
| Schema / Structured Data | 10% | 62 | Article on 41/43 posts but no `image`/human author; no breadcrumbs; blog hub has none. |
| Performance (CWV) | 10% | 72 | Light (22KB CSS), lazy images. Render-blocking Google Fonts; PNG-only images. |
| AI Search Readiness (GEO) | 10% | 62 | Highly citable Q&A content, but no `llms.txt`, weak author entity, no post share-images. |
| Images | 5% | 70 | All have alt + dimensions ✓. PNG-only (no WebP/AVIF); OG image is wrong aspect ratio. |

> Scoring follows the claude-seo weighted model. The dead App-Store CTA is primarily a **conversion** loss (not a ranking signal), so it sits *above* the score as the top business priority rather than inside it.

---

## Top 10 priorities (by impact ÷ effort)

| # | Issue | Severity | Effort | File |
|---|---|---|---|---|
| 1 | "Download on the App Store" CTAs are dead (`href="#"`) site-wide | 🔴 Critical | 10 min | [01](01-critical-and-quick-wins.md) |
| 2 | All 43 blog posts missing `rel="canonical"` | 🟠 High | 30 min | [01](01-critical-and-quick-wins.md) / [02](02-technical-seo.md) |
| 3 | Blog titles exceed 60 chars → truncated in SERPs | 🟠 High | 1–2 hr | [03](03-on-page-and-content.md) |
| 4 | No `og:image` / Twitter card on any post → ugly social + AI cards | 🟠 High | 1 hr | [03](03-on-page-and-content.md) / [05](05-geo-ai-search.md) |
| 5 | 2 legacy posts thin (484 / 580 words) + no schema | 🟠 High | 2 hr | [03](03-on-page-and-content.md) |
| 6 | Article schema has no `image`, author is "Organization" | 🟡 Medium | 1 hr | [04](04-schema-structured-data.md) |
| 7 | No `llms.txt` — leaving AI-citation visibility on the table | 🟡 Medium | 30 min | [05](05-geo-ai-search.md) |
| 8 | Blog hub (`blog.html`) has no canonical/OG/schema | 🟡 Medium | 30 min | [02](02-technical-seo.md) / [04](04-schema-structured-data.md) |
| 9 | Cornerstone posts under-interlinked (1 link vs 7 on newer) | 🟡 Medium | 2–3 hr | [03](03-on-page-and-content.md) |
| 10 | Images are PNG-only; OG image wrong ratio | 🟢 Low–Med | 1–2 hr | [06](06-performance-and-images.md) |

---

## How to use these files

| File | Covers |
|---|---|
| [`01-critical-and-quick-wins.md`](01-critical-and-quick-wins.md) | The must-fix-now items and every change that takes < 30 min |
| [`02-technical-seo.md`](02-technical-seo.md) | Crawl, index, canonical strategy, sitemap, robots, HTTP headers, 404 |
| [`03-on-page-and-content.md`](03-on-page-and-content.md) | Titles, descriptions, headings, internal linking, content depth, E-E-A-T |
| [`04-schema-structured-data.md`](04-schema-structured-data.md) | Full schema audit + copy-paste corrected JSON-LD |
| [`05-geo-ai-search.md`](05-geo-ai-search.md) | AI Overviews / ChatGPT / Perplexity readiness, `llms.txt`, citability |
| [`06-performance-and-images.md`](06-performance-and-images.md) | Core Web Vitals, fonts, image formats, favicon/manifest |
| [`07-action-plan.md`](07-action-plan.md) | Sequenced roadmap with dependencies, success checks, metrics to watch |

---

## What's already done well (don't break these)

- ✅ Complete XML sitemap — all 48 indexable URLs present, no orphans.
- ✅ `robots.txt` valid and points to the sitemap.
- ✅ Homepage has full OG + Twitter + 3 JSON-LD blocks (SoftwareApplication, Organization, FAQPage).
- ✅ Exactly one `<h1>` per page; logical H2 structure.
- ✅ Every `<img>` has descriptive alt text **and** explicit `width`/`height` (prevents layout shift / CLS).
- ✅ Homepage hero image `loading="eager"`, gallery images `loading="lazy"` — correct prioritization.
- ✅ Attribution redirect microsites (`/bennymh/`, `/ilanit/`, `/jonnystorms/`) are correctly `noindex` + canonical to the App Store — clean implementation, not index bloat.
- ✅ Valid HTTP 404 (no soft-404s); HTTPS + HTTP/2 enforced.
- ✅ Newer posts (e.g. *Yetzer Hara*, *Tikkun Leil Shavuot*) already do contextual internal linking well — replicate that pattern everywhere.
