import dash
from dash import dcc, html

from zettlekasten_framework import utils
from zettlekasten_framework.graph import note_to_graph

dash.register_page(__name__, path_template="/note/<note_id>")


def note_to_element(note: utils.Note, external_links=None) -> html.Div:
    if external_links is None:
        external_links = []

    if len(external_links) > 0:
        external_links_element = html.Div(
            [
                html.H3("Links"),
                html.Ul([
                    html.Li(html.A(link, href=link, className="styled-link")) for link in external_links
                ])
            ],
            style={"gridArea": "2 / 1 / "}
        )
    else:
        external_links_element = html.Div()

    return html.Div(
        [
            html.Div(utils.get_category_list(note)),
            html.Div(
                [
                    html.H2(note.header),
                    html.Div([
                        html.Div(note.uid, className="copy-content", id="copy-this"), dcc.Clipboard(
                            target_id="copy-this",
                            title="copy",
                            className="copy",
                        ),
                    ]),
                    dcc.Markdown(note.content, mathjax=True)
                ],
            ),
            external_links_element
        ],
        style={"maxWidth": "30rem"}
    )


def note_to_linked_card(note: utils.Note) -> html.Div:
    return html.Div(
        [
            html.Div(utils.get_category_list(note)),
            dcc.Link(
                [

                    html.Div(
                        [
                            html.H2(note.header),
                            dcc.Markdown(note.content, mathjax=True)
                        ],
                    )
                ],
                href=f"/note/{note.uid}", className="styled-link", style={"margin": "0"}),
        ],
        style={"padding": "2em", "fontSize": "0.8em", "alignSelf": "start"}, className="shadow"
    )


def layout(note_id=None, **kwargs):
    notes = [utils.read_path_to_note(p) for p in utils.get_markdown_pages()]
    note_uids = {n.uid for n in notes}

    note = next((note for note in notes if note_id == note.uid), None)

    if note is None:
        return "404"

    linked_notes = [n for n in notes if note.uid in n.links or n.uid in note.links]
    external_links = [link for link in note.links if link not in note_uids]

    return html.Div(
        [
            html.Div(note_to_element(note, external_links=external_links),
                     style={"marginBottom": "2rem", "gridArea": "1 / 1 / 2 / 3", "fontSize": "1.2em"}),
            html.Div(
                note_to_graph(notes, note, width="100%", height="100%"),
                style={"gridArea": "1 / 3 / 2 / 5"},
                className="inverted-shadow"
            ),
            *[note_to_linked_card(n) for n in linked_notes],

        ], className="grid", style={"gridGap": "2rem"}
    )
