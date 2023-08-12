"""
Purpose: Provide user interaction options for MT Cars dataset.

IDs must be unique. They are capitalized in this app for clarity (not typical).
The IDs are case-sensitive and must match the server code exactly.
Preface IDs with the dataset name to avoid naming conflicts.

"""
from shiny import ui
from random import randint

# Define the UI inputs and include our new selection options

def get_beachday_inputs():
    return ui.panel_sidebar(
        ui.h3("Select a beach from the dropdown below:"),
        ui.tags.br(),
        ui.input_select(
            id="BEACH_LOCATION_SELECT",
            label='',
            choices=[
                    "Bondi Beach, Australia",
                    "Copacabana Beach, Brazil",
                    "Waikiki Beach, Hawaii, USA",
                    "Malibu Beach, California, USA",
                    "Bora Bora Beach, French Polynesia",
                    "Anse Source d'Argent, Seychelles",
                    "Railay Beach, Thailand",
                    "Navagio Beach (Shipwreck Beach), Greece",
                    "Whitehaven Beach, Australia",
                    "Matira Beach, Bora Bora, French Polynesia"
                ],
            selected = "Bondi Beach, Australia",
        ),
        ui.tags.hr(),
        ui.h3("What data would you like to see?"),
        ui.input_switch(
            id="TEMP_SWITCH",
            label="Temperature",
            value=True
        ),
        ui.input_switch(
            id="FEELS_LIKE_SWITCH",
            label="Feels Like Temperature",
            value=True
        ),
        ui.input_switch(
            id="HUMIDITY_SWITCH",
            label="Humidity",
            value=True
        ),
        ui.input_switch(
            id="WIND_SPEED_SWITCH",
            label="Wind Speed",
            value=True
        ),
        ui.input_switch(
            id="CLOUD_COVER_SWITCH",
            label="Cloud Cover",
            value=True
        ),                        

        ui.tags.p("(Unfortunately, I was unable to actually get this to toggle the charts in my outputs on and off before the deadline"),

        ui.hr(),
        ui.p("🕒 Please be patient. Outputs may take a few seconds to load."),
        ui.tags.hr(),
    )
