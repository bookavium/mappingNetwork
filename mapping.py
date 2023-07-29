import networkx as nx
import matplotlib.pyplot as plt

def map_partner_companies(partnerships):
    # Create an empty undirected graph
    G = nx.Graph()

    # Add partnerships as edges to the graph
    for company1, company2 in partnerships:
        G.add_edge(company1, company2)

    return G

def main():
    # Sample data representing partnerships between companies
    partnerships = [
        ("CompanyA", "CompanyB"),
        ("CompanyA", "CompanyC"),
        ("CompanyB", "CompanyD"),
        ("CompanyC", "CompanyD"),
        ("CompanyD", "CompanyE"),
    ]

    # Generate the partner companies graph
    partner_companies_graph = map_partner_companies(partnerships)

    # Visualize the graph
    pos = nx.spring_layout(partner_companies_graph)
    nx.draw(partner_companies_graph, pos, with_labels=True, node_size=1500, node_color="skyblue", font_size=10, font_weight='bold', alpha=0.8)

    # Show the plot
    plt.title("Partner Companies Network")
    plt.show()


if __name__ == "__main__":
    main()
