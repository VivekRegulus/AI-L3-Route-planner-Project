import osmnx as ox
from Graph import Graph
from Uninformed import bfs, dfs
from Informed import greedy, astar
try:
    from Heuristics import precompute_sff, h1, h2
except:
    pass 
from Visualizer import vis_res, vis_sbs, cmp_algos, anim_srch, prnt_tbl

def mk_gr(raw_dat):
    _g=Graph()
    if raw_dat is None: return _g
    for a,b in raw_dat.nodes(data=True):
        try:
            _x=b['x']; _y=b['y']
            _g.add_nd(a,_x,_y)
        except Exception as e:
            continue
    for u,v,d in raw_dat.edges(data=True):
        l=d.get('length',1)
        if l==None: l=1 # just in case
        _g.add_edg(u,v,l)
    return _g

if __name__ == "__main__":
    pt=(28.3615, 75.5885)
    osm_gr=ox.graph_from_point(pt,dist=800,network_type='walk')

    # build graph
    G=_=mk_gr(osm_gr)
    nds=list(G.crds.keys())

    # first/last/middle is pretty arbitrary; ideally pick nodes that are
    # actually far apart and hit interesting spots on campus, not just list indices
    s=nds[0]; g=nds[-1]
    _m=len(nds)//2
    mids=frozenset({nds[_m]})
    t_m=8.5  # 8:30 AM

    sff=precompute_sff(G)
    print(f"running all 4 algorithms: {s} -> {g}, stops={mids}\n")

    R={}
    
    # lambdas inline 
    h1f=lambda z: h1(z,G,frozenset(mids),g)
    h2f=lambda z: h2(z,G,frozenset(mids),g,sff)

    # bfs
    _1=bfs(G,s,g,mids,t_m); R["BFS"]=_1
    # dfs
    _2=dfs(G,s,g,mids,t_m); R["DFS"]=_2
    # greedy
    __t=greedy(G,s,g,h1f,mids,t_m)
    R["Greedy"]=__t
    # astar (keeping separate in case need debug later)
    ___=astar(G,s,g,h2f,mids,t_m)
    R["A*"]=___
    
    prnt_tbl(R)

    # visualize individually (kinda repetitive but fine)
    # loop over the dict keys
    for k in R.keys():
        v=R[k]
        if v is not None:
            vis_res(G,v,s,g,mids,ttl=k)

    # side by side
    vis_sbs(G,R,s,g,mids)
    # compare
    cmp_algos(R)

    # only doing A* animation for now. matplotlib crashes if I do all
    if "A*" in R:
        try: anim_srch(G,R["A*"],s,g,mids,ttl="A* Search",invl=80,spth="astar_demo.mp4")
        except: print("animation failed, missing ffmpeg?")