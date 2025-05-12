"""Data Models"""

from typing import List
import re
from datetime import datetime

from app.services.sec_service import get_cik

class Subscriber:
    """Class for creating subscriber objects"""
    def __init__(self, email: str, name: str, tickers: List[str]):
        self.validate_name(name)
        self.validate_email(email)
        self.validate_tickers(tickers)

        self.name = name
        self.email = email
        self.tickers = [ticker.upper() for ticker in tickers]

    @staticmethod
    def validate_name(name: str) -> None:

        if len(name) == 0:
            raise ValueError('Name cannot be empty')
        if len(name) > 25:
            raise ValueError('Name cannot be more than 25 characters')
        if name.isalpha() is False:
            raise ValueError('Name can only contain letters')


    @staticmethod
    def validate_email(email: str) -> None:
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise ValueError('Invalid email format')

    @staticmethod
    def validate_tickers(tickers: List[str]) -> None:
        if len(tickers) == 0:
            raise ValueError('Tickers cannot be empty')
        for ticker in tickers:
            cik: str = get_cik(ticker)
            if cik == "":
                raise ValueError('Invalid ticker')

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'email': self.email,
            'tickers': self.tickers
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Subscriber':
        return cls(
            name=data.get("name",""),
            email=data.get("email",""),
            tickers=data.get("tickers",[])
        )


