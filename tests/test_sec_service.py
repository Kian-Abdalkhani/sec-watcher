import pytest
import pandas as pd
from unittest.mock import patch, MagicMock

from app.services.sec_service import get_cik, get_filings, check_new_filings

class TestSECService:
    """Test cases for the SEC service"""
    
    @patch('app.services.sec_service.r.get')
    def test_get_cik_valid_ticker(self, mock_get):
        """Test getting CIK for a valid ticker"""
        # Mock the response from the SEC API
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "0": {"cik_str": 320193, "ticker": "AAPL", "title": "Apple Inc."}
        }
        mock_get.return_value = mock_response
        
        # Call the function with a valid ticker
        cik = get_cik("AAPL")
        
        # Assert that the CIK is correct with leading zeros
        assert cik == "0000320193"
        
        # Assert that the API was called with the correct URL and headers
        mock_get.assert_called_once()
    
    @patch('app.services.sec_service.r.get')
    def test_get_cik_invalid_ticker(self, mock_get):
        """Test getting CIK for an invalid ticker"""
        # Mock the response from the SEC API
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "0": {"cik_str": 320193, "ticker": "AAPL", "title": "Apple Inc."}
        }
        mock_get.return_value = mock_response
        
        # Call the function with an invalid ticker
        cik = get_cik("INVALID")
        
        # Assert that an empty string is returned
        assert cik == ""
        
        # Assert that the API was called
        mock_get.assert_called_once()
    
    @patch('app.services.sec_service.r.get')
    def test_get_cik_no_leading_zeros(self, mock_get):
        """Test getting CIK without leading zeros"""
        # Mock the response from the SEC API
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "0": {"cik_str": 320193, "ticker": "AAPL", "title": "Apple Inc."}
        }
        mock_get.return_value = mock_response
        
        # Call the function with a valid ticker and lead_zeros=False
        cik = get_cik("AAPL", lead_zeros=False)
        
        # Assert that the CIK is correct without leading zeros
        assert cik == "320193"
        
        # Assert that the API was called
        mock_get.assert_called_once()
    
    @patch('app.services.sec_service.get_cik')
    @patch('app.services.sec_service.r.get')
    def test_get_filings(self, mock_get, mock_get_cik):
        """Test getting filings for a ticker"""
        # Mock the get_cik function to return a valid CIK
        mock_get_cik.return_value = "0000320193"
        
        # Mock the response from the SEC API
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "filings": {
                "recent": {
                    "accessionNumber": ["0000320193-23-000001", "0000320193-23-000002"],
                    "filingDate": ["2023-01-01", "2023-01-02"],
                    "reportDate": ["2022-12-31", "2022-12-31"],
                    "form": ["10-K", "8-K"]
                }
            }
        }
        mock_get.return_value = mock_response
        
        # Call the function
        filings = get_filings("AAPL")
        
        # Assert that the result is a DataFrame with the correct data
        assert isinstance(filings, pd.DataFrame)
        assert len(filings) == 2
        assert list(filings.columns) == ["accessionNumber", "filingDate", "reportDate", "form"]
        
        # Assert that the date fields were converted to datetime
        assert pd.api.types.is_datetime64_dtype(filings['filingDate'])
        assert pd.api.types.is_datetime64_dtype(filings['reportDate'])
        
        # Assert that the API was called with the correct URL
        mock_get.assert_called_once()
    
    @patch('app.services.sec_service.get_filings')
    def test_check_new_filings_true(self, mock_get_filings):
        """Test checking for new filings when there are filings"""
        # Mock the get_filings function to return a non-empty DataFrame
        mock_df = pd.DataFrame({
            "accessionNumber": ["0000320193-23-000001"],
            "filingDate": ["2023-01-01"],
            "reportDate": ["2022-12-31"],
            "form": ["10-K"]
        })
        mock_get_filings.return_value = mock_df
        
        # Call the function
        result = check_new_filings("AAPL")
        
        # Assert that the result is True
        assert result is True
        
        # Assert that get_filings was called with the correct ticker
        mock_get_filings.assert_called_once_with("AAPL")
    
    @patch('app.services.sec_service.get_filings')
    def test_check_new_filings_false(self, mock_get_filings):
        """Test checking for new filings when there are no filings"""
        # Mock the get_filings function to return an empty DataFrame
        mock_get_filings.return_value = pd.DataFrame()
        
        # Call the function
        result = check_new_filings("AAPL")
        
        # Assert that the result is False
        assert result is False
        
        # Assert that get_filings was called with the correct ticker
        mock_get_filings.assert_called_once_with("AAPL")