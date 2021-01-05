from src.GraphAlgo import GraphAlgo
from src.DiGraph import DiGraph


class TestGraphAlgo:
    graph = DiGraph()
    graph.add_node(1)
    graph.add_node(2)
    graph.add_node(3)
    graph.add_node(4)
    graph.add_node(5)
    graph.add_node(6)
    graph.add_node(7)
    graph.add_node(8)
    graph.add_node(9)
    graph.add_node(10)
    graph.add_node(11)
    graph.add_node(12)
    graph.add_node(13)
    graph.add_node(14)

    graph.add_edge(1, 2, 5)
    graph.add_edge(2, 3, 2)
    graph.add_edge(2, 4, 1)
    graph.add_edge(3, 2, 5)
    graph.add_edge(3, 4, 10)
    graph.add_edge(1, 5, 3)
    graph.add_edge(7, 3, 2)
    graph.add_edge(7, 4, 2)
    graph.add_edge(7, 9, 5)
    graph.add_edge(9, 5, 3)
    graph.add_edge(5, 4, 12)
    graph.add_edge(4, 9, 1.2)
    graph.add_edge(9, 14, 7)
    graph.add_edge(14, 8, 3)
    graph.add_edge(8, 3, 6)
    graph.add_edge(5, 12, 17)
    graph.add_edge(12, 13, 2)
    graph.add_edge(13, 5, 9.4)
    graph.add_edge(5, 6, 1)
    graph.add_edge(6, 11, 4)
    graph.add_edge(11, 10, 4)
    graph.add_edge(10, 11, 4)
    graph.add_edge(10, 12, 2)
    graph.add_edge(3, 9, 3.5)

    graph_algo = GraphAlgo(graph)
    print(graph_algo.shortest_path(5, 12))