import dash
from dash import Dash, html, dcc

from zettlekasten_framework.utils import get_markdown_pages, path_to_markdown_extract

dash.register_page(__name__)


def layout(**kwargs):
    md_pages = get_markdown_pages()

    return html.Div(
        [path_to_markdown_extract(p) for p in md_pages]
    )
