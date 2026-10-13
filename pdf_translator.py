"""
PDF to Vietnamese Translator (using local Ollama model)
---------------------------------------------------------
This script reads a PDF file, sends each page's text to a local
Ollama model for translation into Vietnamese, and saves the result
as a Word (.docx) document.

BEFORE RUNNING, MAKE SURE:
1. Ollama is installed and running (open the Ollama app, or run
   `ollama serve` in a terminal).
2. The model below has been downloaded, e.g.:
       ollama pull qwen2.5
3. Required Python packages are installed:
       pip install pymupdf ollama python-docx
4. You update the CONFIG section below with your own file paths.
"""

import os
import sys
import traceback
from pathlib import Path

import pymupdf
import ollama
from docx import Document

# =========================================================
# CONFIG — CHANGE THESE VALUES FOR YOUR OWN FILE
# =========================================================

# Full path to your input PDF file.
# Use a raw string (the letter r before the quotes) so backslashes
# in Windows paths don't cause errors.
PDF_FILE_PATH = r""

# Full path where the translated Word document will be saved.
OUTPUT_DOCX_PATH = r""

# The Ollama model name to use for translation.
# Must match exactly what "ollama list" shows on your machine.
MODEL_NAME = "gemma2"

# =========================================================
# END OF CONFIG
# =========================================================


def build_prompt(text):
    return f"""Bạn là một dịch giả chuyên nghiệp. Hãy dịch đoạn văn bản sau đây sang tiếng Việt một cách chính xác, mượt mà và sát nghĩa nhất.

YÊU CẦU BẮT BUỘC:
1. Dịch đầy đủ 100% nội dung, TUYỆT ĐỐI KHÔNG tóm tắt, không bỏ sót câu/chữ.
2. Giữ nguyên định dạng logic của câu văn. Các thuật ngữ chuyên ngành có thể giữ nguyên từ gốc trong ngoặc đơn nếu cần.
3. KHÔNG viết lời chào hay giải thích gì thêm, CHỈ xuất ra bản dịch tiếng Việt.

Văn bản gốc:
{text}

Bản dịch tiếng Việt:"""


def translate_text(text, model_name, max_retries=2):
    """Send a chunk of text to the local Ollama model and return the
    Vietnamese translation. Retries on failure instead of crashing."""
    text = text.strip()
    if not text:
        return ""

    last_error = None
    for attempt in range(1, max_retries + 2):
        try:
            response = ollama.chat(
                model=model_name,
                messages=[{"role": "user", "content": build_prompt(text)}],
            )
            return response["message"]["content"].strip()
        except Exception as e:
            last_error = e
            print(f"    - Translation attempt {attempt} failed: {e}")

    # If every attempt failed, keep the original text instead of losing it
    return f"[TRANSLATION FAILED: {last_error}]\n{text}"


def extract_ordered_blocks(page, y_tolerance=5):
    """Get text blocks from a page, sorted top-to-bottom / left-to-right,
    so multi-column layouts don't get scrambled."""
    blocks = page.get_text("blocks")
    return sorted(blocks, key=lambda b: (round(b[1] / y_tolerance), b[0]))


def translate_pdf(pdf_path, output_path, model_name):
    pdf_path = Path(pdf_path)
    output_path = Path(output_path)

    if not pdf_path.exists():
        print(f"ERROR: File not found: {pdf_path}")
        print("Double-check the PDF_FILE_PATH value at the top of this script.")
        return

    # Make sure the output folder exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    pdf_doc = pymupdf.open(str(pdf_path))
    word_doc = Document()
    word_doc.add_heading("BẢN DỊCH TIẾNG VIỆT", level=1)

    total_pages = len(pdf_doc)
    print(f"Opened '{pdf_path.name}' ({total_pages} pages). Starting translation...")

    try:
        for page_num in range(total_pages):
            print(f"-> Translating page {page_num + 1}/{total_pages}...")
            page = pdf_doc[page_num]
            blocks = extract_ordered_blocks(page)

            word_doc.add_heading(f"Trang {page_num + 1}", level=2)

            for block in blocks:
                text = block[4].strip()
                if len(text) > 3:
                    translated = translate_text(text, model_name)
                    word_doc.add_paragraph(translated)

            # Save after every page so progress is never lost if
            # something crashes partway through.
            word_doc.save(str(output_path))

    except KeyboardInterrupt:
        print("\nStopped by user. Saving progress so far...")
        word_doc.save(str(output_path))

    finally:
        pdf_doc.close()

    print(f"Done! Translated file saved to: {output_path}")


if __name__ == "__main__":
    try:
        translate_pdf(PDF_FILE_PATH, OUTPUT_DOCX_PATH, MODEL_NAME)
    except Exception:
        print("\nAn unexpected error occurred:")
        traceback.print_exc()
    finally:
        # Keep the console window open if double-clicked on Windows
        input("\nPress Enter to exit...")