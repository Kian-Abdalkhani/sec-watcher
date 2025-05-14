"""SEC API Integration"""
import requests as r
import pandas as pd

from app.config import HEADERS,SEC_CIK_URL,SEC_FILINGS_URL

def get_cik(ticker: str,lead_zeros: bool = True) -> str:
    """Returns CIK for the input ticker"""
    df_tickers = r.get(SEC_CIK_URL,headers=HEADERS).json()
    df_tickers = pd.DataFrame.from_dict(df_tickers, orient='index')
    df_filtered = df_tickers[df_tickers['ticker'] == ticker]
    if df_filtered.empty:
        return ""
    cik = str(df_filtered['cik_str'].iloc[0])
    if lead_zeros:
        if len(cik) < 10:
            leading_zeros = 10 - len(cik)
            for i in range(leading_zeros):
                cik = '0' + cik
    return cik

def get_filings(ticker: str,exclude_insider: bool = True) -> pd.DataFrame:
    cik = get_cik(ticker)
    # filings = r.get(SEC_FILINGS_URL.format(cik),headers=HEADERS).json()
    filings = r.get(SEC_FILINGS_URL.format(cik=cik),headers=HEADERS).json()
    filings = pd.DataFrame.from_dict(filings['filings']['recent'])

    #convert the two date fields into datetime objects
    filings['filingDate'] = pd.to_datetime(filings['filingDate'])
    filings['reportDate'] = pd.to_datetime(filings['reportDate'])

    if exclude_insider:
        insider_forms: list = ["3","3/A","4","4/A","5","5/A"]
        filings = filings[~filings["form"].isin(insider_forms)]

    return filings

def check_new_filings(cik: str ) -> bool:
    filings = get_filings(cik)
    if filings.empty:
        return False
    else:
        return True