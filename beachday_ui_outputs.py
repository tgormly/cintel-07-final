"""
Purpose: Display output for MT Cars dataset.

@imports shiny.ui as ui
@imports shinywidgets.output_widget for interactive charts
"""
from shiny import ui
from shinywidgets import output_widget


def get_beachday_outputs():
    return ui.panel_main(
        ui.h2("Outputs"),
        ui.p("Real-time weather data courtesy of Openweathermap's API"),
        ui.tags.hr(),
        ui.tags.section(
            ui.h3("Continuous Updates (Weather API)"),
            ui.tags.br(),
            ui.output_text("beach_string"),
            ui.tags.br(),
            ui.output_ui("beach_table"),
            ui.tags.br(),
            output_widget("beach_chart"),
            ui.tags.br(),
            ui.tags.hr(),
        ),
    )
