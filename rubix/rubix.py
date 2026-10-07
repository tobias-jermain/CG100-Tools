# RUBIX for Casio fx-CG100 (MicroPython 1.9.4, casioplot): 3D 2x2 / 3x3 cube with a solver.
# Home: UP/DOWN = choose, EXE = open. Cube: LEFT/RIGHT = pick, UP/EXE = turn clockwise or do, DOWN = anticlockwise, AC = quit.
from casioplot import *
from random import randint
ST=3;SA=0;SL=(11,20);HI=300
# ST = animation step (1 smoothest, 2 smooth, 3 quick, 6 no animation), SA = 1 animates scrambles, SL = 2x2/3x3 scramble lengths,
# HI = pause between turns of the cube on the home screen
W=384;H=192;BK=(0,0,0);WH=(255,255,255);TX=(30,34,60);GY=(110,114,140);HL=(255,196,40);PL=(242,244,250);LN=(222,226,238)
CO=((255,255,255),(214,30,30),(20,160,70),(250,214,0),(255,124,0),(24,78,214))   # U R F D L B
FA="URFDLB";AX=(1,0,2,1,0,2);SG=(1,1,1,-1,-1,-1)
VR=(196,0,-165);VU=(-82,222,-98);VD=(143,128,170)   # screen right, screen up, towards you (x256)
CS=(256,247,222,181,128,66,0);CX=100;CY=88   # cos of 0,15..90 degrees (x256), cube centre on screen
PA=CO+((0,0,0),)   # colour numbers: 0-5 sticker colours, 6 black
YR={"F":"R","R":"B","B":"L","L":"F"}   # turn the cube a quarter about U: slot FR -> RB -> BL -> LF
IT=("U","R","F","D","L","B","MIX","SOLVE","RESET","HOME")
HT=("LEFT / RIGHT   pick a menu item","UP or EXE   turn clockwise, or do it","DOWN   turn anticlockwise",   # HOW TO page
  "MIX scrambles, SOLVE works it out and plays it","EXE during a solve skips to the end","HOME goes back here","Time your own solves with RUBIXTIMER.PY")
HM=(("3X3 CUBE","Scramble, turn and solve",2),("2X2 CUBE","The pocket cube",1),("HOW TO","Controls and tips",5))
SN=("CROSS","1ST LAYER","2ND LAYER","EDGE FLIP","CORNER TWIST","CORNER SWAP","EDGE SWAP")
class Z:pass
z=Z();z.lk=0;z.sel=0;z.hm=0;z.ps=0;z.rk=0;z.sol=[];z.msg="";z.ms=[];z.mi=0;z.st=-1
def dv(a,b):   # a/b without // (binary long division)
  q=0;k=0
  while (b<<(k+1))<=a:k+=1
  while k>=0:
    if (b<<k)<=a:a-=b<<k;q|=1<<k
    k-=1
  return q
RC=[0]+[dv(65536,v) for v in range(1,200)]
def rc(x,y,w,h,c):
  for j in range(y,y+h):
    for i in range(x,x+w):set_pixel(i,j,c)
def rot(v,a):x,y,w=v;return ([x,-w,y],[w,y,-x],[-y,x,w])[a]   # +90 degrees about axis a
def cmp(a,b):return [b[a[i]] for i in range(len(a))]   # map a then map b
def mp(s):   # "R U2 R'" -> move numbers (face*3 + quarter turns-1)
  return [FA.find(t[0])*3+(1 if t[-1]=="2" else 2 if t[-1]=="'" else 0) for t in s.split()]
def nm(m):f=dv(m,3);return FA[f]+("","2","'")[m-3*f]
def ent(s,f=-1):   # alphabet entry: (combined sticker map, face for pruning, moves)
  ms=mp(s);c=list(range(z.T))
  for m in ms:c=cmp(c,z.M[m])
  return (c,f,ms)
def yr(s,k):
  for i in range(k):s="".join([YR.get(ch,ch) for ch in s])
  return s
def build(n):
  z.n=n;z.S=dv(48,n);P=[];IX={};z.T=T=6*n*n
  for f in range(6):
    a=AX[f];s=SG[f];o=[k for k in range(3) if k!=a]
    for i in range(n):
      for j in range(n):
        v=[0,0,0];v[a]=s*n;v[o[0]]=2*i-n+1;v[o[1]]=2*j-n+1;IX[tuple(v)]=len(P);P.append(v)
  z.P=P;z.M=[];z.F=[f for f in range(6) for k in range(n*n)];z.C=list(z.F);cb={};ce=[]
  for f in range(6):
    a=AX[f];s=SG[f];m=[]
    for p in P:
      q=p
      if p[a]*s>=n-1:
        for t in range(1 if s<0 else 3):q=rot(q,a)
      m.append(IX[tuple(q)])
    m2=cmp(m,m);z.M+=[m,m2,cmp(m2,m)]
  for i in range(T):   # stickers on the same piece share a centre
    c=list(P[i]);c[AX[z.F[i]]]=SG[z.F[i]]*(n-1);c=tuple(c);ce.append(c)
    cb[c]=cb.get(c,[])+[i]
  z.CU=[cb[c] for c in ce]
  z.HK=[key(z.C,i) for i in range(T)];z.Q=[[c*z.S for c in p] for p in P]
  g=dv(12,n)+1;z.g=g-1;z.NT=[];z.NO=[]   # net position of each sticker
  for i in range(T):
    x,y,w=P[i];f=z.F[i];h=n-1
    u,v=((x,w),(-w,-y),(x,-y),(x,-w),(w,-y),(-x,-y))[f];ox,oy=((1,0),(2,1),(1,1),(1,2),(0,1),(3,1))[f]
    a=204+ox*(g*n+2);b=26+oy*(g*n+2);z.NT.append((a+g*((u+h)>>1),b+g*((v+h)>>1)))
    if (u+h)+(v+h)==0:z.NO.append((a-1,b-1))
  def sel(c):return [i for i in range(T) if c(P[i],z.F[i])]
  ed=lambda p,a:(p[0]==0)+(p[1]==0)+(p[2]==0)==1;cn=lambda p,a:(p[0]!=0)*(p[1]!=0)*(p[2]!=0)
  z.DE=sel(lambda p,f:f==3 and ed(p,f));z.DC=sel(lambda p,f:f==3 and cn(p,f))
  z.ME=sel(lambda p,f:(f==2 or f==5) and p[1]==0 and ed(p,f))
  z.UE=sel(lambda p,f:f==0 and ed(p,f));z.UC=sel(lambda p,f:f==0 and cn(p,f))
  z.A18=[ent(nm(m),dv(m,3)) for m in range(18)]
  U3=[ent(s,0) for s in ("U","U2","U'")]
  z.AC=U3+[ent(yr(s,k)) for k in range(4) for s in ("R U R'","F' U' F","R U2 R' U' R U R'")]
  z.AE=U3+[ent(yr(s,k)) for k in range(4) for s in ("U R U' R' U' F' U F","U' F' U F U R U' R'")]
  z.AO=U3+[ent("F R U R' U' F'"),ent("F U R U' R' F'")]   # flip edges
  z.AT=U3+[ent(s) for s in ("R U R' U R U2 R'","R U2 R' U' R U' R'","R U R' U R U' R' U R U2 R'","R U2 R2 U' R2 U' R2 U2 R",
    "R2 D R' U2 R D' R' U2 R'","R U R' U' R' F R F'","F R' F' R U R U' R'")]   # twist corners (Sune, H, Pi, U, T, L)
  z.AN=U3+[ent(yr(s,k)) for k in range(4) for s in ("R' F R' B2 R F' R' B2 R2","R2 B2 R F R' B2 R F' R")]   # A-perms
  z.AP=U3+[ent(yr(s,k)) for k in range(4) for s in ("R U' R U R U R U' R' U' R2","R2 U R U R' U' R' U' R' U R'")]   # U-perms
def key(c,i):return sum([1<<c[q] for q in z.CU[i]])
def app(c,m):
  r=[0]*z.T
  for i in range(z.T):r[m[i]]=c[i]
  return r
def find(c,h):
  for p in range(z.T):
    if c[p]==z.F[h] and key(c,p)==z.HK[h]:return p
def dfs(ps,G,A,d,l):
  if d==0:return all([ps[i] in G[i] for i in range(len(ps))])
  for e in A:
    if e[1]>=0 and (e[1]==l or e[1]+3==l):continue   # same face twice, or opposite faces both ways
    m=e[0]
    if dfs([m[p] for p in ps],G,A,d-1,e[1]):z.fd.insert(0,e);return 1
  return 0
def stage(tg,A,dm,si,d0=0):   # tg = (home sticker, positions it may end in); keeps solved pieces in place
  tg=[(h,(h,)) for h in z.dn]+tg;ps=[find(z.W,h) for h,g in tg];G=[g for h,g in tg];z.fd=[]
  for d in range(d0,dm+1):
    if dfs(ps,G,A,d,-1):
      for e in z.fd:
        for m in e[2]:z.W=app(z.W,z.M[m]);add(m,si)
      return 1
def pcs(hs,A,dm,si,m):   # place pieces one at a time, cheapest first
  while hs:
    bar("SOLVING: "+m);d=0;h=-1
    while h<0 and d<=dm:
      for c in hs:
        if stage([(c,(c,))],A,d,si,d):h=c;break
      d+=1
    if h<0:z.msg="NO SOLUTION";return
    z.dn.append(h);hs=[c for c in hs if c!=h]
def add(m,si):   # append a move, merging turns of the same face
  s=z.sol
  if s and dv(s[-1][0],3)==dv(m,3):
    f=dv(m,3)*3;k=(s[-1][0]+m-2*f+2)%4
    z.sol=s[:-1] if k==0 else s[:-1]+[(f+k-1,s[-1][1])]
  else:s.append((m,si))
def solve():
  z.W=list(z.C);z.sol=[];z.dn=[];z.msg="";bar("SOLVING...")
  if z.n==3:pcs(z.DE,z.A18,5,0,"CROSS")
  pcs(z.DC,z.AC,3,1,"CORNERS")
  if z.n==3:pcs(z.ME,z.AE,3,2,"EDGES");bar("SOLVING: LAST LAYER");stage([(h,tuple(z.UE)) for h in z.UE],z.AO,5,3)
  bar("SOLVING: LAST LAYER");stage([(h,tuple(z.UE)) for h in z.UE]+[(h,tuple(z.UC)) for h in z.UC],z.AT,5,4)
  stage([(h,(h,)) for h in z.UC],z.AN,3,5);z.dn+=z.UC
  if z.n==3:stage([(h,(h,)) for h in z.UE],z.AP,3,6)
def tr(p,a,c,s):x,y,w=p;return [x,(y*c-w*s)>>8,(y*s+w*c)>>8] if a==0 else [(w*s+x*c)>>8,y,(w*c-x*s)>>8] if a==1 else [(x*c-y*s)>>8,(x*s+y*c)>>8,w]   # rotate about axis a (cos c, sin s, x256)
def pj(p):return (CX+((p[0]*VR[0]+p[2]*VR[2])>>8),CY-((p[0]*VU[0]+p[1]*VU[1]+p[2]*VU[2])>>8))
def vis(b,t,r):n=[0,0,0];n[b]=t*256;n=tr(n,r[0],r[1],r[2]);return n[0]*VD[0]+n[1]*VD[1]+n[2]*VD[2]>0
def put(r,a,b,c,u):   # add run a..b of colour c to a row of runs; u = only where empty (it is behind)
  if not r or a>r[-1][1]:return r+[(a,b,c)]
  if not u and a<=r[0][0] and b>=r[-1][1]:return [(a,b,c)]
  L=[];R=[];x=a
  for t in r:
    if t[1]<a:L.append(t)
    elif t[0]>b:R.append(t)
    elif u:
      if t[0]>x:L.append((x,t[0]-1,c))
      L.append(t);x=t[1]+1
    else:
      if t[0]<a:L.append((t[0],a-1,t[2]))
      if t[1]>b:R.append((b+1,t[1],t[2]))
  if not u:L.append((a,b,c))
  elif x<=b:L.append((x,b,c))
  return L+R
def fill(p,c,u):   # convex quad into the frame being built
  t=min(p[0][1],p[1][1],p[2][1],p[3][1]);b=-min(-p[0][1],-p[1][1],-p[2][1],-p[3][1]);L=[999]*(b-t+1);R=[-999]*(b-t+1);F=z.nb
  for i in range(4):
    x0,y0=p[i];x1,y1=p[i-3]
    if y0>y1:x0,y0,x1,y1=x1,y1,x0,y0
    d=y1-y0;k=(x1-x0)*RC[d]
    for y in range(y0,y1+1):
      x=x0+(((y-y0)*k+32768)>>16) if d else x0;j=y-t
      a=x1 if d==0 and x1<x else x;e=x1 if d==0 and x1>x else x;L[j]=a if a<L[j] else L[j];R[j]=e if e>R[j] else R[j]
  for y in range(t,b+1):F[y]=put(F[y],L[y-t],R[y-t],c,u)
def box(lo,hi,r,st,u):   # a block: black sides, stickers on top (u = draw it behind what is there)
  q=[];h=(z.S*7)>>3;v=[vis(AX[f],SG[f],r) for f in range(6)]
  for b in range(3):
    for t in (-1,1):
      if vis(b,t,r):
        cn=[(lo[k]+hi[k])>>1 for k in range(3)];cn[b]=hi[b] if t>0 else lo[b];o1=b+1-3*(b>1);o2=b+2-3*(b>0)
        q.append((cn,b,(hi[o1]-lo[o1])>>1,(hi[o2]-lo[o2])>>1,6))
  for i in st:
    if v[z.F[i]]:q.append((z.Q[i],AX[z.F[i]],h,h,z.C[i]))
  if u:q.reverse()
  for cn,b,e1,e2,c in q:
    o1=b+1-3*(b>1);o2=b+2-3*(b>0);ps=[]
    for d1,d2 in ((-1,-1),(1,-1),(1,1),(-1,1)):p=list(cn);p[o1]+=d1*e1;p[o2]+=d2*e2;ps.append(pj(tr(p,r[0],r[1],r[2])))
    fill(ps,c,u)
def cube(f=-1,q=1,k=0):   # draw the cube, face f turned k steps of 15 degrees (q=1 clockwise)
  n=z.n;E=n*z.S;lo=[-E]*3;hi=[E]*3;I=(0,256,0)
  if f<0:z.nb=[[] for y in range(H)];box(lo,hi,I,range(z.T),0);return show()
  a=AX[f];s=SG[f];c=s*(n-2)*z.S;l2=list(lo);h2=list(hi)
  if s>0:l2[a]=c;hi[a]=c
  else:h2[a]=c;lo[a]=c
  if z.rk!=[f]+z.C:   # the rest of the cube stays still during a turn: build it once
    z.rk=[f]+z.C;z.sl=[];rs=[]
    for i in range(z.T):(z.sl if z.P[i][a]*s>=n-1 else rs).append(i)
    z.nb=[[] for y in range(H)];box(lo,hi,I,rs,0);z.rb=z.nb
  z.nb=list(z.rb);box(l2,h2,(a,CS[k],-s*q*CS[6-k]),z.sl,s<0);show()
def show(sp=set_pixel):   # write only the pixels that differ from the last frame
  O=z.fb;N=z.nb
  for y in range(H-17):
    o=O[y];n=N[y]
    if o!=n:
      P=[];i=0;j=0;lo=len(o);ln=len(n)
      for t in o+n:P+=[t[0],t[1]+1]
      P.sort()
      for t in range(len(P)-1):
        a=P[t];b=P[t+1]
        if a<b:
          while i<lo and o[i][1]<a:i+=1
          while j<ln and n[j][1]<a:j+=1
          co=o[i][2] if i<lo and o[i][0]<=a else -1;cn=n[j][2] if j<ln and n[j][0]<=a else -1
          if co!=cn:
            c=PA[cn] if cn>=0 else WH
            for x in range(a,b):sp(x,y,c)
  z.fb=N;show_screen()
def net(a=0):   # flat net; redraws only stickers that changed (a = all)
  g=z.g
  if a:z.nc=[-1]*z.T
  for x,y in z.NO*a:rc(x,y,z.n*(g+1)+1,z.n*(g+1)+1,BK)
  for i in range(z.T):
    if z.nc[i]!=z.C[i]:x,y=z.NT[i];rc(x,y,g,g,CO[z.C[i]]);z.nc[i]=z.C[i]
def tx(i,x,y,s,c=TX):   # text that changes: clear just the old text, then write the new
  if z.tx[i]!=s:rc(x,y,min(len(z.tx[i])*8,W-x),12,WH);draw_string(x,y,s,c,"small");z.tx[i]=s
def bar(m=None,e=1):   # menu bar along the bottom, m = status message, e = only redraw what changed
  x=2;rc(0,H-17,W,1,TX)
  for i in range(len(IT)):
    t=IT[i];w=len(t)*7+8;ch=i==z.sel or i==z.ps
    if ch:rc(x,H-15,w,14,HL if i==z.sel else WH)
    if ch or not e:draw_string(x+4,H-14,t,TX,"small")
    x+=w+2
  z.ps=z.sel
  if m:tx(3,200,141,m)
  show_screen()
def info():   # step, move counter, next moves and message
  x=z.mi-1 if z.mi>0 else 0;t=" ".join([nm(m) for m,i in z.ms[x:x+6]])
  e=z.st>=0;tx(0,200,96,SN[z.st] if e else "");tx(1,200,110,"MOVE "+str(z.mi)+"/"+str(len(z.ms)) if e else "",GY);tx(2,200,124,t);tx(3,200,141,z.msg)
def blank():clear_screen();z.fb=[[] for y in range(H)];z.tx=[""]*4
def scr():
  blank();cube();net(1);draw_string(200,4,"RUBIX "+str(z.n)+"X"+str(z.n),TX);draw_string(320,8,"3D SOLVER",GY,"small");info();bar(None,0)
def turn(m,an=1):   # do move m, animating each quarter turn (the 90 degree frame is the finished turn)
  f=dv(m,3);k=m-f*3;q=-1 if k==2 else 1
  for t in range(2 if k==1 else 1):
    for s in range(ST,7*an,ST):cube(f,q,s)
    z.C=app(z.C,z.M[f*3+(2 if q<0 else 0)])
  if an:net();show_screen()
def done():return all([z.C[i]==z.C[i-i%(z.n*z.n)] for i in range(z.T)])
def keys():
  while 1:
    k=getkey()
    if k!=z.lk:
      z.lk=k
      if k in (14,23,25,34,95):return k
def play():
  z.ms=z.sol;z.mi=0;sk=0
  for m,si in z.ms:
    z.st=si;z.mi+=1;info() if not sk else 0
    k=getkey();sk=sk or (k==95 and z.lk!=95);z.lk=k   # a new EXE press skips to the end
    turn(m,1-sk)
  z.msg="SOLVED IN "+str(len(z.ms))+" MOVES" if done() else z.msg;scr()
def mix():
  l=-1;z.ms=[];z.st=-1;z.mi=0
  for i in range(SL[z.n-2]):
    f=randint(0,5)
    while f==l:f=randint(0,5)
    l=f;turn(f*3+randint(0,2),SA)
  z.msg="SCRAMBLED";scr()
def run():
  scr()
  while 1:
    k=keys();s=z.sel;z.msg=""
    if k==23 or k==25:z.sel=(s+(1 if k==25 else -1))%len(IT);bar();continue
    if s<6:z.ms=[];z.st=-1;info();turn(s*3+(2 if k==34 else 0))
    elif k==34:continue
    elif s==6:mix()
    elif s==7:
      if done():z.msg="ALREADY SOLVED";scr()
      else:solve();play()
    elif s==8:z.C=list(z.F);z.ms=[];z.st=-1;scr()
    else:return
def stripe(x,y):   # thin bar in the cube colours
  for i in range(5):rc(x+i*33,y,31,3,CO[(1,4,3,2,5)[i]])
def card(i,on):   # home menu card, dark when picked
  y=58+i*38;t,d,c=HM[i];rc(212,y,166,32,TX if on else PL);rc(212,y,4,32,CO[c] if on else LN)
  for a,b in ((212,y),(377,y),(212,y+31),(377,y+31)):set_pixel(a,b,WH)
  draw_string(226,y+4,t,WH if on else TX);draw_string(226,y+19,d,(176,182,206) if on else GY,"small")
  if on:draw_string(362,y+10,">",HL)
def foot(t):rc(0,H-17,W,1,LN);draw_string(8,H-13,"tobias-jermain / CG100-Tools",GY,"small");draw_string(260,H-13,t,GY,"small")
def hdraw():
  blank();draw_string(212,6,"RUBIX",TX,"large");stripe(212,30);draw_string(212,38,"3D CUBE SOLVER",GY,"small")
  for i in range(3):card(i,i==z.hm)
  foot("UP/DOWN  EXE OPEN");cube()
def help():
  clear_screen();draw_string(16,6,"HOW TO",TX,"large");stripe(16,30)
  for i,t in enumerate(HT):draw_string(16,42+i*17,t,TX,"small")
  foot("EXE  BACK");show_screen();keys()
def home():   # home menu; the cube turns R U R' U' while you choose
  hdraw();t=0;j=0
  while 1:
    k=getkey();t+=1
    if k!=z.lk:
      z.lk=k
      if k==14 or k==34:card(z.hm,0);z.hm=(z.hm+(1 if k==34 else -1))%3;card(z.hm,1);show_screen()
      if k==95 and z.hm==2:help();hdraw()
      elif k==95:return 3-z.hm
    if t>=HI:
      m=(3,0,5,2)[j];j=(j+1)%4;t=0
      for s in range(ST,7,ST):cube(dv(m,3),1-(m%3),s)
      z.C=app(z.C,z.M[m])
clear_screen();draw_string(150,86,"LOADING...",BK);show_screen();build(3)
while 1:
  n=home();card(z.hm,1);draw_string(300,72+z.hm*38,"LOADING",HL,"small");show_screen()
  build(n) if n!=z.n else 0;z.C=list(z.F);z.sel=0;z.ms=[];z.st=-1;z.msg="";run()
