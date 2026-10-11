"""Render the profile's self-hosted, gently animated architecture artwork.

Run with Pillow installed. All information is visible in frame one; motion only
traces connections. GIFs work in GitHub profile READMEs without external widgets.
"""
from __future__ import annotations

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).parent
REG = '/usr/share/fonts/liberation-sans-fonts/LiberationSans-Regular.ttf'
BOLD = '/usr/share/fonts/liberation-sans-fonts/LiberationSans-Bold.ttf'
W, H = 1200, 390
FRAMES = 16
BG = (8, 20, 38)
PANEL = (15, 38, 61)
PANEL2 = (18, 47, 72)
BORDER = (51, 100, 127)
CYAN = (99, 219, 231)
ORANGE = (255, 171, 74)
WHITE = (244, 249, 252)
MUTED = (171, 194, 208)


def f(n, bold=False):
    return ImageFont.truetype(BOLD if bold else REG, n)


def background(w=W, h=H):
    im = Image.new('RGB', (w, h), BG)
    px = im.load()
    for y in range(h):
        for x in range(w):
            g = max(0.0, 1 - math.hypot((x-w*.78)/(w*.65), (y-h*.3)/(h*1.4)))
            px[x,y] = (int(8+8*y/h+11*g), int(20+15*y/h+18*g), int(38+22*y/h+19*g))
    d = ImageDraw.Draw(im)
    for x in range(36,w,62): d.line((x,0,x,h),fill=(25,55,76),width=1)
    for y in range(35,h,62): d.line((0,y,w,y),fill=(25,55,76),width=1)
    return im


def txt(d, xy, text, size, color=WHITE, bold=False):
    d.text(xy,text,font=f(size,bold),fill=color)


def box(d, rect, title, detail=None, accent=CYAN, title_size=23):
    d.rounded_rectangle(rect,radius=17,fill=PANEL,outline=BORDER,width=2)
    x0,y0,x1,y1=rect
    d.rounded_rectangle((x0+15,y0+16,x0+20,y1-16),radius=2,fill=accent)
    compact = detail is not None and y1-y0 < 90
    txt(d,(x0+34,y0+(9 if compact else 22)),title,title_size,WHITE,True)
    if detail: txt(d,(x0+34,y0+(39 if compact else 58)),detail,16,MUTED)


def label(d, rect, text, accent=CYAN):
    d.rounded_rectangle(rect,radius=11,fill=(20,48,68),outline=(48,95,116),width=1)
    txt(d,(rect[0]+12,rect[1]+8),text,14,accent,True)


def path(d, points, phase, reverse=False, accent=ORANGE):
    d.line(points,fill=(75,137,160),width=3,joint='curve')
    total=0; segments=[]
    for a,b in zip(points,points[1:]):
        length=math.dist(a,b); segments.append((a,b,length)); total+=length
    pos=((1-phase) if reverse else phase)*total
    for a,b,length in segments:
        if pos<=length:
            t=pos/length if length else 0
            x=a[0]+(b[0]-a[0])*t; y=a[1]+(b[1]-a[1])*t
            d.ellipse((x-5,y-5,x+5,y+5),fill=accent)
            break
        pos-=length


def chrome(d, no, title, subtitle):
    d.rounded_rectangle((19,19,1181,371),radius=21,outline=(56,105,130),width=2)
    label(d,(42,38,146,72),f'AWS / {no:02d}',ORANGE)
    txt(d,(167,40),title,31,WHITE,True)
    txt(d,(43,90),subtitle,17,MUTED)
    d.line((43,126,1157,126),fill=(46,95,118),width=2)


def banner(i):
    im=background(1200,340); d=ImageDraw.Draw(im)
    phase=i/FRAMES
    d.rounded_rectangle((21,21,1179,319),radius=22,outline=(56,105,130),width=2)
    d.rounded_rectangle((44,47,51,290),radius=3,fill=ORANGE)
    txt(d,(77,52),'ASRAR',92,WHITE,True)
    txt(d,(82,161),'ASPIRING AWS CLOUD ENGINEER',29,CYAN,True)
    txt(d,(83,213),'Learning cloud infrastructure, one verified lab at a time.',20,MUTED)
    label(d,(82,264,191,296),'EC2  ·  VPC',CYAN)
    label(d,(204,264,331,296),'TERRAFORM',CYAN)
    label(d,(344,264,482,296),'CLOUDWATCH',CYAN)
    d.rounded_rectangle((712,47,1150,285),radius=19,fill=(12,33,53),outline=(50,101,125),width=2)
    txt(d,(737,65),'CLOUD LAB MAP',17,ORANGE,True)
    # Three clear infrastructure nodes, with moving data pulses.
    box(d,(737,111,853,191),'VPC',title_size=22)
    box(d,(891,111,1007,191),'EC2',title_size=22)
    box(d,(1037,111,1125,191),'CW',title_size=22)
    path(d,[(853,151),(891,151)],phase)
    path(d,[(1007,151),(1037,151)],(phase+.43)%1)
    d.line((794,191,794,225,1082,225,1082,191),fill=(65,128,152),width=2)
    txt(d,(761,244),'network  /  compute  /  observability',17,MUTED)
    return im


def ec2(i):
    im=background(); d=ImageDraw.Draw(im); p=i/FRAMES
    chrome(d,1,'EC2 LINUX WEB SERVER','A browser reaches Nginx on a public Amazon Linux instance.')
    box(d,(42,166,230,273),'BROWSER','HTTP request')
    box(d,(330,166,535,273),'SECURITY GROUP','Inbound TCP 80',CYAN,18)
    box(d,(637,166,858,273),'EC2 INSTANCE','Amazon Linux 2023',ORANGE)
    box(d,(960,166,1158,273),'NGINX','Serves web page')
    path(d,[(230,219),(330,219)],p)
    path(d,[(535,219),(637,219)],(p+.33)%1)
    path(d,[(858,219),(960,219)],(p+.66)%1)
    label(d,(43,307,269,340),'SSH CLOSED BY DEFAULT')
    label(d,(283,307,489,340),'ENCRYPTED EBS')
    label(d,(503,307,643,340),'IMDSV2')
    txt(d,(753,314),'Verify: HTTP response + EC2 status checks',16,MUTED)
    return im


def vpc(i):
    im=background(); d=ImageDraw.Draw(im); p=i/FRAMES
    chrome(d,2,'TERRAFORM VPC + EC2','A defined route and security group connect the public subnet to the web server.')
    box(d,(43,186,199,283),'INTERNET','Browser',ORANGE,20)
    d.rounded_rectangle((274,151,1158,300),radius=19,fill=(12,34,56),outline=(60,111,136),width=2)
    label(d,(294,166,493,197),'VPC  10.42.0.0/16')
    box(d,(319,210,488,283),'GATEWAY',None,CYAN,20)
    d.rounded_rectangle((535,166,1135,285),radius=15,outline=(77,139,158),width=2)
    txt(d,(554,174),'PUBLIC SUBNET  10.42.1.0/24',16,CYAN,True)
    box(d,(555,211,735,273),'ROUTE TABLE',None,CYAN,18)
    box(d,(779,211,946,273),'SECURITY GROUP',None,CYAN,16)
    box(d,(987,211,1114,273),'EC2',None,ORANGE,21)
    path(d,[(199,235),(319,235)],p)
    path(d,[(488,245),(555,245)],(p+.25)%1)
    path(d,[(735,245),(779,245)],(p+.5)%1)
    path(d,[(946,245),(987,245)],(p+.75)%1)
    label(d,(43,318,294,350),'0.0.0.0/0  →  GATEWAY')
    txt(d,(684,322),'Verify: route + public IP + HTTP response',16,MUTED)
    return im


def watch(i):
    im=background(); d=ImageDraw.Draw(im); p=i/FRAMES
    chrome(d,3,'CLOUDWATCH TROUBLESHOOTING','Observe EC2 metrics, then diagnose a controlled HTTP outage.')
    box(d,(43,171,252,273),'EC2 INSTANCE','CPU + status checks',ORANGE)
    box(d,(360,171,606,273),'CLOUDWATCH','Built-in EC2 metrics')
    box(d,(732,151,1138,218),'DASHBOARD','CPU and status-check charts',CYAN,20)
    box(d,(732,238,1138,305),'CPU ALARM','>70% for two 5-minute periods',ORANGE,20)
    path(d,[(252,222),(360,222)],p)
    path(d,[(606,222),(670,222),(670,184),(732,184)],(p+.36)%1)
    path(d,[(606,222),(670,222),(670,271),(732,271)],(p+.68)%1)
    label(d,(43,312,330,346),'ALARM ACTIONS DISABLED')
    txt(d,(403,318),'Exercise: remove HTTP rule → diagnose → restore',17,MUTED)
    return im


def save(name, make):
    frames=[make(i).quantize(colors=80,method=Image.Quantize.FASTOCTREE) for i in range(FRAMES)]
    dest=OUT/name
    frames[0].save(dest,save_all=True,append_images=frames[1:],duration=145,loop=0,optimize=True,disposal=2)
    print(name,dest.stat().st_size)


def mobile_banner(i):
    im=background(600,470); d=ImageDraw.Draw(im); phase=i/FRAMES
    d.rounded_rectangle((16,16,584,454),radius=20,outline=(56,105,130),width=2)
    d.rounded_rectangle((35,39,42,219),radius=3,fill=ORANGE)
    txt(d,(62,39),'ASRAR',72,WHITE,True)
    txt(d,(63,136),'ASPIRING AWS',25,CYAN,True)
    txt(d,(63,168),'CLOUD ENGINEER',25,CYAN,True)
    txt(d,(63,213),'Learning one verified lab at a time.',17,MUTED)
    d.rounded_rectangle((35,267,565,419),radius=16,fill=(12,33,53),outline=BORDER,width=2)
    txt(d,(55,282),'CLOUD LAB MAP',16,ORANGE,True)
    box(d,(53,331,190,397),'VPC',title_size=21)
    box(d,(232,331,369,397),'EC2',title_size=21)
    box(d,(411,331,548,397),'METRICS',title_size=18)
    path(d,[(190,364),(232,364)],phase)
    path(d,[(369,364),(411,364)],(phase+.5)%1)
    return im


def mobile_card(i, number):
    im=background(600,690); d=ImageDraw.Draw(im); p=i/FRAMES
    title=['EC2 LINUX WEB SERVER','TERRAFORM VPC + EC2','CLOUDWATCH MONITORING'][number-1]
    subtitle=['Browser to Nginx on Amazon Linux','A routed public subnet and web server','Metrics, alarm, and fault diagnosis'][number-1]
    d.rounded_rectangle((15,15,585,675),radius=20,outline=(56,105,130),width=2)
    label(d,(34,34,138,68),f'AWS / {number:02d}',ORANGE)
    txt(d,(34,86),title,25,WHITE,True)
    txt(d,(35,127),subtitle,17,MUTED)
    d.line((34,161,565,161),fill=(46,95,118),width=2)
    if number==1:
        nodes=[('BROWSER','HTTP request'),('SECURITY GROUP','Inbound TCP 80'),('EC2 INSTANCE','Amazon Linux 2023'),('NGINX','Serves web page')]
        ys=[184,286,388,490]
        for k,((t,detail),y) in enumerate(zip(nodes,ys)):
            box(d,(92,y,508,y+77),t,detail,ORANGE if k==2 else CYAN,21 if k!=1 else 19)
            if k<3:path(d,[(300,y+77),(300,ys[k+1])],(p+k*.29)%1)
        label(d,(34,602,252,635),'SSH CLOSED BY DEFAULT')
        label(d,(269,602,426,635),'ENCRYPTED EBS')
    elif number==2:
        box(d,(92,183,508,260),'INTERNET','Browser',ORANGE)
        d.rounded_rectangle((39,293,561,576),radius=18,fill=(12,34,56),outline=(60,111,136),width=2)
        label(d,(58,307,251,338),'VPC  10.42.0.0/16')
        box(d,(91,354,509,423),'INTERNET GATEWAY',None,CYAN,19)
        d.rounded_rectangle((58,443,542,557),radius=13,outline=(77,139,158),width=2)
        txt(d,(77,452),'PUBLIC SUBNET  10.42.1.0/24',16,CYAN,True)
        box(d,(80,485,279,542),'ROUTE + SG',None,CYAN,18)
        box(d,(325,485,520,542),'EC2',None,ORANGE,20)
        path(d,[(300,260),(300,354)],p)
        path(d,[(300,423),(300,514),(325,514)],(p+.4)%1)
        label(d,(35,605,304,638),'0.0.0.0/0  →  GATEWAY')
    else:
        box(d,(92,184,508,266),'EC2 INSTANCE','CPU and status checks',ORANGE)
        box(d,(92,310,508,392),'CLOUDWATCH','Built-in EC2 metrics')
        path(d,[(300,266),(300,310)],p)
        box(d,(43,463,284,548),'DASHBOARD','Metric charts',CYAN,18)
        box(d,(316,463,557,548),'CPU ALARM','Actions disabled',ORANGE,18)
        path(d,[(300,392),(300,427),(162,427),(162,463)],(p+.3)%1)
        path(d,[(300,392),(300,427),(436,427),(436,463)],(p+.65)%1)
        label(d,(34,603,306,636),'HTTP FAULT EXERCISE')
    return im


if __name__=='__main__':
    for name,make in [('banner.gif',banner),('project-1.gif',ec2),('project-2.gif',vpc),('project-3.gif',watch),('banner-mobile.gif',mobile_banner)]: save(name,make)
    for number in (1,2,3): save(f'project-{number}-mobile.gif',lambda i,n=number: mobile_card(i,n))
