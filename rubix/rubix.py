# RUBIX for Casio fx-CG100 (MicroPython 1.9.4, casioplot): 3D 2x2 / 3x3 cube with a solver.
# Home: UP/DOWN = choose, EXE = open. Cube: LEFT/RIGHT = pick, UP/EXE = turn clockwise or do, DOWN = anticlockwise, AC = quit.
from casioplot import *
from random import randint
ST=2;SA=0;SL=(11,20);HI=300
# ST = animation step (1 smoothest, 2, 3 or 6 fastest), SA = 1 animates scrambles, SL = 2x2/3x3 scramble lengths,
# HI = pause between turns of the cube on the home screen
W=384;H=192;BK=(0,0,0);WH=(255,255,255);TX=(30,34,60);GY=(110,114,140);HL=(255,196,40);PL=(242,244,250);LN=(222,226,238)
CO=((255,255,255),(214,30,30),(20,160,70),(250,214,0),(255,124,0),(24,78,214))   # U R F D L B
FA="URFDLB";AX=(1,0,2,1,0,2);SG=(1,1,1,-1,-1,-1)
VR=(196,0,-165);VU=(-82,222,-98);VD=(143,128,170)   # screen right, screen up, towards you (x256)
CS=(256,247,222,181,128,66,0)   # cos of 0,15..90 degrees (x256)
CX=100;CY=88
YR={"F":"R","R":"B","B":"L","L":"F"}   # turn the cube a quarter about U: slot FR -> RB -> BL -> LF
IT=("U","R","F","D","L","B","MIX","SOLVE","RESET","HOME")
HM=(("3X3 CUBE","Scramble, turn and solve",2),("2X2 CUBE","The pocket cube",1),("HOW TO","Controls and tips",5))
SN=("CROSS","1ST LAYER","2ND LAYER","EDGE FLIP","CORNER TWIST","CORNER SWAP","EDGE SWAP")
class Z:pass
z=Z();z.lk=0;z.sel=0;z.hm=0;z.sol=[];z.msg="";z.ms=[];z.mi=0;z.st=-1
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
def nm(m):
  f=0
  while m>=3:m-=3;f+=1
  return FA[f]+("","2","'")[m]
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
  z.P=P;z.M=[];z.C=[];z.F=[];cb={}
  for f in range(6):
    a=AX[f];s=SG[f];m=[]
    for k in range(n*n):z.C.append(f);z.F.append(f)
    for p in P:
      q=p
      if p[a]*s>=n-1:
        for t in range(1 if s<0 else 3):q=rot(q,a)
      m.append(IX[tuple(q)])
    m2=cmp(m,m);z.M+=[m,m2,cmp(m2,m)]
  ce=[]
  for i in range(T):   # stickers on the same piece share a centre
    c=list(P[i]);c[AX[z.F[i]]]=SG[z.F[i]]*(n-1);c=tuple(c);ce.append(c)
    cb[c]=cb.get(c,[])+[i]
  z.CU=[cb[c] for c in ce]
  z.HK=[key(z.C,i) for i in range(T)]
  z.Q=[[c*z.S for c in p] for p in P]
  g=dv(12,n)+1;z.NT=[];z.NO=[]   # net position of each sticker
  for i in range(T):
    x,y,w=P[i];f=z.F[i];h=n-1
    u,v=((x,w),(-w,-y),(x,-y),(x,-w),(w,-y),(-x,-y))[f];ox,oy=((1,0),(2,1),(1,1),(1,2),(0,1),(3,1))[f]
    a=204+ox*(g*n+2);b=26+oy*(g*n+2);z.NT.append((a+g*((u+h)>>1),b+g*((v+h)>>1)))
    if (u+h)+(v+h)==0:z.NO.append((a-1,b-1))
  z.g=g-1
  def sel(c):return [i for i in range(T) if c(P[i],z.F[i])]
  def ed(p,a):return (p[0]==0)+(p[1]==0)+(p[2]==0)==1
  def cn(p,a):return (p[0]!=0)*(p[1]!=0)*(p[2]!=0)
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
  tg=[(h,(h,)) for h in z.dn]+tg;ps=[find(z.W,h) for h,g in tg];G=[g for h,g in tg]
  for d in range(d0,dm+1):
    z.fd=[]
    if dfs(ps,G,A,d,-1):
      for e in z.fd:
        for m in e[2]:z.W=app(z.W,z.M[m]);add(m,si)
      return 1
def pcs(hs,A,dm,si,m):   # place pieces one at a time, cheapest first
  hs=list(hs)
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
    if k==0:z.sol=s[:-1]
    else:s[-1]=(f+k-1,s[-1][1])
  else:s.append((m,si))
def solve():
  z.W=list(z.C);z.sol=[];z.dn=[];z.msg="";bar("SOLVING...")
  if z.n==3:pcs(z.DE,z.A18,5,0,"CROSS")
  pcs(z.DC,z.AC,3,1,"CORNERS")
  if z.n==3:pcs(z.ME,z.AE,3,2,"EDGES");bar("SOLVING: LAST LAYER");stage([(h,tuple(z.UE)) for h in z.UE],z.AO,5,3)
  bar("SOLVING: LAST LAYER");stage([(h,tuple(z.UE)) for h in z.UE]+[(h,tuple(z.UC)) for h in z.UC],z.AT,5,4)
  stage([(h,(h,)) for h in z.UC],z.AN,3,5);z.dn+=z.UC
  if z.n==3:stage([(h,(h,)) for h in z.UE],z.AP,3,6)
def tr(p,a,c,s):   # rotate point p about axis a (cos c, sin s, x256)
  x,y,w=p
  if a==0:return [x,(y*c-w*s)>>8,(y*s+w*c)>>8]
  if a==1:return [(w*s+x*c)>>8,y,(w*c-x*s)>>8]
  return [(x*c-y*s)>>8,(x*s+y*c)>>8,w]
def pj(p):return (CX+((p[0]*VR[0]+p[2]*VR[2])>>8),CY-((p[0]*VU[0]+p[1]*VU[1]+p[2]*VU[2])>>8))
def vis(b,t,r):n=[0,0,0];n[b]=t*256;n=tr(n,r[0],r[1],r[2]);return n[0]*VD[0]+n[1]*VD[1]+n[2]*VD[2]>0
def fill(p,col,sp=set_pixel):   # convex quad
  t=min(p[0][1],p[1][1],p[2][1],p[3][1]);b=-min(-p[0][1],-p[1][1],-p[2][1],-p[3][1]);L=[999]*(b-t+1);R=[-999]*(b-t+1)
  for i in range(4):
    x0,y0=p[i];x1,y1=p[i-3]
    if y0>y1:x0,y0,x1,y1=x1,y1,x0,y0
    d=y1-y0;k=(x1-x0)*RC[d]
    for y in range(y0,y1+1):
      x=x0+(((y-y0)*k+32768)>>16) if d else x0;j=y-t
      a=x1 if d==0 and x1<x else x;e=x1 if d==0 and x1>x else x;L[j]=a if a<L[j] else L[j];R[j]=e if e>R[j] else R[j]
  for y in range(t,b+1):
    for x in range(L[y-t],R[y-t]+1):sp(x,y,col)
def ln(a,b,sp=set_pixel):   # black line
  x0,y0=a;dx=b[0]-x0;dy=b[1]-y0;n=abs(dx) if abs(dx)>abs(dy) else abs(dy);r=RC[n]
  for i in range(n+1):sp(x0+((dx*i*r+32768)>>16),y0+((dy*i*r+32768)>>16),BK)
def quad(cn,b,e1,e2,r,col,o=0):   # filled side of a block or sticker, o = outline it
  o1=b+1-3*(b>1);o2=b+2-3*(b>0);ps=[]
  for d1,d2 in ((-1,-1),(1,-1),(1,1),(-1,1)):p=list(cn);p[o1]+=d1*e1;p[o2]+=d2*e2;ps.append(pj(tr(p,r[0],r[1],r[2])))
  fill(ps,col)
  if o:
    for i in range(4):ln(ps[i],ps[i-3])
def box(lo,hi,r,st):   # inner (cut) sides of a block in black, then the stickers on its visible sides
  E=z.n*z.S
  for b in range(3):
    for t in (-1,1):
      if vis(b,t,r) and (hi[b] if t>0 else -lo[b])!=E:
        cn=[(lo[k]+hi[k])>>1 for k in range(3)];cn[b]=hi[b] if t>0 else lo[b];o1=b+1-3*(b>1);o2=b+2-3*(b>0)
        quad(cn,b,(hi[o1]-lo[o1])>>1,(hi[o2]-lo[o2])>>1,r,BK)
  h=z.S
  for i in st:
    f=z.F[i]
    if vis(AX[f],SG[f],r):quad(z.Q[i],AX[f],h,h,r,CO[z.C[i]],1)
def cube(f=-1,q=1,k=0):   # draw the cube, face f turned k steps of 15 degrees (q=1 clockwise)
  n=z.n;E=n*z.S;lo=[-E]*3;hi=[E]*3
  if f<0:box(lo,hi,(0,256,0),range(z.T));return
  a=AX[f];s=SG[f];c=s*(n-2)*z.S;sl=[];rs=[]
  for i in range(z.T):(sl if z.P[i][a]*s>=n-1 else rs).append(i)
  l2=list(lo);h2=list(hi)
  if s>0:l2[a]=c;hi=list(hi);hi[a]=c
  else:h2[a]=c;lo=list(lo);lo[a]=c
  r=(a,CS[k],-s*q*CS[6-k])
  if s<0:box(l2,h2,r,sl)
  box(lo,hi,(0,256,0),rs)
  if s>0:box(l2,h2,r,sl)
def net():
  g=z.g
  for x,y in z.NO:rc(x,y,z.n*(g+1)+1,z.n*(g+1)+1,BK)
  for i in range(z.T):x,y=z.NT[i];rc(x,y,g,g,CO[z.C[i]])
def bar(m=None,e=1):   # menu bar along the bottom, m = status message, e = erase first
  if e:rc(0,H-16,W,16,WH)
  rc(0,H-17,W,1,TX);x=2
  for i in range(len(IT)):
    t=IT[i];w=len(t)*7+8
    if i==z.sel:rc(x,H-15,w,14,HL)
    draw_string(x+4,H-14,t,TX,"small");x+=w+2
  if m:rc(196,140,188,14,WH);draw_string(200,141,m,TX,"small")
  show_screen()
def scr(f=-1,q=1,k=0):
  clear_screen();cube(f,q,k);net()
  draw_string(200,4,"RUBIX "+str(z.n)+"X"+str(z.n),TX);draw_string(320,8,"3D SOLVER",GY,"small")
  if z.st>=0:draw_string(200,96,SN[z.st],TX,"small");draw_string(200,110,"MOVE "+str(z.mi)+"/"+str(len(z.ms)),GY,"small")
  t="";x=z.mi-1 if z.mi>0 else 0
  for j in range(x,len(z.ms)):
    if len(t)>22:break
    t+=nm(z.ms[j][0])+" "
  if z.ms:draw_string(200,124,t,TX,"small")
  if z.msg:draw_string(200,141,z.msg,TX,"small")
  bar(None,0)
def turn(m,an=1):   # do move m, animating each quarter turn
  f=dv(m,3);k=m-f*3;q=-1 if k==2 else 1
  for t in range(2 if k==1 else 1):
    if an:
      for s in range(ST,6,ST):scr(f,q,s)
    z.C=app(z.C,z.M[f*3+(2 if q<0 else 0)])
  if an:scr()
def done():
  for i in range(z.T):
    if z.C[i]!=z.C[i-i%(z.n*z.n)]:return 0
  return 1
def keys():
  while 1:
    k=getkey()
    if k!=z.lk:
      z.lk=k
      if k in (14,23,25,34,95):return k
def play():
  z.ms=z.sol;z.mi=0;sk=0
  for m,si in z.ms:
    z.st=si;z.mi+=1
    k=getkey()
    if k==95 and z.lk!=95:sk=1   # a new EXE press skips to the end
    z.lk=k
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
    if s<6:z.ms=[];z.st=-1;turn(s*3+(2 if k==34 else 0))
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
  clear_screen();draw_string(212,6,"RUBIX",TX,"large");stripe(212,30);draw_string(212,38,"3D CUBE SOLVER",GY,"small")
  for i in range(3):card(i,i==z.hm)
  foot("UP/DOWN  EXE OPEN");cube();show_screen()
def help():
  clear_screen();draw_string(16,6,"HOW TO",TX,"large");stripe(16,30)
  for i,t in enumerate(("LEFT / RIGHT   pick a menu item","UP or EXE   turn clockwise, or do it","DOWN   turn anticlockwise",
    "MIX scrambles, SOLVE works it out and plays it","EXE during a solve skips to the end","HOME goes back here","Time your own solves with RUBIXTIMER.PY")):
    draw_string(16,42+i*17,t,TX,"small")
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
      for s in range(ST,7,ST):rc(8,0,200,H-18,WH);cube(dv(m,3),1-(m%3),s);show_screen()
      z.C=app(z.C,z.M[m])
clear_screen();draw_string(150,86,"LOADING...",BK);show_screen()
build(3)
while 1:
  n=home();card(z.hm,1);draw_string(300,72+z.hm*38,"LOADING",HL,"small");show_screen()
  if n!=z.n:build(n)
  z.C=list(z.F);z.sel=0;z.ms=[];z.st=-1;z.msg="";run()
