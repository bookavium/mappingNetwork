
import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
import networkx as nx
import dash_cytoscape as cyto
import base64

# Read data from the CSV file
data = pd.read_csv("partnerships.csv")

# Create a graph using NetworkX
G = nx.from_pandas_edgelist(data, "Company", "Partner")

# Create elements list from the NetworkX graph
elements = []
for edge in G.edges():
    elements.append({"data": {"source": edge[0], "target": edge[1]}})

for node in G.nodes():
    elements.append({"data": {"id": node}})

# Create Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    cyto.Cytoscape(
        id='graph',
        layout={'name': 'concentric'},  # Use "cose" layout instead of "spring"
        style={'width': '100%', 'height': '800px'},
        elements=elements,
        stylesheet=[
            {
                'selector': 'node',
                'style': {
                    'label': 'data(id)',
                    'background-color': 'skyblue',
                    'width': '150px',
                    'height': '50px',
                    'text-valign': 'center',
                    'text-halign': 'center',
                    'border-style': 'solid',
                    'border-width': '2px',
                    'border-color': 'black',
                    'font-size': '12px'
                }
            },
            {
                'selector': 'edge',
                'style': {
                    'width': '2px',
                    'line-color': 'gray'
                }
            }
        ]
    ),
    html.Button("Export as PNG", id="export-png-btn", n_clicks=0),
    html.Button("Export as JPEG", id="export-jpeg-btn", n_clicks=0),
    dcc.Store(id="image-store"),
    html.A("Export", id="export-link", download="graph.png", href="", target="_blank")
])

# Callback to export the graph as PNG or JPEG
@app.callback(
    Output("image-store", "data"),
    Output("export-link", "download"),
    Output("export-link", "href"),
    Input("export-png-btn", "n_clicks"),
    Input("export-jpeg-btn", "n_clicks"),
    State("image-store", "data"),
    prevent_initial_call=True
)
def export_image(png_clicks, jpeg_clicks, current_image):
    ctx = dash.callback_context
    if not current_image:
        current_image = ""

    if ctx.triggered[0]["prop_id"].split(".")[0] == "export-png-btn":
        image_data = cyto.Cytoscape(
            id='png-graph',
            layout={'name': 'cose'},
            style={'width': '100%', 'height': '800px'},
            elements=elements
        ).get_image(as_file=True, format="png")
        download = "graph.png"
    elif ctx.triggered[0]["prop_id"].split(".")[0] == "export-jpeg-btn":
        image_data = cyto.Cytoscape(
            id='jpeg-graph',
            layout={'name': 'cose'},
            style={'width': '100%', 'height': '800px'},
            elements=elements
        ).get_image(as_file=True, format="jpeg")
        download = "graph.jpeg"
    else:
        image_data = current_image
        download = ""

    image_base64 = image_data.split(",")[1]
    href = f"data:image/png;base64,{image_base64}"
    return image_data, download, href

if __name__ == "__main__":
    app.run_server(debug=True)
