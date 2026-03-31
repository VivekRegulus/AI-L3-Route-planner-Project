# Uninformed.py
from collections import deque
# I've implemented both BFS and DFS for Uninformed Search

def _tbu(cf,g_st):
    # changed name to avoid conflict if I merge files later
    p=[]; s=g_st
    while s is not None:
        p.append(s[0]) # sirf node name chahiye
        s=cf.get(s)
    p.reverse() # ulta tha since we are appending at the end
    return p

def bfs(gr,st,gl,rq_s=None,st_t=8.0):
    if rq_s is None: rq_s=set()
    # frozenset isliye ki hashed ho sake state mein
    req=frozenset(rq_s)
    # agar start node khud ek required stop hai toh use already visited consider kro
    iv=frozenset({st}&req)
    is_t=(st,st_t,iv)

    q=deque()
    q.append(is_t)
    
    vs_s={(st,iv)} # ignoring time here; only (node, visited_stops) matters for dedup
    p_map={is_t:None}
    nxp=0; e_ord=[]

    while q:
        cs=q.popleft()
        n,t,v=cs
        nxp+=1; e_ord.append(n)

        # goal check 
        if n==gl and req<=v:
            return {"path":_tbu(p_map,cs),"total_time":t-st_t,"nodes_expanded":nxp,"exploration_order":e_ord}

        # neighbors
        for nb,d,s in gr.get_nbrs(n):
            cst=gr.tcst(n,nb,t); nt=t+cst
            nv=v|(frozenset({nb})&req)
            nst=(nb,nt,nv); kk=(nb,nv)
            if kk not in vs_s:
                vs_s.add(kk)
                p_map[nst]=cs; q.append(nst)

    # no path exists
    return None

# TODO: DFS can blow up memory on dense graphs; consider iterative deepening if needed
def dfs(gr,st,gl,rq_s=None,st_t=8.0):
    # just in case
    if rq_s==None: rq_s=set()
    r2=frozenset(rq_s)
    
    sv=frozenset({st}&r2); s0=(st,st_t,sv)
    stk=[s0]; sn=set(); cf={s0:None}
    xp=0; hst=[]

    while stk:
        tmp=stk.pop() 
        _n,_t,_v=tmp; k2=(_n,_v)

        # cycle detection to prevent infinite loops
        if k2 in sn: continue
        sn.add(k2)
        xp+=1; hst.append(_n)

        if _n==gl and r2<=_v:
            rd={}
            rd["path"]=_tbu(cf,tmp)
            rd["total_time"]=_t-st_t
            rd["nodes_expanded"]=xp
            rd["exploration_order"]=hst
            return rd

        # this is a bit messy but whatever
        for na,du,su in gr.get_nbrs(_n):
            ti=gr.tcst(_n,na,_t); ntm=_t+ti
            nvs=_v|(frozenset({na})&r2)
            nst=(na,ntm,nvs)
            if (na,nvs) not in sn:
                cf[nst]=tmp; stk.append(nst)

    return None