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
        ui.h2("Beach Day Inputs"),
        ui.tags.hr(),
        
        ui.input_select(
            id="BEACH_LOCATION_SELECT",
            label="Choose a beach",
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
        ui.p("🕒 Please be patient. Outputs may take a few seconds to load."),
        ui.tags.hr(),
    )
