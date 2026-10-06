# PAC-MAN style game for Casio fx-CG100 (MicroPython 1.9.4, casioplot)
# Arrows = move, EXE = start/pause, AC = quit. SPD = extra delay per frame.
from casioplot import *
from random import randint
SPD=8000
BK=(0,0,0);BL=(33,33,255);PK=(255,184,174);YL=(255,255,0);WH=(255,255,255);RD=(255,0,0)
MZ=(
"############################","#............##............#","#.####.#####.##.#####.####.#","#o####.#####.##.#####.####o#",
"#.####.#####.##.#####.####.#","#..........................#","#.####.##.########.##.####.#","#.####.##.########.##.####.#",
"#......##....##....##......#","######.##### ## #####.######","######.##### ## #####.######","######.##          ##.######",
"######.## ###--### ##.######","######.## #      # ##.######","      .   #      #   .      ","######.## #      # ##.######",
"######.## ######## ##.######","######.##          ##.######","######.## ######## ##.######","######.## ######## ##.######",
"#............##............#","#.####.#####.##.#####.####.#","#.####.#####.##.#####.####.#","#o..##.......  .......##..o#",
"###.##.##.########.##.##.###","###.##.##.########.##.##.###","#......##....##....##......#","#.##########.##.##########.#",
"#.##########.##.##########.#","#..........................#","############################")
DX=(0,-1,0,1);DY=(-1,0,1,0);KM={14:0,23:1,34:2,25:3};OX=4;OY=3;T=6
NU=((12,11),(15,11),(12,23),(15,23));SC=((25,-3),(2,-3),(27,31),(0,31))
GC=((255,0,0),(255,184,255),(0,255,255),(255,184,81))
HS=((13,11),(13,14),(11,14),(16,14))
FS=(45,38,30,23,15,38,15,15,8,38,15,8,8,23,8,8,0,8)
FP=(100,300,500,700,1000,2000,3000,5000)
FC=((255,0,0),(255,64,128),(255,160,0),(255,40,40),(0,200,0),(255,255,0),(255,220,0),(0,255,255))
FI=(0,1,2,2,3,3,4,4,5,5,6,6,7)
PU=(((2,1),(3,1)),((1,2),(3,2)),((2,2),(3,2)),((2,2),(4,2)))
FR=(0,1,2,1);M=[]
class Z:pass
z=Z();z.t=0;z.bl=1;z.hi=0;z.px=13;z.py=23;z.gh=[];z.dr={};z.o={};z.wc=BL;z.lv=1
class Gh:
  def __init__(s,i):s.i=i
  def rs(s):
    s.x,s.y=HS[s.i];s.d=1;s.s='N' if s.i==0 else 'H';s.a=0;s.f=0;s.rv=0
    s.lim=(0,0,30 if z.lv<2 else 0,60 if z.lv<2 else 50 if z.lv<3 else 0)[s.i]
def pm(d,f,r=36):
  m=[]
  for j in range(6):
    q=0
    for i in range(6):
      u=2*i-5;v=2*j-5;a=u*DX[d]+v*DY[d]
      if u*u+v*v<=r and not(f and a>0 and abs(u*DY[d]-v*DX[d])*2<=a*f):q|=1<<i
    m.append(q)
  return m
def gm(f):
  m=[]
  for j in range(6):
    q=0
    for i in range(6):
      if (j==0 and 0<i<5) or 0<j<5 or (j==5 and i in ((0,2,3,5),(1,2,3,4))[f]):q|=1<<i
    m.append(q)
  return m
PS=[[pm(d,f) for f in range(3)] for d in range(4)]
GB=(gm(0),gm(1))
EW=(0,30,30,0,0,0)
def rc(x,y,w,h,c):
  for i in range(w):
    for j in range(h):set_pixel(x+i,y+j,c)
def spr(x,y,m,c):
  for j in range(6):
    q=m[j]
    for i in range(6):
      if q>>i&1:set_pixel(x+i,y+j,c)
def dly(n):
  for i in range(n):pass
def tx(k,x,y,t):
  if k in z.o:draw_string(x,y,z.o[k],WH)
  draw_string(x,y,t,BK);z.o[k]=t
def dt(x,y,c=0):
  sx=OX+x*T;sy=OY+y*T;h=M[y][x]
  if c:rc(sx,sy,T,T,BK)
  if h=='#':
    for k in range(4):
      nx=x+DX[k];ny=y+DY[k]
      if 0<=nx<28 and 0<=ny<31 and M[ny][nx] not in '#-':
        if k==0:rc(sx,sy,T,2,z.wc)
        elif k==1:rc(sx,sy,2,T,z.wc)
        elif k==2:rc(sx,sy+4,T,2,z.wc)
        else:rc(sx+4,sy,2,T,z.wc)
  elif h=='.':rc(sx+2,sy+2,2,2,PK)
  elif h=='o' and z.bl:rc(sx+1,sy+1,4,4,PK)
  elif h=='-':rc(sx,sy+2,T,2,(255,184,255))
def dgh(g):
  x=OX+g.x*T;y=OY+g.y*T;s=g.s;c=0
  if s!='E' and s!='D':
    c=GC[g.i]
    if g.f:c=WH if (z.fr<15 and (z.fr>>1)&1) else (33,33,222)
    spr(x,y,GB[(z.t>>1)&1],c)
  if g.f and c:
    e=RD if c==WH else PK
    set_pixel(x+1,y+2,e);set_pixel(x+4,y+2,e)
  else:
    spr(x,y,EW,WH)
    for i,j in PU[g.d]:set_pixel(x+i,y+j,(0,0,170))
def rnd():
  for g in z.gh:z.dr[(g.x,g.y)]=1
  z.dr[(z.px,z.py)]=1
  for p in z.dr:dt(p[0],p[1],1)
  z.dr={}
  if z.fv:
    x=OX+14*T-3;y=OY+17*T
    spr(x,y,pm(0,0,25),FC[z.fi]);set_pixel(x+3,y,(0,170,0))
  spr(OX+z.px*T,OY+z.py*T,PS[z.pd][FR[z.pf&3]],YL)
  for g in z.gh:dgh(g)
  show_screen()
def msg(t,c):
  rc(OX+58,OY+17*T-1,52,11,BK);draw_string(OX+60,OY+17*T,t,c,"small");show_screen()
def clr():
  for x in range(9,20):
    for y in range(16,19):z.dr[(x,y)]=1
def wk():
  while getkey()==95:pass
  while getkey()!=95:pass
  while getkey()==95:pass
def pnl():
  if z.sc>z.hi:z.hi=z.sc
  tx(1,180,22,str(z.sc));tx(2,180,66,str(z.hi));z.pn=0
def hud():
  tx(3,180,110,"LEVEL "+str(z.lv))
  rc(178,132,100,10,BK)
  for i in range(z.lives-1):spr(180+i*10,134,PS[1][1],YL)
  rc(178,146,12,10,BK);spr(181,148,pm(0,0,25),FC[z.fi])
def pk(x,y):return 0<=y<31 and M[y][x%28] not in '#-'
def pos():
  for g in z.gh:
    z.dr[(g.x,g.y)]=1;g.rs()
  z.dr[(z.px,z.py)]=1;z.dr[(13,17)]=1;z.dr[(14,17)]=1
  z.px=13;z.py=23;z.pd=1;z.nd=1;z.nx=0;z.pa=0;z.pf=0;z.fr=0;z.fv=0;z.dl=0;z.idle=0;z.cm=0
def setup():
  global M
  M=[list(r) for r in MZ]
  z.left=0
  for r in MZ:z.left+=r.count('.')+r.count('o')
  z.fi=FI[min(z.lv-1,12)];z.wc=BL;z.mt=0;z.ms=0;z.cs=0
  a=52 if z.lv<5 else 37
  z.sch=[a,150,a,150,37,150 if z.lv<2 else 7750,37 if z.lv<2 else 1,9999]
  rc(OX,OY,168,186,BK)
  for y in range(31):
    for x in range(28):dt(x,y)
  pos()
def fright():
  z.cm=0
  n=FS[z.lv-1] if z.lv<19 else 0
  z.fr=n
  for g in z.gh:
    if g.s=='N':g.rv=1
    if n and g.s!='E' and g.s!='D':g.f=1
def eat(c):
  M[z.py][z.px]=' ';z.left-=1;z.dl+=1;z.idle=0;z.pn=1
  if c=='.':z.sc+=10
  else:
    z.sc+=50;fright()
  e=244-z.left
  if e==70 or e==170:
    z.fv=70;z.dr[(13,17)]=1;z.dr[(14,17)]=1
def spac():
  z.dr[(z.px,z.py)]=1
  if pk(z.px+DX[z.nd],z.py+DY[z.nd]):z.pd=z.nd
  d=z.pd;nx=z.px+DX[d];ny=z.py+DY[d]
  if pk(nx,ny):
    z.px=nx%28;z.py=ny;z.pf+=1
    c=M[ny][z.px]
    if c=='.' or c=='o':eat(c)
    if z.fv and ny==17 and z.px in (13,14):
      z.sc+=FP[z.fi];z.fv=0;z.pn=1;z.dr[(13,17)]=1;z.dr[(14,17)]=1
def tgt(g):
  i=g.i
  if g.s=='E':return (13,11)
  if z.cs==0 and not(i==0 and z.left<=20):return SC[i]
  px=z.px;py=z.py
  if i==0:return (px,py)
  n=4 if i==1 else 2
  ax=px+DX[z.pd]*n;ay=py+DY[z.pd]*n
  if z.pd==0:ax-=n
  if i==1:return (ax,ay)
  if i==2:
    b=z.gh[0];return (2*ax-b.x,2*ay-b.y)
  if (px-g.x)**2+(py-g.y)**2>64:return (px,py)
  return SC[3]
def sgh(g):
  s=g.s;x=g.x;y=g.y;d=g.d;z.dr[(x,y)]=1
  if s=='X':
    if x<13:g.x+=1
    elif x>13:g.x-=1
    else:
      g.y-=1
      if g.y==11:g.s='N';g.d=1
    return
  if s=='D':
    g.y+=1
    if g.y==14:g.s='X';g.f=0
    return
  bk=(d+2)%4
  if g.rv:
    g.rv=0;d=bk
  else:
    o=[]
    for k in range(4):
      nx=(x+DX[k])%28;ny=y+DY[k]
      if k==bk or ny<0 or ny>30 or M[ny][nx] in '#-':continue
      if k==0 and not g.f and s=='N' and (x,y) in NU:continue
      o.append(k)
    if not o:o=[bk]
    if g.f:d=o[randint(0,len(o)-1)]
    else:
      t=tgt(g);b=99999
      for k in o:
        e=(x+DX[k]-t[0])**2+(y+DY[k]-t[1])**2
        if e<b:b=e;d=k
  g.d=d;g.x=(x+DX[d])%28;g.y=y+DY[d]
  if s=='E' and g.x==13 and g.y==11:g.s='D'
def gsp(g):
  s=g.s
  if s=='E':return 200
  if s=='H':return 0
  if s=='X' or s=='D':return 60
  if g.y==14 and (g.x<6 or g.x>21):return 50
  if g.f:return 62
  if g.i==0 and z.left<=20:return 106 if z.left<=10 else 100
  return 94
def col():
  for g in z.gh:
    if g.x==z.px and g.y==z.py and g.s=='N':
      if not g.f:return 1
      g.s='E';g.f=0;z.sc+=200<<z.cm;z.cm=min(z.cm+1,3);z.pn=1
  return 0
def mode():
  if z.fr:
    z.fr-=1
    if z.fr==0:
      for g in z.gh:g.f=0
    return
  z.mt+=1
  if z.mt>=z.sch[z.ms]:
    z.mt=0;z.ms=min(z.ms+1,7);z.cs=z.ms&1
    for g in z.gh:
      if g.s=='N':g.rv=1
def rel():
  z.idle+=1
  for g in z.gh:
    if g.s=='H':
      if z.dl>=g.lim or z.idle>32:g.s='X';z.idle=0
      break
def die():
  for g in z.gh:dt(g.x,g.y,1)
  for f in (1,2,3,4,6,9,14):
    dt(z.px,z.py,1);spr(OX+z.px*T,OY+z.py*T,pm(0,f),YL);show_screen();dly(400)
  dt(z.px,z.py,1);z.lives-=1
  if z.lives<1:
    msg("GAME OVER",RD);wk();return 1
  pos();hud();rnd();msg("READY!",YL);wk();clr();return 0
def win():
  for n in range(4):
    z.wc=WH if n%2==0 else BL
    for y in range(31):
      for x in range(28):
        if M[y][x]=='#':dt(x,y)
    show_screen();dly(400)
  z.lv+=1;setup();hud();pnl();rnd();msg("READY!",YL);wk();clr()
def run():
  while 1:
    z.t+=1;k=getkey()
    if k in KM:z.nd=KM[k];z.nx=5
    elif k==95:
      msg("PAUSED",YL);wk();clr()
    if z.nx:
      z.nx-=1
      if z.nx==0:z.nd=z.pd
    z.pa+=(112 if z.lv<2 else 105 if z.lv<5 else 100) if z.fr else 100
    dead=0
    while z.pa>=100 and not dead:
      z.pa-=100;spac();dead=col()
    for g in z.gh:
      g.a+=gsp(g)
      while g.a>=100 and not dead:
        g.a-=100;sgh(g);dead=col()
    mode();rel()
    if z.fv:
      z.fv-=1
      if z.fv==0:z.dr[(13,17)]=1;z.dr[(14,17)]=1
    if z.t%4==0:
      z.bl^=1
      for p in ((1,3),(26,3),(1,23),(26,23)):z.dr[p]=1
    if z.sc>=10000 and not z.xl:
      z.xl=1;z.lives+=1;hud()
    if dead:
      if die():return
    elif z.left==0:win()
    rnd()
    if z.pn and z.t%6==0:pnl()
    dly(SPD)
clear_screen()
draw_string(180,4,"SCORE",BK);draw_string(180,48,"HIGH SCORE",BK)
draw_string(180,160,"ARROWS:MOVE",(90,90,90),"small");draw_string(180,174,"EXE:PAUSE",(90,90,90),"small")
while 1:
  z.lv=1;z.sc=0;z.lives=3;z.xl=0;z.fv=0
  z.gh=[Gh(i) for i in range(4)]
  for g in z.gh:g.rs()
  setup();hud();pnl();rnd();msg("READY!",YL);wk();clr()
  run()
