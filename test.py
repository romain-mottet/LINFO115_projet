from csv import DictReader


class Node:
    def __init__(self, source, target, weight, timestamp):
        self.source = source
        self.target = target
        self.weight = weight
        self.timestamp = timestamp
       
       
# iterate over each line as a ordered dictionary and print only few column by column name
# list = []
# with open('dataset.csv', 'r') as read_obj:
#     csv_dict_reader = DictReader(read_obj)
#     for row in csv_dict_reader:
#         print(row['Source'], row['Target'])
        
#         n = Node(row['Source'), row['Target'], row['Weight'], row['Timestamp'] )
#         list.append(n) 
        
# n1 = list.pop

# n2 = Node(1, 2, 3, 4)

print(n2.timestamp)