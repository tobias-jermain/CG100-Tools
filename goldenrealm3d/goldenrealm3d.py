# GOLDEN REALM 3D for Casio fx-CG100 (MicroPython 1.9.4, casioplot)
# UP/DOWN = walk, LEFT/RIGHT = turn, EXE = start/pause, AC = quit. Find all the gold!
from casioplot import *
SPD=0;MV=40;TR=12;IL=1;VD=9;WS=144;NG=20
# SPD = extra delay per frame, MV = walk step (256 = one block), TR = turn step (256 = full turn),
# IL = 1 redraws every other column while turning (faster, stripy), 0 = clean turns,
# VD = view distance in blocks (lower = faster), WS = wall height in pixels at 1 block, NG = gold to find
W=384;H=192;VW=288;VH=160;HOR=80;NC=72;HC=144;N=64;MX0=304;MY0=8;MD=VD<<8
BK=(0,0,0);WH=(255,255,255);PN=(58,38,24);PL=(96,66,40);GO=(255,210,40);DG=(170,110,10);RD=(220,30,30)
QS=(0,6,13,19,25,31,38,44,50,56,62,68,74,80,86,92,98,104,109,115,121,126,132,137,142,147,152,157,162,
167,172,177,181,185,190,194,198,202,206,209,213,216,220,223,226,229,231,234,237,239,241,243,245,247,248,250,
251,252,253,254,255,255,256,256,256)
TY="MTSCKHF"   # mountain, tree, stone wall, tower, royal keep, house, fence
TC=((120,105,90),(50,130,50),(175,175,180),(140,140,152),(175,40,40),(228,208,165),(150,100,52))
MC=((85,75,65),(30,95,30),(160,160,165),(130,130,140),(180,40,40),(235,215,170),(120,80,40))
FM=(150,125,40);GM=(255,255,0)
KM={14:0,34:1,23:2,25:3}
class Z:pass
z=Z();z.r=4321;z.hi=0
def mx(a,b):return a if a>b else b
def dv(a,b):
  # integer a/b without // (binary long division)
  q=0;k=0
  while (b<<(k+1))<=a:k+=1
  while k>=0:
    if (b<<k)<=a:a-=b<<k;q|=1<<k
    k-=1
  return q
def rc(x,y,w,h,c):
  for i in range(w):
    for j in range(h):set_pixel(x+i,y+j,c)
def dly(n):
  for i in range(n):pass
def rn(n):
  z.r=(z.r*75+74)%65537
  return z.r%n
def bdg(x,y):
  for a,b,w,h in ((0,0,100,1),(0,23,100,1),(0,0,1,24),(99,0,1,24),(100,2,2,24),(2,24,100,2)):rc(x+a,y+b,w,h,BK)
  rc(x+1,y+1,98,22,WH);draw_string(x+5,y+3,"tobias-jermain",BK,"small");draw_string(x+5,y+13,"/ CG100-Tools",(0,102,204),"small")
clear_screen();draw_string(130,80,"LOADING...",BK);show_screen()
SN=[]
for a in range(256):
  b=a&63;q=a>>6
  SN.append((QS[b],QS[64-b],-QS[b],-QS[64-b])[q])
CX=[]   # camera-plane offset of each screen column (-256..256)
for c in range(NC):
  v=2*c+1-NC;q=dv(abs(v)<<8,NC);CX.append(q if v>0 else -q)
RC=[1<<24]   # 65536/v, for ray step lengths
for v in range(1,320):RC.append(dv(65536,v))
HT=[]   # wall height for distance d (index d>>2)
for i in range((VD<<6)+8):HT.append(dv(WS<<10,4*i+2))
SK=dv(218<<8,WS)
SKY=[];FL=[]
for y in range(VH):
  if y<HOR:SKY.append((90+((y*5)>>2),150+((y*7)>>3),225+(y>>2)));FL.append(0)
  else:
    t=y-HOR;dr=dv(20480,t+1);SKY.append(0)
    if dr>3000:FL.append((205,180,105))
    elif (dr>>7)&1:FL.append((150+t,115+((t*3)>>2),35+(t>>2)))
    else:FL.append((172+t,138+((t*3)>>2),45+(t>>2)))
WB=[0];WO=[0];TI={}
for i in range(7):
  c=TC[i];d=((c[0]*3)>>2,(c[1]*3)>>2,(c[2]*3)>>2);e=(c[0]>>1,c[1]>>1,c[2]>>1);TI[TY[i]]=1+i*3
  WB.append(c);WB.append(d);WB.append(e);WO.append(e);WO.append(e);WO.append((e[0]>>1,e[1]>>1,e[2]>>1))
def world():
  g=[[' ']*N for i in range(N)]
  def put(x,y,c):
    if x>0 and y>0 and x<N-1 and y<N-1:g[y][x]=c
  for i in range(N):
    g[0][i]='M';g[N-1][i]='M';g[i][0]='M';g[i][N-1]='M'
    for k in range(rn(3)):put(1+k,i,'M');put(N-2-k,i,'M');put(i,1+k,'M');put(i,N-2-k,'M')
  for n in range(12):   # forests
    cx=2+rn(N-4);cy=2+rn(N-4);r=2+rn(3)
    for y in range(cy-r,cy+r+1):
      for x in range(cx-r,cx+r+1):
        if (x-cx)*(x-cx)+(y-cy)*(y-cy)<=r*r and rn(3):put(x,y,'T')
  for n in range(70):put(2+rn(N-4),2+rn(N-4),'T')
  for n in range(14):   # fences between the fields
    x=3+rn(N-12);y=3+rn(N-12);d=rn(2)
    for k in range(4+rn(6)):
      if rn(5):put(x+k*(1-d),y+k*d,'F')
  for cx,cy in ((12,12),(50,13),(13,50),(51,50),(46,30)):   # villages
    for n in range(6):
      x=cx+rn(9)-4;y=cy+rn(9)-4
      for a in range(-1,3):
        for b in range(-1,3):put(x+a,y+b,' ')
      put(x,y,'H');put(x+1,y,'H');put(x,y+1,'H');put(x+1,y+1,'H')
  for y in range(23,42):
    for x in range(23,42):put(x,y,' ')
  for i in range(26,38):   # castle walls, towers, gate and keep
    put(i,26,'S');put(i,37,'S');put(26,i,'S');put(37,i,'S')
  for x,y in ((25,25),(36,25),(25,36),(36,36)):
    for a in range(3):
      for b in range(3):put(x+a,y+b,'C')
  put(31,37,' ');put(32,37,' ');put(31,26,' ');put(32,26,' ')
  for y in range(30,34):
    for x in range(30,34):put(x,y,'K')
  for y in range(42,47):
    for x in range(29,36):put(x,y,' ')
  return [''.join(r) for r in g]
M=world()
def free(x,y):return M[y>>8][x>>8]==' '
def coins():
  z.cn=[]
  while len(z.cn)<NG:
    x=2+rn(N-4);y=2+rn(N-4)
    if M[y][x]==' ' and M[y-1][x]==' ' and M[y+1][x]==' ' and M[y][x-1]==' ' and M[y][x+1]==' ' and abs(x-32)+abs(y-42)>6:
      ok=1
      for c in z.cn:
        if c[0]>>8==x and c[1]>>8==y:ok=0
      if ok:z.cn.append([(x<<8)+128,(y<<8)+128])
OT=[0]*NC;OB=[0]*NC;OK=[0]*NC;ZB=[0]*NC;S0=[VH]*NC;S1=[0]*NC
def pc(x,a,e,t,b,k,sp=set_pixel):
  # paint rows a..e-1 of the 4 pixel wide column at x: sky, wall (k) or field
  for y in range(a,t if t<e else e):
    c=SKY[y];sp(x,y,c);sp(x+1,y,c);sp(x+2,y,c);sp(x+3,y,c)
  if k:
    o=WO[k];f=WB[k]
    for y in range(a if a>t else t,b if b<e else e):
      c=o if y==t or y==b-1 else f;sp(x,y,c);sp(x+1,y,c);sp(x+2,y,c);sp(x+3,y,c)
  for y in range(a if a>b else b,e):
    c=FL[y];sp(x,y,c);sp(x+1,y,c);sp(x+2,y,c);sp(x+3,y,c)
def walls(il=0):
  # il=1 (turning): repaint every other column, alternating each frame, for twice the speed
  cs=range(NC)
  if il:
    p=z.par;z.par=1-p;cs=range(p,NC,2)
    for c in range(1-p,NC,2):ZB[c]=0
  ca=SN[(z.a+64)&255];sa=SN[z.a];qx=-(sa*169)>>8;qy=(ca*169)>>8
  px=z.x;py=z.y;m0=px>>8;n0=py>>8;fx=px&255;fy=py&255
  for c in cs:
    k=CX[c];rx=ca+((qx*k)>>8);ry=sa+((qy*k)>>8)
    if rx<0:ix=-1;ddx=RC[-rx];sx=(fx*ddx)>>8
    else:ix=1;ddx=RC[rx];sx=((256-fx)*ddx)>>8
    if ry<0:iy=-1;ddy=RC[-ry];sy=(fy*ddy)>>8
    else:iy=1;ddy=RC[ry];sy=((256-fy)*ddy)>>8
    m=m0;n=n0;ch=' '
    while 1:
      if sx<sy:
        d=sx
        if d>MD:break
        m+=ix;sx+=ddx;s=0
      else:
        d=sy
        if d>MD:break
        n+=iy;sy+=ddy;s=1
      ch=M[n][m]
      if ch!=' ':break
    if ch!=' ':
      h=HT[d>>2];t=HOR-(h>>1);b=HOR+(h>>1)
      if t<0:t=0
      if b>VH:b=VH
      kk=TI[ch]+s
    else:t=HOR;b=HOR;kk=0;d=MD
    ZB[c]=d;x=c<<2;t0=OT[c];b0=OB[c]
    if kk!=OK[c]:pc(x,t if t<t0 else t0,b if b>b0 else b0,t,b,kk)
    else:
      if t<t0:pc(x,t,t0+1,t,b,kk)
      elif t>t0:pc(x,t0,t+1,t,b,kk)
      if b<b0:pc(x,b-1,b0,t,b,kk)
      elif b>b0:pc(x,b0-1,b,t,b,kk)
    if S0[c]<S1[c]:pc(x,S0[c],S1[c],t,b,kk);S0[c]=VH;S1[c]=0
    OT[c]=t;OB[c]=b;OK[c]=kk
def sprites(sp=set_pixel):
  ca=SN[(z.a+64)&255];sa=SN[z.a]
  for g in z.cn:
    dx=g[0]-z.x;dy=g[1]-z.y
    if dx>MD or dx<-MD or dy>MD or dy<-MD:continue
    dp=(dx*ca+dy*sa)>>8
    if dp<48 or dp>=MD:continue
    h=HT[dp>>2];lt=(dy*ca-dx*sa)>>8;cx=HC+((lt*h*SK)>>16);r=h>>3
    if r<1:r=1
    if r>14:r=14
    if cx+r<0 or cx-r>=VW:continue
    cy=HOR+(h>>1)-r-(h>>4)
    if cy+r>=VH:cy=VH-1-r
    for X in range(mx(0,cx-r),min(VW,cx+r+1)):
      c=X>>2
      if ZB[c]<=dp:continue
      e=X-cx;hh=CR[r][abs(e)];y0=cy-hh;y1=cy+hh+1
      if hh<1 or e==r or e==-r:
        for Y in range(y0,y1):sp(X,Y,DG)
      else:
        k=WH if e==-(r>>1) else GO
        sp(X,y0,DG)
        for Y in range(y0+1,y1-1):sp(X,Y,k)
        sp(X,y1-1,DG)
      if y0<S0[c]:S0[c]=y0
      if y1>S1[c]:S1[c]=y1
def isq(n):
  r=0
  while (r+1)*(r+1)<=n:r+=1
  return r
CR=[[isq(r*r-e*e) for e in range(r+1)] for r in range(15)]
def mmc(x,y):
  ch=M[y][x]
  if ch!=' ':return MC[TY.find(ch)]
  for g in z.cn:
    if g[0]>>8==x and g[1]>>8==y:return GM
  return FM
def mmp(on):
  x=z.x>>8;y=z.y>>8
  for a in range(-1,2):
    for b in range(-1,2):set_pixel(MX0+x+a,MY0+y+b,RD if on else mmc(x+a,y+b))
def txt(x,y,w,s,big=0):
  rc(x,y,w,16 if big else 11,PN);draw_string(x+2,y+1,s,GO if big else WH,"medium" if big else "small")
def hud():
  txt(298,92,84,str(z.g)+" / "+str(NG),1)
def cmp():
  s=((z.a+16)&255)>>5
  if s!=z.sc:z.sc=s;txt(298,128,84,("EAST","SE","SOUTH","SW","WEST","NW","NORTH","NE")[s],1)
def ovl(y0,y1,c0=8,c1=64):
  # mark rows y0..y1 of columns c0..c1 for repainting on the next frame
  for c in range(c0,c1):
    if y0<S0[c]:S0[c]=y0
    if y1>S1[c]:S1[c]=y1
def box(a,b,c):
  rc(34,52,220,56,PN);rc(36,54,216,52,PL)
  draw_string(46,60,a,GO);draw_string(46,78,b,WH,"small");draw_string(46,92,c,(255,230,150),"small");show_screen()
def wk():
  while getkey()==95:pass
  while getkey()!=95:pass
  while getkey()==95:pass
def frame(il=0):
  walls(il);sprites();show_screen()
def panel():
  rc(VW,0,W-VW,H,PN);rc(VW,0,2,H,BK);rc(0,VH,VW,H-VH,(70,70,82));rc(0,VH,VW,2,BK)
  rc(MX0-2,MY0-2,N+4,N+4,BK)
  for y in range(N):
    r=M[y]
    for x in range(N):
      ch=r[x];set_pixel(MX0+x,MY0+y,FM if ch==' ' else MC[TY.find(ch)])
  for g in z.cn:set_pixel(MX0+(g[0]>>8),MY0+(g[1]>>8),GM)
  draw_string(298,78,"GOLD",(230,200,150),"small");draw_string(298,114,"FACING",(230,200,150),"small")
  draw_string(298,152,"BEST",(230,200,150),"small");txt(298,164,84,str(z.hi)+" STEPS" if z.hi else "-")
  draw_string(6,164,"UP/DOWN: WALK",WH,"small");draw_string(6,176,"LEFT/RIGHT: TURN",WH,"small")
  draw_string(112,170,"EXE:PAUSE",(255,230,150),"small");bdg(180,164)
def newg():
  coins();z.x=(32<<8)+0;z.y=(44<<8)+128;z.a=192;z.g=0;z.st=0;z.sc=-1;z.par=0;z.dt=0
  for c in range(NC):OT[c]=0;OB[c]=VH;OK[c]=-1;S0[c]=VH;S1[c]=0
  panel();hud();cmp();mmp(1);walls()
def collect():
  for g in z.cn:
    if abs(g[0]-z.x)<100 and abs(g[1]-z.y)<100:
      z.cn=[q for q in z.cn if q!=g];z.g+=1;mmp(0);mmp(1);hud();return
def play():
  while 1:
    k=getkey()
    if k==95:
      box("PAUSED","Find the gold in the fields","EXE: CONTINUE");wk();ovl(52,108);frame()
    if k in KM:
      d=KM[k]
      if d>1:z.a=(z.a+(TR if d==3 else -TR))&255
      else:
        v=MV if d==0 else -MV;dx=(SN[(z.a+64)&255]*v)>>8;dy=(SN[z.a]*v)>>8;mmp(0)
        e=z.x+dx+(64 if dx>0 else -64)
        if free(e,z.y-48) and free(e,z.y+48):z.x+=dx
        e=z.y+dy+(64 if dy>0 else -64)
        if free(z.x-48,e) and free(z.x+48,e):z.y+=dy
        z.st+=1;collect();mmp(1)
      z.dt=d>1
      if z.dt:cmp()
      frame(IL and d>1)
      if z.g>=NG:return
    elif z.dt:z.dt=0;frame()   # turning stopped: finish the skipped columns
    dly(SPD)
while 1:
  newg();sprites();box("GOLDEN REALM 3D","Find "+str(NG)+" gold in the fields","EXE: START")
  wk();ovl(52,108);frame();play()
  if z.hi==0 or z.st<z.hi:z.hi=z.st
  box("ALL GOLD FOUND!","The king thanks you!",str(z.st)+" steps   EXE: AGAIN");wk()
