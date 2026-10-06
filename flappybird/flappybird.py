# FLAPPY BIRD for Casio fx-CG100 (MicroPython 1.9.4, casioplot)
# EXE/UP = flap, DOWN = pause, AC = quit. SPD = extra delay per frame (0 = fastest),
# MS = move pipes/ground every MS frames (2-3 = faster, but steppier).
from casioplot import *
from random import randint
SPD=0;MS=1
W=384;H=192;GY=172;HY=16;CW=28;CH=10;BX=80;BW=18;BT=11;SP=150;GS=20
SKY=(78,192,202);WH=(255,255,255);NV=(30,40,80);RD=(224,62,32)
PO=(84,56,71);PL=(160,224,70);PM=(116,190,45);PD=(84,150,30)
BU=(92,170,60);BL=(130,215,80);CLD=(240,252,250)
GL=(150,220,70);GD=(100,175,45);DT=(222,216,149);DL=(250,245,190)
HYS=HY<<4;FK=(95,14);G=7;FL=-84;VM=112;PX=122;PY=44;PW=140;PH=72
BP={'K':PO,'Y':(247,216,66),'W':WH,'R':RD,'B':(250,238,190),'O':(240,150,40)}
BR=(
"....KKKKKK........","..KKYYYYYKKKKK....",".KYYYYYYYKWWWWK...","KYYYYYYYYKWWKKK...",
"KYYYYYYYYYKWWWK...","KYYYYYYYYYYKKKKKKK","KYYYYYYYYYKRRRRRRK","KBBBYYYYYYKKKKKKK.",
".KBBBBBBBBBBBKK...","..KBBBBBBBBBK.....","....KKKKKKKK......")
WG=(".KKKKKK...........",".KOOOOK...........","..KKKK............")
WF=(1,0,1,2)
class Z:pass
z=Z();z.hi=0;z.hd=0;z.tv=0;z.tt=[];z.pn=0;z.oy=90;z.pp=[];z.go=0
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
      if g[j][i]!=0:r.append((BX+i,j,g[j][i]))
  return r
BS=[bs(2),bs(4),bs(6)]
LO=[];HI=[]
for j in range(BT):
  a=0;b=BW
  while BR[j][a]=='.':a+=1
  while BR[j][b-1]=='.':b-=1
  LO.append(BX+a);HI.append(BX+b)
def isq(n):
  r=0
  while (r+1)*(r+1)<=n:r+=1
  return r
BH=[];CT=[];CB=[];T=[]
for x in range(32):d=x-16;T.append(4+((isq(256-d*d)*3)>>3))
for x in range(W):BH.append(T[x%32]);CT.append(0);CB.append(0)
for cx,b in ((50,64),(150,46),(250,72),(340,52)):
  for dx,r in ((-14,10),(0,14),(14,10)):
    for x in range(cx+dx-r,cx+dx+r+1):
      if x>=0 and x<W:
        e=x-cx-dx;t=b-isq(r*r-e*e)
        if CT[x]==0 or t<CT[x]:CT[x]=t;CB[x]=b
def mx(a,b):return a if a>b else b
BM=0;BL2=0
for x in range(BX,BX+BW):
  if BH[x]>BM:BM=BH[x]
  if CT[x]:BL2=1
def rc(x,y,w,h,c):
  for i in range(w):
    for j in range(h):set_pixel(x+i,y+j,c)
def dly(n):
  for i in range(n):pass
BC=(0,PO,PM);CP=(PO,PL,PL,PM,PM,PM,PM,PD,PD,PO)
def bgv(x,a,b,sp=set_pixel):
  t=GY-BH[x];c=CT[x];d=CB[x]
  if c==0:c=d=t
  for y in range(a,b if b<c else c):sp(x,y,SKY)
  for y in range(a if a>c else c,b if b<d else d):sp(x,y,CLD)
  for y in range(a if a>d else d,b if b<t else t):sp(x,y,SKY)
  for y in range(a if a>t else t,b if b<t+2 else t+2):sp(x,y,BL)
  for y in range(a if a>t+2 else t+2,b if b<GY else GY):sp(x,y,BU)
def col(x,y0,y1):
  for p in z.pp:
    c=x-p[0]
    if c>=0 and c<CW:
      t=p[1];b=t+p[2];ed=c==0 or c==CW-1;k=PO if c==1 or c==CW-2 else PM
      for a,e,m in ((HY,t-CH,1),(t-CH,t,2),(t,b,0),(b,b+CH,3),(b+CH,GY,1)):
        if a<y0:a=y0
        if e>y1:e=y1
        if e>a:
          if m==0 or (m==1 and ed):bgv(x,a,e)
          elif m==1:
            for y in range(a,e):set_pixel(x,y,k)
          else:
            for y in range(a,e):set_pixel(x,y,PO if ed else CP[y-(t-CH if m==2 else b)])
      return
  bgv(x,y0,y1)
def rest(x0,x1,y0,y1):
  for x in range(x0,x1):col(x,y0,y1)
def mkt(v):
  L=[]
  for c in range(CW+v):
    d=c-v
    bn=0 if c<1 or c>=CW-1 else 1 if c==1 or c==CW-2 else 2
    bo=0 if d<1 or d>=CW-1 else 1 if d==1 or d==CW-2 else 2
    cn=0 if c>=CW else 1 if c==0 or c==CW-1 else 2
    co=0 if d<0 or d>=CW else 1 if d==0 or d==CW-1 else 2
    if bn!=bo or cn!=co:L.append((c,bn if bn!=bo else -1,cn if cn!=co else -1))
  return L
def mv(v,sp=set_pixel):
  if z.tv!=v:z.tt=mkt(v);z.tv=v
  for p in z.pp:
    xn=p[0]-v;p[0]=xn;t=p[1]-CH;b=p[1]+p[2]
    for c,bn,cn in z.tt:
      x=xn+c
      if x<0 or x>=W:continue
      if bn>0:
        k=PO if bn<2 else PM
        for y in range(HY,t):sp(x,y,k)
        for y in range(b+CH,GY):sp(x,y,k)
      elif bn==0:bgv(x,HY,t);bgv(x,b+CH,GY)
      if cn>1:
        for i in range(CH):k=CP[i];sp(x,t+i,k);sp(x,b+i,k)
      elif cn==1:
        for y in range(t,t+CH):sp(x,y,PO)
        for y in range(b,b+CH):sp(x,y,PO)
      elif cn==0:bgv(x,t,t+CH);bgv(x,b,b+CH)
def gnd(o,s,sp=set_pixel):
  for x0 in range(-(o%GS),W+GS,GS):
    k=GD if (x0+o)%(2*GS)>=GS else GL
    for x in range(x0-s if x0>s else 0,x0 if x0<W else W):
      sp(x,GY+1,k);sp(x,GY+2,k);sp(x,GY+3,k);sp(x,GY+4,k)
def hs(e):
  if e:rc(2,2,100,12,NV)
  draw_string(6,3,"SCORE "+str(z.s),WH,"small")
  if e:rc(284,2,98,12,NV)
  draw_string(288,3,"BEST "+str(z.hi),WH,"small")
def drawb(sp=set_pixel):
  by=z.y>>4;oy=z.oy;h=by-oy;z.oy=by
  tp=by if by<oy else oy;bm=(by if by>oy else oy)+BT;sl=BL2 or bm>GY-BM
  for p in z.pp:
    if p[0]<BX+BW and p[0]+CW>BX and (tp<p[1] or bm>p[1]+p[2]):sl=1
  if sl:rest(BX,BX+BW,oy,oy+BT)
  elif h:
    for j in range(BT):
      a=LO[j];b=HI[j];r=oy+j;j2=j-h
      if j2>=0 and j2<BT:
        c=LO[j2];d=HI[j2]
        for x in range(a,b if b<c else c):sp(x,r,SKY)
        for x in range(a if a>d else d,b):sp(x,r,SKY)
      else:
        for x in range(a,b):sp(x,r,SKY)
  for x,j,c in BS[WF[(z.t>>1)&3]]:sp(x,by+j,c)
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
  draw_string(139,29,"FLAPPY BIRD",PO);draw_string(138,28,"FLAPPY BIRD",WH)
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
    v=z.vy+G;z.vy=v if v<VM else VM;y=z.y+z.vy
    if y<HYS:y=HYS
    if y==HYS and z.vy<0:z.vy=0
    z.y=y
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
for x in range(W):bgv(x,HY,GY)
rc(0,0,W,HY,NV);rc(0,GY,W,1,PO);rc(0,GY+5,W,1,DL);rc(0,GY+6,W,H-GY-6,DT)
for x in range(W):rc(x,GY+1,1,4,GD if x%(2*GS)>=GS else GL)
while 1:
  newg();ready();play();fall();over()
