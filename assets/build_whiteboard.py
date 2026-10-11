"""Render the whiteboard-style learning notes shown on the GitHub profile.

The notes describe code and planned checks; they do not claim an AWS deployment.
Requires Pillow. Font is Handlee (SIL Open Font License; see fonts/OFL.txt).
"""
from __future__ import annotations
import math
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT=Path(__file__).parent
HAND=str(OUT/'fonts/Handlee-Regular.ttf')
SANS='/usr/share/fonts/liberation-sans-fonts/LiberationSans-Bold.ttf'
INK=(35,55,70)
CYAN=(27,142,165)
ORANGE=(207,111,37)
PAPER=(250,248,239)
MUTED=(101,117,126)
R=random.Random(31)

def font(n,bold=False): return ImageFont.truetype(SANS if bold else HAND,n)

def paper(w,h):
    im=Image.new('RGB',(w,h),PAPER); d=ImageDraw.Draw(im)
    for y in range(32,h,42): d.line((0,y,w,y),fill=(234,233,223),width=1)
    for x in range(31,w,42): d.line((x,0,x,h),fill=(240,238,228),width=1)
    d.line((23,0,23,h),fill=(238,194,185),width=2)
    return im

def txt(d,xy,s,size=28,color=INK,bold=False): d.text(xy,s,font=font(size,bold),fill=color)

def stroke(d,pts,color=INK,width=3):
    # Two restrained, offset strokes give the line a sketched edge.
    d.line(pts,fill=color,width=width,joint='curve')
    if len(pts)>1:
        d.line([(x+R.choice([-2,-1,0,1]),y+R.choice([-1,0,1])) for x,y in pts],fill=(*color[:3],) if len(color)==3 else color,width=1,joint='curve')

def loop_box(d,box,color=CYAN,width=3):
    x0,y0,x1,y1=box
    pts=[(x0+7,y0),(x1-8,y0+R.randint(-2,2)),(x1,y0+8),(x1+R.randint(-2,2),y1-8),(x1-8,y1),(x0+7,y1+R.randint(-2,2)),(x0,y1-8),(x0+R.randint(-2,2),y0+8),(x0+7,y0)]
    stroke(d,pts,color,width)

def arrow(d,coords,color=ORANGE):
    stroke(d,coords,color,3)
    x1,y1=coords[-2]; x2,y2=coords[-1]
    a=math.atan2(y2-y1,x2-x1)
    for off in (-.55,.55):
        end=(x2-13*math.cos(a+off),y2-13*math.sin(a+off))
        stroke(d,[(x2,y2),end],color,3)

def circled(d,x,y,n):
    for offset in (0,2): d.ellipse((x-24-offset,y-24,x+24,y+24+offset),outline=ORANGE,width=2)
    txt(d,(x-11,y-19),str(n),30,ORANGE)

def node(d,x,y,w,title,subtitle=None,color=CYAN):
    loop_box(d,(x,y,x+w,y+74),color)
    txt(d,(x+15,y+6),title,25,INK)
    if subtitle: txt(d,(x+15,y+39),subtitle,19,MUTED)

def desktop():
    im=paper(1200,980); d=ImageDraw.Draw(im)
    txt(d,(49,30),'The lab whiteboard',51,INK)
    txt(d,(51,92),'Three questions I want to explain clearly in an interview',26,CYAN)
    txt(d,(840,101),'CODE PREPARED  /  AWS UNVERIFIED',15,ORANGE,True)
    stroke(d,[(45,139),(1161,139)],(172,187,185),2)
    circled(d,77,190,1); txt(d,(118,163),'How does a web request reach EC2?',35)
    node(d,51,232,214,'Browser','HTTP request')
    node(d,341,232,214,'Public IP','internet-facing')
    node(d,632,232,214,'Security group','TCP 80 only')
    node(d,923,232,220,'EC2 + Nginx','serves the page',ORANGE)
    for a,b in [(265,341),(555,632),(846,923)]:arrow(d,[(a,269),(b,269)])
    txt(d,(58,327),'Why it matters:',25,ORANGE)
    txt(d,(223,327),'SSH is closed by default. EBS is encrypted. IMDSv2 is required.',24)
    txt(d,(57,363),'Check it:',25,CYAN);txt(d,(171,363),'HTTP response, instance status checks, and Nginx service.',24)
    stroke(d,[(45,408),(1161,408)],(172,187,185),2)
    circled(d,77,459,2); txt(d,(118,432),'What makes the subnet public?',35)
    loop_box(d,(47,500,1151,664),CYAN)
    txt(d,(67,507),'VPC  10.42.0.0/16',27,CYAN)
    node(d,66,554,215,'Internet','request',ORANGE)
    node(d,346,554,213,'Internet GW','route target')
    node(d,624,554,233,'Public subnet','10.42.1.0/24')
    node(d,921,554,207,'EC2 + SG','public IP')
    for a,b in [(281,346),(559,624),(857,921)]:arrow(d,[(a,591),(b,591)])
    txt(d,(57,688),'Route: 0.0.0.0/0 to the gateway  +  instance public IP  +  SG TCP 80',24)
    txt(d,(57,724),'Check it:',25,CYAN);txt(d,(171,724),'route table, subnet association, public IP, then HTTP.',24)
    stroke(d,[(45,770),(1161,770)],(172,187,185),2)
    circled(d,77,821,3); txt(d,(118,795),'If the page times out, where do I look?',35)
    node(d,56,854,235,'EC2 status','healthy?')
    node(d,351,854,235,'Route + SG','HTTP allowed?')
    node(d,647,854,235,'Nginx logs','service ready?')
    node(d,943,854,202,'CloudWatch','CPU + checks',ORANGE)
    for a,b in [(291,351),(586,647),(882,943)]:arrow(d,[(a,891),(b,891)])
    txt(d,(59,940),'Metrics add context; healthy CPU alone does not prove the website is reachable.',23,CYAN)
    return im

def mobile():
    im=paper(600,1640);d=ImageDraw.Draw(im)
    txt(d,(39,26),'The lab whiteboard',41)
    txt(d,(41,79),'How I would explain the AWS labs',23,CYAN)
    txt(d,(41,111),'CODE PREPARED / AWS UNVERIFIED',15,ORANGE,True)
    stroke(d,[(36,147),(565,147)],(172,187,185),2)
    sections=[(1,177,'How does HTTP reach EC2?',[("Browser","HTTP"),("Public IP","internet"),("SG: TCP 80","filter"),("EC2 + Nginx","response")], 'Check: HTTP response + EC2 status.'),
      (2,667,'What makes a subnet public?',[("Internet GW","attached"),("Route table","0.0.0.0/0"),("Public subnet","10.42.1.0/24"),("EC2 + SG","public IP")],'Check: route, IP, SG, then HTTP.'),
      (3,1157,'If HTTP times out?',[("EC2 status","healthy?"),("Route + SG","open path?"),("Nginx logs","service?"),("CloudWatch","metrics")],'CPU alone cannot prove reachability.')]
    for n,y,title,items,note in sections:
        circled(d,64,y+23,n);txt(d,(99,y),title,29)
        start=y+67
        for k,(a,b) in enumerate(items):
            yy=start+k*88
            node(d,91,yy,418,a,b,ORANGE if k==3 else CYAN)
            if k<3:arrow(d,[(300,yy+74),(300,yy+88)])
        txt(d,(43,y+431),note,22,CYAN)
        if n<3:stroke(d,[(38,y+465),(562,y+465)],(172,187,185),2)
    return im

if __name__=='__main__':
    for name,make in [('whiteboard.png',desktop),('whiteboard-mobile.png',mobile)]:
        im=make();im.save(OUT/name,optimize=True);print(name,im.size,(OUT/name).stat().st_size)
