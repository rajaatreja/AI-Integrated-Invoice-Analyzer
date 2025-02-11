import base64
from services.gmail_service import get_gmail_service
from services.pdf_processing import extract_pdf_text

def get_attachment_data(msg_id, attachment_id):
    """Fetch and decode the attachment data from Gmail."""
    # Get the Gmail service
    service = get_gmail_service()
    # Fetch the attachment using the message ID and attachment ID
    attachment = service.users().messages().attachments().get(
        userId='me', messageId=msg_id, id=attachment_id
    ).execute()

    # Decode the attachment data if it exists
    if 'data' in attachment:
        return base64.urlsafe_b64decode(attachment['data'])
    return None

# Function to download attachments
def download_attachment(service, msg_id, attachment_id, filename):
    attachment = service.users().messages().attachments().get(userId='me', messageId=msg_id, id=attachment_id).execute()
    data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))

    # If it's a PDF, extract text from the binary data
    if filename.lower().endswith(".pdf"):
        extracted_text = extract_pdf_text(data)  # Use the binary data directly
        return extracted_text
    else:
        # Return an empty string for non-PDF attachments
        return ""