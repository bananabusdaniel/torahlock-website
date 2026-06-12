# 04 · Schema / Structured Data

Baseline is above average for a small site — the homepage ships three JSON-LD blocks and 41/43 posts have `Article`. The work here is **enriching** existing schema (so it earns rich results and AI citations) and **filling holes** (2 posts, the blog hub, breadcrumbs).

---

## Current state

| Page(s) | Schema present | Verdict |
|---|---|---|
| `index.html` | `SoftwareApplication`, `Organization`, `FAQPage` | Good base; under-specified (see below) |
| 41 blog posts | `Article` (author+publisher = Organization) | Valid but missing `image`, human author, breadcrumbs |
| `why-the-morning-matters-most.html`, `the-power-of-tehillim-in-five-verses.html` | **none** | 🟠 Add `Article` |
| `blog.html` | **none** | 🟡 Add `Blog` + `BreadcrumbList` |
| `privacy/terms/support` | none | Fine (not needed) |

Schema-type tally across posts: `Article` ×41, `Organization` ×82 (author + publisher per post). Consistent — no malformed blocks found.

---

## Fix 1 — Enrich the `Article` blocks (all posts)

Current (from `what-is-the-shema.html`):
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "What Is the Shema? Understanding Judaism's Most Sacred Prayer",
  "description": "…",
  "datePublished": "2026-04-13",
  "dateModified": "2026-04-13",
  "author": { "@type": "Organization", "name": "Torah Lock" },
  "publisher": { "@type": "Organization", "name": "Torah Lock", "url": "https://torahlock.app" },
  "mainEntityOfPage": "https://torahlock.app/blog/what-is-the-shema.html"
}
```

Issues: (a) no `image` — Article rich results and many AI cards want one; (b) `publisher` has no `logo` (required for Article rich-result eligibility); (c) `author` is an org, not a person (E-E-A-T — see [03](03-on-page-and-content.md)); (d) consider `BlogPosting` (a more precise subtype of `Article`).

Improved:
```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "What Is the Shema? Understanding Judaism's Most Sacred Prayer",
  "description": "The Shema is the central declaration of Jewish faith…",
  "image": "https://torahlock.app/assets/og-default.png",
  "datePublished": "2026-04-13",
  "dateModified": "2026-04-13",
  "author": {
    "@type": "Person",
    "name": "AUTHOR NAME",
    "url": "https://torahlock.app/about.html"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Torah Lock",
    "url": "https://torahlock.app",
    "logo": {
      "@type": "ImageObject",
      "url": "https://torahlock.app/assets/favicon.png"
    }
  },
  "mainEntityOfPage": "https://torahlock.app/blog/what-is-the-shema.html"
}
```
> If you genuinely have no single human author, keeping `Organization` is *allowed* — but add the `publisher.logo` and `image` regardless, since those gate rich-result eligibility. The human author is the E-E-A-T upgrade.

---

## Fix 2 — Add `BreadcrumbList` to every post

No breadcrumb schema anywhere. It produces the `Home › Blog › Post` trail in search results and clarifies hierarchy. Add a second JSON-LD block to each post:
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://torahlock.app/" },
    { "@type": "ListItem", "position": 2, "name": "Blog", "item": "https://torahlock.app/blog.html" },
    { "@type": "ListItem", "position": 3, "name": "What Is the Shema?", "item": "https://torahlock.app/blog/what-is-the-shema.html" }
  ]
}
```
Pair it with a visible breadcrumb nav (replace the lone "← Back to Blog" with `Home › Blog › <title>`) — visible + structured should match.

---

## Fix 3 — Add schema to `blog.html` (the hub)

```json
{
  "@context": "https://schema.org",
  "@type": "Blog",
  "name": "The Torah Lock Blog",
  "url": "https://torahlock.app/blog.html",
  "description": "Insights on Jewish prayer, Tehillim, and digital wellness.",
  "publisher": {
    "@type": "Organization",
    "name": "Torah Lock",
    "logo": { "@type": "ImageObject", "url": "https://torahlock.app/assets/favicon.png" }
  }
}
```
Optionally add an `ItemList` of the latest posts. Add `BreadcrumbList` (`Home › Blog`) too.

---

## Fix 4 — Strengthen `SoftwareApplication` (homepage)

Current block (lines 37–52) is minimal. Add the **real install URL** (the dead-CTA fix in schema form), and — *only if you have genuine ratings* — an `aggregateRating`. **Never fabricate ratings**; invented review counts are a manual-action risk.

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Torah Lock",
  "operatingSystem": "iOS",
  "applicationCategory": "LifestyleApplication",
  "description": "Torah Lock blocks distracting apps each morning until you complete a short daily Jewish prayer — Shema and personalized Tehillim. Under 5 minutes.",
  "url": "https://torahlock.app/",
  "installUrl": "https://apps.apple.com/app/apple-store/id6759348814",
  "downloadUrl": "https://apps.apple.com/app/apple-store/id6759348814",
  "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD" },
  "screenshot": [
    "https://torahlock.app/assets/screenshots/torah-lock-home-screen.png",
    "https://torahlock.app/assets/screenshots/torah-lock-shema-prayer.png",
    "https://torahlock.app/assets/screenshots/torah-lock-tehillim-hebrew.png"
  ]
  // Add ONLY when real:
  // "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.X", "ratingCount": "NN" }
}
```

Also: the `Organization` block (lines 55–63) should gain a `logo` and `sameAs` (links to your App Store listing + any social profiles) to strengthen the brand entity for Knowledge Graph / AI:
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Torah Lock",
  "url": "https://torahlock.app",
  "logo": "https://torahlock.app/assets/favicon.png",
  "sameAs": [
    "https://apps.apple.com/app/apple-store/id6759348814"
    /* add X/Instagram/etc. if they exist */
  ],
  "description": "A Jewish morning prayer app that blocks distracting apps until you pray."
}
```

---

## Fix 5 — The `FAQPage` block (homepage) — ℹ️ keep, but reset expectations

The homepage `FAQPage` (lines 66–97) is **valid and well-formed**. However, since Google's **August 2023** change, FAQ rich results show **only for government and health sites** — a lifestyle app won't get the expandable FAQ in Google SERPs.

**Verdict: keep it.** It costs nothing and still helps **AI engines** (ChatGPT, Perplexity, AI Overviews) extract clean Q&A pairs — which is exactly the GEO play in [05](05-geo-ai-search.md). Just don't expect Google rich snippets from it. *(Per current guidance: don't add new FAQPage for Google rich-result purposes; existing ones are an Info-level item, not a problem to remove.)*

The per-post FAQ sections (e.g. the Shema post's "Frequently Asked Questions") are **not** marked up as `FAQPage` — and that's the right call for commercial pages. Keep them as readable `<h3>` Q&As for snippet/AI eligibility without the schema.

---

## Validation workflow

After edits, validate every template with:
- **Rich Results Test:** https://search.google.com/test/rich-results
- **Schema Markup Validator:** https://validator.schema.org/

Test one of each template type (homepage, a post, blog hub) — they're templated, so one pass per template covers all.

## Schema issue ledger

| Issue | Severity | Effort |
|---|---|---|
| Article missing `image` + `publisher.logo` | 🟡 Medium | 1 hr (templated) |
| Author = Organization (no Person) | 🟡 Medium | with E-E-A-T work |
| No `BreadcrumbList` anywhere | 🟡 Medium | 1 hr |
| 2 posts have no schema | 🟠 High | 15 min |
| `blog.html` has no schema | 🟡 Medium | 15 min |
| `SoftwareApplication` missing install URL / entity links | 🟡 Medium | 20 min |
| FAQPage won't yield Google rich result | ℹ️ Info | none (keep) |
