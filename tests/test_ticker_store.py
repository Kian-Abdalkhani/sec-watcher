import pytest
import os
import json
import pandas as pd
from unittest.mock import patch, MagicMock, mock_open

from app.storage.ticker_store import TickerStore

class TestTickerStore:
    """Test cases for the TickerStore class"""
    
    @pytest.fixture
    def mock_file_path(self):
        """Fixture for a mock file path"""
        return "/tmp/test_tickers.json"
    
    @pytest.fixture
    def sample_tickers(self):
        """Fixture for sample ticker data"""
        return [
            {"ticker": "AAPL", "last_filing": "0000320193-23-000001"},
            {"ticker": "MSFT", "last_filing": "0000789019-23-000001"}
        ]
    
    @patch('app.storage.ticker_store.os.path.exists')
    @patch('app.storage.ticker_store.os.makedirs')
    @patch('app.storage.ticker_store.open', new_callable=mock_open)
    @patch('app.storage.ticker_store.json.dump')
    def test_ensure_file_exists_new_file(self, mock_json_dump, mock_file_open, mock_makedirs, mock_exists, mock_file_path):
        """Test ensuring the file exists when it doesn't"""
        # Mock os.path.exists to return False (file doesn't exist)
        mock_exists.return_value = False
        
        # Create a TickerStore
        ticker_store = TickerStore(file_path=mock_file_path)
        
        # Assert that the directory was created
        mock_makedirs.assert_called_once()
        
        # Assert that the file was opened for writing
        mock_file_open.assert_called_once_with(mock_file_path, 'w')
        
        # Assert that an empty list was written to the file
        mock_json_dump.assert_called_once_with([], mock_file_open())
    
    @patch('app.storage.ticker_store.os.path.exists')
    def test_ensure_file_exists_existing_file(self, mock_exists, mock_file_path):
        """Test ensuring the file exists when it already does"""
        # Mock os.path.exists to return True (file exists)
        mock_exists.return_value = True
        
        # Create a TickerStore
        with patch('app.storage.ticker_store.open', new_callable=mock_open) as mock_file_open:
            ticker_store = TickerStore(file_path=mock_file_path)
            
            # Assert that the file was not opened
            mock_file_open.assert_not_called()
    
    @patch('app.storage.ticker_store.open', new_callable=mock_open)
    @patch('app.storage.ticker_store.json.dump')
    def test_save_tickers(self, mock_json_dump, mock_file_open, mock_file_path, sample_tickers):
        """Test saving tickers to the file"""
        # Create a TickerStore
        with patch('app.storage.ticker_store.os.path.exists', return_value=True):
            ticker_store = TickerStore(file_path=mock_file_path)
            
            # Call save_tickers
            ticker_store.save_tickers(sample_tickers)
            
            # Assert that the file was opened for writing
            mock_file_open.assert_called_with(mock_file_path, 'w')
            
            # Assert that the tickers were written to the file
            mock_json_dump.assert_called_with(sample_tickers, mock_file_open(), indent=2)
    
    @patch('app.storage.ticker_store.open', new_callable=mock_open)
    @patch('app.storage.ticker_store.os.path.getsize')
    @patch('app.storage.ticker_store.json.load')
    def test_get_all_tickers_empty_file(self, mock_json_load, mock_getsize, mock_file_open, mock_file_path):
        """Test getting all tickers from an empty file"""
        # Mock os.path.getsize to return 0 (empty file)
        mock_getsize.return_value = 0
        
        # Create a TickerStore
        with patch('app.storage.ticker_store.os.path.exists', return_value=True):
            ticker_store = TickerStore(file_path=mock_file_path)
            
            # Call get_all_tickers
            tickers = ticker_store.get_all_tickers()
            
            # Assert that the file was opened for reading
            mock_file_open.assert_called_with(mock_file_path, 'r')
            
            # Assert that json.load was not called
            mock_json_load.assert_not_called()
            
            # Assert that an empty list was returned
            assert tickers == []
    
    @patch('app.storage.ticker_store.open', new_callable=mock_open)
    @patch('app.storage.ticker_store.os.path.getsize')
    @patch('app.storage.ticker_store.json.load')
    def test_get_all_tickers_non_empty_file(self, mock_json_load, mock_getsize, mock_file_open, mock_file_path, sample_tickers):
        """Test getting all tickers from a non-empty file"""
        # Mock os.path.getsize to return a non-zero value
        mock_getsize.return_value = 100
        
        # Mock json.load to return sample tickers
        mock_json_load.return_value = sample_tickers
        
        # Create a TickerStore
        with patch('app.storage.ticker_store.os.path.exists', return_value=True):
            ticker_store = TickerStore(file_path=mock_file_path)
            
            # Call get_all_tickers
            tickers = ticker_store.get_all_tickers()
            
            # Assert that the file was opened for reading
            mock_file_open.assert_called_with(mock_file_path, 'r')
            
            # Assert that json.load was called
            mock_json_load.assert_called_once()
            
            # Assert that the sample tickers were returned
            assert tickers == sample_tickers
    
    @patch('app.storage.ticker_store.TickerStore.get_all_tickers')
    @patch('app.storage.ticker_store.TickerStore.save_tickers')
    def test_refresh_tickers_new_ticker(self, mock_save_tickers, mock_get_all_tickers, mock_file_path):
        """Test refreshing tickers with a new ticker"""
        # Mock get_all_tickers to return an empty list
        mock_get_all_tickers.return_value = []
        
        # Create a TickerStore
        with patch('app.storage.ticker_store.os.path.exists', return_value=True):
            ticker_store = TickerStore(file_path=mock_file_path)
            
            # Call refresh_tickers with a new ticker
            ticker_store.refresh_tickers("AAPL")
            
            # Assert that save_tickers was called with the new ticker
            mock_save_tickers.assert_called_with([{"ticker": "AAPL", "last_filing": ""}])
    
    @patch('app.storage.ticker_store.TickerStore.get_all_tickers')
    @patch('app.storage.ticker_store.TickerStore.save_tickers')
    def test_refresh_tickers_remove_ticker(self, mock_save_tickers, mock_get_all_tickers, mock_file_path, sample_tickers):
        """Test refreshing tickers to remove a ticker"""
        # Mock get_all_tickers to return sample tickers
        mock_get_all_tickers.return_value = sample_tickers
        
        # Create a TickerStore
        with patch('app.storage.ticker_store.os.path.exists', return_value=True):
            ticker_store = TickerStore(file_path=mock_file_path)
            
            # Call refresh_tickers with only one of the tickers
            ticker_store.refresh_tickers("AAPL")
            
            # Assert that save_tickers was called with only the AAPL ticker
            mock_save_tickers.assert_called_with([{"ticker": "AAPL", "last_filing": "0000320193-23-000001"}])
    
    @patch('app.storage.ticker_store.get_filings')
    @patch('app.storage.ticker_store.TickerStore.get_all_tickers')
    @patch('app.storage.ticker_store.TickerStore.save_tickers')
    def test_check_filings_no_new_filings(self, mock_save_tickers, mock_get_all_tickers, mock_get_filings, mock_file_path):
        """Test checking for filings when there are no new filings"""
        # Mock get_all_tickers to return a ticker with a last filing
        mock_get_all_tickers.return_value = [{"ticker": "AAPL", "last_filing": "0000320193-23-000001"}]
        
        # Mock get_filings to return a DataFrame with the same accessionNumber
        mock_df = pd.DataFrame({"accessionNumber": ["0000320193-23-000001"]})
        mock_get_filings.return_value = mock_df
        
        # Create a TickerStore
        with patch('app.storage.ticker_store.os.path.exists', return_value=True):
            ticker_store = TickerStore(file_path=mock_file_path)
            
            # Call check_filings
            new_filings = ticker_store.check_filings()
            
            # Assert that get_filings was called with the ticker
            mock_get_filings.assert_called_with("AAPL")
            
            # Assert that save_tickers was called
            mock_save_tickers.assert_called_once()
            
            # Assert that no new filings were returned
            assert new_filings == {}
    
    @patch('app.storage.ticker_store.get_filings')
    @patch('app.storage.ticker_store.TickerStore.get_all_tickers')
    @patch('app.storage.ticker_store.TickerStore.save_tickers')
    def test_check_filings_new_filing(self, mock_save_tickers, mock_get_all_tickers, mock_get_filings, mock_file_path):
        """Test checking for filings when there is a new filing"""
        # Mock get_all_tickers to return a ticker with a last filing
        mock_get_all_tickers.return_value = [{"ticker": "AAPL", "last_filing": "0000320193-23-000001"}]
        
        # Mock get_filings to return a DataFrame with a different accessionNumber
        mock_df = pd.DataFrame({"accessionNumber": ["0000320193-23-000002"]})
        mock_get_filings.return_value = mock_df
        
        # Create a TickerStore
        with patch('app.storage.ticker_store.os.path.exists', return_value=True):
            ticker_store = TickerStore(file_path=mock_file_path)
            
            # Call check_filings
            new_filings = ticker_store.check_filings()
            
            # Assert that get_filings was called with the ticker
            mock_get_filings.assert_called_with("AAPL")
            
            # Assert that save_tickers was called with the updated last_filing
            mock_save_tickers.assert_called_once()
            
            # Assert that the new filing was returned
            assert "AAPL" in new_filings
            assert new_filings["AAPL"] is mock_df.iloc[0]
    
    @patch('app.storage.ticker_store.get_filings')
    @patch('app.storage.ticker_store.TickerStore.get_all_tickers')
    @patch('app.storage.ticker_store.TickerStore.save_tickers')
    def test_check_filings_first_filing(self, mock_save_tickers, mock_get_all_tickers, mock_get_filings, mock_file_path):
        """Test checking for filings when it's the first filing"""
        # Mock get_all_tickers to return a ticker with an empty last_filing
        mock_get_all_tickers.return_value = [{"ticker": "AAPL", "last_filing": ""}]
        
        # Mock get_filings to return a DataFrame with an accessionNumber
        mock_df = pd.DataFrame({"accessionNumber": ["0000320193-23-000001"]})
        mock_get_filings.return_value = mock_df
        
        # Create a TickerStore
        with patch('app.storage.ticker_store.os.path.exists', return_value=True):
            ticker_store = TickerStore(file_path=mock_file_path)
            
            # Call check_filings
            new_filings = ticker_store.check_filings()
            
            # Assert that get_filings was called with the ticker
            mock_get_filings.assert_called_with("AAPL")
            
            # Assert that save_tickers was called with the updated last_filing
            mock_save_tickers.assert_called_once()
            
            # Assert that no new filings were returned (first filing is not considered "new")
            assert new_filings == {}