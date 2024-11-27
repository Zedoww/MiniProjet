import dash
from dash import html, dcc

# Initialisation de l'application Dash
app = dash.Dash(__name__)

# Définition du layout
app.layout = html.Div([
    html.H1("Dashboard Mini-Projet"),
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'Example'},
            ],
            'layout': {
                'title': 'Exemple de graphique'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)