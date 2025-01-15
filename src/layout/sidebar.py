from dash import html, dcc

def sidebar(theme, city_options):
    """
    Sidebar modernisée avec gestion des températures, précipitations, région et ville.
    """
    theme_class = 'sidebar-dark' if theme['name'] == 'dark' else 'sidebar-light'

    return html.Div(
        className=f"sidebar {theme_class}",
        children=[
            # Titre de la sidebar
            html.H2("Menu", className="sidebar-title"),
            
            # Switch Light/Dark Mode
            html.Div(
                className="theme-switch-container",
                children=[
                    html.Span("Light", className="theme-label"),
                    html.Div(
                        id="theme-switch",
                        className=f"switch {'active' if theme['name'] == 'dark' else ''}",
                        children=[html.Div(className="toggle")],
                    ),
                    html.Span("Dark", className="theme-label"),
                ],
            ),

            # Sélection de la ville
            html.Div(
                className="sidebar-section",
                children=[
                    html.Label("Ville :", className="sidebar-label"),
                    dcc.Dropdown(
                        id='city-dropdown',
                        options=city_options,
                        value=city_options[0]['value'] if city_options else None,
                        placeholder="Sélectionnez une ville",
                        className=f"dropdown {'dropdown-dark' if theme['name'] == 'dark' else 'dropdown-light'}",
                        clearable=False,
                    )
                ],
            ),

            # Sélection de la métrique
            html.Div(
                className="sidebar-section",
                children=[
                    html.Label("Sélectionnez une métrique :", className="sidebar-label"),
                    dcc.RadioItems(
                        id='map-metric',
                        options=[
                            {'label': 'Température', 'value': 'temp'},
                            {'label': 'Précipitations', 'value': 'precip'},
                        ],
                        value='temp',
                        className="radio-group",
                        inputClassName="radio-input",
                        labelClassName="radio-label",
                    ),
                ],
            ),

            # Sélection du niveau géographique
            html.Div(
                className="sidebar-section",
                children=[
                    html.Label("Niveau géographique :", className="sidebar-label"),
                    dcc.RadioItems(
                        id='geo-level',
                        options=[
                            {'label': 'Région', 'value': 'region'},
                            {'label': 'Ville', 'value': 'city'},
                        ],
                        value='region',
                        className="radio-group",
                        inputClassName="radio-input",
                        labelClassName="radio-label",
                    ),
                ],
            ),
        ],
    )