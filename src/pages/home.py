from dash import Dash, dcc, html
import pandas as pd

# Acces data
data_file = "data/raw/donnees-synop-essentielles-omm.csv"
#df = pd.read_csv(data_file, sep=";")
#df["Date"] = pd.to_datetime(df["Date"])

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

if __name__ == "__main__":
    # Exemple de données fictives pour tester l'interface graphique
    df = pd.DataFrame({
        "Nom": ["Region 1", "Region 2", "Region 3"],  # Noms fictifs des régions
        "Date": pd.date_range(start="2023-01-01", periods=3, freq="D"),  # Dates fictives
        "Température (°C)": [25, 30, 35],  # Températures fictives
        "Précipitations dans les 24 dernières heures": [5, 10, 0]  # Précipitations fictives
    })

    # Lancer l'application Dash localement
    app = Dash(__name__)
    app.layout = render_home()
    
    # Ouvrir automatiquement dans le navigateur Safari
    import webbrowser
    webbrowser.get("safari").open("http://127.0.0.1:8050/")

    # Démarrer le serveur Dash
    app.run_server(debug=True)