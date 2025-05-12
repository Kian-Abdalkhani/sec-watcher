import pytest
import re
from unittest.mock import patch, MagicMock

from app.models.subscriber import Subscriber

class TestSubscriber:
    """Test cases for the Subscriber model"""

    @patch('app.models.subscriber.get_cik')
    def test_valid_subscriber_creation(self, mock_get_cik):
        """Test creating a valid subscriber"""
        # Mock the get_cik function to return a valid CIK
        mock_get_cik.return_value = "0000320193"  # Example CIK for Apple
        
        # Create a valid subscriber
        subscriber = Subscriber(
            name="John",
            email="john@example.com",
            tickers=["AAPL", "MSFT"]
        )
        
        # Assert that the subscriber was created with the correct attributes
        assert subscriber.name == "John"
        assert subscriber.email == "john@example.com"
        assert subscriber.tickers == ["AAPL", "MSFT"]
        
        # Assert that get_cik was called twice (once for each ticker)
        assert mock_get_cik.call_count == 2
    
    def test_to_dict(self):
        """Test converting a subscriber to a dictionary"""
        with patch('app.models.subscriber.get_cik', return_value="0000320193"):
            subscriber = Subscriber(
                name="John",
                email="john@example.com",
                tickers=["AAPL", "MSFT"]
            )
            
            subscriber_dict = subscriber.to_dict()
            
            assert subscriber_dict == {
                'name': 'John',
                'email': 'john@example.com',
                'tickers': ['AAPL', 'MSFT']
            }
    
    def test_from_dict(self):
        """Test creating a subscriber from a dictionary"""
        with patch('app.models.subscriber.get_cik', return_value="0000320193"):
            subscriber_dict = {
                'name': 'John',
                'email': 'john@example.com',
                'tickers': ['AAPL', 'MSFT']
            }
            
            subscriber = Subscriber.from_dict(subscriber_dict)
            
            assert subscriber.name == "John"
            assert subscriber.email == "john@example.com"
            assert subscriber.tickers == ["AAPL", "MSFT"]
    
    @pytest.mark.parametrize("name, expected_error", [
        ("", "Name cannot be empty"),
        ("A" * 26, "Name cannot be more than 25 characters"),
        ("John123", "Name can only contain letters")
    ])
    def test_invalid_name(self, name, expected_error):
        """Test validation for invalid names"""
        with pytest.raises(ValueError, match=expected_error):
            Subscriber.validate_name(name)
    
    @pytest.mark.parametrize("email, should_raise", [
        ("valid@example.com", False),
        ("invalid-email", True),
        ("@example.com", True),
        ("valid@.com", True),
        ("valid@example.", True)
    ])
    def test_email_validation(self, email, should_raise):
        """Test validation for email addresses"""
        if should_raise:
            with pytest.raises(ValueError, match="Invalid email format"):
                Subscriber.validate_email(email)
        else:
            # Should not raise an exception
            Subscriber.validate_email(email)
    
    @patch('app.models.subscriber.get_cik')
    def test_ticker_validation_empty(self, mock_get_cik):
        """Test validation for empty tickers list"""
        with pytest.raises(ValueError, match="Tickers cannot be empty"):
            Subscriber.validate_tickers([])
    
    @patch('app.models.subscriber.get_cik')
    def test_ticker_validation_invalid(self, mock_get_cik):
        """Test validation for invalid tickers"""
        # Mock get_cik to return empty string for invalid ticker
        mock_get_cik.return_value = ""
        
        with pytest.raises(ValueError, match="Invalid ticker"):
            Subscriber.validate_tickers(["INVALID"])
    
    @patch('app.models.subscriber.get_cik')
    def test_ticker_validation_valid(self, mock_get_cik):
        """Test validation for valid tickers"""
        # Mock get_cik to return a valid CIK
        mock_get_cik.return_value = "0000320193"
        
        # Should not raise an exception
        Subscriber.validate_tickers(["AAPL", "MSFT"])