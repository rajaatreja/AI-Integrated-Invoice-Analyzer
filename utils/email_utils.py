import re
import base64
from services.gmail_service import get_gmail_service
from utils.analyze_content import analyze_email_and_attachments
from utils.attachment_utils import download_attachment

def extract_sender_details(sender):
    sender_email_match = re.search(r"<(.*?)>", sender)
    sender_name_match = re.search(r"^(.*?)(?=\s*<)", sender)

    return {
        "sender_email": sender_email_match.group(1) if sender_email_match else "Not found",
        "sender_name": sender_name_match.group(1) if sender_name_match else "Not found"
    }

# Function to extract plain text or HTML content from email
def extract_email_body(payload):
    body = None
    if 'parts' in payload:
        for part in payload['parts']:
            if part.get('mimeType') == 'text/plain':
                body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                break
            elif part.get('mimeType') == 'text/html':
                body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
    return body if body else "No email content found."

def fetch_inbox_emails():
    service = get_gmail_service()
    # Process only first 100 emails in the INBOX. Hint: Use the `maxResults` parameter.
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=100).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No new emails found in INBOX.")
        return

    for msg in messages:
        message = service.users().messages().get(userId='me', id=msg['id']).execute()
        payload = message.get('payload', {})
        headers = payload.get('headers', [])

        sender = subject = email_content = None
        for header in headers:
            if header['name'] == 'From':
                sender = header['value']
            if header['name'] == 'Subject':
                subject = header['value']

        email_content = extract_email_body(payload)

        attachment_content = "Attachments:\n"
        if 'parts' in payload:
            for part in payload['parts']:
                if part.get('filename'):
                    attachment_id = part['body'].get('attachmentId')
                    if attachment_id:
                        attachment_content += download_attachment(service, msg['id'], attachment_id, part['filename'])
        
        email_content += "\n" + attachment_content
        
        analyze_email_and_attachments(msg['id'], sender, subject, email_content, payload)