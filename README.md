# Marc Duboc — Personal Portfolio

This repository is my personal portfolio site: a small, hand-crafted static site (HTML, CSS, JS) that documents projects, essays, and contact details. I maintain the content directly — no build step, no framework — because clarity and control matter to how I present my work.

What this repo contains
- `main.html` — home page (projects, current reading, essay teasers)
- `essays.html` — essays index
- `essays/<slug>/index.html` — individual essays
- `projects/` — project pages and project-specific assets
- `css/`, `pictures/`, `projects/*/images/` — styles and images

Quick local run
- You can open `main.html` directly in a browser for a quick look.
- For accurate testing of relative links, serve the folder:

```portfolio/README.md#L1-3
python3 -m http.server 8000
```

Then open: `http://localhost:8000/main.html`

Common maintenance tasks
- Verify essays exist under `essays/<slug>/index.html`.
- If you move or rename files, update `href` values in `main.html` and `essays.html`.
- Search for legacy or broken essay links:

```portfolio/README.md#L4-6
grep -R "essay-" -n . || true
grep -R "essays/" -n . || true
```

Deployment guidance
- This is static content. Deploy to GitHub Pages, Netlify, Vercel, S3 + CDN, or any static host.
- If you prefer clean folder URLs (e.g. `/essays/<slug>/`), ensure the host serves `index.html` by folder or keep explicit `index.html` in links.

Contributing
- Make focused changes (text, images, links) and open a PR.
- Test locally before submitting.
- If you rename a folder or slug, update all affected `href`s and mention the change in the PR.

License & contact
- Add a `LICENSE` file if you want explicit reuse terms (MIT, etc.).
- My contact email is included in `main.html`.

Notes
This README is intentionally concise and personal. If you want, I can:
- add a small link-check script (Python or Node),
- create a short GitHub Pages deployment guide with exact commands,
- or convert links to trailing‑slash style and update references.