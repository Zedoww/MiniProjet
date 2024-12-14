from dash.dependencies import Input, Output
from src.layout.themes import light_theme, dark_theme
from dash import dcc, html

def register_general_callbacks(app):

    @app.callback(
        Output('current-theme', 'data'),
        Input('theme-switch', 'value')
    )
    def switch_theme(selected_theme):
        return selected_theme

    @app.callback(
        Output('page-content', 'children'),
        Input('current-theme', 'data')
    )
    def update_page(theme_value):
        from ..dashboard import serve_app_layout
        # On rappelle la fonction pour régénérer la mise en page avec le thème courant
        return serve_app_layout(theme_value)
