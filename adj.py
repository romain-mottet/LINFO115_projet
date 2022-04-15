from json.tool import main
from csv import DictReader
import pandas as pd


def create_adj_matrix():
    adj = [[]]
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

        rows = list(csv_dict_reader)
        total_rows = len(rows)
        for row in rows:
            s = int(row['Source'])
            t = int(row['Target'])
            adj[s].append(t)
    return adj


def count_number_components(adj: [[]]):
    pass


def count_number_bridges(adj: [[]]):
    pass

# def panda_create_adj_matrix():
#     df = pd.read_csv ('Project dataset.csv')
#     source_column = df["Source"]
#     max_source_value = source_column.max()
#     target_column = df["Target"]
#     max_target_value = target_column.max()
#     max = max_source_value if max_source_value > max_target_value else max_target_value
#     print(max)
            
    
if __name__ == '__main__':
    adj = create_adj_matrix()
    print(adj[0])
    print(adj[1])
    print(adj[2])
    print(adj[3])
    print(adj[4])
    print(adj[5])
    print(adj[6])
    print(len(adj))