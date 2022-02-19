from typing import List


class Graph:
    def __init__(self, label: List[int]):
        self.n = len(label)
        self.label = label
        self.adj = [[] for _ in range(0, self.n)]

    def add_edge(self, u: int, v: int):
        assert 0 <= u < self.n
        assert 0 <= v < self.n
        self.adj[u].append(v)


def construct_graph_from_assembler(code: str) -> Graph:
    words = code.split()
    idf = {}
    label = []
    for i in range(0, len(words)):
        w = words[i]
        if w[0] == 'L' and w[-1] == ':':
            idf[w[0:len(w) - 1]] = len(label)
            label.append(0 if w[1].isdigit() else 1)
    G = Graph(label)
    now = 0
    for i in range(0, len(words)):
        w = words[i]
        if w[0] == 'L' and w[-1] == ':':
            now = idf[w[0:len(w) - 1]]
        elif w[0] == 'j':
            assert i + 1 < len(words)
            to = idf[words[i + 1]]
            G.add_edge(now, to)
    return G
