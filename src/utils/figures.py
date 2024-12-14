import plotly.express as px

def create_temperature_figure(filtered_data, theme):
    fig = {
        'data': [
            {
                'x': filtered_data['Date'],
                'y': filtered_data['Température maximale sur 24 heures'] - 273.15,
                'type': 'line',
                'name': 'Température Max',
                'line': {'color': '#4A90E2', 'width': 3}
            },
        ],
        'layout': {
            'title': {'text': 'Températures', 'font': {'color': theme['text_color'], 'size': 16}},
            'xaxis': {'title': 'Date', 'color': theme['text_color'], 'gridcolor': theme['grid_color']},
            'yaxis': {'title': 'Température (°C)', 'color': theme['text_color'], 'gridcolor': theme['grid_color']},
            'plot_bgcolor': theme['card_background'],
            'paper_bgcolor': theme['card_background'],
            'font': {'color': theme['text_color']},
            'margin': {'l': 50, 'r': 20, 't': 50, 'b': 50}
        }
    }
    return fig

def create_precipitation_bar(filtered_data, theme):
    fig = {
        'data': [
            {
                'x': filtered_data['Date'],
                'y': filtered_data['Précipitations dans les 24 dernières heures'],
                'type': 'bar',
                'name': 'Précipitations',
                'marker': {'color': '#4A90E2'}
            }
        ],
        'layout': {
            'title': {'text': 'Précipitations', 'font': {'color': theme['text_color'], 'size': 16}},
            'xaxis': {'title': 'Date', 'color': theme['text_color'], 'gridcolor': theme['grid_color']},
            'yaxis': {'title': 'Précipitations (mm)', 'color': theme['text_color'], 'gridcolor': theme['grid_color']},
            'plot_bgcolor': theme['card_background'],
            'paper_bgcolor': theme['card_background'],
            'font': {'color': theme['text_color']},
            'margin': {'l': 50, 'r': 20, 't': 50, 'b': 50}
        }
    }
    return fig

def create_map_figure(data, geojson, map_metric, theme, featureidkey='properties.code'):
    if map_metric == 'temp':
        z = data['Température'] - 273.15
        colorscale = 'RdYlBu_r'
        title_map = "Température moyenne (°C)"
        hovertemplate = "<b>%{location}</b><br>Temp. moy: %{z:.1f}°C<extra></extra>"
        color_col = 'Température'
    else:
        z = data['Précipitations dans les 24 dernières heures'].fillna(0)
        colorscale = 'Blues'
        title_map = "Précipitations moyennes (mm)"
        hovertemplate = "<b>%{location}</b><br>Précipitations moy: %{z:.1f} mm<extra></extra>"
        color_col = 'Précipitations'

    fig = px.choropleth_mapbox(
        data,
        geojson=geojson,
        locations=data.columns[0],  # la première colonne devrait être 'region (code)' ou 'department (code)'
        featureidkey=featureidkey,
        color=z,
        color_continuous_scale=colorscale,
        mapbox_style='carto-positron',
        zoom=4.5,
        center={"lat": 46.5, "lon": 2},
        opacity=0.7,
        hover_name=data.columns[0],
    )
    fig.update_traces(hovertemplate=hovertemplate)
    fig.update_layout(
        title={'text': title_map, 'font': {'color': theme['text_color'], 'size': 18}},
        paper_bgcolor=theme['card_background'],
        plot_bgcolor=theme['card_background'],
        font=dict(color=theme['text_color']),
        margin={'r':0,'t':50,'l':0,'b':0}
    )

    fig.update_coloraxes(colorbar=dict(
        title=color_col,
        titlefont=dict(color=theme['text_color']),
        tickfont=dict(color=theme['text_color'])
    ))

    return fig

