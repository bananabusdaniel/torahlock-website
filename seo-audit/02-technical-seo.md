# 02 · Technical SEO

Host: **GitHub Pages** behind **Fastly** CDN (confirmed via live `server: GitHub.com` + `x-fastly-request-id`). This shapes what is and isn't fixable (custom response headers, for instance, are largely off-limits).

---

## Crawlability — 🟢 Good

| Check | Status | Detail |
|---|---|---|
| `robots.txt` | ✅ | `User-agent: * / Allow: /` + `Sitemap:` line. Clean. |
| Sitemap reference | ✅ | `https://torahlock.app/sitemap.xml` declared in robots. |
| Crawl blockers | ✅ | Nothing disallowed; no `noindex` on real content; no login walls. |
| JS dependency | ✅ | All content is server-rendered HTML. The blog filter & slider are progressive enhancements — every post card and image is in the raw HTML, so crawlers see everything. |

**Minor:** `robots.txt` could add a `Host:` hint and (optionally) block faceted/query crawling, but there are no query params to worry about here. Leave as-is.

---

## Indexability — 🟡 One real issue

### `/index.html` serves a duplicate 200 of `/`
Live check:
```
GET https://torahlock.app/            → HTTP/2 200
GET https://torahlock.app/index.html  → HTTP/2 200   (identical content, no redirect)
```
The homepage canonical (`https://torahlock.app/`) means Google will *consolidate* the two, so this is **mitigated, not broken**. The leak is internal: your nav logo and footer link to `index.html` / `../index.html`, so internal PageRank flows to the non-canonical variant.

**Fix:** change internal homepage links from `index.html` → `/` (root-relative). Examples:
- `index.html:104` `<a href="index.html" class="nav-logo">` → `href="/"`
- `blog.html:21`, every `blog/*.html` nav: `../index.html` → `/`
- Footer links likewise.

GitHub Pages can't 301 `/index.html` → `/` (no server config), so the canonical + internal-link fix is the correct lever.

### Blog posts missing canonical
Covered in [01](01-critical-and-quick-wins.md) — all 43. This is the bigger indexability item.

---

## Sitemap — 🟢 Complete, with tidy-ups

`sitemap.xml` contains **48 `<loc>` entries = exactly the 48 indexable pages** on disk. No orphans, no missing posts, no stale/deleted URLs. This is genuinely well-maintained.

Tidy-ups (low priority):

1. **`<changefreq>` and `<priority>` are ignored by Google** (officially deprecated as ranking/crawl inputs). Harmless, but they imply a precision Google doesn't use. Keep or drop — don't invest in tuning them.
2. **Homepage `lastmod` is stale:** sitemap says `2026-04-13` for `/` (priority 1.0), but the live homepage's `last-modified` header is `2026-06-08`. Keep `lastmod` honest — it's the *one* field Google does read for scheduling recrawls. Update it whenever the page changes.
3. **Automate it.** With a template-driven static site, generate `sitemap.xml` from the file list + git commit dates so `lastmod` is never wrong and new posts can't be forgotten.

---

## URL structure — 🟢 Acceptable

- `.html` extensions (`/blog/what-is-the-shema.html`) are fine for SEO; not the prettiest, but changing them now would require 301s you can't easily do on GitHub Pages. **Leave them** — consistency beats churn.
- Slugs are clean, lowercase, hyphenated, keyword-rich (`/blog/tehillim-for-anxiety.html`). 👍
- No deep nesting, no parameters, no uppercase, no underscores.

---

## HTTPS / protocol / headers — 🟢 mostly, with host limits

From the live homepage response:

| Header | Value | Verdict |
|---|---|---|
| Protocol | HTTP/2, HTTPS | ✅ |
| `cache-control` | `max-age=600` | ✅ Reasonable for HTML on a CDN. |
| `vary` | `Accept-Encoding` | ✅ Compression negotiated (Brotli/gzip via Fastly). |
| `last-modified` | present | ✅ Enables conditional requests. |
| `strict-transport-security` (HSTS) | **absent** | ⚠️ GitHub Pages doesn't emit HSTS for custom domains. Not directly a ranking factor; minor security gap. Not fixable without moving off GH Pages or fronting with your own CDN/Cloudflare. |
| CSP / `X-Content-Type-Options` / `X-Frame-Options` | absent | ⚠️ Same host limitation. Low SEO impact; note for security posture. |

**If you ever want HSTS + security headers:** front the site with Cloudflare (free) and set headers there. Optional, low priority.

---

## Mobile — 🟢 Good
- `<meta name="viewport" content="width=device-width, initial-scale=1.0">` on every page ✅
- Responsive CSS (22 KB, single stylesheet) ✅
- No intrusive interstitials ✅
- Run a live [Mobile-Friendly check](https://search.google.com/test/mobile-friendly) post-launch to confirm tap-target spacing on the blog filter buttons.

---

## 404 handling — 🟢 Good
`GET /this-page-does-not-exist` → **HTTP/2 404** (true status, not a soft-404). GitHub Pages serves its default 404 body.
**Optional polish:** add a branded `404.html` at repo root (GitHub Pages auto-serves it) with links back to the blog + homepage to recover lost visitors.

---

## Jekyll / build hygiene — 🟢 Note only
- No `.nojekyll` file. GitHub Pages runs Jekyll by default. You have no underscore-prefixed files or folders, so Jekyll isn't stripping anything — **currently harmless**. If you ever add an `_assets/` or `_data/` folder, add an empty `.nojekyll` to repo root to stop Jekyll from hiding it.
- No `CNAME` file in the repo, yet `torahlock.app` resolves — the custom domain is configured in repo Settings → Pages. Fine. (Committing a `CNAME` file makes the domain config reproducible if the repo is ever re-created.)

---

## Technical issue ledger

| Issue | Severity | Fixable on GH Pages? | Action |
|---|---|---|---|
| Blog posts missing canonical | 🟠 High | Yes | Add self-referencing canonical (see 01) |
| `/index.html` duplicate of `/` | 🟡 Medium | Partial | Canonical (done) + repoint internal links to `/` |
| Homepage `lastmod` stale | 🟢 Low | Yes | Keep `lastmod` honest; automate sitemap |
| `changefreq`/`priority` noise | 🟢 Low | Yes | Optional cleanup |
| No HSTS / security headers | 🟢 Low | No (host limit) | Optional: front with Cloudflare |
| No custom 404 | 🟢 Low | Yes | Add `404.html` |
