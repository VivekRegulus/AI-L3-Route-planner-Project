import math

class Graph:
    def __init__(self):
        self.edges = {}
        self.coords = {}

    def add_node(self, node, x, y):
        self.coords[node] = (x, y)
        if node not in self.edges:
            self.edges[node] = []

    def add_edge(self, u, v, cost):
        self.edges[u].append((v, cost))
        self.edges[v].append((u, cost))

    def get_neighbors(self, node):
        return self.edges.get(node, [])

    def heuristic(self, node, goal):
        x1, y1 = self.coords[node]
        x2, y2 = self.coords[goal]
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
