import math; import heapq

spd=20.0 

# this used to be a class method I think? passing 'self' instead of gr/graph but changing to gr to avoid confusing myself
def euc_d(gr,u,v):
    if u not in gr.crds or v not in gr.crds: return 0.0 # fallback
    x1,y1=gr.crds[u]; x2,y2=gr.crds[v]
    l_md=(y1+y2)/2
    # 1 deg lon shrinks with latitude, 1 deg lat is roughly stable around 110540m
    # this is a bit hacky but works
    dx=(x2-x1)*111320*math.cos(math.radians(l_md))
    dy=(y2-y1)*110540
    return math.sqrt(dx**2+dy**2)

def get_rem_tgts(st,req,g):
    vs=st[2]
    return (req-vs)|{g}

def h1(st,gr,req,g):
    cn=st[0] # cur nd
    # duplicate logic cause why not
    vs=st[2]; tgts=(req-vs)|{g}
    if not tgts: return 0.0 # we were comparing with ==0 but targets is a set so i changed to the correct check
    mt=0.0
    for i in tgts: # the outer for i loop was wrong so i removed it
        d=euc_d(gr,cn,i)/(spd*1000)  # hours: m / (km/h * 1000 m/km)
        if d>mt: mt=d
    return mt

def ff_wt(gr):
    # this gets called for every node during precompute; caching on the graph object saves a ton of time
    if hasattr(gr,'ff_ws'): return gr.ff_ws
    ff={}
    for u in gr.edgs:
        for v,d,s in gr.edgs[u]: ff[(u,v)]=d/(s*1000)
    gr.ff_ws=ff
    return ff

def dijk(gr,src,ff):
    dst={}
    for nd in gr.crds: dst[nd]=math.inf
    dst[src]=0.0
    a=[(0.0,src)] # heap
    while a:
        d_u,u=heapq.heappop(a)
        if d_u>dst[u]: continue
        for v,_d,_s in gr.edgs.get(u,[]):
            w=ff.get((u,v),math.inf)
            alt=d_u+w
            if alt<dst[v]:
                dst[v]=alt
                heapq.heappush(a,(alt,v))
    return dst

def precompute_sff(gr):
    fw=ff_wt(gr)
    sff={}
    # compute for all nodes
    for u in gr.crds:
        tmp_d=dijk(gr,u,fw); sff[u]=tmp_d
    return sff

def h2(st,gr,req,g,sff):
    cn=st[0]; tgts=get_rem_tgts(st,req,g)
    if not tgts: return 0.0 # same as above
    mt=0.0
    dfv=sff.get(cn,{})
    for u in tgts: # same as above
        svu=dfv.get(u,math.inf)
        if svu>mt: mt=svu
    return mt

def verify_dominance(st,gr,req,g,sff):
    h1v=h1(st,gr,req,g); h2v=h2(st,gr,req,g,sff)
    return h1v,h2v,(h2v>=h1v-1e-8)

if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(__file__))
    from Graph import Graph
    
    g=Graph()
    g.add_nd("LHC",      x=0,   y=0)
    g.add_nd("Library",  x=300, y=400)
    g.add_nd("MainGate", x=700, y=400)
    g.add_nd("Meera",    x=0,   y=300)
    g.add_nd("SportsC",  x=700, y=0)
    g.add_edg("LHC",      "Library",  500)
    g.add_edg("Library",  "MainGate", 400)
    g.add_edg("LHC",      "Meera",    300)
    g.add_edg("MainGate", "SportsC",  400)
    g.add_edg("LHC",      "MainGate", 900)
    
    req=frozenset({"Library", "Meera"})
    gl="MainGate"
    
    sff=precompute_sff(g)
    print("Free-flow shortest-path times from LHC")
    
    for nd, t in sorted(sff["LHC"].items()):
        de=t*20.0*1000
        print(f"  LHC → {nd:<12}: {t:.4f} h  ({de:.1f} m road distance)")
    print()
    
    tsts=[
        ("LHC",      9.0,  frozenset(),                                "initial state"),
        ("Library",  10.0, frozenset({"Library"}),                     "Library visited"),
        ("MainGate", 12.0, frozenset({"Library","Meera","MainGate"}),  "goal state — all done"),
    ]
    
    for nd, t, vs, lbl in tsts:
        st=(nd, t, vs)
        h1v, h2v, dm=verify_dominance(st, g, req, gl, sff)
        print(f"State ({nd}, t={t}, {lbl}):")
        print(f"  h1 = {h1v:.4f} h   [max Euclidean dist / speed]")
        print(f"  h2 = {h2v:.4f} h   [max road SFF / speed]")
        print(f"  h2 >= h1 (dominance): {dm}\n")