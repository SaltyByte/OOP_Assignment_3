from src.NodeData import NodeData


class DiGraph:
    """This class represents a directed weighted graph with basic functions."""

    def __init__(self, graph=None):
        """
        Constructor
        @param graph: the graph of DiGraph
        """
        if graph is None:
            self.mc = 0
            self.edge_size = 0
            self.nodes_in_graph = {}
            self.edges_in_node = {}
            self.edges_out_node = {}
        # else:
        #     self.mc = graph.mc
        #     self.edge_size = graph.edge_size

    def v_size(self) -> int:
        """
        Returns the number of vertices in this graph
        @return: The number of vertices in this graph
        """
        return len(self.nodes_in_graph)

    def e_size(self) -> int:
        """
        Returns the number of edges in this graph
        @return: The number of edges in this graph
        """
        return self.edge_size

    def get_all_v(self) -> dict:
        """return a dictionary of all the nodes in the Graph, each node is represented using a pair
         (node_id, node_data)
        """
        return self.nodes_in_graph

    def all_in_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected to (into) node_id ,
        each node is represented using a pair (other_node_id, weight)
         """
        in_dict = self.edges_in_node.get(id1)
        if in_dict is None:
            return {}
        else:
            return in_dict

    def all_out_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected from node_id , each node is represented using a pair
        (other_node_id, weight)
        """
        out_dict = self.edges_out_node.get(id1)
        if out_dict is None:
            return {}
        else:
            return out_dict

    def get_mc(self) -> int:
        """
        Returns the current version of this graph,
        on every change in the graph state - the MC should be increased
        @return: The current version of this graph.
        """
        return self.mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        """
        Adds an edge to the graph.
        @param id1: The start node of the edge
        @param id2: The end node of the edge
        @param weight: The weight of the edge
        @return: True if the edge was added successfully, False o.w.
        Note: If the edge already exists or one of the nodes dose not exists the functions will do nothing
        """
        # If id1 is equal to id2 or if id1, id2 are not in the graph, return false
        if id1 is id2 or id1 not in self.nodes_in_graph or id2 not in self.nodes_in_graph:
            return False
        # If id1 is not in the dictionary of edges_out_node, then create a new inner dictionary with id1
        if id1 not in self.edges_out_node:
            self.edges_out_node[id1] = {}
        # If id2 is not in the dictionary of edges_in_node, then create a new inner dictionary with id2
        if id2 not in self.edges_in_node:
            self.edges_in_node[id2] = {}
        # If id1 is in the dictionary of edges_in_node of id2, then there is an edge between them, return false
        if id1 in self.edges_in_node.get(id2):
            return False
        else:
            # Add the key id1 and value weight as an inner dictionary, to the dictionary of edges_in_node of id2
            self.edges_in_node[id2][id1] = weight
            # Add the key id2 and value weight as an inner dictionary, to the dictionary of edges_out_node of id1
            self.edges_out_node[id1][id2] = weight
            # Increment mode counter and edge size by one, because an edge was added to the graph
            self.mc += 1
            self.edge_size += 1
            return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        """
        Adds a node to the graph.
        @param node_id: The node ID
        @param pos: The position of the node
        @return: True if the node was added successfully, False o.w.
        Note: if the node id already exists the node will not be added
        """
        # If node_id is in the graph, return false
        if node_id in self.nodes_in_graph:
            return False
        else:
            # Add the key node_id and value pos (position of the node) as an inner dictionary,
            # to the dictionary nodes_in_graph and increment mode counter
            self.nodes_in_graph[node_id] = NodeData(node_id, pos)
            self.mc += 1
            return True

    def remove_node(self, node_id: int) -> bool:
        """
        Removes a node from the graph.
        @param node_id: The node ID
        @return: True if the node was removed successfully, False o.w.
        Note: if the node id does not exists the function will do nothing
        """
        # If node_id is not in the graph, return false
        if node_id not in self.nodes_in_graph:
            return False

        in_dict = self.all_in_edges_of_node(node_id)
        out_dict = self.all_out_edges_of_node(node_id)

        if in_dict is not None:
            # Loop over all the src nodes that are directed to node_id,
            # creates a list to be able to remove in loop
            for src in list(in_dict):
                # Removes the edge between src node to node_id
                self.remove_edge(src, node_id)

        if out_dict is not None:
            # Loop over all the dest nodes that node_id is directing on to,
            # creates a list to be able to remove in loop
            for dest in list(self.all_out_edges_of_node(node_id)):
                # Removes the edge between node_id to dest node
                self.remove_edge(node_id, dest)

        # Deletes the node_id from the graph and increment mode counter by one
        del self.nodes_in_graph[node_id]
        self.mc += 1
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        """
        Removes an edge from the graph.
        @param node_id1: The start node of the edge
        @param node_id2: The end node of the edge
        @return: True if the edge was removed successfully, False o.w.
        Note: If such an edge does not exists the function will do nothing
        """
        # If id1 is equal to id2 or if id1, id2 are not in the graph, return false
        if node_id1 is node_id2 or node_id1 not in self.nodes_in_graph or node_id2 not in self.nodes_in_graph:
            return False
        # If node_id1 is not in the dictionary of edges_out_node
        # or if node_id2 is not in the dictionary of edges_in_node, then return false
        if node_id1 not in self.edges_out_node or node_id2 not in self.edges_in_node:
            return False
        # If node_id1 is not in the dictionary of edges_in_node of node_id2,
        # then theres no edge between them, return false
        if node_id1 not in self.edges_in_node.get(node_id2):
            return False
        else:
            # Deletes the key node_id2 from the inner dictionary of edges_out_node of node_id1
            del self.edges_out_node[node_id1][node_id2]
            # Deletes the key node_id1 from the inner dictionary of edges_in_node of node_id2
            del self.edges_in_node[node_id2][node_id1]
            # Increment mode counter by one and decrement edge size by one
            self.mc += 1
            self.edge_size -= 1
            return True
