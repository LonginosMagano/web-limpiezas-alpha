#!/usr/bin/env python3
"""Auditoría de link juice / interlinking interno.

Reporta para cada página del sitio:
- enlaces salientes (cuántas URLs internas únicas enlaza)
- enlaces entrantes (cuántas páginas la enlazan)
- los anchor texts con que se la enlaza

Identifica:
- páginas huérfanas (0 enlaces entrantes)
- páginas sobrelinkeadas (todas las páginas en footer cuentan, descartamos)
- distribución del PageRank por tipo de página
- variedad de anchors por destino
"""
from __future__ import annotations

import glob
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).parent.parent
BASE = "/web-limpiezas-alpha"

# Cargar todas las páginas HTML
HTMLS = sorted(glob.glob(str(ROOT / "**" / "*.html"), recursive=True))
HTMLS = [h for h in HTMLS if "/tools/" not in h]

def norm_path(rel: str) -> str:
    """Convierte ruta de archivo a su URL canónica con prefijo BASE_PATH."""
    if rel.endswith("/index.html"):
        return BASE + rel[: -len("index.html")]
    return BASE + rel

pages: dict[str, dict] = {}
for fp in HTMLS:
    rel = fp.replace(str(ROOT), "")
    url = norm_path(rel)
    html = Path(fp).read_text(encoding="utf-8")
    # Solo enlaces dentro de <main> + sidebar + bloques especiales
    # (descartamos el footer y header que se repiten en TODAS las páginas
    #  y distorsionan el ranking de PageRank interno).
    body_match = re.search(r"<main[^>]*>(.*?)</main>", html, re.S)
    main_html = body_match.group(1) if body_match else html
    # Anchors dentro del <main>: (url, anchor_text)
    out = []
    for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', main_html, re.S):
        href, text = m.group(1), m.group(2)
        text = re.sub(r"<[^>]+>", "", text).strip()
        u = urlparse(href)
        if u.scheme or href.startswith(("#", "tel:", "mailto:")):
            continue
        path = u.path
        # quitar prefijo BASE_PATH para comparar con norm_path()
        if path.startswith(BASE + "/") or path == BASE:
            pass
        elif path.startswith("/"):
            path = BASE + path
        else:
            continue
        out.append((path, text))
    pages[url] = {
        "path": rel,
        "out": out,
    }

# Construir grafo inverso: para cada URL, las páginas que la enlazan
inbound: dict[str, list[tuple[str, str]]] = defaultdict(list)
for src, info in pages.items():
    for dst, text in info["out"]:
        if dst == src:
            continue  # auto-link
        inbound[dst].append((src, text))

def classify(url: str) -> str:
    if url == BASE + "/":
        return "home"
    if "/limpieza-despues-de-incendio-" in url:
        if "-madrid-" in url:
            return "barrio"
        # Las landings van a tener trailing slash
        return "landing"
    if "/blog/" in url:
        return "post" if url != BASE + "/blog/" else "blog-idx"
    if url == BASE + "/servicios/limpieza-tras-incendio/":
        return "servicio"
    if "/ubicaciones/" in url:
        return "ubicaciones"
    if "/galeria/" in url:
        return "galeria"
    if "/testimonios/" in url:
        return "testimonios"
    if "/faq/" in url:
        return "faq"
    if "/404" in url:
        return "404"
    return "other"

print("=" * 72)
print("AUDITORÍA DE LINK JUICE INTERNO")
print("=" * 72)
print()

# 1. Distribución de enlaces entrantes por tipo
inbound_count_by_type: dict[str, list[int]] = defaultdict(list)
for url in pages:
    if url not in pages:
        continue
    t = classify(url)
    inbound_count_by_type[t].append(len(inbound.get(url, [])))

print("DISTRIBUCIÓN: cuántos enlaces entrantes (dentro de <main>) recibe cada tipo de página")
print(f"{'TIPO':12s} {'#PÁG':>6s} {'MIN':>5s} {'AVG':>6s} {'MAX':>5s}")
for t, vals in sorted(inbound_count_by_type.items()):
    if not vals:
        continue
    print(f"{t:12s} {len(vals):6d} {min(vals):5d} {sum(vals)/len(vals):6.1f} {max(vals):5d}")
print()

# 2. Páginas huérfanas (0 entrantes dentro de <main>)
print("HUÉRFANAS (0 enlaces entrantes dentro de <main>):")
huerfanas = [u for u, info in pages.items() if not inbound.get(u)]
if not huerfanas:
    print("  ✓ ninguna")
else:
    for u in sorted(huerfanas):
        print(f"  ⚠ {u}")
print()

# 3. Top 10 más linkeadas
print("TOP 10 PÁGINAS CON MÁS ENLACES ENTRANTES:")
counts = [(len(inbound.get(u, [])), u, classify(u)) for u in pages]
counts.sort(reverse=True)
for c, u, t in counts[:10]:
    print(f"  {c:4d}  [{t:9s}]  {u}")
print()

# 4. Variedad de anchors hacia las landings principales
print("ANCHOR TEXTS hacia las 5 landings principales:")
for ciudad in ["madrid", "barcelona", "valencia", "sevilla", "malaga"]:
    url = f"{BASE}/limpieza-despues-de-incendio-{ciudad}/"
    if url not in pages:
        continue
    anchors = [t for _, t in inbound.get(url, [])]
    counter = Counter(anchors)
    print(f"\n  {url}")
    print(f"  Entrantes: {len(anchors)} · Anchors únicos: {len(counter)}")
    for a, n in counter.most_common(5):
        print(f"    {n:3d}× «{a[:60]}»")
print()

# 5. Cross-link de blog
print("LINK JUICE EN BLOG:")
post_urls = [u for u in pages if classify(u) == "post"]
posts_to_landings = 0
posts_to_other_posts = 0
posts_to_home = 0
for u in post_urls:
    out = pages[u]["out"]
    out_paths = {p for p, _ in out}
    if any(classify(p) == "landing" for p in out_paths):
        posts_to_landings += 1
    if any(classify(p) == "post" and p != u for p in out_paths):
        posts_to_other_posts += 1
    if BASE + "/" in out_paths:
        posts_to_home += 1
print(f"  Posts que enlazan a landing geo:  {posts_to_landings}/{len(post_urls)}")
print(f"  Posts que enlazan a otro post:    {posts_to_other_posts}/{len(post_urls)}")
print(f"  Posts que enlazan a la home:      {posts_to_home}/{len(post_urls)}")
print()

# 6. Cross-link entre landings
print("LINK JUICE ENTRE LANDINGS GEO:")
landing_urls = [u for u in pages if classify(u) in ("landing", "barrio")]
landings_to_landings_avg = 0
landings_to_blog = 0
landings_to_home = 0
landings_to_other_landings = []
for u in landing_urls:
    out_paths = {p for p, _ in pages[u]["out"] if p != u}
    landings_to_other_landings.append(sum(1 for p in out_paths if classify(p) in ("landing", "barrio") and p != u))
    if any(classify(p) == "post" for p in out_paths):
        landings_to_blog += 1
    if BASE + "/" in out_paths:
        landings_to_home += 1
avg = sum(landings_to_other_landings) / len(landings_to_other_landings) if landing_urls else 0
print(f"  Promedio de enlaces a otras landings desde cada landing: {avg:.1f}")
print(f"  Landings que enlazan a algún post del blog: {landings_to_blog}/{len(landing_urls)}")
print(f"  Landings que enlazan a la home: {landings_to_home}/{len(landing_urls)}")
print()

# 7. Páginas con poco link juice salido (riesgo de dead end)
print("PÁGINAS CON MENOS ENLACES SALIENTES (dentro de <main>):")
out_counts = [(len(set(p for p, _ in pages[u]["out"])), u, classify(u)) for u in pages]
out_counts.sort()
for c, u, t in out_counts[:8]:
    print(f"  {c:3d}  [{t:9s}]  {u}")
