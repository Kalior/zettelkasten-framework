from pathlib import Path

import dash
from dash import Dash, html, dcc

from zettlekasten_framework.utils import get_markdown_pages, read_path_to_note

dash.register_page(__name__)


def path_to_markdown_extract(p: Path) -> html.Div:
    note = read_path_to_note(p)

    category_list = [
        html.Ul([html.Li(c, className='listItem') for c in note.categories], className='listContainer')
    ]

    return html.Div([
        html.Div(category_list),

        dcc.Link(
            html.H3([note.header, html.Span(f" - {note.date}", style={"color": "#bbb"})],
                    style={"marginBottom": "1em"}),
            href=f"/note/{note.uid}", className="styled-link", style={"margin": 0}),

        html.Div(note.excerpt),
    ],
        className='shadow',
        style={"padding": "1em 2em", "margin": "2em 1em"}
    )


def layout(**kwargs):
    md_pages = get_markdown_pages()

    return html.Div(
        [path_to_markdown_extract(p) for p in md_pages]
    )
