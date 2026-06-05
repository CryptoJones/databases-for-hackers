# Databases for Hackers — Project Summary

A historical record of this project, from the initial idea through to the final
cleanup. The talk is finished and its videos are published, so this repository
exists for **reference rather than active development**. For the canonical
file-by-file listing and the build commands, see the [README](README.md) — this
document tells the story of how it was made. Written in English. Contains no
secrets, keys, or credentials.

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

Seven languages total: **English, Spanish, French, German, Russian, Chinese,
Korean.** Each language ships as a slide deck (`.pptx`), a rendered PDF, a
narrated video, narration audio, and `.srt` captions, all built from a single
~6,000-word speaker script; English additionally has an un-narrated presenter
copy (`slides_presentation.mp4`). The
[README Contents table](README.md#contents) is the single source of truth for
the full file-by-file listing — it lives there so the two documents don't drift.

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
5. **Narration & captions.** Narration audio was produced per language (a
   narrated video for each of the seven), and `.srt` caption files were
   generated for each. The narration voice came from two tools:
   **English and Spanish** were rendered in the speaker's cloned voice via
   **ElevenLabs**, while **French, German, Russian, Chinese, and Korean** were
   synthesized locally with **Coqui XTTS v2**. English additionally has an
   **un-narrated presenter copy** (`slides_presentation.mp4`) that advances on a
   slide-change chime with no voice track — a personal-use deck for presenting
   live. The narration, video-assembly, and caption tooling lived in a separate
   local workspace and is **not** committed to this repository, so the media
   artifacts ship as finished files rather than as something the repo rebuilds.
6. **Licensing & docs.** A `README.md` and an **MIT license** were added,
   © 2026 aaron.clark@milcyber.org.
7. **YouTube descriptions.** Per-language description files
   (`description_<lang>.txt`) were authored for each video.
8. **YouTube publishing & metadata fix** *(this phase)* — see below.

## Publishing to YouTube

All seven narrated videos were uploaded to the
[**0xCryptoJones** channel](https://www.youtube.com/@0xCryptoJones) on YouTube.
Their **titles** and **descriptions** were then standardized programmatically.

### Titles

Each title follows the pattern *"<localized title> (<native language name>)"*,
so each video is labeled in its own language:

| Language | Final title | Watch |
| --- | --- | --- |
| English | Databases for Hackers (English) | https://www.youtube.com/watch?v=PN6ZfugD9Tw |
| Spanish | Bases de datos para hackers (Español) | https://www.youtube.com/watch?v=lHDsoEFpTzs |
| French  | Les bases de données pour les hackers (Français) | https://www.youtube.com/watch?v=_2RhH8lBwTM |
| German  | Datenbanken für Hacker (Deutsch) | https://www.youtube.com/watch?v=TPNOON-02II |
| Russian | Базы данных для хакеров (Русский) | https://www.youtube.com/watch?v=kGu2mGZpdM8 |
| Chinese | 黑客眼中的数据库 (中文) | https://www.youtube.com/watch?v=61-caqQVWHA |
| Korean  | 해커를 위한 데이터베이스 (한국어) | https://www.youtube.com/watch?v=vyqgDxAL18Q |

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

The deck build commands live in the [README](README.md#building); they
regenerate the **decks** only. The reference source material is not distributed
(the scripts use it only if present locally), and the videos, narration audio,
and captions were built with local-only tooling that is not in this repository,
so those media artifacts are preserved here as finished files. The end-to-end
pipeline is described below for anyone who wants to reproduce the full process.

### The full pipeline, stage by stage

The repository ships the **deck** tooling (`build_slides.py`,
`translate_slides.py`, `apply_translation.py`, `autofit_pptx.py`,
`extract_quotes.py`). The **render, narration, video, caption, and publish**
steps ran from a separate local workspace whose scripts are **not committed** —
so those stages are documented here, with the load-bearing settings, rather than
shipped as runnable code. The script names below (`eleven_generate.py`,
`xtts_batch.py`, `build_narrated_video.py`, `update_youtube_descriptions.py`)
refer to those local-only helpers.

**Prerequisites**

- Python: `python-pptx`, `requests`, `Pillow`; for the robot voices `TTS`
  (Coqui) + `torch` (a CUDA GPU is strongly recommended for XTTS).
- System: `ffmpeg` **built with `librubberband`** (used for the formant-preserved
  pitch shift), LibreOffice (headless PDF export), and Poppler (`pdftoppm`).
- Accounts: an **ElevenLabs** account (Creator plan) with an API key, for the
  English + Spanish cloned voice only; a **YouTube Data API v3** OAuth 2.0
  desktop-app credential, for publishing.

**Stages**

1. **Script.** Write `script.md`, then split it into per-slide
   `script_timed_<lang>.md` files with `[SLIDE N]` markers (localized marker
   words: `SLIDE`/`DIAPOSITIVA`/`DIAPOSITIVE`/`FOLIE`/`СЛАЙД`/`幻灯片`/`슬라이드`).
   The marker parser keeps only spoken lines, so the same text feeds both
   narration and captions.
2. **English deck.** `build_slides.py` → `slides.pptx` via python-pptx,
   accessibility-first.
3. **Translations.** `translate_slides.py` builds a per-language string map;
   `apply_translation.py` swaps run text by **exact match** (leaving code,
   ports, URLs, and citations verbatim); `autofit_pptx.py` shrinks fonts so the
   longer strings don't overflow → `slides_<lang>.pptx`.
4. **Render to frames.** Export each deck to PDF with LibreOffice headless, then
   rasterize to per-slide PNGs with `pdftoppm -scale-to-x 1920` (≈144 DPI),
   named `p-NN.png`.
5. **Narration.**
   - **EN + ES** — `eleven_generate.py`: ElevenLabs instant voice clone (IVC)
     from a clean voice sample, model `eleven_multilingual_v2`, voice settings
     `stability 0.45 / similarity_boost 0.8 / style 0 / speaker_boost on /
     speed 0.95`, followed by a **+0.5-semitone, formant-preserved** rubberband
     pitch shift and `loudnorm=I=-16:TP=-1.5:LRA=11`. (Local F5/XTTS were tried
     first for EN/ES and rejected for a "tin-can" resonance — the clean clone
     fixed it.)
   - **FR / DE / RU / ZH / KO** — `xtts_batch.py`: Coqui **XTTS v2**
     (`tts_models/multilingual/multi-dataset/xtts_v2`), synthesized per sentence
     with clause-boundary sub-splitting to stay under XTTS's ~400-token limit,
     then the same `loudnorm`.
   - Output for every language: `audio/<lang>/slide_NN.mp3` plus a concatenated
     `audio/full_<lang>.mp3`.
6. **Narrated video.** `build_narrated_video.py` holds each slide for
   `0.3s lead + len(slide_NN.mp3) + 0.8s tail`, renders 1920×1080 @30fps
   (libx264 / AAC 192k), and concatenates to `slides[_<lang>].mp4`. The silent
   English presenter copy (`slides_presentation.mp4`) uses a fixed per-slide
   hold with a slide-change chime instead of narration.
7. **Captions.** A `.srt` per language is generated from the same per-slide
   spoken text, timed to each slide's audio length — so caption text matches the
   narration exactly.
8. **Publish.** Upload the videos to YouTube; `update_youtube_descriptions.py`
   (local-only, OAuth 2.0) sets each video's localized title and pushes the
   matching `description_<lang>.txt`.

## Distribution

This repository is mirrored on both **GitHub** and **Codeberg** under
`CryptoJones/databases-for-hackers`. This summary is published to both.

## License

[MIT](LICENSE) © 2026 aaron.clark@milcyber.org

Proudly Made in Nebraska. Go Big Red! 🌽 https://xkcd.com/2347/
