from dash import dcc, html

def sidebar(theme, city_options):
    theme_class = 'dropdown-dark' if theme['name'] == 'dark' else 'dropdown-light'

    return html.Div([
        html.H2("Menu", style={
            'color': theme['text_color'], 
            'marginBottom': '20px',
            'transition': 'all 0.3s ease-in-out'
        }),
        
        # Switch pour Light/Dark mode
        html.Div([
            html.Div("Light", className="theme-label"),
            html.Div(
                id="theme-switch", 
                className=f"switch {'active' if theme['name'] == 'dark' else ''}",
                children=[
                    html.Div(className="toggle")
                ]
            ),
            html.Div("Dark", className="theme-label")
        ], style={
            'display': 'flex', 
            'justifyContent': 'space-between', 
            'alignItems': 'center', 
            'marginBottom': '20px'
        }),

        # Ville Dropdown
        html.Div([
            html.Div("Ville :", style={'fontWeight': 'bold', 'marginBottom': '10px', 'color': theme['text_color']}),
            dcc.Dropdown(
                id='city-dropdown',
                options=city_options,
                value=city_options[0]['value'] if city_options else None,
                placeholder="Sélectionnez une ville",
                className=f"dropdown {theme_class}",  # Applique la classe conditionnelle (light/dark)
                clearable=False
            )
        ], style={'marginBottom': '20px'}),

        html.Hr(style={'marginBottom': '20px', 'borderColor': theme['text_color']}),

        # Sélection de la métrique de carte
        html.Div("Données de carte :", style={
            'color': theme['text_color'], 
            'marginBottom': '10px', 
            'fontWeight': 'bold'
        }),
        dcc.RadioItems(
            id='map-metric',
            options=[
                {'label': 'Température', 'value': 'temp'},
                {'label': 'Précipitations', 'value': 'precip'}
            ],
            value='temp',
            labelStyle={
                'display': 'block', 
                'marginBottom': '8px', 
                'color': theme['text_color']
            }
        ),

        html.Hr(style={'marginBottom': '5px', 'borderColor': theme['text_color']}),

        # Sélection du niveau géographique
        dcc.RadioItems(
            id='geo-level',
            options=[
                {'label': ' Région', 'value': 'region'},
                {'label': ' Département', 'value': 'department'},
            ],
            value='region',
            labelStyle={
                'display': 'block', 
                'marginBottom': '8px', 
                'color': theme['text_color']
            }
        ),
        html.Div("À venir... 🚧⏳", style={'color': theme['text_color'], 'marginTop': '20px'}),

    ], style={
        'width': '200px',
        'backgroundColor': theme['card_background'],
        'padding': '20px',
        'boxSizing': 'border-box',
        'transition': 'all 0.3s ease-in-out'
    })