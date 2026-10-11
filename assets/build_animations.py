"""Build the self-hosted GIF artwork used by the GitHub profile README.

Requires Pillow. The first frame contains every label, so previews remain readable.
"""
from __future__ import annotations

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).parent
FONT = '/usr/share/fonts/liberation-sans-fonts/LiberationSans-Regular.ttf'
BOLD = '/usr/share/fonts/liberation-sans-fonts/LiberationSans-Bold.ttf'
NAVY = (8, 19, 39)
CYAN = (94, 224, 239)
ORANGE = (255, 166, 65)
WHITE = (244, 250, 255)
MUTED = (174, 203, 220)
FRAMES = 20


def font(size: int, bold: bool = False):
    return ImageFont.truetype(BOLD if bold else FONT, size)


def base(w: int, h: int):
    im = Image.new('RGB', (w, h))
    px = im.load()
    for y in range(h):
        for x in range(w):
            glow = max(0, 1 - math.hypot((x - w * .83) / (w * .5), (y - h * .55) / (h * .95)))
            px[x, y] = (int(8 + 13 * y / h + 11 * glow), int(19 + 29 * y / h + 25 * glow), int(39 + 42 * y / h + 30 * glow))
    d = ImageDraw.Draw(im)
    for x in range(32, w, 56):
        d.line((x, 0, x, h), fill=(28, 61, 87), width=1)
    for y in range(27, h, 56):
        d.line((0, y, w, y), fill=(28, 61, 87), width=1)
    return im


def capsule(d, box, label, color=CYAN):
    d.rounded_rectangle(box, radius=12, fill=(14, 41, 64), outline=(52, 111, 136), width=2)
    d.ellipse((box[0]+14, box[1]+14, box[0]+22, box[1]+22), fill=color)
    d.text((box[0]+30, box[1]+9), label, font=font(17, True), fill=WHITE)


def banner_frame(i):
    im = base(1200, 320)
    d = ImageDraw.Draw(im)
    phase = i / FRAMES
    d.rounded_rectangle((37, 39, 1163, 280), radius=23, outline=(55, 113, 140), width=2)
    d.rounded_rectangle((51, 54, 57, 265), radius=3, fill=ORANGE)
    d.text((83, 55), 'ASRAR', font=font(91, True), fill=WHITE)
    d.text((87, 164), 'ASPIRING AWS CLOUD ENGINEER', font=font(28, True), fill=CYAN)
    d.text((88, 212), 'Linux  /  Networking  /  Terraform  /  Monitoring', font=font(18), fill=MUTED)
    points = [(747, 124), (810, 78), (884, 130), (960, 69), (1057, 115), (1110, 195), (994, 232), (867, 208), (780, 235)]
    edges = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(8,0),(1,7),(2,6),(3,6)]
    for a,b in edges:
        d.line((*points[a],*points[b]), fill=(49, 129, 155), width=2)
        t = (phase * 1.3 + (a+b) * .11) % 1
        x = points[a][0] * (1-t) + points[b][0] * t
        y = points[a][1] * (1-t) + points[b][1] * t
        d.ellipse((x-3,y-3,x+3,y+3), fill=ORANGE if (a+b)%3==0 else CYAN)
    for j,(x,y) in enumerate(points):
        r = 5 + (2 if int((phase * FRAMES + j*2)%FRAMES) < 4 else 0)
        d.ellipse((x-r,y-r,x+r,y+r), fill=ORANGE if j in (1,3,6) else CYAN)
    d.arc((833,119,1090,210), 187, 351, fill=(191,239,248), width=3)
    d.rounded_rectangle((1004, 250, 1131, 266), radius=7, fill=(17, 51, 73), outline=(62,130,149))
    d.text((1015, 249), 'CLOUD LABS', font=font(12, True), fill=ORANGE)
    return im


def card_frame(i, number, title, subtitle, labels):
    im = base(800, 260)
    d = ImageDraw.Draw(im)
    phase = i / FRAMES
    d.rounded_rectangle((18, 18, 782, 242), radius=18, outline=(57, 116, 143), width=2)
    d.text((39, 35), f'AWS LAB {number:02d}', font=font(18, True), fill=ORANGE)
    d.text((39, 68), title, font=font(31, True), fill=WHITE)
    d.text((40, 112), subtitle, font=font(17), fill=MUTED)
    boxes = [(41,170,217,221),(312,170,488,221),(583,170,759,221)]
    for k,box in enumerate(boxes):
        capsule(d, box, labels[k], ORANGE if k == 2 else CYAN)
    for k,(xa,xb) in enumerate([(217,312),(488,583)]):
        d.line((xa,196,xb,196), fill=(75,173,195), width=3)
        d.polygon([(xb-10,190),(xb,196),(xb-10,202)],fill=(75,173,195))
        t=(phase * 1.4 + k*.5)%1
        x=xa+(xb-xa)*t
        d.ellipse((x-5,191,x+5,201), fill=ORANGE)
    return im


def save(frames, path):
    palette = [f.quantize(colors=72, method=Image.Quantize.FASTOCTREE) for f in frames]
    palette[0].save(path, save_all=True, append_images=palette[1:], duration=115,
                    loop=0, optimize=True, disposal=2)
    print(path.name, path.stat().st_size)


if __name__ == '__main__':
    save([banner_frame(i) for i in range(FRAMES)], OUT/'banner.gif')
    specs = [
        ('EC2 LINUX WEB SERVER','A small public web lab with secure defaults',('Browser','TCP 80','EC2 + Nginx')),
        ('TERRAFORM VPC + EC2','Routing and networking built as code',('Internet','VPC route','EC2 + Nginx')),
        ('CLOUDWATCH MONITORING','Metrics, alarm, and a guided fault exercise',('EC2 metrics','CloudWatch','Dashboard')),
    ]
    for n,(title,subtitle,labels) in enumerate(specs,1):
        save([card_frame(i,n,title,subtitle,labels) for i in range(FRAMES)], OUT/f'project-{n}.gif')
