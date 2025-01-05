from dash import dcc, html

def sidebar(theme, city_options):
    # Définir la classe de style de base pour le thème
    theme_class = 'dropdown-dark' if theme['name'] == 'dark' else 'dropdown-light'

    return html.Div([
        html.H2("Menu", style={'color': theme['text_color'], 'marginBottom': '20px'}),
        html.Div("Thème :", style={'color': theme['text_color'], 'marginBottom': '10px', 'fontWeight': 'bold'}),
        dcc.RadioItems(
            id='theme-switch',
            options=[
                {'label': " ☀️ Light", 'value': 'light'},
                {'label': " 🌙 Dark", 'value': 'dark'}
            ],
            value=theme['name'],
            labelStyle={'display': 'block', 'marginBottom': '8px', 'color': theme['text_color']}
        ),

        html.Hr(style={'marginBottom': '20px'}),
        html.Div([
            html.Div("Ville :", style={'fontWeight': 'bold', 'marginBottom': '10px'}),
            dcc.Dropdown(
                id='city-dropdown',
                options=city_options,
                value=city_options[0]['value'] if city_options else None,
                placeholder="Sélectionnez une ville",
                className=f"dropdown {theme_class}",  # Applique la classe conditionnelle
                clearable=False
            )
        ], style={'marginBottom': '20px'}),

        html.Hr(style={'marginBottom': '20px'}),
        html.Div("Données de carte :", style={'color': theme['text_color'], 'marginBottom': '10px', 'fontWeight': 'bold'}),
        dcc.RadioItems(
            id='map-metric',
            options=[
                {'label': ' 🌡️ Température', 'value': 'temp'},
                {'label': ' 🌧️ Précipitations', 'value': 'precip'}
            ],
            value='temp',
            labelStyle={'display': 'block', 'marginBottom': '8px', 'color': theme['text_color']}
        ),

        html.Hr(style={'marginBottom': '5px'}),
        dcc.RadioItems(
            id='geo-level',
            options=[
                {'label': ' 🌍 Région', 'value': 'region'},
                {'label': ' 🏛️ Département', 'value': 'department'},
            ],
            value='region',
            labelStyle={'display': 'block', 'marginBottom': '8px', 'color': theme['text_color']}
        ),
        html.Div("À venir... 🚧⏳", style={'color': theme['text_color'], 'marginTop': '20px'}),

    ], style={
        'width': '200px',
        'backgroundColor': theme['card_background'],
        'padding': '20px',
        'boxSizing': 'border-box'
    })