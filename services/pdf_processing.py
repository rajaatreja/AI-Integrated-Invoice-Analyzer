from io import BytesIO
import pdfplumber
import pytesseract
from pdf2image import convert_from_path

# Function to extract invoice details from PDF attachments
def extract_pdf_text(pdf_data):
    """Extract text from PDF data (binary format)."""
    text = extract_text_from_pdf(pdf_data)
    if text is None:
        # Fallback to OCR if no text was extracted
        text = extract_text_from_scanned_pdf(pdf_data)
    return text

# Function to extract text from PDF (non-scanned)
def extract_text_from_pdf(pdf_data):
    """Extract text from a non-scanned PDF, given binary data."""
    try:
        # Open the binary PDF data as if it were a file
        with pdfplumber.open(BytesIO(pdf_data)) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text if text.strip() else None
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

# Function to extract text from scanned PDF using OCR
def extract_text_from_scanned_pdf(pdf_data):
    """Extract text from a scanned PDF using OCR, given binary data."""
    try:        
        # Convert binary PDF data to images
        images = convert_from_path(BytesIO(pdf_data))
        text = ""
        for img in images:
            text += pytesseract.image_to_string(img) + "\n"
        return text
    except Exception as e:
        print(f"Error extracting text from scanned PDF: {e}")
        return ""