# RUBIX TIMER for Casio fx-CG100 (MicroPython 1.9.4, casioplot): speedcubing timer with scrambles and averages.
# EXE = inspect, hold EXE then let go = start, any key = stop, UP = +2/DNF, DOWN = delete, LEFT/RIGHT = 2x2/3x3, AC = quit.
from casioplot import *
from random import randint
INS=15;HD=300;TPS=2000;SV=1
# INS = inspection seconds (0 = off), HD = hold time in ms before you can start,
# TPS = timer ticks per second, only used if the calculator has no clock (see description.md), SV = 1 saves times
W=384;H=192;BK=(0,0,0);WH=(255,255,255);TX=(30,34,60);GY=(120,124,150);RD=(214,30,30);GN=(20,160,70);HL=(255,196,40)
SG=(63,6,91,79,102,109,125,7,127,111)   # 7-segment digits 0-9 (bits a..g)
DW=22;DH=44;TK=4;TY=58;DNF=999999
try:
  from time import ticks_ms
  def now():return ticks_ms()
except Exception:now=None
class Z:pass
z=Z();z.p=1;z.ss=[[],[]];z.sc="";z.ds="";z.dc=0;z.tk=0
def dv(a,b):   # a/b without // (binary long division)
  q=0;k=0
  while (b<<(k+1))<=a:k+=1
  while k>=0:
    if (b<<k)<=a:a-=b<<k;q|=1<<k
    k-=1
  return q
def rc(x,y,w,h,c):
  for j in range(y,y+h):
    for i in range(x,x+w):set_pixel(i,j,c)
def tick():   # milliseconds, or loop ticks when there is no clock
  if now:return now()
  z.tk+=1;return z.tk
def ms(a,b):   # time between two tick() readings, in ms
  return b-a if now else dv((b-a)*1000,TPS)
def two(n):return ("0" if n<10 else "")+str(n)
def fm(c):   # centiseconds -> "s.cc" or "m:ss.cc"
  if c>=DNF:return "DNF"
  s=dv(c,100);c-=s*100;m=dv(s,60);s-=m*60
  return (str(m)+":"+two(s) if m else str(s))+"."+two(c)
def val(t):return DNF if t[1]==2 else t[0]+200*t[1]   # time with penalty
def ao(n):   # WCA average of the last n: drop best and worst
  L=z.ss[z.p]
  if len(L)<n:return "-"
  v=[val(t) for t in L[len(L)-n:]];v.sort()
  if v[n-2]>=DNF:return "DNF"
  s=0
  for x in v[1:n-1]:s+=x
  return fm(dv(s+((n-2)>>1),n-2))
def scram():   # random-move scramble: no face twice in a row, no R L R
  F="RUF" if z.p==0 else "RUFLDB";n=11 if z.p==0 else 20;s=[];a=-1;b=-1
  while len(s)<n:
    f=randint(0,len(F)-1)
    if f==a or (len(F)>3 and f%3==a%3 and f%3==b%3 and b>=0):continue
    b=a;a=f;s.append(F[f]+("","2","'")[randint(0,2)])
  z.sc=" ".join(s)
def seg(x,y,d,c):   # one 7-segment digit
  m=SG[d];h=DH>>1
  for i,r in ((0,(TK,0,DW-2*TK,TK)),(1,(DW-TK,TK,TK,h-TK)),(2,(DW-TK,h,TK,h-TK)),(3,(TK,DH-TK,DW-2*TK,TK)),
    (4,(0,h,TK,h-TK)),(5,(0,TK,TK,h-TK)),(6,(TK,h-(TK>>1),DW-2*TK,TK))):
    if m>>i&1:rc(x+r[0],y+r[1],r[2],r[3],c)
def big(s,c):   # draw the time in big digits, redrawing only what changed
  if s==z.ds and c==z.dc:return
  if len(s)!=len(z.ds) or c!=z.dc:rc(4,TY,250,DH+2,WH);z.ds=" "*len(s);z.dc=c
  if s=="DNF":draw_string(70,TY+14,"DNF",c);z.ds=s;show_screen();return
  x=8
  for i in range(len(s)):
    ch=s[i];w=8 if ch in ":." else DW+6
    if ch!=z.ds[i]:
      rc(x,TY,w,DH,WH)
      if ch==":":rc(x+2,TY+12,TK,TK,c);rc(x+2,TY+DH-16,TK,TK,c)
      elif ch==".":rc(x+2,TY+DH-TK,TK,TK,c)
      elif ch=="-" or ch=="+":rc(x+TK,TY+(DH>>1)-2,DW-2*TK,TK,c)
      if ch=="+":rc(x+(DW>>1)-2,TY+TK*3,TK,DH-TK*6,c)
      elif ch>="0" and ch<="9":seg(x,TY,ord(ch)-48,c)
    x+=w
  z.ds=s;show_screen()
def txt(x,y,w,s,c=TX):rc(x,y,w,12,WH);draw_string(x,y,s,c,"small")
def side():   # stats panel and recent times
  L=z.ss[z.p];b=DNF;n=0;t=0
  for x in L:
    v=val(x)
    if v<b:b=v
    if v<DNF:n+=1;t+=v
  rc(262,50,122,120,WH);y=52
  for a,v in (("SOLVES",str(len(L))),("BEST",fm(b) if L else "-"),("AO5",ao(5)),("AO12",ao(12)),("MEAN",fm(dv(t,n)) if n else "-")):
    draw_string(266,y,a,GY,"small");draw_string(318,y,v,TX,"small");y+=18
  rc(4,112,256,58,WH);x=8;y=116;k=len(L)-1;j=0
  while k>=0 and j<8:
    t=L[k];s=fm(val(t))+("+" if t[1]==1 else "")
    draw_string(x,y,str(k+1)+". "+s,TX if j else BK,"small");j+=1;k-=1;x+=124
    if j%2==0:x=8;y+=13
def top():
  rc(0,0,W,48,WH);draw_string(4,2,"RUBIX TIMER",TX);x=150
  for i in range(2):
    t=("2X2","3X3")[i]
    if i==z.p:rc(x,2,30,13,HL)
    draw_string(x+4,3,t,TX,"small");x+=36
  draw_string(240,3,("INSPECT "+str(INS)+"S" if INS else "NO INSPECTION")+("" if now else " (TPS)"),GY,"small")
  s=z.sc;y=20
  while s:
    t=s[:52]
    if len(s)>52:t=t[:t.rfind(" ")]
    draw_string(4,y,t,BK,"small");s=s[len(t):].strip();y+=13
def full():
  clear_screen();top();side()
  rc(0,H-15,W,1,TX);draw_string(4,H-13,"EXE INSPECT/HOLD  UP +2/DNF  DOWN DEL  L/R CUBE",GY,"small")
  z.ds="";L=z.ss[z.p];big(fm(val(L[-1])) if L else "0.00",BK)
def save():
  if not SV:return
  try:
    f=open("rubixtimer.txt","w")
    for p in range(2):
      for t in z.ss[p]:f.write(str(p)+" "+str(t[0])+" "+str(t[1])+"\n")
    f.close()
  except Exception:pass
def load():
  try:
    f=open("rubixtimer.txt");s=f.read();f.close()
    for l in s.split("\n"):
      v=[];n=-1
      for ch in l+" ":
        if ch>="0" and ch<="9":n=(n if n>=0 else 0)*10+ord(ch)-48
        elif n>=0:v.append(n);n=-1
      if len(v)==3 and v[0]<2:z.ss[v[0]].append([v[1],v[2]])
  except Exception:pass
def rel():   # wait until no key is held
  while getkey():pass
def hold(t0=None,lim=0):   # EXE held: red until held long enough, then green; True once let go when green
  a=tick();c=RD;big(fm(0) if t0 is None else str(lim-dv(ms(t0,a),1000)),RD)
  while getkey()==95:
    b=tick()
    if c==RD and ms(a,b)>=HD:c=GN;big(z.ds,GN)
  return c==GN
def inspect():   # count down INS seconds; returns penalty (0, 1 = +2, 2 = DNF) or -1 if cancelled
  rel();t0=tick();pn=0
  while 1:
    e=dv(ms(t0,tick()),1000);r=INS-e
    if r>-2:big(str(r) if r>0 else "+2",RD if r<=3 else BK)
    else:big("DNF",RD)
    pn=0 if r>0 else 1 if r>-2 else 2
    k=getkey()
    if k==95:
      if hold(t0,INS):return 2 if dv(ms(t0,tick()),1000)>=INS+2 else pn
    elif k and k!=95:rel();return -1
def timing(pn):   # run the clock until any key; returns centiseconds
  t0=tick();lt=-1
  while 1:
    k=getkey();t=tick()
    if k:break
    if now:
      c=dv(ms(t0,t),10);d=dv(c,10)
      if d!=lt:lt=d;big(fm(c)[:-1],BK)
    elif lt<0:lt=0;big("-.--",BK)
  c=dv(ms(t0,t),10);L=z.ss[z.p];L.append([c,pn]);save();scram();full();rel()
def run():
  scram();full()
  while 1:
    k=getkey()
    if k==95:
      if INS:
        pn=inspect()
        if pn>=0:timing(pn)
        else:full()
      elif hold():timing(0)
      else:full()
    elif k in (23,25):z.p=1-z.p;scram();full();rel()
    elif k==14 and z.ss[z.p]:t=z.ss[z.p][-1];t[1]=(t[1]+1)%3;save();full();rel()
    elif k==34 and z.ss[z.p]:z.ss[z.p]=z.ss[z.p][:-1];save();full();rel()
load();run()
