# AI-L3-Route-planner-Project
CS F407 Assignment <br>

**Overview** <br>
We have built a walking route planner of the BITS Pilani Campus modeling it as a weighted graph.<br>
It implements optional waypoint criteria as well as time dependent weight calculation.<br>

**Algorithms Used**<br>
1. BFS 2. DFS 3. A* 4. Greedy<br>

**Heurisitcs used**<br>
1. Euclidean 2. Max free flow shortest path<br>

**Files explanation**<br>
Main.py - loads osm data, builds the graph from the osm data and runs the search algorithms on it<br>
graph.py - graph data structure<br>
uninformed.py - bfs and dfs search algorithm implementation<br>
informed.py - greedy and a-star search algorithm implementation<br>
heuristics.py - heuristic function implementation<br>
visualier.py - plotting the output on matplotlib to see the search algoirthms in working and its output<br>

**Setup Instructions**<br>
1. git clone https://github.com/VivekRegulus/AI-L3-Route-planner-Project.git<br>
cd AI-L3-Route-planner-Project<br>
2. **Install dependencies** : pip install osmnx matplotlib networkx<br>
3. Set your goal, start and way points and run the search algorithms.<br>

**Test Case Generation and Execution**<br>
Test cases are generated randomly at runtime using the node set of the constructed graph.<br>

1. The graph nodes are collected after building the graph from OSM data.<br>
2. For each run:<br>
   - A random start node and goal node are selected (ensuring they are different).<br>
   - A fixed number of intermediate waypoints are randomly selected (excluding start and goal).<br>
3. The number of runs and waypoints are controlled by:<br>
   - `NUM_RUNS` → number of test cases executed<br>
   - `NUM_WAYPOINTS` → number of waypoints per test case<br>
4. For each generated test case, all four algorithms (BFS, DFS, Greedy, A*) are executed on the same input.<br>
5. Results are printed in a table and visualized using plotting utilities.<br>

To run the test cases:<br>
- Simply execute `Main.py` after setup.<br>
- The script will automatically generate and run multiple randomized test cases.<br>