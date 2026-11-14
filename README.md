# iterrate.in

Website of Iterrate (OPC) Private Limited, served by GitHub Pages from the `docs/` folder.

- Page texts, header and footer live in `src/build.py`. Edit them there, then run `python3 src/build.py` to regenerate `docs/*.html`.
- Styles: `docs/style.css`. The home-page loop is drawn by `docs/loop.js`.
- Annual returns (Companies Act s.92(3)) go in `docs/annual-returns/`, published without their attachments, and get a row on `company.html` (edit in `build.py`).
- `docs/CNAME` sets the custom domain; `docs/.nojekyll` stops GitHub running Jekyll.
