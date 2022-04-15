

from json.tool import main
from csv import DictReader


def create_adj_matrix():
    adj = [[]]
    with open('Project dataset.csv', 'r') as read_obj:
        csv_dict_reader = DictReader(read_obj)
        
        rows = list(csv_dict_reader)
        totalrows = len(rows)
        print(totalrows)
        adj = [[] for x in range(totalrows)]
        
        for row in csv_dict_reader:
            print(row['Source'], row['Target'])
            s = int(row['Source'])
            t = int(row['Target'])
            adj[s].append(t)
    return adj
            
    
if __name__ == '__main__':
    adj = create_adj_matrix()
    print(adj[0])
    print(adj[1])
    print(adj[2])
    print(adj[3])
    print(adj[4])
    print(adj[5])
    print(adj[6])