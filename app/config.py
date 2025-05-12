import os
from dotenv import load_dotenv

#load environment variables from .env file
load_dotenv()

#Frequency of scheduled task to be ran (minutes)
TASK_FREQ = 30

#Email Credentials for Email Service
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("PASSWORD")

#header for SEC Web Scraping
HEADERS = {'User-Agent': EMAIL_ADDRESS}

#URLs for SEC
SEC_CIK_URL = "https://www.sec.gov/files/company_tickers.json"
SEC_FILINGS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"
API_TIMEOUT = 30

#paths for both stores
SUB_PATH = os.path.join(os.getcwd(), "data", "subscribers.json")
TICK_PATH = os.path.join(os.getcwd(), "data", "tickers.json")