#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild blog.html into a three-column docs-style layout."""
import re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(r"C:\Users\zjm\Documents\个人网页")
SRC = ROOT / "blog.html"

html = SRC.read_text(encoding="utf-8")
soup = BeautifulSoup(html, "html.parser")

# ---------- Append new CSS ----------
new_css = """
      /* ===== Three-column blog layout ===== */
      .blog-feed--source { display: none; }

      .blog-layout {
        display: grid;
        grid-template-columns: 260px minmax(0, 1fr) 220px;
        gap: 32px;
        max-width: 1400px;
        margin: 0 auto;
        padding: 28px var(--section-x) 80px;
        align-items: start;
      }

      .blog-sidebar,
      .blog-toc {
        position: sticky;
        top: 86px;
        max-height: calc(100vh - 100px);
        overflow-y: auto;
        scrollbar-width: thin;
        scrollbar-color: rgba(255, 255, 255, 0.15) transparent;
      }
      .blog-sidebar::-webkit-scrollbar,
      .blog-toc::-webkit-scrollbar { width: 5px; }
      .blog-sidebar::-webkit-scrollbar-thumb,
      .blog-toc::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.15); border-radius: 4px; }

      .blog-sidebar { padding-right: 8px; }
      .blog-toc { padding-left: 8px; }

      .sidebar-header {
        font-size: 12px; letter-spacing: 0.12em; color: var(--muted);
        text-transform: uppercase; margin-bottom: 16px; padding: 0 8px;
      }

      .sidebar-group { margin-bottom: 6px; }
      .sidebar-group-toggle {
        width: 100%; display: flex; align-items: center; justify-content: space-between;
        padding: 8px 10px; border-radius: 8px; border: none; background: transparent;
        color: #d0d0d0; font-size: 13.5px; font-weight: 500; cursor: pointer;
        transition: background 0.2s ease, color 0.2s ease;
      }
      .sidebar-group-toggle:hover { background: rgba(255, 255, 255, 0.05); color: #fff; }
      .sidebar-group-toggle svg { width: 14px; height: 14px; transition: transform 0.2s ease; opacity: 0.6; }
      .sidebar-group.expanded .sidebar-group-toggle svg { transform: rotate(90deg); }

      .sidebar-items { display: none; padding-left: 8px; margin: 2px 0 8px; }
      .sidebar-group.expanded .sidebar-items { display: block; }

      .sidebar-item {
        display: block; width: 100%; text-align: left;
        padding: 7px 10px 7px 14px; border-radius: 7px; border: none; background: transparent;
        color: #a0a0a0; font-size: 13px; line-height: 1.4; cursor: pointer;
        transition: background 0.2s ease, color 0.2s ease;
      }
      .sidebar-item:hover { background: rgba(255, 255, 255, 0.05); color: #e0e0e0; }
      .sidebar-item.active { background: rgba(138, 180, 255, 0.12); color: #fff; }

      .blog-content {
        min-width: 0;
        padding: 0 8px;
      }

      .blog-article { animation: fade-in 0.35s ease; }
      @keyframes fade-in { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: none; } }

      .blog-content .post-tag { margin-bottom: 14px; }
      .blog-content .post-title { font-size: clamp(28px, 4.2vw, 40px); line-height: 1.12; }
      .blog-content .post-meta { margin-top: 12px; }
      .blog-content .post-excerpt { margin-top: 14px; font-size: 15.5px; line-height: 1.72; color: #bfbfbf; }
      .blog-content .post-divider { display: block; margin: 22px 0 4px; border: 0; border-top: 1px dashed var(--border-soft); }
      .blog-content .post-body { display: block; margin-top: 28px; }
      .blog-content .post-foot { display: flex; }

      .toc-title {
        font-size: 12px; letter-spacing: 0.08em; color: var(--muted);
        text-transform: uppercase; margin-bottom: 14px; padding: 0 4px;
      }
      .toc-nav { display: flex; flex-direction: column; gap: 4px; }
      .toc-link {
        display: block; padding: 5px 8px; border-radius: 6px;
        color: #9a9a9a; font-size: 12.5px; line-height: 1.45;
        transition: background 0.2s ease, color 0.2s ease;
      }
      .toc-link:hover { background: rgba(255, 255, 255, 0.05); color: #e0e0e0; }
      .toc-link.active { color: #8ab4ff; background: rgba(138, 180, 255, 0.1); }
      .toc-link.h3 { padding-left: 18px; font-size: 12px; color: #888; }
      .toc-link.h3.active { color: #8ab4ff; }

      @media (max-width: 1100px) {
        .blog-layout { grid-template-columns: 220px minmax(0, 1fr) 180px; gap: 20px; }
      }
      @media (max-width: 900px) {
        .blog-layout { grid-template-columns: 1fr; padding-top: 18px; }
        .blog-sidebar, .blog-toc { display: none; }
      }
"""
style_tag = soup.find("style")
if style_tag:
    style_tag.string = (style_tag.string or "") + new_css

# ---------- Replace main content ----------
main = soup.find("main", {"id": "top"})
if main:
    feed = main.find("section", {"id": "feed"})
    if feed:
        feed["class"] = (feed.get("class", []) if isinstance(feed.get("class"), list) else feed.get("class", "").split()) + ["blog-feed--source"]
        feed["aria-hidden"] = "true"
    main.clear()

    layout = BeautifulSoup("""
      <div class="blog-layout">
        <aside class="blog-sidebar">
          <div class="sidebar-header">笔记分类</div>
          <nav class="sidebar-nav" id="sidebarNav"></nav>
        </aside>
        <article class="blog-content" id="blogContent"></article>
        <aside class="blog-toc">
          <div class="toc-title">On this page</div>
          <nav class="toc-nav" id="tocNav"></nav>
        </aside>
      </div>
    """, "html.parser")

    if feed:
        main.append(feed)
    main.append(layout)

# ---------- Remove article-view overlay (no longer needed) ----------
article_view = soup.find("div", {"id": "articleView"})
if article_view:
    article_view.decompose()

# ---------- Replace script content ----------
new_script = """(function () {
        var appears = document.querySelectorAll(".appear");
        appears.forEach(function (node) {
          node.addEventListener("animationend", function () { node.classList.add("is-in"); }, { once: true });
        });
        requestAnimationFrame(function () {
          requestAnimationFrame(function () {
            appears.forEach(function (node) {
              var anims = node.getAnimations ? node.getAnimations() : [];
              var running = anims.some(function (a) { return a.playState === "running"; });
              var finished = anims.some(function (a) { return a.playState === "finished"; });
              if (!running && !finished) node.classList.add("is-in");
            });
          });
        });

        var reveals = document.querySelectorAll(".reveal");
        if ("IntersectionObserver" in window) {
          var io = new IntersectionObserver(function (entries) {
            entries.forEach(function (e) {
              if (e.isIntersecting) { e.target.classList.add("is-visible"); io.unobserve(e.target); }
            });
          }, { threshold: 0.1, rootMargin: "0px 0px -6% 0px" });
          reveals.forEach(function (r) { io.observe(r); });
        } else {
          reveals.forEach(function (r) { r.classList.add("is-visible"); });
        }

        var burger = document.querySelector(".burger");
        var body = document.body;
        var nav = document.getElementById("site-nav");
        function closeMenu() { body.classList.remove("menu-open"); if (burger) { burger.setAttribute("aria-expanded", "false"); burger.setAttribute("aria-label", "打开菜单"); } }
        function openMenu() { body.classList.add("menu-open"); if (burger) { burger.setAttribute("aria-expanded", "true"); burger.setAttribute("aria-label", "关闭菜单"); } }
        if (burger) burger.addEventListener("click", function () { if (body.classList.contains("menu-open")) closeMenu(); else openMenu(); });
        if (nav) nav.querySelectorAll("a").forEach(function (a) { a.addEventListener("click", closeMenu); });
        document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeMenu(); });
        window.addEventListener("resize", function () { if (window.matchMedia("(min-width: 901px)").matches) closeMenu(); });

        // ===== Three-column blog =====
        var feed = document.getElementById("feed");
        var sidebarNav = document.getElementById("sidebarNav");
        var blogContent = document.getElementById("blogContent");
        var tocNav = document.getElementById("tocNav");
        var cards = feed ? Array.from(feed.querySelectorAll(".post-card[data-post]")) : [];
        var activePostId = null;
        var tocObserver = null;

        var catLabels = {
          ui: "UI 与 Slate",
          render: "渲染",
          engine: "引擎",
          cpp: "C++",
          math: "数学",
          physics: "物理",
          anim: "动画",
          platform: "平台"
        };

        function groupByCat(list) {
          var groups = {};
          list.forEach(function (card) {
            var raw = card.getAttribute("data-cat") || "other";
            var cats = raw.split(",").map(function (s) { return s.trim(); });
            cats.forEach(function (cat) {
              if (!groups[cat]) groups[cat] = [];
              groups[cat].push(card);
            });
          });
          return groups;
        }

        function buildSidebar() {
          if (!sidebarNav) return;
          var groups = groupByCat(cards);
          var order = ["ui", "render", "engine", "cpp", "math", "physics", "anim", "platform"];
          var cats = Object.keys(groups).sort(function (a, b) {
            var ia = order.indexOf(a), ib = order.indexOf(b);
            if (ia === -1) ia = 999; if (ib === -1) ib = 999;
            return ia - ib;
          });
          var svgArrow = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>';

          cats.forEach(function (cat) {
            var group = document.createElement("div");
            group.className = "sidebar-group expanded";
            var toggle = document.createElement("button");
            toggle.className = "sidebar-group-toggle";
            toggle.type = "button";
            toggle.innerHTML = "<span>" + (catLabels[cat] || cat) + "</span>" + svgArrow;
            var items = document.createElement("div");
            items.className = "sidebar-items";

            groups[cat].forEach(function (card) {
              var titleEl = card.querySelector(".post-title");
              var btn = document.createElement("button");
              btn.className = "sidebar-item";
              btn.type = "button";
              btn.textContent = titleEl ? titleEl.textContent : "";
              btn.dataset.post = card.dataset.post;
              btn.addEventListener("click", function () { loadPost(card.dataset.post); });
              items.appendChild(btn);
            });

            toggle.addEventListener("click", function () { group.classList.toggle("expanded"); });
            group.appendChild(toggle);
            group.appendChild(items);
            sidebarNav.appendChild(group);
          });
        }

        function buildToc(body) {
          if (!tocNav) return;
          tocNav.innerHTML = "";
          var headings = body.querySelectorAll("h2, h3");
          headings.forEach(function (h, i) {
            var id = "toc-" + i;
            h.id = id;
            var link = document.createElement("a");
            link.className = "toc-link " + h.tagName.toLowerCase();
            link.href = "#" + id;
            link.textContent = h.textContent;
            link.addEventListener("click", function (e) {
              e.preventDefault();
              h.scrollIntoView({ behavior: "smooth", block: "start" });
              history.replaceState(null, null, "#" + id);
            });
            tocNav.appendChild(link);
          });
        }

        function updateSidebarActive(id) {
          if (!sidebarNav) return;
          sidebarNav.querySelectorAll(".sidebar-item").forEach(function (btn) {
            btn.classList.toggle("active", btn.dataset.post === id);
          });
        }

        function observeToc(body) {
          if (tocObserver) tocObserver.disconnect();
          var headings = body.querySelectorAll("h2, h3");
          if (!headings.length || !window.IntersectionObserver) return;
          tocObserver = new IntersectionObserver(function (entries) {
            var visible = entries.filter(function (e) { return e.isIntersecting; }).map(function (e) { return e.target.id; });
            if (!visible.length) return;
            tocNav.querySelectorAll(".toc-link").forEach(function (link) {
              link.classList.toggle("active", visible[0] && link.getAttribute("href") === "#" + visible[0]);
            });
          }, { rootMargin: "-80px 0px -60% 0px", threshold: 0 });
          headings.forEach(function (h) { tocObserver.observe(h); });
        }

        function loadPost(id) {
          var card = cards.find(function (c) { return c.dataset.post === id; });
          if (!card || !blogContent) return;
          activePostId = id;

          blogContent.innerHTML = "";
          var article = document.createElement("article");
          article.className = "blog-article";

          ["post-tag", "post-title", "post-meta", "post-excerpt", "post-divider", "post-body", "post-foot"].forEach(function (cls) {
            var el = card.querySelector("." + cls);
            if (el) article.appendChild(el.cloneNode(true));
          });

          blogContent.appendChild(article);
          updateSidebarActive(id);

          var body = article.querySelector(".post-body");
          if (body) {
            buildToc(body);
            observeToc(body);
          }
          window.scrollTo({ top: 0, behavior: "smooth" });
        }

        buildSidebar();
        if (cards.length) loadPost(cards[0].dataset.post);

        // Email modal
        var emailBtn = document.getElementById("emailBtn");
        var modal = document.getElementById("emailModal");
        var modalEmail = document.getElementById("modalEmail");
        var copyBtn = document.getElementById("copyEmail");
        function openModal() {
          var raw = emailBtn.getAttribute("data-email") || "";
          modalEmail.textContent = raw.replace(/#/g, "@");
          modal.classList.add("open"); modal.setAttribute("aria-hidden", "false");
        }
        function closeModal() { modal.classList.remove("open"); modal.setAttribute("aria-hidden", "true"); }
        if (emailBtn) emailBtn.addEventListener("click", openModal);
        modal.querySelectorAll("[data-close]").forEach(function (el) { el.addEventListener("click", closeModal); });
        document.addEventListener("keydown", function (e) { if (e.key === "Escape" && modal.classList.contains("open")) closeModal(); });
        if (copyBtn) {
          copyBtn.addEventListener("click", function () {
            var text = modalEmail.textContent;
            var done = function () { copyBtn.textContent = "已复制 ✓"; setTimeout(function () { copyBtn.textContent = "复制邮箱"; }, 1500); };
            if (navigator.clipboard && navigator.clipboard.writeText) { navigator.clipboard.writeText(text).then(done, done); }
            else { var ta = document.createElement("textarea"); ta.value = text; document.body.appendChild(ta); ta.select(); try { document.execCommand("copy"); } catch (e) {} document.body.removeChild(ta); done(); }
          });
        }
      })();"""

script_tag = soup.find("script")
if script_tag:
    script_tag.string = new_script

# ---------- Save ----------
SRC.write_text(str(soup), encoding="utf-8")
print("Rebuilt", SRC)
