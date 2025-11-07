import pytesseract
from pdf2image import convert_from_bytes
import os
from dotenv import load_dotenv

load_dotenv()

# Configure tesseract path (especially for Windows)
pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_PATH", "tesseract")

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Convert a PDF (in bytes) to text using OCR.
    """
    try:
        images = convert_from_bytes(pdf_bytes)
        full_text = ""
        for img in images:
            full_text += pytesseract.image_to_string(img)
        return full_text
    except Exception as e:
        raise RuntimeError(f"OCR extraction failed: {e}")
