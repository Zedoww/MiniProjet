from dash import html

def create_kpi_cards():
    return html.Div([
        html.Div([
            html.H4("Maximum Temperature", style={"marginBottom": "10px"}),
            html.H2(id='kpi-max-temp', style={"fontWeight": "bold"})
        ], className="card text-center p-3", style={
            "width": "250px",
            "height": "150px",
            "display": "inline-block",
            "margin": "20px",
            "border": "2px solid black",
            "borderRadius": "10px",
            "boxShadow": "2px 2px 10px rgba(0, 0, 0, 0.1)",
            "textAlign": "center",
            "padding": "20px",
            "verticalAlign": "middle"
        }),

        html.Div([
            html.H4("Minimum Temperature", style={"marginBottom": "10px"}),
            html.H2(id='kpi-min-temp', style={"fontWeight": "bold"})
        ], className="card text-center p-3", style={
            "width": "250px",
            "height": "150px",
            "display": "inline-block",
            "margin": "20px",
            "border": "2px solid black",
            "borderRadius": "10px",
            "boxShadow": "2px 2px 10px rgba(0, 0, 0, 0.1)",
            "textAlign": "center",
            "padding": "20px",
            "verticalAlign": "middle"
        })
    ], style={"textAlign": "center", "marginTop": 20, "display": "flex", "justifyContent": "center", "alignItems": "center"})
