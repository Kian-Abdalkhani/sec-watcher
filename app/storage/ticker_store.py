"""Stores ticker and last filing into a json file"""
import os
import json
from typing import List, Dict, Any
import logging

from app.services.sec_service import get_filings

logger = logging.getLogger(__name__)

class TickerStore:
    def __init__(self, file_path):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            with open(self.file_path, 'w') as f:
                json.dump([], f)

    def save_tickers(self, tickers: List[Dict[str, Any]]) -> None:
        with open(self.file_path, 'w') as f:
            json.dump(tickers, f, indent=2)

    def get_all_tickers(self) -> List[Dict[str, Any]]:
        with open(self.file_path, 'r') as f:
            if os.path.getsize(self.file_path) == 0:
                return []
            else:
                return json.load(f)

    def refresh_tickers(self,tickers: list == []) -> None:
        """Updates ticker list after every subscriber list change"""
        ticker_data = self.get_all_tickers()
        current_tick_list = [tick["ticker"] for tick in ticker_data]
        #if new ticker in list
        if tickers not in current_tick_list:
            ticker_data.append({"ticker":tickers,"last_filing":""})
        #for old tickers to be removed
        for tick in ticker_data:
            if tick["ticker"] not in tickers:
                ticker_data.remove(tick)
        logger.info(f"Tickers {tickers} synced to {self.file_path} successfully.")
        self.save_tickers(ticker_data)

    def check_filings(self) -> dict[str,Any]:
        """returns a list of tickers with new filings"""
        ticker_list = self.get_all_tickers()
        new_filings = {}
        for ticker in ticker_list:
            latest_filing = get_filings(ticker["ticker"]).iloc[0]
            if ticker["last_filing"] == "":
                ticker["last_filing"] = latest_filing["accessionNumber"]
            elif ticker["last_filing"] != latest_filing["accessionNumber"]:
                new_filings[ticker["ticker"]] = latest_filing
                ticker["last_filing"] = latest_filing["accessionNumber"]
            else:
                continue

        self.save_tickers(ticker_list)
        return new_filings










