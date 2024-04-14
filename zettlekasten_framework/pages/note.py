import dash
from dash import Dash, html, dcc

dash.register_page(__name__,  path_template="/notes/<note_id>")

def layout(note_id=None, **kwargs):
    return html.Div(
f"The user requested report ID: {note_id}."
        )