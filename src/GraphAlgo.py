from typing import List
import heapq as q
from src import GraphInterface
from src.NodeData import NodeData
from src.DiGraph import DiGraph
import math
import json
import random as rand
import matplotlib.pyplot as plt


class GraphAlgo:
    """This abstract class represents an interface of a graph."""

    def __init__(self, graph=DiGraph()):
        self.graph = graph

    def get_graph(self) -> GraphInterface:
        """
        :return: the directed graph on which the algorithm works on.
        """
        return self.graph

    def load_from_json(self, file_name: str) -> bool:
        """
        Loads a graph from a json file.
        @param file_name: The path to the json file
        @returns True if the loading was successful, False o.w.
        """

        if file_name is None:
            return False
        with open(file_name, 'r') as file:
            graph_dict = json.load(file)
        graph = DiGraph()
        nodes_list = graph_dict["Nodes"]
        edges_list = graph_dict["Edges"]
        for node_dict in nodes_list:
            graph.add_node(node_dict["id"])

        for edge_dict in edges_list:
            graph.add_edge(edge_dict["src"], edge_dict["dest"], edge_dict["w"])
        self.graph = graph
        return True

    def save_to_json(self, file_name: str) -> bool:
        """
        Saves the graph in JSON format to a file
        @param file_name: The path to the out file
        @return: True if the save was successful, False o.w.
        """

        if file_name is None:
            return False
        all_nodes = self.graph.get_all_v()
        data = {}
        list_of_nodes = []
        for key, node in all_nodes.items():
            dict_of_nodes = {"id": key}
            list_of_nodes.append(dict_of_nodes)
        data["Nodes"] = list_of_nodes

        list_of_edges = []
        for src_node in all_nodes:
            out_edges = self.graph.all_out_edges_of_node(src_node)
            for dest_node, weight in out_edges.items():
                dict_of_edges = {"src": src_node, "w": weight, "dest": dest_node}
                list_of_edges.append(dict_of_edges)
        data["Edges"] = list_of_edges
        with open(file_name, 'w') as file:
            json.dump(data, file)
        return True

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm
        @param id1: The start node id
        @param id2: The end node id
        @return: The distance of the path, a list of the nodes ids that the path goes through
        Example:
#      >>> from GraphAlgo import GraphAlgo
#       >>> g_algo = GraphAlgo()
#        >>> g_algo.addNode(0)
#        >>> g_algo.addNode(1)
#        >>> g_algo.addNode(2)
#        >>> g_algo.addEdge(0,1,1)
#        >>> g_algo.addEdge(1,2,4)
#        >>> g_algo.shortestPath(0,1)
#        (1, [0, 1])
#        >>> g_algo.shortestPath(0,2)
#        (5, [0, 1, 2])
        Notes:
        If there is no path between id1 and id2, or one of them dose not exist the function returns (float('inf'),[])
        More info:
        https://en.wikipedia.org/wiki/Dijkstra's_algorithm
        """

        all_nodes = self.graph.get_all_v()
        if id1 not in all_nodes or id2 not in all_nodes:
            return math.inf, []
        if id1 is id2:
            return 0, [id2]
        distance = self.dijkstra(id1, id2)
        if all_nodes[id2].tag is math.inf:
            return math.inf, []

        node = all_nodes[id2]
        shortest_path = [node.key]
        while node.key is not all_nodes[id1].key:
            node = all_nodes.get(node.parent)
            shortest_path.append(node.key)
        shortest_path.reverse()
        return distance, shortest_path

    def connected_component(self, id1: int) -> list:
        """
        Finds the Strongly Connected Component(SCC) that node id1 is a part of.
        @param id1: The node id
        @return: The list of nodes in the SCC
        Notes:
        If the graph is None or id1 is not in the graph, the function should return an empty list []
        """
        connected = []
        if self.graph is None:
            return connected
        all_nodes_original = self.graph.get_all_v()
        if all_nodes_original is None or not all_nodes_original or all_nodes_original[id1] is None:
            return connected

        original_list = []
        copy_list = []
        self.dijkstra(id1)
        original_graph = self.graph
        copy_graph = DiGraph()
        for key, node in all_nodes_original.items():
            copy_graph.add_node(key)
            if node.tag < math.inf:
                original_list.append(key)

        for src in all_nodes_original:
            for dest, weight in original_graph.all_out_edges_of_node(src).items():
                copy_graph.add_edge(dest, src, weight)

        self.graph = copy_graph
        self.dijkstra(id1)

        for key, node in copy_graph.get_all_v().items():
            if node.tag < math.inf:
                copy_list.append(key)

        for key in copy_list:
            if key in original_list:
                connected.append(key)
        self.graph = original_graph
        return connected

    def connected_components(self) -> List[list]:
        """
        Finds all the Strongly Connected Component(SCC) in the graph.
        @return: The list all SCC
        Notes:
        If the graph is None the function should return an empty list []
        """

        connected_components = []
        if self.graph is None:
            return connected_components

        all_nodes = self.graph.get_all_v()
        if all_nodes is None or not all_nodes:
            return connected_components

        check_set = set()
        for key in all_nodes:
            if not connected_components or key not in check_set:
                connected_list = self.connected_component(key)
                if connected_list:
                    connected_components.append(connected_list)
                    check_set |= set(connected_list)
        return connected_components

    def plot_graph(self) -> None:
        """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        @return: None
        """
        x_list = []
        y_list = []
        pos_dict = {}
        all_nodes = self.graph.get_all_v()
        x_min, y_min, x_max, y_max = self.get_min_max()
        for key, node in all_nodes.items():
            if node.pos is not None:
                x, y = node.pos
                x_list.append(x)
                y_list.append(y)
                pos_dict[key] = node.pos
            else:
                x_val = rand.uniform(x_min, x_max)
                y_val = rand.uniform(y_min, y_max)
                x_list.append(x_val)
                y_list.append(y_val)
                pos_dict[key] = x_val, y_val

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(x_list, y_list, ls="", marker="o", color='red')
        for x, y, key in zip(x_list, y_list, all_nodes):
            ax.annotate(str(key), xy=(x, y), fontsize=15, color='green')

        for key in all_nodes:
            for dest, weight in self.graph.all_out_edges_of_node(key).items():
                x_src, y_src = pos_dict[key]
                x_dest, y_dest = pos_dict[dest]
                ax.arrow(x_src, y_src, x_dest - x_src, y_dest - y_src, head_width=0.1, head_length=0.2, fc='k',
                         ec='k',
                         length_includes_head=True, width=0.01)

        plt.title("Graph Plot")
        plt.show()

    def dijkstra(self, src: int, dest: int = None) -> float:
        all_nodes = self.graph.get_all_v()
        for key, node in all_nodes.items():
            node.tag = math.inf
            node.parent = 0
        queue = []
        all_nodes.get(src).tag = 0
        q.heappush(queue, all_nodes.get(src))
        while queue:
            node: NodeData = q.heappop(queue)
            edges = self.graph.all_out_edges_of_node(node.key)
            for dest_key in edges:
                dest_node = all_nodes.get(dest_key)
                if node.tag < dest_node.tag and dest_node not in queue:
                    dest_node.tag = node.tag + edges.get(dest_key)
                    dest_node.parent = node.key
                    q.heappush(queue, dest_node)
                elif node.tag + edges.get(dest_key) < dest_node.tag:
                    dest_node.tag = node.tag + edges.get(dest_key)
                    dest_node.parent = node.key
            if dest is not None and node.key is dest:
                return node.tag

    def get_min_max(self) -> (float, float, float, float):
        all_nodes = self.graph.get_all_v()
        x_list = []
        y_list = []
        for key, node in all_nodes.items():
            if node.pos is not None:
                x, y = node.pos
                x_list.append(x)
                y_list.append(y)
        if not x_list or not y_list:
            return 0, 0, 10, 10
        return min(x_list), min(y_list), max(x_list), max(y_list)
