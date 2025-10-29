from dotenv import load_dotenv
from pathlib import Path
import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# --- Cross-platform safe env loading ---
# Try loading from feedback_email.py folder and main.py folder
base_dir = Path(__file__).resolve().parent
env_paths = [
    base_dir / ".env",
    base_dir.parent / ".env",
]

for env_path in env_paths:
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        print(f"Loaded .env from: {env_path}")
        break
else:
    print("WARNING: .env not found in expected locations")

def send_feedback_email(feedback_text: str):
    sender_email = os.getenv("EMAIL_ADDRESS")
    sender_password = os.getenv("EMAIL_APP_PASSWORD")

    if not sender_email or not sender_password:
        return False, "Email credentials not found in .env file."

    receiver_email = sender_email
    subject = "New Feedback Submission"
    body = f"""
New feedback received at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:

{feedback_text}
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return True, None
    except Exception as e:
        return False, str(e)
