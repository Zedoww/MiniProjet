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
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_dashboard(start_date, end_date):
    # Convertir start_date et end_date en datetime.date avec parse
    start_date = parse(start_date).date()
    end_date = parse(end_date).date()

    # Filtrer les données
    filtered_data = data_daily[(data_daily['Date'] >= start_date) & (data_daily['Date'] <= end_date)]
    
    # Calculer les KPI
    max_temp = round(filtered_data['Température maximale sur 24 heures'].max()-273, 1)
    min_temp = round(filtered_data['Température minimale sur 24 heures'].min()-273, 1)
    total_precipitation = round(filtered_data['Précipitations dans les 24 dernières heures'].sum(), 1)
    avg_wind_speed = round(filtered_data['Vitesse du vent moyen 10 mn'].mean(), 1)
    
    # Créer les graphiques
    temp_fig = {
        'data': [
            {'x': filtered_data['Date'], 'y': filtered_data['Température maximale sur 24 heures'], 'type': 'line', 'name': 'Max Temp'},
            {'x': filtered_data['Date'], 'y': filtered_data['Température minimale sur 24 heures'], 'type': 'line', 'name': 'Min Temp'}
        ],
        'layout': {
            'title': 'Temperature Over Time',
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Temperature (°C)'}
        }
    }
    
    precipitation_fig = {
        'data': [
            {'x': filtered_data['Date'], 'y': filtered_data['Précipitations dans les 24 dernières heures'].cumsum(), 'type': 'line', 'name': 'Cumulative Precipitation'}
        ],
        'layout': {
            'title': 'Cumulative Precipitation Over Time',
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Precipitation (mm)'}
        }
    }
    
    return f"{max_temp}°C", f"{min_temp}°C", f"{total_precipitation} mm", f"{avg_wind_speed} km/h", temp_fig, precipitation_fig

