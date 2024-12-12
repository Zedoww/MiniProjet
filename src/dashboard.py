import pandas as pd
from datetime import datetime
from dateutil.parser import parse
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import requests
import json

# Charger les données nettoyées
cleaned_data_path = "data/cleaned/cleaneddata.csv"
data = pd.read_csv(cleaned_data_path)

# Forcer la conversion en datetime
data['Date'] = pd.to_datetime(data['Date'], errors='coerce', utc=True)
data = data.dropna(subset=['Date'])

# Obtenir la plage de dates
min_date = data['Date'].min().date()
max_date = data['Date'].max().date()

# Récupérer le GeoJSON des régions
url = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions.geojson"
response = requests.get(url)
france_regions_geojson = response.json()

# Thèmes
light_theme = {
    'name': 'light',
    'background': '#FAFAFA',
    'card_background': '#FFFFFF',
    'text_color': '#333333',
    'secondary_text': '#666666',
    'grid_color': '#DDDDDD',
    'box_shadow': '0px 2px 10px rgba(0,0,0,0.05)',
    'header_bg': '#F2F2F2',
    'emoji_color': '#333333',
    'map_text_color': '#000000'
}

dark_theme = {
    'name': 'dark',
    'background': '#181818',
    'card_background': '#2C2C2C',
    'text_color': '#E0E0E0',
    'secondary_text': '#B0B0B0',
    'grid_color': '#383838',
    'box_shadow': '0px 4px 12px rgba(0,0,0,0.4)',
    'header_bg': '#181818',
    'emoji_color': '#FFFFFF',
    'map_text_color': '#FFFFFF'
}

app = dash.Dash(__name__)
app.title = "Tableau de bord historique météo"

app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        <title>Tableau de bord historique météo</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            html, body {
                margin: 0;
                padding: 0;
                height: 100%;
                width: 100%;
                overflow: hidden;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""

def serve_layout(theme):
    card_style = {
        'background': theme['card_background'],
        'padding': '20px',
        'borderRadius': '14px',
        'boxShadow': theme['box_shadow'],
        'textAlign': 'center',
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',
        'justifyContent': 'center'
    }

    label_style = {
        'textAlign': 'center',
        'color': theme['secondary_text'],
        'fontSize': '14px',
        'marginTop': '5px',
        'fontWeight': '500'
    }

    value_style = {
        'textAlign': 'center',
        'fontWeight': 'bold',
        'fontSize': '28px',
        'color': theme['text_color'],
        'margin': '0'
    }

    emoji_style = {
        'fontSize': '32px',
        'textAlign': 'center',
        'marginBottom': '5px',
        'color': theme['emoji_color']
    }

    sidebar_style = {
        'width': '200px',
        'backgroundColor': theme['card_background'],
        'padding': '20px',
        'boxSizing': 'border-box'
    }

    theme_switch_style = {
        'textAlign': 'left',
        'marginBottom': '20px',
        'color': theme['text_color']
    }

    return html.Div([
        dcc.Store(id='current-theme', data='light'),
        html.Div([
            # Sidebar
            html.Div([
                html.H2("Menu", style={'color': theme['text_color'], 'marginBottom': '20px'}),
                html.Div("Thème :", style={'color': theme['text_color'], 'marginBottom': '10px'}),
                dcc.RadioItems(
                    id='theme-switch',
                    options=[
                        {'label': "Clair", 'value': 'light'},
                        {'label': "Sombre", 'value': 'dark'}
                    ],
                    value=theme['name'],
                    style=theme_switch_style,
                    labelStyle={'display': 'block', 'marginBottom': '8px', 'color': theme['text_color']}
                ),
                html.Hr(),

                html.Div("Données sur la carte :", style={'color': theme['text_color'], 'marginBottom': '10px'}),
                dcc.RadioItems(
                    id='map-metric',
                    options=[
                        {'label': 'Température', 'value': 'temp'},
                        {'label': 'Précipitations', 'value': 'precip'}
                    ],
                    value='temp',
                    labelStyle={'display': 'block', 'marginBottom': '8px', 'color': theme['text_color']}
                ),

                html.Hr(),
                html.Div("À venir...", style={'color': theme['text_color'], 'marginTop': '20px'})
            ], style=sidebar_style),

            # Contenu principal
            html.Div([
                # En-tête
                html.Div([
                    html.H1(
                        "Tableau de bord historique météo",
                        style={
                            'textAlign': 'center',
                            'fontSize': '24px',
                            'fontWeight': '600',
                            'color': theme['text_color'],
                            'marginBottom': '5px',
                            'marginTop': '10px'
                        }
                    ),
                    html.P(
                        "Une vue sobre et moderne des données météorologiques historiques de la ville sélectionnée.",
                        style={'textAlign': 'center', 'color': theme['secondary_text'], 'fontSize': '14px', 'margin': '0', 'paddingBottom': '10px'}
                    ),
                ], style={
                    'backgroundColor': theme['header_bg'],
                    'padding': '20px',
                    'borderRadius': '14px',
                    'boxShadow': theme['box_shadow'],
                    'marginBottom': '20px'
                }),

                # Filtres
                html.Div([
                    html.Div([
                        dcc.Dropdown(
                            id='city-dropdown',
                            options=[{'label': city, 'value': city} for city in data['communes (name)'].unique()],
                            value=data['communes (name)'].unique()[0],
                            placeholder="Sélectionnez une ville",
                            style={
                                'width': '100%',
                                'padding': '10px',
                                'fontSize': '16px',
                                'backgroundColor': theme['card_background'],
                                'color': theme['text_color']
                            },
                            className="dropdown"
                        )
                    ], style={'flex': '1', 'paddingRight': '10px'}),

                    html.Div([
                        dcc.DatePickerRange(
                            id='date-picker-range',
                            start_date=min_date,
                            end_date=max_date,
                            min_date_allowed=min_date,
                            max_date_allowed=max_date,
                            display_format='YYYY-MM-DD',
                            style={
                                'width': '100%',
                                'borderRadius': '8px',
                                'padding': '10px',
                                'fontSize': '16px',
                                'backgroundColor': theme['card_background'],
                                'border': f'1px solid {theme["grid_color"]}',
                                'color': theme['text_color']
                            }
                        )
                    ], style={'flex': '1', 'paddingLeft': '10px'})
                ], style={
                    'display': 'flex',
                    'marginBottom': '20px',
                    'borderRadius': '14px',
                    'padding': '10px',
                    'backgroundColor': theme['card_background'],
                    'boxShadow': theme['box_shadow']
                }),

                # KPI Cards
                html.Div([
                    html.Div([
                        html.Div("🌡️", style=emoji_style),
                        html.H4("Température maximale", style=label_style),
                        html.P(id='max-temp-24h', style=value_style),
                    ], style=card_style),

                    html.Div([
                        html.Div("❄️", style=emoji_style),
                        html.H4("Température minimale", style=label_style),
                        html.P(id='min-temp-24h', style=value_style),
                    ], style=card_style),

                    html.Div([
                        html.Div("🌧️", style=emoji_style),
                        html.H4("Précipitations totales", style=label_style),
                        html.P(id='total-precipitation', style=value_style),
                    ], style=card_style),

                    html.Div([
                        html.Div("☔", style=emoji_style),
                        html.H4("Jours de précipitations", style=label_style),
                        html.P(id='precipitation-days', style=value_style),
                    ], style=card_style)
                ], style={
                    'display': 'grid',
                    'gridTemplateColumns': 'repeat(4, 1fr)',
                    'gap': '20px',
                    'marginBottom': '30px'
                }),

                # Graphiques
                html.Div([
                    dcc.Graph(id='temp-graph', style={
                        'height': '300px',
                        'borderRadius': '14px',
                        'backgroundColor': theme['card_background'],
                        'boxShadow': theme['box_shadow'],
                        'padding': '10px'
                    }),
                    dcc.Graph(id='precipitation-bar', style={
                        'height': '300px',
                        'borderRadius': '14px',
                        'backgroundColor': theme['card_background'],
                        'boxShadow': theme['box_shadow'],
                        'padding': '10px'
                    })
                ], style={
                    'display': 'grid',
                    'gridTemplateColumns': 'repeat(2, 1fr)',
                    'gap': '20px',
                    'marginBottom': '20px',
                }),

                # Carte
                html.Div([
                    dcc.Graph(id='map-graph', style={
                        'height': '500px',
                        'borderRadius': '14px',
                        'backgroundColor': theme['card_background'],
                        'boxShadow': theme['box_shadow'],
                        'padding': '10px'
                    })
                ], style={
                    'marginBottom': '20px'
                }),

            ], style={
                'flex': '1',
                'padding': '20px',
                'boxSizing': 'border-box',
                'overflowY': 'auto'
            })
        ], style={
            'display': 'flex',
            'flexDirection': 'row',
            'height': '100vh',
            'margin': '0',
            'padding': '0'
        })
    ], style={
        'fontFamily': '-apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif',
        'backgroundColor': theme['background'],
        'width': '100%',
        'height': '100%',
        'margin': '0',
        'padding': '0',
        'color': theme['text_color']
    })


app.layout = html.Div([
    dcc.Store(id='current-theme', data='light'),
    html.Div(id='page-content', children=serve_layout(light_theme))
], style={
    'backgroundColor': '#000000',
    'minHeight': '100vh',
    'width': '100vw',
    'height': '100vh',
    'margin': '0',
    'padding': '0'
})


@app.callback(
    Output('current-theme', 'data'),
    Input('theme-switch', 'value')
)
def switch_theme(selected_theme):
    return selected_theme

@app.callback(
    Output('page-content', 'children'),
    Input('current-theme', 'data')
)
def update_page(theme_value):
    if theme_value == 'dark':
        return serve_layout(dark_theme)
    return serve_layout(light_theme)


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
        Input('map-metric', 'value')
    ]
)
def update_dashboard(start_date, end_date, selected_city, theme_value, map_metric):
    start_date = parse(start_date).date()
    end_date = parse(end_date).date()

    # Copie des données pour la ville sélectionnée
    city_data = data.loc[data['communes (name)'] == selected_city].copy()

    city_data.loc[:, 'Température maximale sur 24 heures'] = city_data['Température maximale sur 24 heures'].fillna(city_data['Température'])
    city_data.loc[:, 'Température minimale sur 24 heures'] = city_data['Température minimale sur 24 heures'].fillna(city_data['Température'])

    city_data.loc[:, 'Date'] = pd.to_datetime(city_data['Date'])
    city_data_daily = city_data.groupby(city_data['Date'].dt.date).mean(numeric_only=True).reset_index()
    filtered_data = city_data_daily[(city_data_daily['Date'] >= start_date) & (city_data_daily['Date'] <= end_date)]

    if filtered_data.empty:
        return "N/A", "N/A", "N/A", "N/A", {}, {}, {}

    max_temp = round(filtered_data['Température maximale sur 24 heures'].max() - 273.15, 1)
    min_temp = round(filtered_data['Température minimale sur 24 heures'].min() - 273.15, 1)
    total_precipitation = round(filtered_data['Précipitations dans les 24 dernières heures'].fillna(0).sum(), 1)
    precipitation_days = len(filtered_data[filtered_data['Précipitations dans les 24 dernières heures'].fillna(0) > 0])

    theme = dark_theme if theme_value == 'dark' else light_theme
    bg_color = theme['card_background']
    text_color = theme['text_color']
    grid_color = theme['grid_color']

    # Graphique températures
    temp_fig = {
        'data': [
            {
                'x': filtered_data['Date'],
                'y': filtered_data['Température maximale sur 24 heures'] - 273.15,
                'type': 'line',
                'name': 'Température Max',
                'line': {'color': '#4A90E2', 'width': 3}
            },
        ],
        'layout': {
            'title': {'text': 'Températures', 'font': {'color': text_color, 'size': 16}},
            'xaxis': {'title': 'Date', 'color': text_color, 'gridcolor': grid_color},
            'yaxis': {'title': 'Température (°C)', 'color': text_color, 'gridcolor': grid_color},
            'plot_bgcolor': bg_color,
            'paper_bgcolor': bg_color,
            'font': {'color': text_color},
            'margin': {'l': 50, 'r': 20, 't': 50, 'b': 50}
        }
    }

    # Graphique précipitations
    precipitation_fig = {
        'data': [
            {
                'x': filtered_data['Date'],
                'y': filtered_data['Précipitations dans les 24 dernières heures'],
                'type': 'bar',
                'name': 'Précipitations',
                'marker': {'color': '#4A90E2'}
            }
        ],
        'layout': {
            'title': {'text': 'Précipitations', 'font': {'color': text_color, 'size': 16}},
            'xaxis': {'title': 'Date', 'color': text_color, 'gridcolor': grid_color},
            'yaxis': {'title': 'Précipitations (mm)', 'color': text_color, 'gridcolor': grid_color},
            'plot_bgcolor': bg_color,
            'paper_bgcolor': bg_color,
            'font': {'color': text_color},
            'margin': {'l': 50, 'r': 20, 't': 50, 'b': 50}
        }
    }

    # Données globales pour la carte (agrégation par région)
    global_filtered_data = data.copy()
    global_filtered_data.loc[:, 'Date'] = pd.to_datetime(global_filtered_data['Date'])
    global_filtered_data = global_filtered_data[(global_filtered_data['Date'].dt.date >= start_date) & (global_filtered_data['Date'].dt.date <= end_date)]

    if global_filtered_data.empty:
        return f"{max_temp}°C", f"{min_temp}°C", f"{total_precipitation} mm", f"{precipitation_days}", temp_fig, precipitation_fig, {}

    region_data = global_filtered_data.groupby('region (code)', as_index=False).agg({
        'Température': 'mean',
        'Précipitations dans les 24 dernières heures': 'mean'
    })

    # Configuration de la carte par région
    if map_metric == 'temp':
        z = region_data['Température'] - 273.15
        colorscale = 'RdYlBu_r'
        title_map = "Température moyenne par région (°C)"
        hovertemplate = "<b>Région %{location}</b><br>Température moy: %{z:.1f}°C<extra></extra>"
        color_col = 'Température'
    else:
        z = region_data['Précipitations dans les 24 dernières heures'].fillna(0)
        colorscale = 'Blues'
        title_map = "Précipitations moyennes par région (mm)"
        hovertemplate = "<b>Région %{location}</b><br>Précipitations moy: %{z:.1f} mm<extra></extra>"
        color_col = 'Précipitations'

    map_fig = px.choropleth_mapbox(
        region_data,
        geojson=france_regions_geojson,
        locations='region (code)',
        featureidkey='properties.code',  # Assurez-vous que ce champ correspond aux codes région
        color=z,
        color_continuous_scale=colorscale,
        mapbox_style='carto-positron',
        zoom=4.5,
        center={"lat": 46.5, "lon": 2},
        opacity=0.7,
        hover_name='region (code)',
    )
    map_fig.update_traces(hovertemplate=hovertemplate)

    map_fig.update_layout(
        title={'text': title_map, 'font': {'color': text_color, 'size': 18}},
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        font=dict(color=text_color),
        margin={'r':0,'t':50,'l':0,'b':0}
    )

    map_fig.update_coloraxes(colorbar=dict(
        title=color_col,
        titlefont=dict(color=text_color),
        tickfont=dict(color=text_color)
    ))

    return (
        f"{max_temp}°C",
        f"{min_temp}°C",
        f"{total_precipitation} mm",
        f"{precipitation_days}",
        temp_fig,
        precipitation_fig,
        map_fig
    )


