"""
Purpose: Display output for MT Cars dataset.

@imports shiny.ui as ui
@imports shinywidgets.output_widget for interactive charts
"""
from shiny import ui
from shinywidgets import output_widget


def get_beachday_outputs():
    return ui.panel_main(
        ui.h2("Main Panel with Continuous and Reactive Output"),
        ui.tags.hr(),
        ui.tags.section(
            ui.h3("Continuous Updates (Weather API)"),
            ui.tags.br(),
            ui.output_text("mtcars_location_string"),
            ui.tags.br(),
            ui.output_ui("mtcars_location_table"),
            ui.tags.br(),
            output_widget("mtcars_location_chart"),
            ui.tags.br(),
            ui.tags.hr(),
        ),
    )
