# FLAPPY BIRD for Casio fx-CG100 (MicroPython 1.9.4, casioplot)
# EXE/UP = flap, DOWN = pause, AC = quit. SPD = extra delay per frame,
# MS = move pipes/ground every MS frames (2-3 = faster, but steppier).
# Y1,Y2 = where the blue sky fades to white (set both to GY for a full blue sky, slower to load).
from casioplot import *
from random import randint
SPD=2000;MS=1
W=384;H=192;GY=172;HY=16;CW=28;CH=10;BX=80;BW=18;BT=11;SP=150;GS=20
SKY=(78,192,202);SK2=(168,224,230);Y1=32;Y2=44;WH=(255,255,255);NV=(30,40,80);RD=(224,62,32)
PO=(84,56,71);PL=(160,224,70);PM=(116,190,45);PD=(84,150,30)
BU=(92,170,60);BL=(130,215,80);CLD=(250,252,252)
GL=(150,220,70);GD=(100,175,45);DT=(222,216,149);DL=(250,245,190)
FK=(95,14);G=7;FL=-84;VM=112;PX=122;PY=44;PW=140;PH=72
BP={'K':PO,'Y':(247,216,66),'W':WH,'R':RD,'B':(250,238,190),'O':(240,150,40)}
BR=(
"....KKKKKK........","..KKYYYYYKKKKK....",".KYYYYYYYKWWWWK...","KYYYYYYYYKWWKKK...",
"KYYYYYYYYYKWWWK...","KYYYYYYYYYYKKKKKKK","KYYYYYYYYYKRRRRRRK","KBBBYYYYYYKKKKKKK.",
".KBBBBBBBBBBBKK...","..KBBBBBBBBBK.....","....KKKKKKKK......")
WG=(".KKKKKK...........",".KOOOOK...........","..KKKK............")
WF=(1,0,1,2)
class Z:pass
z=Z();z.hi=0;z.hd=0;z.pn=0;z.oy=90;z.pp=[];z.go=0
def bs(t):
  g=[]
  for j in range(BT):
    g.append([])
    for i in range(BW):
      g[j].append(BP[BR[j][i]] if BR[j][i]!='.' else 0)
  for j in range(3):
    for i in range(BW):
      if WG[j][i]!='.':g[t+j][i]=BP[WG[j][i]]
  r=[]
  for j in range(BT):
    for i in range(BW):
      if g[j][i]!=0:r.append((i,j,g[j][i]))
  return r
BS=[bs(2),bs(4),bs(6)]
def isq(n):
  r=0
  while (r+1)*(r+1)<=n:r+=1
  return r
BH=[];CT=[];CB=[];T=[]
for x in range(32):d=x-16;T.append(4+((isq(256-d*d)*3)>>3))
for x in range(W):BH.append(T[x%32]);CT.append(0);CB.append(0)
for cx,b in ((50,40),(150,31),(250,42),(340,34)):
  for dx,r in ((-14,10),(0,14),(14,10)):
    for x in range(cx+dx-r,cx+dx+r+1):
      if x>=0 and x<W:
        e=x-cx-dx;t=b-isq(r*r-e*e)
        if CT[x]==0 or t<CT[x]:CT[x]=t;CB[x]=b
def mx(a,b):return a if a>b else b
def rc(x,y,w,h,c):
  for i in range(w):
    for j in range(h):set_pixel(x+i,y+j,c)
def dly(n):
  for i in range(n):pass
def sk(a,b):
  r=[]
  for s,e,c in ((HY,Y1,SKY),(Y1,Y2,SK2),(Y2,GY,WH)):
    s=mx(s,a);e=min(e,b)
    if e>s:r.append((s,e,c))
  return r
def bgl(x):
  t=GY-BH[x];c=CT[x]
  s=sk(HY,c)+[(c,CB[x],CLD)]+sk(CB[x],t) if c else sk(HY,t)
  return s+[(t,t+2,BL),(t+2,GY,BU)]
def bgs(x,a,b):
  r=[]
  for s,e,c in bgl(x):
    s=mx(s,a);e=min(e,b)
    if e>s:r.append((s,e,c))
  return r
def cap(a,e):
  return [(a,a+CH,PO)] if e else [(a,a+1,PO),(a+1,a+3,PL),(a+3,a+7,PM),(a+7,a+9,PD),(a+9,a+10,PO)]
def cs(x,p,g):
  c=x-p[0];t=p[1];b=t+p[2]
  if c<0 or c>=CW:return bgs(x,HY,t)+(bgs(x,t,b) if g else [])+bgs(x,b,GY)
  e=c==0 or c==CW-1;k=PO if c==1 or c==CW-2 else PM
  s=(bgs(x,HY,t-CH) if e else [(HY,t-CH,k)])+cap(t-CH,e)
  if g:s+=bgs(x,t,b)
  return s+cap(b,e)+(bgs(x,b+CH,GY) if e else [(b+CH,GY,k)])
def pa(x,s,y0,y1):
  for a,b,c in s:
    for y in range(mx(a,y0),min(b,y1)):set_pixel(x,y,c)
def col(x,y0,y1):
  s=None
  for p in z.pp:
    if 0<=x-p[0]<CW:s=cs(x,p,1)
  pa(x,s if s else bgs(x,HY,GY),y0,y1)
def rest(x0,x1,y0,y1):
  for x in range(x0,x1):col(x,y0,y1)
def kc(c):return -1 if c<0 or c>=CW else c if c<2 or c>=CW-2 else 2
def mv(v):
  for p in z.pp:
    xo=p[0];xn=xo-v;p[0]=xn
    for x in range(mx(0,xn),min(W,xo+CW)):
      if kc(x-xn)!=kc(x-xo):pa(x,cs(x,p,0),0,H)
def gnd(o,s):
  for x0 in range(-(o%GS),W+GS,GS):
    for x in range(mx(0,x0-s),min(W,x0)):rc(x,GY+1,1,4,GD if (x+o+s)%(2*GS)>=GS else GL)
def hs(e):
  if e:rc(2,2,100,12,NV)
  draw_string(6,3,"SCORE "+str(z.s),WH,"small")
  if e:rc(284,2,98,12,NV)
  draw_string(288,3,"BEST "+str(z.hi),WH,"small")
def drawb():
  by=z.y>>4;rest(BX,BX+BW,z.oy,z.oy+BT);z.oy=by
  for i,j,c in BS[WF[(z.t>>1)&3]]:set_pixel(BX+i,by+j,c)
  show_screen()
def spawn():
  g=mx(46,62-2*(z.s>>2));lo=HY+CH+10;hi=GY-g-CH-10
  z.lt=randint(mx(lo,z.lt-70),min(hi,z.lt+70));z.pp.append([W,z.lt,g,0])
def pause():
  rc(150,2,90,12,NV);draw_string(162,3,"PAUSED",(255,210,60),"small");show_screen()
  while getkey()==34:pass
  while getkey()!=34:pass
  while getkey()==34:pass
  rc(150,2,90,12,NV);show_screen()
def newg():
  old=z.pp;z.pp=[]
  for p in old:rest(mx(0,p[0]),min(W,p[0]+CW),HY,GY)
  if z.pn:rest(PX,PX+PW,PY,PY+PH)
  rest(BX,BX+BW,z.oy,z.oy+BT)
  z.pn=0;z.s=0;z.v=2;z.pb=z.hi;z.lt=70;z.vy=0;z.y=90<<4;z.oy=90;z.fp=1;z.t=0
  hs(z.hd);z.hd=1
def bdg(x,y):
  for a,b,w,h in ((0,0,100,1),(0,23,100,1),(0,0,1,24),(99,0,1,24),(100,2,2,24),(2,24,100,2)):rc(x+a,y+b,w,h,PO)
  rc(x+1,y+1,98,22,WH);draw_string(x+5,y+3,"tobias-jermain",PO,"small");draw_string(x+5,y+13,"/ CG100-Tools",(0,102,204),"small")
def ready():
  draw_string(139,29,"FLAPPY BIRD",WH);draw_string(138,28,"FLAPPY BIRD",NV)
  draw_string(125,56,"EXE / UP : FLAP",PO,"small");draw_string(125,68,"DOWN : PAUSE",PO,"small");bdg(140,86)
  while 1:
    z.t+=1;z.y=(84+abs(z.t%32-16))<<4;drawb();dly(SPD)
    if getkey() in FK:break
  rest(100,300,22,114);z.vy=FL
def play():
  while 1:
    z.t+=1;k=getkey();f=k in FK
    if f and not z.fp:z.vy=FL
    z.fp=f
    if k==34:pause()
    z.vy=min(z.vy+G,VM);z.y=mx(z.y+z.vy,HY<<4)
    if z.y==HY<<4 and z.vy<0:z.vy=0
    if z.t%MS==0:v=z.v*MS;mv(v);gnd(z.go,v);z.go+=v
    if not z.pp or z.pp[-1][0]<=W-SP:spawn()
    if z.pp[0][0]+CW<=0:
      n=[]
      for p in z.pp:
        if p!=z.pp[0]:n.append(p)
      z.pp=n
    by=z.y>>4;dead=by+BT>=GY
    for p in z.pp:
      if p[0]<BX+BW-2 and p[0]+CW>BX+2 and (by+2<p[1] or by+BT-2>p[1]+p[2]):dead=1
      if not p[3] and p[0]+CW<BX:
        p[3]=1;z.s+=1;z.v=2+(z.s>=10)+(z.s>=25);z.hi=mx(z.hi,z.s);hs(1)
    drawb()
    if dead:return
    dly(SPD)
def fall():
  while (z.y>>4)+BT<GY:
    z.vy=min(z.vy+G,VM);z.y=min(z.y+z.vy,(GY-BT)<<4);drawb();dly(SPD)
def medal(x,y):
  s=z.s
  if s<10:return
  c=(205,127,50) if s<20 else (200,205,215) if s<30 else (255,200,40) if s<40 else (120,235,235)
  for j in range(-10,11):
    for i in range(-10,11):
      d=i*i+j*j
      if d<=100:set_pixel(x+i,y+j,PO if d>76 else c)
def over():
  z.pn=1;rc(PX,PY,PW,PH,DT)
  rc(PX,PY,PW,2,PO);rc(PX,PY+PH-2,PW,2,PO);rc(PX,PY,2,PH,PO);rc(PX+PW-2,PY,2,PH,PO)
  draw_string(PX+30,PY+6,"GAME OVER",RD)
  draw_string(PX+10,PY+28,"SCORE "+str(z.s),PO,"small");draw_string(PX+10,PY+42,"BEST "+str(z.hi),PO,"small")
  if z.s>z.pb:draw_string(PX+10,PY+56,"NEW BEST!",RD,"small")
  draw_string(PX+72,PY+56,"EXE:RETRY",PO,"small");medal(PX+PW-30,PY+36);show_screen()
  while getkey() in FK:pass
  while getkey() not in FK:pass
clear_screen()
for x in range(W):
  for a,b,c in bgs(x,HY,GY):
    if c!=WH:
      for y in range(a,b):set_pixel(x,y,c)
rc(0,0,W,HY,NV);rc(0,GY,W,1,PO);rc(0,GY+5,W,1,DL);rc(0,GY+6,W,H-GY-6,DT)
for x in range(W):rc(x,GY+1,1,4,GD if x%(2*GS)>=GS else GL)
while 1:
  newg();ready();play();fall();over()
