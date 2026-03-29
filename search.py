from collections import deque


def _reconstruct_path(came_from, goal_state):
    path = []
    state = goal_state
    while state is not None:
        path.append(state[0])
        state = came_from.get(state)
    path.reverse()
    return path


def bfs(graph, start, goal, required_stops=None, start_time=8.0):
    """Breadth-First Search — guarantees fewest-hops path."""
    if required_stops is None:
        required_stops = set()
    required_stops = frozenset(required_stops)

    init_visited = frozenset({start} & required_stops)
    init_state = (start, start_time, init_visited)

    frontier = deque([init_state])
    explored = {(start, init_visited)}
    came_from = {init_state: None}
    nodes_expanded = 0

    while frontier:
        current_state = frontier.popleft()
        curr_node, curr_time, curr_visited = current_state
        nodes_expanded += 1

        if curr_node == goal and required_stops <= curr_visited:
            return {
                "path": _reconstruct_path(came_from, current_state),
                "total_time": curr_time - start_time,
                "nodes_expanded": nodes_expanded,
            }

        for neighbor, distance, speed in graph.get_neighbors(curr_node):
            travel_time = graph.travel_cost(curr_node, neighbor, curr_time)
            new_time = curr_time + travel_time
            new_visited = curr_visited | (frozenset({neighbor}) & required_stops)
            new_state = (neighbor, new_time, new_visited)
            state_key = (neighbor, new_visited)

            if state_key not in explored:
                explored.add(state_key)
                came_from[new_state] = current_state
                frontier.append(new_state)

    return None


def dfs(graph, start, goal, required_stops=None, start_time=8.0):
    """Depth-First Search — memory-efficient, not optimal."""
    if required_stops is None:
        required_stops = set()
    required_stops = frozenset(required_stops)

    init_visited = frozenset({start} & required_stops)
    init_state = (start, start_time, init_visited)

    frontier = [init_state]
    explored = set()
    came_from = {init_state: None}
    nodes_expanded = 0

    while frontier:
        current_state = frontier.pop()
        curr_node, curr_time, curr_visited = current_state
        state_key = (curr_node, curr_visited)

        if state_key in explored:
            continue
        explored.add(state_key)
        nodes_expanded += 1

        if curr_node == goal and required_stops <= curr_visited:
            return {
                "path": _reconstruct_path(came_from, current_state),
                "total_time": curr_time - start_time,
                "nodes_expanded": nodes_expanded,
            }

        for neighbor, distance, speed in graph.get_neighbors(curr_node):
            travel_time = graph.travel_cost(curr_node, neighbor, curr_time)
            new_time = curr_time + travel_time
            new_visited = curr_visited | (frozenset({neighbor}) & required_stops)
            new_state = (neighbor, new_time, new_visited)

            if (neighbor, new_visited) not in explored:
                came_from[new_state] = current_state
                frontier.append(new_state)

    return None
