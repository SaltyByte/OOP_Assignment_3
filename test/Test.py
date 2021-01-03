from src.DiGraph import DiGraph


def main():
    graph = DiGraph()
    graph.add_node(0)
    graph.add_node(1)
    graph.add_node(2)
    graph.add_node(3)
    graph.add_node(4)

    graph.add_edge(0, 1, 10)
    graph.add_edge(1, 0, 80)
    graph.add_edge(1, 3, 70)
    graph.add_edge(2, 0, 30)
    graph.add_edge(2, 1, 20)
    graph.add_edge(2, 3, 40)
    graph.add_edge(4, 2, 60)
    graph.add_edge(4, 3, 50)
    graph.add_edge(-1, 2, 100)
    graph.add_edge(5, 3, 200)
    graph.add_edge(7, 8, 300)
    graph.add_edge(0, 0, 400)
    graph.add_edge(0, 1, 500)

    print("MC(13) : " + str(graph.get_mc()) + ", Node size(5) : " + str(graph.v_size()) + ", Edge size(8) : " + str(
        graph.e_size()) + ", Edges out of 0(1{1: 10}) : " + str(graph.all_out_edges_of_node(0)))
    print("Edges in 2(1{4: 60}) : " + str(graph.all_in_edges_of_node(2)))
    print("Edges out of 2(3{0: 30,1: 20,3: 40}) : " + str(graph.all_out_edges_of_node(2)))

    graph.remove_edge(0, 2)
    graph.remove_edge(0, 3)
    graph.remove_edge(2, 0)
    graph.remove_edge(5, 6)
    graph.remove_edge(5, 2)
    graph.remove_edge(2, 5)
    graph.remove_edge(-1, 0)
    graph.remove_edge(0, 0)
    graph.remove_edge(0, 1)
    graph.remove_edge(1, 0)

    print("MC(16) : " + str(graph.get_mc()) + ", Edge size(5) : " + str(
        graph.e_size()) + ", Edges out of 0(0{}) : " + str(
        graph.all_out_edges_of_node(0)))

    print("Edges out of 3(0{}): " + str(graph.all_out_edges_of_node(3)))
    graph.remove_node(3)

    print("MC(20) : " + str(graph.get_mc()) + ", Edge size(2) : " + str(
        graph.e_size()) + ", Nodes in graph(4) : " + str(graph.v_size()))


if __name__ == '__main__':
    main()
