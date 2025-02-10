from utils.email_utils import fetch_inbox_emails
from services.db_service import create_table

def start_email_processing():
    """Function to initialize database and fetch emails."""
    create_table()  # Ensures the PostgreSQL database table exists
    fetch_inbox_emails()  # Fetch emails from the inbox

if __name__ == "__main__":
    start_email_processing()
