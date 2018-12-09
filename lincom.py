import networkx as nx
from collections import deque

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


def preprocess_graph(g):
    return max(nx.connected_component_subgraphs(g), key=len)


def get_score(g, node, influenced):
    '''
    returns the INS score
    :param g: NetworkX graph
    :param node: a node in the graph
    :param influenced: set of influenced nodes in the graph
    :return:
    '''
    score = 0
    for neigh in g.neighbors(node):
        if neigh in influenced:
            score += 1
    return score / g.degree(node)

def bf_df(g, start, thresh):
    '''
    Runs the hybrid BF-DF method
    :param g: NetworkX graph object
    :param start: start node
    :param thresh: threshold
    :return: visit times
    '''
    S = []   # stack
    Q = deque()  # queue
    S.append(start)  # add the start node to the stack

    visited = {start}  # set of visited nodes
    influenced = {start}  # set of influenced nodes
    scores = {start: 0}  # dict of INS scores

    broker_roots = {}  # stores the broker that led to discovery
    levels = {}  # stores the level of discovery for community nodes

    latest_broker = None  # stores the latest discovered broker - all the items in the queue are children of the broker
    level = None  # stores the level of the community nodes corresponding to that broker

    while len(S) + len(Q) != 0:  # while both are non-empty
        if len(Q) != 0:  # prioritize the queue over stack
            u = Q.popleft()
            mark = 'Q'  # marker denoting the origin data structure
            level += 1
        else:  # use the stack only if Q is empty
            u = S.pop()
            mark = 'S'
            latest_broker = u  # u is now the root of a new tree
            level = 0

        print(f'({mark}) Processing {u}, degree: {g.degree(u)}, score: {round(scores[u], 3)}')

        for v in g.neighbors(u):  # influence all neighbors of u
            if v not in influenced:
                influenced.add(v)

        for v in g.neighbors(u): # put the neighbors into the stack or the queue depending on their score
            if v in visited:
                continue
            else:
                visited.add(v)

            score = get_score(g, v, influenced)
            scores[v] = round(score, 4)
            if score > thresh:  # the score exceeds the threshold
                Q.append(v)  # put in the queue
                broker_roots[v] = latest_broker
                levels[v] = level + 1
            else:
                S.append(v)  # else put in the stack
    return

def main():
    g = nx.karate_club_graph(); start = 0
    # g = toy_graph(); start = 'N'
    g = preprocess_graph(g)
    bf_df(g, start, 0.66)


if __name__ == '__main__':
    main()


