# 05 · GEO — AI Search Readiness (AI Overviews / ChatGPT / Perplexity)

**This is Torah Lock's biggest untapped channel.** The blog is 43 clear, factual, well-structured answers to questions people literally type into ChatGPT and Google ("what is the shema," "which tehillim for healing," "what does baruch hashem mean"). That is *exactly* the content AI engines cite. A few cheap signals would make you the source they quote.

---

## Why this site is GEO-friendly already

- **Question-shaped URLs and H1s** ("What Is X?") map 1:1 to AI prompts.
- **Definitional, answer-first paragraphs** under each H2.
- **Original, specific, sourced claims** (verse citations, Talmudic references) — AI engines favor specific, verifiable text over fluff.
- **Clean semantic HTML** with one H1 and logical H2s — easy to parse into passages.
- **Homepage `FAQPage`** already provides extractable Q&A pairs (see [04](04-schema-structured-data.md)).

You're ~5 changes away from being a default citation for niche Jewish-practice queries, where authoritative competition is thin.

---

## Gap 1 — No `llms.txt` (add it)

There's no `/llms.txt`. It's the emerging convention (like robots.txt, but for LLMs) that gives AI crawlers a curated map of your best content. Drop this at repo root as `llms.txt`:

```markdown
# Torah Lock

> Torah Lock is an iOS app that blocks distracting apps each morning until you complete a short Jewish prayer — the Shema and personalized Tehillim (Psalms). It helps Jews put Hashem first before the day's noise begins. Enforcement is on-device via Apple Screen Time; nothing is collected.

## App
- [Torah Lock on the App Store](https://apps.apple.com/app/apple-store/id6759348814): Download the iOS app
- [Homepage](https://torahlock.app/): What it is and how it works

## Prayer guides
- [What Is the Shema?](https://torahlock.app/blog/what-is-the-shema.html)
- [What Is Shacharit?](https://torahlock.app/blog/what-is-shacharit.html)
- [What Is the Amidah?](https://torahlock.app/blog/what-is-the-amidah.html)
- [Modeh Ani: The First Prayer of the Day](https://torahlock.app/blog/modeh-ani-the-first-prayer-of-the-day.html)
- [Birchot HaShachar: The 15 Morning Blessings](https://torahlock.app/blog/birchot-hashachar-morning-blessings.html)

## Tehillim (Psalms)
- [What Is Tehillim?](https://torahlock.app/blog/what-is-tehillim.html)
- [Tehillim for Healing](https://torahlock.app/blog/tehillim-for-healing.html)
- [Tehillim for Anxiety](https://torahlock.app/blog/tehillim-for-anxiety.html)
- [Which Tehillim to Say Every Morning](https://torahlock.app/blog/which-tehillim-to-say-every-morning.html)

## Digital wellness
- [What the Torah Says About Phone Addiction](https://torahlock.app/blog/what-the-torah-says-about-phone-addiction.html)
- [How to Stop Checking Your Phone in the Morning](https://torahlock.app/blog/how-to-stop-checking-your-phone-in-the-morning.html)
- [Digital Shabbat](https://torahlock.app/blog/digital-shabbat-unplugging-once-a-week.html)

## Full index
- [All articles](https://torahlock.app/blog.html)
```
Keep it curated (your best 15–25 URLs), not a dump of all 43. Update when you publish cornerstone pieces.

---

## Gap 2 — No share/citation image on posts

0/43 posts have `og:image`. AI answer cards, social embeds, and Discord/Slack/iMessage previews all fall back to nothing. Ship a branded **1200×630** default now (`assets/og-default.png`), then per-post images later. (Covered as a quick win in [01](01-critical-and-quick-wins.md); image specs in [06](06-performance-and-images.md).)

---

## Gap 3 — Weak author/brand entity

AI engines increasingly weight *who* is making a claim, especially on religious topics. Today the author is an anonymous "Organization."

- Add a named author + `/about` page (see [03](03-on-page-and-content.md), [04](04-schema-structured-data.md)).
- Add `Organization.sameAs` linking your App Store + social profiles ([04](04-schema-structured-data.md)) so engines can resolve "Torah Lock" to one entity.
- Where you state halacha, cite the primary source with an outbound link (Sefaria for Tanakh/Talmud). AI engines reward content that links to authoritative corroboration.

---

## Gap 4 — Make passages more "liftable"

AI Overviews lift a single self-contained passage. Help it:
1. **Answer-first.** Open each post with a 1–2 sentence direct answer *before* the narrative lead. The Shema post buries "the Shema is the central declaration of Jewish faith…" — promote a crisp definition to sentence one. (Several posts already do this; standardize it.)
2. **Convert FAQ `<p><strong>Q?</strong></p>` to `<h3>Q?</h3>`** so each Q&A is an addressable passage.
3. **Add a TL;DR / key-facts list** near the top of cornerstone posts (e.g. for Tehillim-for-healing: a short list of the traditional chapters). Lists are disproportionately lifted into AI answers and featured snippets.

---

## Gap 5 — Confirm AI crawlers aren't blocked

Your `robots.txt` allows everyone (good — GPTBot, PerplexityBot, Google-Extended, ClaudeBot all permitted). **Decision point:** if you *want* AI citations (you do — it's free distribution for a niche topic), keep it open. Only restrict if you later decide AI answers cannibalize clicks. For a top-of-funnel app, openness is the right call.

---

## GEO issue ledger

| Item | Severity | Effort |
|---|---|---|
| Add `llms.txt` | 🟡 Medium | 30 min |
| Default `og:image` on posts | 🟠 High | 1 hr |
| Named author + `sameAs` entity | 🟡 Medium | with E-E-A-T work |
| Answer-first + `<h3>` FAQs + TL;DR lists | 🟡 Medium | 2–3 hr |
| Keep AI crawlers allowed | ✅ | none (already open) |

**Leading indicator to watch:** search Perplexity / ChatGPT-with-search for "which tehillim for healing" and "what is the shema" monthly. When your domain starts appearing as a cited source, the GEO work is landing — well before it shows in Search Console.
