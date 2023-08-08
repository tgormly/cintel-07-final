"""
Tim Gormly
7/29/2023

Purpose: Illustrate addition of continuous information from the Yahoo. 

This is a simple example that uses a deque to store the last 15 minutes of
temperature readings for three locations.

The data is updated every minute.

Continuous information might also come from a database, a data lake, a data warehouse, or a cloud service.

----------------------------
Open API Weather Information
-----------------------------

Go to: https://openweathermap.org/

And sign up for your own free account and API key. 

The key should be kept secret - do not share it with others.
Open Weather API allows 1000 free requests per day.
That's about 125 per working hour, so comment it out when first testing. 

After everything works, and you have your own API key, uncomment it and use the real information.

-----------------------
Keeping Secrets Secret
-----------------------

Keep secrets in a .env file - load it, read the values.
Add the .env file to your .gitignore so you don't publish it to GitHub.
We usually include a .env-example file to illustrate the format.

"""


# Standard Library
import asyncio
from datetime import datetime
from pathlib import Path
import os
from random import randint

# External Packages
import pandas as pd
from collections import deque
from dotenv import load_dotenv

# Local Imports
from fetch import fetch_from_url
from util_logger import setup_logger

# Set up a file logger
logger, log_filename = setup_logger(__file__)

# unsure if this is needed - the yahoo finance querying method we are using does not seem to require an API key
"""
def get_API_key():
    # Keep secrets in a .env file - load it, read the values.
    # Load environment variables from .env file
    load_dotenv()
    key = os.getenv("OPEN_WEATHER_API_KEY")
    return key
"""

def lookup_ticker(company):
    """Return the ticker for a given company."""
    company_dictionary = {
        "Duolingo": "DUOL",
        "The Vita Coco Company": "COCO",
        "Cricut": "CRCT",
        "Allbirds": "BIRD",
    }
    ticker = company_dictionary[company]
    return ticker


async def get_stock_price(ticker):
    """Receives a company's stock symbol/ticker, queries yahoo stock api with 
    this ticker, and returns the current regular market price of this stock"""
    # logger stores record that function has been called and with which ticker
    logger.info("Querying yahoo finance for {ticker}")

    # the query URL is created and stored in the stock_api_url variable based
    # on the ticker provided by the user
    stock_api_url = f"https://query1.finance.yahoo.com/v7/finance/options/{ticker}"

    # logger stores record that the async function fetch_from_url is being called
    logger.info(f"Calling fetch_from_url for {stock_api_url}")
    result = await fetch_from_url(stock_api_url, "json")
    
    logger.info(f"Data for {ticker}: {result}")
    price = result.data["optionChain"]["result"][0]["quote"]["regularMarketPrice"]

    # placeholder code to test functionality without making API calls
    # price = randint(25, 150)

    return price




# Function to create or overwrite the CSV file with column headings
def init_csv_file(file_path):
    df_empty = pd.DataFrame(
        columns=["Company", "Ticker", "RegularMarketPrice", "Time"]
    )
    df_empty.to_csv(file_path, index=False)


async def update_csv_stock():
    """Update the CSV file with the latest stock information."""
    logger.info("Calling update_csv_stock")
    try:
        companies = ["Duolingo", "The Vita Coco Company", "Cricut", "Allbirds"]
        update_interval = 60  # Update every 1 minute (60 seconds)
        total_runtime = 15 * 60  # Total runtime maximum of 15 minutes
        num_updates = 10 * len(companies) # Keep the most recent 10 readings
        logger.info(f"update_interval: {update_interval}")
        logger.info(f"total_runtime: {total_runtime}")
        logger.info(f"num_updates: {num_updates}")

        # Use a deque to store just the last, most recent 10 readings in order
        records_deque = deque(maxlen=num_updates)

        fp = Path(__file__).parent.joinpath("data").joinpath("mtcars_stock.csv")

        # Check if the file exists, if not, create it with only the column headings
        if not os.path.exists(fp):
            init_csv_file(fp)

        logger.info(f"Initialized csv file at {fp}")

        for _ in range(num_updates):  # To get num_updates readings
            for company in companies:
                ticker = lookup_ticker(company)
                new_price = await get_stock_price(ticker)
                time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current time
                new_record = {
                    "Company": company,
                    "Ticker": ticker,
                    "RegularMarketPrice": new_price,
                    "Time": time_now,
                }
                records_deque.append(new_record)

            # Use the deque to make a DataFrame
            df = pd.DataFrame(records_deque)

            # Save the DataFrame to the CSV file, deleting its contents before writing
            df.to_csv(fp, index=False, mode="w")
            logger.info(f"Saving stock prices to {fp}")

            # Wait for update_interval seconds before the next reading
            await asyncio.sleep(update_interval)

    except Exception as e:
        logger.error(f"ERROR in update_csv_stock: {e}")
