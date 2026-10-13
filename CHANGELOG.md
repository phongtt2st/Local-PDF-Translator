# Changelog

## Unreleased

- Added installation, configuration, usage, privacy, and limitation documentation for the legacy script.
- Added direct runtime dependency constraints, Git ignore rules, and line-ending/binary-file attributes.
- Added contribution guidance, security guidance, and third-party licensing references.
- Selected AGPL-3.0-only for the project's source code and added the official GNU AGPL v3 license text. Documented PyMuPDF's open-source AGPL route and the separate licenses/terms of dependencies and external models.
- Preserved `pdf_translator.py` unchanged; no translation behavior was added or redesigned.

## Legacy initial version

- Preserved original single-file implementation; no historical release number or date is established.
- Extracts PDF blocks page by page and requests Vietnamese translations through Ollama, with `gemma2` configured.
- Writes DOCX headings and paragraphs, saves after each page, and attempts a save on Ctrl+C during processing.
- Retries translation failures and retains the original block with an error marker if retries are exhausted.
