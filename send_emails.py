import smtplib
import os
import csv
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Load environment variables
SMTP_SERVER = os.getenv("SMTP_SERVER")  # e.g., "smtp.gmail.com"
SMTP_PORT = os.getenv("SMTP_PORT")  # e.g., 587
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Load recipient list from TXT file
RECIPIENTS_FILE = "recipients.txt"
CSV_OUTPUT_FILE = "email_status.csv"

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

        return True  # Email sent successfully
    except Exception as e:
        print(f"❌ Failed to send email to {recipient}: {e}")
        return False  # Email sending failed

def main():
    subject = "Exclusive Offer: Boost Your Productivity with Our Latest Tools!"
    body = """\
Dear,

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

    try:
        with open(RECIPIENTS_FILE, "r") as file:
            recipients = {line.strip() for line in file if line.strip()}  # Remove duplicates and empty lines

        if not recipients:
            print("⚠ No valid email addresses found in recipients.txt.")
            return

        # Prepare data for CSV output
        email_status = []

        # First attempt to send emails
        for recipient in recipients:
            status = send_email(recipient, subject, body)
            email_status.append({"email": recipient, "status": status})

        # Write status to CSV file
        with open(CSV_OUTPUT_FILE, "w", newline='') as csvfile:
            fieldnames = ['email', 'status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in email_status:
                writer.writerow(row)

        print(f"✅ Email statuses written to {CSV_OUTPUT_FILE}")

        # Retry sending emails for those who failed
        failed_recipients = [row['email'] for row in email_status if row['status'] is False]

        # Continue retrying until no failed recipients
        retry_count = 0
        while failed_recipients:
            print(f"🔄 Retrying failed recipients... Attempt {retry_count + 1}")
            for recipient in failed_recipients:
                print(f"🔄 Retrying email to {recipient}")
                status = send_email(recipient, subject, body)
                # Update the status in the email_status list with the retry result
                for row in email_status:
                    if row['email'] == recipient:
                        row['status'] = status

            # Write updated status to CSV after retries
            with open(CSV_OUTPUT_FILE, "w", newline='') as csvfile:
                fieldnames = ['email', 'status']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for row in email_status:
                    writer.writerow(row)

            # Check for failed recipients again
            failed_recipients = [row['email'] for row in email_status if row['status'] is False]
            retry_count += 1

            # Wait for 1 minute before the next retry
            if failed_recipients:
                print("⏳ Waiting 1 minute before retrying...")
                time.sleep(60)  # Wait for 60 seconds (1 minute)

            # If we reach 5 retries, stop to prevent infinite looping
            if retry_count >= 5:
                print("❌ Maximum retry attempts reached. Some emails may not have been sent.")
                break

        print(f"✅ Retry results written to {CSV_OUTPUT_FILE}")

    except FileNotFoundError:
        print(f"❌ Error: '{RECIPIENTS_FILE}' not found. Please ensure the file exists.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
