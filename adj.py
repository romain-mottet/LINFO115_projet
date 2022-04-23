from code import interact
from copy import deepcopy
from json.tool import main
from csv import DictReader
from time import time
import pandas as pd
import sys

#Global variables
DATASET_FILE = 'datasets/local_bridge/4_lb_2.csv'
cpt_bridge = 0
timer = 0

""" Class used to represent a weighted and directed node in a graph
"""
class Edge:
    def __init__(self, source, target, weight, timestamp):
        self.source = source
        self.target = target
        self.weight = weight
        self.timestamp = timestamp
        
""" Class used to represent a graph, with an adjacency matrix
"""
class Graph:
    def __init__(self, adj=[[]], number_vertices=0, number_edges=0, nodes=[]):
        self.adj = adj
        self.number_vertices = number_vertices
        self.number_edges = number_edges
        self.nodes = nodes

    def print_adj(self):
        print("Vertices | adj[]\n-----------")
        for i, line in enumerate(self.adj):
            print("{} | {}".format(i, str(line)))
            
        # print('\n'.join(' '.join(str(x) for x in row) for row in self.adj))



""" Function which create a Graph object based on 'DATASET_FILE' csv file.
"""
def create_graph():
    g = Graph()
    with open(DATASET_FILE, 'r') as read_obj:
        csv_dict_reader = DictReader(read_obj)
        # Get number of vertices to create adjency matrix
        df = pd.read_csv(DATASET_FILE)
        source_column = df["Source"]
        max_source_value = source_column.max()
        target_column = df["Target"]
        max_target_value = target_column.max()
        max_vertices = max_source_value if max_source_value > max_target_value else max_target_value
        max_vertices += 1
        adj = [[] for x in range(max_vertices)]
        g.number_vertices = int(max_vertices)
        print("number vertices :" + str(g.number_vertices))

        # Get number of edges
        rows = list(csv_dict_reader)
        g.number_edges = len(rows)
        for row in rows:
            s = int(row['Source'])
            t = int(row['Target'])
            adj[s].append(t)
            adj[t].append(s)

        g.adj = adj
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

"""
idée:
in a graph is a local bridge if its endpoints A and B have no friends in common
"""
def count_number_local_bridges(g:Graph):
    cpt = 0
    for v in range(g.number_vertices):
        for w in g.adj[v]:
            if len(intersection(g.adj[v], g.adj[w])) == 0:
                cpt+=1
    return cpt/2


if __name__ == '__main__':
    print("Dataset : '"+DATASET_FILE+"'")
    sys.setrecursionlimit(2000)
    g = create_graph()
    # g.print_adj()
    cpt_components = count_number_components(g)
    print("number_components : "+str(cpt_components))
    
    count_number_bridges(g)
    print("number_bridges : "+str(cpt_bridge))
    
    cpt_local_bridge = count_number_local_bridges(g)
    print("local bridges : {}".format(cpt_local_bridge))

