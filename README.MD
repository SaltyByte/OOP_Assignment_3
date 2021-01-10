# Assignment Three Information

This repository is split into Three parts.
Part one of the repository is a representation of a directed weighted graph.
The second part is a representation of a weighted directed graph algorithms.

Part One Explanation:
The first part of the repository is located in the src folder and is representing a directed weighted graph.
A directed weighted graph is a graph which each edge has source and destination nodes connected to it.
A valid path must start with source node and end with destination node, can not be otherwise.

Each node contains a value which is unique, it can not have the same id's in one graph.
Each edge is connected with two nodes and contains a weight value.
The weight value is the "distance" or weight the edge has.

Part Two Explanation:
The second part of the repository is located in the src folder and representing a directed weighted graph algorithms.
It contains graph algorithms class which is the algorithms used on the graph.
The main algorithm is Dijkstra's algorithm, which finds the shortest path between two nodes by weights on the graph.

The main functions are: 
shortest_path(returns distance of the sum of weights of the shortest path, and a list of nodes with the shortest path between two nodes based on weights).
connected_component(returns a list of the Strongly Connected Component that node id1 is a part of).
connected_components(returns a list of the lists of all the Strongly Connected Component in the graph).
plot_graph(plots the graph).
save_to_json(Saves the graph associated with the GraphAlgo object in a Json format).
load_from_json(Loads the new graph to the GraphAlgo object).

Part Three Explanation:
Part three contains the comparison of the algorithms in GraphAlgo class.
Comparing the functions connected_component, connected_components and shortest_path from GraphAlgo in python and java,
also comparing those functions in python and networkx library that contains those functions we created.
The comparison is meant to check the difference of the running time of the main algorithms in GraphAlgo
that we wrote in Python to a build library with those functions, and to those functions written in Java language,
This running time difference and the GraphAlgo algorithms written in java, can be found in the wiki in the repository.