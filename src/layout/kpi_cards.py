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
        'justifyContent': 'center'
    }

    label_style = {
        'textAlign': 'center',
        'color': theme['secondary_text'],
        'fontSize': '14px',
        'marginTop': '5px',
        'fontWeight': '500'
    }

    value_style = {
        'textAlign': 'center',
        'fontWeight': 'bold',
        'fontSize': '28px',
        'color': theme['text_color'],
        'margin': '0'
    }

    emoji_style = {
        'fontSize': '32px',
        'textAlign': 'center',
        'marginBottom': '5px',
        'color': theme['emoji_color']
    }

    return html.Div([
        html.Div([
            html.Div("🌡️", style=emoji_style),
            html.H4("Température maximale", style=label_style),
            html.P(id='max-temp-24h', style=value_style),
        ], style=card_style),

        html.Div([
            html.Div("❄️", style=emoji_style),
            html.H4("Température minimale", style=label_style),
            html.P(id='min-temp-24h', style=value_style),
        ], style=card_style),

        html.Div([
            html.Div("🌧️", style=emoji_style),
            html.H4("Précipitations totales", style=label_style),
            html.P(id='total-precipitation', style=value_style),
        ], style=card_style),

        html.Div([
            html.Div("☔", style=emoji_style),
            html.H4("Jours de précipitations", style=label_style),
            html.P(id='precipitation-days', style=value_style),
        ], style=card_style)
    ], style={
        'display': 'grid',
        'gridTemplateColumns': 'repeat(4, 1fr)',
        'gap': '20px',
        'marginBottom': '30px'
    })
