from collections import deque

# I've implemented both BFS and DFS for Uninformed Search

def _trace_back(came_from, goal_state):
    path = []
    s = goal_state
    while s is not None:
        path.append(s[0])  # sirf node name chahiye
        s = came_from.get(s)
    path.reverse()  # ulta tha since we are appending at the end
    return path


def bfs(graph, start, goal, required_stops=None, start_time=8.0):
    if required_stops is None:
        required_stops = set()
    required_stops = frozenset(required_stops)  # frozenset isliye ki hashed ho sake state mein

    # agar start node khud ek required stop hai toh use already visited consider kro
    init_visited = frozenset({start} & required_stops)
    init_state = (start, start_time, init_visited)

    frontier = deque([init_state])
    explored = {(start, init_visited)}  # ignoring time here
    came_from = {init_state: None}
    nodes_expanded = 0
    exploration_order = [] 

    while frontier:
        state = frontier.popleft() 
        node, time, visited = state
        nodes_expanded += 1
        exploration_order.append(node)

        # goal check 
        if node == goal and required_stops <= visited:
            return {
                "path": _trace_back(came_from, state),
                "total_time": time - start_time,
                "nodes_expanded": nodes_expanded,
                "exploration_order": exploration_order,
            }

        for neighbor, dist, spd in graph.get_neighbors(node):
            t_cost = graph.travel_cost(node, neighbor, time)
            new_time = time + t_cost
            new_visited = visited | (frozenset({neighbor}) & required_stops)
            new_state = (neighbor, new_time, new_visited)
            key = (neighbor, new_visited)

            if key not in explored:
                explored.add(key)
                came_from[new_state] = state
                frontier.append(new_state)

    # no path exists
    return None


def dfs(graph, start, goal, required_stops=None, start_time=8.0):
    if required_stops is None:
        required_stops = set()
    required_stops = frozenset(required_stops)

    init_visited = frozenset({start} & required_stops)
    init_state = (start, start_time, init_visited)

    frontier = [init_state]
    explored = set()
    came_from = {init_state: None}
    nodes_expanded = 0
    exploration_order = []

    while frontier:
        state = frontier.pop() 
        node, time, visited = state
        key = (node, visited)

        # cycle detection to prevent infinite loops
        if key in explored:
            continue
        explored.add(key)
        nodes_expanded += 1
        exploration_order.append(node)

        if node == goal and required_stops <= visited:
            return {
                "path": _trace_back(came_from, state),
                "total_time": time - start_time,
                "nodes_expanded": nodes_expanded,
                "exploration_order": exploration_order,
            }

        for neighbor, dist, spd in graph.get_neighbors(node):
            t_cost = graph.travel_cost(node, neighbor, time)
            new_time = time + t_cost
            new_visited = visited | (frozenset({neighbor}) & required_stops)
            new_state = (neighbor, new_time, new_visited)

            if (neighbor, new_visited) not in explored:
                came_from[new_state] = state
                frontier.append(new_state)

    return None