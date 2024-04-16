import dash
from dash import Dash, dcc, html

app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True)

app.layout = html.Div(
    className="header",
    children=[
        html.H1("Zettlekasten", className="title"),
        html.Div([
            dcc.Link("All notes", href="/all-notes", className="styled-link"),
            dcc.Link("Full graph", href="/graph", className="styled-link")
        ], style={"display": "inline-block"}
                 ),
        html.Div(className="content", children=dash.page_container),
        html.Div(id="click-dummy-output", style={"display": "none"})
    ]
)


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
