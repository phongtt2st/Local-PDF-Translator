# Local PDF Translator — Legacy

The original, single-file implementation of Local PDF Translator. It extracts text from a PDF, asks an Ollama model to translate each eligible text block into Vietnamese, and writes a Word document. This repository preserves `pdf_translator.py` without redesigning it.

This is the legacy implementation. A newer rewrite may exist separately; no rewrite URL is established here. This project's source code is licensed under **AGPL-3.0-only**; see [License](#license) and [Third-party notices](THIRD_PARTY_NOTICES.md).

## What it does

- Opens one PDF with PyMuPDF and processes its pages sequentially.
- Extracts blocks using `page.get_text("blocks")`, sorting by vertical position rounded into 5-point bands, then horizontal position.
- Sends each stripped block longer than three characters to `ollama.chat`, with a prompt requesting a complete Vietnamese translation. English text can be supplied, but the code neither detects nor restricts the source language.
- Creates a DOCX with a Vietnamese document heading, a numbered heading for each source page, and one paragraph per processed block.
- Retries a failed translation twice (three attempts total). If all attempts fail, writes a failure marker, the exception message, and the original block into the DOCX.
- Saves the DOCX after every completed page. Ctrl+C during the processing loop also attempts to save the work collected so far.
- Prints progress and errors to the console, then waits for Enter before exiting when run as a script.

## Requirements

- **Windows:** these instructions use Windows Command Prompt (CMD), not PowerShell. Use a Windows installation supported by [Ollama for Windows](https://docs.ollama.com/windows). The Python code uses portable APIs, but other operating systems have not been verified for this project.
- **Python 3.10 or newer** for the dependency baseline below; Python 3.12 is recommended because syntax and imports were checked on 3.12.3. The script has no explicit Python-version declaration. Older dependency combinations and other Python versions were not tested.
- **Ollama**, installed separately and running, with the **`gemma2`** model downloaded. Model inference needs sufficient memory and disk space; the script does not check hardware capacity.
- Three direct Python packages in `requirements.txt`:

  | Package | Constraint | Used for |
  | --- | --- | --- |
  | PyMuPDF | `>=1.28.2,<2` | Opening PDFs and extracting page blocks (`import pymupdf`). |
  | ollama | `>=0.6.2,<0.7` | Calling the Ollama chat API. |
  | python-docx | `>=1.2.0,<2` | Creating headings, paragraphs, and DOCX files (`from docx import Document`). |

The lower bounds match the installed versions whose imports were checked during repository preparation. They are a conservative setup baseline, not a claim about the oldest versions that could work. Upper bounds keep PyMuPDF and python-docx within their current major series and the pre-1.0 Ollama client within its current minor series. Other versions in these ranges have not been tested here. Pip installs their transitive dependencies automatically; standard-library modules need no separate installation.

Git is needed only for cloning/publishing. A DOCX viewer such as Word or LibreOffice is optional for reading results. Microsoft Word, Tesseract, Poppler, custom fonts, and a cloud API key are not required by this script. Typical PyMuPDF wheel installation needs no separate PDF tool; see its [installation documentation](https://pymupdf.readthedocs.io/en/latest/installation.html) if a compatible wheel is unavailable.

## Installation (Windows CMD)

Install [Python](https://www.python.org/downloads/windows/), [Git](https://git-scm.com/downloads/win) if cloning, and [Ollama](https://ollama.com/download/windows) separately.

If you already have this folder, open CMD inside it and skip cloning. Otherwise, replace **both uppercase placeholders** in the example URL with the real GitHub owner and repository. The URL below is a placeholder, not an existing project URL:

```bat
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git local-pdf-translator-legacy
cd local-pdf-translator-legacy
```

From the project folder:

```bat
python --version
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -c "import pymupdf, ollama; from docx import Document; print('Imports OK')"
```

Use the intended Python 3.10+ interpreter for `python`. Activate the same virtual environment in each new CMD window.

## Ollama setup

The active configuration is `MODEL_NAME = "gemma2"`. The original script's header contains an example mentioning `qwen2.5`; that example does **not** match the active configuration. Download `gemma2` for the unchanged model setting.

Open the Ollama application. If its server is not already running, run this in a separate CMD window and leave it open:

```bat
ollama serve
```

In the CMD window where you will run the translator, explicitly select the local server, verify that it responds, and download the configured model if needed:

```bat
set OLLAMA_HOST=http://127.0.0.1:11434
ollama list
ollama pull gemma2
ollama list
```

`ollama list` should return a model list without a connection error. After pulling, it should include `gemma2:latest`, the default tag for `gemma2`. Pulling downloads model files and can take significant time and disk space. The translator does not download models itself. See the official [model page](https://ollama.com/library/gemma2) and [CLI reference](https://docs.ollama.com/cli).

## Usage

There is no command-line argument parser, file picker, batch mode, or configuration file. You must edit the CONFIG section in `pdf_translator.py` before running it.

1. Choose a PDF containing selectable text. It may live anywhere you can read; no particular input directory is required.
2. Set `PDF_FILE_PATH` to the PDF filename and `OUTPUT_DOCX_PATH` to a **full output filename ending in `.docx`**, not merely a directory. Both values are empty in the preserved script. Blank paths resolve to the current directory and will not work as input/output filenames.
3. Keep `MODEL_NAME = "gemma2"` for this documented setup. It is editable in the source, but no alternative model is validated here.
4. Run from CMD with the virtual environment active and Ollama running:

   ```bat
   python pdf_translator.py
   ```

5. Wait for processing to finish, press Enter to exit, and open the configured DOCX. Check it for untranslated text and failure markers; the final `Done!` message does not prove that every translation succeeded.

Use raw strings (`r"..."`) for Windows paths. Absolute paths are least ambiguous; relative paths are resolved from the current working directory. The program creates missing output parent directories, provided it has permission. It overwrites the chosen DOCX without asking, so select a new filename for results you want to keep.

### Example workflow

Use your own non-sensitive, text-based PDF. From the project folder, optionally create a private input folder:

```bat
mkdir input
```

Place your PDF at `input\document.pdf`, then manually set these two lines in the script:

```python
PDF_FILE_PATH = r"input\document.pdf"
OUTPUT_DOCX_PATH = r"output\document_vi.docx"
```

With this folder as CMD's current directory, run `python pdf_translator.py`. The script creates `output` as needed and writes `output\document_vi.docx`. These names are illustrative; no sample PDF or translated document is bundled. The folders are optional and ignored by Git.

Local edits to the Python configuration remain changes to a source file that will normally be tracked. Before publishing, restore the two path settings to empty strings or inspect them carefully to prevent leaking personal paths and document names.

## Known limitations

- **No OCR.** Image-only/scanned PDFs do not yield their document text. Empty pages may produce only page headings. The code does not reject or warn about a scanned PDF.
- **No layout reconstruction.** Images, fonts, tables, equations, and source page breaks are not reproduced as structured content. Coordinate sorting is a heuristic and can interleave columns. The code does not filter block types; an image-description block, if returned by PyMuPDF, can be treated as text.
- Blocks with three or fewer stripped characters are skipped, potentially losing short labels, numbers, or words.
- Each block is translated independently. There is no shared document context, glossary, chunk-size control, explicit context-window setting, or validation of completeness/accuracy. Large blocks may exceed model limits. The prompt's request for a complete translation is not a guarantee.
- Processing is sequential. There is no progress percentage, cancellation UI, or parallel translation.
- **Page saves are not resumable checkpoints.** Rerunning starts from the first page with a new DOCX and overwrites the selected output. A crash can lose unsaved work from the current page; saves are not atomic. A save itself can fail.
- Translation retries happen immediately, without backoff. After repeated failures the original text and error are included in the output, and processing continues. A server outage can therefore produce a mostly untranslated DOCX.
- Missing-file checks only test whether a path exists, not whether it is a readable PDF. There is no password handling for encrypted PDFs. Corrupt documents, directory paths, and permission problems may raise exceptions.
- Most other failures stop processing and print a traceback. The outer handler does not explicitly set a failing exit status, so automation cannot rely on the process exit code alone. The final Enter prompt requires an interactive console.
- No pages means the page loop never saves a DOCX. There is no explicit empty-document validation.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| `ModuleNotFoundError` | Activate `.venv` and run `python -m pip install -r requirements.txt`. Install `PyMuPDF` and `python-docx`, not unrelated packages named `fitz` or `docx`. |
| `ollama` command not recognized | Install Ollama, then reopen CMD so its PATH is refreshed. |
| Connection errors / repeated failed attempts | Start the Ollama app or `ollama serve`, set `OLLAMA_HOST` as above, and check `ollama list` in the same CMD session. Stop an unwanted run with Ctrl+C. |
| Model not found | Run `ollama pull gemma2` and verify the model list. The model setting is `gemma2`, regardless of the header example. |
| File not found / directory used as PDF | Set a nonempty `PDF_FILE_PATH` to an existing PDF filename; check spelling and the current directory for relative paths. |
| Cannot save DOCX / permission denied | Set `OUTPUT_DOCX_PATH` to a filename in a writable location. Close the destination in Word or other software, check folder permissions and free space, and avoid protected system folders. |
| Headings but little/no translated text | Check that you can select PDF text. This program has no OCR and skips very short blocks. |
| Encrypted or damaged PDF fails | Supply a readable, unencrypted PDF you are authorized to process. The script has no password prompt or repair workflow. |
| Missing content or garbled reading order | Inspect the source columns/tables and the output manually. Sorting, extraction, and model output can all lose information. |
| Output contains `[TRANSLATION FAILED: ...]` | All three attempts failed for that block. Fix the model/server error before rerunning; use a different output filename if keeping the partial result. |
| Appears idle / waiting at the end | Inference can be slow and has no per-block progress display. At `Press Enter to exit...`, press Enter. |

## Privacy and repository hygiene

The script opens the PDF from disk and sends extracted blocks, plus its translation prompt, through the Ollama Python client. With a local Ollama server and the downloaded `gemma2` model, inference is intended to run on your machine. The script has no explicit cloud upload or telemetry code.

It does **not** enforce a local endpoint. The client defaults to `http://127.0.0.1:11434` but honors `OLLAMA_HOST`; a remote endpoint would receive document text. Review your server, model, proxy, and environment settings before processing sensitive material. Installing software and downloading models use the network. This project cannot guarantee the behavior or logging of external software. See the [Ollama client implementation](https://github.com/ollama/ollama-python/blob/main/ollama/_client.py).

The DOCX can contain original text on translation failures, and console tracebacks can expose file paths. Keep documents, outputs, logs, models, environments, secrets, and credentials out of Git; see [SECURITY.md](SECURITY.md).

`.gitignore` excludes private input/output folders, PDF/Word documents anywhere in the tree (including uppercase extensions), common model files, caches, and credentials. For a future **reviewed, redistributable** public sample, add a narrow exception at the end of `.gitignore`, such as `!/samples/public-example.pdf`, and place it outside ignored input/output folders. Check the PDF's content and metadata and document its source/license first. Do not broadly unignore all PDFs. No sample directory is currently required.

Ignore rules do not remove files already tracked and cannot identify every possible secret or file format. Always review `git status` and staged changes before committing.

## Maintenance

This is a small legacy script, not an installable Python package. `requirements.txt` is sufficient; there is no `pyproject.toml`, packaged CLI, automated test suite, or bundled model. See [CONTRIBUTING.md](CONTRIBUTING.md) for safe checks and [CHANGELOG.md](CHANGELOG.md) for the repository preparation record.

## License

This project's source code, including the preserved `pdf_translator.py`, is licensed under the **GNU Affero General Public License v3.0 only** (SPDX: **AGPL-3.0-only**). See [LICENSE](LICENSE) for the official, unmodified license text. This grant is for version 3 only, not "version 3 or any later version."

PyMuPDF is used under its open-source AGPL licensing route. Third-party dependencies retain their own licenses; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

AI models downloaded separately, including **Gemma 2**, are governed by their own model terms and are not licensed under this repository's AGPL license. Gemma 2 is subject to [Google's Gemma Terms of Use](https://ai.google.dev/gemma/terms). No model files are bundled.
