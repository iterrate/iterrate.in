# iterrate.in

Website of Iterrate (OPC) Private Limited, served by GitHub Pages from the `docs/` folder.

- Page texts, header, footer and the milestone list live in `src/build.py`. Edit them there, then run `python3 src/build.py` to regenerate `docs/*.html`, `docs/sitemap.xml` and `docs/robots.txt`.
- Type straight quotes in `build.py`; the build turns them into curly ones.
- Styles: `docs/style.css` (light, dark and print). The home-page loop is drawn by `docs/loop.js`.
- Malayalam text: wrap it in `lang="ml"` (for example `<span lang="ml">…</span>`). The Noto Sans Malayalam font is only downloaded on pages that contain Malayalam.
- Link-preview image: `docs/share.png`, rendered from `src/share-image.html` (1200×630).
- `docs/404.html` is shown by GitHub for any missing address.
- `docs/CNAME` sets the custom domain; `docs/.nojekyll` stops GitHub running Jekyll.

## Each year, after the annual return (MGT-7A) is filed

1. Make a copy of the filed form **without its attachments** (they hold personal details).
2. Name it `Iterrate-MGT-7A-FY2026-27.pdf` (with that year) and put it in `docs/annual-returns/`.
3. Run `python3 src/build.py`. The Company page gets a new row by itself, newest first.
4. Publish, then give the CS the link for the board's report: https://iterrate.in/company.html#disclosures

## Fonts

Crimson Pro and Noto Sans Malayalam are under the SIL Open Font Licence 1.1.
