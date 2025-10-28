from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

from pathlib import Path
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


def send_feedback_email(feedback_text: str):
    """Sends a feedback email through Gmail using environment variables."""

    sender_email = os.getenv("EMAIL_ADDRESS")
    sender_password = os.getenv("EMAIL_APP_PASSWORD")
    receiver_email = sender_email  # You can change this if you want

    if not sender_email or not sender_password:
        return False, "Email credentials not found in .env file."

    subject = "New Feedback Submission"
    body = f"""
New feedback received at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:

{feedback_text}
"""

    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(message)
        return True, None
    except Exception as e:
        return False, str(e)
