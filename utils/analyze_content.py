import json
import re
from services.gemini_service import analyze_text_with_gemini
from services.db_service import store_invoice_data_in_db

def clean_email_content(email_content):
    return email_content.replace("Dear", "").replace("Best regards", "").strip()

# Function to analyze email content and attachments
def analyze_email_and_attachments(msg_id, sender, subject, email_content, payload):
    """Analyzes email content and extracts invoice details using Gemini AI."""
    
    cleaned_content = clean_email_content(email_content)
    analysis_result = analyze_text_with_gemini(f"{subject}\n{cleaned_content}")

    if analysis_result:
        candidates = analysis_result.get('candidates', [])
        if candidates:
            extracted_text_parts = candidates[0].get('content', {}).get('parts', [])
            if extracted_text_parts:
                json_text = extracted_text_parts[0].get("text", "").strip()
                json_text = re.sub(r"```json\n|\n```", "", json_text).strip()  

                try:
                    extracted_data = json.loads(json_text)
                    extracted_data["sender_name"] = "Not found"
                    extracted_data["sender_email"] = "Not found"
                    extracted_data["email_uid"] = msg_id

                    sender_email_match = re.search(r"<(.*?)>", sender)
                    sender_name_match = re.search(r"^(.*?)(?=\s*<)", sender)

                    if sender_email_match:
                        extracted_data["sender_email"] = sender_email_match.group(1)
                    if sender_name_match:
                        extracted_data["sender_name"] = sender_name_match.group(1)

                    # Only store if invoice_number is found
                    if extracted_data.get("invoice_number"):
                        print(f"Extracted Data: {extracted_data}")
                        # Store the invoice data in the database
                        store_invoice_data_in_db(extracted_data, msg_id, payload)

                except json.JSONDecodeError:
                    print("Error decoding JSON response from Gemini:", json_text)
            else:
                print("Failed to extract meaningful parts from Gemini response.")
        else:
            print("No candidates found in Gemini response.")
    else:
        print("Could not extract invoice data from email content.")