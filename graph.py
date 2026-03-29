import math

class Graph:
    def __init__(self):
        self.edges = {}
        self.coords = {}

    def add_node(self, node, x, y):
        self.coords[node] = (x, y)
        if node not in self.edges:
            self.edges[node] = []

    def add_edge(self, u, v, distance, speed=20):
        self.edges[u].append((v, distance, speed))
        self.edges[v].append((u, distance, speed))

    def get_neighbors(self, node):
        return self.edges.get(node, [])

    def rush_hour_factor(self, time):
        hour = int(time) % 24
        minute = int((time % 1) * 60)
        if hour >= 18 or hour < 8 or hour == 13:
            return 1.0
        if minute >= 0 and minute < 10:
            return 1.2
        if minute < 60 and minute >= 50:
            return 1.5
        return 1.0

    def travel_cost(self, u, v, current_time):
        for neighbour, distance, speed in self.edges.get(u, []):
            if neighbour == v:
                normal_time = distance / speed
                return normal_time * self.rush_hour_factor(current_time)
        return float('inf')

    def euclidean_distance(self, u, v):
        x1, y1 = self.coords[u]
        x2, y2 = self.coords[v]
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
