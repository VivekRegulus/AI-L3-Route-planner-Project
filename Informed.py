import heapq

# I've implemented Greedy and A* for Informed Search

def _trace_back(came_from, goal_state):
    path = []
    s = goal_state
    while s is not None:
        path.append(s[0])
        s = came_from.get(s)
    path.reverse()
    return path


def greedy(graph, start, goal, heuristic_fn, required_stops=None, start_time=8.0):
    if required_stops is None:
        required_stops = set()
    required_stops = frozenset(required_stops)

    init_visited = frozenset({start} & required_stops)
    init_state = (start, start_time, init_visited)

    h0 = heuristic_fn(init_state)
    # heap state -> (h_value, counter, state)
    # counter isliye ki when two states are equal, their comparison doesn't crash
    frontier = [(h0, 0, init_state)]
    explored = set()
    came_from = {init_state: None}
    nodes_expanded = 0
    counter = 1  # tiebreaker
    exploration_order = []

    while frontier:
        _, _, state = heapq.heappop(frontier)  # get the lowest one
        node, time, visited = state
        key = (node, visited)

        # delete lazily
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
                h = heuristic_fn(new_state) 
                heapq.heappush(frontier, (h, counter, new_state))
                counter += 1

    return None


def astar(graph, start, goal, heuristic_fn, required_stops=None, start_time=8.0):
    if required_stops is None:
        required_stops = set()
    required_stops = frozenset(required_stops)

    init_visited = frozenset({start} & required_stops)
    init_state = (start, start_time, init_visited)

    # g_costs is the best known cost till now
    g_costs = {(start, init_visited): 0.0}
    h0 = heuristic_fn(init_state)
    frontier = [(h0, 0, init_state)]  # f = g + h; g is 0 at 0, so its h0
    explored = set()
    came_from = {init_state: None}
    nodes_expanded = 0
    counter = 1
    exploration_order = []

    while frontier:
        _, _, state = heapq.heappop(frontier)  # sabse kam f(n) wala node
        node, time, visited = state
        key = (node, visited)

        # no rexapansion is already seen
        if key in explored:
            continue
        explored.add(key)
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

        g_now = g_costs.get(key, float('inf'))  # best g value of the current node

        for neighbor, dist, spd in graph.get_neighbors(node):
            t_cost = graph.travel_cost(node, neighbor, time)
            new_time = time + t_cost
            new_visited = visited | (frozenset({neighbor}) & required_stops)
            new_state = (neighbor, new_time, new_visited)
            new_key = (neighbor, new_visited)

            new_g = g_now + t_cost

            # only update if we get a better path to the neighbour
            if new_key not in explored and new_g < g_costs.get(new_key, float('inf')):
                g_costs[new_key] = new_g
                came_from[new_state] = state
                h = heuristic_fn(new_state)
                heapq.heappush(frontier, (new_g + h, counter, new_state))  
                counter += 1

    return None