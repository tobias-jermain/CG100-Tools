# TETRIS for Casio fx-CG100 (MicroPython 1.9.4, casioplot)
# LEFT/RIGHT = move, UP = rotate, DOWN = soft drop, EXE = hard drop / start, AC = quit.
from casioplot import *
from random import randint
SPD=0;DAS=6;ARR=2;GH=1
# SPD = extra delay per frame, DAS = frames before a held key repeats, ARR = frames between repeats,
# GH = 1 shows the ghost piece (where the piece will land), 0 hides it
W=384;H=192;CS=9;BW=10;BH=20;OX=147;OY=6
BK=(0,0,0);WH=(255,255,255);BG=(16,16,28);GL=(32,32,50);PN=(28,28,44);TX=(170,170,200);AC=(255,210,40)
PC=((0,200,230),(240,210,0),(160,60,200),(60,190,60),(220,50,50),(40,90,220),(240,140,20))
SH=(((0,1),(1,1),(2,1),(3,1)),((1,0),(2,0),(1,1),(2,1)),((1,0),(0,1),(1,1),(2,1)),((1,0),(2,0),(0,1),(1,1)),
((0,0),(1,0),(1,1),(2,1)),((0,0),(0,1),(1,1),(2,1)),((2,0),(0,1),(1,1),(2,1)))   # I O T S Z J L
GV=(36,32,28,24,20,17,14,11,9,7,6,5,4,3,2)   # frames per row at each level
SC=(0,40,100,300,1200)
KK=(0,1,-1,2,-2)   # wall kicks tried when rotating
class Z:pass
z=Z();z.hi=0
def rc(x,y,w,h,c):
  for i in range(w):
    for j in range(h):set_pixel(x+i,y+j,c)
def dly(n):
  for i in range(n):pass
def lt(c):return (min(c[0]+80,255),min(c[1]+80,255),min(c[2]+80,255))
def dk(c):return ((c[0]*5)>>3,(c[1]*5)>>3,(c[2]*5)>>3)
RT=[]   # RT[p][r] = the 4 cells of piece p in rotation r
for p in range(7):
  s=SH[p];L=[s];n=3 if p>1 else 4
  for r in range(3):
    if p!=1:s=tuple((n-1-y,x) for x,y in s)
    L.append(s)
  RT.append(L)
def pic(c,g):
  # 9x9 cell picture: g 0 = empty, 1 = block, 2 = ghost outline, 3 = white flash
  P=[]
  for y in range(CS):
    r=[]
    for x in range(CS):
      e=x==0 or y==0;f=x==CS-1 or y==CS-1
      if g==0:r.append(GL if e else BG)
      elif g==1:r.append(lt(c) if e else dk(c) if f else c)
      elif g==2:r.append(dk(c) if e or f else BG)
      else:r.append(WH)
    P.append(r)
  return P
CP=[pic(0,0)]+[pic(c,1) for c in PC]+[pic(c,2) for c in PC]+[pic(0,3)]
def cell(x,y,k,sp=set_pixel):
  P=CP[k];X=OX+x*CS;Y=OY+y*CS
  for j in range(CS):
    r=P[j];v=Y+j
    for i in range(CS):sp(X+i,v,r[i])
def mini(x,y,p,sp=set_pixel):
  # small 6 pixel block for the NEXT box
  c=PC[p];l=lt(c);d=dk(c)
  for j in range(6):
    for i in range(6):sp(x+i,y+j,l if i==0 or j==0 else d if i==5 or j==5 else c)
def fits(p,r,x,y):
  for a,b in RT[p][r]:
    X=x+a;Y=y+b
    if X<0 or X>=BW or Y>=BH:return 0
    if Y>=0 and z.b[Y*BW+X]:return 0
  return 1
def dropy():
  y=z.y
  while fits(z.p,z.r,z.x,y+1):y+=1
  return y
def ovl():
  # redraw only the cells of the falling piece and its ghost that changed
  n={}
  if GH:
    g=dropy()
    for a,b in RT[z.p][z.r]:n[(z.x+a,g+b)]=8+z.p
  for a,b in RT[z.p][z.r]:
    if z.y+b>=0:n[(z.x+a,z.y+b)]=1+z.p
  for q in z.o:
    if q not in n:cell(q[0],q[1],z.b[q[1]*BW+q[0]])
  for q in n:
    if z.o.get(q)!=n[q]:cell(q[0],q[1],n[q])
  z.o=n
def txt(x,y,w,s,c=WH):rc(x,y,w,16,PN);draw_string(x+2,y+1,s,c)
def stats():
  txt(14,46,110,str(z.s));txt(14,86,110,str(z.lv));txt(14,126,110,str(z.ln));txt(14,166,110,str(z.hi),AC)
def nbag():
  # 7-bag: each piece once per bag, in random order
  b=[0,1,2,3,4,5,6]
  while b:
    i=randint(0,len(b)-1);z.bg.append(b[i]);b=b[:i]+b[i+1:]
def nxt():
  if len(z.bg)<2:nbag()
  z.p=z.bg[0];z.bg=z.bg[1:];z.r=0;z.x=3;z.y=-1 if z.p==0 else 0;z.gt=0
  rc(268,30,40,22,BG);q=z.bg[0]
  for a,b in RT[q][0]:mini(274+a*7,(30 if q==0 else 34)+b*7,q)
  return fits(z.p,z.r,z.x,z.y)
def lock():
  for a,b in RT[z.p][z.r]:
    if z.y+b>=0:z.b[(z.y+b)*BW+z.x+a]=1+z.p
  for q in z.o:
    if not z.b[q[1]*BW+q[0]]:cell(q[0],q[1],0)   # remove ghost cells
  z.o={};fl=[]
  for y in range(BH):
    f=1
    for x in range(BW):
      if not z.b[y*BW+x]:f=0;break
    if f:fl.append(y)
  if not fl:return
  for k in (15,0):   # flash the full rows white, then clear them
    for y in fl:
      for x in range(BW):cell(x,y,k)
    show_screen();dly(3000)
  nb=[0]*(BW*len(fl))
  for y in range(BH):
    if y in fl:
      for x in range(BW):z.b[y*BW+x]=0
    else:nb=nb+z.b[y*BW:y*BW+BW]
  for y in range(BH):   # repaint only the cells that changed
    for x in range(BW):
      i=y*BW+x
      if nb[i]!=z.b[i]:cell(x,y,nb[i])
  z.b=nb;n=len(fl);z.ln+=n;z.s+=SC[n]*(z.lv+1);v=0;m=z.ln
  while m>=10:m-=10;v+=1
  z.lv=min(v,14)
def frame():
  clear_screen()
  for a,b,w,h in ((0,0,W,6),(0,186,W,6),(0,6,8,180),(134,6,10,180),(240,6,16,180),(376,6,8,180)):rc(a,b,w,h,BK)
  rc(OX-3,OY-3,BW*CS+6,BH*CS+6,(90,90,120));rc(OX-1,OY-1,BW*CS+2,BH*CS+2,BK)
  rc(8,6,126,180,PN);rc(256,6,120,180,PN)
  draw_string(20,12,"TETRIS",AC)
  for i,s in ((0,"SCORE"),(1,"LEVEL"),(2,"LINES"),(3,"BEST")):draw_string(16,34+i*40,s,TX,"small")
  draw_string(266,14,"NEXT",TX,"small");rc(266,28,44,26,BK);rc(268,30,40,22,BG)
  for i,s in ((0,"LEFT/RIGHT: MOVE"),(1,"UP: ROTATE"),(2,"DOWN: SOFT DROP"),(3,"EXE: HARD DROP")):draw_string(262,64+i*12,s,TX,"small")
  for a,b,w,h in ((0,0,100,1),(0,23,100,1),(0,0,1,24),(99,0,1,24),(100,2,2,24),(2,24,100,2)):rc(264+a,150+b,w,h,BK)
  rc(265,151,98,22,WH);draw_string(269,153,"tobias-jermain",BK,"small");draw_string(269,163,"/ CG100-Tools",(0,102,204),"small")
def msg(a,b):
  rc(OX+2,74,BW*CS-4,40,BK);rc(OX+4,76,BW*CS-8,36,PN)
  draw_string(OX+8,80,a,AC,"small");draw_string(OX+8,96,b,WH,"small");show_screen()
def wk():
  while getkey()==95:pass
  while getkey()!=95:pass
  while getkey()==95:pass
def newg():
  z.b=[0]*(BW*BH);z.o={};z.bg=[];z.s=0;z.lv=0;z.ln=0;z.lk=95;z.da=0
  for y in range(BH):
    for x in range(BW):cell(x,y,0)
  stats();nxt()
def play():
  while 1:
    k=getkey();nw=k!=z.lk;z.lk=k;mv=0
    if k==23 or k==25:   # move, repeating while held
      if nw:z.da=0
      else:z.da+=1
      if nw or (z.da>=DAS and (z.da-DAS)%ARR==0):
        d=1 if k==25 else -1
        if fits(z.p,z.r,z.x+d,z.y):z.x+=d;mv=1
    elif k==14 and nw:   # rotate with wall kicks
      r=(z.r+1)&3
      for d in KK:
        if fits(z.p,r,z.x+d,z.y):z.x+=d;z.r=r;mv=1;break
    elif k==34:   # soft drop
      if fits(z.p,z.r,z.x,z.y+1):z.y+=1;z.s+=1;z.gt=0;mv=1
    elif k==95 and nw:   # hard drop
      g=dropy();z.s+=2*(g-z.y);z.y=g;z.gt=GV[z.lv]
    z.gt+=1
    if z.gt>=GV[z.lv]:
      z.gt=0
      if fits(z.p,z.r,z.x,z.y+1):z.y+=1;mv=1
      else:
        ovl();lock()
        if z.s>z.hi:z.hi=z.s
        stats()
        if not nxt():return
        mv=1
    if mv:ovl()
    show_screen();dly(SPD)
frame();newg();msg("TETRIS","EXE: START");wk();newg()
while 1:
  ovl();play();ovl();show_screen()
  msg("GAME OVER","EXE: PLAY AGAIN");wk();newg()
