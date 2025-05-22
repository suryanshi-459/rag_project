import fitz  # PyMuPDF

def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        text = ""
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            if doc.page_count == 0:
                print("[WARNING] PDF has no pages.")
                return ""

            for page_num, page in enumerate(doc):
                page_text = page.get_text().strip()
                if page_text:
                    text += page_text + "\n"
                else:
                    print(f"[INFO] No text found on page {page_num + 1}")
        
        print(f"[INFO] Total characters extracted: {len(text)}")
        return text

    except Exception as e:
        print(f"[ERROR] Failed to read PDF: {e}")
        return ""

