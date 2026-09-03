# -*- coding: utf-8 -*-
"""生成博客页专用的 Open Graph 分享图 (1200x630)。"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG = (30, 30, 30)          # #1e1e1e，与站点深色主题一致
BLUE = (138, 180, 255)     # #8ab4ff，站点强调色
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
LINE = (58, 58, 58)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "og-blog.jpg")


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


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    f_title = load_font(92, bold=True)
    f_sub = load_font(46, bold=True)
    f_desc = load_font(28, bold=False)

    # ---- 左侧文字区 ----
    x = 90
    d.text((x, 190), "技术博客", font=f_title, fill=WHITE)
    d.text((x, 310), "Grapeman_zx", font=f_sub, fill=BLUE)
    d.text((x, 392), "UE · 渲染 · C++ · 图形学 调研笔记", font=f_desc, fill=GRAY)

    # 底部装饰线
    d.line([(x, 470), (x + 300, 470)], fill=BLUE, width=4)

    # ---- 右侧：四元数球面示意（呼应最新笔记）----
    cx, cy, r = 900, 300, 118
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=LINE, width=3)

    # A、B 两点 + 弧线
    ax, ay = cx - 62, cy - 52
    bx, by = cx + 64, cy + 48
    d.arc([cx - r, cy - r, cx + r, cy + r], start=200, end=20, fill=BLUE, width=4)
    d.ellipse([ax - 9, ay - 9, ax + 9, ay + 9], fill=BLUE)
    d.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=BLUE)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, "JPEG", quality=88, optimize=True)
    print("saved:", OUT)
    print("size:", os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
