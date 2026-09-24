# canon-lawyer.ca

Website for Richard Verver, JCL, Canon Lawyer. Served by GitHub Pages from the `docs/` folder.

## Editing

- Page content lives in `_src/pages/*.html` (the comment block at the top holds the title, description and URL).
- Shared header, footer, SEO tags and site settings (email, form endpoint) are in `build.py`.
- Styles: `docs/assets/css/site.css`. Images: `docs/assets/img/`.

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
