# Third-party notices — legacy implementation

These references identify the direct Python dependencies and external runtime/model used by `pdf_translator.py`. They do not grant a license to this project's own source and are not a substitute for the license texts accompanying third-party distributions.

## Project license and dependency scope

This project's source code, including the preserved `pdf_translator.py`, is licensed under the **GNU Affero General Public License v3.0 only** (SPDX: **AGPL-3.0-only**). The project [LICENSE](LICENSE) contains only the official, unmodified GNU AGPL v3 text. The project's grant is for version 3 only; the license text's example wording in "How to Apply These Terms to Your New Programs" does not extend this grant to later versions.

The standard license text was copied unchanged from the [GNU AGPL v3 copy in PyMuPDF's official repository](https://github.com/pymupdf/PyMuPDF/blob/main/COPYING). No third-party-specific notices or model terms have been appended to the project `LICENSE`.

PyMuPDF is offered under GNU Affero General Public License v3 (AGPLv3) or a separate Artifex commercial license. **This project uses its open-source AGPL route**, not the commercial route. See the [official licensing information](https://pymupdf.io/licensing). Third-party dependencies retain their own licenses and notices; the project's license does not relicense them.

AI models are external downloads and are not covered by this project's AGPL license or by the Ollama software's MIT license. In particular, Gemma 2 remains subject to [Google's Gemma Terms of Use](https://ai.google.dev/gemma/terms). No model files are bundled.

## Components

| Component | Role in this legacy program | Upstream license / terms | Official reference |
| --- | --- | --- | --- |
| PyMuPDF / MuPDF | `import pymupdf`: opens PDFs and extracts page blocks. PyMuPDF uses MuPDF. | AGPLv3 or Artifex commercial licensing; this project uses the open-source AGPL route. | [PyMuPDF project](https://github.com/pymupdf/PyMuPDF), [licensing](https://pymupdf.io/licensing) |
| Ollama Python client (`ollama`) | Calls `ollama.chat` for block translation. | MIT. | [Client project](https://github.com/ollama/ollama-python), [license](https://github.com/ollama/ollama-python/blob/main/LICENSE) |
| python-docx (`docx`) | Creates the Word document, headings, and paragraphs. | MIT. | [Project](https://github.com/python-openxml/python-docx), [license](https://github.com/python-openxml/python-docx/blob/master/LICENSE) |
| Ollama runtime | Separately installed model server used by the Python client. | Main project: MIT; bundled components may carry additional notices. | [Project](https://github.com/ollama/ollama), [license](https://github.com/ollama/ollama/blob/main/LICENSE) |
| Google Gemma 2 (`gemma2` in Ollama) | Configured model used to generate Vietnamese translations. Downloaded separately; not bundled. | Gemma Terms of Use, including associated use restrictions; not covered by this project's AGPL license or the Ollama MIT license. | [Ollama model page](https://ollama.com/library/gemma2), [Google's terms](https://ai.google.dev/gemma/terms) |

Dependency names, baseline versions, Python requirements, and Python-package license labels were checked against the installed distribution metadata. Upstream references were reviewed during repository preparation. Consult the specific versions and artifacts you actually install when assessing redistribution obligations.

Pip also installs transitive dependencies, including `httpx` and `pydantic` for the Ollama client and `lxml` and `typing_extensions` for python-docx at the inspected baseline. This table is not an exhaustive notice bundle for a packaged application. If distributing environments, wheels, executables, or models later, collect their actual licenses and notices as well.

No third-party source, custom fonts, model weights, sample PDFs, or generated documents are bundled in this repository. No separate font notice is needed for assets supplied here. Review the source and redistribution rights of any future sample document before adding it.
