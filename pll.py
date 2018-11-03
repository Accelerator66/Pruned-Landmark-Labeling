from graph_loader.loader import Loader
import graph_loader.utils as utils
import os
from queue import Queue
import copy


class PLL:
    def __init__(self, data_set_name):
        self.cache_path = "C:\\SHIFAN\\PythonProgram\\parallel-pll\\cache"
        self.name = data_set_name
        self.graph = Loader(data_set_name)
        self.MAX_DIST = self.graph.db.num_edge * 10
        self.order_dict = self.graph.create_sorted_dict()
        self.labels = []
        for i in range(self.graph.db.MAX_ID):
            self.labels.append([])

    def index_stage(self, preload=True):
        path = os.path.join(self.cache_path, self.name + "labels")
        if os.path.exists(path) and preload:
            self.labels = utils.load_object(path)
            return
        for i in range(len(self.order_dict)):
            label1 = self.num_label()
            self.pruned_bfs(i)
            label2 = self.num_label()
            print("Indexes: %d, Node: %d, add label: %d" % (i, self.order_dict[i], label2 - label1))
        utils.save_object(self.labels, path)

    def pruned_bfs(self, index):
        vertex = self.order_dict[index]
        distance = []
        temp_labels = copy.deepcopy(self.labels)
        for i in range(self.graph.db.MAX_ID):
            if i == vertex:
                distance.append(0)
            else:
                distance.append(self.MAX_DIST)
        q = Queue()
        q.put(vertex)
        while q.empty() is False:
            u = q.get()
            if self.query(vertex, u, labels=temp_labels) <= distance[u]:
                continue
            self.labels[u].append([index, distance[u]])
            neighbor = self.graph.db.first[u]
            while neighbor != -1:
                edge = self.graph.db.edges[neighbor]
                if distance[edge[1]] == self.MAX_DIST:
                    distance[edge[1]] = distance[u] + 1
                    q.put(edge[1])
                neighbor = edge[2]

    def query(self, from_id, to_id, labels=None):
        if labels is None:
            labels = self.labels
        distance = self.MAX_DIST
        from_len = len(labels[from_id])
        to_len = len(labels[to_id])
        if from_len == 0 or to_len == 0:
            return distance
        from_point = 0
        to_point = 0
        while from_point < from_len and to_point < to_len:
            if labels[from_id][from_point][0] == labels[to_id][to_point][0]:
                distance = min(distance, labels[from_id][from_point][1] + labels[to_id][to_point][1])
                from_point += 1
                to_point += 1
            elif labels[from_id][from_point][0] < labels[to_id][to_point][0]:
                from_point += 1
            else:
                to_point += 1
        return distance

    def num_label(self):
        num = 0
        for label in self.labels:
            num += len(label)
        return num


if __name__ == "__main__":
    pll = PLL("small")
    pll.index_stage(preload=False)
    print(pll.query(1, 5))
    print(pll.query(2, 5))
    print(pll.query(5, 5))
    print(pll.query(4, 2))
    print(pll.query(3, 1))
    print(pll.query(1, 3))
    print(pll.query(1, 1))
