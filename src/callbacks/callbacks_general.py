from dash.dependencies import Input, Output, State

def register_general_callbacks(app):
    # Callback pour basculer entre les thèmes
    @app.callback(
        [Output('current-theme', 'data'),  # Stocke le thème actif
         Output('theme-switch', 'className')],  # Met à jour la classe CSS du switch
        [Input('theme-switch', 'n_clicks')],
        [State('current-theme', 'data')]  # Récupère le thème actuel
    )
    def toggle_theme(n_clicks, current_theme):
        if n_clicks is None:  # Aucun clic effectué (initialisation)
            return current_theme or 'light', "switch"  # Par défaut, thème clair

        # Alterner entre Light et Dark
        if current_theme == 'light':
            return 'dark', "switch active"  # Classe active pour mode sombre
        else:
            return 'light', "switch"  # Classe par défaut pour mode clair

    # Callback pour recharger le contenu de la page en fonction du thème
    @app.callback(
        Output('page-content', 'children'),  # Recharge le layout
        Input('current-theme', 'data')  # Écoute les changements de thème
    )
    def update_layout(theme_name):
        from ..dashboard import serve_app_layout
        return serve_app_layout(theme_name)