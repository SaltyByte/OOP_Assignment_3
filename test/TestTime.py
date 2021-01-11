import networkx as nx
import time
from src.GraphAlgo import GraphAlgo

if __name__ == '__main__':

    algo_graph_ex3 = GraphAlgo()
    algo_graph_ex3.load_from_json("G_100_800_1.json")
    graph_nx = nx.DiGraph()

    for key in algo_graph_ex3.graph.get_all_v():
        graph_nx.add_node(key)

    for src in algo_graph_ex3.graph.get_all_v():
        for dest, weight in algo_graph_ex3.get_graph().all_out_edges_of_node(src).items():
            graph_nx.add_edge(src, dest, weight=weight)

    # sum1 = 0
    # sum2 = 0
    #
    # start = time.time()
    # path = nx.single_source_dijkstra(graph_nx, 1, 5)
    # end = time.time()
    # sum1 += (end - start)
    #
    # start_my = time.time()
    # our_path = algo_graph_ex3.shortest_path(1, 5)
    # end_my = time.time()
    # sum2 += (end_my - start_my)
    #
    # print("Shortest path time of networkX : " + str(sum1))
    # print("Shortest path time of Python : " + str(sum2))



    # sum1 = 0
    # sum2 = 0
    #
    # start = time.time()
    # connected = nx.strongly_connected_components(graph_nx)
    # end = time.time()
    # sum1 += (end - start)
    #
    # start_my = time.time()
    # our_connected = algo_graph_ex3.connected_components()
    # end_my = time.time()
    # sum2 += (end_my - start_my)
    #
    # print("connected components time of networkX : " + str(sum1))
    # print("connected components time of Python : " + str(sum2))

    # sum2 = 0
    # start_my = time.time()
    # our_connect = algo_graph_ex3.connected_component(1)
    # end_my = time.time()
    # sum2 += (end_my - start_my)
    # print("connected component time of Python : " + str(sum2))
