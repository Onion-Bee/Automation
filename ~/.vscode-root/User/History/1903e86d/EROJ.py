# Script to auto-send personalized messages via SMTP

import os
import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 1. Load messages CSV
def load_messages(path='messages_output.csv'):
    return pd.read_csv(path)

# 2. Email sender setup
def get_smtp_server():
    # Use env vars
    smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', 465))
    user = os.getenv('EMAIL_USER')
    password = os.getenv('EMAIL_PASS')
    if not user or not password:
        raise EnvironmentError('EMAIL_USER and EMAIL_PASS must be set as environment variables')

    # Establish a secure SSL connection
    server = smtplib.SMTP_SSL(smtp_host, smtp_port)
    server.login(user, password)
    return server, user

# 3. Craft and send each email
def send_emails(csv_path='messages_output.csv', subject='Hello from Our Team'):    
    df = load_messages(csv_path)
    server, sender_email = get_smtp_server()

    for _, row in df.iterrows():
        recipient = row['email']
        body = row['message']

        # Create MIME message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient
        msg['Subject'] = subject

        # Attach the text body
        msg.attach(MIMEText(body, 'plain'))

        try:
            server.sendmail(sender_email, recipient, msg.as_string())
            print(f"Email sent to {recipient}")
        except Exception as e:
            print(f"Failed to send to {recipient}: {e}")

    server.quit()

if __name__ == '__main__':
    send_emails()
    print("All emails processed.")
