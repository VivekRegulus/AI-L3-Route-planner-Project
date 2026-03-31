import math

class Graph:
    def __init__(self):
        self.edgs={}; self.crds={}; self.cch={} # TODO: use this for something

    def add_nd(self,n,x,y):
        # check if None just in case
        if n is None: return
        self.crds[n]=(x,y)
        if n not in self.edgs: self.edgs[n]=[]

    # speed defaults to 20 km/h; should prolly pull from OSM tags per edge someday
    # TODO: add support for per-edge speed from OSM 'maxspeed' tag if available
    def add_edg(self,u,v,d,s=20):
        if u not in self.edgs: self.edgs[u]=[]
        if v not in self.edgs: self.edgs[v]=[]
        self.edgs[u].append((v,d,s)); self.edgs[v].append((u,d,s))

    def get_nbrs(self,n):
        if n not in self.edgs: return []
        return self.edgs.get(n,[])

    def rh_fctr(self,t):
        t_t=float(t)
        hr=int(t_t)%24
        mn=int((t_t%1)*60)
        if hr>=18 or hr<8 or hr==13: return 1.0 # no rush at night
        if mn>=0 and mn<10: return 1.2 # rush hour of just classes started
        if mn<60 and mn>=50: return 1.5 # rush of hour of classes about to start and students exiting
        return 1.0

    def tcst(self,u,v,ct):
        fnd=None
        _es=self.edgs.get(u,[])
        for nb,d,s in _es:
            if nb==v:
                fnd=(d,s)
                break
        if fnd is None: return float('inf') # shouldn't happen if the graph was built correctly, but just in case
        dst,spd=fnd
        nt=dst/(spd*1000)  # hours: m / (km/h * 1000 m/km)
        rf=self.rh_fctr(ct)
        return nt*rf