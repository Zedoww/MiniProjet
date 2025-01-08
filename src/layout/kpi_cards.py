from dash import html

def kpi_cards(theme):
    card_style = {
        'background': theme['card_background'],
        'padding': '20px',
        'borderRadius': '14px',
        'boxShadow': theme['box_shadow'],
        'textAlign': 'center',
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',
        'justifyContent': 'center',
        'transition': 'all 0.3s ease-in-out'
    }

    label_style = {
        'textAlign': 'center',
        'color': theme['secondary_text'],
        'fontSize': '14px',
        'marginTop': '5px',
        'fontWeight': '500',
        'transition': 'all 0.3s ease-in-out'
    }

    value_style = {
        'textAlign': 'center',
        'fontWeight': 'bold',
        'fontSize': '28px',
        'color': theme['text_color'],
        'margin': '0',
        'transition': 'all 0.3s ease-in-out'
    }

    # Optionnel, si tu utilises des emojis
    emoji_style = {
        'fontSize': '32px',
        'textAlign': 'center',
        'marginBottom': '5px',
        'color': theme['emoji_color'],
        'transition': 'all 0.3s ease-in-out'
    }

    return html.Div([
        html.Div([
            html.H4("Température maximale", style=label_style),
            html.P(id='max-temp-24h', style=value_style),
        ], style=card_style),

        html.Div([
            html.H4("Température minimale", style=label_style),
            html.P(id='min-temp-24h', style=value_style),
        ], style=card_style),

        html.Div([
            html.H4("Précipitations totales", style=label_style),
            html.P(id='total-precipitation', style=value_style),
        ], style=card_style),

        html.Div([
            html.H4("Jours de précipitations", style=label_style),
            html.P(id='precipitation-days', style=value_style),
        ], style=card_style)
    ], style={
        'display': 'grid',
        'gridTemplateColumns': 'repeat(4, 1fr)',
        'gap': '20px',
        'marginBottom': '30px'
    })