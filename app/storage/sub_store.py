"""Stores subscriber data into JSON file"""
import json
import os
from typing import List, Dict, Any

from app.models.subscriber import Subscriber
from app.storage.ticker_store import TickerStore


class SubStore:
    def __init__(self, file_path, ticker_store: TickerStore):
        self.file_path = file_path
        self._ensure_file_exists()
        self.ticker_store = ticker_store

    def _ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            with open(self.file_path, 'w') as f:
                json.dump([], f)

    def get_all_subscribers(self) -> List[Dict[str, Any]]:
        with open(self.file_path, 'r') as f:
            if os.path.getsize(self.file_path) == 0:
                return []
            else:
                return json.load(f)

    def save_subscribers(self, subscribers: List[Dict[str, Any]]):
        with open(self.file_path, 'w') as f:
            json.dump(subscribers, f, indent=2)
        self.ticker_store.refresh_tickers(self.get_all_tickers())

    def add_subscriber(self, name: str, email: str, tickers: List[str]) -> bool:
        try:
            new_subscriber = Subscriber(email=email, name=name, tickers=tickers)

            #get existing subscribers and add a new one
            subscribers = self.get_all_subscribers()
            for subscriber in subscribers:
                #check if subscriber already exists
                if subscriber["email"] == new_subscriber.email:

                    #checks if tickers are different
                    if subscriber["tickers"] != new_subscriber.tickers:
                        subscriber["tickers"] = new_subscriber.tickers
                        self.save_subscribers(subscribers)
                        return True
                    else: # If exact same Subscriber
                        raise ValueError("Subscriber already exists")
            # If new Subscriber
            subscribers.append(new_subscriber.to_dict())
            self.save_subscribers(subscribers)
            return True

        except ValueError as e:
            print(f"Validation error: {str(e)}")
            return False

    def remove_subscriber(self, email: str) -> bool:
        try:
            subscribers = self.get_all_subscribers()
            for subscriber in subscribers:
                if subscriber["email"] == email:
                    subscribers.remove(subscriber)
                    self.save_subscribers(subscribers)
                    return True

            return False
        except ValueError as e:
            print(f"Validation error: {str(e)}")
            return False

    def get_all_tickers(self) -> List[str]:
        subscribers = self.get_all_subscribers()
        tickers = []
        for sub in subscribers:
            tickers.extend(sub["tickers"])
        return list(set(tickers))

    def get_subscribers_by_ticker(self, ticker: str) -> List[Dict[str, Any]]:
        subscribers = self.get_all_subscribers()
        return [sub for sub in subscribers if ticker.upper() in [t.upper() for t in sub["tickers"]]]