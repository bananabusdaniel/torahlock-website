# 07 · Action Plan

> **✅ IMPLEMENTED 2026-06-09 — Phases 1–4 are all done.** This plan is retained as the record of intent; see [`IMPLEMENTATION.md`](IMPLEMENTATION.md) for what shipped and how it was verified. Remaining open items are only those that need a human decision or real data: named author (E-E-A-T), genuine `aggregateRating`, optional self-hosted fonts, HSTS (host limitation), and submitting to Google Search Console.

Sequenced by dependency and impact ÷ effort. Each item lists **how you'll know it worked** (falsifiability) and, where relevant, a **leading indicator** to monitor without re-running the audit.

---

## Phase 1 — This week (Critical + quick wins) · ~2–3 hrs total

| # | Action | File | Done-when (falsifiability) |
|---|---|---|---|
| 1 | Point both homepage CTAs to `apps.apple.com/app/apple-store/id6759348814?...ct=website` | [01](01-critical-and-quick-wins.md) | Button lands on App Store; web installs appear under `ct=website` in App Store Connect |
| 2 | Add self-referencing `rel="canonical"` to all 43 posts (+ blog/legal pages) | [01](01-critical-and-quick-wins.md) | View-source shows one matching canonical per page; GSC stops flagging "duplicate without canonical" |
| 3 | Add post-bottom App Store CTA block to all posts | [01](01-critical-and-quick-wins.md) | Every post has an outbound App Store link |
| 4 | Trim homepage meta description to ~150 chars | [01](01-critical-and-quick-wins.md) | SERP snippet no longer ends in "…" mid-word |
| 5 | Fix `© 2025` → `2026` on homepage footer | [01](01-critical-and-quick-wins.md) | Footer year consistent site-wide |
| 6 | Add canonical + OG to `blog.html`; descriptions to legal pages | [01](01-critical-and-quick-wins.md)/[02](02-technical-seo.md) | Hub + legal pages share/snippet correctly |

**Dependency:** none — Phase 1 is all independent, fast, and high-certainty. Do it first.

---

## Phase 2 — Next 1–2 weeks (High impact) · ~6–10 hrs

| # | Action | File | Done-when |
|---|---|---|---|
| 7 | Shorten all `<title>`s to ≤60 chars (keep long version as H1/og:title) | [03](03-on-page-and-content.md) | No post title truncates in the Rich Results / SERP preview |
| 8 | Create `assets/og-default.png` (1200×630); set on homepage + all posts + Twitter card | [01](01)/[05](05)/[06](06) | Sharing a post URL renders a branded landscape card; homepage OG no longer a portrait crop |
| 9 | Add `Article`/`BlogPosting` schema to the 2 schema-less posts | [04](04-schema-structured-data.md) | Rich Results Test passes for both |
| 10 | Expand 2 thin posts (484/580w) to ~1,200w; expand `support.html` | [03](03-on-page-and-content.md) | Both posts ≥1,100 words; support page answers real questions |
| 11 | Add `llms.txt` at repo root | [05](05-geo-ai-search.md) | `https://torahlock.app/llms.txt` returns the curated list |
| 12 | Enrich Article schema: add `image` + `publisher.logo` across template | [04](04-schema-structured-data.md) | Article rich-result eligibility (logo+image) confirmed in test |

**Dependency:** #8 (og-default.png) unblocks the image half of #12 and the GEO card work. Make the image first.

---

## Phase 3 — Within the month (Authority + depth) · ongoing

| # | Action | File | Done-when |
|---|---|---|---|
| 13 | Backfill 3–6 contextual internal links into the ~15 under-linked cornerstone posts | [03](03-on-page-and-content.md) | Shema/Shacharit/Tehillim hubs each link to ≥4 siblings |
| 14 | Designate `what-is-tehillim` & `what-is-shacharit` as pillar pages; link spokes up | [03](03-on-page-and-content.md) | Every cluster spoke links to its pillar |
| 15 | Add `BreadcrumbList` schema + visible breadcrumb to posts | [04](04-schema-structured-data.md) | Breadcrumb trail shows in Rich Results Test |
| 16 | Add named author + `/about` page; switch schema `author` to `Person`; add `Organization.sameAs` | [03](03)/[04](04) | Posts show a byline; about page live and linked |
| 17 | Convert PNG screenshots → WebP with `<picture>` fallback | [06](06-performance-and-images.md) | WebP served to supporting browsers; total image bytes down 30%+ |
| 18 | Trim/preload (or self-host) fonts | [06](06-performance-and-images.md) | PSI shows reduced render-blocking; faster FCP/LCP |
| 19 | Convert post FAQ `<p><strong>Q?</strong></p>` → `<h3>`; add answer-first openings + TL;DR lists | [03](03)/[05](05) | Each FAQ is its own heading; posts open with a direct answer |

---

## Phase 4 — Backlog (Low priority / nice-to-have)

| # | Action | File |
|---|---|---|
| 20 | Repoint internal `index.html` links → `/` | [02](02-technical-seo.md) |
| 21 | Add branded `404.html` | [02](02-technical-seo.md) |
| 22 | Automate `sitemap.xml` generation (honest `lastmod`) | [02](02-technical-seo.md) |
| 23 | 180×180 apple-touch-icon, `theme-color`, web manifest | [06](06-performance-and-images.md) |
| 24 | `prefers-reduced-motion` guard on homepage slider | [06](06-performance-and-images.md) |
| 25 | New page types: `/features`, comparison/alternatives, `/faq` hub | [03](03-on-page-and-content.md) |
| 26 | (Optional) Front with Cloudflare for HSTS + security headers | [02](02-technical-seo.md) |

---

## Effort ÷ impact map

```
IMPACT
  high │  [1 CTA]            [7 titles]  [13 interlink]
       │  [2 canonicals]     [8 OG img]  [16 author/E-E-A-T]
       │  [11 llms.txt]      [10 thin]   [14 pillars]
  med  │  [4 desc][6 hub]    [9 schema]  [17 webp][18 fonts]
       │                     [12 schema] [15 breadcrumb][19 GEO fmt]
  low  │  [5 year]                       [20-24 polish]
       └─────────────────────────────────────────────────
          low effort          med            high effort
        ◀ do first                         schedule later ▶
```

---

## Measurement & cadence

**Set up first (if not already):**
- Google Search Console (verify the property, submit `sitemap.xml`) — your source of truth for indexation, queries, CTR, position.
- PageSpeed Insights baseline for `/` and one post.

**Watch monthly:**
| Signal | Where | What "working" looks like |
|---|---|---|
| Pages indexed | GSC → Indexing | All 48 indexed; zero "duplicate/no canonical" |
| Impressions + avg position | GSC → Performance | Rising on "what is the shema," "tehillim for healing," etc. |
| CTR per page | GSC → Performance | Up after title/description fixes (Phase 1–2) |
| App Store web installs | App Store Connect | `ct=website` / `ct=blog` campaigns recording installs (proves CTA fix) |
| AI citations | Manual Perplexity/ChatGPT checks | Domain cited for niche prayer queries (proves GEO work) |

**Re-audit trigger:** after Phase 2 ships, re-run `/seo audit` (or `/seo drift compare`) to confirm the score moved and nothing regressed.
