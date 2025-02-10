import json
import requests

with open("config/gemini_api.json", "r") as file:
    api_config = json.load(file)
gemini_token = api_config["gemini_token"]

# Function to authenticate and use the Gemini API   
def analyze_text_with_gemini(text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_token}"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [{
            "parts": [{
                "text": f"""
                    Extract the following details from the provided email content and return a structured JSON object:

                    - invoice_number
                    - amount
                    - due_date

                    Provide the response **only** as a JSON object with these exact keys. Example format:

                    {{
                        "invoice_number": "INV-123456",
                        "amount": "450.00",
                        "due_date": "March 15, 2025"
                    }}

                    Email Content: {text}
                """
            }]
        }]
    }
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()
    else:
        print("Analysis failed:", response.json())
        return None