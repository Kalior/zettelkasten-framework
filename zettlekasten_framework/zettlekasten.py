import dash
from dash import Dash, html, dcc

if __name__ == '__main__':
    app = Dash(__name__, use_pages=True)

    app.layout = html.Div(
        className='header',
        children=[
            html.H1('Zettlekasten', className="title"),
            html.Div([
                dcc.Link(f"{page['name']}", href=page["relative_path"], className="styled-link")
                for page in dash.page_registry.values()]
            ),
            html.Div(className='content', children=dash.page_container)
        ]
    )

    app.run(debug=True)
