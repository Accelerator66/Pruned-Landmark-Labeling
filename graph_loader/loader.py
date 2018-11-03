from graph_loader.wiki_vote import WikiVote
from graph_loader.small import Small


class Loader:
    def __init__(self, data_set):
        self.db = None
        if data_set == "wiki-vote":
            self.db = WikiVote()
        elif data_set == "small":
            self.db = Small()

    def create_sorted_dict(self):
        return sorted(range(len(self.db.degree)),
                      key=lambda k: self.db.degree[k],
                      reverse=True)[:self.db.num_node]

    def create_random_dict(self):
        return self.db.dict


if __name__ == "__main__":
    loader = Loader("wiki-vote")
    d = loader.create_sorted_dict()
    dd = loader.db.dict
    print(d)
