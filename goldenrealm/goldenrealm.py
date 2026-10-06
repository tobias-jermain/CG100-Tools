# GOLDEN REALM for Casio fx-CG100 (MicroPython 1.9.4, casioplot)
# Arrows = walk, EXE = start/pause, AC = quit. Gather gold from the fields and bring it to the king.
from casioplot import *
SPD=0;PS=2;NG=24;LV=3
# SPD = extra delay per frame, PS = walking speed in pixels, NG = gold to find, LV = hearts
W=384;H=192;HY=16;TW=24;TH=11;SW=5;SH=5;WX=TW*SW;WY=TH*SH;VW=384;VH=176
BK=(0,0,0);WH=(255,255,255);HB=(46,32,20);GO=(255,210,40);RD=(220,40,40)
KM={14:0,23:1,34:2,25:3};DX=(0,-1,0,1);DY=(-1,0,1,0)
TS=".,TW=RhHDSCPKMFf"   # grass, wheat, tree, water, bridge, road, roof, wall, door, stone, tower, paving, king, rock, fence, flowers
SL="TWhHDSCKMF"         # solid tiles
BA=((76,166,64),(222,184,64),(76,166,64),(54,110,210),(160,110,60),(196,166,116),(178,60,40),(236,224,190),(236,224,190),(150,150,158),(128,128,138),(200,196,180),(200,196,180),(130,115,100),(76,166,64),(76,166,64))
class Z:pass
z=Z();z.r=2024;z.hi=0
def rn(n):z.r=(z.r*75+74)%65537;return z.r%n
def nz(x,y,s):return ((x*37+y*91+s*17)*(x*13+y*7+s*29+1))%97
def rc(x,y,w,h,c):
  for i in range(w):
    for j in range(h):set_pixel(x+i,y+j,c)
def dly(n):
  for i in range(n):pass
def wk():
  while getkey()==95:pass
  while getkey()!=95:pass
  while getkey()==95:pass
def bdg(x,y):
  for a,b,w,h in ((0,0,100,1),(0,23,100,1),(0,0,1,24),(99,0,1,24),(100,2,2,24),(2,24,100,2)):rc(x+a,y+b,w,h,BK)
  rc(x+1,y+1,98,22,WH);draw_string(x+5,y+3,"tobias-jermain",BK,"small");draw_string(x+5,y+13,"/ CG100-Tools",(0,102,204),"small")
clear_screen();draw_string(130,80,"LOADING...",BK);show_screen()
def tile(t):
  # build the 16x16 picture of tile t
  b=BA[t];g=[[b]*16 for i in range(16)]
  for y in range(16):
    for x in range(16):
      n=nz(x,y,t);c=b
      if t in (0,2,14,15):c=(60,140,50) if n<9 else (110,190,80) if n>92 else b
      if t==1:
        if (x+2*(y>>3))%4==1:c=(250,225,120) if y%8==1 else (186,146,40)
      elif t==2:
        d=(x-8)*(x-8)+(y-6)*(y-6)
        if d<=40:c=(70,150,60) if (x-6)*(x-6)+(y-4)*(y-4)<=5 else (34,110,40)
        elif d<=54:c=(20,70,25)
        elif x>6 and x<9 and y>11:c=(110,70,30)
      elif t==3:
        if y%8==3 and (x+y)%8<3:c=(120,170,240)
      elif t==4:
        if y==0 or y==15:c=(90,60,30)
        elif y%4==0:c=(120,80,40)
      elif t==5:c=(170,140,95) if n<9 else (220,195,150) if n>90 else b
      elif t==6:
        if y%4==3 or (x+(y>>2)*4)%8==0:c=(130,40,28)
      elif t==7 or t==8:
        if y==0 or y==15 or x==0 or x==15 or (t==7 and (x==y or x==15-y)):c=(100,64,34)
        if t==8 and x>3 and x<12 and y>3:c=(250,210,60) if x==10 and y==10 else (120,74,36)
      elif t==9 or t==10:
        if y%8==7 or (x+(4 if (y>>3)&1 else 0))%8==7:c=(110,110,118)
        elif n>90:c=(175,175,182)
        if t==10 and y<4:c=(90,90,98) if (x>>2)&1 else (128,128,138)
      elif t==11 or t==12:
        if y%8==0 or x%8==0:c=(170,166,150)
        if t==12:
          if y<3 and x>4 and x<11 and (y>0 or x%2==1):c=GO
          elif y>2 and y<7 and x>5 and x<10:c=(240,200,160) if y<6 else (230,230,230)
          elif y>6 and x>4-((y-7)>>2) and x<11+((y-7)>>2):c=(240,220,120) if x==7 or x==8 else (120,40,140)
      elif t==13:
        c=(100,88,76) if n<20 or y>13 else (165,150,135) if n>85 or y<2 else b
      elif t==14:
        if y==5 or y==10:c=(150,100,50)
        elif (x==2 or x==13) and y>2 and y<14:c=(110,70,35)
      elif t==15:
        if n<3:c=(230,60,60)
        elif n<5:c=WH
        elif n<7:c=(250,220,60)
      g[y][x]=c
  return g
TP=[tile(t) for t in range(16)]   # tile pictures, and DT = their pixels that differ from the base colour
DT=[[(x,y,TP[t][y][x]) for y in range(16) for x in range(16) if TP[t][y][x]!=BA[t]] for t in range(16)]
def spr(rows,pal):
  # sprite strings -> two lists of (x,y,colour): facing right and mirrored
  a=[];b=[];w=len(rows[0])
  for y in range(len(rows)):
    for x in range(w):
      ch=rows[y][x]
      if ch!='.':a.append((x,y,pal[ch]));b.append((w-1-x,y,pal[ch]))
  return a,b
PP={'G':(175,175,190),'g':(100,100,120),'S':(240,200,160),'K':(20,20,20),'R':(200,40,40),'r':(140,25,25),
'Y':GO,'B':(100,60,30),'L':(60,60,100),'W':(230,230,235),'k':(60,60,60),'y':(200,140,20),'E':RD}
TOP=("....gGGg....","...gGGGGg...","...gSSSSg...","...SKSSKS...","....SSSS....","..rRRYYRRr..",
".SrRRYYRRrS.",".SrRRRRRRrS.","..rRRRRRRr..","..BBBYYBBB..")
P1=spr(TOP+("...LL..LL...","...LL..LL...","...KK..KK..."),PP)[0]
P2=spr(TOP+("..LL....LL..","..LL....LL..","..KK....KK.."),PP)[0]
WT=("........g..g","........gGGg","G.......GEGG",".GGGGGGGGGGW",".GGGGGGGGGg.",".GGGGGGGGG..")
WA=spr(WT+(".G.G...G.G..",".G.G...G.G..",".k.k...k.k.."),PP);WB=spr(WT+("..G.G.G..G..","..G.G.G..G..","..k.k.k..k.."),PP)
GN=spr(("..YYYY..",".YWYYYy.","YYYYYYYy","YYYYYyyy",".yYYyyy.","..yyyy.."),PP)[0]
HT=spr((".EE.EE.","EEEEEEE","EEEEEEE",".EEEEE.","..EEE..","...E..."),PP)[0]
def world():
  g=[['.']*WX for i in range(WY)]
  def put(x,y,c):
    if x>=0 and y>=0 and x<WX and y<WY:g[y][x]=c
  for n in range(18):   # forests
    cx=rn(WX);cy=rn(WY);r=2+rn(3)
    for y in range(cy-r,cy+r+1):
      for x in range(cx-r,cx+r+1):
        if (x-cx)*(x-cx)+(y-cy)*(y-cy)<=r*r and rn(4):put(x,y,'T')
  for n in range(130):put(rn(WX),rn(WY),'T')
  for n in range(160):put(rn(WX),rn(WY),'f')
  for n in range(4):   # lakes
    cx=rn(WX);cy=rn(WY);r=1+rn(3)
    for y in range(cy-r,cy+r+1):
      for x in range(cx-r-1,cx+r+2):
        if (x-cx)*(x-cx)+(y-cy)*(y-cy)<=r*r+1:put(x,y,'W')
  x=30
  for y in range(WY):   # river
    for k in range(3):put(x+k,y,'W')
    x+=rn(3)-1;x=24 if x<24 else 38 if x>38 else x
  z.fd=[]
  for n in range(16):   # golden wheat fields, with a clear path around each
    w=8+rn(6);h=4+rn(4);x0=3+rn(WX-w-6);y0=3+rn(WY-h-6)
    if x0+w>46 and x0<74 and y0+h>20 and y0<34:continue
    for y in range(y0-1,y0+h+1):
      for x in range(x0-1,x0+w+1):
        c=x>=x0 and y>=y0 and x<x0+w and y<y0+h;put(x,y,',' if c else '.')
        if c:z.fd.append((x,y))
    if rn(2):
      for x in range(x0,x0+w):
        if x-x0!=w>>1:put(x,y0-1,'F')
  for cx,cy in ((12,8),(100,10),(14,46),(98,45),(80,30)):   # villages
    for n in range(4):
      x=cx+rn(10)-5;y=cy+rn(6)-3
      for a in range(-1,3):
        for b in range(-1,3):put(x+a,y+b,'.')
      d=rn(2);put(x,y,'h');put(x+1,y,'h');put(x,y+1,'D' if d else 'H');put(x+1,y+1,'H' if d else 'D')
  for x in range(2,WX-2):put(x,38,'=' if g[38][x]=='W' else 'R')
  for y in range(32,WY-2):put(60,y,'=' if g[y][60]=='W' else 'R')
  for y in range(22,33):
    for x in range(48,72):put(x,y,'.')
  for y in range(23,32):   # castle
    for x in range(52,68):put(x,y,'S' if y==23 or y==31 or x==52 or x==67 else 'P')
  for x,y in ((52,23),(66,23),(52,30),(66,30)):
    for a in range(2):
      for b in range(2):put(x+a,y+b,'C')
  put(59,31,'R');put(60,31,'R');put(59,26,'K')
  for i in range(WX):   # rocky border
    for k in range(1+rn(2)):put(i,k,'M');put(i,WY-1-k,'M')
  for i in range(WY):
    for k in range(1+rn(2)):put(k,i,'M');put(WX-1-k,i,'M')
  z.fd=[p for p in z.fd if g[p[1]][p[0]]==',']
  return [''.join(r) for r in g]
M=world()
CUR=[-1]*(TW*TH);SX=[];SY=[]
for j in range(TH):
  for i in range(TW):SX.append(i<<4);SY.append(HY+(j<<4))
def dtile(i,t,u,sp=set_pixel):
  # draw tile t over tile u in slot i; if both share a base colour only the detail pixels are touched
  X=SX[i];Y=SY[i];g=TP[t]
  if u>=0 and BA[u]==BA[t]:
    for x,y,c in DT[u]:sp(X+x,Y+y,g[y][x])
    for x,y,c in DT[t]:sp(X+x,Y+y,c)
  else:
    for y in range(16):
      r=g[y];v=Y+y
      for x in range(16):sp(X+x,v,r[x])
def scr():
  # draw the current screen, only the tiles that differ from what is shown
  x0=z.sx*TW;y0=z.sy*TH;i=0
  for j in range(TH):
    r=M[y0+j]
    for k in range(TW):
      t=TS.find(r[x0+k])
      if CUR[i]!=t:dtile(i,t,CUR[i]);CUR[i]=t
      i+=1
def inv(x0,y0,x1,y1):
  for i in range(TW*TH):
    if SX[i]+16>x0 and SX[i]<x1 and SY[i]+16>y0 and SY[i]<y1:CUR[i]=-1
def ds(x,y,S,sp=set_pixel):
  y+=HY
  for a,b,c in S:sp(x+a,y+b,c)
def es(x,y,S,sp=set_pixel):
  # erase a sprite by repainting the tile pixels under it
  for a,b,c in S:
    X=x+a;Y=y+b;sp(X,Y+HY,TP[CUR[(Y>>4)*TW+(X>>4)]][Y&15][X&15])
def sol(X,Y):return M[Y>>4][X>>4] in SL
def pf(X,Y):return not(sol(X+2,Y+8) or sol(X+9,Y+8) or sol(X+2,Y+12) or sol(X+9,Y+12))
def wf(x,y):
  X=z.sx*VW+x;Y=z.sy*VH+y
  return not(sol(X,Y+2) or sol(X+11,Y+2) or sol(X,Y+8) or sol(X+11,Y+8))
def txt(x,w,s,c=WH):rc(x,2,w,12,HB);draw_string(x+2,3,s,c,"small")
def hg():txt(14,40,str(z.g)+"/"+str(NG),GO)
def hh():
  for i in range(LV):
    for a,b,c in HT:set_pixel(64+i*10+a,5+b,RD if i<z.hp else (95,60,45))
def hm(s="GOLDEN REALM"):txt(120,210,s);z.mt=0 if s=="GOLDEN REALM" else 90
def hmap():
  for j in range(SH):
    for i in range(SW):rc(344+i*7,1+j*3,6,2,GO if i==z.sx and j==z.sy else (120,90,60))
def hud():
  rc(0,0,W,HY,HB);ds(3,-11,GN);hg();hh();hm();hmap()
def enter():
  z.gs=[];z.ws=[]
  for g in z.gold:
    x=g[0]-z.sx*VW;y=g[1]-z.sy*VH
    if x>=0 and y>=0 and x<VW and y<VH:z.gs.append([x,y,g])
  n=0 if z.sx==2 and z.sy==2 else rn(3)
  for k in range(30):
    if len(z.ws)>=n:break
    x=rn(VW-12);y=rn(VH-9)
    if wf(x,y) and abs(x-z.x)+abs(y-z.y)>140:z.ws.append([x,y,4,0,0])
def redraw():
  for x,y,S in z.dr:es(x,y,S)
  for g in z.gs:ds(g[0],g[1],GN)
  d=[]
  for w in z.ws:d.append((w[0],w[1],(WA if (z.t>>2)&1 else WB)[w[4]]))
  if z.iv==0 or z.t&2:d.append((z.x,z.y,P2 if (z.st>>2)&1 else P1))
  for x,y,S in d:ds(x,y,S)
  z.dr=d
def go(ix,iy,x,y):
  for a,b,S in z.dr:es(a,b,S)
  for g in z.gs:es(g[0],g[1],GN)
  z.dr=[];z.sx+=ix;z.sy+=iy;z.x=x;z.y=y;scr();enter();hmap()
def box(a,b,c,e,br=0):
  rc(72,44,240,96,BK);rc(74,46,236,92,HB)
  draw_string(84,52,a,GO);draw_string(84,74,b,WH,"small");draw_string(84,86,c,WH,"small")
  draw_string(84,120 if br else 104,e,(255,230,150),"small")
  if br:draw_string(84,100,"ARROWS:WALK EXE:PAUSE",(200,200,200),"small");bdg(204,110)
  show_screen();wk();inv(72,44,312,140);scr();redraw();show_screen()
def hurt(w):
  z.hp-=1;z.iv=45;hh()
  dx=z.x-w[0];dy=z.y+4-w[1]
  if abs(dx)>abs(dy):nx=z.x+(12 if dx>0 else -12);ny=z.y
  else:nx=z.x;ny=z.y+(12 if dy>0 else -12)
  if nx>=0 and ny>=0 and nx<=VW-12 and ny<=VH-13 and pf(z.sx*VW+nx,z.sy*VH+ny):z.x=nx;z.y=ny
def wolves():
  for w in z.ws:
    dx=z.x-w[0];dy=z.y+4-w[1]
    if abs(dx)+abs(dy)<110:   # chase: try the longer axis first, then the other
      a=3 if dx>0 else 1;b=2 if dy>0 else 0
      L=(a,b) if abs(dx)>abs(dy) else (b,a)
    else:
      w[3]-=1
      if w[3]<=0:w[2]=rn(5);w[3]=20+rn(40)
      L=(w[2],)
    for d in L:
      if d>3:break
      nx=w[0]+DX[d];ny=w[1]+DY[d]
      if nx>=0 and ny>=0 and nx<=VW-12 and ny<=VH-9 and wf(nx,ny):
        w[0]=nx;w[1]=ny
        if d&1:w[4]=d==1
        break
      w[3]=0
    if z.iv==0 and abs(w[0]-z.x)<10 and abs(w[1]-z.y-4)<9:hurt(w)
def newg():
  z.gold=[]
  while len(z.gold)<NG:
    p=z.fd[rn(len(z.fd))];g=[(p[0]<<4)+4,(p[1]<<4)+5]
    if g not in z.gold:z.gold.append(g)
  for i in range(TW*TH):CUR[i]=-1
  z.sx=2;z.sy=2;z.x=176;z.y=96;z.hp=LV;z.g=0;z.iv=0;z.kt=0;z.st=0;z.t=0;z.dr=[]
  clear_screen();hud();scr();enter();redraw()
def play():
  while 1:
    z.t+=1;k=getkey();ch=len(z.ws)>0 or z.iv>0
    if k==95:box("PAUSED","Gold found: "+str(z.g)+" of "+str(NG),"Hearts left: "+str(z.hp),"EXE: CONTINUE")
    if k in KM:
      d=KM[k];nx=z.x+DX[d]*PS;ny=z.y+DY[d]*PS;z.st+=1;ch=1;ix=0;iy=0;tx=nx;ty=ny
      if nx<0:ix=-1;tx=VW-12
      elif nx>VW-12:ix=1;tx=0
      elif ny<0:iy=-1;ty=VH-13
      elif ny>VH-13:iy=1;ty=0
      if pf((z.sx+ix)*VW+tx,(z.sy+iy)*VH+ty):
        if ix or iy:go(ix,iy,tx,ty)
        else:z.x=tx;z.y=ty
    wolves()
    if z.iv:z.iv-=1
    if z.hp<=0:
      redraw();box("YOU FELL!","The wolves got you.","Gold found: "+str(z.g),"EXE: TRY AGAIN");return
    for g in z.gs:
      if abs(g[0]-z.x-2)<9 and abs(g[1]-z.y-5)<9:
        es(g[0],g[1],GN);z.gs=[q for q in z.gs if q!=g];z.gold=[q for q in z.gold if q!=g[2]];z.g+=1;hg()
        hm("GOLD! "+str(NG-z.g)+" LEFT" if z.g<NG else "ALL GOLD! SEE THE KING")
        break
    if z.kt:z.kt-=1
    if z.sx==2 and z.sy==2 and abs(z.x-178)<22 and abs(z.y-65)<24 and z.kt==0:
      z.kt=60
      if z.g>=NG:
        if z.hi==0 or z.st<z.hi:z.hi=z.st
        redraw();box("LONG LIVE THE KING!","All the gold is safe.",str(z.st)+" steps, best "+str(z.hi),"EXE: PLAY AGAIN");return
      hm("KING: BRING ME "+str(NG-z.g)+" MORE GOLD")
    if z.mt:
      z.mt-=1
      if z.mt==0:hm()
    if ch:redraw();show_screen()
    dly(SPD)
while 1:
  newg();box("GOLDEN REALM","Gather "+str(NG)+" gold from the fields","and bring it to the king.","EXE: START",1)
  play()
