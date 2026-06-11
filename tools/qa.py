#!/usr/bin/env python3
"""Auditoría del sitio contra el checklist §12 de la especificación.

Recorre todos los index.html, parsea metadatos, JSON-LD y enlaces internos.
Imprime un informe agrupado con OK / WARN / ERROR.
"""
from __future__ import annotations

import glob
import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).parent.parent
HTMLS = sorted(glob.glob(str(ROOT / "**" / "*.html"), recursive=True))
HTMLS = [h for h in HTMLS if "/tools/" not in h]

KEYWORD = "Limpieza Despues de Incendio"
DOMAIN = "https://limpiezadeincendiosalpha.es"
BASE_PATH = ""

errors, warnings, oks = [], [], []
def err(msg): errors.append(msg)
def warn(msg): warnings.append(msg)
def ok(msg): oks.append(msg)

# --- Indexar contenido ---------------------------------------------------
pages = []
for fp in HTMLS:
    rel = fp.replace(str(ROOT), "")
    html = Path(fp).read_text(encoding="utf-8")
    m_title = re.search(r"<title>(.*?)</title>", html, re.S)
    m_desc = re.search(r'name="description"\s+content="(.*?)"', html, re.S)
    m_canon = re.search(r'rel="canonical"\s+href="(.*?)"', html)
    h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    h2s = re.findall(r"<h2[^>]*>(.*?)</h2>", html, re.S)
    imgs = re.findall(r"<img\b([^>]*)>", html)
    hrefs = re.findall(r'href="([^"]+)"', html)
    jsonlds = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    intro_m = re.search(r'<p class="lead">(.*?)</p>', html, re.S)
    pages.append({
        "path": rel, "html": html,
        "title": (m_title.group(1) if m_title else "").strip(),
        "desc": (m_desc.group(1) if m_desc else "").strip(),
        "canon": m_canon.group(1) if m_canon else "",
        "h1": [re.sub(r"<.*?>", "", x).strip() for x in h1s],
        "h2": [re.sub(r"<.*?>", "", x).strip() for x in h2s],
        "imgs": imgs,
        "hrefs": hrefs,
        "jsonlds": jsonlds,
        "intro": re.sub(r"<.*?>", "", intro_m.group(1)).strip() if intro_m else "",
    })

print(f"Auditando {len(pages)} páginas HTML…\n")

# --- 1. Titles y descriptions únicos -------------------------------------
titles = Counter(p["title"] for p in pages)
descs = Counter(p["desc"] for p in pages)
dup_t = [t for t, c in titles.items() if c > 1]
dup_d = [d for d, c in descs.items() if c > 1]
if dup_t: err(f"Títulos duplicados: {len(dup_t)} ({dup_t[:2]})")
else: ok("Todos los <title> son únicos")
if dup_d: err(f"Descripciones duplicadas: {len(dup_d)} ({dup_d[:2]})")
else: ok("Todas las meta descriptions son únicas")

# --- 2. H1 único por página ----------------------------------------------
multi_h1 = [p["path"] for p in pages if len(p["h1"]) != 1]
if multi_h1: warn(f"Páginas con !=1 <h1>: {len(multi_h1)} (ej. {multi_h1[:3]})")
else: ok("Cada página tiene exactamente 1 H1")

# --- 3. Keyword en H1+title+intro de home y landing madre ---------------
def check_keyword(p, label):
    kw = KEYWORD.lower()
    if kw not in p["title"].lower():
        err(f"[{label}] keyword no está en <title>: {p['path']}")
    elif kw not in " ".join(p["h1"]).lower():
        err(f"[{label}] keyword no está en H1: {p['path']}")
    else:
        ok(f"[{label}] keyword en H1+title")

home = next((p for p in pages if p["path"] == "/index.html"), None)
madre = next((p for p in pages
              if p["path"] == "/servicios/limpieza-tras-incendio/index.html"), None)
if home: check_keyword(home, "HOME")
if madre: check_keyword(madre, "LANDING-MADRE")

# --- 4. En landings geo: keyword en title, H1, meta y primeros 100 chars --
geo = [p for p in pages if "/limpieza-despues-de-incendio-" in p["path"]]
fails_intro = []
fails_title = []
for p in geo:
    if KEYWORD.lower() not in p["title"].lower():
        fails_title.append(p["path"])
    if KEYWORD.lower() not in p["intro"][:120].lower():
        fails_intro.append(p["path"])
if fails_title: err(f"Geo sin keyword en title: {len(fails_title)} ({fails_title[:2]})")
else: ok(f"Las {len(geo)} landings geo tienen keyword en <title>")
if fails_intro: err(f"Geo sin keyword en primeros 100 chars del intro: {len(fails_intro)} ({fails_intro[:2]})")
else: ok(f"Las {len(geo)} landings geo tienen keyword en primeros 100 chars")

# --- 5. JSON-LD válido ---------------------------------------------------
ld_bad = []
ld_types = Counter()
for p in pages:
    for j in p["jsonlds"]:
        try:
            data = json.loads(j)
            if isinstance(data, list):
                for d in data:
                    if isinstance(d, dict) and "@type" in d:
                        ld_types[d["@type"]] += 1
            elif isinstance(data, dict) and "@type" in data:
                ld_types[data["@type"]] += 1
        except json.JSONDecodeError as e:
            ld_bad.append((p["path"], str(e)[:60]))
if ld_bad:
    err(f"JSON-LD inválido en {len(ld_bad)} páginas: {ld_bad[:2]}")
else:
    ok(f"Todos los JSON-LD parsean (tipos: {dict(ld_types)})")

# Verificar presencia de schemas obligatorios
def has_schema_type(p, t):
    for j in p["jsonlds"]:
        try:
            data = json.loads(j)
            if isinstance(data, list):
                for d in data:
                    if isinstance(d, dict) and d.get("@type") == t:
                        return True
            elif isinstance(data, dict) and data.get("@type") == t:
                return True
        except: pass
    return False

if home and has_schema_type(home, "Organization"): ok("Home con schema Organization")
else: err("Home sin schema Organization")
if home and has_schema_type(home, "WebSite"): ok("Home con schema WebSite")
else: err("Home sin schema WebSite")
if home and has_schema_type(home, "FAQPage"): ok("Home con schema FAQPage")
else: err("Home sin schema FAQPage")

geo_missing_lb = [p["path"] for p in geo if not has_schema_type(p, "LocalBusiness")]
if geo_missing_lb: err(f"Landings geo sin LocalBusiness: {len(geo_missing_lb)}")
else: ok(f"Las {len(geo)} landings geo con schema LocalBusiness")

geo_missing_bc = [p["path"] for p in geo if not has_schema_type(p, "BreadcrumbList")]
if geo_missing_bc: err(f"Landings geo sin BreadcrumbList: {len(geo_missing_bc)}")
else: ok(f"Las {len(geo)} landings geo con BreadcrumbList")

# --- 6. Canonical absoluto -----------------------------------------------
canon_bad = [p["path"] for p in pages if not p["canon"].startswith("https://")]
if canon_bad: err(f"Canonical no absoluto en {len(canon_bad)} páginas")
else: ok("Todos los canonicals son absolutos (https://…)")

# --- 7. Imágenes con alt -------------------------------------------------
img_no_alt = []
for p in pages:
    for attrs in p["imgs"]:
        if "alt=" not in attrs:
            img_no_alt.append(p["path"])
            break
if img_no_alt: warn(f"Páginas con <img> sin alt: {len(img_no_alt)} (ej. {img_no_alt[:3]})")
else: ok("Todas las imágenes tienen atributo alt")

# Cada landing geo: al menos una foto de contenido (no solo el icono wa.svg)
geo_no_foto = []
geo_alt_sin_kw = []
for p in geo:
    content_imgs = [a for a in p["imgs"] if "wa.svg" not in a]
    if not content_imgs:
        geo_no_foto.append(p["path"])
        continue
    # alt debe contener keyword principal
    ok_alt = False
    for a in content_imgs:
        m = re.search(r'alt="([^"]+)"', a)
        if m and KEYWORD.lower() in m.group(1).lower():
            ok_alt = True
            break
    if not ok_alt:
        geo_alt_sin_kw.append(p["path"])
if geo_no_foto: err(f"Landings geo sin foto de contenido: {len(geo_no_foto)}")
else: ok(f"Las {len(geo)} landings geo tienen al menos una foto de contenido")
if geo_alt_sin_kw: err(f"Landings con foto pero sin alt con keyword: {len(geo_alt_sin_kw)}")
else: ok("Todas las fotos de landings tienen alt con keyword principal")

# --- 8. "Toda España" prohibido ------------------------------------------
malos = []
for p in pages:
    if re.search(r"toda España|en toda España|cobertura nacional", p["html"], re.I):
        malos.append(p["path"])
if malos: err(f'Menciones a "toda España" en {len(malos)} páginas: {malos[:3]}')
else: ok('Sin menciones a "toda España"')

# --- 9. Servicios no ofrecidos -------------------------------------------
prohibidos = [r"\breformamos\b", r"\brestauramos\b",
              r"\breparamos\b", r"\bobra\b.{0,30}\bnueva\b"]
malos2 = []
for p in pages:
    text = re.sub(r"<.*?>", " ", p["html"])
    for pat in prohibidos:
        for m in re.finditer(pat, text, re.I):
            # contexto previo: si lleva "no", "sin" o "tampoco" cerca, es negación válida
            ctx = text[max(0, m.start() - 40):m.start()].lower()
            if re.search(r"\b(no|sin|tampoco|nunca)\b[^.]{0,20}$", ctx):
                continue
            malos2.append((p["path"], pat))
            break
if malos2: warn(f"Posibles menciones a servicios no ofrecidos: {len(malos2)} (ej. {malos2[:3]})")
else: ok("Sin menciones a 'reformamos/restauramos/reparamos'")

# --- 10. Enlaces internos rotos ------------------------------------------
existing = set()
for fp in HTMLS:
    rel = fp.replace(str(ROOT), "")
    existing.add(rel)
    if rel.endswith("/index.html"):
        existing.add(rel[:-len("index.html")])
# añadir robots, sitemap, llms
for f in ["/robots.txt", "/sitemap.xml", "/llms.txt", "/assets/styles.css",
          "/assets/favicon.ico", "/assets/logo.webp", "/assets/hero.jpg",
          "/assets/wa.svg"]:
    if (ROOT / f.lstrip("/")).exists():
        existing.add(f)
# SVGs por landing
for svg in (ROOT / "assets" / "landings").glob("*.svg"):
    existing.add("/assets/landings/" + svg.name)
# Otros assets de /assets/ (fotos, vídeos, audios)
for ext in ("*.webp", "*.jpg", "*.jpeg", "*.png", "*.gif", "*.mp4",
            "*.webm", "*.svg", "*.pdf"):
    for f in (ROOT / "assets").glob(ext):
        existing.add("/assets/" + f.name)

broken = []
for p in pages:
    for href in p["hrefs"]:
        u = urlparse(href)
        if u.scheme or href.startswith(("tel:", "mailto:", "#")):
            continue
        path = u.path
        if not path.startswith("/"):
            continue
        # Quitar el prefijo BASE_PATH para comparar contra la estructura local
        if BASE_PATH and path.startswith(BASE_PATH + "/"):
            path = path[len(BASE_PATH):]
        elif BASE_PATH and path == BASE_PATH:
            path = "/"
        if path in existing or (path + "index.html") in existing:
            continue
        broken.append((p["path"], href))
if broken:
    err(f"Enlaces internos rotos: {len(broken)}")
    for b in broken[:10]:
        print(f"  - {b[0]} → {b[1]}")
else:
    ok("Sin enlaces internos rotos")

# --- 11. Sitemap consistente ---------------------------------------------
sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
sm_urls = set(re.findall(r"<loc>(.*?)</loc>", sitemap))
sm_paths = {u.replace(DOMAIN, "") for u in sm_urls}
real_paths = set()
for p in pages:
    rp = p["path"]
    if rp.endswith("/index.html"):
        real_paths.add(rp[:-len("index.html")])
    elif rp == "/404.html":
        continue
    else:
        real_paths.add(rp)
in_sitemap_not_real = sm_paths - real_paths
real_not_in_sitemap = real_paths - sm_paths
if in_sitemap_not_real: warn(f"En sitemap pero no en disco: {len(in_sitemap_not_real)} {list(in_sitemap_not_real)[:3]}")
if real_not_in_sitemap: warn(f"En disco pero no en sitemap: {len(real_not_in_sitemap)} {list(real_not_in_sitemap)[:3]}")
if not in_sitemap_not_real and not real_not_in_sitemap:
    ok(f"sitemap.xml consistente: {len(sm_urls)} URLs")

# --- 12. robots.txt y llms.txt -------------------------------------------
robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
for bot in ["GPTBot", "ClaudeBot", "PerplexityBot", "Google-Extended"]:
    if bot in robots: ok(f"robots.txt permite {bot}")
    else: err(f"robots.txt sin permiso para {bot}")
if "Sitemap:" in robots: ok("robots.txt apunta al sitemap")
else: err("robots.txt sin referencia al sitemap")

if (ROOT / "llms.txt").exists(): ok("llms.txt presente")
else: err("llms.txt no existe")

if (ROOT / ".htaccess").exists():
    htacc = (ROOT / ".htaccess").read_text(encoding="utf-8")
    for piece in ["DirectoryIndex", "HTTPS", "R=301", "mod_expires", "mod_deflate",
                  "X-Content-Type-Options", "ErrorDocument 404"]:
        if piece in htacc: ok(f".htaccess: {piece}")
        else: err(f".htaccess sin {piece}")

# --- Resumen -------------------------------------------------------------
print("\n" + "=" * 60)
print(f"OK:      {len(oks)}")
print(f"WARN:    {len(warnings)}")
print(f"ERROR:   {len(errors)}")
print("=" * 60)
if warnings:
    print("\nWARNINGS:")
    for w in warnings: print(f"  ⚠ {w}")
if errors:
    print("\nERRORS:")
    for e in errors: print(f"  ✗ {e}")
    sys.exit(1)
print("\n✓ QA OK")
