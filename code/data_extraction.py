import yfinance as yf
import pandas as pd
# openpyxl is implicitly used by pandas for .xlsx format, so importing it 
# just confirms its role but is not strictly necessary for this script to run.
import openpyxl 
import os

# 1. defining our ticker, period, interval, and file name (can be changed upon our needs)
TICKER = "GBPUSD=X"
DATA_PERIOD = "1mo"
DATA_INTERVAL = "30m"
FILE_NAME = "GBPUSD_1_Month_30M_Data.xlsx"

def extract_forex_data_to_excel():
    """
    Downloading OHLCV data for a specified Forex pair, removes the 
    Volume column, and saves it to a .xlsx file.
    """
    print(f"Downloading {DATA_PERIOD} of {DATA_INTERVAL} data for {TICKER}...")

    try:
        # 2. download the data
        data = yf.download(
            tickers=TICKER, 
            period=DATA_PERIOD, 
            interval=DATA_INTERVAL,
            progress=False # suppress progress bar for cleaner output
        )

        if data.empty:
            print(f"Warning: No data downloaded for {TICKER}. Check ticker, period, or interval.")
            return
        
        # 3. remove the Volume column
        if 'Volume' in data.columns:
            data = data.drop(columns=['Volume'])
            print("Volume column removed.")

        # 4. remove timezone information from the Datetime index

        if data.index.tz is not None:
             data.index = data.index.tz_localize(None)
             print("Timezone information successfully removed from the index.")

        # 5. save the data to Excel
        data.to_excel(FILE_NAME)
        
        print(f"\n Success! Data saved to {os.path.abspath(FILE_NAME)}")
        print(f"File contains {data.shape[0]} rows and {data.shape[1]} columns.")
        

    except Exception as e:
        print(f"\n An error occurred during download or saving: {e}")

if __name__ == '__main__':
    extract_forex_data_to_excel()