import pdfplumber
from pathlib import Path

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from a PDF file."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()

# Test extraction
if __name__ == "__main__":
    sample_pdf = "data/documents/Module 3_Fundamental Analysis.pdf"  # Place a test PDF in `data/documents/`
    pdf_text = extract_text_from_pdf(sample_pdf)
    print(pdf_text)
