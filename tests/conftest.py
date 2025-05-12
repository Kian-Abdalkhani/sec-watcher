import pytest
import os
import tempfile
import json
from unittest.mock import MagicMock

from app.storage.ticker_store import TickerStore
from app.storage.sub_store import SubStore

@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir

@pytest.fixture
def temp_ticker_file(temp_dir):
    """Create a temporary ticker file path"""
    return os.path.join(temp_dir, "tickers.json")

@pytest.fixture
def temp_subscriber_file(temp_dir):
    """Create a temporary subscriber file path"""
    return os.path.join(temp_dir, "subscribers.json")

@pytest.fixture
def sample_tickers():
    """Sample ticker data for tests"""
    return [
        {"ticker": "AAPL", "last_filing": "0000320193-23-000001"},
        {"ticker": "MSFT", "last_filing": "0000789019-23-000001"}
    ]

@pytest.fixture
def sample_subscribers():
    """Sample subscriber data for tests"""
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

@pytest.fixture
def mock_ticker_store():
    """Mock TickerStore for tests"""
    return MagicMock(spec=TickerStore)

@pytest.fixture
def mock_sub_store():
    """Mock SubStore for tests"""
    return MagicMock(spec=SubStore)

@pytest.fixture
def ticker_store_with_data(temp_ticker_file, sample_tickers):
    """Create a TickerStore with sample data"""
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(temp_ticker_file), exist_ok=True)
    
    # Write sample data to the file
    with open(temp_ticker_file, 'w') as f:
        json.dump(sample_tickers, f)
    
    # Create and return the TickerStore
    return TickerStore(file_path=temp_ticker_file)

@pytest.fixture
def sub_store_with_data(temp_subscriber_file, sample_subscribers, ticker_store_with_data):
    """Create a SubStore with sample data"""
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(temp_subscriber_file), exist_ok=True)
    
    # Write sample data to the file
    with open(temp_subscriber_file, 'w') as f:
        json.dump(sample_subscribers, f)
    
    # Create and return the SubStore
    return SubStore(file_path=temp_subscriber_file, ticker_store=ticker_store_with_data)