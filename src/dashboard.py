import dash
from dash import html, dcc
from datetime import datetime
from .utils.data_loader import load_cleaned_data, load_regions_geojson, load_departements_geojson
from .layout.themes import light_theme, dark_theme
from .layout.layout import serve_layout

data = load_cleaned_data()
france_regions_geojson = load_regions_geojson("data/regions.geojson")
france_departements_geojson = load_departements_geojson("data/departements.geojson")

app = dash.Dash(__name__)
app.title = "Tableau de bord historique météo"

min_date = data['Date'].min().date()
max_date = data['Date'].max().date()

city_options = [{'label': c, 'value': c} for c in data['communes (name)'].unique()]

def serve_app_layout(theme_name='light'):
    theme = dark_theme if theme_name == 'dark' else light_theme
    return serve_layout(theme, city_options, min_date, max_date)

app.layout = html.Div([
    dcc.Store(id='current-theme', data='light'),
    html.Div(id='page-content', children=serve_app_layout('light'))
], style={
    'backgroundColor': '#000000',
    'minHeight': '100vh',
    'width': '100vw',
    'height': '100vh',
    'margin': '0',
    'padding': '0'
})

# Import et enregistrement des callbacks
from .callbacks.callbacks_general import register_general_callbacks
from .callbacks.callbacks_figures import register_figures_callbacks

register_general_callbacks(app)
register_figures_callbacks(app, data, france_regions_geojson,france_departements_geojson)
