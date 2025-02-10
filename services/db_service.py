import json
import psycopg2
from dateutil import parser
from utils.attachment_utils import get_attachment_data

def get_db_connection():
    try:
        # Load database configuration from fb_config.json
        with open('config/db_config.json', 'r') as config_file:
            config = json.load(config_file)
        # Connect to PostgreSQL using the parameters from the JSON file
        connection = psycopg2.connect(
            dbname=config['dbname'],
            user=config['user'],
            password=config['password'],
            host=config['host'],
            port=config['port']
        )
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def create_table():
    connection = get_db_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()

            # Check if the 'invoices' table exists
            check_table_query = """
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'invoices'
            );
            """
            cursor.execute(check_table_query)
            table_exists = cursor.fetchone()[0]

            if not table_exists:
                # If the table does not exist, create the table
                create_table_query = """
                CREATE TABLE invoices (
                    email_uid VARCHAR(255) PRIMARY KEY,
                    invoice_number VARCHAR(255),
                    amount DECIMAL(10, 2),
                    due_date DATE,
                    sender_name VARCHAR(255),
                    sender_email VARCHAR(255),
                    attachment_filename VARCHAR(255),  -- Optional, to store the filename
                    attachment_data BYTEA             -- To store the binary data of the attachment
                );
                """
                cursor.execute(create_table_query)
                connection.commit()

        except Exception as e:
            print(f"Error creating table: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Connection to the database failed!")

# Function to convert date to PostgreSQL-friendly format
def convert_to_postgres_date(date_str):
    if not date_str:
        return None
    try:
        # Parse the date using dateutil.parser
        parsed_date = parser.parse(date_str)
        # Return the date in PostgreSQL-friendly format (YYYY-MM-DD)
        return parsed_date.strftime("%Y-%m-%d")
    except (ValueError, TypeError) as e:
        print(f"Invalid date format: {date_str}")
        return None
    
def store_invoice_data_in_db(extracted_data, msg_id, payload):
    """Store the extracted invoice data and attachments in the database."""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Convert due_date to PostgreSQL-friendly format
            due_date = convert_to_postgres_date(extracted_data.get("due_date"))

            # Handle missing due date
            if not due_date:
                due_date = None

            attachment_filename = None
            attachment_data = None

            # Process attachments (handle PDFs properly)
            if 'parts' in payload:
                for part in payload['parts']:
                    if part.get('filename'):  # Ensure it's an actual file
                        attachment_filename = f"{msg_id}_{part.get('filename')}"

                        # Extract and decode the attachment data
                        attachment_id = part['body'].get('attachmentId')
                        if attachment_id:
                            attachment = get_attachment_data(msg_id, attachment_id)
                            if attachment:
                                attachment_data = psycopg2.Binary(attachment)  # Convert to binary for DB storage
                                break  # Stop after the first valid attachment (can be modified for multiple)

            # Insert the invoice data
            insert_query = """
            INSERT INTO invoices (email_uid, invoice_number, amount, due_date, sender_name, sender_email, attachment_filename, attachment_data)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (email_uid) DO UPDATE 
            SET invoice_number = EXCLUDED.invoice_number,
                amount = EXCLUDED.amount,
                due_date = EXCLUDED.due_date,
                sender_name = EXCLUDED.sender_name,
                sender_email = EXCLUDED.sender_email,
                attachment_filename = EXCLUDED.attachment_filename,
                attachment_data = EXCLUDED.attachment_data;
            """
            
            cursor.execute(insert_query, (
                extracted_data.get("email_uid"),
                extracted_data.get("invoice_number"),
                extracted_data.get("amount"),
                due_date,
                extracted_data.get("sender_name"),
                extracted_data.get("sender_email"),
                attachment_filename,
                attachment_data
            ))

            connection.commit()
            cursor.close()
            print(f"Invoice {extracted_data.get('invoice_number')} saved successfully.")

        except Exception as e:
            print(f"Error inserting invoice data into PostgreSQL: {e}")

        finally:
            connection.close()