# Invoice Processing and Web Application

This project is a web application that processes email invoices through API, extracts relevant details using Google Gemini AI, and stores them in a PostgreSQL database. The application also provides a web interface to view and download stored invoices.

## Directory Structure

### **Directories and Files**

- `config/` - Contains configuration files for database, API credentials, and tokens.
  - `credentials.json` - Google API credentials. (Client secret file to be downloaded from Google Cloud project)
  - `db_config.json` - Database configuration.
  - `gemini_api.json` - Gemini API token.
  - `token.json` - OAuth token for Gmail API. (This file is automatically genereated once the authentication is done through login)
- `main.py` - Entry point for email processing.
- `requirements.txt` - List of dependencies.
- `services/` - Contains service modules for database, Gmail, PDF processing, and Gemini API.
  - `db_service.py` - Database operations.
  - `gemini_service.py` - Gemini API integration.
  - `gmail_service.py` - Gmail API integration.
  - `pdf_processing.py` - PDF text extraction.
- `templates/` - Contains HTML templates for the web interface.
  - `index.html` - Main dashboard template.
- `utils/` - Utility modules for email and attachment processing.
  - `analyze_content.py` - Analyzes email content.
  - `attachment_utils.py` - Handles email attachments.
  - `email_utils.py` - Fetches and processes emails.
- `Web_App.py` - Flask web application.

## Setup

### **Clone the repository:**

```sh
git clone https://github.com/rajaatreja/AI-Integrated-Invoice-Analyzer.git
cd AI-Integrated-Invoice-Analyzer
```

### **Install dependencies:**

```sh
pip install -r requirements.txt
```

### **Configure the application:**

- Update `config/db_config.json` with your PostgreSQL database details.
- Update `config/credentials.json` with your Google API credentials by downloading and pasting it in config folder.
- Update `config/gemini_api.json` with your Gemini API token.

### **Run the web application:**

```sh
python Web_App.py
```

## Usage

### **Web Interface**

- **Dashboard:** Access the main dashboard at [http://localhost:5000/](http://localhost:5000/).

### **Email Processing**

- **Start Email Processing:** Run `main.py` to initialize the database and fetch emails and print the output on the terminal.

## Application Workflow

The application automates invoice email processing, extracts key details, and stores them in a PostgreSQL database while providing a web interface for users to view and download invoices.

1. **Fetching Emails**: The process starts with `main.py`, which initializes the database using `db_service.py` and then fetches emails from Gmail using `email_utils.py`, which interacts with the Gmail API (`gmail_service.py`).

2. **Extracting Invoice Details**: Once an email is retrieved, its content is analyzed in `analyze_content.py` using Gemini AI (`gemini_service.py`). This extracts details like invoice number, amount, and due date.

3. **Processing Attachments**: If an email contains a PDF invoice, `attachment_utils.py` downloads the file, and `pdf_processing.py` extracts text using PDFPlumber for digital PDFs or OCR (via Pytesseract) for scanned PDFs.

4. **Storing in Database**: Extracted invoice details are stored in PostgreSQL using `db_service.py`.

5. **Web Interface**: The Flask web application (`Web_App.py`) allows users to:
   - View invoices at `http://localhost:5000/invoices`
   - Download attachments at `http://localhost:5000/download/<email_uid>`
   - Trigger email fetching manually at `http://localhost:5000/fetch-emails`

This automated workflow ensures efficient invoice management, minimizing manual efforts through an interactive web dashboard.


## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgements

- **Flask** - Web framework for building the application.
- **psycopg2** - PostgreSQL database adapter for Python.
- **Google API Python Client** - Integrates with Google services (Gmail API).
- **PDFPlumber** - Extracts text from PDFs.
- **Pytesseract** - OCR for extracting text from scanned PDFs.

## Contribution

Feel free to contribute to this project by submitting issues or pull requests!

