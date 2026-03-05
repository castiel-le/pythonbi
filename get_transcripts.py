import os
import time
import random
import fitz  # PyMuPDF
from curl_cffi import requests

# --- CONFIGURATION ---
TICKERS = ["AAPL", "MSFT", "NVDA", "TSLA", "BA"]  # Add your tickers here
START_YEAR = 2023
END_YEAR = 2025  # Downloads up to and including this year
QUARTERS = [1, 2, 3, 4]

# Replace with your actual sessionid from browser DevTools
COOKIES = {"sessionid": "znrpopsjqpgun73fpojhatd3iyb78geq"} 

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

def pdf_to_text(pdf_content):
    """Extracts text from PDF bytes."""
    text = ""
    try:
        with fitz.open(stream=pdf_content, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        return f"Conversion Error: {e}"
    return text

def run_mass_download():
    base_dir = "transcripts"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    for ticker in TICKERS:
        # Create a specific folder for each company
        ticker_dir = os.path.join(base_dir, ticker)
        if not os.path.exists(ticker_dir):
            os.makedirs(ticker_dir)
            
        print(f"\n>>> Processing: {ticker}")

        # Loop through years from START_YEAR to END_YEAR
        for year in range(START_YEAR, END_YEAR + 1):
            for q in QUARTERS:
                file_name = f"{ticker}_{year}_Q{q}.txt"
                file_path = os.path.join(ticker_dir, file_name)

                # Skip if file already exists to save time
                if os.path.exists(file_path):
                    continue

                pdf_url = f"https://discountingcashflows.com/transcript/{ticker}/{year}/{q}/pdf/"
                
                try:
                    # Impersonate Chrome to bypass basic bot protection
                    response = requests.get(pdf_url, headers=HEADERS, cookies=COOKIES, impersonate="chrome120")
                    
                    if response.status_code == 200 and response.content.startswith(b'%PDF'):
                        text = pdf_to_text(response.content)
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(text)
                        print(f"  [✓] Saved: {file_name}")
                    elif response.status_code == 404:
                        # Some older years or future quarters might not exist
                        pass 
                    else:
                        print(f"  [!] Failed {year} Q{q}: Status {response.status_code}")

                    # Randomized sleep to avoid IP rate-limiting
                    time.sleep(random.uniform(4, 8))

                except Exception as e:
                    print(f"  [!] Error for {ticker} {year}: {e}")
                    time.sleep(10) # Longer wait if a connection error occurs

if __name__ == "__main__":
    run_mass_download()
    print("\nBatch process complete.")