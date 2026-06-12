#!/usr/bin/env python3
"""
Torah Lock — deterministic on-page SEO transform.
Idempotent. Processes the 41 standard blog posts + index.html + blog.html + legal pages.
The 2 thin posts (why-the-morning-matters-most, the-power-of-tehillim-in-five-verses)
and support.html are handled separately (full rewrites by content agents).
"""
import re, json, pathlib, html as htmllib

ROOT = pathlib.Path(__file__).resolve().parents[2]
OG = "https://torahlock.app/assets/og-default.png"
APP = "https://apps.apple.com/app/apple-store/id6759348814?pt=128568230&ct=website&mt=8"
APP_BLOG = "https://apps.apple.com/app/apple-store/id6759348814?pt=128568230&ct=blog&mt=8"
LOGO = "https://torahlock.app/assets/favicon.png"

THIN = {"why-the-morning-matters-most", "the-power-of-tehillim-in-five-verses"}

TITLES = {
 "birchot-hashachar-morning-blessings": "Birchot HaShachar: The 15 Jewish Morning Blessings",
 "counting-the-omer-sefirat-haomer": "What Is Counting the Omer? Sefirat HaOmer Guide",
 "digital-shabbat-unplugging-once-a-week": "Digital Shabbat: Unplugging One Day a Week",
 "emunah-vs-bitachon": "Emunah vs. Bitachon: Jewish Faith vs. Trust",
 "how-to-stop-checking-your-phone-in-the-morning": "How to Stop Checking Your Phone in the Morning",
 "kavanah-how-to-pray-with-intention": "Kavanah: How to Pray With Intention",
 "modeh-ani-the-first-prayer-of-the-day": "Modeh Ani: The First Prayer of the Day",
 "pirkei-avot-ethics-of-the-fathers": "Pirkei Avot: Judaism's Ethics of the Fathers",
 "psalm-121-meaning-esa-einai": "Psalm 121 Meaning: Esa Einai (Song of Protection)",
 "psalm-23-meaning-in-judaism": "Psalm 23 in Judaism: The Meaning of Mizmor LeDavid",
 "psalm-27-meaning-ledavid-hashem-ori": "Psalm 27 Meaning: L'David Hashem Ori",
 "psalm-91-meaning-yoshev-bseter-elyon": "Psalm 91 Meaning: The Jewish Song of Protection",
 "tefilat-haderech-travelers-prayer": "What Is Tefilat HaDerech? The Traveler's Prayer",
 "tehillim-for-anxiety": "Tehillim for Anxiety: 7 Psalms to Calm the Mind",
 "tehillim-for-healing": "Tehillim for Healing: Psalms for a Refuah Shlema",
 "tikkun-leil-shavuot": "Tikkun Leil Shavuot: All-Night Torah Learning",
 "what-does-baruch-hashem-mean": 'What Does "Baruch Hashem" Mean?',
 "what-is-a-dopamine-detox": "What Is a Dopamine Detox? A Torah Perspective",
 "what-is-a-mezuzah": "What Is a Mezuzah? Meaning, Mitzvah & How to Hang",
 "what-is-chesed": "What Is Chesed? The Jewish Practice of Kindness",
 "what-is-daf-yomi": "What Is Daf Yomi? The Daily Talmud Cycle Explained",
 "what-is-doomscrolling": "What Is Doomscrolling? How to Break the Habit",
 "what-is-hakarat-hatov": "What Is Hakarat Hatov? Recognizing the Good",
 "what-is-hitbodedut": "What Is Hitbodedut? Personal Prayer Explained",
 "what-is-lag-baomer": "What Is Lag BaOmer? A Beginner's Guide",
 "what-is-mussar": "What Is Mussar? The Jewish Path of Character",
 "what-is-shacharit": "What Is Shacharit? The Jewish Morning Prayer",
 "what-is-shavuot": "What Is Shavuot? A Beginner's Guide to the Holiday",
 "what-is-simcha": "What Is Simcha? The Jewish Meaning of Joy",
 "what-is-tefillin": "What Is Tefillin? Meaning, Mitzvah & How to Wrap",
 "what-is-tehillim": "What Is Tehillim? A Guide to the Book of Psalms",
 "what-is-teshuvah": "What Is Teshuvah? The Jewish Meaning of Repentance",
 "what-is-the-amidah": "What Is the Amidah? The Jewish Standing Prayer",
 "what-is-the-kaddish": "What Is the Kaddish? The Mourner's Kaddish Explained",
 "what-is-the-shema": "What Is the Shema? Judaism's Most Sacred Prayer",
 "what-is-the-talmud": "What Is the Talmud? A Beginner's Guide",
 "what-is-the-yetzer-hara": "What Is the Yetzer Hara? The Jewish Inner Struggle",
 "what-is-tikkun-olam": "What Is Tikkun Olam? Repairing the World",
 "what-is-tzedakah": "What Is Tzedakah? The Jewish Approach to Giving",
 "what-the-torah-says-about-phone-addiction": "What the Torah Says About Phone Addiction",
 "which-tehillim-to-say-every-morning": "Which Tehillim to Say Every Morning",
}

# ---- parse blog.html for clusters + card titles ----
blog_html = (ROOT / "blog.html").read_text(encoding="utf-8")
cards = re.findall(
    r'<a href="blog/([^"]+)\.html" class="blog-card[^"]*" data-topic="([^"]+)">.*?<h2 class="blog-card-title">(.*?)</h2>',
    blog_html, re.S)
slug_topic, slug_title, topic_members = {}, {}, {}
for slug, topic, title in cards:
    title = title.strip()
    slug_topic[slug] = topic
    slug_title[slug] = title
    topic_members.setdefault(topic, []).append(slug)


def related_for(slug):
    topic = slug_topic.get(slug)
    members = topic_members.get(topic, [])
    if slug not in members or len(members) < 2:
        return []
    i = members.index(slug)
    return [members[(i + 1 + j) % len(members)] for j in range(min(3, len(members) - 1))]


def first(pat, text, default=""):
    m = re.search(pat, text)
    return m.group(1) if m else default


def common(text):
    """Edits applied to every page."""
    text = text.replace(
        '<link rel="apple-touch-icon" href="/assets/favicon.png">',
        '<link rel="apple-touch-icon" sizes="180x180" href="/assets/apple-touch-icon.png">\n'
        '  <link rel="manifest" href="/site.webmanifest">\n'
        '  <meta name="theme-color" content="#091B34">')
    text = text.replace('href="../index.html"', 'href="/"')
    text = text.replace('href="index.html"', 'href="/"')
    text = text.replace('&copy; 2025 Torah Lock', '&copy; 2026 Torah Lock')
    text = text.replace('Inter:wght@300;400;500;600;700', 'Inter:wght@400;500;600;700')
    return text


def process_post(path):
    slug = path.stem
    t = path.read_text(encoding="utf-8")
    url = first(r'<meta property="og:url" content="([^"]+)"', t)
    ogtitle = first(r'<meta property="og:title" content="([^"]+)"', t)
    ogdesc = first(r'<meta property="og:description" content="([^"]+)"', t)

    # 1. title
    if slug in TITLES:
        newt = htmllib.escape(TITLES[slug], quote=False)
        t = re.sub(r'<title>.*?</title>', f'<title>{newt}</title>', t, count=1, flags=re.S)

    # 2. canonical after description
    if 'rel="canonical"' not in t:
        t = re.sub(r'(<meta name="description"[^>]*>)',
                   r'\1\n  <link rel="canonical" href="%s">' % url, t, count=1)

    # 3. og:image + twitter after og:url
    if 'og:image' not in t and url:
        block = (f'<meta property="og:url" content="{url}">\n'
                 f'  <meta property="og:image" content="{OG}">\n'
                 f'  <meta property="og:site_name" content="Torah Lock">\n'
                 f'  <meta name="twitter:card" content="summary_large_image">\n'
                 f'  <meta name="twitter:title" content="{ogtitle}">\n'
                 f'  <meta name="twitter:description" content="{ogdesc}">\n'
                 f'  <meta name="twitter:image" content="{OG}">')
        t = t.replace(f'<meta property="og:url" content="{url}">', block, 1)

    # 4. schema enrich
    t = t.replace('"@type": "Article"', '"@type": "BlogPosting"')
    if '"image":' not in t:
        t = t.replace('"@type": "BlogPosting",',
                      '"@type": "BlogPosting",\n    "image": "%s",' % OG, 1)
    t = t.replace(
        '"publisher": { "@type": "Organization", "name": "Torah Lock", "url": "https://torahlock.app" }',
        '"publisher": { "@type": "Organization", "name": "Torah Lock", "url": "https://torahlock.app", "logo": { "@type": "ImageObject", "url": "%s" } }' % LOGO)

    # 5. breadcrumb before <!-- Fonts -->
    if 'BreadcrumbList' not in t and url:
        name3 = json.dumps(htmllib.unescape(ogtitle))
        item3 = json.dumps(url)
        crumb = (
            '  <script type="application/ld+json">\n'
            '  { "@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [\n'
            '    {"@type":"ListItem","position":1,"name":"Home","item":"https://torahlock.app/"},\n'
            '    {"@type":"ListItem","position":2,"name":"Blog","item":"https://torahlock.app/blog.html"},\n'
            f'    {{"@type":"ListItem","position":3,"name":{name3},"item":{item3}}}\n'
            '  ] }\n'
            '  </script>\n\n'
            '  <!-- Fonts -->')
        t = t.replace('  <!-- Fonts -->', crumb, 1)

    # 6. FAQ <p><strong>Q?</strong> A</p> -> <h3>Q?</h3><p>A</p> (only inside FAQ section)
    m = re.search(r'(<h2[^>]*>[^<]*(?:Frequently Asked Questions|FAQ)[^<]*</h2>)(.*?)(?=<h2|<!-- Read Next|</article>)', t, re.S | re.I)
    if m:
        body = re.sub(r'<p><strong>([^<]*\?)</strong>\s*(.*?)</p>',
                      r'<h3 class="blog-faq-q">\1</h3>\n      <p>\2</p>', m.group(2), flags=re.S)
        t = t[:m.start(2)] + body + t[m.end(2):]

    # 7. CTA + related reading before footer block
    if 'post-cta' not in t:
        rel = related_for(slug)
        rel_html = ""
        if rel:
            links = "\n".join(
                f'          <a href="{s}.html" class="blog-related-link">{slug_title.get(s, s)}</a>'
                for s in rel)
            rel_html = (
                '\n      <div class="blog-related">\n'
                '        <p class="blog-related-label">Related reading</p>\n'
                '        <div class="blog-related-grid">\n'
                f'{links}\n'
                '        </div>\n'
                '      </div>\n')
        cta = (
            '\n      <aside class="post-cta">\n'
            '        <p>Torah Lock guards your morning prayer before the day pulls you away &mdash; Shema and personalized Tehillim in under five minutes.</p>\n'
            f'        <a href="{APP_BLOG}" class="btn btn-gold" target="_blank" rel="noopener">Download on the App Store</a>\n'
            '      </aside>\n'
            f'{rel_html}\n'
            '      <!-- Read Next -->')
        t = t.replace('\n      <!-- Read Next -->', cta, 1)

    t = common(t)
    path.write_text(t, encoding="utf-8")
    return slug


def process_index():
    p = ROOT / "index.html"
    t = p.read_text(encoding="utf-8")
    t = t.replace('href="#"', f'href="{APP}" target="_blank" rel="noopener"')
    t = t.replace(
        '<meta name="description" content="Torah Lock blocks distracting apps each morning until you complete Shema and personalized Tehillim. A Jewish prayer app that helps you put Hashem first. Under 5 minutes. Free to try.">',
        '<meta name="description" content="Torah Lock blocks distracting apps each morning until you finish a short Jewish prayer — Shema and personalized Tehillim. Under 5 minutes. Free on iOS.">')
    t = t.replace(
        '<meta property="og:image" content="https://torahlock.app/assets/screenshots/torah-lock-home-screen.png">',
        f'<meta property="og:image" content="{OG}">')
    t = t.replace(
        '<meta name="twitter:image" content="https://torahlock.app/assets/screenshots/torah-lock-home-screen.png">',
        f'<meta name="twitter:image" content="{OG}">')
    # SoftwareApplication enrich
    t = t.replace(
        '    "screenshot": "https://torahlock.app/assets/screenshots/torah-lock-home-screen.png"\n  }',
        '    "url": "https://torahlock.app/",\n'
        '    "installUrl": "https://apps.apple.com/app/apple-store/id6759348814",\n'
        '    "downloadUrl": "https://apps.apple.com/app/apple-store/id6759348814",\n'
        '    "screenshot": [\n'
        '      "https://torahlock.app/assets/screenshots/torah-lock-home-screen.png",\n'
        '      "https://torahlock.app/assets/screenshots/torah-lock-shema-prayer.png",\n'
        '      "https://torahlock.app/assets/screenshots/torah-lock-tehillim-hebrew.png"\n'
        '    ]\n  }')
    # Organization enrich
    t = t.replace(
        '    "url": "https://torahlock.app",\n    "description": "A Jewish morning prayer app that blocks distracting apps until you pray."',
        '    "url": "https://torahlock.app",\n'
        '    "logo": "https://torahlock.app/assets/favicon.png",\n'
        '    "sameAs": [ "https://apps.apple.com/app/apple-store/id6759348814" ],\n'
        '    "description": "A Jewish morning prayer app that blocks distracting apps until you pray."')
    # reduced motion
    t = t.replace(
        '    function startAutoplay() {\n      autoplayTimer = setInterval(function() { goTo(current + 1); }, 4000);\n    }',
        '    function startAutoplay() {\n      if (window.matchMedia && window.matchMedia(\'(prefers-reduced-motion: reduce)\').matches) return;\n      autoplayTimer = setInterval(function() { goTo(current + 1); }, 4000);\n    }')
    # <picture> wrap screenshots
    if '<picture>' not in t:
        t = re.sub(r'<img src="assets/screenshots/([a-z0-9-]+)\.png"([^>]*?)>',
                   r'<picture><source srcset="assets/screenshots/\1.webp" type="image/webp"><img src="assets/screenshots/\1.png"\2></picture>',
                   t)
    t = common(t)
    p.write_text(t, encoding="utf-8")


def process_blog():
    p = ROOT / "blog.html"
    t = p.read_text(encoding="utf-8")
    t = t.replace('<title>Blog — Torah Lock</title>',
                  '<title>The Torah Lock Blog — Jewish Prayer & Digital Wellness</title>')
    if 'rel="canonical"' not in t:
        ins = (
            '  <link rel="canonical" href="https://torahlock.app/blog.html">\n'
            '  <meta property="og:type" content="website">\n'
            '  <meta property="og:title" content="The Torah Lock Blog — Jewish Prayer & Digital Wellness">\n'
            '  <meta property="og:description" content="Insights on Jewish prayer, Tehillim, and building a deeper connection with Hashem in a distracted world.">\n'
            '  <meta property="og:url" content="https://torahlock.app/blog.html">\n'
            f'  <meta property="og:image" content="{OG}">\n'
            '  <meta property="og:site_name" content="Torah Lock">\n'
            '  <meta name="twitter:card" content="summary_large_image">\n'
            '  <meta name="twitter:title" content="The Torah Lock Blog">\n'
            '  <meta name="twitter:description" content="Insights on Jewish prayer, Tehillim, and digital wellness.">\n'
            f'  <meta name="twitter:image" content="{OG}">\n'
            '  <script type="application/ld+json">\n'
            '  { "@context":"https://schema.org","@type":"Blog","name":"The Torah Lock Blog","url":"https://torahlock.app/blog.html","description":"Insights on Jewish prayer, Tehillim, and digital wellness.","publisher":{"@type":"Organization","name":"Torah Lock","logo":{"@type":"ImageObject","url":"%s"}}}\n'
            '  </script>\n'
            '  <script type="application/ld+json">\n'
            '  { "@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[\n'
            '    {"@type":"ListItem","position":1,"name":"Home","item":"https://torahlock.app/"},\n'
            '    {"@type":"ListItem","position":2,"name":"Blog","item":"https://torahlock.app/blog.html"}\n'
            '  ] }\n'
            '  </script>\n') % LOGO
        t = t.replace(
            '<meta name="description" content="Insights on Jewish prayer, digital wellness, and building a deeper connection with Hashem. The Torah Lock blog.">',
            '<meta name="description" content="Insights on Jewish prayer, digital wellness, and building a deeper connection with Hashem. The Torah Lock blog.">\n' + ins)
    t = common(t)
    p.write_text(t, encoding="utf-8")


LEGAL = {
 "privacy.html": "Read the Torah Lock privacy policy. We minimize data collection — app restrictions run on-device via Apple Screen Time, and we never sell your data.",
 "terms.html": "The Torah Lock terms of service: the rules and conditions for using the Torah Lock iOS app and website.",
}


def process_legal():
    for fname, desc in LEGAL.items():
        p = ROOT / fname
        t = p.read_text(encoding="utf-8")
        title = first(r'<title>([^<]*)</title>', t)
        url = f"https://torahlock.app/{fname}"
        if 'name="description"' not in t:
            ins = (
                f'  <meta name="description" content="{desc}">\n'
                f'  <link rel="canonical" href="{url}">\n'
                '  <meta property="og:type" content="website">\n'
                f'  <meta property="og:title" content="{title}">\n'
                f'  <meta property="og:url" content="{url}">\n'
                f'  <meta property="og:image" content="{OG}">\n'
                '  <meta property="og:site_name" content="Torah Lock">\n'
                '  <meta name="twitter:card" content="summary_large_image">\n'
                f'  <meta name="twitter:image" content="{OG}">')
            t = re.sub(r'(<title>[^<]*</title>)', r'\1\n' + ins.replace('\\', '\\\\'), t, count=1)
        t = common(t)
        p.write_text(t, encoding="utf-8")


CSS = """

/* === SEO components (post CTA, related reading, FAQ headings) === */
.post-cta {
  background: var(--primary);
  border-radius: var(--radius-lg);
  padding: 2.75rem 2rem;
  text-align: center;
  margin: 3.5rem 0 2.5rem;
}
.post-cta p {
  color: var(--white);
  font-size: 1.1rem;
  line-height: 1.6;
  margin: 0 0 1.5rem;
  opacity: 0.92;
}
.blog-related {
  margin: 2.5rem 0;
  padding-top: 2rem;
  border-top: 1px solid var(--border);
}
.blog-related-label {
  font-family: 'Inter', sans-serif;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--gold);
  margin: 0 0 1rem;
}
.blog-related-grid { display: grid; gap: 0.6rem; }
.blog-related-link {
  display: block;
  padding: 0.85rem 1.1rem;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  color: var(--primary);
  text-decoration: none;
  font-weight: 500;
  transition: border-color var(--transition), background var(--transition);
}
.blog-related-link:hover { border-color: var(--gold); background: var(--bg-subtle); }
.blog-faq-q {
  font-family: 'Lora', Georgia, serif;
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--primary);
  margin: 1.75rem 0 0.5rem;
}
"""


def append_css():
    p = ROOT / "styles.css"
    t = p.read_text(encoding="utf-8")
    if '/* === SEO components' not in t:
        p.write_text(t + CSS, encoding="utf-8")


def main():
    posts = sorted((ROOT / "blog").glob("*.html"))
    done = []
    for path in posts:
        if path.stem in THIN:
            continue
        done.append(process_post(path))
    process_index()
    process_blog()
    process_legal()
    append_css()
    print(f"Processed {len(done)} posts + index + blog + legal.")
    missing_title = [s for s in done if s not in TITLES]
    if missing_title:
        print("WARN: no title mapping for:", missing_title)


if __name__ == "__main__":
    main()
