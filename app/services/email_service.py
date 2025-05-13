"""Service for sending emails"""

import smtplib
import os
import logging
from datetime import datetime
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

    def send_email(self, subscriber_email, subject, message) -> bool:
        try:
            server = self.connect()

            #email format
            email_text = f"From: {self.email_address}\nTo: {subscriber_email}\nSubject: {subject}\n\n{message}"
            server.sendmail(self.email_address, subscriber_email, email_text)
            server.quit()
            logger.info(f"Email sent successfully to {subscriber_email} for {subject}")
            return True
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False

