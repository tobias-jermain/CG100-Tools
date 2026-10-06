# GOLDEN REALM for Casio fx-CG100 (MicroPython 1.9.4, casioplot)
# Arrows = walk, EXE = dash / start, AC = quit. Speedrun: gather the golden sheaves and bring the harvest home.
from casioplot import *
SPD=0;PS=2;NG=12;FPS=30;MG=(75,95,120)
# SPD = extra delay per tick, PS = walk speed in pixels, NG = sheaves to gather,
# FPS = timer ticks per second, MG = gold/silver/bronze medal times in seconds
W=384;H=192;HY=16;TW=24;TH=11;SW=5;SH=5;WX=120;WY=55;VW=384;VH=176
BK=(0,0,0);WH=(255,255,255);HB=(58,40,26);GO=(255,214,90);CR=(255,236,190);GR=(110,96,80)
KM={14:0,23:1,34:2,25:3};DX=(0,-1,0,1);DY=(-1,0,1,0)
TS=".,TPBAUkFfYrW12=RbhHDM"   # grass,wheat,oak,pine,birch,apple,autumn,bush,fence,flowers,hay,runestone,water,
SL="TPBAUkFYrWhHDM"           # windblown wheat,rippled water (animation frames),planks,path,sand,turf roof,wall,door,rock
G=(104,170,76);WA=(58,120,190);WD=(124,84,52);BA=(G,(228,190,84),G,G,G,G,G,G,G,G,G,G,WA,(228,190,84),WA,(150,104,62),(198,168,120),(232,212,160),(96,146,66),WD,WD,(130,122,114))
FS=((14,10),(92,12),(16,46),(84,48));SD=(78,136,62);TR=(110,72,42);CN={2:((54,126,58),(92,162,74),(36,96,46)),5:((58,130,60),(96,166,78),(38,98,48)),6:((222,130,50),(246,180,86),(170,88,38))}
class Z:pass
z=Z();z.r=1066;z.pb=0
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
def px(t,x,y):   # colour of pixel (x,y) of tile t
  n=nz(x,y,t);b=BA[t];c=b;d=(x-8)*(x-8)+(y-6)*(y-6);e=(x-9)*(x-9)+8*(y-14)*(y-14);f=(x-8)*(x-8)+(y-5)*(y-5);h=(x-8)*(x-8)+2*(y-10)*(y-10)
  if t<12:
    c=(84,148,62) if n<6 else (140,196,98) if n>90 else b
    if t in CN:   # round trees: oak, apple, autumn
      q=CN[t]
      if d<=40:c=q[1] if (x-6)*(x-6)+(y-4)*(y-4)<=6 else q[2] if n<14 else q[0]
      else:c=q[2] if d<=52 else TR if x>6 and x<9 and y>11 else SD if e<=20 else c
      if t==5 and d<=34 and (x*3+y*5)%11==0:c=(214,48,44)
    elif t==3:   # pine
      k=(y>=5)+(y>=10);w=y-4*k+1
      if y<14 and x>7-w and x<8+w:c=(24,66,50) if x==8-w or x==7+w else (44,108,76) if x<8 else (30,84,62)
      else:c=TR if y>13 and x>6 and x<9 else SD if e<=20 else c
    elif t==4:   # birch
      if f<=20:c=(178,216,112) if (x-6)*(x-6)+(y-3)*(y-3)<=4 else (130,188,86)
      else:c=(96,150,64) if f<=28 else ((44,44,44) if (y*3+x)%5==0 else (238,236,226)) if x>6 and x<9 and y>6 else SD if e<=20 else c
    elif t==7:c=((200,40,90) if (x+y*3)%7==0 and h<34 else (62,134,62) if n<40 else (86,158,72)) if h<=40 else (42,100,46) if h<=52 else c   # berry bush
    elif t==8:c=(156,108,62) if y==6 or y==10 else (112,76,44) if (x==2 or x==13) and y>3 and y<14 else c   # fence
    elif t==9:   # flowers: little five-petal blooms
      for a,b,k in ((3,4,(240,140,170)),(11,3,(250,250,240)),(7,10,(130,160,240)),(13,12,(240,140,170)),(2,13,(250,250,240))):
        c=(250,210,70) if x==a and y==b else k if abs(x-a)+abs(y-b)==1 else (70,130,56) if x==a and y==b+2 else c
    elif t==10:   # haystack
      d=h+4*y-38
      if d<=44 and y<14:c=(248,222,132) if (x-6)*(x-6)+2*(y-6)*(y-6)<=6 else (190,148,56) if x>10 or y>11 or (x+2*y)%6==0 else (228,186,82)
      elif e<=24:c=SD
    elif t==11:   # runestone
      if x>4 and x<12 and y>1 and y<15 and not((x==5 or x==11) and y==2):
        c=(184,52,40) if y>3 and y<12 and (x==8 or (x+y)%5==0) and x>5 and x<11 else (116,116,124) if x>9 else (158,158,166)
      elif y==15 and x>4 and x<14:c=SD
  elif t==12 or t==14:   # water, with two ripple frames
    c=(118,174,226) if ((y%8==3 and (x+y)%8<3) if t==12 else (y%8==5 and (x+y+4)%8<3)) else (46,102,172) if n<5 else b
  elif t==13:c=((255,240,176) if y%8<2 else (204,158,58)) if (x+(y&7)+2*(y>>3))%4==1 else b   # wheat bent by the wind
  elif t==15:c=(96,64,38) if y==0 or y==15 else (122,82,48) if y%4==0 or n<3 else b
  elif t==16:c=(176,146,104) if n<9 else (222,198,156) if n>90 else b
  elif t==17:c=(214,192,140) if n<10 else (244,228,184) if n>92 else b
  elif t==18:c=(110,72,40) if y>12 else (74,118,52) if (x+(y>>1))%5==0 else (132,182,92) if n>90 else (240,200,80) if n==50 else b
  elif t<21:
    c=(70,46,28) if y==15 else (88,58,36) if x%4==3 else b
    if t==20 and x>3 and x<12 and y>2 and not(y==3 and (x==4 or x==11)):c=(204,172,90) if x==10 and y==9 else (54,34,20) if x==7 else (72,46,28)
  else:c=(98,92,86) if n<22 or y>13 else (166,158,150) if n>80 or y<2 else b
  if t==1:c=((250,226,140) if y%8==1 else (196,150,52)) if (x+2*(y>>3))%4==1 else b
  return c
GP=[];GI={}
def ix(c):
  if c not in GI:GI[c]=len(GP);GP.append(c)
  return chr(35+GI[c])
# tiles are stored as strings of palette indexes (saves memory); DT = pixels that differ from the base colour
TP=[[''.join([ix(px(t,x,y)) for x in range(16)]) for y in range(16)] for t in range(22)]
DT=[[(y<<4)|x for y in range(16) for x in range(16) if GP[ord(TP[t][y][x])-35]!=BA[t]] for t in range(22)]
PP={'Y':(236,200,110),'y':(196,156,80),'S':(240,200,160),'K':(40,30,24),'G':(74,124,96),'g':(50,90,70),'B':GO,'b':(110,70,40),'L':(120,110,96),'W':(246,246,240),'w':(210,210,204),'E':WH,'O':(246,206,80),'o':(252,232,150),'R':(240,140,60)}
def spr(R):return [(x,y,PP[R[y][x]]) for y in range(len(R)) for x in range(len(R[0])) if R[y][x]!='.']
LG=(("...LL..LL...","...LL..LL...","...KK..KK..."),("..LL....LL..","..LL....LL..","..KK....KK.."))
BD=("..gGGGGGGg..",".SgGGBBGGgS.",".SgGGGGGGgS.","..gGGGGGGg..","..bbbbbbbb..")
PF=[spr(("....YYYY....","...YYYYYY...","...YSSSSY...","...SKSSKS...","....SSSS....")+BD+l) for l in LG];PB=[spr(("....YYYY....","...YYYYYY...","...YYYYYY...","...yYYYYy...","....yyyy....")+BD+l) for l in LG]
SB=("...wWWWw....",".wWWWWWWWw..","wWWWWWWWWKK.","WWWWWWWWKEKK","wWWWWWWWWKK.",".wwwwwwwww..");SP=[spr(SB+("..K.K..K.K..","..K.K..K.K..")),spr(SB+("...KK...KK..","...KK...KK.."))]
SR=("..bOOOb..","...bbb...","..bOOOb..",".bOOOOOb.","bOObObOOb",".bb.b.bb.");SV=spr(("..b.b.b..",".bobobob.",".bOOoOOb.")+SR)
ST=spr(("..b.b.b..",".bobEbob.",".bOOoOOb.")+SR)   # twinkle frame (same pixels, one turns white)
BF=[[spr(tuple(q.replace('C',L) for q in R)) for R in (("CC.CC","CCKCC","..K.."),("..K..",".CKC.","..K.."))] for L in "EOR"]   # butterflies
PU=(spr((".ww.","wWWw","wWWw",".ww.")),spr(("ww","ww")))   # chimney smoke
def world():
  g=[['.']*WX for i in range(WY)]
  def put(x,y,c):
    if x>=0 and y>=0 and x<WX and y<WY:g[y][x]=c
  def blob(cx,cy,r,ch,p):
    for y in range(cy-r,cy+r+1):
      for x in range(cx-r,cx+r+1):
        if (x-cx)*(x-cx)+(y-cy)*(y-cy)<=r*r and rn(4)<p:put(x,y,ch[rn(len(ch))])
  for n in range(10):blob(4+rn(90),3+rn(10),2+rn(3),"PPPB",3)   # pine woods in the north
  for n in range(10):blob(4+rn(90),15+rn(28),2+rn(2),"TTBAk",3)   # mixed woods
  for n in range(5):blob(4+rn(40),36+rn(14),2+rn(2),"UUTk",3)   # autumn grove
  for n in range(150):put(rn(WX),rn(WY),"TPBUkff"[rn(7)])
  for n in range(90):blob(rn(WX),rn(WY),1,"f",2)
  for n in range(3):blob(8+rn(80),8+rn(40),1+rn(2),"W",4)
  x=34
  for y in range(42):   # river: south from the hills, then east to the fjord
    put(x,y,'W');put(x+1,y,'W');x+=rn(3)-1;x=28 if x<28 else 40 if x>40 else x
  y=40;z.fd=[]
  for i in range(x,WX):
    put(i,y,'W');put(i,y+1,'W')
    if rn(4)==0:y+=rn(3)-1;y=38 if y<38 else 44 if y>44 else y
  for n in range(16):   # golden wheat fields with a clear edge
    w=7+rn(6);h=4+rn(3);x0=3+rn(84);y0=3+rn(WY-h-6)
    if x0+w>46 and x0<74 and y0+h>20 and y0<34:continue
    for y in range(y0-1,y0+h+1):
      for x in range(x0-1,x0+w+1):
        c=x>=x0 and y>=y0 and x<x0+w and y<y0+h;put(x,y,',' if c else '.')
        if c:z.fd.append((x,y))
    for x in range(x0,x0+w*rn(2)):put(x,y0-1,'F' if x-x0!=w>>1 else '.')
  for cx,cy in FS:   # farmsteads
    for a in range(-1,6):
      for b in range(-1,4):put(cx+a,cy+b,'h' if a>=0 and a<4 and b<2 else ('D' if a==1 else 'H') if a>=0 and a<4 and b==2 else 'Y' if a==5 and b==1 else '.')
  xs=104
  for y in range(WY):   # fjord and beach
    put(xs-2,y,'b');put(xs-1,y,'b')
    for x in range(xs,WX):put(x,y,'W')
    xs+=rn(3)-1;xs=100 if xs<100 else 107 if xs>107 else xs
  for y in range(22,33):   # keep the home farm screen clear
    for x in range(48,72):put(x,y,'.')
  for y in range(3,WY-3):put(58,y,'=' if g[y][58]=='W' else 'R')
  for x in range(3,WX):   # road from the hills to the beach
    if g[26][x]=='W' and x>95:break
    put(x,26,'=' if g[26][x]=='W' else 'R')
  for y in range(22,26):   # home farm: longhouse, orchard, hay and fields
    for x in range(50,68):put(x,y,'.')
  for x in range(55,62):put(x,23,'h');put(x,24,'h');put(x,25,'D' if x==58 else 'H')
  for x in range(50,54):put(x,23,'Y' if x&1 else 'f');put(x+13,23,'A')
  for y in range(27,31):
    for x in range(50,56):put(x,y,',');put(x+11,y,',');z.fd.append((x,y));z.fd.append((x+11,y))
  for x,y in ((20,25),(45,27),(75,25),(57,15),(59,40)):put(x,y,'r')
  for i in range(WX):   # hills around the edge (not over the sea)
    for k in range(1+rn(3)):put(i,k,'W' if g[k][i]=='W' else 'M');put(i,WY-1-k,'W' if g[WY-1-k][i]=='W' else 'M')
  for i in range(WY):
    for k in range(1+rn(2)):put(k,i,'M')
  z.fd=[p for p in z.fd if g[p[1]][p[0]]==',']
  return [''.join(r) for r in g]
M=world()
S0=[]   # the sheaves are in the same places every run, so routes can be learned
while len(S0)<NG:
  p=z.fd[rn(len(z.fd))];ok=1
  for q in S0:
    if abs(q[0]-p[0])+abs(q[1]-p[1])<14:ok=0
  if ok:S0.append(p)
CH=[(58*16+6,23*16)]+[((cx+1)*16+8,cy*16) for cx,cy in FS]   # chimneys
z.fd=0;CUR=[-1]*(TW*TH);SX=[i<<4 for j in range(TH) for i in range(TW)];SY=[HY+(j<<4) for j in range(TH) for i in range(TW)]
def dtile(i,t,u,sp=set_pixel):   # draw tile t over tile u; if both share a base colour only the detail pixels are touched
  X=SX[i];Y=SY[i];g=TP[t]
  if u>=0 and BA[u]==BA[t]:
    for p in DT[u]+DT[t]:sp(X+(p&15),Y+(p>>4),GP[ord(g[p>>4][p&15])-35])
  else:
    for y in range(16):
      r=g[y];v=Y+y
      for x in range(16):sp(X+x,v,GP[ord(r[x])-35])
def scr():
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
  for a,b,c in S:sp(x+a,y+HY+b,c)
def es(x,y,S,sp=set_pixel):   # erase a sprite by repainting the tile pixels under it
  for a,b,c in S:
    X=x+a;Y=y+b;sp(X,Y+HY,GP[ord(TP[CUR[(Y>>4)*TW+(X>>4)]][Y&15][X&15])-35])
def sol(X,Y):return M[Y>>4][X>>4] in SL
def pf(X,Y):return not(sol(X+2,Y+8) or sol(X+9,Y+8) or sol(X+2,Y+12) or sol(X+9,Y+12))
def wf(x,y):X=z.sx*VW+x;Y=z.sy*VH+y;return not(sol(X,Y+2) or sol(X+11,Y+2) or sol(X,Y+7) or sol(X+11,Y+7))
def fm(t,cs):   # ticks -> "m:ss" or "m:ss.cc"
  s=0;m=0
  while t>=FPS:t-=FPS;s+=1
  while s>=60:s-=60;m+=1
  r=str(m)+(":0" if s<10 else ":")+str(s)
  if cs:
    c=0;t*=100
    while t>=FPS:t-=FPS;c+=1
    r+=(".0" if c<10 else ".")+str(c)
  return r
def txt(x,w,s,c=CR):rc(x,2,w,12,HB);draw_string(x+2,3,s,c,"small")
def hm(s="GOLDEN REALM"):txt(176,150,s,WH);z.mt=0 if s=="GOLDEN REALM" else 75
def hmap():
  for j in range(SH):
    for i in range(SW):rc(348+i*7,1+j*3,6,2,GO if i==z.sx and j==z.sy else GR)
def hdash():rc(334,5,7,7,(120,220,120) if z.dc==0 else GR)
def hud():
  rc(0,0,W,HY,HB);ds(3,-14,SV);txt(14,40,str(z.g)+"/"+str(NG),GO);txt(58,40,fm(z.t,0))
  txt(102,70,"PB "+fm(z.pb,0) if z.pb else "PB -",(200,190,170));hm();hmap();hdash()
def enter():
  a=z.sx*VW;b=z.sy*VH;z.sh=[];z.gs=[[g[0]-a,g[1]-b,g] for g in z.sv if g[0]>=a and g[1]>=b and g[0]<a+VW and g[1]<b+VH]
  for k in range(30):
    if len(z.sh)>=1+rn(2):break
    x=rn(VW-12);y=rn(VH-8)
    if wf(x,y):z.sh.append([x,y,rn(5),0,0])
  z.bf=[[rn(VW-5),rn(VH-3),1-2*rn(2),rn(3)] for k in range(2)]
def redraw():
  for x,y,S in z.dr:es(x,y,S)
  for g in z.gs:ds(g[0],g[1],ST if (z.t>>2)&7==0 else SV)
  a=z.sx*VW;b=z.sy*VH;d=[(s[0],s[1],SP[s[4]]) for s in z.sh]+[(z.x,z.y,(PB if z.f==0 else PF)[(z.st>>2)&1])]+[(f[0],f[1],BF[f[3]][(z.t>>1)&1]) for f in z.bf]
  for x,y in CH:
    if x>=a and y>=b+16 and x<a+VW-8 and y<b+VH:
      for k in range(3):o=((z.t+k*21)&63)>>2;d.append((x-a+(o>>2),y-b-o,PU[o>7]))
  for x,y,S in d:ds(x,y,S)
  z.dr=d
def go(ix,iy,x,y):
  for a,b,S in z.dr:es(a,b,S)
  for g in z.gs:es(g[0],g[1],SV)
  z.dr=[];z.sx+=ix;z.sy+=iy;z.x=x;z.y=y;scr();enter();hmap()
def box(a,b,c,e,br=0):
  rc(72,40,240,104,BK);rc(74,42,236,100,HB)
  draw_string(84,48,a,GO);draw_string(84,70,b,WH,"small");draw_string(84,82,c,WH,"small")
  draw_string(84,124 if br else 104,e,(255,230,150),"small")
  if br:draw_string(84,98,"ARROWS:WALK  EXE:DASH",(200,200,200),"small");bdg(204,114)
  show_screen();wk();inv(72,40,312,144);scr();redraw();show_screen()
def step(d,v):
  nx=z.x+DX[d]*v;ny=z.y+DY[d]*v;ix=0;iy=0;tx=nx;ty=ny
  if nx<0:ix=-1;tx=VW-12
  elif nx>VW-12:ix=1;tx=0
  elif ny<0:iy=-1;ty=VH-13
  elif ny>VH-13:iy=1;ty=0
  if z.sx+ix<0 or z.sx+ix>=SW or z.sy+iy<0 or z.sy+iy>=SH:return
  if pf((z.sx+ix)*VW+tx,(z.sy+iy)*VH+ty):
    if ix or iy:go(ix,iy,tx,ty)
    else:z.x=tx;z.y=ty
def sheep():
  for f in z.bf:   # butterflies zigzag about
    f[0]+=f[2];f[1]+=(1,0,-1,0)[(z.t>>2)&3]
    if f[0]<1 or f[0]>VW-7 or rn(60)==0:f[2]=-f[2]
    f[1]=1 if f[1]<1 else VH-4 if f[1]>VH-4 else f[1]
  for s in z.sh:
    s[3]-=1
    if s[3]<=0:s[2]=rn(6);s[3]=20+rn(50)
    if s[2]<4 and z.t&1:
      nx=s[0]+DX[s[2]];ny=s[1]+DY[s[2]]
      if nx>=0 and ny>=0 and nx<=VW-12 and ny<=VH-8 and wf(nx,ny):s[0]=nx;s[1]=ny;s[4]=(nx+ny>>2)&1
      else:s[3]=0
def wind():
  c=z.wc;z.wc=0 if c>TW+30 else c+1
  for j in range(TH):
    i=j*TW+c
    if c<TW:
      u=CUR[i];t=13 if u==1 else 14 if u==12 else 0
      if t:dtile(i,t,u);CUR[i]=t
    if c>2 and c<TW+3:
      u=CUR[i-3];t=1 if u==13 else 12 if u==14 else 0
      if t:dtile(i-3,t,u);CUR[i-3]=t
def save():
  try:f=open("goldenrealm.txt","w");f.write(str(z.pb));f.close()   # keep the record between sessions if files work
  except Exception:pass
def load():
  try:
    f=open("goldenrealm.txt");s=f.read();f.close();n=0
    for ch in s:n=n*10+ord(ch)-48 if ch>="0" and ch<="9" else n
    z.pb=n
  except Exception:pass
def finish():
  t=z.t;old=z.pb;sec=0;n=t
  while n>=FPS:n-=FPS;sec+=1
  md="GOLD MEDAL!" if sec<MG[0] else "SILVER MEDAL" if sec<MG[1] else "BRONZE MEDAL" if sec<MG[2] else "KEEP TRYING!"
  if old==0 or t<old:z.pb=t;save();r="NEW RECORD!"
  else:r="PB "+fm(old,1)+"  +"+fm(t-old,1)
  box("HARVEST HOME!","TIME "+fm(t,1)+"   "+md,r,"EXE: RUN AGAIN")
def newrun():
  z.sv=[[(p[0]<<4)+4,(p[1]<<4)+3] for p in S0];z.f=2;z.g=0;z.st=0;z.t=0;z.fr=0;z.dc=0;z.dd=0;z.ex=1;z.wc=0
  go(2-z.sx,2-z.sy,162,58);hud();redraw()
def play():
  while 1:
    k=getkey();e=k==95
    if e and not z.ex and z.dc==0:z.dd=6;z.dc=40;hdash()   # dash
    z.ex=e
    if z.dd:z.dd-=1;step(z.f,6)
    elif k in KM:z.f=KM[k];step(z.f,PS);z.st+=1
    if z.dc:z.dc-=1;z.dc or hdash()
    sheep()
    for g in z.gs:
      if abs(g[0]-z.x-2)<9 and abs(g[1]-z.y-4)<10:
        es(g[0],g[1],SV);z.gs=[q for q in z.gs if q!=g];z.sv=[q for q in z.sv if q!=g[2]];z.g+=1
        txt(14,40,str(z.g)+"/"+str(NG),GO);hm(("SHEAF "+str(z.g)+"  " if z.g<NG else "ALL! HEAD HOME ")+fm(z.t,1));break
    if z.g>=NG and abs(z.sx*VW+z.x-930)<20 and abs(z.sy*VH+z.y-414)<20:redraw();finish();return   # back at the longhouse door
    if z.t%3==0:wind()
    if z.mt:z.mt-=1;z.mt or hm()
    z.t+=1;z.fr+=1
    if z.fr>=FPS:z.fr=0;txt(58,40,fm(z.t,0))
    redraw();show_screen();dly(SPD)
load();z.dr=[];z.gs=[];z.sx=2;z.sy=2;newrun()
box("GOLDEN REALM","A cozy harvest speedrun.","Gather "+str(NG)+" sheaves, bring them home.","EXE: START",1)
while 1:
  play();newrun()
