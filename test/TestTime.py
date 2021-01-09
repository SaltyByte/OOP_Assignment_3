import networkx as nx
import time
from src.GraphAlgo import GraphAlgo

if __name__ == '__main__':

    algo_graph_ex3 = GraphAlgo()
    algo_graph_ex3.load_from_json("G_10_80_0.json")
    graph_nx = nx.DiGraph()

    for key in algo_graph_ex3.graph.get_all_v():
        graph_nx.add_node(key)

    for src in algo_graph_ex3.graph.get_all_v():
        for dest, weight in algo_graph_ex3.get_graph().all_out_edges_of_node(src).items():
            graph_nx.add_edge(src, dest, weight=weight)

    start = time.time()
    path = nx.dijkstra_path(graph_nx, 0, 5)
    end = time.time()
    print(end - start)
    print(path)

    start = time.time()
    our_path = algo_graph_ex3.shortest_path(0, 5)
    end = time.time()
    print(end - start)
    print(our_path)
