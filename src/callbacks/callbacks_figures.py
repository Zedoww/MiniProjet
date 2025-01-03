from dash.dependencies import Input, Output
from ..utils.data_loader import load_cleaned_data
from ..utils.figures import create_temperature_figure, create_precipitation_bar, create_map_figure
from ..layout.themes import light_theme, dark_theme
import pandas as pd
from datetime import date


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
            Input('date-range-slider', 'value'),
            Input('city-dropdown', 'value'),
            Input('current-theme', 'data'),
            Input('map-metric', 'value'),
            Input('geo-level', 'value')
        ]
    )
    def update_dashboard(date_range, selected_city, theme_value, map_metric, geo_level=None):
        # Définir une valeur par défaut pour geo_level si elle est manquante
        if geo_level is None:
            geo_level = "region"

        # Convertir les valeurs ordinales du RangeSlider en dates
        start_date = date.fromordinal(date_range[0])
        end_date = date.fromordinal(date_range[1])

        # Filtrage par ville
        city_data = data.loc[data['communes (name)'] == selected_city].copy()

        # Remplir les valeurs manquantes
        city_data['Température maximale sur 24 heures'] = city_data['Température maximale sur 24 heures'].fillna(city_data['Température'])
        city_data['Température minimale sur 24 heures'] = city_data['Température minimale sur 24 heures'].fillna(city_data['Température'])
        city_data['Précipitations dans les 24 dernières heures'] = city_data['Précipitations dans les 24 dernières heures'].fillna(0)

        # Regroupement par date avec agrégations spécifiques
        city_data_daily = city_data.groupby(city_data['Date'].dt.date).agg({
            'Température maximale sur 24 heures': 'max',
            'Température minimale sur 24 heures': 'min',
            'Précipitations dans les 24 dernières heures': 'mean'  # Moyenne des précipitations
        }).reset_index()

        # Filtrer les données par plage de dates
        filtered_data = city_data_daily[(city_data_daily['Date'] >= start_date) & (city_data_daily['Date'] <= end_date)]

        if filtered_data.empty:
            return "N/A", "N/A", "N/A", "N/A", {}, {}, {}

        # Calcul des valeurs
        max_temp = round(filtered_data['Température maximale sur 24 heures'].max() - 273.15, 1)
        min_temp = round(filtered_data['Température minimale sur 24 heures'].min() - 273.15, 1)
        total_precipitation = round(filtered_data['Précipitations dans les 24 dernières heures'].sum(), 1)
        precipitation_days = len(filtered_data[filtered_data['Précipitations dans les 24 dernières heures'] > 0])

        # Définir le thème
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