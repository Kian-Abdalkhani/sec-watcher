"""Scheduled Task Runner"""
from app.storage.ticker_store import TickerStore
from app.storage.sub_store import SubStore
from app.services.email_service import EmailService
from datetime import datetime

def scheduled_task(tick_list: TickerStore, sub_list: SubStore) -> bool:
    new_filings = tick_list.check_filings()

    #if no new filings, stop check
    if new_filings == {}:
        print(f"{datetime.now()}: No new filings")
        return False

    emailer = EmailService()
    for ticker, filing in new_filings.items():
        subscribers = sub_list.get_subscribers_by_ticker(ticker)
        for subscriber in subscribers:
            emailer.send_email(subscriber_email=subscriber["email"],
                               subject=f"New {ticker} filing",
                               message=f"New {ticker} filing: {filing}"
                               )
        print(f"{datetime.now()}: New filings for {ticker}")
    return True