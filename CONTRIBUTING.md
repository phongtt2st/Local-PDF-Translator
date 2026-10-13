# Contributing to the legacy implementation

Keep changes focused on preserving and documenting the original behavior. Discuss larger redesigns separately. This project's source code is licensed under **AGPL-3.0-only**; see [LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Submit only contributions you have the right to provide under these terms.

1. Clone the actual repository using the placeholder-replacement instructions in [README.md](README.md), or fork it once a remote exists.
2. In Windows CMD, create an environment, install dependencies, and work on a branch:

   ```bat
   python -m venv .venv
   .venv\Scripts\activate.bat
   python -m pip install -r requirements.txt
   git switch -c your-change-name
   ```

3. Run safe checks before submitting:

   ```bat
   python -B -c "from pathlib import Path; p = Path('pdf_translator.py'); compile(p.read_bytes(), str(p), 'exec'); print('Syntax OK')"
   python -B -c "import pymupdf, ollama; from docx import Document; print('Imports OK')"
   git diff --check
   git diff
   git status --short
   ```

   These syntax/import checks do not translate documents or contact Ollama. There is no automated translation test suite. For behavior changes, describe a manual check using your own non-sensitive, redistributable PDF and a local model. Inspect the DOCX, including any failure markers; do not claim an end-to-end test from import checks alone. Run manual translation only when you intend to process that document.

4. Explain the change and the checks performed in your pull request, including any checks you could not run.

Never commit private PDFs, generated DOCX files, models, virtual environments, logs, keys, credentials, or personal data. Inspect local path edits in `pdf_translator.py`; `.gitignore` cannot hide sensitive strings inside tracked source. Restore private configuration before staging. Before committing, inspect `git diff --cached` and `git status`; ignored files can still be force-added, and already tracked files remain tracked.
