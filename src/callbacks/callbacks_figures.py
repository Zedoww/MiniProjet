from dash.dependencies import Input, Output
from ..utils.data_loader import load_cleaned_data
from ..utils.figures import create_temperature_figure, create_precipitation_bar, create_map_figure
from ..layout.themes import light_theme, dark_theme
import pandas as pd
from dateutil.parser import parse

def register_figures_callbacks(app, data, france_regions_geojson, france_departements_geojson):

    @app.callback(
        [
            Output('max-temp-24h', 'children'),
            Output('min-temp-24h', 'children'),
            Output('total-precipitation', 'children'),
            Output('precipitation-days', 'children'),
            Output('temp-graph', 'figure'),
            Output('precipitation-bar', 'figure'),
            Output('map-graph', 'figure')
        ],
        [
            Input('date-picker-range', 'start_date'),
            Input('date-picker-range', 'end_date'),
            Input('city-dropdown', 'value'),
            Input('current-theme', 'data'),
            Input('map-metric', 'value'),
            Input('geo-level', 'value')
        ]
    )
    def update_dashboard(start_date, end_date, selected_city, theme_value, map_metric, geo_level):
        start_date = parse(start_date).date()
        end_date = parse(end_date).date()

        # Filtrage par ville
        city_data = data.loc[data['communes (name)'] == selected_city].copy()

        city_data['Température maximale sur 24 heures'] = city_data['Température maximale sur 24 heures'].fillna(city_data['Température'])
        city_data['Température minimale sur 24 heures'] = city_data['Température minimale sur 24 heures'].fillna(city_data['Température'])

        city_data_daily = city_data.groupby(city_data['Date'].dt.date).mean(numeric_only=True).reset_index()
        filtered_data = city_data_daily[(city_data_daily['Date'] >= start_date) & (city_data_daily['Date'] <= end_date)]

        if filtered_data.empty:
            return "N/A", "N/A", "N/A", "N/A", {}, {}, {}

        max_temp = round(filtered_data['Température maximale sur 24 heures'].max() - 273.15, 1)
        min_temp = round(filtered_data['Température minimale sur 24 heures'].min() - 273.15, 1)
        total_precipitation = round(filtered_data['Précipitations dans les 24 dernières heures'].fillna(0).sum(), 1)
        precipitation_days = len(filtered_data[filtered_data['Précipitations dans les 24 dernières heures'].fillna(0) > 0])

        theme = dark_theme if theme_value == 'dark' else light_theme

        # Graphiques
        temp_fig = create_temperature_figure(filtered_data, theme)
        precipitation_fig = create_precipitation_bar(filtered_data, theme)

        # Données globales pour la carte
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
            map_fig
        )
