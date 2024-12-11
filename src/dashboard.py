import pandas as pd
from datetime import datetime
from dateutil.parser import parse
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Charger les données nettoyées
cleaned_data_path = "data/cleaned/cleaneddata.csv"
data = pd.read_csv(cleaned_data_path)

# Forcer la conversion en datetime
data['Date'] = pd.to_datetime(data['Date'], errors='coerce', utc=True)

# Supprimer les lignes avec des dates invalides
data = data.dropna(subset=['Date'])

# Obtenir la plage de dates
min_date = data['Date'].min().date()
max_date = data['Date'].max().date()

# Grouper les données par jour pour simplifier les graphiques
data_daily = data.groupby(data['Date'].dt.date).mean(numeric_only=True).reset_index()

# Renommer la colonne "Date" pour éviter les conflits
data_daily = data_daily.rename(columns={'index': 'Date'})

# Créer l'application Dash
app = dash.Dash(__name__)
app.title = "Historique Météo en France"

# Mise en page
app.layout = html.Div([
    html.H1("Historique Météo en France", style={'textAlign': 'center', 'marginBottom': '20px'}),
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=min_date,
        end_date=max_date,
        min_date_allowed=min_date,
        max_date_allowed=max_date,
        display_format='YYYY-MM-DD',
        initial_visible_month=min_date,
        style={'marginBottom': '30px', 'width': '100%', 'display':'flex', 'justify-content': 'center'}
),
dcc.Dropdown(
    id='city-dropdown',
    options=[{'label': city, 'value': city} for city in data['communes (name)'].unique()],
    value=data['communes (name)'].unique()[0],  # Ville par défaut
    style={'marginBottom': '30px'}
),
    html.Div([
        html.Div([
            html.H3("Max Temp", style={'textAlign': 'center'}),
            html.P(id='max-temp-24h', style={'fontSize': '24px', 'textAlign': 'center'}),
        ], className="kpi", style={'flex': '1', 'margin': '0 10px'}),
        html.Div([
            html.H3("Min Temp", style={'textAlign': 'center'}),
            html.P(id='min-temp-24h', style={'fontSize': '24px', 'textAlign': 'center'}),
        ], className="kpi", style={'flex': '1', 'margin': '0 10px'}),
        html.Div([
            html.H3("Total Precipitation", style={'textAlign': 'center'}),
            html.P(id='total-precipitation', style={'fontSize': '24px', 'textAlign': 'center'}),
        ], className="kpi", style={'flex': '1', 'margin': '0 10px'}),
        html.Div([
            html.H3("Avg Wind Speed", style={'textAlign': 'center'}),
            html.P(id='avg-wind-speed', style={'fontSize': '24px', 'textAlign': 'center'}),
        ], className="kpi", style={'flex': '1', 'margin': '0 10px'}),
    ], style={'display': 'flex', 'justifyContent': 'center', 'marginBottom': '30px'}),
    dcc.Graph(id='temp-graph', style={'marginBottom': '30px'}),
    dcc.Graph(id='precipitation-bar', style={'marginBottom': '30px'})
])

# Callbacks pour l'interactivité
@app.callback(
    [
        Output('max-temp-24h', 'children'),
        Output('min-temp-24h', 'children'),
        Output('total-precipitation', 'children'),
        Output('avg-wind-speed', 'children'),
        Output('temp-graph', 'figure'),
        Output('precipitation-bar', 'figure')
    ],
    [
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date'),
        Input('city-dropdown', 'value')  # Nouvelle entrée pour la ville
    ]
)
def update_dashboard(start_date, end_date, selected_city):
    # Convertir les dates en objets datetime
    start_date = parse(start_date).date()
    end_date = parse(end_date).date()

    # Filtrer les données pour la ville sélectionnée
    city_data = data[data['communes (name)'] == selected_city]

    # Utiliser la colonne Température comme base si les données 24h sont manquantes
    city_data['Température maximale sur 24 heures'] = city_data['Température maximale sur 24 heures'].fillna(city_data['Température'])
    city_data['Température minimale sur 24 heures'] = city_data['Température minimale sur 24 heures'].fillna(city_data['Température'])

    # Regrouper les données par jour
    city_data['Date'] = pd.to_datetime(city_data['Date'])
    city_data_daily = city_data.groupby(city_data['Date'].dt.date).mean(numeric_only=True).reset_index()

    # Filtrer les données pour la plage de dates sélectionnée
    filtered_data = city_data_daily[(city_data_daily['Date'] >= start_date) & (city_data_daily['Date'] <= end_date)]

    if filtered_data.empty:
        return "Données indisponibles", "Données indisponibles", "Données indisponibles", "Données indisponibles", {}, {}

    # Calcul des KPI
    max_temp = round(filtered_data['Température maximale sur 24 heures'].max() - 273.15, 1)
    min_temp = round(filtered_data['Température minimale sur 24 heures'].min() - 273.15, 1)
    total_precipitation = round(filtered_data['Précipitations dans les 24 dernières heures'].sum(), 1) if 'Précipitations dans les 24 dernières heures' in filtered_data else "Données indisponibles"
    avg_wind_speed = round(filtered_data['Vitesse du vent moyen 10 mn'].mean(), 1) if 'Vitesse du vent moyen 10 mn' in filtered_data else "Données indisponibles"

    # Créer les graphiques
    temp_fig = {
        'data': [
            {'x': filtered_data['Date'], 'y': filtered_data['Température maximale sur 24 heures'], 'type': 'line', 'name': 'Max Temp'},
            {'x': filtered_data['Date'], 'y': filtered_data['Température minimale sur 24 heures'], 'type': 'line', 'name': 'Min Temp'}
        ],
        'layout': {
            'title': 'Températures au fil du temps',
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Température (°C)'}
        }
    }

    precipitation_fig = {
        'data': [
            {'x': filtered_data['Date'], 'y': filtered_data['Précipitations dans les 24 dernières heures'].cumsum(), 'type': 'line', 'name': 'Précipitations cumulées'}
        ],
        'layout': {
            'title': 'Précipitations cumulées au fil du temps',
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Précipitations (mm)'}
        }
    }

    # Retourner les KPI et les graphiques
    return (
        f"{max_temp}°C",
        f"{min_temp}°C",
        f"{total_precipitation} mm",
        f"{avg_wind_speed} km/h",
        temp_fig,
        precipitation_fig
    )