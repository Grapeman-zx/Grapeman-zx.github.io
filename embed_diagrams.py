#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Embed generated quaternion diagrams into the Evernote HTML as base64."""

import base64
import os
import re

HTML_PATH = r"C:\Users\zjm\Documents\个人网页\quaternion_evernote.html"
DIAGRAM_DIR = r"C:\Users\zjm\Documents\个人网页\assets\quaternion-diagrams"


def b64_img(name):
    path = os.path.join(DIAGRAM_DIR, name)
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("ascii")
    return f'<img src="data:image/png;base64,{data}" style="display:block;margin:18px auto;max-width:100%;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,0.15);" alt="{name}">'


with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

replacements = [
    # 1. forward axis
    ("""        前 Z
        ↑
        |
        ● ——→ X""", b64_img("forward_axis.png")),

    # 2. quaternion space vertical + double cover mapping (two adjacent pre blocks)
    ("""      q ●
        |
        |
        O
        |
        |
     ● -q""", ""),  # handled together below

    ("""q  ────┐
       ├──→ 同一个旋转
-q ────┘""", b64_img("double_cover.png")),

    # 3. sphere A/B/-B
    ("""        A ●
       /   \\
      /     \\
     /       \\
    ●---------●
   -B         B""", b64_img("slerp_sphere.png")),

    # 4. A near -B vs B
    ("""A ●───● -B


                 ● B""", ""),  # remove after replacing sphere block

    # 5. Slerp arc A->B
    ("""           A ●
          /   .
         /     .
        /       .
       O         ● B""", ""),  # remove; covered by sphere image

    # 6. Lerp line + Slerp arc (two pre blocks)
    ("""A ●────────● B""", b64_img("lerp_vs_slerp.png")),

    ("""A ●
    .
      .
        .
          ● B""", ""),  # remove after replacing lerp line
]

# Remove the quaternion space vertical block first, then its mapping becomes the image
html = html.replace("""      q ●
        |
        |
        O
        |
        |
     ● -q""", "")

for old, new in replacements:
    if old:
        html = html.replace(old, new)

# Remove any empty <pre>...</pre> blocks that may remain
html = re.sub(r"<pre[^>]*>\s*</pre>", "", html)
# Remove whitespace-only pre blocks
html = re.sub(r"<pre[^>]*>\s*</pre>", "", html)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Diagrams embedded into quaternion_evernote.html")
