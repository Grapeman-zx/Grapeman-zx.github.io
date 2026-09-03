# -*- coding: utf-8 -*-
"""生成站点专用的 Open Graph 分享图 (1200x630)：首页 + 博客页。

用法： python make_og_image.py
依赖： Pillow
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG = (30, 30, 30)          # #1e1e1e，与站点深色主题一致
BLUE = (138, 180, 255)     # #8ab4ff，站点强调色
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
LINE = (58, 58, 58)

ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ROOT, "assets")


def load_font(size, bold=True):
    """按优先级找可用的中文字体。"""
    candidates = []
    if bold:
        candidates += [
            r"C:\Windows\Fonts\msyhbd.ttc",
            r"C:\Windows\Fonts\simhei.ttf",
        ]
    candidates += [
        r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\simhei.ttf",
        r"C:\Windows\Fonts\simsun.ttc",
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def draw_sphere(d, cx, cy, r):
    """四元数球面示意：圆 + A/B 两点 + 弧线（博客页）。"""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=LINE, width=3)
    d.arc([cx - r, cy - r, cx + r, cy + r], start=200, end=20, fill=BLUE, width=4)
    ax, ay = cx - 62, cy - 52
    bx, by = cx + 64, cy + 48
    d.ellipse([ax - 9, ay - 9, ax + 9, ay + 9], fill=BLUE)
    d.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=BLUE)


def draw_cube(d, cx, cy, s):
    """等距投影线框立方体（首页，呼应游戏 / 3D 渲染）。"""
    k = s * 0.866  # cos(30°)
    top = (cx, cy - s)
    rt = (cx + k, cy - s * 0.5)
    rb = (cx + k, cy + s * 0.5)
    bot = (cx, cy + s)
    lb = (cx - k, cy + s * 0.5)
    lt = (cx - k, cy - s * 0.5)

    # 六边形外轮廓
    d.polygon([top, rt, rb, bot, lb, lt], outline=LINE)
    # 内部三条棱（交于中心）
    for p in (bot, rt, lt):
        d.line([(cx, cy), p], fill=BLUE, width=3)
    # 中心节点
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=BLUE)


def make_card(filename, title, subtitle, desc, deco):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    f_title = load_font(92, bold=True)
    f_sub = load_font(46, bold=True)
    f_desc = load_font(28, bold=False)

    # ---- 左侧文字区 ----
    x = 90
    d.text((x, 190), title, font=f_title, fill=WHITE)
    d.text((x, 310), subtitle, font=f_sub, fill=BLUE)
    d.text((x, 392), desc, font=f_desc, fill=GRAY)

    # 底部装饰线
    d.line([(x, 470), (x + 300, 470)], fill=BLUE, width=4)

    # ---- 右侧装饰 ----
    if deco == "sphere":
        draw_sphere(d, 900, 300, 118)
    else:
        draw_cube(d, 900, 300, 96)

    out = os.path.join(ASSETS, filename)
    os.makedirs(ASSETS, exist_ok=True)
    img.save(out, "JPEG", quality=88, optimize=True)
    print("saved: %s  (%d bytes)" % (out, os.path.getsize(out)))


def main():
    make_card(
        "og-home.jpg",
        "独立游戏开发者",
        "Grapeman_zx",
        "多人联机 · 实时渲染",
        "cube",
    )
    make_card(
        "og-blog.jpg",
        "技术博客",
        "Grapeman_zx",
        "UE · 渲染 · C++ · 图形学 调研笔记",
        "sphere",
    )


if __name__ == "__main__":
    main()
