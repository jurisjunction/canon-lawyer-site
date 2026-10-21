# canon-lawyer.ca

Website for Richard Verver, JCL, Canon Lawyer. Served by GitHub Pages from the `docs/` folder.

## Editing

- Page content lives in `_src/pages/*.html` (the comment block at the top holds the title, description and URL).
- Shared header, footer, SEO tags and site settings (email, form endpoint) are in `build.py`.
- Styles: `docs/assets/css/site.css`. Images: `docs/assets/img/`.
- The essays' Strudel tracks live in `docs/assets/music/`, and each names its parents in its header, one quoted line per edge with a short hash. `music.py` reads those headers, checks every hash and every parent, and writes the household (`family.strudel.js`, every track in one file), the family tree (`family.svg`), and the generated parts of the music page, `/music/`. After adding or changing a track, add it to `TRACKS` in `music.py` and run `python3 music.py && python3 build.py`.
- Essays are filed on the map of disciplines in `essay_map.py`. Give each essay `field: <slug>` (and, if it touches others, `also: <slug>, <slug>`) and a `summary:` in its comment block. The essays index, the page for each discipline, and each essay's breadcrumb and map links are generated from that file; the build refuses an unknown field or a cycle.

- Every piece of writing (essays, reflections, colloquies, explainers) gets a downloadable PDF next to its page, typeset by `pdfs.py` with [WeasyPrint](https://weasyprint.org) (`pip install weasyprint`). A PDF is rebuilt only when its text changes (hashes in `_src/pdf-manifest.json`). If WeasyPrint is not installed, the build still runs: out-of-date PDFs are not linked (the page offers print to PDF instead) and the build lists them.
- Essays and the pages of the homeschool curriculum (`/curriculum/`) are dedicated to the public domain under CC0 1.0: the notice, the licence link and the PDF colophon are added by the build. Reflections, colloquies and explainers stay all rights reserved. To exempt a page, add `license: reserved` to its comment block.
- The homeschool curriculum walks the same map, one unit page per field (`kind: unit` in its comment block; see `curriculum.py`). The build refuses a year that misses a field or takes one before what it draws on.

After editing, rebuild and commit:

```
python3 build.py
git add -A && git commit -m "Update site" && git push
```

GitHub Pages republishes automatically within a minute or two.

## Contact form

The form posts to [FormSubmit](https://formsubmit.co). The first submission triggers an activation
email to the address in `build.py`; click the link once and enquiries will arrive by email.
FormSubmit then offers a random alias you can put in `form_endpoint` to hide the address.

## Old URLs

`/home`, `/mission` and `/areas-of-practice` (from the old Google Site) redirect to the new pages.
