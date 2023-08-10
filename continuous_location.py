"""
Use Open Weather Map API to find and store the temperature for 10 popular beach destinations around the wrold
----------------------------
Open API Weather Information
-----------------------------
Go to: https://openweathermap.org/
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


def get_API_key():
    # Keep secrets in a .env file - load it, read the values.
    # Load environment variables from .env file
    load_dotenv()
    key = os.getenv("OPEN_WEATHER_API_KEY")
    return key


def lookup_lat_long(location):
    """Return the latitude and longitude for the given location."""
    # Master dictionary of locations. Each key is a location, and each value is
    # a dictionary itself with a "latitude" and "longitude" key, and actual numeric value for each key as the value
    beach_dictionary = {
    "Bondi Beach, Australia": {"latitude": -33.8917, "longitude": 151.2745},
    "Copacabana Beach, Brazil": {"latitude": -22.9714, "longitude": -43.1828},
    "Waikiki Beach, Hawaii, USA": {"latitude": 21.2765, "longitude": -157.8272},
    "Malibu Beach, California, USA": {"latitude": 34.0259, "longitude": -118.7798},
    "Bora Bora Beach, French Polynesia": {"latitude": -16.5004, "longitude": -151.7415},
    "Anse Source d'Argent, Seychelles": {"latitude": -4.3608, "longitude": 55.8305},
    "Railay Beach, Thailand": {"latitude": 8.0119, "longitude": 98.8365},
    "Navagio Beach (Shipwreck Beach), Greece": {"latitude": 37.8515, "longitude": 20.6248},
    "Whitehaven Beach, Australia": {"latitude": -20.2825, "longitude": 149.0393},
    "Matira Beach, Bora Bora, French Polynesia": {"latitude": -16.5015, "longitude": -151.7414}
    }

    # this sets the location dictionary returned by the function, based on the location that was passed into this
    # function
    answer_dict = beach_dictionary[location]
    lat = answer_dict["latitude"] # assigns value of latitude key into lat variable
    long = answer_dict["longitude"] # assigns value of longitude key into long variable
    return lat, long


async def get_temperature_from_openweathermap(lat, long):
    logger.info("Calling get_temperature_from_openweathermap for {lat}, {long}}")
    api_key = get_API_key()
    open_weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={api_key}&units=imperial"
    logger.info(f"Calling fetch_from_url for {open_weather_url}")
    # result = await fetch_from_url(open_weather_url, "json")
    # logger.info(f"Data from openweathermap: {result}")
    # temp_F = result.data["main"]["temp"]
    temp_F = randint(68, 77)
    return temp_F


# Function to create or overwrite the CSV file with column headings
def init_csv_file(file_path):
    df_empty = pd.DataFrame(
        columns=["Location", "Latitude", "Longitude", "Time", "Temp_F"]
    )
    df_empty.to_csv(file_path, index=False)


async def update_csv_beach():
    """Update the CSV file with the latest location information."""
    logger.info("Calling update_csv_location")
    try:
        locations = [   "Bondi Beach, Australia",
                        "Copacabana Beach, Brazil",
                        "Waikiki Beach, Hawaii, USA",
                        "Malibu Beach, California, USA",
                        "Bora Bora Beach, French Polynesia",
                        "Anse Source d'Argent, Seychelles",
                        "Railay Beach, Thailand",
                        "Navagio Beach (Shipwreck Beach), Greece",
                        "Whitehaven Beach, Australia",
                        "Matira Beach, Bora Bora, French Polynesia"]
        update_interval = 60  # Update every 1 minute (60 seconds)
        total_runtime = 15 * 60  # Total runtime maximum of 15 minutes
        num_updates = 10 * len(locations) # Keep the most recent 10 readings
        logger.info(f"update_interval: {update_interval}")
        logger.info(f"total_runtime: {total_runtime}")
        logger.info(f"num_updates: {num_updates}")

        # Use a deque to store just the last, most recent 10 readings in order
        records_deque = deque(maxlen=num_updates)

        fp = Path(__file__).parent.joinpath("data").joinpath("mtcars_location.csv")

        # Check if the file exists, if not, create it with only the column headings
        if not os.path.exists(fp):
            init_csv_file(fp)

        logger.info(f"Initialized csv file at {fp}")

        for _ in range(num_updates):  # To get num_updates readings
            for location in locations:
                lat, long = lookup_lat_long(location)
                new_temp = await get_temperature_from_openweathermap(lat, long)
                time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current time
                new_record = {
                    "Location": location,
                    "Latitude": lat,
                    "Longitude": long,
                    "Time": time_now,
                    "Temp_F": new_temp,
                }
                records_deque.append(new_record)

            # Use the deque to make a DataFrame
            df = pd.DataFrame(records_deque)

            # Save the DataFrame to the CSV file, deleting its contents before writing
            df.to_csv(fp, index=False, mode="w")
            logger.info(f"Saving temperatures to {fp}")

            # Wait for update_interval seconds before the next reading
            await asyncio.sleep(update_interval)

    except Exception as e:
        logger.error(f"ERROR in update_csv_location: {e}")
