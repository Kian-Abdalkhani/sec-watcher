import pytest
from unittest.mock import patch, MagicMock

from app.services.email_service import EmailService

class TestEmailService:
    """Test cases for the email service"""
    
    @patch('app.services.email_service.smtplib.SMTP')
    def test_connect(self, mock_smtp):
        """Test connecting to the SMTP server"""
        # Create a mock SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        # Create an email service
        email_service = EmailService(
            smtp_server='test.smtp.com',
            smtp_port=123
        )
        
        # Call the connect method
        server = email_service.connect()
        
        # Assert that the SMTP server was created with the correct parameters
        mock_smtp.assert_called_once_with('test.smtp.com', 123)
        
        # Assert that starttls and login were called
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with(email_service.email_address, email_service.password)
        
        # Assert that the server was returned
        assert server == mock_server
    
    @patch('app.services.email_service.EmailService.connect')
    def test_send_email_success(self, mock_connect):
        """Test sending an email successfully"""
        # Create a mock SMTP server
        mock_server = MagicMock()
        mock_connect.return_value = mock_server
        
        # Create an email service
        email_service = EmailService()
        
        # Call the send_email method
        result = email_service.send_email(
            subscriber_email='test@example.com',
            subject='Test Subject',
            message='Test Message'
        )
        
        # Assert that the email was sent
        mock_server.sendmail.assert_called_once()
        
        # Assert that the server was closed
        mock_server.quit.assert_called_once()
        
        # Assert that the method returned True
        assert result is True
    
    @patch('app.services.email_service.EmailService.connect')
    def test_send_email_failure(self, mock_connect):
        """Test sending an email with a failure"""
        # Create a mock SMTP server that raises an exception
        mock_server = MagicMock()
        mock_server.sendmail.side_effect = Exception("Test error")
        mock_connect.return_value = mock_server
        
        # Create an email service
        email_service = EmailService()
        
        # Call the send_email method
        result = email_service.send_email(
            subscriber_email='test@example.com',
            subject='Test Subject',
            message='Test Message'
        )
        
        # Assert that the method returned False
        assert result is False
    
    @patch('app.services.email_service.EmailService.connect')
    def test_send_email_format(self, mock_connect):
        """Test the format of the email being sent"""
        # Create a mock SMTP server
        mock_server = MagicMock()
        mock_connect.return_value = mock_server
        
        # Create an email service with a specific email address
        email_service = EmailService()
        email_service.email_address = "sender@example.com"
        
        # Call the send_email method
        email_service.send_email(
            subscriber_email='recipient@example.com',
            subject='Test Subject',
            message='Test Message'
        )
        
        # Get the email text that was sent
        args, kwargs = mock_server.sendmail.call_args
        sender, recipient, email_text = args
        
        # Assert that the sender and recipient are correct
        assert sender == "sender@example.com"
        assert recipient == "recipient@example.com"
        
        # Assert that the email text has the correct format
        assert "From: sender@example.com" in email_text
        assert "To: recipient@example.com" in email_text
        assert "Subject: Test Subject" in email_text
        assert "Test Message" in email_text