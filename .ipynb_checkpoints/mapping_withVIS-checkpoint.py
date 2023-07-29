import networkx as nx
import pandas as pd
from pyvis.network import Network

c1 = "ResilienX"

def map_partner_companies(partnerships):
    # Create an empty undirected graph
    G = nx.Graph()

    # Add partnerships as edges to the graph
    for r1, r2 in partnerships:
        G.add_edge(r1, r2)

    return G


def main():
    # Sample data representing partnerships between companies in a pandas DataFrame
    partnerships_data = {
        "r1": ["Transoft", "RhomanAero"],
        "r2": ["TruWeatherSolution", "ResilienX"],
        "r3": ["Moonware", "EVE"]
    }
    df = pd.DataFrame(partnerships_data)
    print(df)

    # Generate the partner companies graph from pandas DataFrame
    partner_companies_graph = nx.from_pandas_edgelist(df, "r1", "r2", "r3")

    # Visualize the graph using pyvis
    nt = Network(notebook=True)
    nt.from_nx(partner_companies_graph)
    nt.show("partner_companies_graph.html")


if __name__ == "__main__":
    main()
