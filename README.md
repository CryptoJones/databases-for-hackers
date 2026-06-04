# Databases for Hackers

A 45-minute stand-up talk / webinar for **Ronin 48**, aimed at people coming
into security without a computer-science background — entry-level SOC analysts,
junior pentesters, and GRC folks moving into technical work.

It walks through how databases actually work and how they get attacked and
defended: SQL and NoSQL injection, cloud misconfigurations, the shared
responsibility model, and the security questions around RAG / vector databases —
no CS degree required.

## Contents

| File | What it is |
| --- | --- |
| `script.md` | Full speaker script (~6,000 words, ~140 wpm) |
| `slides.pptx` | Accessibility-first slide deck (English) |
| `slides_es.pptx` … `slides_ko.pptx` | Translated decks: Spanish, French, German, Russian, Chinese, Korean |
| `build_slides.py` | Generates the English deck with [python-pptx](https://python-pptx.readthedocs.io/) |
| `translate_slides.py` | Produces the translated decks from the English source |
| `extract_quotes.py` | Helper that pulls quotes from reference material (sources not included — see below) |

## Building

```bash
pip install python-pptx
python build_slides.py      # regenerate slides.pptx
python translate_slides.py  # regenerate the translated decks
```

## A note on sources

The reference PDFs the talk draws from are copyrighted and are **not** included
in this repository (`source_books/` and the extracted `book_quotes.json` are
gitignored). The build scripts will reference them if present locally, but the
deck and script ship as standalone deliverables.

## License

[MIT](LICENSE) © 2026 Aaron K. Clark
