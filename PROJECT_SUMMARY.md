# Databases for Hackers — Project Summary

A complete record of this project, from the initial idea through to the final
cleanup. Written in English. Contains no secrets, keys, or credentials.

## The idea

"Databases for Hackers" is a 45-minute stand-up talk / webinar built for
**Ronin 48**. The premise: *every breach you've ever read about ends at a
database.* The goal was to explain how databases actually work — and how they
get attacked and defended — for people entering security **without** a
computer-science background: entry-level SOC analysts, junior pentesters, and
GRC professionals moving into technical work. No CS degree required.

Topics covered include SQL and NoSQL injection, cloud misconfigurations, the
shared responsibility model, and the newer security questions around RAG /
vector databases.

## Deliverables

| Artifact | Description |
| --- | --- |
| `script.md` | Full speaker script (~6,000 words at ~140 wpm) |
| `slides.pptx` | Accessibility-first English slide deck (~40 slides) |
| `slides_es/fr/de/ru/zh/ko.pptx` | Translated decks: Spanish, French, German, Russian, Chinese, Korean |
| Rendered PDFs | One per deck, for distribution and review |
| Narrated videos (`.mp4`) | One per language, paced to ~45 minutes |
| Narration audio + `.srt` captions | Per language, for accessibility |
| Build tooling | `build_slides.py`, `translate_slides.py`, `extract_quotes.py` |

Seven languages total: **English, Spanish, French, German, Russian, Chinese,
Korean.**

## How it was built (chronological)

1. **Script & source research.** The speaker script was written first, drawing
   on reference material. The source PDFs are copyrighted and were deliberately
   **kept out of the repository** (`source_books/` and the extracted
   `book_quotes.json` are gitignored); the deck and script ship as standalone
   deliverables.
2. **English deck.** `build_slides.py` generates `slides.pptx` programmatically
   with [python-pptx](https://python-pptx.readthedocs.io/), built
   accessibility-first.
3. **Translations.** `translate_slides.py` produces the six translated decks
   from the English source. The OWASP year reference was corrected to **2025**.
4. **Rendering.** Each deck was exported to PDF and to a ~45-minute paced video.
5. **Narration & captions.** Narration audio was produced per language, videos
   were rebuilt in narrated and un-narrated variants, and `.srt` caption files
   were generated for each language.
6. **Licensing & docs.** A `README.md` and an **MIT license** were added,
   © 2026 aaron.clark@milcyber.org.
7. **YouTube descriptions.** Per-language description files
   (`description_<lang>.txt`) were authored for each video.
8. **YouTube publishing & metadata fix** *(this phase)* — see below.

## Publishing to YouTube

All seven narrated videos were uploaded to YouTube. Their **titles** and
**descriptions** were then standardized programmatically.

### Titles

Each title follows the pattern *"<localized title> (<native language name>)"*,
so each video is labeled in its own language:

| Language | Final title |
| --- | --- |
| English | Databases for Hackers (English) |
| Spanish | Bases de datos para hackers (Español) |
| French  | Les bases de données pour les hackers (Français) |
| German  | Datenbanken für Hacker (Deutsch) |
| Russian | Базы данных для хакеров (Русский) |
| Chinese | 黑客眼中的数据库 (中文) |
| Korean  | 해커를 위한 데이터베이스 (한국어) |

### Descriptions

Each video received its matching `description_<lang>.txt` content.

### Tooling

A small local-only helper (`update_youtube_descriptions.py`, gitignored)
pushes the title and description for each language to the YouTube Data API v3.
Notes on how it works:

- Editing your own videos is a **write** operation, so it uses **OAuth 2.0**
  (a read-only API key is not sufficient).
- The OAuth desktop-app credential and the cached login token were stored
  **locally only**, were **gitignored**, were **never committed**, and were
  **deleted during final cleanup** (see below). No credentials appear anywhere
  in this repository.
- The script supports `--list` (enumerate uploads), `--dry-run` (preview
  changes without writing), and a real apply mode.
- A duplicate Spanish upload existed (one public, one older unlisted preview).
  Only the **public** video was updated; the unlisted preview was left
  untouched.

### Verification

After applying, all seven videos were **read back from YouTube** and their live
titles and descriptions were compared field-by-field against the intended
values. All seven matched exactly.

## Final cleanup

To leave the workspace and repository clean and credential-free:

- Removed the local OAuth desktop-app credential and the cached login token.
- Removed a stray copy of the credential from the Downloads folder.
- Removed temporary working files created during publishing (a setup guide, a
  run log, an error-detail note, and a convenience launcher script).
- Confirmed no credential or token files remain in the project directory.

The reusable, gitignored description-update tool was kept in place (it contains
no secrets), so the metadata can be refreshed later by re-authorizing.

## Reproducing the build

```bash
pip install python-pptx
python build_slides.py      # regenerate slides.pptx (English)
python translate_slides.py  # regenerate the six translated decks
```

The reference source material is not distributed; the build scripts use it only
if present locally.

## Distribution

This repository is mirrored on both **GitHub** and **Codeberg** under
`CryptoJones/databases-for-hackers`. This summary is published to both.

## License

[MIT](LICENSE) © 2026 aaron.clark@milcyber.org

Proudly Made in Nebraska. Go Big Red! 🌽 https://xkcd.com/2347/
