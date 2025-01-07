from dash.dependencies import Input, Output, State
from dash import callback_context
from datetime import date
import pandas as pd
from ..utils.figures import (
    create_temperature_figure,
    create_precipitation_bar,
    create_map_figure,
    create_temperature_histogram
)
from ..layout.themes import light_theme, dark_theme

def register_fullscreen_callbacks(app):
    @app.callback(
        [
            Output('temp-graph', 'className'),
            Output('precipitation-bar', 'className'),
            Output('map-graph', 'className'),
            Output('temp-histogram', 'className'),
            Output('fullscreen-temp-graph-btn', 'style'),
            Output('exit-fullscreen-temp-graph-btn', 'style'),
            Output('fullscreen-precipitation-bar-btn', 'style'),
            Output('exit-fullscreen-precipitation-bar-btn', 'style'),
            Output('fullscreen-map-graph-btn', 'style'),
            Output('exit-fullscreen-map-graph-btn', 'style'),
            Output('fullscreen-histogram-btn', 'style'),
            Output('exit-fullscreen-histogram-btn', 'style'),
            Output('temp-graph', 'style'),
            Output('precipitation-bar', 'style'),
            Output('map-graph', 'style'),
            Output('temp-histogram', 'style')
        ],
        [
            Input('fullscreen-temp-graph-btn', 'n_clicks'),
            Input('exit-fullscreen-temp-graph-btn', 'n_clicks'),
            Input('fullscreen-precipitation-bar-btn', 'n_clicks'),
            Input('exit-fullscreen-precipitation-bar-btn', 'n_clicks'),
            Input('fullscreen-map-graph-btn', 'n_clicks'),
            Input('exit-fullscreen-map-graph-btn', 'n_clicks'),
            Input('fullscreen-histogram-btn', 'n_clicks'),
            Input('exit-fullscreen-histogram-btn', 'n_clicks'),
        ],
        prevent_initial_call=True
    )
    def toggle_fullscreen(
        temp_enter, temp_exit,
        precip_enter, precip_exit,
        map_enter, map_exit,
        hist_enter, hist_exit
    ):
        ctx = callback_context
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None

        # Réinitialiser les classes et styles
        temp_class = 'fullscreenable'
        precip_class = 'fullscreenable'
        map_class = 'fullscreenable'
        hist_class = 'fullscreenable'

        temp_style = {}
        precip_style = {}
        map_style = {}
        hist_style = {}

        temp_btn_style = precip_btn_style = map_btn_style = hist_btn_style = {'display': 'block'}
        temp_exit_style = precip_exit_style = map_exit_style = hist_exit_style = {'display': 'none'}

        if triggered_id == 'fullscreen-temp-graph-btn':
            temp_class += ' fullscreen'
            temp_btn_style = {'display': 'none'}
            temp_exit_style = {'display': 'block'}

            precip_btn_style = map_btn_style = hist_btn_style = {'display': 'none'}

            temp_style = {'height': '100vh', 'width': '100vw'}

        elif triggered_id == 'exit-fullscreen-temp-graph-btn':
            temp_class = 'fullscreenable'
            temp_style = {'height': '', 'width': ''}

        elif triggered_id == 'fullscreen-precipitation-bar-btn':
            precip_class += ' fullscreen'
            precip_btn_style = {'display': 'none'}
            precip_exit_style = {'display': 'block'}

            temp_btn_style = map_btn_style = hist_btn_style = {'display': 'none'}

            precip_style = {'height': '100vh', 'width': '100vw'}

        elif triggered_id == 'exit-fullscreen-precipitation-bar-btn':
            precip_class = 'fullscreenable'
            precip_style = {'height': '', 'width': ''}

        elif triggered_id == 'fullscreen-map-graph-btn':
            map_class += ' fullscreen'
            map_btn_style = {'display': 'none'}
            map_exit_style = {'display': 'block'}

            temp_btn_style = precip_btn_style = hist_btn_style = {'display': 'none'}

            map_style = {'height': '100vh', 'width': '100vw'}

        elif triggered_id == 'exit-fullscreen-map-graph-btn':
            map_class = 'fullscreenable'
            map_style = {'height': '', 'width': ''}

        elif triggered_id == 'fullscreen-histogram-btn':
            hist_class += ' fullscreen'
            hist_btn_style = {'display': 'none'}
            hist_exit_style = {'display': 'block'}

            temp_btn_style = precip_btn_style = map_btn_style = {'display': 'none'}

            hist_style = {'height': '100vh', 'width': '100vw'}

        elif triggered_id == 'exit-fullscreen-histogram-btn':
            hist_class = 'fullscreenable'
            hist_style = {'height': '', 'width': ''}

        return (
            temp_class, precip_class, map_class, hist_class,
            temp_btn_style, temp_exit_style,
            precip_btn_style, precip_exit_style,
            map_btn_style, map_exit_style,
            hist_btn_style, hist_exit_style,
            temp_style, precip_style, map_style, hist_style
        )

def register_figures_callbacks(app, data, france_regions_geojson, france_departements_geojson):
    @app.callback(
        [
            Output('max-temp-24h', 'children'),
            Output('min-temp-24h', 'children'),
            Output('total-precipitation', 'children'),
            Output('precipitation-days', 'children'),
            Output('temp-graph', 'figure'),
            Output('precipitation-bar', 'figure'),
            Output('map-graph', 'figure'),
            Output('temp-histogram', 'figure')
        ],
        [
            Input('date-range-slider', 'value'),
            Input('city-dropdown', 'value'),
            Input('current-theme', 'data'),
            Input('map-metric', 'value'),
            Input('geo-level', 'value')
        ]
    )
    def update_dashboard(date_range, selected_city, theme_value, map_metric, geo_level=None):
        if geo_level is None:
            geo_level = "region"

        start_date = date.fromordinal(date_range[0])
        end_date = date.fromordinal(date_range[1])

        city_data = data.loc[data['communes (name)'] == selected_city].copy()

        city_data['Température maximale sur 24 heures'] = city_data['Température maximale sur 24 heures'].fillna(city_data['Température'])
        city_data['Température minimale sur 24 heures'] = city_data['Température minimale sur 24 heures'].fillna(city_data['Température'])
        city_data['Précipitations dans les 24 dernières heures'] = city_data['Précipitations dans les 24 dernières heures'].fillna(0)

        city_data_daily = city_data.groupby(city_data['Date'].dt.date).agg({
            'Température maximale sur 24 heures': 'max',
            'Température minimale sur 24 heures': 'min',
            'Précipitations dans les 24 dernières heures': 'mean'
        }).reset_index()

        filtered_data = city_data_daily[(city_data_daily['Date'] >= start_date) & (city_data_daily['Date'] <= end_date)]

        if filtered_data.empty:
            return "N/A", "N/A", "N/A", "N/A", {}, {}, {}, {}

        max_temp = round(filtered_data['Température maximale sur 24 heures'].max() - 273.15, 1)
        min_temp = round(filtered_data['Température minimale sur 24 heures'].min() - 273.15, 1)
        total_precipitation = round(filtered_data['Précipitations dans les 24 dernières heures'].sum(), 1)
        precipitation_days = len(filtered_data[filtered_data['Précipitations dans les 24 dernières heures'] > 0])

        theme = dark_theme if theme_value == 'dark' else light_theme

        temp_fig = create_temperature_figure(filtered_data, theme)
        precipitation_fig = create_precipitation_bar(filtered_data, theme)
        histogram_fig = create_temperature_histogram(filtered_data, theme)

        global_filtered_data = data[(data['Date'].dt.date >= start_date) & (data['Date'].dt.date <= end_date)]

        if geo_level == 'region':
            agg_col = 'region (code)'
            geojson = france_regions_geojson
            feature_id_key = 'properties.code'
        else:
            agg_col = 'department (code)'
            geojson = france_departements_geojson
            feature_id_key = 'properties.code'

        region_or_dept_data = global_filtered_data.groupby(agg_col, as_index=False).agg({
            'Température': 'mean',
            'Précipitations dans les 24 dernières heures': 'mean'
        })

        map_fig = create_map_figure(region_or_dept_data, geojson, map_metric, theme, feature_id_key)

        return (
            f"{max_temp}°C",
            f"{min_temp}°C",
            f"{total_precipitation} mm",
            f"{precipitation_days}",
            temp_fig,
            precipitation_fig,
            map_fig,
            histogram_fig  # Retourner l'histogramme
        )