from dash import Dash
from src.pages.home import render_home

# Initialiser l'application Dash
app = Dash(__name__)

# Définir la mise en page avec le contenu du fichier home.py
app.layout = render_home()

if __name__ == "__main__":
    app.run_server(debug=True)