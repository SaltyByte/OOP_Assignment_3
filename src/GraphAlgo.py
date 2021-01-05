from typing import List
import heapq as q
from src import GraphInterface
from src.NodeData import NodeData
from src.DiGraph import DiGraph


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

    def save_to_json(self, file_name: str) -> bool:
        """
        Saves the graph in JSON format to a file
        @param file_name: The path to the out file
        @return: True if the save was successful, False o.w.
        """

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

        # make full false so when we reach dest we quit
        all_nodes = self.graph.get_all_v()
        if id1 not in all_nodes or id2 not in all_nodes:
            return float('inf'), []
        if id1 is id2:
            return 0, [id2]
        distance, path = self.dijkstra(id1, id2)
        if all_nodes[id2].tag is float('inf'):
            return float('inf'), []
        return distance, path


    def connected_component(self, id1: int) -> list:
        """
        Finds the Strongly Connected Component(SCC) that node id1 is a part of.
        @param id1: The node id
        @return: The list of nodes in the SCC
        Notes:
        If the graph is None or id1 is not in the graph, the function should return an empty list []
        """
        # make this function run one time by making the full true
        connected = []
        all_nodes = self.graph.get_all_v()
        for node in all_nodes:
            self.dijkstra()


    def connected_components(self) -> List[list]:
        """
        Finds all the Strongly Connected Component(SCC) in the graph.
        @return: The list all SCC
        Notes:
        If the graph is None the function should return an empty list []
        """

    def plot_graph(self) -> None:
        """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        @return: None
        """

    def dijkstra(self, src: int, dest: int = None, full: bool = False) -> (float, list):
        all_nodes = self.graph.get_all_v()
        for key, node in all_nodes.items():
            node.tag = float('inf')
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
            if node.key is dest and not full:
                parent = node.parent
                shortest_path = [node]
                while parent is not all_nodes[src].key:
                    shortest_path.append(all_nodes.get(parent))
                    parent = all_nodes.get(parent).parent
                shortest_path.append(all_nodes.get(parent))
                shortest_path.reverse()
                return node.tag, shortest_path
                # move list making to shortest path to reduce run time
