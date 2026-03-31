# AI-L3-Route-planner-Project
CS F407 Assignment
**Overview**
We have built a walking route planner of the BITS Pilani Campus modeling it as a weighted graph.
It implements optional waypoint criteria as well as time dependent weight calculation.

**Algorithms Used**
1. BFS 2. DFS 3. A* 4. Greedy

**Heurisitcs used**
1. Euclidean 2. Max free flow shortest path

**Files explanation**
Main.py - loads osm data, builds the graph from the osm data and runs the search algorithms on it
graph.py - graph data structure
uninformed.py - bfs and dfs search algorithm implementation
informed.py - greedy and a-star search algorithm implementation
heu.py - heuristic function implementation
visualier.py - plotting the output on matplotlib to see the search algoirthms in working and its output

**Setup Instructions**
1. git clone https://github.com/VivekRegulus/AI-L3-Route-planner-Project.git
cd AI-L3-Route-planner-Project
2. **Install dependencies** : pip install osmnx matplotlib networkx
3.
