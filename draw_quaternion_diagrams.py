#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate clean PNG diagrams for the quaternion article."""

from PIL import Image, ImageDraw, ImageFont
import os

OUT_DIR = r"C:\Users\zjm\Documents\个人网页\assets\quaternion-diagrams"
os.makedirs(OUT_DIR, exist_ok=True)

BG = "#1e1e1e"
FG = "#e8e8e8"
ACCENT = "#8ab4ff"
GREEN = "#7ee787"
RED = "#ff7b72"
GRAY = "#6e7681"


def get_font(size=24):
    candidates = [
        r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\msyhbd.ttc",
        r"C:\Windows\Fonts\simhei.ttf",
        r"C:\Windows\Fonts\simsun.ttc",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def draw_text_centered(draw, pos, text, font, fill=FG):
    bbox = draw.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((pos[0] - w / 2, pos[1] - h / 2), text, font=font, fill=fill)


def draw_text_left(draw, pos, text, font, fill=FG):
    bbox = draw.textbbox((0, 0), text, font=font)
    h = bbox[3] - bbox[1]
    draw.text((pos[0], pos[1] - h / 2), text, font=font, fill=fill)


def double_cover():
    W, H = 700, 500
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    font = get_font(26)
    small = get_font(22)

    cx, top, bot = 220, 90, 410
    mid = (top + bot) // 2
    r = 8

    # vertical dotted axis
    for y in range(top, bot + 1, 10):
        draw.line([(cx, y), (cx, min(y + 5, bot))], fill=FG, width=2)

    # dots
    draw.ellipse([(cx - r, top - r), (cx + r, top + r)], fill=FG)
    draw.ellipse([(cx - r, bot - r), (cx + r, bot + r)], fill=FG)
    draw.ellipse([(cx - 6, mid - 6), (cx + 6, mid + 6)], outline=FG, width=2)

    # labels
    draw_text_left(draw, (cx + 18, top), "q", font)
    draw_text_left(draw, (cx + 18, bot), "-q", font)
    draw_text_left(draw, (cx + 18, mid), "O", font)

    # mapping to same rotation
    right_x = 560
    draw.line([(cx, top), (right_x, mid)], fill=FG, width=2)
    draw.line([(cx, bot), (right_x, mid)], fill=FG, width=2)
    # arrow
    draw.polygon([(right_x, mid), (right_x - 12, mid - 7), (right_x - 12, mid + 7)], fill=FG)
    draw_text_left(draw, (right_x + 18, mid), "同一个旋转", small)

    img.save(os.path.join(OUT_DIR, "double_cover.png"))
    print("saved double_cover.png")


def forward_axis():
    W, H = 600, 520
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    font = get_font(26)
    small = get_font(20)

    ox, oy = 260, 360
    axis_len = 180

    # Z axis arrow (up)
    draw.line([(ox, oy), (ox, oy - axis_len)], fill=FG, width=3)
    draw.polygon([(ox, oy - axis_len), (ox - 9, oy - axis_len + 18), (ox + 9, oy - axis_len + 18)], fill=FG)
    draw_text_left(draw, (ox + 16, oy - axis_len + 10), "前 Z", font)

    # X axis arrow (right)
    draw.line([(ox, oy), (ox + axis_len, oy)], fill=FG, width=3)
    draw.polygon([(ox + axis_len, oy), (ox + axis_len - 18, oy - 9), (ox + axis_len - 18, oy + 9)], fill=FG)
    draw_text_left(draw, (ox + axis_len + 12, oy), "X", font)

    # origin dot / character
    draw.ellipse([(ox - 10, oy - 10), (ox + 10, oy + 10)], fill=ACCENT)
    draw_text_centered(draw, (ox, oy + 32), "角色当前位置", small, fill=GRAY)

    img.save(os.path.join(OUT_DIR, "forward_axis.png"))
    print("saved forward_axis.png")


def slerp_sphere():
    W, H = 800, 520
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    font = get_font(24)
    small = get_font(18)

    cx, cy, R = 280, 260, 170

    # sphere outline
    draw.ellipse([(cx - R, cy - R), (cx + R, cy + R)], outline=GRAY, width=2)

    # points
    import math
    A = (cx + int(R * math.cos(math.radians(160))), cy + int(R * math.sin(math.radians(160))))
    negB = (cx + int(R * math.cos(math.radians(140))), cy + int(R * math.sin(math.radians(140))))
    B = (cx + int(R * math.cos(math.radians(-20))), cy + int(R * math.sin(math.radians(-20))))

    def mark(p, label, fill=FG):
        r = 7
        draw.ellipse([(p[0] - r, p[1] - r), (p[0] + r, p[1] + r)], fill=fill)
        draw_text_left(draw, (p[0] + 14, p[1]), label, font)

    mark(A, "A")
    mark(negB, "-B", fill=GREEN)
    mark(B, "B")

    # long arc A -> B (the wrong way)
    draw.arc([(cx - R, cy - R), (cx + R, cy + R)], start=160, end=340, fill=RED, width=3)
    # short arc A -> -B (correct way)
    draw.arc([(cx - R, cy - R), (cx + R, cy + R)], start=140, end=160, fill=GREEN, width=4)

    # legend
    lx, ly = 520, 160
    draw.line([(lx, ly), (lx + 30, ly)], fill=GREEN, width=4)
    draw_text_left(draw, (lx + 42, ly), "正确短路径", small)
    ly += 36
    draw.line([(lx, ly), (lx + 30, ly)], fill=RED, width=3)
    draw_text_left(draw, (lx + 42, ly), "错误绕远路", small)

    img.save(os.path.join(OUT_DIR, "slerp_sphere.png"))
    print("saved slerp_sphere.png")


def sphere_ab():
    W, H = 640, 520
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    font = get_font(26)
    small = get_font(20)

    cx, cy, R = 320, 260, 170

    # sphere outline
    draw.ellipse([(cx - R, cy - R), (cx + R, cy + R)], outline=GRAY, width=2)
    # subtle equator-ish dashed ellipse to suggest 3D
    for a in range(0, 360, 8):
        import math
        x0 = cx + int(R * math.cos(math.radians(a)))
        y0 = cy + int(R * 0.35 * math.sin(math.radians(a)))
        x1 = cx + int(R * math.cos(math.radians(a + 3)))
        y1 = cy + int(R * 0.35 * math.sin(math.radians(a + 3)))
        draw.line([(x0, y0), (x1, y1)], fill=GRAY, width=1)

    import math
    A = (cx + int(R * math.cos(math.radians(150))), cy + int(R * math.sin(math.radians(150))))
    B = (cx + int(R * math.cos(math.radians(30))), cy + int(R * math.sin(math.radians(30))))

    def mark(p, label, fill=FG):
        r = 8
        draw.ellipse([(p[0] - r, p[1] - r), (p[0] + r, p[1] + r)], fill=fill)
        draw_text_left(draw, (p[0] + 14, p[1]), label, font)

    mark(A, "A")
    mark(B, "B")

    draw_text_centered(draw, (cx, cy + R + 36), "球面上的两个 Quaternion", small)

    img.save(os.path.join(OUT_DIR, "sphere_ab.png"))
    print("saved sphere_ab.png")


def lerp_vs_slerp():
    W, H = 900, 420
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    font = get_font(26)
    small = get_font(20)

    R = 130

    def panel(px, py, title, use_arc):
        # circle
        draw.ellipse([(px - R, py - R), (px + R, py + R)], outline=GRAY, width=2)
        # points A and B
        A = (px - R + 20, py - 20)
        B = (px + R - 20, py + 20)
        for p, label in [(A, "A"), (B, "B")]:
            r = 7
            draw.ellipse([(p[0] - r, p[1] - r), (p[0] + r, p[1] + r)], fill=FG)
            draw_text_left(draw, (p[0] + 12, p[1]), label, font)

        if use_arc:
            # arc along the circle
            draw.arc([(px - R, py - R), (px + R, py + R)], start=140, end=380, fill=ACCENT, width=4)
        else:
            # straight chord
            draw.line([A, B], fill=ACCENT, width=4)

        draw_text_centered(draw, (px, py + R + 36), title, small)

    panel(220, 180, "Lerp：直接穿球内部", use_arc=False)
    panel(680, 180, "Slerp：沿球面圆弧", use_arc=True)

    img.save(os.path.join(OUT_DIR, "lerp_vs_slerp.png"))
    print("saved lerp_vs_slerp.png")


if __name__ == "__main__":
    double_cover()
    forward_axis()
    sphere_ab()
    slerp_sphere()
    lerp_vs_slerp()
    print("done")
