center_point = (28.3615, 75.5885)   # centre of BITS

BITS_osm = ox.graph_from_point(
    center_point,
    dist=800,  # meters
    network_type='walk'
)

from graph import Graph

def build_graph_from_osm(BITS_osm):
    G = Graph()
    
    # Add nodes
    for node, data in BITS_osm.nodes(data=True):
        x = data['x']
        y = data['y']
        G.add_node(node, x, y)

    # Add edges
    for u, v, data in BITS_osm.edges(data=True):
        length = data.get('length', 1)  # meters
        G.add_edge(u, v, length)

    return G
