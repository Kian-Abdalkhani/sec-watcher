import pytest
import os
import json
from unittest.mock import patch, MagicMock, mock_open

from app.storage.sub_store import SubStore
from app.storage.ticker_store import TickerStore
from app.models.subscriber import Subscriber

class TestSubStore:
    """Test cases for the SubStore class"""
    
    @pytest.fixture
    def mock_file_path(self):
        """Fixture for a mock file path"""
        return "/tmp/test_subscribers.json"
    
    @pytest.fixture
    def mock_ticker_store(self):
        """Fixture for a mock TickerStore"""
        return MagicMock(spec=TickerStore)
    
    @pytest.fixture
    def sample_subscribers(self):
        """Fixture for sample subscriber data"""
        return [
            {
                "name": "John",
                "email": "john@example.com",
                "tickers": ["AAPL", "MSFT"]
            },
            {
                "name": "Jane",
                "email": "jane@example.com",
                "tickers": ["GOOGL", "AMZN"]
            }
        ]
    
    @patch('app.storage.sub_store.os.path.exists')
    @patch('app.storage.sub_store.os.makedirs')
    @patch('app.storage.sub_store.open', new_callable=mock_open)
    @patch('app.storage.sub_store.json.dump')
    def test_ensure_file_exists_new_file(self, mock_json_dump, mock_file_open, mock_makedirs, mock_exists, mock_file_path, mock_ticker_store):
        """Test ensuring the file exists when it doesn't"""
        # Mock os.path.exists to return False (file doesn't exist)
        mock_exists.return_value = False
        
        # Create a SubStore
        sub_store = SubStore(file_path=mock_file_path, ticker_store=mock_ticker_store)
        
        # Assert that the directory was created
        mock_makedirs.assert_called_once()
        
        # Assert that the file was opened for writing
        mock_file_open.assert_called_once_with(mock_file_path, 'w')
        
        # Assert that an empty list was written to the file
        mock_json_dump.assert_called_once_with([], mock_file_open())
    
    @patch('app.storage.sub_store.os.path.exists')
    def test_ensure_file_exists_existing_file(self, mock_exists, mock_file_path, mock_ticker_store):
        """Test ensuring the file exists when it already does"""
        # Mock os.path.exists to return True (file exists)
        mock_exists.return_value = True
        
        # Create a SubStore
        with patch('app.storage.sub_store.open', new_callable=mock_open) as mock_file_open:
            sub_store = SubStore(file_path=mock_file_path, ticker_store=mock_ticker_store)
            
            # Assert that the file was not opened
            mock_file_open.assert_not_called()
    
    @patch('app.storage.sub_store.open', new_callable=mock_open)
    @patch('app.storage.sub_store.os.path.getsize')
    @patch('app.storage.sub_store.json.load')
    def test_get_all_subscribers_empty_file(self, mock_json_load, mock_getsize, mock_file_open, mock_file_path, mock_ticker_store):
        """Test getting all subscribers from an empty file"""
        # Mock os.path.getsize to return 0 (empty file)
        mock_getsize.return_value = 0
        
        # Create a SubStore
        with patch('app.storage.sub_store.os.path.exists', return_value=True):
            sub_store = SubStore(file_path=mock_file_path, ticker_store=mock_ticker_store)
            
            # Call get_all_subscribers
            subscribers = sub_store.get_all_subscribers()
            
            # Assert that the file was opened for reading
            mock_file_open.assert_called_with(mock_file_path, 'r')
            
            # Assert that json.load was not called
            mock_json_load.assert_not_called()
            
            # Assert that an empty list was returned
            assert subscribers == []
    
    @patch('app.storage.sub_store.open', new_callable=mock_open)
    @patch('app.storage.sub_store.os.path.getsize')
    @patch('app.storage.sub_store.json.load')
    def test_get_all_subscribers_non_empty_file(self, mock_json_load, mock_getsize, mock_file_open, mock_file_path, mock_ticker_store, sample_subscribers):
        """Test getting all subscribers from a non-empty file"""
        # Mock os.path.getsize to return a non-zero value
        mock_getsize.return_value = 100
        
        # Mock json.load to return sample subscribers
        mock_json_load.return_value = sample_subscribers
        
        # Create a SubStore
        with patch('app.storage.sub_store.os.path.exists', return_value=True):
            sub_store = SubStore(file_path=mock_file_path, ticker_store=mock_ticker_store)
            
            # Call get_all_subscribers
            subscribers = sub_store.get_all_subscribers()
            
            # Assert that the file was opened for reading
            mock_file_open.assert_called_with(mock_file_path, 'r')
            
            # Assert that json.load was called
            mock_json_load.assert_called_once()
            
            # Assert that the sample subscribers were returned
            assert subscribers == sample_subscribers
    
    @patch('app.storage.sub_store.open', new_callable=mock_open)
    @patch('app.storage.sub_store.json.dump')
    def test_save_subscribers(self, mock_json_dump, mock_file_open, mock_file_path, mock_ticker_store, sample_subscribers):
        """Test saving subscribers to the file"""
        # Create a SubStore
        with patch('app.storage.sub_store.os.path.exists', return_value=True):
            sub_store = SubStore(file_path=mock_file_path, ticker_store=mock_ticker_store)
            
            # Call save_subscribers
            sub_store.save_subscribers(sample_subscribers)
            
            # Assert that the file was opened for writing
            mock_file_open.assert_called_with(mock_file_path, 'w')
            
            # Assert that the subscribers were written to the file
            mock_json_dump.assert_called_with(sample_subscribers, mock_file_open(), indent=2)
            
            # Assert that refresh_tickers was called on the ticker_store
            mock_ticker_store.refresh_tickers.assert_called_once_with(sub_store.get_all_tickers())
    
    @patch('app.storage.sub_store.Subscriber')
    @patch('app.storage.sub_store.SubStore.get_all_subscribers')
    @patch('app.storage.sub_store.SubStore.save_subscribers')
    def test_add_subscriber_new(self, mock_save_subscribers, mock_get_all_subscribers, mock_subscriber, mock_file_path, mock_ticker_store):
        """Test adding a new subscriber"""
        # Mock get_all_subscribers to return an empty list
        mock_get_all_subscribers.return_value = []
        
        # Mock Subscriber to return a mock subscriber
        mock_subscriber_instance = MagicMock()
        mock_subscriber_instance.email = "john@example.com"
        mock_subscriber_instance.tickers = ["AAPL", "MSFT"]
        mock_subscriber_instance.to_dict.return_value = {
            "name": "John",
            "email": "john@example.com",
            "tickers": ["AAPL", "MSFT"]
        }
        mock_subscriber.return_value = mock_subscriber_instance
        
        # Create a SubStore
        with patch('app.storage.sub_store.os.path.exists', return_value=True):
            sub_store = SubStore(file_path=mock_file_path, ticker_store=mock_ticker_store)
            
            # Call add_subscriber
            result = sub_store.add_subscriber(
                name="John",
                email="john@example.com",
                tickers=["AAPL", "MSFT"]
            )
            
            # Assert that Subscriber was created with the correct parameters
            mock_subscriber.assert_called_once_with(
                name="John",
                email="john@example.com",
                tickers=["AAPL", "MSFT"]
            )
            
            # Assert that save_subscribers was called with the new subscriber
            mock_save_subscribers.assert_called_once_with([mock_subscriber_instance.to_dict()])
            
            # Assert that the method returned True
            assert result is True
    
    @patch('app.storage.sub_store.Subscriber')
    @patch('app.storage.sub_store.SubStore.get_all_subscribers')
    @patch('app.storage.sub_store.SubStore.save_subscribers')
    def test_add_subscriber_existing_same_tickers(self, mock_save_subscribers, mock_get_all_subscribers, mock_subscriber, mock_file_path, mock_ticker_store):
        """Test adding a subscriber that already exists with the same tickers"""
        # Mock get_all_subscribers to return a list with the subscriber
        mock_get_all_subscribers.return_value = [{
            "name": "John",
            "email": "john@example.com",
            "tickers": ["AAPL", "MSFT"]
        }]
        
        # Mock Subscriber to return a mock subscriber
        mock_subscriber_instance = MagicMock()
        mock_subscriber_instance.email = "john@example.com"
        mock_subscriber_instance.tickers = ["AAPL", "MSFT"]
        mock_subscriber.return_value = mock_subscriber_instance
        
        # Create a SubStore
        with patch('app.storage.sub_store.os.path.exists', return_value=True):
            sub_store = SubStore(file_path=mock_file_path, ticker_store=mock_ticker_store)
            
            # Call add_subscriber
            with pytest.raises(ValueError, match="Subscriber already exists"):
                sub_store.add_subscriber(
                    name="John",
                    email="john@example.com",
                    tickers=["AAPL", "MSFT"]
                )
            
            # Assert that save_subscribers was not called
            mock_save_subscribers.assert_not_called()
    
    @patch('app.storage.sub_store.Subscriber')
    @patch('app.storage.sub_store.SubStore.get_all_subscribers')
    @patch('app.storage.sub_store.SubStore.save_subscribers')
    def test_add_subscriber_existing_different_tickers(self, mock_save_subscribers, mock_get_all_subscribers, mock_subscriber, mock_file_path, mock_ticker_store):
        """Test adding a subscriber that already exists but with different tickers"""
        # Mock get_all_subscribers to return a list with the subscriber
        mock_get_all_subscribers.return_value = [{
            "name": "John",
            "email": "john@example.com",
            "tickers": ["AAPL", "MSFT"]
        }]
        
        # Mock Subscriber to return a mock subscriber
        mock_subscriber_instance = MagicMock()
        mock_subscriber_instance.email = "john@example.com"
        mock_subscriber_instance.tickers = ["GOOGL", "AMZN"]
        mock_subscriber.return_value = mock_subscriber_instance
        
        # Create a SubStore
        with patch('app.storage.sub_store.os.path.exists', return_value=True):
            sub_store = SubStore(file_path=mock_file_path, ticker_store=mock_ticker_store)
            
            # Call add_subscriber
            result = sub_store.add_subscriber(
                name="John",
                email="john@example.com",
                tickers=["GOOGL", "AMZN"]
            )
            
            # Assert that save_subscribers was called with the updated subscriber
            mock_save_subscribers.assert_called_once_with([{
                "name": "John",
                "email": "john@example.com",
                "tickers": ["GOOGL", "AMZN"]
            }])
            
            # Assert that the method returned True
            assert result is True
    
    @patch('app.storage.sub_store.SubStore.get_all_subscribers')
    @patch('app.storage.sub_store.SubStore.save_subscribers')
    def test_remove_subscriber_existing(self, mock_save_subscribers, mock_get_all_subscribers, mock_file_path, mock_ticker_store, sample_subscribers):
        """Test removing an existing subscriber"""
        # Mock get_all_subscribers to return sample subscribers
        mock_get_all_subscribers.return_value = sample_subscribers
        
        # Create a SubStore
        with patch('app.storage.sub_store.os.path.exists', return_value=True):
            sub_store = SubStore(file_path=mock_file_path, ticker_store=mock_ticker_store)
            
            # Call remove_subscriber
            result = sub_store.remove_subscriber("john@example.com")
            
            # Assert that save_subscribers was called with the remaining subscriber
            mock_save_subscribers.assert_called_once_with([sample_subscribers[1]])
            
            # Assert that the method returned True
            assert result is True
    
    @patch('app.storage.sub_store.SubStore.get_all_subscribers')
    @patch('app.storage.sub_store.SubStore.save_subscribers')
    def test_remove_subscriber_non_existing(self, mock_save_subscribers, mock_get_all_subscribers, mock_file_path, mock_ticker_store, sample_subscribers):
        """Test removing a non-existing subscriber"""
        # Mock get_all_subscribers to return sample subscribers
        mock_get_all_subscribers.return_value = sample_subscribers
        
        # Create a SubStore
        with patch('app.storage.sub_store.os.path.exists', return_value=True):
            sub_store = SubStore(file_path=mock_file_path, ticker_store=mock_ticker_store)
            
            # Call remove_subscriber
            result = sub_store.remove_subscriber("nonexistent@example.com")
            
            # Assert that save_subscribers was not called
            mock_save_subscribers.assert_not_called()
            
            # Assert that the method returned False
            assert result is False
    
    @patch('app.storage.sub_store.SubStore.get_all_subscribers')
    def test_get_all_tickers(self, mock_get_all_subscribers, mock_file_path, mock_ticker_store, sample_subscribers):
        """Test getting all tickers from subscribers"""
        # Mock get_all_subscribers to return sample subscribers
        mock_get_all_subscribers.return_value = sample_subscribers
        
        # Create a SubStore
        with patch('app.storage.sub_store.os.path.exists', return_value=True):
            sub_store = SubStore(file_path=mock_file_path, ticker_store=mock_ticker_store)
            
            # Call get_all_tickers
            tickers = sub_store.get_all_tickers()
            
            # Assert that the correct tickers were returned (unique and sorted)
            assert set(tickers) == {"AAPL", "MSFT", "GOOGL", "AMZN"}
    
    @patch('app.storage.sub_store.SubStore.get_all_subscribers')
    def test_get_subscribers_by_ticker(self, mock_get_all_subscribers, mock_file_path, mock_ticker_store, sample_subscribers):
        """Test getting subscribers by ticker"""
        # Mock get_all_subscribers to return sample subscribers
        mock_get_all_subscribers.return_value = sample_subscribers
        
        # Create a SubStore
        with patch('app.storage.sub_store.os.path.exists', return_value=True):
            sub_store = SubStore(file_path=mock_file_path, ticker_store=mock_ticker_store)
            
            # Call get_subscribers_by_ticker
            subscribers = sub_store.get_subscribers_by_ticker("AAPL")
            
            # Assert that the correct subscribers were returned
            assert len(subscribers) == 1
            assert subscribers[0]["email"] == "john@example.com"
            
            # Test case insensitivity
            subscribers = sub_store.get_subscribers_by_ticker("aapl")
            assert len(subscribers) == 1
            assert subscribers[0]["email"] == "john@example.com"