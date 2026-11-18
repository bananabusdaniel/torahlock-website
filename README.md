# Torah Lock website

Static website for [Torah Lock](https://torahlock.app), published to GitHub Pages by `.github/workflows/static.yml` when `main` is pushed.

## Local preview

Run `python3 -m http.server 4371 --bind 127.0.0.1` from this folder, then open `http://127.0.0.1:4371`.

`styles.css` retains the article layouts; `refresh.css` contains the shared visual refresh and mobile homepage styles. `site.js` handles the navigation, accessible screenshot tabs, and Android waitlist feedback. No build step is required.

## Android waitlist

The form at `/#android-waitlist` sends signups to the owner's connected Gmail address through FormSubmit. The public form alias in the form action hides the recipient address; it is not an API secret. Emails use the subject **Torah Lock — Android waitlist signup** and contain the subscriber's email and launch-update consent. Search Gmail for that subject to collect or export the list. FormSubmit also retains a submission archive for 30 days.

JavaScript keeps signup on the page and only confirms success after the service accepts it. Without JavaScript, the standard POST redirects to `android-thanks.html`. A honeypot catches simple bot submissions. The privacy policy describes the email collection and removal process.

## App Store credibility

The homepage shows the US App Store rating, verified on November 19, 2026: **4.9 / 5 from 75 ratings**. The carousel contains excerpts of verified five-star App Store reviews by Hof_Coral and IMBUSY. These values are static; verify them against the linked App Store listing before updating. Screenshot sources are recorded in `asset-provenance.json`.
