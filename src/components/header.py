from dash import html

def create_header():
    return html.Header([
        html.H1("Weather History Dashboard", style={"textAlign": "center", "padding": "10px"})
    ])
