# NAME for Casio fx-CG100 (MicroPython 1.9.4, casioplot)
# Arrows = move, EXE = start/pause, AC = quit. SPD = extra delay per frame.
from casioplot import *
SPD=2000
W=384;H=192
BK=(0,0,0);WH=(255,255,255);BL=(33,33,255)
KM={14:0,23:1,34:2,25:3}   # key code -> direction (up,left,down,right)
DX=(0,-1,0,1);DY=(-1,0,1,0)
class Z:pass
z=Z();z.x=192;z.y=96;z.hi=0
def rc(x,y,w,h,c):
  for i in range(w):
    for j in range(h):set_pixel(x+i,y+j,c)
def dly(n):
  for i in range(n):pass
def wk():
  while getkey()==95:pass
  while getkey()!=95:pass
  while getkey()==95:pass
def run():
  while 1:
    k=getkey()
    if k==95:wk()                 # EXE pauses
    if k in KM:
      rc(z.x,z.y,8,8,WH)          # erase old position
      d=KM[k];z.x=min(z.x+DX[d]*4,W-8);z.y=min(z.y+DY[d]*4,H-8)
      if z.x<0:z.x=0
      if z.y<0:z.y=0
    rc(z.x,z.y,8,8,BL);show_screen()
    dly(SPD)
clear_screen()
draw_string(4,4,"TEMPLATE",BK);draw_string(4,20,"EXE:START",(90,90,90),"small");show_screen()
wk();clear_screen()
run()
