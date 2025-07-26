import pdfplumber

def ocr_from_scanned_pdf(pdf_path):
    try:
        full_text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                full_text += page.extract_text() + "\n"
        return full_text
    except Exception as e:
        print(f"❌ Error during OCR: {e}")
        return ""