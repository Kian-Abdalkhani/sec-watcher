# SEC Watcher Tests

This directory contains tests for the SEC Watcher application. The tests are written using pytest and cover all the main components of the application.

## Test Structure

- `test_subscriber.py`: Tests for the Subscriber model
- `test_sec_service.py`: Tests for the SEC service
- `test_email_service.py`: Tests for the email service
- `test_ticker_store.py`: Tests for the TickerStore class
- `test_sub_store.py`: Tests for the SubStore class
- `test_scheduler.py`: Tests for the scheduler functionality
- `conftest.py`: Common fixtures and configuration for all tests

## Running the Tests

To run all tests:

```bash
pytest
```

To run a specific test file:

```bash
pytest tests/test_subscriber.py
```

To run a specific test:

```bash
pytest tests/test_subscriber.py::TestSubscriber::test_valid_subscriber_creation
```

To run tests with verbose output:

```bash
pytest -v
```

## Test Coverage

The tests cover the following functionality:

### Subscriber Model
- Creating a valid subscriber
- Converting a subscriber to a dictionary
- Creating a subscriber from a dictionary
- Validation for invalid names
- Validation for email addresses
- Validation for tickers

### SEC Service
- Getting a CIK for a valid ticker
- Getting a CIK for an invalid ticker
- Getting a CIK without leading zeros
- Getting filings for a ticker
- Checking for new filings

### Email Service
- Connecting to the SMTP server
- Sending an email successfully
- Handling failures when sending an email
- Verifying the format of the email being sent

### TickerStore
- Ensuring the file exists
- Saving tickers to the file
- Getting all tickers
- Refreshing tickers
- Checking for filings

### SubStore
- Ensuring the file exists
- Getting all subscribers
- Saving subscribers
- Adding a subscriber
- Removing a subscriber
- Getting all tickers
- Getting subscribers by ticker

### Scheduler
- Scheduled task when there are no new filings
- Scheduled task when there are new filings
- Scheduled task when there are new filings for multiple tickers
- Scheduled task when there are new filings but no subscribers

## Mocking

The tests use unittest.mock to mock external dependencies such as:
- File operations
- API calls
- SMTP server
- Other components of the application

This ensures that the tests are isolated and do not depend on external services or the state of the file system.