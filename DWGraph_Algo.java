package api;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Queue;
import java.util.Set;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonDeserializationContext;
import com.google.gson.JsonDeserializer;
import com.google.gson.JsonElement;
import com.google.gson.JsonParseException;

/**
 * This class implements dw_graph_algorithms interface that represents
 * a Directed (positive) Weighted Graph Theory Algorithms including:
 * 0. clone(); (copy)
 * 1. init(graph);
 * 2. isConnected(); // strongly (all ordered pais connected)
 * 3. double shortestPathDist(int src, int dest);
 * 4. List of node_data - shortestPath(int src, int dest);
 * 5. Save(file); // JSON file
 * 6. Load(file); // JSON file
 */
public class DWGraph_Algo implements dw_graph_algorithms {

	private directed_weighted_graph graph;
	// HashMap that holds for each node the information gathered by the Dijkstra algorithm 
	private HashMap<Integer, DijkstraNodeInfo> dijkstraNodeMap;

	/**
	 * Init the graph on which this set of algorithms operates on.
	 * @param  g - the graph needed to be initialized
	 */
	@Override
	public void init(directed_weighted_graph g) {
		this.graph = g;
	}

	/**
	 * Returns the underlying graph of which this class works.
	 * @return directed_weighted_graph - get graph
	 */
	@Override
	public directed_weighted_graph getGraph() {
		return this.graph;
	}

	/**
	 * Compute a deep copy of this weighted graph.
	 * @return directed_weighted_graph - copied graph
	 */
	@Override
	public directed_weighted_graph copy() {
		// If this graph is not null, then copy
		if (this.graph != null) {
			// Using deep copy constructor in DWGraph_DS class
			return new DWGraph_DS(this.graph);

		}
		return null;
	}

	/**
	 * Returns true if and only if there is a valid path from each node to each
	 * other node. NOTE: assume directional graph (all n*(n-1) ordered pairs).
	 * If graph is null or size of nodes in the graph is zero or equals to one, then graph is connected.
	 * This function uses Dijkstra algorithm to gather information about each node
	 * by passing all the nodes in the graph. 
	 * @return boolean - true if graph is strongly connected and false if not connected
	 */
	@Override
	public boolean isConnected() {
		// If this graph is null, then return true,
		// If the graph contains no nodes or contains only one node
		// it means the graph is connected, then return true
		if (graph == null || graph.getV().size() <= 1) {
			return true;
		}
		// Loop over the nodes in the graph
		for (node_data node : graph.getV()) {
			// Use the private function Dijkstra to save all sum weights that were passed through in the HashMap
			Dijkstra(node.getKey(), null);
			// If the amount of nodes in the graph is not equal to the amount in the HashMap, then the graph is not connected
			if (dijkstraNodeMap.size() != graph.nodeSize()) {
				return false;
			}
		}
		return true;
	}

	/**
	 * Returns the length of the shortest path between src to dest,
	 * If no such path -- returns -1.
	 * @param src - start node
	 * @param dest - end (target) node
	 * @return double - the shortest distance between src and dest
	 */
	@Override
	public double shortestPathDist(int src, int dest) {
		//  If the graph is null or src or dest are not in the graph, then return -1
		if (graph == null || graph.getNode(src) == null || graph.getNode(dest) == null){
			return -1;
		}
		//  If src and dest are equal, then return 0 - in this case, the shortest path distance is 0
		if (src == dest) {
			return 0;
		}
		// Using Dijkstra algorithm to find the shortest path according to the weight from src to dest
		Dijkstra(src,dest);
		// If the hashMap does not contain the dest key, then it did not reach the dest node,
		// then return -1
		if (!dijkstraNodeMap.containsKey(dest)) {
			return -1;
		}
		// Returns the sum of the weights from dest node which was set to the shortest distance from src
		return dijkstraNodeMap.get(dest).getSumWeight();
	}

	/**
	 * Returns the shortest path between src to dest - as an ordered List of nodes:
	 * src--n1--n2--...dest
	 * If no such path -- returns null.
	 * @param src - start node
	 * @param dest - end (target) node
	 * @return List of node_data
	 */
	@Override
	public List<node_data> shortestPath(int src, int dest) {
		// If the distance of the shortest path is equal to -1, then there is no path,
		// or if the graph is empty, then return null
		if (shortestPathDist(src, dest) == -1 || graph.getV().isEmpty()) {
			return null;
		}
		// List of nodes of the shortest path
		List<node_data> list = new ArrayList<>();
		//  If src and dest are equal, then return the path with the one node
		if (src == dest) {
			list.add(graph.getNode(src));
			return list;
		}

		// Add the dest node to the list
		node_data destNode = graph.getNode(dest);
		list.add(destNode);
		boolean finished = false;
		int nextNodeIndex = 0;
		// While loop, adds shortest path from dest -> src
		while (!finished) {
			// Get the next node data from the list
			node_data node = list.get(nextNodeIndex);
			// Add the parent to the list and increment the index
			list.add(dijkstraNodeMap.get(node.getKey()).getParent());
			nextNodeIndex++;
			// If reached the src node, then we have all the nodes from dest to src and we can end the loop
			if(list.get(list.size() - 1) == graph.getNode(src)){
				finished = true;
			}
		}
		// Using reverse function from collections, because we want the list to be from src -> dest
		Collections.reverse(list);
		return list;
	}

	/** 
	 * Private function that uses Dijkstra algorithm from src to dest nodes and for each node it saves
	 * the minimum sum weight and its parent calculated from src.
	 * @param src - starting node
	 * @param dest - end (target) node
	 */
	private void Dijkstra(Integer src, Integer dest) {
		dijkstraNodeMap = new HashMap<>();
		// This priority queue is used for the Dijkstra algorithm, its priority is sorted according to the weights
		Queue<node_data> queue = new PriorityQueue<>(new WeightComparator());
		// Add the src node to the queue
		node_data nodeSrc = graph.getNode(src);
		queue.add(nodeSrc);
		// Create DijkstraNodeInfo instance that holds the src (with sum weight of 0) node info and put it in the map
		dijkstraNodeMap.put(src, new DijkstraNodeInfo(0, null));

		// Loop while queue is not empty
		while (!queue.isEmpty()) {
			// Get the node with the lowest weight from the priority queue
			node_data node = queue.poll();
			// Loop over all the edges of this node
			for (edge_data edge : graph.getE(node.getKey())) {
				// Calculate the sum weight by adding to the current weight of the edge to the previous sum weight
				double sumWeight = edge.getWeight() + dijkstraNodeMap.get(node.getKey()).getSumWeight();
				node_data neighbor = graph.getNode(edge.getDest());
				// Check if the neighbor does not exists in the map and the queue
				if (!dijkstraNodeMap.containsKey(neighbor.getKey()) && !queue.contains(neighbor)) {
					// Add the neighbor to the map and to the queue
					dijkstraNodeMap.put(edge.getDest(), new DijkstraNodeInfo(sumWeight, node));
					queue.add(neighbor);
				}
				// If the neighbor already exists in the map and the sumWeight is lower, then replace it in the map
				else if (sumWeight < dijkstraNodeMap.get(edge.getDest()).getSumWeight()) {
					dijkstraNodeMap.put(edge.getDest(), new DijkstraNodeInfo(sumWeight, node));
				}
				// If the current node is equal to dest then return
				if (dest != null && node.getKey() == dest){
					return;
				}
			}
		}
	}

	/**
	 * Saves this weighted (directed) graph to the given
	 * file name - in JSON format.
	 * @param file - the file name (may include a relative path)
	 * @return true - if and only if the file was successfully saved
	 */
	@Override
	public boolean save(String file) {
		// Create JSON string from the graph
		Gson gson = new GsonBuilder().setPrettyPrinting().create();
		String json = gson.toJson(this.graph);	
		try
		{
			// Write graph object which is in JSON format
			PrintWriter pw = new PrintWriter(new File(file));
			pw.write(json);
			// Close PrintWriter
			pw.close();
		} 
		catch (FileNotFoundException e) {
			e.printStackTrace();
			return false;
		}
		return true;
	}

	/**
	 * This method load a graph to this graph algorithm.
	 * if the file was successfully loaded - the underlying graph
	 * of this class will be changed (to the loaded one), in case the
	 * graph was not loaded the original graph should remain "as is".
	 * @param file - file name of JSON file
	 * @return true - if and only if the graph was successfully loaded
	 */
	@Override
	public boolean load(String file) {
		try 
		{
			// Create GsonBuilder
			GsonBuilder gsonBuilder = new GsonBuilder();
			gsonBuilder.setLenient();
			// Register interfaces to classes so the GSON builder can use its constructors
			gsonBuilder.registerTypeAdapter(node_data.class, new InterfaceAdapter<>(NodeData.class));
			gsonBuilder.registerTypeAdapter(edge_data.class, new InterfaceAdapter<>(EdgeData.class));
			// Create Gson from GsonBuilder
			Gson gson = gsonBuilder.create();
			// Read from JSON string to create the graph
			FileReader reader = new FileReader(file);
			this.graph = gson.fromJson(reader, DWGraph_DS.class);
			// Close FileReader
			reader.close();
		} 
		catch (IOException e) {
			e.printStackTrace();
			return false;
		}
		return true;
	}

	/**
	 * Finds the Strongly Connected Component(SCC) that node id1 is a part of.
	 * @param id1: The node id
	 * @return: The list of nodes in the SCC
	 * Notes:
	 * If the graph is None or id1 is not in the graph, the function should return an empty list []
	 */
	public List<Integer> connected_component(int id1) {
		List<Integer> connected = new ArrayList<>();
		// If graph is empty, returns an empty list
		if (graph == null) {
			return connected;
		}  		
		Collection<node_data> allNodesOriginal = graph.getV();
		// If there are no nodes in the graph or all nodes is empty
		// or id1 does not exists in the graph, returns an empty list
		if (allNodesOriginal == null || allNodesOriginal.isEmpty() || graph.getNode(id1) == null) {
			return connected;
		}

		List<Integer> originalList = new ArrayList<>();
		List<Integer> copyList = new ArrayList<>();
		// Using dijkstra on id1 as a starting node to go over the graph
		Dijkstra(id1, null);
		directed_weighted_graph originalGraph = this.graph;
		// Create a new graph as a copy_graph to reverse the edges to find the strongly connected nodes
		directed_weighted_graph copyGraph = new DWGraph_DS();
		// Loop over the nodes in the original graph and add the key of the node to the copy_graph
		for (node_data node: allNodesOriginal) {
			copyGraph.addNode(node);
			// If the node sumWeight is not null, then add the key to the list, because the node was passed though
			if (node != null && dijkstraNodeMap.get(node.getKey()) != null && dijkstraNodeMap.get(node.getKey()).getSumWeight() != null) {
				originalList.add(node.getKey());
			}
		}
		// Loop over all the nodes in the original graph
		for (node_data node: allNodesOriginal) {
			// Loop over all the out edges of a node to get its dest node and the weight between them
			for (edge_data edge: graph.getE(node.getKey())) {
				// add an edge backwards from dest to src with the weight between them
				copyGraph.connect(edge.getDest(), edge.getSrc(), edge.getWeight());
			}
		}
		// Copy the copy_graph to the graph to use dijkstra on id1
		this.graph = copyGraph;
		Dijkstra(id1, null);
		// Loop over the nodes in the copy_graph
		for (node_data node: copyGraph.getV()) {
			// If the node sumWeight is not null, then add the key of the node to the copy_list
			if (node != null && dijkstraNodeMap.get(node.getKey()) != null && dijkstraNodeMap.get(node.getKey()).getSumWeight() != null) {
				copyList.add(node.getKey());
			}
		}
		// Loop over the copy_list
		for (int key: copyList) {
			// If the key of the copy_list is in the original list, then add the key to the connected list
			if (originalList.contains(key)) {
				connected.add(key);
			}
		}
		// Copy the original graph to the graph
		this.graph = originalGraph;
		return connected;
	}
	
	/**
    * Finds all the Strongly Connected Component(SCC) in the graph.
    * @return: The list all SCC
    * Notes:
    * If the graph is None the function should return an empty list []
    */
    public List<List<Integer>> connected_components() {

        List<List<Integer>> connectedComponents = new ArrayList<>();
        // If graph is empty, returns an empty list
        if (graph == null) {
            return connectedComponents;
        }

        Collection<node_data> allNodes = this.graph.getV();
        // If there are no nodes in the graph or all nodes is empty, returns an empty list
        if (allNodes == null || allNodes.isEmpty()) {
        	return connectedComponents;
        }
        // Create a set of the nodes that were passed though in the graph
        Set<Integer> checkSet = new HashSet<>();
        // Loop over all the nodes in the graph
        for (node_data node: allNodes) {
        	// If the connected_components list is empty or if the key does not exists in the set,
            // then use connected_component function on the key and add it to a list of strongly connected nodes
        	if (connectedComponents.isEmpty() || !checkSet.contains(node.getKey())) {
        		List<Integer> connectedList = this.connected_component(node.getKey());
        		// If the strongly connected nodes list exists, then add to the final list
                // the strongly connected nodes from the connected_list
        		if (!connectedList.isEmpty()) {
        			connectedComponents.add(connectedList);
                    // Change the list to a set, and put in check_set
                    checkSet.addAll(connectedList);
        		}
        	}
        }
        return connectedComponents;  
    }

	/**
	 * This private class implements JsonDeserializer interface with generic type,
	 * This is needed for the GsonBuilder to be able to deserialize interfaces.
	 */
	private class InterfaceAdapter<T> implements JsonDeserializer<T> {

		// Class that implements the interface
		private Class<T> targetClass;

		// Constructor
		public InterfaceAdapter(Class<T> targetClass) {
			this.targetClass = targetClass;
		}

		// Override the deserialize method, so that the targetClass will be used to as a constructor for the interface
		@Override
		public T deserialize(JsonElement json, Type typeOfT, JsonDeserializationContext context) throws JsonParseException {
			return context.deserialize(json.getAsJsonObject(), targetClass);
		}
	}

	/**
	 * This class implements Comparator interface and compare weights
	 * that are used to save the distance from src.
	 * This is needed for the priority queue.
	 */
	private class WeightComparator implements Comparator<node_data> {

		/**
		 * Overrides compare method by tag (weight), if node1 is greater than node2 return 1,
		 * if node1 is less than node2 return -1, else return 0.
		 * used in the priorityQueue.
		 * @param node1 - node1 to compare
		 * @param node2 - node2 to compare
		 * @return If node1 is greater than node2 return 1, if node1 is less than node2 return -1, else return 0.
		 */
		@Override
		public int compare(node_data node1, node_data node2) {
			double sum1 = dijkstraNodeMap.get(node1.getKey()).getSumWeight();
			double sum2 = dijkstraNodeMap.get(node2.getKey()).getSumWeight();
			if (sum1 > sum2) {
				return 1;
			} else if (sum1 <sum2) {
				return -1;
			}
			return 0;
		}
	}

	/**
	 * This private class represents node information gathered by the Dijkstra algorithm.
	 */
	private class DijkstraNodeInfo {
		// The sum weight from src to this node
		private Double sumWeight;
		// The parent of this node from src
		private node_data parent;

		// Constructor
		public DijkstraNodeInfo(double sumWeight, node_data parent) {
			this.parent = parent;
			this.sumWeight = sumWeight;
		}

		public Double getSumWeight(){
			return sumWeight;
		}

		public node_data getParent() {
			return parent;
		}
	}
	
	public static void main(String[] args) {
		directed_weighted_graph g = new DWGraph_DS();
		DWGraph_Algo ga = new DWGraph_Algo();

		for (int i = 0; i < 9; i++) {
			node_data n = new NodeData(i);
			g.addNode(n);
		}
		g.connect(0, 1, 2);
		g.connect(1, 4, 5);
		g.connect(1, 2, 3.5);
		g.connect(2, 3, 7.1);
		g.connect(2, 4, 9.3);
		g.connect(3, 7, 2);
		g.connect(4, 6, 1);
		g.connect(4, 1, 3);
		g.connect(5, 6, 8);
		g.connect(6, 8, 10);
		g.connect(7, 3, 1);
		g.connect(8, 5, 7.5);
		
		ga.init(g);
		System.out.println(ga.connected_component(4));
		System.out.println(ga.connected_components());
	}
}