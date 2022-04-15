from json.tool import main
from csv import DictReader
import pandas as pd
import sys


class Node:
    def __init__(self, source, target, weight, timestamp):
        self.source = source
        self.target = target
        self.weight = weight
        self.timestamp = timestamp


class Graph:
    def __init__(self, adj=[[]], number_vertices=0, number_edges=0, nodes=[]):
        self.adj = adj
        self.number_vertices = number_vertices
        self.number_edges = number_edges
        self.nodes = nodes


def create_graph():
    g = Graph()
    with open('Project dataset.csv', 'r') as read_obj:
        csv_dict_reader = DictReader(read_obj)
        # Get number of vertices to create adjency matrix
        df = pd.read_csv('Project dataset.csv')
        source_column = df["Source"]
        max_source_value = source_column.max()
        target_column = df["Target"]
        max_target_value = target_column.max()
        max_vertices = max_source_value if max_source_value > max_target_value else max_target_value
        adj = [[] for x in range(max_vertices)]
        g.number_vertices = int(max_vertices)

        # Get number of edges
        rows = list(csv_dict_reader)
        g.number_edges = len(rows)
        for row in rows:
            s = int(row['Source'])
            t = int(row['Target'])
            adj[s].append(t)

        g.adj = adj
    return g


def count_number_components(g: Graph):
    marked = [False] * g.number_vertices
    cpt = 0

    for vertice in range(g.number_vertices):
        if not marked[vertice]:
            depth_first_search(g, vertice, marked)
            cpt+=1
    return cpt


def depth_first_search(g: Graph, v:int, marked):
    marked[v] = True
    for w in g.adj[v]:
        if not marked[w]:
            depth_first_search(g, w, marked)


def count_number_bridges(adj):
    pass

if __name__ == '__main__':
    sys.setrecursionlimit(2000)
    g = create_graph()
    cpt = count_number_components(g)
    print(cpt)
    # list = [False] * 10
    # print(list)