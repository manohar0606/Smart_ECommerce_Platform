import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")


EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() == "true"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")


def send_email(
    recipient_email: str,
    subject: str,
    message: str,
) -> None:
    if not EMAIL_HOST_USER or not EMAIL_HOST_PASSWORD:
        print("Email settings are not configured.")
        return

    email = EmailMessage()
    email["From"] = EMAIL_HOST_USER
    email["To"] = recipient_email
    email["Subject"] = subject
    email.set_content(message)

    try:
        with smtplib.SMTP(
            EMAIL_HOST,
            EMAIL_PORT,
            timeout=30,
        ) as server:

            if EMAIL_USE_TLS:
                server.starttls()

            server.login(
                EMAIL_HOST_USER,
                EMAIL_HOST_PASSWORD,
            )

            server.send_message(email)

        print(f"Email sent successfully to {recipient_email}")

    except Exception as exc:
        print(f"Email sending failed: {exc}")