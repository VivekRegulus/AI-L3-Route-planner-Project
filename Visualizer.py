import matplotlib
matplotlib.rcParams['figure.dpi']=130
matplotlib.rcParams['font.family']='monospace'
import matplotlib.pyplot as plt
import matplotlib.patches as mptch
import matplotlib.animation as anim
import numpy as np
from matplotlib.lines import Line2D

# I've implemented graph drawing, animation and comparison charts
PAL={"bg":"#0d1117","pnl":"#10151d","edg":"#1e2b3c","nd":"#3a4a5c","exp":"#ff4757","p_e":"#ffd32a","p_n":"#ffd32a","st":"#2ed573","gl":"#1e90ff","stp":"#ffa502","txt":"#dfe6e9","bc":["#2ed573","#ff4757","#ffd32a","#1e90ff"]}

def _ps(g):
    # just extract coords
    r={}
    for n in g.crds: r[n]=(g.crds[n][0],g.crds[n][1])
    return r

def _drw_b(x,gr,ps):
    es=set()
    for u in gr.edgs:
        for v,_,_ in gr.edgs[u]:
            pr=tuple(sorted((u,v)))
            if pr in es: continue
            es.add(pr)
            if u in ps and v in ps:
                x1,y1=ps[u]; x2,y2=ps[v]
                x.plot([x1,x2],[y1,y2],color=PAL["edg"],lw=1.4,zorder=1,solid_capstyle="round",alpha=0.95)
    ax=[]; ay=[]
    for n in ps:
        ax.append(ps[n][0]); ay.append(ps[n][1])
    x.scatter(ax,ay,s=7,color=PAL["nd"],zorder=2,linewidths=0,alpha=0.75)

def _dp(x,gr,ps,pth):
    # check if none
    if pth is None: return
    for i in range(len(pth)-1):
        u=pth[i]; v=pth[i+1]
        if u in ps and v in ps:
            x1,y1=ps[u]; x2,y2=ps[v]
            x.plot([x1,x2],[y1,y2],color=PAL["p_e"],lw=9.0,alpha=0.15,zorder=3,solid_capstyle="round")
            x.plot([x1,x2],[y1,y2],color=PAL["p_e"],lw=3.0,zorder=4,solid_capstyle="round")
    for n in pth:
        if n in ps:
            x.scatter(*ps[n],s=80,color=PAL["p_n"],zorder=5,linewidths=0)
            x.scatter(*ps[n],s=130,color=PAL["p_n"],zorder=4,linewidths=0,alpha=0.25)

def vis_res(gr,res,st,gl,rq_s=None,ttl="Search Result"):
    if res is None: print("nothing to show — the search returned None"); return
    rs=rq_s if rq_s is not None else set()
    # not sure if path can ever be None here but guarding anyway
    if "path" not in res or not res["path"]: print("result has no path?"); return
    ps=_ps(gr)
    try: f,x=plt.subplots(figsize=(12,9))
    except: return # maybe matplotlib failed
    f.patch.set_facecolor(PAL["bg"])
    # inline style
    x.set_facecolor(PAL["pnl"]); x.tick_params(colors=PAL["txt"],labelsize=7)
    for sp in x.spines.values(): sp.set_color("#1e2b3c")
    if ttl: x.set_title(ttl,color=PAL["txt"],fontsize=11,pad=8,fontweight="bold")
    _drw_b(x,gr,ps)
    exp=res.get("exploration_order",[])
    if exp:
        ex=[ps[n][0] for n in exp if n in ps]; ey=[ps[n][1] for n in exp if n in ps]
        x.scatter(ex,ey,s=30,color=PAL["exp"],alpha=0.48,zorder=3,linewidths=0)
    _dp(x,gr,ps,res["path"])
    # marking special nodes inline
    if st in ps:
        x.scatter(*ps[st],s=320,color=PAL["st"],zorder=8,marker="*",linewidths=0)
        x.annotate("  start",ps[st],color=PAL["st"],fontsize=8,zorder=9,fontweight="bold")
    if gl in ps:
        x.scatter(*ps[gl],s=320,color=PAL["gl"],zorder=8,marker="*",linewidths=0)
        x.annotate("  goal",ps[gl],color=PAL["gl"],fontsize=8,zorder=9,fontweight="bold")
    for sp in rs:
        if sp in ps and sp not in (st,gl): x.scatter(*ps[sp],s=170,color=PAL["stp"],zorder=7,marker="D",linewidths=0)
    # legend inline
    itms=[mptch.Patch(color=PAL["exp"],alpha=0.72,label="Explored"),mptch.Patch(color=PAL["p_e"],label="Final path")]
    x.legend(handles=itms,facecolor="#0d1117",labelcolor=PAL["txt"],loc="upper left",fontsize=7.5)
    # stats
    p=res.get("path",[]); ne=res.get("nodes_expanded",0); mns=res.get("total_time",0)*60 # hours se minutes mein convert
    t_s=f"expanded:  {ne}\nhops:      {len(p)-1}\ntime:      {mns:.1f} min"
    x.text(0.985,0.02,t_s,transform=x.transAxes,fontsize=8,color=PAL["txt"],va="bottom",ha="right",family="monospace")
    x.margins(0.06); plt.tight_layout(); plt.show()

def vis_sbs(gr,rd,st,gl,rq_s=None):
    rs=rq_s if rq_s else set()
    lbls=list(rd.keys()); n=len(lbls)
    if n==0: return
    cls=min(n,2); rws=int((n+1)/2) # used to be 
    f,axs=plt.subplots(rws,cls,figsize=(cls*10,rws*7))
    f.patch.set_facecolor(PAL["bg"])
    if n==1: axs=[axs]
    elif rws==1: axs=list(axs)
    else:
        # flatten
        t=[]
        for rw in axs:
            for a in rw: t.append(a)
        axs=t
    ps=_ps(gr)
    for i,lb in enumerate(lbls):
        x=axs[i]; rr=rd[lb]
        # inline ax style
        x.set_facecolor(PAL["pnl"]); x.tick_params(colors=PAL["txt"],labelsize=7)
        for sp in x.spines.values(): sp.set_color("#1e2b3c")
        x.set_title(lb,color=PAL["txt"],fontsize=11,pad=8,fontweight="bold")
        _drw_b(x,gr,ps)
        if rr is not None:
            ex=rr.get("exploration_order",[])
            if ex:
                xp=[ps[n][0] for n in ex if n in ps]; yp=[ps[n][1] for n in ex if n in ps]
                x.scatter(xp,yp,s=22,color=PAL["exp"],alpha=0.42,zorder=3,linewidths=0)
            _dp(x,gr,ps,rr["path"])
        else:
            # agar algorithm fail hua to center mein message
            x.text(0.5,0.5,"no solution found",transform=x.transAxes,color=PAL["exp"],fontsize=12,ha="center",va="center",fontweight="bold")
        # mark stuff
        if st in ps: x.scatter(*ps[st],s=320,color=PAL["st"],zorder=8,marker="*",linewidths=0)
        if gl in ps: x.scatter(*ps[gl],s=320,color=PAL["gl"],zorder=8,marker="*",linewidths=0)
        for sp in rs:
            if sp in ps and sp not in (st,gl): x.scatter(*ps[sp],s=170,color=PAL["stp"],zorder=7,marker="D",linewidths=0)
        x.margins(0.06)
    # hide unused
    for j in range(i+1,len(axs)): axs[j].set_visible(False)
    plt.suptitle("Algorithm Comparison : Side by Side",color=PAL["txt"],fontsize=14,y=1.01,fontweight="bold")
    plt.tight_layout(); plt.show()

def cmp_algos(rd):
    ls=list(rd.keys()); ne=[]; tt=[]; hc=[]
    for l in ls:
        r=rd[l]
        if r is None: ne.append(0); tt.append(0.0); hc.append(0)
        else: ne.append(r["nodes_expanded"]); tt.append(r["total_time"]*60); hc.append(len(r["path"])-1)
    xv=np.arange(len(ls))
    try: f,axs=plt.subplots(1,3,figsize=(17,5.5))
    except: return
    f.patch.set_facecolor(PAL["bg"])
    ds=[(axs[0],ne,"Nodes Expanded","count"),(axs[1],tt,"Travel Time (minutes)","minutes"),(axs[2],hc,"Path Length (hops)","hops")]
    for x,vs,ts,yl in ds:
        x.set_facecolor(PAL["pnl"]); x.tick_params(colors=PAL["txt"],labelsize=7)
        for sp in x.spines.values(): sp.set_color("#1e2b3c")
        x.set_title(ts,color=PAL["txt"],fontsize=11,pad=8,fontweight="bold")
        bs=x.bar(xv,vs,color=PAL["bc"][:len(ls)],width=0.52,zorder=2,edgecolor="none",alpha=0.90)
        x.set_xticks(xv); x.set_xticklabels(ls,color=PAL["txt"],fontsize=10,fontweight="bold")
        x.set_ylabel(yl,color=PAL["txt"],fontsize=9)
        tp=max(vs) if max(vs)>0 else 1
        for b,v in zip(bs,vs):
            # har bar ke upar value print karo
            vs_s=f"{v:.1f}" if isinstance(v,float) else str(v)
            x.text(b.get_x()+b.get_width()/2,v+tp*0.025,vs_s,ha="center",va="bottom",color=PAL["txt"],fontsize=9.5,fontweight="bold")
        x.set_ylim(0,tp*1.22) # thoda space upar taaki label clip na ho
        x.grid(axis="y",color="#1e2b3c",linewidth=0.9,zorder=0,alpha=0.9)
    f.suptitle("All Four Algorithms — Empirical Comparison",color=PAL["txt"],fontsize=14,y=1.03,fontweight="bold")
    plt.tight_layout(); plt.show()

def anim_srch(gr,res,st,gl,rq_s=None,ttl="",invl=60,spth=None):
    if res is None: print("no result to animate"); return None
    ps=_ps(gr); eo=res.get("exploration_order",[]); pth=res.get("path",[]); tt=len(eo)
    # if somehow exploration_order is empty there's nothing to animate
    if tt==0: return None
    f,x=plt.subplots(figsize=(12,9)); f.patch.set_facecolor(PAL["bg"]); x.set_facecolor(PAL["pnl"])
    for sp in x.spines.values(): sp.set_color("#1e2b3c")
    if ttl: x.set_title(ttl,color=PAL["txt"],fontsize=11,pad=8,fontweight="bold")
    _drw_b(x,gr,ps)
    rs=rq_s if rq_s else set()
    if st in ps: x.scatter(*ps[st],s=320,color=PAL["st"],zorder=8,marker="*")
    if gl in ps: x.scatter(*ps[gl],s=320,color=PAL["gl"],zorder=8,marker="*")
    for sp in rs:
        if sp in ps and sp not in (st,gl): x.scatter(*ps[sp],s=170,color=PAL["stp"],zorder=7,marker="D")
    x.margins(0.06)
    ex_s=x.scatter([],[],s=30,color=PAL["exp"],alpha=0.55,zorder=3,linewidths=0)
    ct=x.text(0.01,0.99,"",transform=x.transAxes,color=PAL["txt"],fontsize=9,va="top",ha="left",family="monospace")
    ex,ey=[],[]
    pd=[False]
    def up(fm):
        if fm<tt:
            n=eo[fm]
            if n in ps:
                ex.append(ps[n][0]); ey.append(ps[n][1])
                # wtf matplotlib
                ex_s.set_offsets(np.column_stack([ex,ey]) if ex else np.empty((0,2)))
            pc=int((fm+1)/tt*100)
            ct.set_text(f"expanded: {fm+1} / {tt}  ({pc}%)")
        elif not pd[0] and pth:
            _dp(x,gr,ps,pth); pd[0]=True
        return (ex_s,ct)
    tfs=len(eo)+20
    anm=anim.FuncAnimation(f,up,frames=tfs,interval=invl,blit=False)
    if spth:
        try:
            wrt=anim.FFMpegWriter(fps=1000//invl,bitrate=1800)
            anm.save(spth,writer=wrt)
            print(f"saved animation to {spth}")
        except: print("couldnt save mp4, probably ffmpeg missing")
    plt.tight_layout(); plt.show()
    return anm

def prnt_tbl(rd):
    hd=["Algorithm","Expanded","Time (min)","Hops","Complete?","Optimal?"]
    kd={"BFS":(True,"only uniform cost"),"DFS":(True,"no"),"Greedy":(True,"no"),"A*":(True,"yes (admissible h)")}
    rs=[]
    for l,rr in rd.items():
        c,o=kd.get(l,("?","?"))
        if rr is None: rs.append([l,"-","-","-",str(c),o])
        else: rs.append([l,str(rr["nodes_expanded"]),f"{rr['total_time']*60:.2f}",str(len(rr["path"])-1),str(c),o])
    cw=[]
    for i,h in enumerate(hd):
        m=len(h)
        for r in rs:
            if len(r[i])>m: m=len(r[i])
        cw.append(m+2)
    sp="+"+"+".join("-" * w for w in cw)+"+"
    fmt="|"+"|".join(f" {{:<{w-1}}}" for w in cw)+"|"
    print(sp); print(fmt.format(*hd)); print(sp)
    for r in rs: print(fmt.format(*r))
    print(sp)