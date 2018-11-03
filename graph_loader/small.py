import re
import os
import graph_loader.utils as utils


class Small:
    def __init__(self):
        self.data_path = "C:\\SHIFAN\\PythonProgram\\parallel-pll\\datasets\\small.txt"
        self.cache_path = "C:\\SHIFAN\\PythonProgram\\parallel-pll\\cache"
        self.MAX_ID = 10000
        self.num_node, self.num_edge = self.read_num()
        self.dict = self.read_dict()
        self.edges = []
        self.first = []
        self.degree = []
        self.read_graph()
        utils.save_object(self.edges, os.path.join(self.cache_path, "small_edges"))
        utils.save_object(self.first, os.path.join(self.cache_path, "small_first"))
        utils.save_object(self.degree, os.path.join(self.cache_path, "small_degree"))

    def read_num(self):
        data_set = open(self.data_path, "r+")
        num_node = 0
        num_edge = 0

        index = 0
        for line in data_set:
            if index == 2:
                items = re.split(r'[\t\s\n]', line)
                num_node = int(items[2])
                num_edge = int(items[4])
            index += 1

        data_set.close()
        print("%d nodes and %d edges" % (num_node, num_edge))
        return num_node, num_edge

    def read_dict(self):
        data_set = open(self.data_path, "r+")

        index = 0
        d = []
        for line in data_set:
            if index <= 3:
                index += 1
                continue
            items = re.split(r'[\t\s\n]', line)
            # get edges
            from_node_id = int(items[0])
            to_node_id = int(items[1])
            try:
                d.index(from_node_id)
            except ValueError:
                d.append(from_node_id)
            try:
                d.index(to_node_id)
            except ValueError:
                d.append(to_node_id)
            index += 1

        data_set.close()
        return d

    def read_graph(self):
        data_set = open(self.data_path, "r+")

        # init array
        for i in range(self.MAX_ID):
            self.first.append(-1)
            self.degree.append(0)

        index = 0
        for line in data_set:
            if index <= 3:
                index += 1
                continue
            items = re.split(r'[\t\s\n]', line)
            # get edges
            from_node_id = int(items[0])
            to_node_id = int(items[1])
            self.insert_node(from_node_id, to_node_id)
            self.insert_node(to_node_id, from_node_id)
            self.degree[from_node_id] += 1
            self.degree[to_node_id] += 1
            index += 1

        data_set.close()
        print("Load all nodes and edges from data set")

    def insert_node(self, from_node_id, to_node_id):
        last_index = self.first[from_node_id]
        edge_index = len(self.edges)
        self.edges.append([from_node_id, to_node_id, last_index])
        self.first[from_node_id] = edge_index


if __name__ == "__main__":
    small = Small()
