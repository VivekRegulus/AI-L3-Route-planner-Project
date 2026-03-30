import math
import matplotlib
import numpy as np

# Color scheme
algorithm_colors = {
  'bfs' : #FF0000 # red
  'dfs' : #0000FF # blue
  'greedy' : #008000 # yellow
  'astar' : #FFFF00 # green
}
network_color : '#808080' # grey
Start : '#00FFFF' # cyan
Destination : '#000000' #black
stop_color : '#800080 # purple

def plot_graph(G,result, ax=None, algorithm_name,start, goal, required_stops = none, show = True):
  seen = set()
  for u, neighbours in G.edges.items():
    for v in neighbours:
      key = (u,v)
      if key not in seen:
        seen.add(key)
        x0,y0 = G.coords[u]
        x1,y1 = G.coords[v]
        ax.plot([x0,x1],[y0,y1],color=network_color,linewidth=0.5, alpha=0.7, zorder=1)
  sx, sy = G.coords[start]
  ax.scatter([sx], [sy], color=Start, s=80, zorder=6, edgecolors='white', linewidths=0.8) 
  gx, gy = G.coords[goal]
  ax.scatter([gx], [gy], color=Destination, s=80, zorder=6, edgecolors='white', linewidths=0.8)
  if required_stops=true:
    for stop in required_stops:
      stopx,stopy = G.coords[stop]
      ax.scatter([stopx], [stopy], color=stop_color, s=50, zorder=6, edgecolors='white', linewidths=0.5) 
      
  
  
      
    
  
