import plotly.graph_objects as go
import networkx as nx
import dash
import numpy as np
from dash import Dash, html, dcc, Input, Output, callback

from zettlekasten_framework import utils

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
        style={"padding": "2em"}, className='shadow'
    )


def note_to_graph(note: utils.Note, notes: list[utils.Note]) -> html.Div:
    # Use networkx to position nodes (first, build graph in networkx).

    G = nx.Graph()

    uid_notes = [n.uid for n in notes]
    G.add_nodes_from(uid_notes)
    G.add_edges_from([(n.uid, link) for n in notes for link in n.links if link in uid_notes])

    pos = nx.spring_layout(G, seed=24601)

    edge_x = np.ravel([[pos[e][0] for e in edge] + [None] for edge in G.edges()])
    edge_y = np.ravel([[pos[e][1] for e in edge] + [None] for edge in G.edges()])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_pos = [pos[un] for un in uid_notes]
    node_x, node_y = [list(vs) for vs in zip(*node_pos)]

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        customdata=[n.uid for n in notes],
        marker=dict(
            size=10,
            line_width=2
        )
    )

    node_trace.marker.color = ["#aac4e2" if n.uid == note.uid else "#333" for n in notes]
    node_trace.text = [n.header for n in notes]
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=5, l=5, r=5, t=5),
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )

    graph = dcc.Graph(figure=fig, id='graph', config={
        'displayModeBar': False
    })

    return html.Div(graph, style={"width": "30rem", "height": "30rem"})


@callback(Output('click-dummy-output', 'children'), Input('graph', 'clickData'))
def clickdata(click_data, *args, **kwargs):
    print(click_data)
    if click_data is None:
        return None
    # print(kwargs)
    clicked_uid = click_data['points'][0]['customdata']
    return dcc.Location(pathname=f"/note/{clicked_uid}", id=f"/note/{clicked_uid}")


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
                note_to_graph(note, notes),
                style={"gridArea": "1 / 3 / 2 / 5"},
                className='inverted-shadow'
            ),
            *[note_to_linked_card(n) for n in linked_notes]
        ], className='grid', style={"gridGap": "2rem"}
    )


"""
<Layout>
    <Grid>
        <div style={{ gridArea: "1 / 1 / 2 / 3", fontSize: "1.2em" }}>
            <MainNote note={note} externalLinks={externalLinks} />
        </div>
        <InvertedShadow style={{ gridArea: "1 / 3 / 2 / 5" }}>
            <GraphContainer
                allNotes={relatedNotes}
                onClickNode={onClickNode}
                highlightNode={note}
            />
        </InvertedShadow>
        <LinkedNotes links={allLinks} />
    </Grid>
</Layout>
"""
