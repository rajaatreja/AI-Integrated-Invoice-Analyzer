import json
import requests

# Load the Gemini API configuration from a JSON file
with open("config/gemini_api.json", "r") as file:
    api_config = json.load(file)
# Extract the Gemini token from the configuration
gemini_token = api_config["gemini_token"]

# Function to authenticate and use the Gemini API   
def analyze_text_with_gemini(text):
    # Define the URL for the Gemini API endpoint
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_token}"
    
    # Set the headers for the API request
    headers = {
        "Content-Type": "application/json"
    }
    # Create the payload for the API request. This inculdes the prompt text.
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
    # Send the POST request to the Gemini API
    response = requests.post(url, headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json() # Return the JSON response from the API
    else:
        # Print an error message if the request failed
        print("Analysis failed:", response.json())
        return None