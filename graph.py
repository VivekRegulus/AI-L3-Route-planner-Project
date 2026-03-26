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
        self.edges[u].append((v,distance,speed))
        self.edges[v].append((u,distance,speed))

    def get_neighbors(self, node):
        return self.edges.get(node, [])

    def rush_hour_factor(self,time):
        hour = time%24 #still have to make a time convertor function undecided where to put it right now
        minute = (time % 1)*60
        if hour >=18 or hour < 8 or hour == 13:
            return 1.0  # normal travel time during night hours and lunch hour
        if minutes >=0 and minutes minutes <10:
            return 1.2 #rush hour during students going to classes slightly late or leaving 
        if minutes < 60 and minutes >= 50:
            return 1.5 #peak rush hours of class going students
        return 1.0

    #Cost Function
    def travel_cost(self,u,v,current_time):
        for edge in self.edges[u]:
            neighbour = edge[0] 
            distance = edge[1] 
            speed = edge[2]
            if neighbour == v:
                normal_time = distance/speed
                travel_time = normal_time *rush_hour_factor(current_time)
                return travel_time
        
   
