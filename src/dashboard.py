import pandas as pd
from datetime import datetime
from dateutil.parser import parse
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Charger les données nettoyées
cleaned_data_path = "data/cleaned/cleaneddata.csv"
data = pd.read_csv(cleaned_data_path)
data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

# Obtenir la plage de dates
min_date = data['Date'].min()
max_date = data['Date'].max()

# Grouper les données par jour pour simplifier les graphiques
data_daily = data.groupby(data['Date'].dt.date).mean()

# Supprimer toute colonne existante "Date" avant de réinitialiser l'index
if 'Date' in data_daily.columns:
    data_daily = data_daily.drop(columns=['Date'])

data_daily = data_daily.rename_axis('Date').reset_index()

# Créer l'application Dash
app = dash.Dash(__name__)
app.title = "Weather History Dashboard"

# Mise en page
app.layout = html.Div([
    html.H1("Weather History Dashboard", style={'textAlign': 'center', 'marginBottom': '20px'}),
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=min_date,
        end_date=max_date,
        min_date_allowed=min_date,
        max_date_allowed=max_date,
        display_format='YYYY-MM-DD',
        initial_visible_month=min_date,
        style={'marginBottom': '30px'}
    ),
    html.Div([
        html.Div([
            html.H3("Maximum Temperature", style={'textAlign': 'center'}),
            html.P(id='max-temp', style={'fontSize': '24px', 'textAlign': 'center'}),
        ], className="kpi", style={'flex': '1', 'margin': '0 10px'}),
        html.Div([
            html.H3("Minimum Temperature", style={'textAlign': 'center'}),
            html.P(id='min-temp', style={'fontSize': '24px', 'textAlign': 'center'}),
        ], className="kpi", style={'flex': '1', 'margin': '0 10px'}),
        html.Div([
            html.H3("Total Precipitation", style={'textAlign': 'center'}),
            html.P(id='total-precipitation', style={'fontSize': '24px', 'textAlign': 'center'}),
        ], className="kpi", style={'flex': '1', 'margin': '0 10px'}),
    ], style={'display': 'flex', 'justifyContent': 'center', 'marginBottom': '30px'}),
    dcc.Graph(id='temp-graph', style={'marginBottom': '30px'}),
    dcc.Graph(id='precipitation-bar', style={'marginBottom': '30px'})
])

# Callbacks pour l'interactivité
@app.callback(
    [
        Output('max-temp', 'children'),
        Output('min-temp', 'children'),
        Output('total-precipitation', 'children'),
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
    max_temp = round(filtered_data['Temperature'].max(), 1)
    min_temp = round(filtered_data['Temperature'].min(), 1)
    total_precipitation = round(filtered_data['Precipitation'].sum(), 1)
    
    # Créer les graphiques
    temp_fig = {
        'data': [
            {'x': filtered_data['Date'], 'y': filtered_data['Temperature'], 'type': 'line', 'name': 'Temperature'}
        ],
        'layout': {
            'title': 'Temperature Over Time',
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Temperature (°C)'}
        }
    }
    
    precipitation_fig = {
        'data': [
            {'x': filtered_data['Date'], 'y': filtered_data['Precipitation'].cumsum(), 'type': 'line', 'name': 'Cumulative Precipitation'}
        ],
        'layout': {
            'title': 'Cumulative Precipitation Over Time',
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Precipitation (mm)'}
        }
    }
    
    return f"{max_temp}°C", f"{min_temp}°C", f"{total_precipitation} mm", temp_fig, precipitation_fig

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
