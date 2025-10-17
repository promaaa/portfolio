# Marc Duboc — Personal Portfolio

This repository contains my personal portfolio site: a small, hand-maintained static site (HTML, CSS, JS). I edit these files directly to publish projects, essays, and contact details. No build step or tooling required.

What’s included
- `main.html` — homepage (projects, current reading, essay teasers)
- `essays.html` — essay index
- `essays/<slug>/index.html` — individual essays
- `projects/` — project pages and assets
- `css/`, `pictures/`, `projects/*/images/` — styles and images

Run locally
- Quick: open `main.html` in your browser.
- Recommended: from the repo root run:
  ```
  python3 -m http.server 8000
  ```
  then open `http://localhost:8000/main.html`.

Simple checks and maintenance
- Verify each essay folder includes `index.html` (e.g. `essays/unspoken-dialogue/index.html`).
- If you move or rename pages, update `href` values in `main.html` and `essays.html`.
- Quick searches:
  ```
  grep -R "essay-" -n . || true
  grep -R "essays/" -n . || true
  ```

Deployment
- This is static content; deploy to GitHub Pages, Netlify, Vercel, S3 + CDN, or any static host.
- If you prefer folder-style URLs (e.g. `/essays/<slug>/`), ensure the host serves `index.html` for directory requests or keep explicit `index.html` links.

Contributing
- Keep changes focused (text, images, links).
- Test locally before opening a PR and describe any structural changes (renames, moved folders).
- If you rename slugs, update all affected `href` values.

License
- I’ve added an MIT license to this repository. See `LICENSE` for details.

— Marc Duboc