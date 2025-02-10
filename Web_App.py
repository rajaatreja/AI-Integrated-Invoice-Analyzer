from flask import Flask, render_template, jsonify, send_file
import threading
import psycopg2
import io
import json
from main import start_email_processing  # Import your email processing script

app = Flask(__name__)

# PostGreSQL Database Connection
def get_db_connection():
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

# Fetch stored invoices from database
@app.route("/invoices")
def get_invoices():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT email_uid, invoice_number, amount, due_date, sender_name, sender_email, attachment_filename FROM invoices")
        invoices = cursor.fetchall()
        cursor.close()
        connection.close()

        return jsonify([{
            "email_uid": row[0],
            "invoice_number": row[1],
            "amount": row[2],
            "due_date": row[3],
            "sender_name": row[4],
            "sender_email": row[5],
            "attachment_filename": row[6]
        } for row in invoices])

    except Exception as e:
        return jsonify({"error": str(e)})

# Download invoice attachment
@app.route("/download/<email_uid>")
def download_attachment(email_uid):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT attachment_filename, attachment_data FROM invoices WHERE email_uid = %s", (email_uid,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        if result and result[1]:  # Ensure there's data to download
            filename, file_data = result
            return send_file(
                io.BytesIO(file_data),
                mimetype="application/pdf",
                as_attachment=True,
                download_name=filename
            )
        else:
            return "No attachment found", 404

    except Exception as e:
        return f"Error retrieving file: {e}", 500

# Trigger email fetching
@app.route("/fetch-emails", methods=["POST"])
def fetch_emails():
    thread = threading.Thread(target=start_email_processing)
    thread.start()
    return jsonify({"message": "Email fetching started!"})

# Serve HTML dashboard
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)