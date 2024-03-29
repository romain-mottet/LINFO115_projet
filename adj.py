from code import interact
from copy import deepcopy
from json.tool import main
from csv import DictReader
from time import time
from numpy import source, quantile
import pandas as pd
import sys
import statistics

#Global variables
DATASET_FILE = 'Project dataset.csv'
cpt_bridge = 0
timer = 0
median_timestamp = 0

""" Class used to represent a weighted and directed node in a graph
"""
class Edge:
    def __init__(self, target, weight, timestamp):
        self.target = target
        self.weight = weight
        self.timestamp = timestamp
        
    def __str__(self) -> str:
        return "(t:{}, w:{}, ts: {})".format(self.target, self.weight, self.timestamp)
        
""" Class used to represent a graph, with an adjacency matrix
"""
class Graph:
    def __init__(self, adj=[[]], adj_one_link=[[]], number_vertices=0, number_edges=0, edges_adj=[[]]):
        self.adj = adj
        self.adj_one_link = adj_one_link
        self.number_vertices = number_vertices
        self.number_edges = number_edges
        self.edges_adj = edges_adj

    def print_adj(self):
        print("Vertices | adj[]\n-----------")
        for i, line in enumerate(self.adj):
            print("{} | {}".format(i, str(line)))
            
    def print_edges_adj(self):
        print("Vertices | edges_adj[]\n-----------")
        for i, line in enumerate(self.edges_adj):
            line_str = ','.join(str(e) for e in line)
            print("{} | {}".format(i, str(line_str)))
            
        # print('\n'.join(' '.join(str(x) for x in row) for row in self.adj))



""" Function which create a Graph object based on 'DATASET_FILE' csv file.
"""
def create_graph(df, timestamp_limit=float('inf')):
    g = Graph()

    source_column = df["Source"]
    max_source_value = source_column.max()
    target_column = df["Target"]
    max_target_value = target_column.max()
    max_vertices = max_source_value if max_source_value > max_target_value else max_target_value
    max_vertices += 1
    # Adjacency list for neighbour
    adj = [[] for x in range(max_vertices)]
    adj2 = [[] for x in range(max_vertices)]
    # Adjacency edges list for neighbour (with weight and timestamp)
    edges_adj = [[] for x in range(max_vertices)]
    g.number_vertices = int(max_vertices)
    print("number vertices :" + str(g.number_vertices))
    
    timestamp_list = []

    # Get number of edges
    # rows = list(csv_dict_reader)
    g.number_edges = df.shape[0]
    #For each row, complete adacency lists of graph (adj[] and edges_adj[])
    for index, row in df.iterrows():
        s = int(row['Source'])
        t = int(row['Target'])
        if t not in adj2[s] :
            adj2[s].append(t)
        if s not in adj2[t] :
            adj2[t].append(s)
        ts = float(row['Timestamp'])
        #Take only transactions for correct period
        if ts < timestamp_limit:
            adj[s].append(t)
            adj[t].append(s)
            timestamp_list.append(ts)
            w = int(row['Weight'])
            edge = Edge(t, w, ts)
            edge_s = Edge(s, w, ts)
            
            """Take only last transaction between two nodes ("if you find multiple transactions between the same two nodes,
            consider only the oldest one according to the timestamp")"""
            temp = filter(lambda e: e.target != s and e.target != t, edges_adj[s])
            edges_adj[s] = list(temp)

            temp = filter(lambda e: e.target != s and e.target != t, edges_adj[t])
            edges_adj[t] = list(temp)

            edges_adj[s].append(edge)
            edges_adj[t].append(edge_s)

    #Compute median_timestamp
    global median_timestamp
    if len(timestamp_list) != 0:
        median_timestamp = statistics.median(timestamp_list)
        quantiles_list = []
        quantiles_list.append(quantile(timestamp_list, .25))
        quantiles_list.append(quantile(timestamp_list, .5))
        quantiles_list.append(quantile(timestamp_list, .75))
        print("Quantiles : {}".format(quantiles_list))
    
    g.adj = adj
    g.adj_one_link = adj2
    g.edges_adj = edges_adj
    return g



""" Function used to count the number of components in a graph
"""
def count_number_components(g: Graph):
    marked = [False] * g.number_vertices
    cpt = 0

    for vertice in range(g.number_vertices):
        if not marked[vertice]:
            count_components_dfs_stack(g, vertice, marked)
            cpt += 1
    return cpt

""" Stack based DFS function used to count number of components in a graph
"""
def count_components_dfs_stack(g: Graph, root: int, marked):
    marked[root] = True
    stack = []
    stack.append(root)

    while not len(stack) == 0:
        v = stack.pop()
        for w in g.adj[v]:
            if not marked[w]:
                stack.append(w)
                marked[w] = True
                
""" Function used to count number of bridge in a graph
"""
def count_number_bridges(g: Graph):
    visited = [False] * g.number_vertices
    disc = [float("Inf")] * g.number_vertices
    low = [float("Inf")] * g.number_vertices
    parent = [-1] * g.number_vertices
    
    for vertice in range(g.number_vertices):
        if not visited[vertice]:
            count_number_bridges_dfs_recursive(g, vertice, visited, parent, low, disc)
    global cpt_bridge
    return cpt_bridge


""" Recursive function to count the number of bridge in a graph 
"""
def count_number_bridges_dfs_recursive(g, root, visited, parent, low, disc):
    # Mark current node as visited
    visited[root] = True
    # Use globals variables timer and cpt_bridge
    global timer, cpt_bridge
    # Initialize discovery time and low value, and increment timer
    disc[root] = timer
    low[root] = timer
    timer+=1
        
    # Loop through all neighbours of root
    for v in g.adj[root]:
        # If v is not yet visited, recur on it like if it's a child of 'root'
        if not visited[v]:
            parent[v] = root
            count_number_bridges_dfs_recursive(g, v, visited, parent, low, disc)
            
            """ Check if the subtree rooted with v has a connection to
             one of the ancestors of u"""
            low[root] = min(low[root], low[v])


            """ If the lowest vertex reachable from subtree
            under v is below u in DFS tree, then u-v is
            a bridge"""
            if low[v] > disc[root]:
                cpt_bridge+=1
        
        # Update low value of u for parent function calls.
        elif v != parent[root]: 
            low[root] = min(low[root], disc[v])
            

def intersection(a, b):
    return list(set(a) & set(b))

def is_common (list1, list2):
    for i in range (len(list1)):
        for j in range (len(list2)):
            if list1[i] == list2[j]:
                return True
    return False
"""
idée:
in a graph is a local bridge if its endpoints A and B have no friends in common
"""

def count_number_local_bridges(g:Graph):
    cpt = 0
    for num_sommet in range(g.number_vertices):
        for num_link_sommet in range (len(g.adj_one_link[num_sommet])):
            if is_common(g.adj_one_link[num_sommet], g.adj_one_link[g.adj_one_link[num_sommet][num_link_sommet]]):
                    pass
            else :
                cpt += 1
    return cpt/2


def count_nb_triangle(g: Graph):
    cpt = 0
    for v in range(g.number_vertices):
        for w in g.edges_adj[v]:
            for x in g.edges_adj[w.target]:
                if any(nei.target == v for nei in g.edges_adj[x.target]):
                    cpt+=1
    return cpt/6

"""
Input: Pandas dataframe as described above representing a graph
Output: (number_of_different_components, number_of_bridges, number_of_local_bridges)
"""
def basic_properties(dataframe):
    g = create_graph(dataframe)
    cpt_components = count_number_components(g)
    cpt_bridge_var = count_number_bridges(g)
    number_lb = count_number_local_bridges(g)
    return (cpt_components, cpt_bridge_var, number_lb) #replace with your own code


"""
Input: Pandas dataframe as described above representing a graph
Output: Returns the total amount of triadic closures that arrise between the median timestamp of the dataframe until the last timestamp.
Reminder: The triadic closures do not take into account the sign of the edges.
"""
def total_triadic_closures(dataframe):
    g = create_graph(dataframe)
    nb_triangles = count_nb_triangle(g)
    g_median = create_graph(df=dataframe, timestamp_limit=1358386882.63905)
    nb_triangles_median = count_nb_triangle(g_median)
    return nb_triangles-nb_triangles_median

if __name__ == '__main__':
    print("Dataset : '"+DATASET_FILE+"'")
    sys.setrecursionlimit(2000)
    #timestamp_limit=1358386882.63905
    
    with open(DATASET_FILE, 'r') as read_obj:
        csv_dict_reader = DictReader(read_obj)
        # Get number of vertices to create adjency matrix
        df = pd.read_csv(DATASET_FILE)
        print("total triadic : {}".format(total_triadic_closures(df)))
        # print(basic_properties(df))
        # g = create_graph(df)
        # print("timestamp median : {}".format(median_timestamp))
        # # g.print_adj()
        # # g.print_edges_adj()
        # cpt_components = count_number_components(g)
        # print("number_components : "+str(cpt_components))
        
        # cpt_bridge_var = count_number_bridges(g)
        # print("number_bridges : "+str(cpt_bridge_var))

        # number_lb = count_number_local_bridges(g)
        # print("Number of local bridges: {}".format(number_lb))
        
        # nb_triangles = count_nb_triangle(g)
        # print("number triangles : {}".format(nb_triangles))
        
        #timestamp_limit=1358386882.63905
        # g = create_graph(timestamp_limit=1376598564.33713)
        
        # g_median = create_graph(df=df, timestamp_limit=1358386882.63905)
        # nb_triangles_median = count_nb_triangle(g_median)
        # print("number triangles median: {}".format(nb_triangles_median))
        
        # for i in range(3):
        #     print("=====================")
        #     print("adj : "+str(g.adj[i]))
        #     print("edge_adj : "+str(g.edges_adj[i][1]))
        
        # cpt_local_bridge = count_number_local_bridges(g)
        # print("local bridges : {}".format(cpt_local_bridge))

