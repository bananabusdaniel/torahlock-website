# 03 · On-Page SEO & Content

The content itself is the site's biggest asset — and also where the most ranking upside is locked up. The writing is original, accurate, and genuinely useful (1,100–1,900 words per post on focused, searchable questions). The problems are in *packaging* and *interlinking*, not substance.

---

## Title tags — 🟠 Truncated site-wide

**Nearly every blog `<title>` is 81–99 characters.** Google displays ~580px ≈ 60 characters; everything past that is cut with an ellipsis. The culprit is the `… — Torah Lock Blog` suffix (~18 chars) bolted onto already-long titles.

Worst offenders (character count):

| Chars | Page | Displayed title would cut at… |
|---|---|---|
| 99 | `what-is-tefillin.html` | "…A Beginner's Guide to the Mitz…" |
| 99 | `tehillim-for-anxiety.html` | "…7 Psalms Jews Have Said for…" |
| 98 | `what-is-shavuot.html` | cut mid-subtitle |
| 97 | `what-does-baruch-hashem-mean.html` | cut mid-subtitle |
| 96 | `what-is-mussar.html` | cut mid-subtitle |
| 94 | `psalm-27-…`, `emunah-vs-bitachon.html` | cut mid-subtitle |
| … | **~40 of 43 posts exceed 60 chars** | — |

**Fix pattern.** Front-load the keyword, shorten the subtitle, shorten or drop the brand suffix (the brand already appears in the URL and snippet):

| Current (99) | Suggested (≤60) |
|---|---|
| `What Is Tefillin? A Beginner's Guide to the Mitzvah, the Meaning, and How to Wrap — Torah Lock Blog` | `What Is Tefillin? Meaning, Mitzvah & How to Wrap` |
| `What Is the Shema? Understanding Judaism's Most Sacred Prayer — Torah Lock Blog` | `What Is the Shema? Judaism's Most Sacred Prayer` |
| `Tehillim for Anxiety: 7 Psalms Jews Have Said for Centuries to Calm a Racing Mind — Torah Lock Blog` | `Tehillim for Anxiety: 7 Psalms to Calm the Mind` |

Keep the long, evocative version as the **`<h1>` and `og:title`** (no length limit there) — only the `<title>` needs to be tight. This is the highest-CTR-per-hour fix on the site.

---

## Meta descriptions — 🟡 Mostly good, a few long

- Homepage: **182 chars** → trim to ~150 (see [01](01-critical-and-quick-wins.md)).
- `what-is-teshuvah.html`: 168 chars → trim slightly.
- Most posts land 150–160 — good. Spot-check any over 160.
- `privacy.html` / `terms.html` / `support.html`: **no description at all** → add one each.

---

## Headings — 🟢 Good
- Exactly **one `<h1>` per page** across all 48 pages. ✅
- Posts use a clean `<h2>` outline (e.g. the Shema post: Text → Declaration of Faith → When Recited → How to Recite → … → FAQ → Conclusion). Scannable and well-structured for both readers and featured snippets.
- Recommendation: where a post answers a clear sub-question (e.g. "Can women recite the Shema?"), make it an `<h3>` rather than bold `<p><strong>` so it's eligible as its own snippet/PAA target. The Shema FAQ section currently uses `<p><strong>Q?</strong></p>` — convert those to `<h3>`.

---

## Internal linking — 🟡 Strong template, inconsistently applied

This is the single biggest *organic* (non-CTA) opportunity.

**What's there:** every post has nav + footer + a "← Back to Blog" + one hardcoded "Read next" card.

**The gap:** contextual body links to sibling posts range from **1 to 7** depending on the post's age:
- Newer posts (`what-is-the-yetzer-hara`, `tikkun-leil-shavuot`, `what-is-tzedakah`, `what-is-simcha`) embed **4–7** contextual links. This is the correct pattern.
- Cornerstone/older posts embed **only the single "Read next."** The flagship `what-is-the-shema.html` — first in the sitemap, your highest-intent term — links out to **just one** post (*Why the Morning Matters Most*), despite the site containing directly related articles on Shacharit, Tefillin, Mezuzah, Modeh Ani, the Amidah, and Birchot HaShachar (all of which the Shema text explicitly mentions!).

**Why it matters:** internal links spread ranking signal, define topical clusters, and keep readers on-site. You've built a dense Jewish-prayer knowledge base but the cornerstone pages don't pass authority into it.

**Fix:**
1. **Backfill contextual links** into the ~15 oldest posts to match the newer pattern (3–6 per post). In the Shema post, the words "tefillin," "mezuzah," "Shacharit," and "Modeh Ani" should each link to their post.
2. **Add a standardized "Related reading" block** (3 links) above the single "Read next," grouped by the post's topic cluster.

### Topic clusters already on the site (build pillar → spoke links)

| Cluster | Natural pillar page | Spokes (link up to the pillar, and across) |
|---|---|---|
| **Tehillim / Psalms** | `what-is-tehillim.html` | for-healing, for-anxiety, which-to-say-every-morning, power-of-tehillim, psalm-23/27/91/121 |
| **Morning prayer** | `what-is-shacharit.html` | shema, amidah, birchot-hashachar, modeh-ani, kavanah, which-tehillim, why-the-morning-matters |
| **Digital wellness** | `what-the-torah-says-about-phone-addiction.html` | doomscrolling, dopamine-detox, digital-shabbat, how-to-stop-checking-your-phone |
| **Jewish wisdom/values** | (none yet — *gap*) | chesed, tzedakah, hakarat-hatov, simcha, tikkun-olam, mussar, emunah-vs-bitachon |
| **Holidays/calendar** | (none yet — *gap*) | shavuot, lag-baomer, counting-the-omer, tikkun-leil-shavuot |

Designating `what-is-tehillim.html` and `what-is-shacharit.html` as pillar pages (and linking all spokes up to them) would concentrate authority on your two most commercially relevant head terms.

---

## Content depth & quality — 🟢 Strong, two exceptions

41 of 43 posts are 1,100–1,900 words of substantive, well-organized content. Two outliers are the original posts and now look thin next to the rest:

| Post | Words | Issue |
|---|---|---|
| `why-the-morning-matters-most.html` | 484 | Thin **and** no Article schema |
| `the-power-of-tehillim-in-five-verses.html` | 580 | Thin **and** no Article schema |

These two are also the "Read next" targets from several posts, so they receive internal traffic they don't fully earn. **Action:** expand each to ~1,200+ words to match the library, and add Article schema ([04](04-schema-structured-data.md)).

Also thin: **`support.html` = 39 words.** A support page with one line reads as low-value. Add real content: how to contact support, common questions (does it work on Android? how does Shabbat detection work? how do I choose which apps to block?), response-time expectations. This doubles as a conversion/trust asset.

---

## E-E-A-T — 🟡 The credibility gap

The content covers **halacha and Jewish practice** — topics where accuracy matters and readers (and Google's quality raters) look for *who is saying this*. Right now:

- `author` in every Article schema is `{"@type": "Organization", "name": "Torah Lock"}` — **no human author, no credentials, no byline** in the visible page either.
- No `/about` page establishing who is behind Torah Lock or what their Jewish-knowledge basis is.

**Why it matters:** E-E-A-T (Experience, Expertise, Authoritativeness, Trust) is disproportionately weighted for religious/health/finance-adjacent ("Your Money or Your Life"-adjacent) content. A named author with a short bio — ideally someone with relevant background, or a "reviewed by Rabbi ___" line — materially strengthens trust signals and AI-citation likelihood.

**Fix:**
1. Add a visible byline to posts ("By [Name]" or "Reviewed by [Name]").
2. Add an `/about` page (founder + editorial approach + sources) and link it in the nav/footer.
3. Switch Article `author` to a `Person` with a `url` to the about/author page (see [04](04-schema-structured-data.md)).
4. Cite primary sources you already reference (Deuteronomy 6:4, specific Talmud tractates) as links to Sefaria — outbound links to authoritative sources are a positive trust signal for this content type.

---

## Content/keyword gaps (new-page opportunities)

The blog answers "what is X" extremely well. Missing intent types that would expand coverage:

| Gap | Example pages | Why |
|---|---|---|
| **Product/feature pages** | `/features`, `/how-it-works` (as real URLs, not just homepage sections) | Capture "app to block apps until you pray," "Jewish screen time app" |
| **Comparison / alternatives** | "Torah Lock vs [generic app-blocker]," "Jewish alternative to Opal/one-sec" | High commercial intent; you have a unique angle |
| **About / editorial** | `/about` | E-E-A-T + brand entity |
| **FAQ hub** | `/faq` | Consolidate the per-post FAQs; AI-citation magnet |
| **Pillar pages** | designate `what-is-tehillim`, `what-is-shacharit` as hubs | Topical authority |

---

## On-page issue ledger

| Issue | Severity | Effort |
|---|---|---|
| Titles >60 chars (≈40 posts) | 🟠 High | 1–2 hr |
| Cornerstone posts under-interlinked | 🟡 Medium | 2–3 hr |
| Author = Organization (no human E-E-A-T) | 🟡 Medium | 2–4 hr |
| 2 thin legacy posts + thin support.html | 🟡 Medium | 2–3 hr |
| Homepage / a few descriptions too long | 🟢 Low | 15 min |
| FAQ `<p><strong>` → `<h3>` | 🟢 Low | 30 min |
| Missing product/comparison/about pages | 🟡 Medium | ongoing |
