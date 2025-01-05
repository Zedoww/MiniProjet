import dash
from dash import html, dcc
from datetime import datetime
from .utils.data_loader import load_cleaned_data, load_regions_geojson, load_departements_geojson
from .layout.themes import light_theme, dark_theme
from .layout.layout import serve_layout
from .callbacks.callbacks_figures import register_fullscreen_callbacks

# Charger les données
data = load_cleaned_data()
france_regions_geojson = load_regions_geojson("data/regions.geojson")
france_departements_geojson = load_departements_geojson("data/departements.geojson")

# Initialiser l'application Dash
#app = dash.Dash(__name__)
app = dash.Dash(__name__)
app.title = "Tableau de bord historique météo"
register_fullscreen_callbacks(app)

# Définir les plages de dates
min_date = data['Date'].min().date()
max_date = data['Date'].max().date()

# Générer les options de ville
city_options = [{'label': c, 'value': c} for c in data['communes (name)'].unique()]

# Définir la disposition dynamique
def serve_app_layout(theme_name='light'):
    theme = dark_theme if theme_name == 'dark' else light_theme
    return serve_layout(theme, city_options, min_date, max_date)

# Mise en page principale de l'application
app.layout = html.Div([
    dcc.Store(id='current-themee', data='light'),
    html.Div(id='page-content', children=serve_app_layout('light'))
], style={
    'backgroundColor': '#000000',
    'minHeight': '100vh',
    'width': '100vw',
    'height': '100vh',
    'margin': '0',
    'padding': '0'
})

# Importer et enregistrer les callbacks
from .callbacks.callbacks_general import register_general_callbacks
from .callbacks.callbacks_figures import register_figures_callbacks

register_general_callbacks(app)
register_figures_callbacks(app, data, france_regions_geojson, france_departements_geojson)