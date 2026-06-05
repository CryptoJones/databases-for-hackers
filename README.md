# Databases for Hackers

A 45-minute stand-up talk / webinar for **Ronin 48**, aimed at people coming
into security without a computer-science background — entry-level SOC analysts,
junior pentesters, and GRC folks moving into technical work.

It walks through how databases actually work and how they get attacked and
defended: SQL and NoSQL injection, cloud misconfigurations, the shared
responsibility model, and the security questions around RAG / vector databases —
no CS degree required.

## Watch

All seven narrated versions are on YouTube
([**@0xCryptoJones**](https://www.youtube.com/@0xCryptoJones)):

| Language | Video |
| --- | --- |
| English | [Databases for Hackers](https://www.youtube.com/watch?v=PN6ZfugD9Tw) |
| Spanish | [Bases de datos para hackers](https://www.youtube.com/watch?v=lHDsoEFpTzs) |
| French | [Les bases de données pour les hackers](https://www.youtube.com/watch?v=_2RhH8lBwTM) |
| German | [Datenbanken für Hacker](https://www.youtube.com/watch?v=TPNOON-02II) |
| Russian | [Базы данных для хакеров](https://www.youtube.com/watch?v=kGu2mGZpdM8) |
| Chinese | [黑客眼中的数据库](https://www.youtube.com/watch?v=61-caqQVWHA) |
| Korean | [해커를 위한 데이터베이스](https://www.youtube.com/watch?v=vyqgDxAL18Q) |

## Contents

| File | What it is |
| --- | --- |
| `script.md` | Full speaker script (~6,000 words, ~140 wpm) |
| `script_timed.md`, `script_timed_<lang>.md` | The same script split per slide with `[SLIDE N]` markers, used to keep narration and captions in sync (English plus the six translations) |
| `slides.pptx` | Accessibility-first slide deck (English) |
| `slides_es.pptx` … `slides_ko.pptx` | Translated decks: Spanish, French, German, Russian, Chinese, Korean |
| `slides*.pdf` | A rendered PDF of each deck |
| `slides*.mp4` | Narrated video of each deck, paced to ~45 minutes |
| `slides_presentation.mp4` | English deck only — **un-narrated** presenter copy that advances on a slide-change chime (no voice track) |
| `slides*.srt` | Caption file for each narrated video |
| `audio/<lang>/slide_NN.mp3`, `audio/full_<lang>.mp3` | Narration audio, per slide and as one full-length track per language |
| `description_<lang>.txt` | YouTube title/description text for each video |
| `build_slides.py` | Generates the English deck with [python-pptx](https://python-pptx.readthedocs.io/) |
| `translate_slides.py` | Produces the translated decks from the English source |
| `apply_translation.py`, `autofit_pptx.py` | Deck-build helpers: apply a translation map by exact run match, then shrink fonts so longer translations don't overflow |
| `extract_quotes.py` | Helper that pulls quotes from reference material (sources not included — see below) |

## Building

```bash
pip install python-pptx
python build_slides.py      # regenerate slides.pptx
python translate_slides.py  # regenerate the translated decks
```

## Narration

Each language ships as a narrated video. The voice was produced with two tools:

- **English and Spanish** — the speaker's cloned voice via **ElevenLabs**.
- **French, German, Russian, Chinese, and Korean** — synthesized locally with
  **Coqui XTTS v2**.

The narration, video-assembly, and caption tooling lived in a separate local
workspace and is **not** included here, so the `build_slides.py` /
`translate_slides.py` steps above regenerate the decks but **not** the videos,
audio, or `.srt` captions — those ship as finished artifacts. If you want to
reproduce the full pipeline, [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md#the-full-pipeline-stage-by-stage)
documents every stage and its settings.

## A note on sources

The reference PDFs the talk draws from are copyrighted and are **not** included
in this repository (`source_books/` and the extracted `book_quotes.json` are
gitignored). The build scripts will reference them if present locally, but the
deck and script ship as standalone deliverables.

## License

[MIT](LICENSE) © 2026 aaron.clark@milcyber.org

Proudly Made in Nebraska. Go Big Red! 🌽 https://xkcd.com/2347/
