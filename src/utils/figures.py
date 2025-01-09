import plotly.express as px
import plotly.graph_objects as go

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

def create_temperature_histogram(filtered_data, theme):
    temperatures = filtered_data['Température maximale sur 24 heures'] - 273.15

    fig = px.histogram(
        temperatures,
        x=temperatures,
        nbins=30,
        title='Distribution des Températures Maximales sur l\'Année',
        labels={'x': 'Température (°C)', 'y': 'Fréquence'},
        template='plotly_dark' if theme['name'] == 'dark' else 'plotly_white',
        color_discrete_sequence=['#4A90E2']
    )

    fig.update_layout(
        title={
            'text': 'Fréquence des Températures Max',
            'font': {'color': theme['text_color'], 'size': 16},
            'x': 0.5
        },
        xaxis={'title': 'Température (°C)', 'color': theme['text_color'], 'gridcolor': theme['grid_color']},
        yaxis={'title': 'Fréquence', 'color': theme['text_color'], 'gridcolor': theme['grid_color']},
        plot_bgcolor=theme['card_background'],
        paper_bgcolor=theme['card_background'],
        font={'color': theme['text_color']},
        margin={'l': 50, 'r': 20, 't': 50, 'b': 50}
    )

    return fig


def create_map_figure(
    data,
    geojson,
    map_metric,
    theme,
    featureidkey='properties.code',
    geo_level='region',
    selected_city=None
):
    """
    Crée une carte en fonction des régions ou des villes.
    """

    # Style de la carte
    mapbox_style = 'carto-darkmatter' if theme['name'] == 'dark' else 'carto-positron'

    # Gestion des métriques pour l'échelle de couleur
    if map_metric == 'temp':
        color_label = "Température moyenne (°C)"
        data['val_metric'] = data['Température'] - 273.15  # Conversion en °C
    else:
        color_label = "Précipitations moyennes (mm)"
        data['val_metric'] = data['Précipitations dans les 24 dernières heures'].fillna(0)

    # Mode Région
    if geo_level == 'region':
        fig = px.choropleth_mapbox(
            data,
            geojson=geojson,
            locations=data.columns[0],  # Colonne des régions (ex: 'region (code)')
            featureidkey=featureidkey,
            color='val_metric',  # Utiliser la colonne calculée
            color_continuous_scale='RdYlBu_r' if map_metric == 'temp' else 'Blues',
            mapbox_style=mapbox_style,
            zoom=4.5,
            center={"lat": 46.5, "lon": 2},
            opacity=0.7,
            hover_name=data.columns[0],
            custom_data=['val_metric']  # Référence à la colonne calculée
        )
        fig.update_traces(
            hovertemplate="<b>%{location}</b><br>Métrique: %{customdata[0]:.2f}<extra></extra>"
        )
        fig.update_layout(
            title={
                'text': color_label,
                'font': {'color': theme['text_color'], 'size': 18},
                'x': 0.5
            },
            paper_bgcolor=theme['card_background'],
            plot_bgcolor=theme['card_background'],
            font=dict(color=theme['text_color']),
            margin={'r': 0, 't': 50, 'l': 0, 'b': 0},
        )
        fig.update_coloraxes(colorbar=dict(
            title=color_label,
            titlefont=dict(color=theme['text_color']),
            tickfont=dict(color=theme['text_color'])
        ))
    else:
        # Mode Ville
        grouped = data.groupby('communes (name)', as_index=False).agg({
            'Latitude': 'mean',
            'Longitude': 'mean',
            'Température': 'mean',
            'Précipitations dans les 24 dernières heures': 'mean'
        })

        if map_metric == 'temp':
            grouped['val_metric'] = grouped['Température'] - 273.15
        else:
            grouped['val_metric'] = grouped['Précipitations dans les 24 dernières heures']

        # Remplir les NaN dans la taille pour éviter les erreurs
        grouped['val_metric'] = grouped['val_metric'].fillna(0)
        grouped['size'] = grouped['val_metric'].apply(lambda x: max(10, min(20, x)))  # Limiter la taille
        grouped['opacity'] = 0.9  # Rendre les marqueurs visibles

        fig = go.Figure()

        # Tracer les marqueurs
        fig.add_trace(
            go.Scattermapbox(
                lat=grouped['Latitude'],
                lon=grouped['Longitude'],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=grouped['size'],
                    color=grouped['val_metric'],
                    colorscale='RdYlBu_r' if map_metric == 'temp' else 'Blues',
                    opacity=grouped['opacity'],
                    showscale=True,
                    colorbar=dict(
                        title=color_label,
                        titlefont=dict(color=theme['text_color']),
                        tickfont=dict(color=theme['text_color'])
                    )
                ),
                text=grouped['communes (name)'],  # Afficher le nom de la ville
                customdata=grouped['communes (name)'],  # Nom des villes pour hover
                hovertemplate="<b>%{text}</b><br>Métrique: %{marker.color:.2f}<extra></extra>",
                showlegend=False 
            )
        )

        # Mettre en avant la ville sélectionnée
        if selected_city in grouped['communes (name)'].values:
            selected_row = grouped[grouped['communes (name)'] == selected_city]
            fig.add_trace(
                go.Scattermapbox(
                    lat=selected_row['Latitude'],
                    lon=selected_row['Longitude'],
                    mode='markers',
                    marker=go.scattermapbox.Marker(
                        size=25,
                        color="red",
                        opacity=1
                    ),
                    hoverinfo="skip",
                    showlegend=False
                )
            )

        fig.update_layout(
            mapbox_style=mapbox_style,
            mapbox_zoom=5,
            mapbox_center={"lat": 46.5, "lon": 2},
            margin={'r': 0, 't': 50, 'l': 0, 'b': 0},
            paper_bgcolor=theme['card_background'],
            font=dict(color=theme['text_color']),
        )

    return fig