""" 
Purpose: Provide continuous and reactive output for the MT Cars dataset.

- Use inputs from the UI Sidebar to filter the dataset.
- Update reactive outputs in the UI Main Panel.

Matching the IDs in the UI Sidebar and function/output names in the UI Main Panel
to this server code is critical. They are case sensitive and must match exactly.

------------------------------------
Important Concept - Variable Scope
------------------------------------
In Python, the scope of a variable refers to where in the code that variable 
can be accessed and used. 

Variables defined outside of functions or blocks have global scope 
and can be used anywhere in the file. 

Variables defined inside a function or block have local scope 
and can only be used within that specific function or block.

------------------------------------
Important Concept - Reactivity
------------------------------
Reactive Effects only have "side effects" (they set reactive values, but don't return anything directly).
Reactive Calcs return a value (they can also set reactive values).
If a reactive.Effect depends on inputs, you must add them using the
reactive.event decorator (otherwise, the function won't be triggered).
"""

# Standard Library
from pathlib import Path

# External Libraries
import matplotlib.pyplot as plt
import pandas as pd
from plotnine import aes, geom_point, ggplot, ggtitle
import plotly.express as px
from shiny import render, reactive
from shinywidgets import render_widget

# Local Imports
from util_logger import setup_logger

# Set up a global logger for this file
logger, logname = setup_logger(__name__)

# Declare our file path variables globally so they can be used in all the functions (like logger)
csv_beaches = Path(__file__).parent.joinpath("data").joinpath("beaches.csv")


def get_beachday_server_functions(input, output, session):
    """Define functions to create UI outputs."""

    # First, declare shared reactive values (used between functions) up front
    # Initialize the values on startup

    reactive_location = reactive.Value("Bondi Beach, Australia")


    ###############################################################
    # CONTINUOUS LOCATION UPDATES (string, table, chart)
    ###############################################################

    @reactive.Effect
    @reactive.event(input.BEACH_LOCATION_SELECT)
    def _():
        """Set two reactive values (the location and temps df) when user changes location"""
        reactive_location.set(input.BEACH_LOCATION_SELECT())
        df = get_beaches_df()
        logger.info(f"init reactive_temp_df len: {len(df)}")

    @reactive.file_reader(str(csv_beaches))
    def get_beaches_df():
        logger.info(f"READING df from {csv_beaches}")
        df = pd.read_csv(csv_beaches)
        logger.info(f"READING df len {len(df)}")
        return df

    @reactive.file_reader(str(csv_beaches))
    def get_current_beaches_df():
        "Return a filtered dataframe that contains only the most recent record for every location"
        logger.info(f"READING df from {csv_beaches}")
        df = pd.read_csv(csv_beaches)
        
        # Convert 'Time' column to datetime
        df['Time'] = pd.to_datetime(df['Time'])
        
        # Sort DataFrame by 'Time'
        df.sort_values(by='Time', ascending=False, inplace=True)
        
        # Drop duplicates based on 'Location', keeping the first occurrence
        current_df = df.drop_duplicates(subset='Location', keep='first')
        
        return current_df

    ############ SUMMARY OF CURRENT WEATHER ###################################################

    @output
    @render.text
    def beach_weather_summary():
        "Return a string that contains a summary of current weather data for selected location"
        logger.info("beach_weather_summary starting")
        selected = reactive_location.get()
        df = get_current_beaches_df()

        selected_row = df[df['Location'] == selected]
        temperature = selected_row['Temp_F'].iloc[0]
        feels_like = selected_row['Feels_Like_Temp_F'].iloc[0]
        humidity = selected_row['Humidity'].iloc[0]
        wind_speed = selected_row['Wind_Speed'].iloc[0]
        cloud_cover = selected_row['Cloud Cover'].iloc[0]

        description = selected_row['Weather_Description'].iloc[0]
        description = description[0].upper() + description[1:]

        summary = f"""{selected}

{description}

• Current Temperature:  {temperature}°F
• Feels Like:           {feels_like}°F
• Humidity:             {humidity}%
• Wind Speed:           {wind_speed} mph
• Cloud Cover:          {cloud_cover}%
"""
        return summary


    ################## RECENT DATA FOR SELECTED BEACH #####

    @output
    @render.table
    def beach_table():
        df = get_beaches_df()
        # Filter the data based on the selected location
        df_location = df[df["Location"] == reactive_location.get()]
        logger.info(f"Rendering TEMP table with {len(df_location)} rows")
        return df_location



    ################# TEMP CHART ##########################

    @output
    @render.text
    def beach_temp_chart_string():
        """Return a string based on selected location."""
        logger.info("beach_string starting")
        selected = reactive_location.get()
        line1 = f"Recent Temperature in F for {selected}."
        line2 = "Updated once per minute for 15 minutes."
        line3 = "Keeps the most recent 10 minutes of data."
        message = f"{line1}\n{line2}\n{line3}"
        logger.info(f"{message}")
        return message

    @output
    @render_widget
    def beach_temp_chart():
        df = get_beaches_df()
        # Filter the data based on the selected location
        df_location = df[df["Location"] == reactive_location.get()]
        logger.info(f"Rendering TEMP chart with {len(df_location)} points")
        plotly_express_plot = px.line(
            df_location, x="Time", y="Temp_F", color="Location", markers=True
        )
        plotly_express_plot.update_layout(title="Continuous Temperature (F)")
        return plotly_express_plot

    ################# FEELS LIKE CHART ##########################

    @output
    @render.text
    def beach_feels_like_chart_string():
        """Return a string based on selected location."""
        logger.info("beach_string starting")
        selected = reactive_location.get()
        line1 = f'Recent "Feels Like" Temperature in F for {selected}.'
        line2 = "Updated once per minute for 15 minutes."
        line3 = "Keeps the most recent 10 minutes of data."
        message = f"{line1}\n{line2}\n{line3}"
        logger.info(f"{message}")
        return message

    @output
    @render_widget
    def beach_feels_like_chart():
        df = get_beaches_df()
        # Filter the data based on the selected location
        df_location = df[df["Location"] == reactive_location.get()]
        logger.info(f"Rendering Feels Like chart with {len(df_location)} points")
        plotly_express_plot = px.line(
            df_location, x="Time", y="Feels_Like_Temp_F", color="Location", markers=True
        )
        plotly_express_plot.update_layout(title="Continuous 'Feels Like' Temperature (F)")
        return plotly_express_plot
    
    ################# HUMIDITY CHART ##########################

    @output
    @render.text
    def beach_humidity_chart_string():
        """Return a string based on selected location."""
        logger.info("beach_string starting")
        selected = reactive_location.get()
        line1 = f'Recent Humidity % for {selected}.'
        line2 = "Updated once per minute for 15 minutes."
        line3 = "Keeps the most recent 10 minutes of data."
        message = f"{line1}\n{line2}\n{line3}"
        logger.info(f"{message}")
        return message

    @output
    @render_widget
    def beach_humidity_chart():
        df = get_beaches_df()
        # Filter the data based on the selected location
        df_location = df[df["Location"] == reactive_location.get()]
        logger.info(f"Rendering humidity chart with {len(df_location)} points")
        plotly_express_plot = px.line(
            df_location, x="Time", y="Humidity", color="Location", markers=True
        )
        plotly_express_plot.update_layout(title="Continuous Humidity %")
        return plotly_express_plot

    ################# WIND SPEED CHART ##########################

    @output
    @render.text
    def beach_wind_speed_chart_string():
        """Return a string based on selected location."""
        logger.info("beach_string starting")
        selected = reactive_location.get()
        line1 = f'Recent wind speed (mph) for {selected}.'
        line2 = "Updated once per minute for 15 minutes."
        line3 = "Keeps the most recent 10 minutes of data."
        message = f"{line1}\n{line2}\n{line3}"
        logger.info(f"{message}")
        return message

    @output
    @render_widget
    def beach_wind_speed_chart():
        df = get_beaches_df()
        # Filter the data based on the selected location
        df_location = df[df["Location"] == reactive_location.get()]
        logger.info(f"Rendering wind speed chart with {len(df_location)} points")
        plotly_express_plot = px.line(
            df_location, x="Time", y="Wind_Speed", color="Location", markers=True
        )
        plotly_express_plot.update_layout(title="Continuous Wind Speed (mph)")
        return plotly_express_plot
    
    ################# CLOUD COVER CHART ##########################

    @output
    @render.text
    def beach_cloud_cover_chart_string():
        """Return a string based on selected location."""
        logger.info("beach_string starting")
        selected = reactive_location.get()
        line1 = f'Recent cloud cover % for {selected}.'
        line2 = "Updated once per minute for 15 minutes."
        line3 = "Keeps the most recent 10 minutes of data."
        message = f"{line1}\n{line2}\n{line3}"
        logger.info(f"{message}")
        return message

    @output
    @render_widget
    def beach_cloud_cover_chart():
        df = get_beaches_df()
        # Filter the data based on the selected location
        df_location = df[df["Location"] == reactive_location.get()]
        logger.info(f"Rendering cloud cover % chart with {len(df_location)} points")
        plotly_express_plot = px.line(
            df_location, x="Time", y="Cloud Cover", color="Location", markers=True
        )
        plotly_express_plot.update_layout(title="Continuous Cloud Cover %")
        return plotly_express_plot
    
    ###############################################################

    # return a list of function names for use in reactive outputs

    return [
        beach_weather_summary,
        beach_temp_chart_string,
        beach_table,
        beach_temp_chart,
        beach_feels_like_chart_string,
        beach_feels_like_chart,
        beach_humidity_chart_string,
        beach_humidity_chart,
        beach_wind_speed_chart_string,
        beach_wind_speed_chart,
        beach_cloud_cover_chart_string,
        beach_cloud_cover_chart
    ]


"""
WorkFlow for Continuous and Interactive Apps

Step 1. Define the UI Inputs

1. Think: what can the user change?
2. Add new user inputs - define them in the ui_inputs.py file

Step 2. What continuous updates do you need? (Not UI driven)

These changes are not triggered by user input, but happen continuously
Write the functions needed and call them once to test them. 
Much of this work occurs outside the Shiny framework. 

For this example, we want to illustrate continuous updates
1. Using a function that returns a number (it can be anything)
2. Using web requests to the Open Weather API
3. Using web requests to the Yahoo Finance API

In this example, see these new files:
mtcars_constants.py - for basic functions outside Shiny
mtcars_get_temps.py - for continuous updates from the Open Weather API
mtcars_get_prices.py - for continuous updates from the Yahoo Finance API
These are all data-related - nothing to do with Shiny. 
Write and test these files separately. 

Step 3. Define the UI Outputs

1. Think: what does the user want to see?
2. For temperatures
    - We want a string to display the location and lat and long
    - We want a table to display the temperatures
    - We want a chart to display the temperatures

3. For company stock prices
    - We want a string to display the company and ticker
    - We want a table to display the prices
    - We want a chart to display the prices

4. Add these to the UI Outputs - define them in the ui_outputs.py file

Use the UI to verify each step. Get the input, lookup the lat/long, and show it in the output.
Show your tables first - this clarifies column names and data types.
Then you'll have what you need to make the charts work best.

Step 4. Define the Server Functions

1. Think: what do you need to do to create the outputs?
2. We wanted a reusable filtered df to drive the table and charts
3. Now, we need to add the continuous updates to the server function

2. Then, incorporate these inputs into the server function
3. Define reactive values - things you care about like the filtered df
   And the continuously updating dfs for temperatures and prices 
3. In the As you create outputs, add them to the return list
4. Add them to the output UI

IMPORTANT: All output functions must either depend on a input 
or a reactive value - either because the user changed something or because the reactive.invalidate_later() was called to update it continuously. 

"""
