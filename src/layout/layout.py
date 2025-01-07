from dash import html, dcc
from .themes import light_theme, dark_theme
from .sidebar import sidebar
from .kpi_cards import kpi_cards
import pandas as pd
from datetime import date
import locale

locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

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
                        style={
                            'textAlign': 'center',
                            'color': theme['secondary_text'],
                            'fontSize': '14px',
                            'margin': '0',
                            'paddingBottom': '10px'
                        }
                    ),
                ], style={
                    'backgroundColor': theme['header_bg'],
                    'padding': '20px',
                    'borderRadius': '14px',
                    'boxShadow': theme['box_shadow'],
                    'marginBottom': '20px'
                }),

                # Filtres de date (slider)
                html.Div([
                    dcc.RangeSlider(
                        id='date-range-slider',
                        min=min_date.toordinal(),
                        max=max_date.toordinal(),
                        value=[min_date.toordinal(), max_date.toordinal()],
                        marks={
                            d.toordinal(): d.strftime('%b').capitalize()
                            for d in pd.date_range(min_date, max_date, freq='ME')
                        },
                        tooltip={
                            "placement": "bottom",
                            "always_visible": True,
                            "template": "{value}",
                            "transform": "ordinalToDate"
                        },
                        included=True,
                        updatemode='drag',
                        className="custom-range-slider"
                    )
                ], style={
                    'margin': '30px 0',
                    'padding': '10px',
                    'borderRadius': '14px',
                    'backgroundColor': theme['card_background'],
                    'boxShadow': theme['box_shadow']
                }),

                # KPI Cards
                kpi_cards(theme),

                # Graphiques (Temp + Précip)
                html.Div([
                    html.Div([
                        dcc.Graph(
                            id='temp-graph',
                            className='fullscreenable',
                            style={}
                        ),
                        html.Button(
                            "⛶",
                            id='fullscreen-temp-graph-btn',
                            className='fullscreen-button'
                        ),
                        html.Button(
                            "Quitter le plein écran",
                            id='exit-fullscreen-temp-graph-btn',
                            className='exit-fullscreen-button',
                            style={'display': 'none'}
                        )
                    ], className='graph-container'),

                    html.Div([
                        dcc.Graph(
                            id='precipitation-bar',
                            className='fullscreenable',
                            style={}
                        ),
                        html.Button(
                            "⛶",
                            id='fullscreen-precipitation-bar-btn',
                            className='fullscreen-button'
                        ),
                        html.Button(
                            "Quitter le plein écran",
                            id='exit-fullscreen-precipitation-bar-btn',
                            className='exit-fullscreen-button',
                            style={'display': 'none'}
                        )
                    ], className='graph-container'),

                    html.Div([
                        dcc.Graph(
                            id='temp-histogram',
                            className='fullscreenable',
                            style={}
                        ),
                        html.Button(
                            "⛶",
                            id='fullscreen-histogram-btn',
                            className='fullscreen-button'
                        ),
                        html.Button(
                            "Quitter le plein écran",
                            id='exit-fullscreen-histogram-btn',
                            className='exit-fullscreen-button',
                            style={'display': 'none'}
                        )
                    ], className='graph-container'),
                ], style={
                    'display': 'grid',
                    'gridTemplateColumns': 'repeat(3, 1fr)',
                    'gap': '20px',
                    'marginBottom': '20px',
                }),

                # Graphique Carte
                html.Div([
                    html.Div([
                        dcc.Graph(
                            id='map-graph',
                            className='fullscreenable',
                            style={}
                        ),
                        html.Button(
                            "⛶",
                            id='fullscreen-map-graph-btn',
                            className='fullscreen-button'
                        ),
                        html.Button(
                            "Quitter le plein écran",
                            id='exit-fullscreen-map-graph-btn',
                            className='exit-fullscreen-button',
                            style={'display': 'none'}
                        )
                    ], className='graph-container')
                ])
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