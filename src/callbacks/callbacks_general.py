from dash.dependencies import Input, Output
from src.layout.themes import light_theme, dark_theme
from dash import dcc, html

from dash.dependencies import Input, Output
from src.layout.themes import light_theme, dark_theme
from dash import dcc, html

def register_general_callbacks(app):

    @app.callback(
        [
            Output('current-theme', 'data'),
            Output('page-content', 'children'),
        ],
        [
            Input('theme-switch', 'value'),
            Input('current-theme', 'data')
        ]
    )
    def handle_theme_and_update(selected_theme, current_theme):
        from ..dashboard import serve_app_layout

        # Determine if theme needs to be updated
        theme = selected_theme if selected_theme != current_theme else current_theme

        # Adjust map style based on theme
        map_style = 'carto-dark' if theme == 'dark' else 'carto-positron'

        # Generate the updated page content
        page_content = serve_app_layout(theme)

        return theme, page_content
    
