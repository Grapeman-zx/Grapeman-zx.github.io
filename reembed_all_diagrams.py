#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Re-embed all quaternion diagrams (including sphere_ab) into the HTML."""

import base64
import os
import re

HTML_PATH = r"C:\Users\zjm\Documents\个人网页\quaternion_evernote.html"
DIAGRAM_DIR = r"C:\Users\zjm\Documents\个人网页\assets\quaternion-diagrams"


def b64_for(name):
    with open(os.path.join(DIAGRAM_DIR, name), "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def img_tag(name, alt):
    b64 = b64_for(name)
    return f'<img src="data:image/png;base64,{b64}" style="display:block;margin:18px auto;max-width:100%;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,0.15);" alt="{alt}">'


with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# Replace existing embedded images by matching their alt attribute
name_map = {
    "forward_axis.png": "forward_axis.png",
    "double_cover.png": "double_cover.png",
    "slerp_sphere.png": "slerp_sphere.png",
    "lerp_vs_slerp.png": "lerp_vs_slerp.png",
}

for alt_name, file_name in name_map.items():
    pattern = re.compile(
        rf'<img[^>]*alt="{re.escape(alt_name)}"[^>]*>'
    )
    html = pattern.sub(img_tag(file_name, alt_name), html)

# Replace the placeholder text with the new sphere_ab image
html = html.replace(
    "【图片：球面上 A、B 两点】",
    img_tag("sphere_ab.png", "sphere_ab.png"),
)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("All diagrams re-embedded, including sphere_ab.png")
