import networkx as nx


def populate_graph(lines):
    graph = nx.Graph()

    for line in lines:
        component_a, b = line.split(":")

        for component_b in b.strip().split():
            graph.add_edge(component_a, component_b)
            graph.add_edge(component_b, component_a)

    return graph


def remove_edges_cut(graph):
    graph.remove_edges_from(nx.minimum_edge_cut(graph))


def get_product_of_two_groups_length(graph):
    a, b = nx.connected_components(graph)

    return len(a) * len(b)


lines = open("input.txt").read().splitlines()

graph = populate_graph(lines)

remove_edges_cut(graph)

product_of_two_groups_length = get_product_of_two_groups_length(graph)

print(f"Merry Christmas! {product_of_two_groups_length}")
