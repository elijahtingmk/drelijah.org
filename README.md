# Elijah Ting, ED – L&D — website redesign (publish-ready)

Static marketing site for [drelijah.org](https://drelijah.org). Cream / navy / gold design system. English only. No build step.

## Preview

```bash
python3 -m http.server 8765
```

Then open http://127.0.0.1:8765/ — or open `index.html` in a browser.

## Pages

| File | Purpose |
| --- | --- |
| `index.html` | Homepage |
| `solutions.html` | How the three solutions relate |
| `earned-leadership.html` | Earned Leadership™ |
| `workplace-resilience.html` | PR6 workplace resilience |
| `prisma.html` | PRisMA OSH compliance |
| `about.html` | Practitioner and credentials |
| `contact.html` | Scoping-call form + email |
| `privacy.html` | Privacy notice for the form (English and Bahasa Malaysia) |

Primary CTA: Book a 30-minute scoping call → `contact.html?need=…&from=…#book`

The form on `contact.html` posts to `https://big5.drelijah.org/api/enquiry` (the
`b5` Worker), which saves the request, sends a Telegram alert, and redirects back
to `contact.html?sent=1#book`. Booking buttons pass `need` (prisma, resilience,
leadership, coaching, unsure) to pre-select the form and `from` to record the page.

Spam protection: a hidden honeypot field and a minimum fill time. To add
Cloudflare Turnstile, put its site key in `data-turnstile-sitekey` on the form
and set `TURNSTILE_SECRET` on the b5 Worker.

## Stack

HTML, CSS, vanilla JS (`js/main.js`). Drop this folder on any static host.

## Package

Publish zip: `/workspace/drelijah-org-redesign.zip` (folder prefix `drelijah-org-redesign/`; screenshots excluded).
