import smtplib
import os
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Load environment variables
SMTP_SERVER = os.getenv("SMTP_SERVER")  # e.g., "smtp.gmail.com"
SMTP_PORT = os.getenv("SMTP_PORT")  # e.g., 587
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Load recipient list from CSV file
RECIPIENTS_FILE = "recipients.csv"

def send_email(recipient, subject, body):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(SMTP_SERVER, int(SMTP_PORT))
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, recipient, msg.as_string())
        server.quit()

        print(f"Email sent to {recipient}")

    except Exception as e:
        print(f"Failed to send email to {recipient}: {e}")

def main():
    subject = "Exclusive Offer: Boost Your Productivity with Our Latest Tools!"
    body = """\
    Dear 
    
    We’re excited to introduce our latest suite of online tools designed to help you save time and maximize efficiency.
    
    🔥 What’s New?
    ✔ Advanced text analysis for content creators
    ✔ AI-powered automation for faster workflows
    ✔ Free access to premium website tools
    
    💡 Limited-Time Offer:
    Sign up today and enjoy exclusive early access!
    
    👉 Click here to explore: https://multiculturaltoolbox.com/
    
    Best regards,  
    Edward Lance Lorilla
    https://multiculturaltoolbox.com/
    """

    with open(RECIPIENTS_FILE, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            recipient = row[0]
            send_email(recipient, subject, body)

if __name__ == "__main__":
    main()
