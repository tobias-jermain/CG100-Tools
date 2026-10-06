# CIRCUIT SOLVER for Casio fx-CG100 (MicroPython 1.9.4, casioplot)
# Arrows = move, OK = add/change part, 0-9 . = value, +/- = value up/down, EXE = flip cell/switch, DEL = delete, x10^x = examples, AC = quit
from casioplot import *
SPD=0;LP=6;HOLD=8   # SPD = extra delay per frame, LP = lamp watts for full glow, HOLD = frames before an arrow repeats
W=384;H=192;C=6;R=4;S=44;X0=10;Y0=22;PX=268
NH=(C-1)*R;NE=NH+C*(R-1);NN=C*R
BG=(255,255,255);WC=(30,30,40);TX=(70,70,90);AC=(0,102,204);CU=(0,160,255);RD=(220,40,40)
GR=(200,205,215);RC=(200,90,20);RF=(255,226,190);DC=(255,160,0);HL=(255,240,160)
LC=((215,215,215),(245,230,170),(250,215,100),(255,195,40),(255,150,0))   # lamp colour by brightness
NM=("EMPTY","WIRE","RESISTOR","LAMP","CELL","SWITCH")
DF=(0,0,10,12,6,0)   # default value of each part
ZN=(None,None,(12,32),(12,32),(18,27),(13,31))   # where current dots hide behind the symbol
KD={91:"0",81:"1",82:"2",83:"3",71:"4",72:"5",73:"6",61:"7",62:"8",63:"9",92:"."}
# examples: wires (x, y, 0 = right / 1 = down), then parts (x, y, o, part, value, flag = cell + at left/top end, or switch closed)
EXS=((((0,0,1),(0,2,1),(0,0,0),(2,0,0),(3,0,0),(4,0,0),(3,0,1),(3,2,1),(5,0,1),(5,2,1),(0,3,0),(2,3,0),(3,3,0),(4,3,0)),
((0,1,1,4,12,1),(1,0,0,2,4,0),(3,1,1,3,12,0),(5,1,1,3,6,0),(1,3,0,5,0,1))),
(((0,0,1),(0,2,1),(0,0,0),(1,0,0),(2,0,0),(3,2,1),(3,1,0),(4,2,1),(0,3,0),(1,3,0),(2,3,0),(3,3,0)),
((0,1,1,4,9,1),(3,0,1,2,6,0),(3,1,1,2,3,0),(4,1,1,3,6,0))),
(((0,0,1),(0,2,1),(4,0,1),(4,2,1),(1,0,0),(2,0,0),(2,0,1),(2,2,1),(0,3,0),(1,3,0),(2,3,0),(3,3,0)),
((0,1,1,4,6,1),(4,1,1,4,3,1),(0,0,0,2,2,0),(3,0,0,2,1,0),(2,1,1,2,4,0))),((),()))
EXN=("LAMPS IN PARALLEL","POTENTIAL DIVIDER","TWO CELLS","BLANK BOARD")
class Z:pass
z=Z();z.lk=0;z.hc=0;z.tx={};z.ex=0;z.cx=1;z.cy=0;z.sel=0;z.ie=-1;z.ib="";z.err=""
EA=[];EB=[];EO=[];EX=[];EY=[];NX=[];NY=[];NI=[]
for o in (0,1):   # edges: first the horizontal ones (o = 0), then the vertical ones
  for y in range(R-o):
    for x in range(C-1+o):EA.append(y*C+x);EB.append(y*C+x+(C if o else 1));EO.append(o);EX.append(X0+x*S);EY.append(Y0+y*S)
for y in range(R):
  for x in range(C):NX.append(X0+x*S);NY.append(Y0+y*S);NI.append([])
for e in range(NE):NI[EA[e]].append(e);NI[EB[e]].append(e)
def eid(x,y,o):return NH+y*C+x if o else y*(C-1)+x
def rc(x,y,w,h,c):
  for i in range(w):
    for j in range(h):set_pixel(x+i,y+j,c)
def dly(n):
  for i in range(n):pass
# exact fractions are stored as (numerator, denominator) with denominator > 0
def dv(a,b):   # a//b for a>=0, b>0, done with shifts (the calculator avoids //)
  q=0;s=0
  while (b<<(s+1))<=a:s+=1
  while s>=0:
    if (b<<s)<=a:a-=b<<s;q+=1<<s
    s-=1
  return q
def fr(n,d):
  if d<0:n=-n;d=-d
  a=abs(n);b=d
  while b:a,b=b,a%b
  return (dv(n,a) if n>=0 else -dv(-n,a),dv(d,a))
O=(0,1);I1=(1,1)
def fa(x,y):return fr(x[0]*y[1]+y[0]*x[1],x[1]*y[1])
def fs(x,y):return fr(x[0]*y[1]-y[0]*x[1],x[1]*y[1])
def fm(x,y):return fr(x[0]*y[0],x[1]*y[1])
def fq(x,y):return fr(x[0]*y[1],x[1]*y[0])
def ng(x):return (-x[0],x[1])
def fab(x):return (abs(x[0]),x[1])
def fst(f):return str(f[0]) if f[1]==1 else str(f[0])+"/"+str(f[1])
def dec(f):   # decimal to 3 places, rounded, trailing zeros removed
  m=dv(2000*abs(f[0])+f[1],2*f[1]);t=str(dv(m,1000))+"."+str(1000+m%1000)[1:]
  t=t.rstrip("0").rstrip(".")
  return ("-" if f[0]<0 and t!="0" else "")+t
def vs(f):return fst(f) if f[1]==1 else dec(f)
def pv(s):
  n=0;d=1;p=0
  for c in s:
    if c==".":p=1
    else:n=n*10+"0123456789".index(c);d*=10 if p else 1
  return fr(n,d)
def fnd(p,a):   # solver: nodal analysis with exact fractions
  while p[a]!=a:a=p[a]
  return a
def cond(e):return z.t[e]==1 or (z.t[e]==5 and z.f[e])
def st(A,i,j,v):
  if i>=0 and j>=0:A[i][j]=fa(A[i][j],v)
def solve():
  z.err="";z.I=[O]*NE;z.V=[O]*NE;z.np=[None]*NN;z.nc=0
  p=list(range(NN))
  for e in range(NE):   # wires and closed switches join grid points into one node
    if cond(e):p[fnd(p,EA[e])]=fnd(p,EB[e])
  g=[fnd(p,i) for i in range(NN)];q=list(range(NN));L=[];gd={};ix={}
  for e in range(NE):   # q groups the nodes into separate circuits
    if z.t[e]>1 and z.t[e]<5:L.append(e);q[fnd(q,g[EA[e]])]=fnd(q,g[EB[e]])
  cs=[e for e in L if z.t[e]==4];z.nc=len(cs)
  for e in cs:   # 0 V = negative terminal of the first cell in each separate circuit
    m=g[EB[e]] if z.f[e] else g[EA[e]];c=fnd(q,m);gd[c]=gd.get(c,m)
  for e in L:
    for m in (g[EA[e]],g[EB[e]]):
      c=fnd(q,m);gd[c]=gd.get(c,m)
      if gd[c]!=m and m not in ix:ix[m]=len(ix)
  nv=len(ix);n=nv+len(cs);A=[[O]*(n+1) for i in range(n)];j=nv
  for e in L:
    a=g[EA[e]];b=g[EB[e]];ia=ix[a] if a in ix else -1;ib=ix[b] if b in ix else -1
    if z.t[e]<4:
      if a!=b:G=fq(I1,z.v[e]);st(A,ia,ia,G);st(A,ib,ib,G);st(A,ia,ib,ng(G));st(A,ib,ia,ng(G))
    else:
      if a==b:z.err="SHORT CIRCUIT!";return
      if z.f[e]:ia,ib=ib,ia   # ib = + terminal, ia = - terminal
      st(A,ib,j,(-1,1));st(A,ia,j,I1);st(A,j,ib,I1);st(A,j,ia,(-1,1));A[j][n]=z.v[e];j+=1
  for c in range(n):   # Gaussian elimination; the sparsest pivot row keeps the fractions small
    k=-1;w=n+2
    for r in range(c,n):
      m=len([v for v in A[r] if v[0]]) if A[r][c][0] else w
      if m<w:k=r;w=m
    if k<0:z.err="SHORT CIRCUIT!";return
    A[c],A[k]=A[k],A[c];P=A[c]
    for r in range(c+1,n):
      if A[r][c][0]:
        f=fq(A[r][c],P[c]);Q=A[r]
        for i in range(c,n+1):Q[i]=fs(Q[i],fm(f,P[i])) if P[i][0] else Q[i]
  x=[O]*n
  for c in range(n-1,-1,-1):
    v=A[c][n]
    for i in range(c+1,n):v=fs(v,fm(A[c][i],x[i])) if A[c][i][0] else v
    x[c]=fq(v,A[c][c])
  def pot(m):return x[ix[m]] if m in ix else O
  inj=[O]*NN;j=nv;tg={}
  for e in L:
    a=g[EA[e]];b=g[EB[e]];tg[a]=1;tg[b]=1;v=fs(pot(a),pot(b));z.V[e]=v
    if z.t[e]<4:i=fq(v,z.v[e])
    else:i=ng(x[j]) if z.f[e] else x[j];j+=1
    z.I[e]=i;inj[EB[e]]=fa(inj[EB[e]],i);inj[EA[e]]=fs(inj[EA[e]],i)
  z.np=[pot(g[m]) if g[m] in tg else None for m in range(NN)]
  od=[];pe=[-1]*NN;sn=[0]*NN;h=0   # wire currents: walk a spanning tree of the wires, leaves first
  for s in range(NN):
    if not sn[s]:sn[s]=1;od.append(s)
    while h<len(od):
      u=od[h];h+=1
      for e in NI[u]:
        w=EB[e] if EA[e]==u else EA[e]
        if cond(e) and not sn[w]:sn[w]=1;pe[w]=e;od.append(w)
  for k in range(len(od)-1,0,-1):
    u=od[k];e=pe[u]
    if e>=0:w=EB[e] if EA[e]==u else EA[e];c=inj[u];z.I[e]=c if EA[e]==u else ng(c);inj[w]=fa(inj[w],c)
def calc():
  try:solve()
  except Exception:z.err="TOO COMPLEX";z.I=[O]*NE;z.V=[O]*NE;z.np=[None]*NN   # numbers too big for the calculator
  post()
def post():   # lamp brightness and current-dot speeds from the solution
  mx=O
  for e in range(NE):
    if z.t[e] and abs(z.I[e][0])*mx[1]>mx[0]*z.I[e][1]:mx=fab(z.I[e])
  for e in range(NE):
    i=z.I[e];z.sp[e]=0
    if z.t[e] and i[0]:z.sp[e]=(1+dv(7*abs(i[0])*mx[1],i[1]*mx[0]))*(1 if i[0]>0 else -1)
    if z.t[e]==3:w=fab(fm(z.V[e],i));l=min(4,dv(4*w[0],LP*w[1]));z.lv[e]=1 if w[0] and l==0 else l
def lr(e,u,v,w,h,c):   # rectangle in edge coordinates: u along the edge, v across it
  rc(EX[e]+v,EY[e]+u,h,w,c) if EO[e] else rc(EX[e]+u,EY[e]+v,w,h,c)
def disc(e,r,c):
  for j in range(-r,r+1):
    w=0
    while (w+1)*(w+1)<=r*r-j*j:w+=1
    lr(e,22-w,j,2*w+1,1,c)
def de(e):
  t=z.t[e];f=z.f[e];z.dp[e]=[]
  lr(e,5,-2,35,6,BG);lr(e,11,-10,23,21,BG)   # wire strip + symbol box, kept clear of the neighbours
  rc(EX[e]+12,EY[e]+(12 if EO[e] else -21),22,11,BG)   # value label: right of a vertical part, above a horizontal one
  if t==0:[lr(e,u,0,1,1,GR) for u in range(7,39,4)]   # faint guide where a part can go
  elif t==1:lr(e,5,0,35,2,WC)
  elif t==2:lr(e,5,0,7,2,WC);lr(e,33,0,7,2,WC);lr(e,12,-5,21,12,RC);lr(e,13,-4,19,10,RF)
  elif t==3:
    lr(e,5,0,9,2,WC);lr(e,31,0,9,2,WC);l=z.lv[e]
    if l==4:disc(e,10,HL)
    disc(e,8,WC);disc(e,7,LC[l])
    for k in range(-4,5):lr(e,22+k,k,1,1,WC);lr(e,22+k,-k,1,1,WC)
  elif t==4:
    lr(e,5,0,14,2,WC);lr(e,26,0,14,2,WC)
    if f:lr(e,19,-8,2,18,WC);lr(e,25,-4,3,10,WC);p=13   # long plate = + terminal
    else:lr(e,18,-4,3,10,WC);lr(e,25,-8,2,18,WC);p=31
    lr(e,p-2,-7,5,1,RD);lr(e,p,-9,1,5,RD)
  else:
    lr(e,5,0,9,2,WC);lr(e,31,0,9,2,WC);lr(e,13,-1,3,4,WC);lr(e,29,-1,3,4,WC)
    if f:lr(e,15,0,14,2,WC)
    else:[lr(e,15+k,-(k>>1),1,2,WC) for k in range(15)]
  if t>1 and t<5:
    draw_string(EX[e]+13,EY[e]+(12 if EO[e] else -21),vs(z.v[e])+("V" if t==4 else ""),RD if t==4 else TX,"small")
  if z.sel==e:lr(e,11,-10,23,1,CU);lr(e,11,10,23,1,CU);lr(e,11,-10,1,21,CU);lr(e,33,-10,1,21,CU)
def dn(n):
  x=NX[n];y=NY[n];k=0
  rc(x-4,y-4,9,9,BG)
  for e in NI[n]:
    if z.t[e]:
      k+=1;a=EA[e]==n   # wire stub towards each connected part
      rc(x,y if a else y-4,2,5,WC) if EO[e] else rc(x if a else x-4,y,5,2,WC)
  if k==0:rc(x,y,2,2,GR)
  if k>2:rc(x-1,y-1,4,4,WC)
  if z.sel==-1-n:rc(x-4,y-4,9,1,CU);rc(x-4,y+4,9,1,CU);rc(x-4,y-4,1,9,CU);rc(x+4,y-4,1,9,CU)
def ds(s):dn(-1-s) if s<0 else de(s)
def anim():   # move the current dots along every edge that carries current
  for e in range(NE):
    s=z.sp[e];o=z.dp[e]
    if s==0 and not o:continue
    n=[]
    if s:
      z.ph[e]+=s;f=(z.ph[e]>>2)%33;q=ZN[z.t[e]]
      for k in (0,11,22):
        u=5+(f+k)%33
        if q is None or u+2<q[0] or u>q[1]:n.append(u)
    for u in o:
      if u not in n:lr(e,u,-1,3,1,BG);lr(e,u,0,3,2,WC);lr(e,u,2,3,1,BG)
    for u in n:
      if u not in o:lr(e,u,-1,3,4,DC)
    z.dp[e]=n
def tx(k,y,s,c=TX):   # panel text: erase the old string by drawing it again in white
  o=z.tx.get(k)
  if o==(s,c):return
  if o:draw_string(PX+4,y,o[0],BG,"small")
  if s:draw_string(PX+4,y,s,c,"small")
  z.tx[k]=(s,c)
def qty(k,y,l,f,u):
  if f is None:tx(k,y,"");tx(k+1,y+11,"");return
  a=fst(f)
  if len(a)>7:tx(k,y,l+" ~ "+dec(f)+" "+u);tx(k+1,y+11,"")
  else:tx(k,y,l+" = "+a+" "+u);tx(k+1,y+11,"    = "+dec(f) if f[1]>1 else "")
def panel():
  s=z.sel;V=None;I=None;P=None
  if s<0:
    V=z.np[-1-s];tx(1,18,"NODE",AC);tx(2,30,"not connected" if V is None else "0 V = cell's -")
  else:
    t=z.t[s];tx(1,18,NM[t],AC)
    if t<2:tx(2,30,"" if t else "OK: add a part")
    elif t==5:tx(2,30,"CLOSED" if z.f[s] else "OPEN")
    else:
      v=z.ib+"_" if z.ie==s else vs(z.v[s])
      tx(2,30,"E = "+v+" V" if t==4 else "R = "+v+" ohm")
    if t:I=fab(z.I[s])
    if t>1 and t<5:V=fab(z.V[s]);P=fab(fm(V,I))
  qty(3,43,"V",V,"V");qty(5,66,"I",I,"A");qty(7,89,"P",P,"W")
  tx(9,112,z.err if z.err else "" if z.nc else "ADD A CELL",RD)
def full():
  clear_screen();z.tx={}
  rc(PX-4,0,1,H,GR);rc(PX-3,0,W-PX+3,14,AC);draw_string(PX+4,2,"CIRCUIT SOLVER",BG,"small")
  for i,s in ((0,"ARROWS move"),(1,"OK  change part"),(2,"0-9 +/- value"),(3,"EXE flip/switch"),(4,"DEL delete"),(5,"x10^x examples")):
    draw_string(PX+4,126+i*11,s,TX,"small")
  for e in range(NE):de(e)
  for n in range(NN):dn(n)
  draw_string(X0,H-14,EXN[z.ex],TX,"small");panel();show_screen()
def load():
  z.t=[0]*NE;z.v=[O]*NE;z.f=[0]*NE;z.lv=[0]*NE;z.sp=[0]*NE;z.ph=[0]*NE;z.dp=[[] for e in range(NE)];z.ie=-1
  for x,y,o in EXS[z.ex][0]:z.t[eid(x,y,o)]=1
  for x,y,o,t,v,f in EXS[z.ex][1]:e=eid(x,y,o);z.t[e]=t;z.v[e]=(v,1);z.f[e]=f
  calc();full()
def upd(e):   # re-solve after an edit and redraw what changed
  o=list(z.lv);calc();de(e);dn(EA[e]);dn(EB[e])
  for i in range(NE):
    if z.t[i]==3 and z.lv[i]!=o[i] and i!=e:de(i)
  panel()
def setv(e):
  v=pv(z.ib) if z.ib and z.ib!="." else O
  if v[0] or (z.t[e]==4 and z.ib):z.v[e]=v
def cur():   # the cursor moves on a half-step grid: even x and y = node, odd x = horizontal edge, odd y = vertical edge
  x=z.cx;y=z.cy;return eid(x>>1,y>>1,0) if x&1 else eid(x>>1,y>>1,1) if y&1 else -1-((y>>1)*C+(x>>1))
def move(k):
  x=z.cx;y=z.cy
  if k==25:x+=2 if y&1 else 1
  elif k==23:x-=2 if y&1 else 1
  elif k==34:y+=2 if x&1 else 1
  else:y-=2 if x&1 else 1
  if x<0 or y<0 or x>2*C-2 or y>2*R-2:return
  o=z.sel;z.cx=x;z.cy=y;z.sel=cur();z.ie=-1;ds(o);ds(z.sel);panel()
def key(k):
  if k in (14,23,25,34):move(k);return
  if k==93:z.ex=(z.ex+1)%len(EXS);load();return
  s=z.sel
  if s<0:return
  t=z.t[s]
  if k==24:t=(t+1)%6;z.t[s]=t;z.v[s]=(DF[t],1);z.f[s]=1 if t==5 else 0;z.ie=-1
  elif k in KD and t!=1 and t!=5:
    if t==0:z.t[s]=2;z.v[s]=(DF[2],1);z.f[s]=0   # typing on an empty edge adds a resistor
    if z.ie!=s:z.ie=s;z.ib=""
    if len(z.ib)<5 and not(k==92 and "." in z.ib):z.ib+=KD[k];setv(s)
  elif k==64:
    if z.ie==s and z.ib:z.ib=z.ib[:-1];setv(s)
    else:z.t[s]=0;z.ie=-1
  elif (k==84 or k==85) and t>1 and t<5:
    z.ie=-1;v=fa(z.v[s],(1 if k==84 else -1,1))
    if v[0]>0 or (t==4 and v[0]==0):z.v[s]=v
  elif k==95 and z.ie==s:z.ie=-1;de(s);panel();return   # EXE ends typing
  elif k==95 and t>3:z.f[s]=1-z.f[s]
  else:return
  upd(s)
def splash():
  clear_screen();draw_string(110,20,"CIRCUIT SOLVER",AC,"large")
  for i,s in ((0,"Build a DC circuit with the arrow keys and OK."),(1,"Every current, voltage and power is solved"),(2,"exactly, as fractions, while you edit.")):
    draw_string(40,58+i*14,s,TX,"small")
  rc(142,118,100,24,WC);rc(143,119,98,22,BG)   # tobias-jermain / CG100-Tools badge
  draw_string(147,121,"tobias-jermain",WC,"small");draw_string(147,131,"/ CG100-Tools",AC,"small")
  draw_string(150,160,"EXE: START",RD,"small");show_screen()
  while getkey()!=95:pass
  while getkey()==95:pass
splash();load()
while 1:
  k=getkey()
  if k!=z.lk:z.lk=k;z.hc=0;nw=1
  else:z.hc+=1;nw=k in (14,23,25,34) and z.hc>HOLD and z.hc%3==0
  if nw and k:key(k)
  anim();show_screen();dly(SPD)
