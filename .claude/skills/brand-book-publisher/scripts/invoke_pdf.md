# Handing off to anthropic-skills:pdf

This is a prompt template for invoking the `anthropic-skills:pdf` skill from `brand-book-publisher` for **post-processing** the PDF produced by `canvas-design`.

Skip this step if no post-processing is needed.

---

## When to invoke

- The user wants the infographic page appended to the PDF.
- The user wants bookmarks / outline added.
- The user wants metadata embedded (title, author).
- The user wants the PDF watermarked or password-protected.
- The user wants multiple PDFs merged.

## Request template (append infographic as final page)

```
Take the existing PDF at:
  /Users/erikgamboa/Documents/CMO/projects/{{SLUG}}/03-brand-book.pdf

Append a new final page containing the image at:
  /Users/erikgamboa/Documents/CMO/projects/{{SLUG}}/03-brand-book-infographic.png

The new page should be A4 portrait with the image centered, scaled to fit with 1.5cm margin.

Add PDF metadata:
  Title: "{{BRAND_NAME}} — Brand Book"
  Author: "{{BRAND_NAME}}"
  Subject: "Manual de marca"
  Keywords: "brand book, identidad, {{BRAND_NAME}}"

Save back to the same path: /Users/erikgamboa/Documents/CMO/projects/{{SLUG}}/03-brand-book.pdf
```

## Request template (only metadata + bookmarks)

```
Modify the PDF at:
  /Users/erikgamboa/Documents/CMO/projects/{{SLUG}}/03-brand-book.pdf

Add metadata:
  Title: "{{BRAND_NAME}} — Brand Book"
  Author: "{{BRAND_NAME}}"

Add bookmarks (outline) matching the section headings detected in the document.

Save back to the same path.
```

## Notes

- Do not let `pdf` regenerate the document — it should only post-process.
- If `anthropic-skills:pdf` isn't available, skip post-processing silently and report the limitation to the user. Canvas-design's raw PDF output is still usable.
