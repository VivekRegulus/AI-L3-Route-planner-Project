import heapq

# I've implemented Greedy and A* for Informed Search

def _tb(cf,g_st):
    p=[]
    s=g_st
    # loop till root
    while s is not None:
        p.append(s[0])
        s=cf.get(s)
    p.reverse()
    return p

def greedy(gr,st,gl,h_f,rq_s=None,st_t=8.0):
    if rq_s is None: rq_s=set()
    req=frozenset(rq_s)
    i_v=frozenset({st}&req)
    s0=(st,st_t,i_v)

    h0=h_f(s0)
    # heap state -> (h_value, counter, state)
    # counter isliye ki when two states are equal, their comparison doesn't crash
    fr=[(h0,0,s0)]
    expl=set()
    cf={s0:None}
    nxp=0; cnt=1  # tiebreaker
    ordr=[]

    while fr:
        _,_,cs=heapq.heappop(fr)  # get the lowest one
        nd,tv,vs=cs
        kk=(nd,vs)

        # delete lazily
        if kk in expl: continue
        expl.add(kk)
        
        nxp+=1
        ordr.append(nd)

        # check if we reached goal with all stops
        if nd==gl and req<=vs:
            # inline traceback just for greedy to see if it's faster
            p=[]
            cur=cs
            while cur:
                p.append(cur[0])
                cur=cf.get(cur)
            p.reverse()
            return {"path":p,"total_time":tv-st_t,"nodes_expanded":nxp,"exploration_order":ordr}

        for nb,d,sp in gr.get_nbrs(nd):
            tc=gr.tcst(nd,nb,tv)
            nt=tv+tc
            nv=vs|(frozenset({nb})&req) # intermediate visited
            nst=(nb,nt,nv)

            if (nb,nv) not in expl:
                cf[nst]=cs
                hv=h_f(nst) 
                heapq.heappush(fr,(hv,cnt,nst))
                cnt+=1
    return None

def astar(gr,st,gl,h_f,rq_s=None,st_t=8.0):
    if rq_s is None: rq_s=set()
    req=frozenset(rq_s)
    iv=frozenset({st}&req)
    s0=(st,st_t,iv)

    # g_costs is the best known cost till now
    gc={(st,iv):0.0}
    h0=h_f(s0)
    fr=[(h0,0,s0)]  # f = g + h; g is 0 at 0, so its h0
    ex=set()
    cf={s0:None}
    nxp=0; cnt=1; ordr=[]

    while len(fr)>0:
        _f,_c,cs=heapq.heappop(fr)  # sabse kam f(n) wala node
        nd,tv,vs=cs
        kk=(nd,vs)

        # no rexapansion is already seen
        if kk in ex: continue
        ex.add(kk)
        nxp+=1; ordr.append(nd)

        # goal check 
        if nd==gl:
            if req<=vs:
                return {"path":_tb(cf,cs),"total_time":tv-st_t,"nodes_expanded":nxp,"exploration_order":ordr}

        gnw=gc.get(kk,float('inf'))  # best g value of the current node

        nl=gr.get_nbrs(nd)
        for i in range(len(nl)):
            nb,d,sp=nl[i]
            tc=gr.tcst(nd,nb,tv)
            nt=tv+tc
            nv=vs|(frozenset({nb})&req)
            nst=(nb,nt,nv); nk=(nb,nv)
            ng=gnw+tc

            # only update if we get a better path to the neighbour
            og=gc.get(nk,float('inf'))
            if nk not in ex and ng<og:
                gc[nk]=ng
                cf[nst]=cs
                h=h_f(nst)
                fn=ng+h
                heapq.heappush(fr,(fn,cnt,nst))  
                cnt+=1
    return None