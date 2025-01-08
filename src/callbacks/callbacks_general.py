from dash.dependencies import Input, Output, State
from src.layout.themes import light_theme, dark_theme

def register_general_callbacks(app):
    @app.callback(
        [Output('current-theme', 'data'),  # Stocke le thème actif
         Output('theme-switch', 'className')],  # Met à jour la classe CSS du switch
        [Input('theme-switch', 'n_clicks')],
        [State('current-theme', 'data')]  # Récupère le thème actuel
    )
    def toggle_theme(n_clicks, current_theme):
        if not n_clicks:  # Si aucun clic n'a été effectué, ne rien faire
            return current_theme, "switch"

        # Alterner entre Light et Dark
        if current_theme == 'light':
            return 'dark', "switch active"
        else:
            return 'light', "switch"
    
    @app.callback(
        Output('page-content', 'children'),  # Recharge le layout en fonction du thème
        Input('current-theme', 'data')
    )
    def update_layout(theme_name):
        from ..dashboard import serve_app_layout
        return serve_app_layout(theme_name)