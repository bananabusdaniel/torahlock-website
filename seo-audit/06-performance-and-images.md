# 06 · Performance & Images

The site is light and static — a strong starting point. No framework, no bloat, one 22 KB stylesheet, lazy-loaded images, served over HTTP/2 from a CDN. The opportunities are render-blocking fonts, image formats, and the OG image.

> **Note on measurement:** real Core Web Vitals (LCP, INP, CLS) require field data from CrUX/PageSpeed Insights, which needs sufficient traffic. Run https://pagespeed.web.dev/ against `https://torahlock.app/` and a blog post for live lab+field numbers. The items below are the structural wins visible from the source.

---

## Fonts — 🟡 Render-blocking, the main perf lever

`index.html` lines 31–33 (and every page) load Google Fonts:
```html
<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```
That's **two families × ~10 weights**, render-blocking, from a third-party origin.

Good already: `preconnect` to both font origins ✅, and `display=swap` ✅ (no invisible-text FOIT).

Improvements (in order of impact):
1. **Cut weights you don't use.** Audit the CSS — you likely use 2–3 weights per family, not 10. Each weight is a separate download. Trim the URL to e.g. `Lora:wght@400;600;700` + `Inter:wght@400;500;700`.
2. **`preload` the single most-used weight** so text paints faster:
   ```html
   <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap">
   ```
3. **Optional — self-host** the woff2 files in `/assets/fonts/`. Removes the third-party round-trip entirely and is the biggest LCP win for text-heavy blog pages. Use `font-display: swap` in your `@font-face`.

---

## Images — 🟡 Format is the win

Inventory: 7 product screenshots + 1 favicon, **all PNG**. No WebP/AVIF anywhere.

What's already right:
- ✅ Every `<img>` has descriptive, keyword-relevant `alt` (e.g. *"Shema Yisrael declaration of faith screen in Torah Lock Jewish prayer app"*).
- ✅ Explicit `width`/`height` on every image → no layout shift (protects CLS).
- ✅ Hero screenshot `loading="eager"`; gallery `loading="lazy"` → correct LCP prioritization.

Improvements:
1. **Convert PNG → WebP (and/or AVIF).** Phone-screenshot PNGs typically shrink 30–60% as WebP at equal quality. Serve with a fallback:
   ```html
   <picture>
     <source srcset="assets/screenshots/torah-lock-home-screen.webp" type="image/webp">
     <img src="assets/screenshots/torah-lock-home-screen.png"
          alt="Torah Lock home screen showing Morning Session ready to start"
          width="320" height="693" loading="eager">
   </picture>
   ```
   Quick local conversion:
   ```bash
   cd assets/screenshots
   for f in *.png; do cwebp -q 82 "$f" -o "${f%.png}.webp"; done   # brew install webp
   ```
2. **Serve responsive sizes.** The screenshots render at ~320px wide but the source files may be larger. Export at the displayed size (or 2× for retina = 640px) and stop there.

---

## OG / social image — 🟠 Wrong aspect ratio

`index.html` line 17 uses a **portrait phone screenshot** (`torah-lock-home-screen.png`, 320×693) as `og:image`. Social/AI cards expect **landscape 1200×630 (1.91:1)**; a tall portrait image gets cropped to an awkward sliver or rejected.

**Fix:** create a dedicated `assets/og-default.png` at **1200×630** — app name + tagline ("Put Hashem first every morning") + a phone mockup composited on brand background. Use it for:
- homepage `og:image` / `twitter:image`
- the default post `og:image` (the 0/43 gap from [01](01-critical-and-quick-wins.md)/[05](05-geo-ai-search.md))

---

## Favicon & manifest — 🟢 Low priority

- Only `assets/favicon.png` + `apple-touch-icon` (same file). Works, but:
  - Add a proper `apple-touch-icon` at **180×180** (a 32px favicon scaled up looks soft on iOS home screens).
  - No `site.webmanifest` / PWA manifest. For a marketing site this is optional, but a small manifest (name, theme color, icons) is a cheap polish + enables "Add to Home Screen."
- A `theme-color` meta would tint mobile browser chrome to brand:
  ```html
  <meta name="theme-color" content="#YOUR_BRAND_HEX">
  ```

---

## CSS / JS — 🟢 Healthy
- `styles.css` = 22 KB, one file, external (cacheable). Fine. If chasing a perfect LCP, inline the ~critical above-the-fold rules and defer the rest — but at 22 KB this is optional.
- Homepage JS (slider autoplay, IntersectionObserver fade-ins) is small, vanilla, and non-blocking. The 4-second autoplay slider is fine; ensure it respects `prefers-reduced-motion` for accessibility:
  ```js
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) { /* skip startAutoplay() */ }
  ```

---

## Performance issue ledger

| Item | Severity | Effort | Metric helped |
|---|---|---|---|
| Trim/preload/self-host fonts | 🟡 Medium | 1–2 hr | LCP, FCP |
| PNG → WebP/AVIF | 🟡 Medium | 1 hr | LCP, total bytes |
| OG image wrong ratio | 🟠 High* | 1 hr | Social/AI CTR (*high for sharing, not CWV) |
| 180×180 apple-touch-icon | 🟢 Low | 15 min | polish |
| `theme-color` + manifest | 🟢 Low | 30 min | mobile polish |
| `prefers-reduced-motion` on slider | 🟢 Low | 15 min | a11y |
| Run PSI/CrUX for field data | — | 10 min | establishes baseline |
