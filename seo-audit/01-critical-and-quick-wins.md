# 01 · Critical Issues & Quick Wins

Two issues are urgent. Everything else in this file is a < 30-minute change with outsized return.

---

## 🔴 CRITICAL-1 — The primary CTA is dead site-wide

**Evidence:**
- `index.html` lines 122 & 298: `<a href="#" class="btn btn-primary">…Download on the App Store</a>`
- `grep "6759348814"` across `index.html` **and all 43 blog posts** → **0 matches**. Nothing on the public site links to the live listing.
- The real listing is known — your own attribution redirects expose it:
  `https://apps.apple.com/app/apple-store/id6759348814` (see `/bennymh/`, `/ilanit/`, `/jonnystorms/`).
- Confirmed live: the homepage on production still serves `href="#"`.

**Why it matters:** Every visitor who clicks "Download" goes nowhere (the `#` just scrolls to top). You are spending content + SEO effort to drive traffic to a page whose single conversion action is broken. It also removes a strong relevance signal — an outbound link from your homepage to your App Store product page.

**Fix (10 minutes).** Point both homepage buttons at the real listing. Add a campaign token so you can attribute web installs:

```html
<!-- index.html — replace BOTH href="#" on the .btn-primary buttons (lines ~122 and ~298) -->
<a href="https://apps.apple.com/app/apple-store/id6759348814?pt=128568230&ct=website&mt=8"
   class="btn btn-primary" target="_blank" rel="noopener">
```

Then add a download CTA to the **end of every blog post** (see CRITICAL/▶ "Quick win 6" below) — 43 articles currently send engaged readers to a dead end with no app link at all.

**Falsifiability / how you'll know it worked:** click the button → lands on the App Store product page; App Store Connect shows web-referrer installs under campaign `ct=website`.

---

## 🟠 CRITICAL-2 — All 43 blog posts are missing `rel="canonical"`

**Evidence:** `grep -L 'rel="canonical"' blog/*.html` → all 43 posts. Only `index.html` has a canonical.

**Why it matters:** Canonicals are the cheapest defense against duplicate-URL dilution. Pages are reachable at multiple paths (e.g. `/blog/x.html`, and via query strings, and the `/index.html` vs `/` issue on the homepage shows the host *does* serve duplicate paths — see [02](02-technical-seo.md)). A self-referencing canonical removes all ambiguity and is a positive crawl signal.

**Fix (30 minutes for all 43).** Each post already declares its URL in `og:url` — mirror it into a canonical. Add one line to each post's `<head>`:

```html
<!-- e.g. blog/what-is-the-shema.html -->
<link rel="canonical" href="https://torahlock.app/blog/what-is-the-shema.html">
```

Batch approach (each post's `og:url` is the canonical URL — script it):

```bash
cd /Users/danielnamatinia/Code/TorahLockMain
for f in blog/*.html; do
  url=$(grep -o 'og:url" content="[^"]*"' "$f" | sed 's/.*content="//;s/"//')
  grep -q 'rel="canonical"' "$f" || \
    sed -i '' "s#<meta property=\"og:url\" content=\"$url\">#<link rel=\"canonical\" href=\"$url\">\n  <meta property=\"og:url\" content=\"$url\">#" "$f"
done
```
*(Review the diff before committing — `sed -i ''` is the macOS form. Add `blog.html`, `privacy.html`, `terms.html`, `support.html` canonicals too.)*

**Falsifiability:** View source on a live post → one `<link rel="canonical">` pointing to itself; Search Console "Page indexing" shows "Submitted and indexed," not "Duplicate without user-selected canonical."

---

## Quick wins (each < 30 min)

### ▶ Quick win 1 — Trim the homepage meta description
`index.html` line 10 is **182 characters** — Google truncates around 155–160. Tighten it so the call-to-value isn't cut off:

```html
<meta name="description" content="Torah Lock blocks distracting apps each morning until you finish a short Jewish prayer — Shema and personalized Tehillim. Under 5 minutes. Free on iOS.">
```
(≈150 chars, keeps "Jewish prayer," "Shema," "Tehillim," "iOS.")

### ▶ Quick win 2 — Fix the footer copyright mismatch
`index.html` line 313 says **© 2025**; `blog.html` and every post say **© 2026**. Make the homepage 2026 (or, better, drop the year from the static markup and stop dating the site).

### ▶ Quick win 3 — Add canonical + OG to `blog.html`
The hub page has **no canonical, no Open Graph, no Twitter card** (only `<title>` + description). Add:
```html
<link rel="canonical" href="https://torahlock.app/blog.html">
<meta property="og:type" content="website">
<meta property="og:title" content="The Torah Lock Blog — Jewish Prayer & Digital Wellness">
<meta property="og:description" content="Insights on Jewish prayer, Tehillim, and building a deeper connection with Hashem in a distracted world.">
<meta property="og:url" content="https://torahlock.app/blog.html">
<meta property="og:image" content="https://torahlock.app/assets/og-default.png">
```

### ▶ Quick win 4 — Add a default `og:image` + Twitter card to every post
0 / 43 posts have a share image or Twitter card. Until per-post art exists, ship one branded 1200×630 default (`assets/og-default.png`) and reference it in every post head:
```html
<meta property="og:image" content="https://torahlock.app/assets/og-default.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="<!-- same as og:title -->">
<meta name="twitter:description" content="<!-- same as description -->">
<meta name="twitter:image" content="https://torahlock.app/assets/og-default.png">
```
(See [05](05-geo-ai-search.md) and [06](06-performance-and-images.md) — this also helps AI engines render a card and is why the homepage's portrait OG image should be fixed.)

### ▶ Quick win 5 — Add meta descriptions to `privacy.html`, `terms.html`, `support.html`
All three lack `<meta name="description">`. Google will scrape arbitrary text. One sentence each prevents that.

### ▶ Quick win 6 — Add a post-level app CTA block
Append a consistent CTA to the bottom of every post (right before `.blog-post-footer`). This both converts blog readers and adds the missing internal/outbound app link:
```html
<aside class="post-cta">
  <p>Torah Lock helps you guard your morning prayer before the day pulls you away.</p>
  <a href="https://apps.apple.com/app/apple-store/id6759348814?pt=128568230&ct=blog&mt=8"
     class="btn btn-primary" target="_blank" rel="noopener">Download on the App Store</a>
</aside>
```

---

## Quick-win impact summary

| Win | Time | Primary benefit |
|---|---|---|
| Fix dead CTA | 10 min | Conversions + homepage→App-Store relevance |
| Canonicals ×43 | 30 min | Index consolidation, crawl clarity |
| Homepage description | 5 min | Higher SERP CTR (no truncation) |
| Copyright year | 2 min | Trust/polish |
| blog.html OG/canonical | 10 min | Hub shares correctly, consolidates |
| Default og:image ×43 | 20 min | Social + AI card rendering |
| Legal-page descriptions | 10 min | Clean SERP snippets |
| Post CTA block ×43 | 30 min | Blog→app conversion path |
