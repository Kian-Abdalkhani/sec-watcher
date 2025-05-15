"""Service for sending emails"""

import smtplib
import os
import logging
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.config import EMAIL_ADDRESS,PASSWORD

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self, smtp_server='smtp.gmail.com', smtp_port=587):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email_address = EMAIL_ADDRESS
        self.password = PASSWORD

    def connect(self):
        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        server.starttls()
        server.login(self.email_address, self.password)
        return server

    def send_email(self, subscriber_email, subject, message, is_html=True) -> bool:
        try:
            server = self.connect()

            #email format
            email_message = MIMEMultipart("alternative")
            email_message['From'] = self.email_address
            email_message['To'] = subscriber_email
            email_message['Subject'] = subject

            text_part = MIMEText(message, "plain")

            if is_html:
                html_part = MIMEText(message, "html")
                email_message.attach(text_part)
                email_message.attach(html_part)

            server.sendmail(self.email_address, subscriber_email, email_message.as_string())
            server.quit()
            logger.info(f"Email sent successfully to {subscriber_email} for {subject}")
            return True
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False


emailer = EmailService()

emailer.send_email(subscriber_email=emailer.email_address,subject="Test Email",message="This is a test email")
