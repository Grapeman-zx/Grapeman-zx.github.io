# -*- coding: utf-8 -*-
"""
为首页卡片生成真正的缩略图（16:10，居中裁剪，800x500，JPEG q82）。
首页原来直接引用正文里的原图，导致首屏要下载 3.16 MB（其中一张 1.7MB 的动图）。
用法：python make_thumbs.py
"""
import json
import os
import sys
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(ROOT, "assets", "thumbs")
W, H = 800, 500           # 16:10
TARGET_AR = W / H
BG = (17, 17, 17)         # 与 .home-card-thumb 背景 #111 一致

# (原始封面, 输出名) —— 与 blog.html 中 12 篇 post-card 一一对应
COVERS = [
    ("assets/blog/font_image1.png",       "font_image1.jpg"),
    ("assets/blog/umg_image1.png",        "umg_image1.jpg"),
    ("assets/blog/listitem_image1.png",   "listitem_image1.jpg"),
    ("assets/blog/tbwrap_image1.gif",     "tbwrap_image1.jpg"),
    ("assets/blog/adjustfont_image1.png", "adjustfont_image1.jpg"),
    ("assets/blog/xcode_image1.png",      "xcode_image1.jpg"),
    ("assets/blog/thumb_image1.png",      "thumb_image1.jpg"),
    ("assets/blog/rdg_image1.jpeg",      "rdg_image1.jpg"),
    ("assets/blog/iosplist_image1.png",   "iosplist_image1.jpg"),
    ("assets/blog/animcalc_image1.png",   "animcalc_image1.jpg"),
    ("assets/blog/cpp_image1.png",        "cpp_image1.jpg"),
    # #12 在 blog.html 里显式写了 data-thumb，以它为准（不是正文首图 forward_axis.png）
    ("assets/quaternion-diagrams/sphere_ab.png", "sphere_ab.jpg"),
]


def flatten(img):
    """带 alpha 的图合成到深色背景上，避免 JPEG 转出黑块/白块。"""
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGBA")
        canvas = Image.new("RGBA", img.size, BG + (255,))
        canvas.alpha_composite(img)
        return canvas.convert("RGB")
    return img.convert("RGB")


def crop_to_ar(img, ar):
    """居中裁剪到目标宽高比。"""
    w, h = img.size
    cur = w / h
    if abs(cur - ar) < 0.01:
        return img
    if cur > ar:            # 太宽 -> 裁左右
        nw = int(round(h * ar))
        left = (w - nw) // 2
        return img.crop((left, 0, left + nw, h))
    else:                   # 太高 -> 裁上下
        nh = int(round(w / ar))
        top = (h - nh) // 2
        return img.crop((0, top, w, top + nh))


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    total_before = 0
    total_after = 0
    rows = []
    manifest = []

    for src_rel, out_name in COVERS:
        src = os.path.join(ROOT, src_rel.replace("/", os.sep))
        dst = os.path.join(OUT_DIR, out_name)
        if not os.path.exists(src):
            print("  [缺失] %s" % src_rel)
            rows.append((out_name, "-", "-", "MISSING"))
            continue

        before = os.path.getsize(src)
        im = Image.open(src)
        im.load()                      # 强制读取，GIF 只取第一帧
        im = flatten(im)
        im = crop_to_ar(im, TARGET_AR)
        im = im.resize((W, H), Image.LANCZOS)
        im.save(dst, "JPEG", quality=82, optimize=True, progressive=True)

        after = os.path.getsize(dst)

        # 原图已经很小的时候，放大成 800x500 反而更占地方 —— 直接沿用原图
        if after >= before:
            os.remove(dst)
            used, after = src_rel, before
            note = "沿用原图"
        else:
            used = "assets/thumbs/" + out_name
            note = ""

        total_before += before
        total_after += after
        rows.append((out_name,
                     "%.0f KB" % (before / 1024),
                     "%.0f KB" % (after / 1024),
                     "-%.0f%%" % ((1 - after / before) * 100) if after < before else "0%",
                     note))
        manifest.append({"src": src_rel, "thumb": used})

    print("")
    for name, b, a, d, note in rows:
        print("  %-24s %10s -> %8s  %8s  %s" % (name, b, a, d, note))
    print("")
    print("原图合计 : %.2f MB" % (total_before / 1048576))
    print("缩略图   : %.2f MB" % (total_after / 1048576))
    print("节省     : %.2f MB (-%.0f%%)" % (
        (total_before - total_after) / 1048576,
        (1 - total_after / total_before) * 100 if total_before else 0))

    with open(os.path.join(ROOT, "thumbs_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print("\n已写出映射: thumbs_manifest.json (%d 条)" % len(manifest))


if __name__ == "__main__":
    main()
