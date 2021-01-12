from src.GraphAlgo import GraphAlgo
from src.DiGraph import DiGraph
import unittest


class TestGraphAlgo(unittest.TestCase):
    def setUp(self):
        graph = DiGraph()
        for i in range(1, 15):
            graph.add_node(i)
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
        graph.add_node(15, (9, 5, 0))
        self.graph_algo = GraphAlgo(graph)

        graph2 = DiGraph()
        for i in range(1, 15):
            graph2.add_node(i)

        graph2.add_edge(1, 2, 5)
        graph2.add_edge(2, 3, 5)
        graph2.add_edge(3, 1, 5)
        graph2.add_edge(3, 4, 5)
        graph2.add_edge(4, 5, 5)
        graph2.add_edge(5, 6, 5)
        graph2.add_edge(6, 4, 5)
        graph2.add_edge(6, 8, 5)
        graph2.add_edge(8, 9, 5)
        graph2.add_edge(9, 8, 5)
        graph2.add_edge(9, 10, 5)
        graph2.add_edge(10, 11, 5)
        graph2.add_edge(11, 12, 5)
        graph2.add_edge(12, 13, 5)
        graph2.add_edge(13, 14, 5)
        graph2.add_edge(14, 12, 5)
        self.graph_algo2 = GraphAlgo(graph2)

    def test_load_and_save(self):
        graph_algo2 = GraphAlgo()
        self.assertEqual(False, self.graph_algo.save_to_json(None))
        self.assertEqual(True, self.graph_algo.save_to_json("Testing_Save.json"))
        self.assertEqual(False, graph_algo2.load_from_json(None))
        self.assertEqual(False, graph_algo2.load_from_json("test"))
        self.assertEqual(True, graph_algo2.load_from_json("Testing_Save.json"))
        self.assertEqual(self.graph_algo.get_graph().all_out_edges_of_node(3), graph_algo2.get_graph().all_out_edges_of_node(3))
        self.assertEqual(self.graph_algo.get_graph().get_mc(), graph_algo2.get_graph().get_mc())
        self.assertEqual(self.graph_algo.get_graph().get_all_v().keys(), graph_algo2.get_graph().get_all_v().keys())
        self.assertEqual(self.graph_algo.get_graph().v_size(), graph_algo2.get_graph().v_size())
        self.assertEqual(self.graph_algo.get_graph().e_size(), graph_algo2.get_graph().e_size())
        dict1 = self.graph_algo.get_graph().__dict__
        dict2 = graph_algo2.get_graph().__dict__
        self.assertEqual(dict1, dict2)
        self.assertEqual(self.graph_algo.get_graph().all_in_edges_of_node(4), graph_algo2.get_graph().all_in_edges_of_node(4))
        self.assertNotEqual(self.graph_algo.get_graph(), graph_algo2.get_graph())

    def test_shortest_path(self):
        self.assertEqual((16, [1, 5, 6, 11, 10, 12, 13]), self.graph_algo.shortest_path(1, 13))
        self.assertEqual((16, [9, 14, 8, 3]), self.graph_algo.shortest_path(9, 3))
        self.assertEqual((float('inf'), []), self.graph_algo.shortest_path(2, 1))
        self.assertEqual((2, [7, 4]), self.graph_algo.shortest_path(7, 4))
        self.assertEqual((float('inf'), []), self.graph_algo.shortest_path(0, 0))
        self.assertEqual((0, [10]), self.graph_algo.shortest_path(10, 10))
        self.assertEqual((float('inf'), []), self.graph_algo.shortest_path(7, 0))
        self.assertEqual((float('inf'), []), self.graph_algo.shortest_path(0, 7))
        self.assertEqual((6, [3, 2, 4]), self.graph_algo.shortest_path(3, 4))

    def test_connected_components(self):
        self.assertEqual([[1, 2, 3], [4, 5, 6], [7], [8, 9], [10], [11], [12, 13, 14]], self.graph_algo2.connected_components())
        self.assertEqual([4, 5, 6], self.graph_algo2.connected_component(4))
        self.assertEqual([12, 13, 14], self.graph_algo2.connected_component(12))


if __name__ == '__main__':
    unittest.main()



