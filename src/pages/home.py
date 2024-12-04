from dash import dcc, html
import pandas as pd

# Acces data
data_file = "data/raw/donnees-synop-essentielles-omm.csv"
df = pd.read_csv(data_file, sep=";")
df["Date"] = pd.to_datetime(df["Date"])

# Dropdown menu
def create_dropdown():
    return dcc.Dropdown(
        id="region-dropdown",
        options=[
            {"label": region, "value": region} for region in df["Nom"].unique()
        ],
        placeholder="Select a region",
        style={"width": "50%", "margin": "auto"},
    )

# Helper function to create the stats container
def create_stats_container():
    return html.Div(
        id="stats-container",
        style={"display": "flex", "justifyContent": "space-around"},
        children=[
            html.Div(id="max-temp", children="Maximum Temperature: N/A"),
            html.Div(id="min-temp", children="Minimum Temperature: N/A"),
            html.Div(id="precipitation", children="Precipitation: N/A"),
        ],
    )

# Créations de graphes
def create_graphs():
    return html.Div(
        children=[
            dcc.Graph(id="temperature-graph"),
            dcc.Graph(id="precipitation-graph"),
        ]
    )

# Assemblage des parties
def render_home():
    return html.Div(
        children=[
            html.H1("Weather Dashboard", style={"textAlign": "center"}),
            create_dropdown(),
            create_stats_container(),
            create_graphs(),
        ]
    )