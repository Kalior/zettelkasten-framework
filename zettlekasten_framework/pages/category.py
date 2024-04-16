import dash
from dash import Dash, html, dcc, Input, Output, callback

from zettlekasten_framework import utils

dash.register_page(__name__, path_template="/category/<category_id>")


def note_to_category_card(note: utils.Note) -> html.Div:
    return html.Div(
        [
            html.Div(utils.get_category_list(note)),
            dcc.Link(
                [

                    html.Div(
                        [
                            html.H2(note.header),
                            dcc.Markdown(note.content)
                        ],
                    )
                ],
                href=f"/note/{note.uid}", className='styled-link', style={"margin": "0"}),
        ],
        style={"padding": "2em", "fontSize": "0.8em", "alignSelf": "start"}, className='shadow'
    )

def layout(category_id=None, **kwargs):
    print(kwargs)
    notes = [utils.read_path_to_note(p) for p in utils.get_markdown_pages()]

    if category_id is None:
        return '404'

    category_notes = [n for n in notes if category_id in n.categories]

    return html.Div(
        [
            *[note_to_category_card(n) for n in category_notes]
        ], className='grid', style={"gridGap": "2rem"}
    )
