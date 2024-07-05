from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.utils.constants import (
    SENDER_EMAIL,
    SUBJECT,
    SENDGRID_API_KEY,
)

class Email:
    @staticmethod
    def send_email(recipient:str,html_template:str):
        message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=recipient,
        subject=SUBJECT,
        html_content=html_template)
        sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)
        response = sg.send(message)
        return True
