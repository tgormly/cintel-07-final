"""
Purpose: Display output for MT Cars dataset.

@imports shiny.ui as ui
@imports shinywidgets.output_widget for interactive charts
"""
from shiny import ui
from shinywidgets import output_widget


def get_beachday_outputs():
    return ui.panel_main(
        ui.tags.section(
            ui.h3("Current Weather:"),
            ui.output_text_verbatim("beach_weather_summary"),
            ui.tags.br(),

            ui.h4("Recent weather data for your selected beach"),
            ui.output_ui("beach_table"),
            ui.tags.br(),

            ui.output_text("beach_temp_chart_string"),
            output_widget("beach_temp_chart"),
            ui.tags.hr(),

            ui.output_text("beach_feels_like_chart_string"),
            output_widget("beach_feels_like_chart"),
            ui.tags.hr(),

            ui.output_text("beach_humidity_chart_string"),
            output_widget("beach_humidity_chart"),
            ui.tags.hr(),

            ui.output_text("beach_wind_speed_chart_string"),
            output_widget("beach_wind_speed_chart"),
            ui.tags.hr(),

            ui.output_text("beach_cloud_cover_chart_string"),
            output_widget("beach_cloud_cover_chart"),
            ui.tags.hr(),        

        ),
        ui.p("Real-time weather data courtesy of Openweathermap's API")
    )
