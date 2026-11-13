import os,json,random,urllib.request as u
MATE=100000;INF=200000
V=[0,82,337,365,477,1025,0];import base64
T=[b if b<128 else b-256 for b in base64.b64decode('AAAAAAAAAABihj1fRH4i9foHGh9BOBns8g0GFRcMEenl/vsMEQYK5+b8/PYDAyH03f/s6fEYJuoAAAAAAAAAAFmn3s89n/GVt9dIJBc+B+/RPCVBVIFJLPcREzUlRRIW8wQQDRwTFfjp9wwKExEZ8OPL9P3/EvLtl+vG3+/k7enjBK7b59YH+OYQ7vMeOxLR8CUrKCMyJf78BRMyJSUH/voNDRoiDAoEAA8PDw4bEgoEDxAABxUhAd/98uvz9NnrICogMz8JHysbIDo+UEMaLPsTGiQRLT0Q6PUHGhgj+Ozc5vT/CfkG6dPn8O8DAPvf1PDs9/8L+rnt8wEREAfb5uQAHQw7LCst6Nn7AfA5HDbz7wcIHTgvOeXl8PD/Ef4B9+b39v78A/3yAvX++wIOBd34CwIID/0B/+73CvHn4c6/FxDxyN4CDR3/7Pn4/Nrj9xgC8OwGFurv7PTl4ufy3M//5dnS1N/N8vLq0tTi8eUBB/jA1fAJCPEkDMoI5BgO')]
for i,v in [(9, 134), (64, -167), (85, 129)]: T[i]=v
MG=[T[i*64:(i+1)*64] for i in range(6)]
KN=[-33,-31,-18,-14,14,18,31,33];KI=[-17,-16,-15,-1,1,15,16,17]
BD=[-17,-15,15,17];RD=[-16,-1,1,16]
R=random.Random(20261113)
Z=[[R.getrandbits(64) for _ in range(64)] for _ in range(16)]
ZS=R.getrandbits(64);ZC=[R.getrandbits(64) for _ in range(16)];ZE=[R.getrandbits(64) for _ in range(8)]
PHW=[0,0,1,1,2,4,0]
CR={0:2,7:1,112:8,119:4}
b=[0]*128;side=0;cast=0;ep=-1;half=0;mg=0;ph=0;bw=0;bb=0;h=0;kw=0;kb=0
TT={};KIL=[[0,0] for _ in range(128)];HIS=[0]*32768
NODES=0;BUDGET=50000
SQS=[s for s in range(128) if not s&0x88]
class Abort(Exception): pass
def s64(s): return (s>>4)*8+(s&7)
def psa(pc,sq,sgn):
    global mg,ph
    t=pc&7;c=pc>>3
    i=(7-(sq>>4))*8+(sq&7) if c==0 else (sq>>4)*8+(sq&7)
    v=V[t]+MG[t-1][i]
    mg+=sgn*v if c==0 else -sgn*v
    if t>1: ph+=sgn*PHW[t]
def stp(fen):
    global b,side,cast,ep,half,mg,ph,bw,bb,h,kw,kb
    b=[0]*128;mg=0;ph=0;bw=0;bb=0;h=0
    parts=fen.split();rows=parts[0].split('/')
    for r,row in enumerate(rows):
        f=0
        for ch in row:
            if ch.isdigit(): f+=int(ch)
            else:
                t='PNBRQK'.index(ch.upper())+1;c=0 if ch.isupper() else 1
                pc=t|(c<<3);sq=(7-r)*16+f
                b[sq]=pc;psa(pc,sq,1);h^=Z[pc][s64(sq)]
                if t==3: bw+=1-c;bb+=c
                if t==6: kw,kb=(sq,kb) if c==0 else (kw,sq)
                f+=1
    side=0 if parts[1]=='w' else 1
    cast=0
    if len(parts)>2:
        for ch in parts[2]:
            if ch in 'KQkq': cast|=1<<'KQkq'.find(ch)
    ep=-1
    if len(parts)>3 and parts[3]!='-':
        ep=(int(parts[3][1])-1)*16+'abcdefgh'.index(parts[3][0])
    half=int(parts[4]) if len(parts)>4 else 0
    if side: h^=ZS
    h^=ZC[cast]
    if ep>=0: h^=ZE[ep&7]
def atk(sq,by):
    for d in (-15,-17) if by==0 else (15,17):
        if not (sq+d)&0x88 and b[sq+d]==(1|(by<<3)): return True
    for ds,pt in ((KN,2),(KI,6)):
        for d in ds:
            if not (sq+d)&0x88 and b[sq+d]==(pt|(by<<3)): return True
    for d in BD+RD:
        t=sq+d
        while not t&0x88:
            pc=b[t]
            if pc:
                if pc==(5|(by<<3)) or pc==((3 if d in BD else 4)|(by<<3)): return True
                break
            t+=d
    return False
def ich():
    return atk(kw if side==0 else kb,side^1)
def gn(ms,caps):
    us=side;them=us^1;fwd=16 if us==0 else -16
    sr=1 if us==0 else 6;lr=7 if us==0 else 0
    for s in SQS:
        pc=b[s]
        if not pc or (pc>>3)!=us: continue
        t=pc&7
        if t==1:
            o=s+fwd
            if b[o]==0:
                if (o>>4)==lr:
                    ms.extend(s|(o<<7)|(p<<14) for p in (5,4,3,2))
                elif not caps:
                    ms.append(s|(o<<7))
                    if (s>>4)==sr and b[o+fwd]==0: ms.append(s|((o+fwd)<<7))
            for d in (fwd-1,fwd+1):
                to=s+d
                if to&0x88: continue
                tg=b[to]
                if tg and (tg>>3)==them:
                    if (to>>4)==lr:
                        ms.extend(s|(to<<7)|(p<<14) for p in (5,4,3,2))
                    else: ms.append(s|(to<<7))
                elif to==ep and ep>=0:
                    ms.append(s|(to<<7))
        elif t==2 or t==6:
            for d in KN if t==2 else KI:
                to=s+d
                if to&0x88: continue
                tg=b[to]
                if tg==0 and not caps or tg and (tg>>3)==them: ms.append(s|(to<<7))
        else:
            ds=BD if t==3 else RD if t==4 else BD+RD
            for d in ds:
                to=s+d
                while not to&0x88:
                    tg=b[to]
                    if tg==0 and not caps or tg and (tg>>3)==them: ms.append(s|(to<<7))
                    if tg: break
                    to+=d
    if not caps:
        for bt,k,r,t,e,a,rk in ((1,4,7,6,(5,6),(4,5,6),4),(2,4,0,2,(3,2,1),(4,3,2),4),(4,116,119,118,(117,118),(116,117,118),12),(8,116,112,114,(115,114,113),(116,115,114),12)):
            if cast&bt and b[r]==rk and all(not b[x] for x in e) and all(not atk(x,us^1) for x in a): ms.append(k|(t<<7))
def mk(m):
    global side,cast,ep,half,h,mg,ph,bw,bb,kw,kb
    frm=m&127;to=(m>>7)&127;pr=(m>>14)&7
    pc=b[frm];us=side;t=pc&7
    cap=b[to];csq=to
    if t==1 and to==ep and cap==0:
        csq=to-16 if us==0 else to+16;cap=b[csq]
    und=(m,cap,csq,cast,ep,half,h,mg,ph,bw,bb,kw,kb)
    h^=ZC[cast]
    h^=Z[pc][s64(frm)];psa(pc,frm,-1)
    if cap:
        h^=Z[cap][s64(csq)];psa(cap,csq,-1)
        if (cap&7)==3: bw-=1-(cap>>3);bb-=cap>>3
        if csq in CR: cast&=~CR[csq]
    npc=pr|(us<<3) if pr else pc
    b[to]=npc;b[frm]=0
    if csq!=to: b[csq]=0
    h^=Z[npc][s64(to)];psa(npc,to,1)
    if pr==3: bw+=1-us;bb+=us
    if t==6:
        if us==0: kw=to
        else: kb=to
        if abs(to-frm)==2:
            rf=frm+3 if to>frm else frm-4;rt=rf-2 if to>frm else rf+3
            rk=b[rf];b[rt]=rk;b[rf]=0
            h^=Z[rk][s64(rf)]^Z[rk][s64(rt)];psa(rk,rf,-1);psa(rk,rt,1)
        cast&=~3 if us==0 else ~12
    if frm in CR: cast&=~CR[frm]
    if ep>=0: h^=ZE[ep&7]
    ep=-1
    if t==1 and abs(to-frm)==32:
        epawn=9 if us==0 else 1
        if ((to&7)>0 and b[to-1]==epawn) or ((to&7)<7 and b[to+1]==epawn):
            ep=frm+16 if us==0 else frm-16
    if ep>=0: h^=ZE[ep&7]
    h^=ZC[cast]
    half=0 if t==1 or cap else half+1
    side^=1;h^=ZS
    return und
def umk(und):
    global side,cast,ep,half,h,mg,ph,bw,bb,kw,kb
    (m,cap,csq,ocast,oep,ohalf,oh, omg,oph,obw,obb,okw,okb)=und
    frm=m&127;to=(m>>7)&127;pr=(m>>14)&7
    pc=b[to] if not pr else (1|((side^1)<<3))
    b[frm]=pc;b[to]=0
    if cap: b[csq]=cap
    if (pc&7)==6 and abs(to-frm)==2:
        rf=frm+3 if to>frm else frm-4;rt=rf-2 if to>frm else rf+3
        b[rf]=b[rt];b[rt]=0
    side^=1;cast=ocast;ep=oep;half=ohalf;h=oh;mg=omg;ph=oph;bw=obw;bb=obb;kw=okw;kb=okb
def nmk():
    global side,ep,h
    und=(ep,h)
    if ep>=0: h^=ZE[ep&7]
    ep=-1;side^=1;h^=ZS
    return und
def nuk(und):
    global side,ep,h
    oep,oh=und
    side^=1;ep=oep;h=oh
def ev():
    s=mg+25*(bw>=2)-25*(bb>=2)
    if ph<8: s+=((7-abs((kw&7)-3)-abs((kw>>4)-3))-(7-abs((kb&7)-3)-abs((kb>>4)-3)))*6
    return s if side==0 else -s
def odr(ms,ply,ttm):
    sc=[]
    for m in ms:
        to=(m>>7)&127;tg=b[to];s=0
        if tg:
            s=10000+10*V[tg&7]-V[(b[m&127])&7]
        if (m>>14)&7: s+=20000+V[(m>>14)&7]
        if m==ttm: s=1000000
        elif m==KIL[ply][0]: s=5000
        elif m==KIL[ply][1]: s=4000
        else: s+=HIS[(m&127)<<7|to]>>4
        sc.append((s,m))
    return [m for _,m in sorted(sc,key=lambda x:-x[0])]
def q(a,be,ply):
    global NODES
    NODES+=1
    if NODES>=BUDGET: raise Abort
    if half>=100: return 0
    chk=ich()
    if not chk:
        s=ev()
        if s>=be: return s
        if s>a: a=s
        best=s
    else: best=-MATE-1
    ms=[];gn(ms,1 if not chk else 0)
    ms=odr(ms,ply,0)
    for m in ms:
        und=mk(m)
        if atk(kw if side==1 else kb,side):
            umk(und);continue
        s=-q(-be,-a,ply+1)
        umk(und)
        if s>best: best=s
        if s>=be: return s
        if s>a: a=s
    if chk and best==-MATE-1: return -MATE+ply
    return best
def sch(d,a,be,ply,seen):
    global NODES
    if half>=100: return 0
    if d<=0: return q(a,be,ply)
    NODES+=1
    if NODES>=BUDGET: raise Abort
    alpha0=a;best=-MATE-1;bestm=0
    ent=TT.get(h)
    ttm=0
    if ent:
        _,fl,sv,mv=ent;ttm=mv
        if ent[0]>=d:
            s=sv-(ply if sv>MATE-1000 else -ply if sv<-MATE+1000 else 0)
            if fl==1 or (fl==2 and s>=be) or (fl==3 and s<=a): return s
    chk=ich()
    if d>=3 and ply>0 and not chk and ev()>=be and ph>0:
        und=nmk()
        try: s=-sch(d-3,-be,-be+1,ply+1,seen)
        except Abort: nuk(und);raise
        nuk(und)
        if s>=be: return be
    ms=[];gn(ms,0)
    ms=odr(ms,ply,ttm)
    i=0
    for m in ms:
        und=mk(m)
        if atk(kw if side==1 else kb,side):
            umk(und);continue
        i+=1
        if h in seen:
            s=0
        else:
            seen.add(h)
            if i==1:
                s=-sch(d-1,-be,-a,ply+1,seen)
            elif d>=3 and i>3 and not und[1] and not ((m>>14)&7) and not chk:
                s=-sch(d-2,-a-1,-a,ply+1,seen)
                if s>a: s=-sch(d-1,-be,-a,ply+1,seen)
            else:
                s=-sch(d-1,-a-1,-a,ply+1,seen)
                if s>a and s<be: s=-sch(d-1,-be,-a,ply+1,seen)
            seen.discard(h)
        umk(und)
        if s>best: best=s;bestm=m
        if s>=be:
            if not b[(m>>7)&127] and not ((m>>14)&7):
                if m!=KIL[ply][0]:
                    KIL[ply][1]=KIL[ply][0];KIL[ply][0]=m
                HIS[(m&127)<<7|((m>>7)&127)]+=d*d
            break
        if s>a: a=s
    if i==0: return -MATE+ply if chk else 0
    sv=best+(ply if best>MATE-1000 else -ply if best<-MATE+1000 else 0)
    TT[h]=(d,2 if best>=be else 3 if best<=alpha0 else 1,sv,bestm)
    return best
def rtm(seen):
    global NODES
    ms=[];gn(ms,0)
    lg=[]
    for m in ms:
        und=mk(m)
        if not atk(kw if side==1 else kb,side): lg.append(m)
        umk(und)
    if not lg: return None,[]
    if len(lg)==1: return lg[0],lg
    lg=odr(lg,0,0)
    best=lg[0]
    for d in range(1,13):
        NODES=0
        a=-INF;be=INF
        sc=[]
        try:
            for j,m in enumerate(lg):
                und=mk(m)
                if h in seen:
                    s=0
                else:
                    seen.add(h)
                    if j==0: s=-sch(d-1,-be,-a,1,seen)
                    else:
                        s=-sch(d-1,-a-1,-a,1,seen)
                        if s>a and s<be: s=-sch(d-1,-be,-a,1,seen)
                    seen.discard(h)
                umk(und)
                sc.append((s,m))
                if s>a: a=s
            sc.sort(key=lambda x:-x[0])
            lg=[m for _,m in sc]
            best=lg[0]
            if sc[0][0]>MATE-1000: break
        except Abort:
            break
    return best,lg
def uc(m):
    frm=m&127;to=(m>>7)&127
    f='abcdefgh'[frm&7]+str((frm>>4)+1);t='abcdefgh'[to&7]+str((to>>4)+1)
    p=(m>>14)&7
    return f+t+('nbrq'[p-2] if p else '')
def puc(s):
    f='abcdefgh'.index(s[0])+(int(s[1])-1)*16
    t='abcdefgh'.index(s[2])+(int(s[3])-1)*16
    p=0
    if len(s)>4: p='nbrq'.index(s[4])+2
    return f|(t<<7)|(p<<14)
def hhs(moves):
    stp('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    hs=set()
    for s in moves:
        mk(puc(s));hs.add(h)
    return hs
def po(path,obj):
    req=u.Request(URL+path,data=json.dumps(obj).encode(),headers={'Content-Type':'application/json'})
    return json.load(u.urlopen(req))
def main():
    global URL
    URL=os.environ['MAKEFUN_ENV_URL']
    while True:
        g=po('/game',{})
        if g.get('status')=='done': return
        while g.get('status')=='your_move':
            fen=g['fen'];lg=g.get('legal_moves',[])
            stp(fen)
            seen=hhs(g.get('moves',[]))
            stp(fen)
            bm,od=rtm(seen)
            mv=next((x for c in od for x in [uc(c)] if x in lg),None)
            if mv is None:
                if lg: mv=lg[0]
                else:
                    po('/resign',{'game':g['game']});break
            try: g=po('/move',{'game':g['game'],'move':mv})
            except Exception:
                po('/resign',{'game':g['game']});break
if __name__=='__main__': main()
