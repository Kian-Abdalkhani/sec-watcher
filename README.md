# SEC Watcher

SEC Watcher is an automated system that monitors SEC filings for specified ticker symbols and sends email notifications to subscribers when new filings are detected.

## Features

- Monitors SEC filings for multiple ticker symbols
- Sends email notifications to subscribers when new filings are detected
- Configurable monitoring frequency
- Easy subscriber management
- Persistent storage of ticker and subscriber data

## Requirements

- Python 3.12 or higher
- Docker and Docker Compose (for containerized deployment)

## Installation

### Using Python with uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast, reliable Python package installer and resolver, written in Rust.

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/sec-watcher.git
   cd sec-watcher
   ```

2. Install uv:
   ```bash
   # Using pip
   pip install uv

   # Using curl (macOS/Linux)
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Using PowerShell (Windows)
   irm https://astral.sh/uv/install.ps1 | iex
   ```

3. Create a virtual environment and install dependencies:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -e .
   ```
   
### Using Python with pip

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/sec-watcher.git
   cd sec-watcher
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   ```

### Using Docker

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/sec-watcher.git
   cd sec-watcher
   ```

2. Build and run the Docker container:
   ```bash
   docker-compose up -d
   ```

   Note: The Docker image uses uv instead of pip for package installation and environment management, providing faster and more reliable dependency resolution.

## Configuration

1. Copy the environment template file:
   ```bash
   cp .env.template .env
   ```

2. Edit the `.env` file and fill in your email credentials:
   ```
   EMAIL_ADDRESS=your_email@gmail.com
   PASSWORD=your_app_password
   ```

   Note: For Gmail, you need to use an app password. You can generate one at https://myaccount.google.com/apppasswords

3. Additional configuration options can be found in `app/config.py`:
   - `TASK_FREQ`: Frequency of checking for new filings (in minutes)
   - `API_TIMEOUT`: Timeout for SEC API requests (in seconds)
   - `SEC_CIK_URL` and `SEC_FILINGS_URL`: URLs for SEC API endpoints

## Usage

### Running the Application

```bash
python main.py
```

The application will start and run in the background, checking for new SEC filings at the configured interval.

### Managing Subscribers

Subscribers are stored in `data/subscribers.json`. You can add or remove subscribers programmatically using the `SubStore` class:

```python
from app.storage.sub_store import SubStore
from app.storage.ticker_store import TickerStore
from app.config import SUB_PATH, TICK_PATH

# Initialize stores
tick_list = TickerStore(file_path=TICK_PATH)
sub_list = SubStore(file_path=SUB_PATH, ticker_store=tick_list)

# Add a subscriber
sub_list.add_subscriber(
    name="John Doe",
    email="john.doe@example.com",
    tickers=["AAPL", "MSFT", "GOOGL"]
)

# Remove a subscriber
sub_list.remove_subscriber(email="john.doe@example.com")
```

### Managing Tickers

Tickers are stored in `data/tickers.json` and are automatically managed based on subscriber preferences. The system will only monitor tickers that have at least one subscriber.

## Testing

Tests are written using pytest. To run the tests:

```bash
pytest
```

## Docker Deployment

The project includes Docker and Docker Compose configuration for easy deployment:

```bash
# Build and start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

## Project Structure

- `app/`: Main application package
  - `config.py`: Configuration settings
  - `models/`: Data models
  - `services/`: Service classes for SEC API and email
  - `storage/`: Storage classes for tickers and subscribers
- `data/`: Data storage directory
  - `subscribers.json`: Subscriber data
  - `tickers.json`: Ticker data
- `tests/`: Test directory
- `main.py`: Application entry point
- `scheduler.py`: Scheduled task definition
- `pyproject.toml`: Project metadata and dependencies

## License

[MIT License](LICENSE)
