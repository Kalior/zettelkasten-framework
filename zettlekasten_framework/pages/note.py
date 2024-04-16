import dash
from dash import Dash, html, dcc, Input, Output, callback

from zettlekasten_framework import utils
from zettlekasten_framework.graph import note_to_graph

dash.register_page(__name__, path_template="/note/<note_id>")


def note_to_element(note: utils.Note, is_main: bool = True) -> html.Div:
    category_list = [
        html.Ul([html.Li(c, className='listItem') for c in note.categories], className='listContainer')
    ]

    return html.Div(
        [
            html.Div(category_list),
            html.Div(
                [
                    html.H2(note.header),
                    html.Div(note.uid, className='copy'),
                    dcc.Markdown(note.content)
                ],
            )
        ],
        style={'maxWidth': "30rem"}
    )


def note_to_linked_card(note: utils.Note) -> html.Div:
    category_list = [
        html.Ul([html.Li(c, className='listItem') for c in note.categories], className='listContainer')
    ]
    return html.Div(
        dcc.Link(
            [
                html.Div(category_list),
                html.Div(
                    [
                        html.H2(note.header),
                        dcc.Markdown(note.content)
                    ],
                )
            ],
            href=f"/note/{note.uid}", className='styled-link'),
        style={"padding": "2em", "fontSize": "0.8em", "alignSelf": "start"}, className='shadow'
    )


def layout(note_id=None, **kwargs):
    notes = [utils.read_path_to_note(p) for p in utils.get_markdown_pages()]

    note = next((note for note in notes if note_id == note.uid), None)

    if note is None:
        return '404'

    linked_notes = [n for n in notes if note.uid in n.links or n.uid in note.links]

    return html.Div(
        [
            html.Div(note_to_element(note),
                     style={'marginBottom': "2rem", "gridArea": "1 / 1 / 2 / 3", "fontSize": "1.2em"}),
            html.Div(
                note_to_graph(notes, note),
                style={"gridArea": "1 / 3 / 2 / 5"},
                className='inverted-shadow'
            ),
            *[note_to_linked_card(n) for n in linked_notes]
        ], className='grid', style={"gridGap": "2rem"}
    )
