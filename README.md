# Timothy Lee portfolio

Static site: plain HTML, CSS, and a little JavaScript. Hosted on GitHub Pages from `main`.

- `build.py` regenerates every page from the content inside it (run `python build.py`). Edit content there, not in the HTML files.
- `style.css` holds the design; `site.js` adds the image lightbox, scroll effects, and table-of-contents highlighting.
- Put photos in `images/` and videos in `videos/` using the file names in `build.py`.
- Text in [brackets], such as `[Caption]` or `[Text: ...]`, is a note to self and stays hidden on the live site.
- Missing images are hidden on the live site. To see placeholders for them and the bracketed notes, preview locally
  (`python -m http.server`, then open http://localhost:8000) or add `?drafts` to any live URL.
- Publish: `git add -A && git commit -m "..." && git push`
