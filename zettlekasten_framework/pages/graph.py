import dash
from dash import Input, Output, callback, dcc, html

from zettlekasten_framework import utils
from zettlekasten_framework.graph import note_to_graph

dash.register_page(__name__)


@callback(Output("click-dummy-output", "children"), Input("graph", "clickData"))
def clickdata(click_data, *args, **kwargs):
    if click_data is None:
        return None
    clicked_uid = click_data["points"][0]["customdata"]
    return dcc.Location(pathname=f"/note/{clicked_uid}", id=f"/note/{clicked_uid}")


def layout(**kwargs):
    notes = [utils.read_path_to_note(p) for p in utils.get_markdown_pages()]

    return html.Div(
        [
            html.Div(
                note_to_graph(notes, None, "90vw", "100%"),
                className="inverted-shadow"
            ),
        ], className="grid", style={"gridGap": "2rem"}
    )
