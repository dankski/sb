#!/usr/bin/env python3

import os
import re
import networkx as nx
import plotly.graph_objects as go
import pathlib
import subprocess
from bs4 import BeautifulSoup 

# Ordner mit deinen Zetteln
ZETTEL_DIR = os.path.join(pathlib.Path().resolve(), "permanent")

# Regex für Tags in adoc-Dateien
TAG_PATTERN = re.compile(r"^:tags:\s*(.*)", re.IGNORECASE)



def adoc_to_html(adoc_file):
    """
    Converts an AsciiDoc file to HTML and returns the HTML as a string.
    Requires the Ruby-based 'asciidoctor' installed and in PATH.
    """
    result = subprocess.run(
        ["asciidoctor", "--embedded", "-o", "-", str(adoc_file)],  # -o - means output to stdout
        check=True,
        capture_output=True,
        text=True  # return output as string instead of bytes
    )

    html = result.stdout
    soup = BeautifulSoup(html, 'html.parser')
    body = ""

    for line in [line for line in soup.stripped_strings]:
        if line.startswith("Note"):
            body += "<br><b>" + line + "</b><br>"
        elif line.startswith("References"):
            body += "<br><b>" + line + "</b><br>"
        else:
            body += line + "<br>"

    return body


def documents_to_graph(g):

    for filename in os.listdir(ZETTEL_DIR):
        if filename.endswith(".adoc"):
            filepath = os.path.join(ZETTEL_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.readlines()

            doc_id = filename.replace(".adoc", "")

            # Search title (= ...)
            doc_title = None
            for line in content:
                if line.strip().startswith("= "):
                    doc_title = line.strip().lstrip("= ").strip()
                    break

            if not doc_title:
                doc_title = doc_id  # Fallback if title is missing

            doc_preview = adoc_to_html(filepath)

            g.add_node(doc_id, group="zettel", title=doc_title, preview=doc_preview)

            # Extract Tags
            for line in content:
                match = TAG_PATTERN.match(line.strip())
                if match:
                    tags = [t.strip() for t in match.group(1).split(",") if t.strip()]
                    for tag in tags:
                        g.add_node(tag, group="tag")
                        g.add_edge(doc_id, tag)

def generate_graph(g):
    # 3D Layout calculation
    pos = nx.spring_layout(g, dim=3, seed=42)

    # Prepare nodes
    node_x, node_y, node_z = [], [], []
    node_text, node_color, node_preview = [], [], []
    for node, attr in g.nodes(data=True):
        x, y, z = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_z.append(z)
        # Titel for Tooltip/Text
        node_text.append(attr.get("title", node))
        node_color.append("orange" if attr["group"] == "zettel" else "skyblue")
        node_preview.append(attr.get("preview", ""))

    # Prepare edges
    edge_x, edge_y, edge_z = [], [], []
    for u, v in g.edges():
        x0, y0, z0 = pos[u]
        x1, y1, z1 = pos[v]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_z.extend([z0, z1, None])

    # Create plotly figure
    fig = go.Figure()

    # Draw edeges
    fig.add_trace(go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z,
        mode='lines',
        line=dict(color='gray', width=2),
        hoverinfo='none'
    ))

    # Draw nodes
    fig.add_trace(go.Scatter3d(
        x=node_x, y=node_y, z=node_z,
        mode='markers+text',
        text=node_text,
        textposition="top center",
        marker=dict(
            size=10,
            color=node_color,
            opacity=0.9
        ),
        customdata=node_preview,
        hovertemplate="%{text}<br>%{customdata}<extra></extra>"
    ))

    # Layout
    fig.update_layout(
        title="Zettelkasten 3D Graph",
        margin=dict(l=0, r=0, t=30, b=0),
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False)
        ),
        paper_bgcolor="black",   # whole page background
        plot_bgcolor="black",    # 2D plot area background
        font=dict(color="white") # labels in white
    )

    return fig

if __name__ == "__main__":
    G = nx.Graph()
    documents_to_graph(G)
    fig = generate_graph(G)

    # Show in browser
    fig.show()