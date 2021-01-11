from typing import List
from src import GraphInterface
from src.NodeData import NodeData
from src.DiGraph import DiGraph
import math
import heapq
import json
import random as rand
import matplotlib.pyplot as plt


class GraphAlgo:
    """This class represents algorithms functions, save and load to json and plot of a graph."""

    def __init__(self, graph=DiGraph()):
        """
        Constructor
        @param graph: the graph of DiGraph
        """
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

        # If file is empty, return false
        if file_name is None:
            return False
        # Read from json format file and load to graph
        try:
            with open(file_name, 'r') as file:
                graph_dict = json.load(file)
        except FileNotFoundError:
            return False
        graph = DiGraph()
        nodes_list = graph_dict["Nodes"]
        edges_list = graph_dict["Edges"]
        # Loop over the nodes list from the json format
        for node_dict in nodes_list:
            # If pos does not exists in the dictionary of nodes from the nodes list, add only the id
            if "pos" not in node_dict:
                graph.add_node(node_dict["id"])
            # If pos does exists in the dictionary of nodes from the nodes list, add id and pos
            else:
                list_of_pos = node_dict["pos"]
                if type(list_of_pos) is str:
                    x, y, z = list_of_pos.split(',')
                else:
                    x, y, z = list_of_pos
                graph.add_node(node_dict["id"], (float(x), float(y), float(z)))

        # Loop over the edges list from the json format
        for edge_dict in edges_list:
            # add an edge between src, dest and weight from the json format to the graph
            graph.add_edge(edge_dict["src"], edge_dict["dest"], edge_dict["w"])

        # Copy the updated graph to the original graph
        self.graph = graph
        return True

    def save_to_json(self, file_name: str) -> bool:
        """
        Saves the graph in JSON format to a file
        @param file_name: The path to the out file
        @return: True if the save was successful, False o.w.
        """

        # If file is empty, return false
        if file_name is None:
            return False
        all_nodes = self.graph.get_all_v()
        data = {}
        list_of_nodes = []
        # Loop over all the nodes in the graph
        for key, node in all_nodes.items():
            # Put in the dictionary of nodes the id and pos from json format
            if node.pos is not None:
                dict_of_nodes = {"id": key, "pos": node.pos}
            else:
                dict_of_nodes = {"id": key}
            # Put in the list of nodes the dictionary of the nodes that contains the id and pos
            list_of_nodes.append(dict_of_nodes)
        # The dictionary data includes the key that contains Nodes from json format and in value the list of nodes
        data["Nodes"] = list_of_nodes

        list_of_edges = []
        # Loop over all the nodes in the graph
        for src_node in all_nodes:
            out_edges = self.graph.all_out_edges_of_node(src_node)
            # Loop over all the dest and weight of the out edges in the graph
            for dest_node, weight in out_edges.items():
                # Put in the dictionary of edges the src, dest and weight from json format
                dict_of_edges = {"src": src_node, "w": weight, "dest": dest_node}
                # Put in the dictionary of edges the dictionary of the edges that contains the src, dest and weight
                list_of_edges.append(dict_of_edges)
        # The dictionary data includes the key that contains Edges from json format and in value the list of edges
        data["Edges"] = list_of_edges
        # Write the graph to a file in json format
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
        # If id1 or id2 are not in the graph, returns distance of infinity and an empty list
        if id1 not in all_nodes or id2 not in all_nodes:
            return math.inf, []
        # If id1 is equal to id2, returns distance of 0 and a list with one of the node ids
        if id1 is id2:
            return 0, [id2]
        # Using dijkstra algorithm with id1 to receive the distance of the shortest path
        self.dijkstra(id1)
        # If the tag of id2 node is equal to infinity it was not visited, returns distance of infinity and an empty list
        if all_nodes[id2].tag is math.inf:
            return math.inf, []

        # put in the shortest path list the node key of id2 (the dest node)
        node = all_nodes[id2]
        shortest_path = [node.key]
        # Loop while have not reached id1 node key (the src node)
        while node.key is not all_nodes[id1].key:
            # Get the parent node and put the key in the shortest path list
            node = all_nodes.get(node.parent)
            shortest_path.append(node.key)
        # Reverse the shortest path list to get from src to dest, that was inserted backwards
        shortest_path.reverse()
        return all_nodes[id2].tag, shortest_path

    def connected_component(self, id1: int) -> list:
        """
        Finds the Strongly Connected Component(SCC) that node id1 is a part of.
        @param id1: The node id
        @return: The list of nodes in the SCC
        Notes:
        If the graph is None or id1 is not in the graph, the function should return an empty list []
        """
        connected = []
        # If graph is empty, returns an empty list
        if self.graph is None:
            return connected
        all_nodes_original = self.graph.get_all_v()
        # If there are no nodes in the graph or all nodes is empty
        # or id1 does not exists in the graph, returns an empty list
        if all_nodes_original is None or not all_nodes_original or all_nodes_original[id1] is None:
            return connected

        original_list = []
        copy_list = []
        # Using dijkstra on id1 as a starting node to go over the graph
        self.dijkstra(id1)
        original_graph = self.graph
        # Create a new graph as a copy_graph to reverse the edges to find the strongly connected nodes
        copy_graph = DiGraph()
        # Loop over the nodes in the original graph and add the key of the node to the copy_graph
        for key, node in all_nodes_original.items():
            copy_graph.add_node(key)
            # If the node tag is less then infinity, then add the key to the list, because the node was passed though
            if node.tag < math.inf:
                original_list.append(key)
        # Loop over all the nodes in the original graph
        for src in all_nodes_original:
            # Loop over all the out edges of a node to get its dest node and the weight between them
            for dest, weight in original_graph.all_out_edges_of_node(src).items():
                # add an edge backwards from dest to src with the weight between them
                copy_graph.add_edge(dest, src, weight)

        # Copy the copy_graph to the graph to use dijkstra on id1
        self.graph = copy_graph
        self.dijkstra(id1)

        # Loop over the nodes in the copy_graph
        for key, node in copy_graph.get_all_v().items():
            # If the node tag is less then infinity, then add the key of the node to the copy_list
            if node.tag < math.inf:
                copy_list.append(key)

        # Loop over the copy_list
        for key in copy_list:
            # If the key of the copy_list is in the original list, then add the key to the connected list
            if key in original_list:
                connected.append(key)
        # Copy the original graph to the graph
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
        # If graph is empty, returns an empty list
        if self.graph is None:
            return connected_components

        all_nodes = self.graph.get_all_v()
        # If there are no nodes in the graph or all nodes is empty, returns an empty list
        if all_nodes is None or not all_nodes:
            return connected_components

        # Create a set of the nodes that were passed though in the graph
        check_set = set()
        # Loop over all the node keys in the graph
        for key in all_nodes:
            # If the connected_components list is empty or if the key does not exists in the set,
            # then use connected_component function on the key and add it to a list of strongly connected nodes
            if not connected_components or key not in check_set:
                connected_list = self.connected_component(key)
                # If the strongly connected nodes list exists, then add to the final list
                # the strongly connected nodes from the connected_list
                if connected_list:
                    connected_components.append(connected_list)
                    # Change the list to a set, and put in check_set
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
        z_list = []
        pos_dict = {}
        all_nodes = self.graph.get_all_v()
        # Use min_max function to get the min and max of x, y, z
        x_min, y_min, z_min, x_max, y_max, z_max = self.get_min_max()
        # Loop over all the nodes in the graph
        for key, node in all_nodes.items():
            # If the node pos exists, then add the pos of the nodes to x, y, z lists
            if node.pos is not None:
                x, y, z = node.pos
                x_list.append(x)
                y_list.append(y)
                z_list.append(z)
                # Put in the pos dictionary in key the node pos value
                pos_dict[key] = node.pos
            # If the node pos does not exists, use random function  on x, y, z min and max
            else:
                x_val = rand.uniform(x_min, x_max)
                y_val = rand.uniform(y_min, y_max)
                z_val = rand.uniform(z_min, z_max)
                # Add the x, y, z random min and max values to x, y, z lists
                x_list.append(x_val)
                y_list.append(y_val)
                z_list.append(z_val)
                # Put in pos dictionary in key, the x, y, z random min and max values
                pos_dict[key] = x_val, y_val, z_val

        # Create the panel and frame to paint on
        fig, ax = plt.subplots(figsize=(10, 5))
        # Add the nodes from the lists to the plot
        ax.plot(x_list, y_list, ls="", marker="o", color='red')
        # Loop over with iterator on x, y, key from the tuple, and paint the keys over the nodes
        for x, y, key in zip(x_list, y_list, all_nodes):
            ax.annotate(str(key), xy=(x, y), fontsize=15, color='green')

        # Loop over all the node keys in the graph
        for key in all_nodes:
            # Loop over all the out edges of a node to get the dest and the weight between them
            for dest, weight in self.graph.all_out_edges_of_node(key).items():
                # Put in x, y, z src and dest the src key and dest from the pos dictionary
                x_src, y_src, z_src = pos_dict[key]
                x_dest, y_dest, z_dest = pos_dict[dest]
                # Making an arrow between the nodes to point the in edges and out edges
                ax.arrow(x_src, y_src, x_dest - x_src, y_dest - y_src, head_width=0.0003, head_length=0.0003, fc='k',
                         ec='k',
                         length_includes_head=True, width=0.00005)

        # Add a title to the plot and show the graph
        plt.title("Graph Plot")
        plt.show()

    def dijkstra(self, src: int):
        all_nodes = self.graph.get_all_v()
        for key, node in all_nodes.items():
            node.tag = math.inf
            node.parent = 0
        all_nodes.get(src).tag = 0
        all_nodes.get(src).parent = src
        queue = []
        heapq.heappush(queue, all_nodes[src])
        while queue:
            node: NodeData = heapq.heappop(queue)
            edges = self.graph.all_out_edges_of_node(node.key)
            for dest_key, weight in edges.items():
                dest_node = all_nodes.get(dest_key)
                path = node.tag + weight
                if dest_node.tag is math.inf:
                    dest_node.tag = path
                    dest_node.parent = node.key
                    heapq.heappush(queue, dest_node)
                elif path < dest_node.tag:
                    dest_node.tag = path
                    dest_node.parent = node.key
                    heapq.heappush(queue, dest_node)

    def get_min_max(self) -> (float, float, float, float, float, float):
        """
        Get the minimum and maximum of the positions of nodes in the graph.
        If the nodes have a position, the nodes then returns the minimum and maximum of x, y, z positions.
        Otherwise, they will be placed in a random but elegant manner.
        @return: tuple of (float, float, float, float, float, float)
        """
        all_nodes = self.graph.get_all_v()
        x_list = []
        y_list = []
        z_list = []
        # Loop over the nodes in the graph
        for key, node in all_nodes.items():
            # If node pos exists, then add the pos of x, y, z to their lists
            if node.pos is not None:
                x, y, z = node.pos
                x_list.append(x)
                y_list.append(y)
                z_list.append(z)
        # If the lists are empty, returns basic values to min and max of x, y, z
        if not x_list or not y_list or len(x_list) == 1 or len(y_list) == 1:
            return 0, 0, 0, 10, 10, 0
        # Using min and max functions to return the min and max of x,y,z from their lists
        return min(x_list), min(y_list), min(z_list), max(x_list), max(y_list), max(z_list)
