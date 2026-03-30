import math
import heapq
speed=20.0
def euclidean_distance(self, u, v):
        x1, y1 = self.coords[u]
        x2, y2 = self.coords[v]
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
def get_remaining_targets(state, required, goal):
    
    visited = state[2]
    return (required - visited) | {goal}
def h1(state, graph, required, goal):
    current_node= state[0]
    targets = get_remaining_targets(state, required, goal)
    if not targets:   # we were comparing with ==0 but targets is a set so i changed to the correct check
        return 0.0
    maxtime=0.0
    for i in targets: # the outer for i loop was wrong so i removed it
        d=euclidean_distance(graph,current_node,i)/speed  
        if d>maxtime:
            maxtime=d
    return maxtime
def free_flow_weight(graph):
    if hasattr(graph, 'ff_weights'):
        return graph.ff_weights
    ff = {}
    for u in graph.edges:
        for v, distance, speed in graph.edges[u]:
            ff[(u, v)] = distance / speed   
    graph.ff_weights = ff
    return ff
def dijkstra(graph, source, ff):
    dist={}
    for node in graph.coords:
        dist[node] = math.inf   
    dist[source] = 0.0
    a = [(0.0, source)]
    while a:
        d_u, u = heapq.heappop(a)
        if d_u > dist[u]:      
            continue
        for v, _dist, _speed in graph.edges.get(u, []):
            w   = ff.get((u, v), math.inf)
            alter = d_u + w
            if alter < dist[v]:
                dist[v] = alter
                heapq.heappush(a, (alter, v))
    return dist
def precompute_sff(graph):
    ff_weights = free_flow_weight(graph)
    sff = {}
    for u in graph.coords:
        sff[u] = dijkstra(graph, u, ff_weights)
    return sff
def h2(state, graph, required, goal, sff):
    current_node= state[0]
    targets = get_remaining_targets(state, required, goal)
    if not targets:  # same as above
        return 0.0
    maxtime=0.0
    dist_from_v = sff.get(current_node, {})
    for u in targets:  # same as above
        sff_vu = dist_from_v.get(u, math.inf)   
        if sff_vu > maxtime:
            maxtime = sff_vu
    return maxtime
def verify_dominance(state, graph, required, goal, sff):
    h1_v = h1(state, graph, required, goal)
    h2_v = h2(state, graph, required, goal, sff)
    return h1_v, h2_v, (h2_v >= h1_v - 1e-8)
if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(__file__))
    from graph import Graph
    g = Graph()
    g.add_node("LHC",      x=0,   y=0)
    g.add_node("Library",  x=300, y=400)   
    g.add_node("MainGate", x=700, y=400)
    g.add_node("Meera",    x=0,   y=300)   
    g.add_node("SportsC",  x=700, y=0)
    g.add_edge("LHC",      "Library",  distance=500)
    g.add_edge("Library",  "MainGate", distance=400)
    g.add_edge("LHC",      "Meera",    distance=300)
    g.add_edge("MainGate", "SportsC",  distance=400)
    g.add_edge("LHC",      "MainGate", distance=900)
    required = frozenset({"Library", "Meera"})
    goal     = "MainGate"
    sff = precompute_sff(g)
    print("=== Free-flow shortest-path times from LHC ===")
    for node, t in sorted(sff["LHC"].items()):
        dist_equiv = t * 20.0
        print(f"  LHC → {node:<12}: {t:.4f} h  ({dist_equiv:.1f} m road distance)")
    print()
    tests = [
        ("LHC",      9.0,  frozenset(),                                "initial state"),
        ("Library",  10.0, frozenset({"Library"}),                     "Library visited"),
        ("MainGate", 12.0, frozenset({"Library","Meera","MainGate"}),  "goal state — all done"),
    ]
    for node, time, visited, label in tests:
        state = (node, time, visited)
        h1_val, h2_val, dom = verify_dominance(state, g, required, goal, sff)
        print(f"State ({node}, t={time}, {label}):")
        print(f"  h1 = {h1_val:.4f} h   [max Euclidean dist / speed]")
        print(f"  h2 = {h2_val:.4f} h   [max road SFF / speed]")
        print(f"  h2 >= h1 (dominance): {dom}")
        print()