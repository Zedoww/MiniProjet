from dash import dcc, html

def sidebar(theme, city_options):
    return html.Div([
        html.H2("Menu", style={'color': theme['text_color'], 'marginBottom': '20px'}),
        html.Div("Thème :", style={'color': theme['text_color'], 'marginBottom': '10px'}),
        dcc.RadioItems(
            id='theme-switch',
            options=[
                {'label': "Light", 'value': 'light'},
                {'label': "Dark", 'value': 'dark'}
            ],
            value=theme['name'],
            labelStyle={'display': 'block', 'marginBottom': '8px', 'color': theme['text_color']}
        ),

        

        html.Hr(),
        html.Div("Ville :", style={'color': theme['text_color'], 'marginBottom': '10px'}),
        dcc.Dropdown(
            id='city-dropdown',
            options=city_options,
            value=city_options[0]['value'] if city_options else None,
            placeholder="Sélectionnez une ville",
            style={
                'width': '100%',
                'padding': '10px',
                'fontSize': '16px',
                'backgroundColor': theme['card_background'],
                'color': theme['text_color']
            },
            className="dropdown"
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
        dcc.RadioItems(
            id='geo-level',
            options=[
                {'label': 'Région', 'value': 'region'},
                {'label': 'Département', 'value': 'department'},
            ],
            value='region',  # Valeur par défaut
            labelStyle={'display': 'block', 'marginBottom': '8px', 'color': theme['text_color']}
),
        html.Div("À venir...", style={'color': theme['text_color'], 'marginTop': '20px'}),

        

    ], style={
        'width': '200px',
        'backgroundColor': theme['card_background'],
        'padding': '20px',
        'boxSizing': 'border-box'
    })
