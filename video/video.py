# VIDEO PLAYER for Casio fx-CG100 (MicroPython 1.9.4, casioplot)
# EXE = play/pause, RIGHT = next frame (paused), LEFT = restart, UP/DOWN = faster/slower, AC = quit.
# Make your own clip on a PC with mkvideo.py, which rewrites the DATA block below.
from casioplot import *
SPD=0;LP=1;ST=400
W=384;H=192;BK=(0,0,0);GR=(90,90,90);BU=(0,102,204)
#<DATA
CW=48;CH=24;S=8;NF=60
P=((19,24,60),(39,139,60),(249,203,39),(84,72,54),)
D=(
"$)%#$&M'%#$&O&&cccccccccccc)ccccG$!$$##$&'%%L$&&&%M(%#$&N&%#$&!%%##$&'$%K%#($%#$&K$#'%%#$&O&%#$&M'%#$&O&&!'&##&&M%##$&&$",
"%L$##$&'%%K$##$&'%%L$&&&%M(%#$&N&%#$&!*&#O(#M&##$&O%##$&'$%K%#($%#$&K$#'%%#$&O&%#$&M'%#$&O&&!cL'#N&##&&M%##$&&$%L$##$&'%",
"%K$##$&'%%L$&&&%M(%#$&N&%#$&!cc?&#O(#M&##$&O%##$&'$%K%#($%#$&K$#'%%#$&O&%#$&M'%#$&O&&!cccb'#N&##&&M%##$&&$%L$##$&'%%K$##",
"$&'%%L$&&&%M(%#$&N&%#$&!ccccT&#O(#M&##$&O%##$&'$%K%#($%#$&K$#'%%#$&O&%#$&M'%#$&O&&!cccccc7'#N&##&&M%##$&&$%L$##$&'%%K$##",
"$&'%%L$&&&%M(%#$&N&%#$&!ccccccc*&#O(#M&##$&O%##$&'$%K%#($%#$&K$#'%%#$&O&%#$&M'%#$&O&&!ccccccc-&&O$&#'%Q&%K$##$&'%%K$##$&",
"'%%K%#'$%#$&K&#Q(#O&#!cccccc=$&#&%O(%L$#'%%#$&J%#($%#$&J%#($%#$&J&#'$&L&##%&O'#!cccc^&&O$&#'%Q&%K$##$&'%%K$##$&'%%K%#'$%",
"#$&K&#Q(#O&#!cccc.$&#&%O(%L$#'%%#$&J%#($%#$&J%#($%#$&J&#'$&L&##%&O'#!ccN&&O$&#'%Q&%K$##$&'%%K$##$&'%%K%#'$%#$&K&#Q(#O&#!",
"c_$&#&%O(%L$#'%%#$&J%#($%#$&J%#($%#$&J&#'$&L&##%&O'#!?&&O$&#'%Q&%K$##$&'%%K$##$&'%%K%#'$%#$&K&#Q(#O&#!@(%L$#'%%#$&J%#($%",
"#$&J%#($%#$&J&#'$&L&##%&O'#!?$##$&'%%K$##$&'%%K%#'$%#$&K&#Q(#O&#!@%#($%#$&J&#'$&L&##%&O'#!B$##$&'%%L$&&&%M(%#$&N&%#$&!C%",
"##$&'$%K%#($%#$&K$#'%%#$&O&%#$&M'%#$&O&&!E&##&&M%##$&&$%L$##$&'%%K$##$&'%%L$&&&%M(%#$&N&%#$&!H&#O(#M&##$&O%##$&'$%K%#($%",
"#$&K$#'%%#$&O&%#$&M'%#$&O&&!cc+'#N&##&&M%##$&&$%L$##$&'%%K$##$&'%%L$&&&%M(%#$&N&%#$&!cc^&#O(#M&##$&O%##$&'$%K%#($%#$&K$#",
"'%%#$&O&%#$&M'%#$&O&&!cccc@'#N%##&&#$#M$##$&'$#L$&($%L$&($%L$&'%%M(%#$&N&%#$&!ccccc2&#O(#Q&#K$&#$%'%#K%%'$&#$#K%%'$&#$#K",
"&%Q'%#$&O&&!ccccccQ'#O%&#&#L$&'&#J$&#$%(%#J$&#$%(%#J$&#%%'$#L(%O&%#$&!cccccccA&#O(#Q&#K$&#$%'%#K%%'$&#$#K%%'$&#$#K&%Q'%#",
"$&O&&!ccccccc>&&O$&#'%M$&#&%O$&#%%'$#K$&#$%(%#K$%'$&#%#O$&#&#M(#O&#!ccccccK$&#&%N$&#(%M&%&$&L%%'$&#$#K%%'$&#$#L$%&$&#%#M",
"&&#&#N'#!ccccc)&&O$&#'%M$&#&%O$&#%%'$#K$&#$%(%#K$%'$&#%#O$&#&#M(#O&#!cccc6$&#&%N$&#(%M&%&$&L%%'$&#$#K%%'$&#$#L$%&$&#%#M&",
"&#&#N'#!ccS&&O$&#'%M$&#&%O$&#%%'$#K$&#$%(%#K$%'$&#%#O$&#&#M(#O&#!ca$&#&%N$&#(%M&%&$&L%%'$&#$#K%%'$&#$#L$%&$&#%#M&&#&#N'#",
"!>&&O$&#'%M$&#&%O$&#%%'$#K$&#$%(%#K$%'$&#%#O$&#&#M(#O&#!;$&#(%M&%&$&L%%'$&#$#K%%'$&#$#L$%&$&#%#M&&#&#N'#!9$&#%%'$#K$&#$%",
"(%#K$%'$&#%#O$&#&#M(#O&#!8%%'$&#$#L$%&$&#%#M&&#&#N'#!6$&#$%(%#J$&#%%'$#L(%O&%#$&!5$&#$%'%#K%%'$&#$#K%%'$&#$#K&%Q'%#$&O&&",
"!6%&#&#L$&'&#J$&#$%(%#J$&#$%(%#J$&#%%'$#L(%O&%#$&!5&#O(#Q&#K$&#$%'%#K%%'$&#$#K%%'$&#$#K&%Q'%#$&O&&!cT'#O%&#&#L$&'&#J$&#$",
"%(%#J$&#$%(%#J$&#%%'$#L(%O&%#$&!ccD&#O(#Q&#K$&#$%'%#K%%'$&#$#K%%'$&#$#K&%Q'%#$&O&&!cccc$'#O%&#&#L$&'&#J$&#$%(%#J$&#$%(%#",
"J$&#%%'$#L(%O&%#$&!ccccS&#O(#Q&#K$&#$%'%#K%%'$&#$#K%%'$&#$#K&%Q'%#$&O&&!cccccc3'#O%&#&#L$&'&#J$&#$%(%#J$&#$%(%#J$&#%%'$#",
"L(%O&%#$&!ccccccc#&#O(#Q&#K$&#$%'%#K%%'$&#$#K%%'$&#$#K&%Q'%#$&O&&!cccccc`&&O$&#'%M$&#&%O$&#%%'$#K$&#$%(%#K$%'$&#%#O$&#&#",
"M(#O&#!cccccc-$&#&%N$&#(%M&%&$&L%%'$&#$#K%%'$&#$#L$%&$&#%#M&&#&#N'#!ccccJ&&O$&#'%M$&#&%O$&#%%'$#K$&#$%(%#K$%'$&#%#O$&#&#",
"M(#O&#!cccY$&#&%N$&#(%M$%'$%#$&K$#)$&K$#)$&K%#'$&M%##&&#$#N'#!cc:&&O$&#'%Q&%K$##$&'%%K$##$&'%%K%#'$%#$&K&#Q(#O&#!cJ$&#&%",
"O(%L$#'%%#$&J%#($%#$&J%#($%#$&J&#'$&L&##%&O'#!+&&O$&#'%Q&%K$##$&'%%K$##$&'%%K%#'$%#$&K&#Q(#O&#!,(%L$#'%%#$&J%#($%#$&J%#(",
"$%#$&J&#'$&L&##%&O'#!+$##$&'%%K$##$&'%%K%#'$%#$&K&#Q(#O&#!}",
)
#DATA>
OX=(W-CW*S)>>1;OY=(H-CH*S)>>1
class Z:pass
z=Z()
def rc(x,y,w,h,c):
  sp=set_pixel
  for j in range(y,y+h):
    for i in range(x,x+w):sp(i,j,c)
def dly(n):
  for i in range(n):pass
def key(k):
  while getkey()==k:pass
# Data: one char per value, value=ord(c)-35 with the backslash skipped.
# A value of 63 means "add 63 and read on". '!' ends a frame, '}' ends the clip.
def ch():
  s=D[z.l]
  if z.p>=len(s):z.l+=1;z.p=0;s=D[z.l]
  c=s[z.p];z.p+=1;return c
def num(c):
  v=0
  while 1:
    o=ord(c);d=o-35-(o>92);v+=d
    if d<63:return v
    c=ch()
# Draws one frame as runs of (skip, length, colour) over the CW x CH cell grid.
def frame():
  x=0;y=0;sp=set_pixel
  while 1:
    c=ch()
    if c=='!':return 1
    if c=='}':return 0
    x+=num(c);n=num(ch());o=ord(ch());k=P[o-35-(o>92)]
    while x>=CW:x-=CW;y+=1
    while n>0:
      m=CW-x
      if m>n:m=n
      X=OX+x*S;Y=OY+y*S
      for j in range(Y,Y+S):
        for i in range(X,X+m*S):sp(i,j,k)
      n-=m;x+=m
      if x>=CW:x=0;y+=1
def start():
  z.l=0;z.p=0;z.f=0
  clear_screen();rc(OX,OY,CW*S,CH*S,P[0])
def bdg(x,y):
  for a,b,w,h in ((0,0,100,1),(0,23,100,1),(0,0,1,24),(99,0,1,24),(100,2,2,24),(2,24,100,2)):rc(x+a,y+b,w,h,BK)
  draw_string(x+5,y+3,"tobias-jermain",BK,"small");draw_string(x+5,y+13,"/ CG100-Tools",BU,"small")
def title():
  clear_screen();draw_string(120,24,"VIDEO PLAYER",BK)
  draw_string(96,50,str(NF)+" frames, "+str(CW)+"x"+str(CH)+" cells",GR,"small")
  t=("EXE : PLAY / PAUSE","RIGHT : NEXT FRAME (PAUSED)","LEFT : RESTART","UP / DOWN : FASTER / SLOWER")
  for i in range(4):draw_string(96,68+i*12,t[i],GR,"small")
  bdg(142,130);show_screen()
  while getkey()!=95:pass
  key(95)
def run():
  start();pz=0
  while 1:
    k=getkey()
    if k==95:key(95);pz=1-pz
    elif k==23:key(23);start()
    elif k==14:SP[0]-=ST;key(14)
    elif k==34:SP[0]+=ST;key(34)
    if SP[0]<0:SP[0]=0
    if pz and k!=25:continue
    if k==25:key(25)
    if frame():z.f+=1;show_screen();dly(SP[0])
    elif LP:start()
    else:
      show_screen();pz=1
      while getkey()!=95:pass
      key(95);start();pz=0
SP=[SPD]
title();run()
