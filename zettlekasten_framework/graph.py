import networkx as nx
import numpy as np
import plotly.graph_objects as go
from dash import dcc, html

from zettlekasten_framework import utils


def note_to_graph(notes: list[utils.Note], note: utils.Note | None = None, width: str = "30rem",
                  height: str = "30rem") -> html.Div:
    if note is None:
        note = utils.Note(None, None, None, [], None, [])

    graph = nx.Graph()

    uid_notes = [n.uid for n in notes]
    graph.add_nodes_from(uid_notes)
    graph.add_edges_from([(n.uid, link) for n in notes for link in n.links if link in uid_notes])

    pos = nx.spring_layout(graph, seed=24601)

    edge_x = np.ravel([[pos[e][0] for e in edge] + [None] for edge in graph.edges()])
    edge_y = np.ravel([[pos[e][1] for e in edge] + [None] for edge in graph.edges()])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line={"width": 0.5, "color": "#888"},
        hoverinfo="none",
        mode="lines")

    node_pos = [pos[un] for un in uid_notes]
    node_x, node_y = (list(vs) for vs in zip(*node_pos))

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode="markers",
        hoverinfo="text",
        customdata=[n.uid for n in notes],
        marker={
            "size": 10,
            "line_width": 2
        }
    )

    node_trace.marker.color = ["#aac4e2" if n.uid == note.uid else "#333" for n in notes]
    node_trace.text = [n.header for n in notes]

    if note.header is not None:
        x_range = np.max(node_x) - np.min(node_x)
        y_range = np.max(node_y) - np.min(node_y)
        note_x, note_y = pos[note.uid]
        xlim = [note_x - x_range / 5, note_x + x_range / 5]
        ylim = [note_y - y_range / 5, note_y + y_range / 5]
    else:
        xlim = None
        ylim = None

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode="closest",
                        margin={"b": 5, "l": 5, "r": 5, "t": 5},
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)",
                        xaxis={"showgrid": False, "zeroline": False, "showticklabels": False, "range": xlim},
                        yaxis={"showgrid": False, "zeroline": False, "showticklabels": False, "range": ylim})
                    )

    return html.Div(dcc.Graph(figure=fig, id="graph", config={
        "displayModeBar": False
    }), style={"width": width, "height": height})
