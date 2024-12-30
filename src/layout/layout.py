from dash import html, dcc
from .themes import light_theme, dark_theme
from .sidebar import sidebar
from .kpi_cards import kpi_cards

def serve_layout(theme, city_options, min_date, max_date):
    return html.Div([
        dcc.Store(id='current-theme', data=theme['name']),
        html.Div([
            # Sidebar
            sidebar(theme, city_options),

            # Contenu principal
            html.Div([
                # En-tête
                html.Div([
                    html.H1(
                        "Tableau de bord historique météo",
                        style={
                            'textAlign': 'center',
                            'fontSize': '24px',
                            'fontWeight': '600',
                            'color': theme['text_color'],
                            'marginBottom': '5px',
                            'marginTop': '10px'
                        }
                    ),
                    html.P(
                        "Une vue sobre et moderne des données météorologiques historiques.",
                        style={'textAlign': 'center', 'color': theme['secondary_text'], 'fontSize': '14px', 'margin': '0', 'paddingBottom': '10px'}
                    ),
                ], style={
                    'backgroundColor': theme['header_bg'],
                    'padding': '20px',
                    'borderRadius': '14px',
                    'boxShadow': theme['box_shadow'],
                    'marginBottom': '20px'
                }),

                # Filtres de date
                html.Div([
                dcc.DatePickerRange(
                    id='date-picker-range',
                    start_date=min_date,
                    end_date=max_date,
                    min_date_allowed=min_date,
                    max_date_allowed=max_date,
                    display_format='YYYY-MM-DD',
                    style={
                        'width': '100%',
                        'borderRadius': '8px',
                        'padding': '10px',
                        'fontSize': '16px',
                        'backgroundColor': theme['card_background'],  # Fond sombre basé sur le thème
                        'color': theme['text_color'],                # Couleur du texte
                        'border': f'1px solid {theme["grid_color"]}', # Bordure adaptée au thème
                        'boxShadow': theme['box_shadow'],            # Ombre douce
                        'outline': 'none'                            # Supprime les bordures au focus
                    }
                )
            ], style={
                'flex': '1',
                'padding': '10px',
                'backgroundColor': theme['card_background'],  # Fond sombre pour le conteneur
                'boxShadow': theme['box_shadow'],             # Ombre pour le conteneur
                'borderRadius': '14px',
                'marginBottom': '20px'
            }),

                # KPI Cards
                kpi_cards(theme),

                # Graphiques
                html.Div([
                    dcc.Graph(id='temp-graph', style={
                        'height': '300px',
                        'borderRadius': '14px',
                        'backgroundColor': theme['card_background'],
                        'boxShadow': theme['box_shadow'],
                        'padding': '10px'
                    }),
                    dcc.Graph(id='precipitation-bar', style={
                        'height': '300px',
                        'borderRadius': '14px',
                        'backgroundColor': theme['card_background'],
                        'boxShadow': theme['box_shadow'],
                        'padding': '10px'
                    })
                ], style={
                    'display': 'grid',
                    'gridTemplateColumns': 'repeat(2, 1fr)',
                    'gap': '20px',
                    'marginBottom': '20px',
                }),

                # Carte
                html.Div([
                    dcc.Graph(id='map-graph', style={
                        'height': '500px',
                        'borderRadius': '14px',
                        'backgroundColor': theme['card_background'],
                        'boxShadow': theme['box_shadow'],
                        'padding': '10px'
                    })
                ], style={
                    'marginBottom': '20px'
                }),

            ], style={
                'flex': '1',
                'padding': '20px',
                'boxSizing': 'border-box',
                'overflowY': 'auto'
            })
        ], style={
            'display': 'flex',
            'flexDirection': 'row',
            'height': '100vh',
            'margin': '0',
            'padding': '0'
        })
    ], style={
        'fontFamily': '-apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif',
        'backgroundColor': theme['background'],
        'width': '100%',
        'height': '100%',
        'margin': '0',
        'padding': '0',
        'color': theme['text_color']
    })
