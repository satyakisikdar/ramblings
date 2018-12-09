import networkx as nx

def preprocess_graph(g):
    return max(nx.connected_component_subgraphs(g), key=len)


def toy_graph():
    g = nx.Graph()
    g.add_edges_from([
        ('A', 'B'), ('A', 'D'), ('A', 'E'),
        ('B', 'C'), ('B', 'E'), ('B', 'F'),
        ('C', 'D'), ('C', 'M'),
        ('D', 'E'),
        ('F', 'G'), ('F', 'H'), ('F', 'I'),
        ('G', 'H'), ('G', 'I'),
        ('H', 'I'),
        ('I', 'L'),
        ('K', 'L'), ('K', 'M'),
        ('L', 'M'), ('L', 'N')
    ])
    return g


def assign_weights(g):
    '''
    assigns weight to every edge
    :param g:
    :return:
    '''
    weight = {}

    for u, v in g.edges():
        gamma_uv = len(set(nx.common_neighbors(g, u, v)))
        w = gamma_uv / (g.degree(u) + g.degree(v) - gamma_uv)  # jaccard -> intersection / union
        weight[(u, v)] = w

    nx.set_edge_attributes(g, weight, 'weight')
    return g

def main():
    # g = toy_graph()
    g = nx.karate_club_graph()
    g = assign_weights(g)
    # print(g.edges(data=True))
    spanner = nx.spanner(g, 7, 'weight')
    print(g.size(), spanner.size())

if __name__ == '__main__':
    main()