from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from dotenv import load_dotenv
import os

# Import your helper modules
from utils.ocr import extract_text_from_pdf
from utils.file_parser import parse_invoice_text, parse_po_text
from utils.matcher import compare_invoice_po

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Enable CORS (allows Streamlit frontend to talk to backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini client
try:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
except Exception as e:
    raise RuntimeError("Failed to initialize Gemini client. Check your GEMINI_API_KEY.") from e


@app.post("/reconcile")
async def reconcile(invoice: UploadFile = File(...), po: UploadFile = File(...)):
    """
    Upload invoice and PO PDF files, extract fields, compare, and get Gemini summary.
    """
    try:
        # Step 1: OCR text extraction
        invoice_text = extract_text_from_pdf(await invoice.read())
        po_text = extract_text_from_pdf(await po.read())

        # Step 2: Parse fields
        invoice_data = parse_invoice_text(invoice_text)
        po_data = parse_po_text(po_text)

        # Step 3: Compare results
        result = compare_invoice_po(invoice_data, po_data)

        # Step 4: Generate AI explanation (if mismatches found)
        if result.get("mismatches"):
            prompt = (
                "You are an AI assistant that helps with invoice reconciliation.\n"
                "Given the following mismatches between an invoice and a purchase order, "
                "generate a short, human-readable explanation for why the mismatch might have occurred, "
                "and what the finance team should verify.\n\n"
                f"Mismatches: {result['mismatches']}"
            )

            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
                result["ai_summary"] = response.text.strip()
            except Exception as e:
                result["ai_summary"] = f"AI summary unavailable (error: {str(e)})"
        else:
            result["ai_summary"] = "All fields match perfectly. No discrepancies detected."

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
