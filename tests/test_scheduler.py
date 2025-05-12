import pytest
from unittest.mock import patch, MagicMock

from scheduler import scheduled_task
from app.storage.ticker_store import TickerStore
from app.storage.sub_store import SubStore
from app.services.email_service import EmailService

class TestScheduler:
    """Test cases for the scheduler functionality"""
    
    @pytest.fixture
    def mock_ticker_store(self):
        """Fixture for a mock TickerStore"""
        return MagicMock(spec=TickerStore)
    
    @pytest.fixture
    def mock_sub_store(self):
        """Fixture for a mock SubStore"""
        return MagicMock(spec=SubStore)
    
    @patch('scheduler.EmailService')
    def test_scheduled_task_no_new_filings(self, mock_email_service_class, mock_ticker_store, mock_sub_store):
        """Test scheduled task when there are no new filings"""
        # Mock check_filings to return an empty dictionary (no new filings)
        mock_ticker_store.check_filings.return_value = {}
        
        # Call the scheduled_task function
        result = scheduled_task(mock_ticker_store, mock_sub_store)
        
        # Assert that check_filings was called
        mock_ticker_store.check_filings.assert_called_once()
        
        # Assert that EmailService was not instantiated
        mock_email_service_class.assert_not_called()
        
        # Assert that the function returned False
        assert result is False
    
    @patch('scheduler.EmailService')
    def test_scheduled_task_with_new_filings(self, mock_email_service_class, mock_ticker_store, mock_sub_store):
        """Test scheduled task when there are new filings"""
        # Mock check_filings to return a dictionary with new filings
        mock_filing = MagicMock()
        mock_ticker_store.check_filings.return_value = {"AAPL": mock_filing}
        
        # Mock get_subscribers_by_ticker to return a list of subscribers
        mock_subscribers = [
            {"email": "john@example.com", "name": "John", "tickers": ["AAPL"]},
            {"email": "jane@example.com", "name": "Jane", "tickers": ["AAPL"]}
        ]
        mock_sub_store.get_subscribers_by_ticker.return_value = mock_subscribers
        
        # Mock EmailService
        mock_email_service = MagicMock(spec=EmailService)
        mock_email_service_class.return_value = mock_email_service
        
        # Call the scheduled_task function
        result = scheduled_task(mock_ticker_store, mock_sub_store)
        
        # Assert that check_filings was called
        mock_ticker_store.check_filings.assert_called_once()
        
        # Assert that get_subscribers_by_ticker was called with the correct ticker
        mock_sub_store.get_subscribers_by_ticker.assert_called_once_with("AAPL")
        
        # Assert that EmailService was instantiated
        mock_email_service_class.assert_called_once()
        
        # Assert that send_email was called for each subscriber
        assert mock_email_service.send_email.call_count == 2
        
        # Assert that the function returned True
        assert result is True
    
    @patch('scheduler.EmailService')
    def test_scheduled_task_with_multiple_tickers(self, mock_email_service_class, mock_ticker_store, mock_sub_store):
        """Test scheduled task when there are new filings for multiple tickers"""
        # Mock check_filings to return a dictionary with new filings for multiple tickers
        mock_filing_aapl = MagicMock()
        mock_filing_msft = MagicMock()
        mock_ticker_store.check_filings.return_value = {
            "AAPL": mock_filing_aapl,
            "MSFT": mock_filing_msft
        }
        
        # Mock get_subscribers_by_ticker to return different subscribers for each ticker
        mock_subscribers_aapl = [
            {"email": "john@example.com", "name": "John", "tickers": ["AAPL"]}
        ]
        mock_subscribers_msft = [
            {"email": "jane@example.com", "name": "Jane", "tickers": ["MSFT"]}
        ]
        mock_sub_store.get_subscribers_by_ticker.side_effect = [
            mock_subscribers_aapl,
            mock_subscribers_msft
        ]
        
        # Mock EmailService
        mock_email_service = MagicMock(spec=EmailService)
        mock_email_service_class.return_value = mock_email_service
        
        # Call the scheduled_task function
        result = scheduled_task(mock_ticker_store, mock_sub_store)
        
        # Assert that check_filings was called
        mock_ticker_store.check_filings.assert_called_once()
        
        # Assert that get_subscribers_by_ticker was called for each ticker
        assert mock_sub_store.get_subscribers_by_ticker.call_count == 2
        
        # Assert that EmailService was instantiated
        mock_email_service_class.assert_called_once()
        
        # Assert that send_email was called for each subscriber
        assert mock_email_service.send_email.call_count == 2
        
        # Assert that the function returned True
        assert result is True
    
    @patch('scheduler.EmailService')
    def test_scheduled_task_with_no_subscribers(self, mock_email_service_class, mock_ticker_store, mock_sub_store):
        """Test scheduled task when there are new filings but no subscribers"""
        # Mock check_filings to return a dictionary with new filings
        mock_filing = MagicMock()
        mock_ticker_store.check_filings.return_value = {"AAPL": mock_filing}
        
        # Mock get_subscribers_by_ticker to return an empty list
        mock_sub_store.get_subscribers_by_ticker.return_value = []
        
        # Mock EmailService
        mock_email_service = MagicMock(spec=EmailService)
        mock_email_service_class.return_value = mock_email_service
        
        # Call the scheduled_task function
        result = scheduled_task(mock_ticker_store, mock_sub_store)
        
        # Assert that check_filings was called
        mock_ticker_store.check_filings.assert_called_once()
        
        # Assert that get_subscribers_by_ticker was called with the correct ticker
        mock_sub_store.get_subscribers_by_ticker.assert_called_once_with("AAPL")
        
        # Assert that EmailService was instantiated
        mock_email_service_class.assert_called_once()
        
        # Assert that send_email was not called
        mock_email_service.send_email.assert_not_called()
        
        # Assert that the function returned True
        assert result is True