#!/usr/bin/env python3
"""Generador de la web SEO de Limpiezas de Incendios Alpha.

Produce:
- index.html (home genérica)
- /servicios/limpieza-tras-incendio/ (landing madre del servicio)
- /limpieza-despues-de-incendio-{slug}/ (landings de provincia, municipio y barrio)
- /ubicaciones/
- /404.html
- sitemap.xml, robots.txt, llms.txt, .htaccess
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import unicodedata
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from data import (
    BRAND, DOMAIN, PHONE, PHONE_INTL, EMAIL, KEYWORD, KEYWORD_SLUG,
    KW_VARIANTS_NUCLEO, KW_SECUNDARIAS,
    CCAA, MUNICIPIOS, BARRIOS_MADRID, SLUG_ALIAS, LOCAL_NOTES,
)
from templates import TITLE, META, H1, PARRAFOS, COBERTURA_BLURB, FAQ_LOCAL_POOL

ROOT = Path(__file__).parent.parent
NOW = "2026-05-23"

# ------------------------------------------------------------- helpers --

def slugify(text: str) -> str:
    t = text.lower().strip()
    if t in SLUG_ALIAS:
        return SLUG_ALIAS[t]
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode("ascii")
    t = re.sub(r"['`´’]", "", t)
    t = re.sub(r"[^a-z0-9]+", "-", t)
    return t.strip("-")

def h(seed: str) -> int:
    return int(hashlib.md5(seed.encode("utf-8")).hexdigest(), 16)

def pick(pool: list, seed: str, idx: int = 0) -> str:
    return pool[(h(seed) + idx) % len(pool)]

def kw_variant_for(slug: str) -> str:
    return KW_VARIANTS_NUCLEO[h("var-" + slug) % len(KW_VARIANTS_NUCLEO)]

def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

# Diccionarios de provincia/ccaa para cada municipio y barrio
PROV_OF_MUN: dict[str, str] = {}
for prov, muns in MUNICIPIOS.items():
    for m in muns:
        PROV_OF_MUN[m] = prov

CCAA_OF_PROV: dict[str, tuple[str, str]] = {}
for ccaa_name, ccaa_slug, provs in CCAA:
    for p in provs:
        CCAA_OF_PROV[p] = (ccaa_name, ccaa_slug)

# Inventario de geo-páginas
GeoPage = dict  # {kind, name, slug, url, provincia, ccaa, ccaa_slug, parent}
PAGES: list[GeoPage] = []

for ccaa_name, ccaa_slug, provs in CCAA:
    for provincia in provs:
        pslug = slugify(provincia)
        PAGES.append({
            "kind": "provincia",
            "name": provincia,
            "ciudad": provincia,
            "slug": pslug,
            "url": f"/{KEYWORD_SLUG}-{pslug}/",
            "provincia": provincia,
            "ccaa": ccaa_name,
            "ccaa_slug": ccaa_slug,
            "parent": None,
        })

for prov, muns in MUNICIPIOS.items():
    for m in muns:
        mslug = slugify(m)
        ccaa_name, ccaa_slug = CCAA_OF_PROV[prov]
        PAGES.append({
            "kind": "municipio",
            "name": m,
            "ciudad": m,
            "slug": mslug,
            "url": f"/{KEYWORD_SLUG}-{mslug}/",
            "provincia": prov,
            "ccaa": ccaa_name,
            "ccaa_slug": ccaa_slug,
            "parent": prov,
        })

for b in BARRIOS_MADRID:
    bslug = f"madrid-{slugify(b)}"
    ccaa_name, ccaa_slug = CCAA_OF_PROV["Madrid"]
    PAGES.append({
        "kind": "barrio",
        "name": b,
        "ciudad": f"{b} (Madrid)",
        "slug": bslug,
        "url": f"/{KEYWORD_SLUG}-{bslug}/",
        "provincia": "Madrid",
        "ccaa": ccaa_name,
        "ccaa_slug": ccaa_slug,
        "parent": "Madrid",
    })

PAGE_BY_PROV: dict[str, list[GeoPage]] = {}
for p in PAGES:
    PAGE_BY_PROV.setdefault(p["provincia"], []).append(p)

PAGE_BY_PARENT: dict[str, list[GeoPage]] = {}
for p in PAGES:
    if p["parent"]:
        PAGE_BY_PARENT.setdefault(p["parent"], []).append(p)

# ---------------------------------------------------------- HTML shared --

def head_block(title: str, description: str, canonical: str,
               og_image: str = "/assets/hero.jpg",
               extra_jsonld: list | None = None) -> str:
    """`<head>` común: meta, OG, Twitter, favicon, CSS preload, JSON-LD."""
    css = "/assets/styles.css"
    favicon = "/assets/favicon.svg"
    canonical_abs = DOMAIN + canonical
    og_image_abs = DOMAIN + og_image
    jsonld = json.dumps(extra_jsonld or [], ensure_ascii=False, separators=(",", ":"))
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical_abs}">
<meta name="theme-color" content="#0b0f14">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical_abs}">
<meta property="og:image" content="{og_image_abs}">
<meta property="og:locale" content="es_ES">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{og_image_abs}">
<link rel="icon" type="image/svg+xml" href="{favicon}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;700;900&family=Oswald:wght@500;700&display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;700;900&family=Oswald:wght@500;700&display=swap">
<link rel="preload" as="style" href="{css}">
<link rel="stylesheet" href="{css}">
<script type="application/ld+json">{jsonld}</script>
</head>"""

def header_html(active: str = "") -> str:
    """Cabecera (sticky), logo con ruta relativa al raíz."""
    return f"""<body class="alpha">
<div class="top-alert"><div class="wrap"><span>Operativos 24/7 · Servicio profesional 365 días</span><a href="tel:{PHONE}">Urgencias y valoración: {PHONE}</a></div></div>
<header class="main-nav"><div class="wrap">
  <a class="brand-row" href="/"><span class="logo-mark">A</span><span class="logo-text">{BRAND}</span></a>
  <nav class="nav">
    <a href="/servicios/limpieza-tras-incendio/">Servicio</a>
    <a href="/ubicaciones/">Ubicaciones</a>
    <a href="/blog/">Blog</a>
    <a href="/testimonios/">Testimonios</a>
    <a href="/faq/">FAQ</a>
  </nav>
  <a class="btn" href="tel:{PHONE}">Llamar {PHONE}</a>
</div></header>"""

def footer_html() -> str:
    return f"""<div class="floating-contact">
  <a class="btn" href="tel:{PHONE}" aria-label="Llamar">📞 Llamar</a>
  <a class="btn alt" href="https://wa.me/{PHONE_INTL}" aria-label="WhatsApp">
    <img src="/assets/wa.svg" alt="WhatsApp" width="22" height="22" loading="lazy"> WhatsApp
  </a>
</div>
<footer class="site-foot"><div class="wrap">
  <div>
    <a class="brand-row" href="/"><span class="logo-mark">A</span><span class="logo-text">{BRAND}</span></a>
    <p>Servicio profesional de {KEYWORD.lower()}: hollín, humo, olor a quemado y apoyo en la documentación del seguro.</p>
    <p class="small">"{BRAND}" forma parte del Grupo <a href="/">Limpiezas de Incendios Alpha</a>.</p>
  </div>
  <div>
    <h3>Contacto</h3>
    <p><a href="tel:{PHONE}">{PHONE}</a><br>
    <a href="https://wa.me/{PHONE_INTL}">WhatsApp 24h</a><br>
    <a href="mailto:{EMAIL}">{EMAIL}</a></p>
  </div>
  <div>
    <h3>Sitio</h3>
    <p><a href="/servicios/limpieza-tras-incendio/">Servicio</a><br>
    <a href="/ubicaciones/">Ubicaciones</a><br>
    <a href="/blog/">Blog</a><br>
    <a href="/galeria/">Galería</a><br>
    <a href="/testimonios/">Testimonios</a><br>
    <a href="/faq/">Preguntas frecuentes</a></p>
  </div>
  <div>
    <h3>Legal</h3>
    <p><a href="/aviso-legal/">Aviso legal</a><br>
    <a href="/privacidad/">Política de privacidad</a><br>
    <a href="/cookies/">Política de cookies</a></p>
  </div>
</div></footer>
<div id="cookies" class="cookie-banner" hidden>
  <p>Usamos cookies técnicas y de medición. <a href="/cookies/">Más info</a>.</p>
  <button type="button">Aceptar</button>
</div>
<script>
  // Banner cookies
  (function(){{
    var k="lda_cookies_v1", b=document.getElementById("cookies");
    if(!localStorage.getItem(k)){{ b.hidden=false; }}
    b.querySelector("button").addEventListener("click", function(){{
      localStorage.setItem(k, "1"); b.hidden=true;
    }});
  }})();
  // Formulario inline (FormSubmit AJAX)
  document.addEventListener("submit", function(e){{
    var f = e.target.closest("form.callback-form");
    if(!f) return;
    e.preventDefault();
    var ok = f.querySelector(".form-ok"), err = f.querySelector(".form-err");
    if(ok) ok.style.display="none"; if(err) err.style.display="none";
    fetch(f.action, {{ method: "POST", body: new FormData(f),
      headers: {{ "Accept": "application/json" }} }})
      .then(function(r){{
        if(r.ok){{ if(ok) ok.style.display="block"; f.reset(); }}
        else throw 0;
      }}).catch(function(){{ if(err) err.style.display="block"; }});
  }});
</script>
</body></html>"""

def breadcrumb_ld(items: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name,
             "item": DOMAIN + url}
            for i, (name, url) in enumerate(items)
        ],
    }

def organization_ld() -> dict:
    return {
        "@context": "https://schema.org", "@type": "Organization",
        "name": BRAND, "url": DOMAIN + "/",
        "logo": DOMAIN + "/assets/logo.svg",
        "telephone": "+" + PHONE_INTL,
        "email": EMAIL,
        "description": f"Empresa especializada en {KEYWORD.lower()}: hollín, humo, olor y descontaminación tras incendio.",
        "areaServed": [ccaa for ccaa, _, _ in CCAA],
    }

def local_business_ld(ciudad: str, url: str) -> dict:
    return {
        "@context": "https://schema.org", "@type": "LocalBusiness",
        "name": f"{BRAND} – {ciudad}",
        "url": DOMAIN + url, "telephone": "+" + PHONE_INTL,
        "email": EMAIL,
        "image": DOMAIN + "/assets/hero.jpg",
        "priceRange": "€€",
        "areaServed": ciudad,
        "address": {"@type": "PostalAddress", "addressLocality": ciudad, "addressCountry": "ES"},
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification",
             "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
             "opens": "07:00", "closes": "22:00"},
            {"@type": "OpeningHoursSpecification",
             "dayOfWeek": ["Saturday", "Sunday"],
             "opens": "08:00", "closes": "16:00"},
        ],
    }

def faqpage_ld(pairs: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in pairs
        ],
    }

def service_ld(ciudad: str) -> dict:
    return {
        "@context": "https://schema.org", "@type": "Service",
        "serviceType": KEYWORD,
        "provider": {"@type": "LocalBusiness", "name": BRAND, "telephone": "+" + PHONE_INTL},
        "areaServed": ciudad,
        "description": f"{KEYWORD} en {ciudad}: hollín, humo, olor y documentación para el seguro.",
    }

def website_ld() -> dict:
    return {
        "@context": "https://schema.org", "@type": "WebSite",
        "name": BRAND, "url": DOMAIN + "/", "inLanguage": "es-ES",
    }

def aggregate_rating_ld() -> dict:
    return {
        "@context": "https://schema.org", "@type": "LocalBusiness",
        "name": BRAND, "url": DOMAIN + "/",
        "aggregateRating": {
            "@type": "AggregateRating", "ratingValue": "4.9",
            "reviewCount": "47", "bestRating": "5", "worstRating": "1",
        },
    }

# ---------------------------------------------------------- form block --

def form_block(origen: str) -> str:
    """Formulario inline: Nombre, Teléfono, Población. Origen oculto."""
    return f"""<aside class="card form-card">
  <p class="eyebrow">Nosotros te llamamos</p>
  <h3>Pide tu valoración</h3>
  <p>Solo necesitamos 3 datos. Te llamamos en menos de 1 hora en horario laboral.</p>
  <form class="callback-form" action="https://formsubmit.co/ajax/{EMAIL}" method="POST">
    <input type="hidden" name="_subject" value="Aviso desde {origen}">
    <input type="hidden" name="_template" value="table">
    <input type="hidden" name="_captcha" value="false">
    <input type="hidden" name="Origen" value="{DOMAIN}{origen}">
    <label>Nombre</label>
    <input name="Nombre" placeholder="Tu nombre" required>
    <label>Teléfono</label>
    <input name="Telefono" type="tel" placeholder="600 000 000" required>
    <label>Población</label>
    <input name="Poblacion" placeholder="Ej. {pick(['Madrid','Valencia','Sevilla','Barcelona','Murcia'], origen)}" required>
    <button class="btn" type="submit">Te llamamos</button>
    <p class="form-ok" style="display:none;color:#0a7">Recibido. Te llamamos en breve.</p>
    <p class="form-err" style="display:none;color:#b00">No se ha podido enviar. Llámanos al {PHONE}.</p>
  </form>
</aside>"""

# ---------------------------------------------------------- generators --

def render_geo_page(p: GeoPage) -> str:
    slug = p["slug"]
    ciudad = p["name"]
    provincia = p["provincia"]
    ccaa = p["ccaa"]
    url = p["url"]
    kw_var = kw_variant_for(slug)

    title_t = pick(TITLE, slug)
    meta_t = pick(META, slug)
    h1_t = pick(H1, slug)

    fmt = dict(keyword=KEYWORD, kw_var=kw_var, ciudad=ciudad,
               provincia=provincia, brand=BRAND, phone=PHONE)

    title = title_t.format(**fmt)
    desc = meta_t.format(**fmt)
    h1 = h1_t.format(**fmt)

    # ---- intro (la keyword principal en los primeros 100 caracteres) ----
    intro = (f"{KEYWORD} en {ciudad}: te ayudamos con el hollín, el humo y el "
             f"olor a quemado tras un incendio en {ciudad} ({provincia}). "
             f"Llegamos, valoramos y limpiamos.")

    # ---- cuerpo: 6 párrafos rotados por hash(slug) ----
    notes = LOCAL_NOTES.get(provincia, {}) if p["kind"] != "barrio" else LOCAL_NOTES.get("Madrid", {})
    local = {
        "tipo": notes.get("tipo", "viviendas, locales y pequeñas comunidades"),
        "rasgo": notes.get("rasgo", "trato cercano y respuesta rápida"),
        "riesgo": notes.get("riesgo", "incendios de cocina y eléctricos en pisos urbanos"),
    }
    parr_fmt = dict(fmt, **local)
    chosen = [PARRAFOS[(h(slug) + i * 3) % len(PARRAFOS)] for i in range(7)]
    body_html = "\n".join(f"<p>{para.format(**parr_fmt)}</p>" for para in chosen)

    # ---- cobertura ----
    cobertura = pick(COBERTURA_BLURB, slug).format(**fmt)

    # ---- FAQ local (4 preguntas elegidas por hash) ----
    faqs = []
    for i in range(4):
        item = FAQ_LOCAL_POOL[(h(slug) + i * 2) % len(FAQ_LOCAL_POOL)]
        if item in faqs:
            item = FAQ_LOCAL_POOL[(h(slug) + i * 2 + 1) % len(FAQ_LOCAL_POOL)]
        faqs.append(item)
    # dedupe preservando orden
    seen = set(); ufaqs = []
    for it in faqs:
        if it["q"] not in seen:
            seen.add(it["q"]); ufaqs.append(it)
    faq_pairs = [(it["q"].format(**fmt), it["a"].format(**fmt)) for it in ufaqs]

    faq_html = "".join(
        f'<details class="card"><summary><h3>{q}</h3></summary><p>{a}</p></details>'
        for q, a in faq_pairs
    )

    # ---- interlinking: "También cubrimos" ----
    tambien_html = ""
    if p["kind"] == "provincia":
        muns_with_page = [pg for pg in PAGE_BY_PARENT.get(provincia, [])
                          if pg["kind"] == "municipio"]
        chips = []
        for m in MUNICIPIOS.get(provincia, []):
            pg = next((x for x in muns_with_page if x["name"] == m), None)
            if pg:
                chips.append(f'<a class="chip chip-on" href="{pg["url"]}">→ {m}</a>')
            else:
                chips.append(f'<span class="chip">{m}</span>')
        if provincia == "Madrid":
            for b in BARRIOS_MADRID:
                pg = next((x for x in PAGES if x["kind"] == "barrio" and x["name"] == b), None)
                if pg:
                    chips.append(f'<a class="chip chip-on" href="{pg["url"]}">→ Barrio {b}</a>')
        if chips:
            tambien_html = (
                '<section class="section"><div class="wrap">'
                f'<h2>También cubrimos en {provincia}</h2>'
                f'<div class="chips">{"".join(chips)}</div>'
                '</div></section>'
            )
    elif p["kind"] in ("municipio", "barrio"):
        provincia_page = next((x for x in PAGES
                               if x["kind"] == "provincia" and x["name"] == provincia), None)
        bits = []
        if provincia_page:
            bits.append(f'<a class="chip chip-on" href="{provincia_page["url"]}">→ {provincia}</a>')
        sib = [x for x in PAGE_BY_PROV.get(provincia, [])
               if x["slug"] != slug and x["kind"] != "provincia"][:8]
        for x in sib:
            bits.append(f'<a class="chip chip-on" href="{x["url"]}">→ {x["name"]}</a>')
        if bits:
            tambien_html = (
                '<section class="section"><div class="wrap">'
                f'<h2>Otras zonas cercanas a {ciudad}</h2>'
                f'<div class="chips">{"".join(bits)}</div></div></section>'
            )

    # ---- sidebar: "Otras poblaciones de provincia" + provincias cercanas ----
    sidebar_links = []
    for pg in PAGE_BY_PROV.get(provincia, []):
        if pg["slug"] != slug:
            sidebar_links.append(f'<a href="{pg["url"]}">{pg["name"]}</a>')
    sidebar_links = sidebar_links[:12]

    cercanas = []
    ccaa_slug = p["ccaa_slug"]
    for ccaa_name2, ccaa_slug2, provs in CCAA:
        if ccaa_slug2 != ccaa_slug:
            continue
        for prov in provs:
            if prov == provincia:
                continue
            ppage = next((x for x in PAGES
                          if x["kind"] == "provincia" and x["name"] == prov), None)
            if ppage:
                cercanas.append(f'<a href="{ppage["url"]}">{prov}</a>')
    cercanas = cercanas[:8]

    sidebar_html = f"""<aside class="sidebar">
      <div class="card">
        <h3>Otras poblaciones de {provincia}</h3>
        {''.join(sidebar_links) or '<p>Próximamente.</p>'}
        <p><a class="btn alt" href="/ubicaciones/">Ver todas las ubicaciones</a></p>
      </div>
      <div class="card">
        <h3>Provincias cercanas</h3>
        {''.join(cercanas) or '<p>—</p>'}
      </div>
    </aside>"""

    # ---- breadcrumbs ----
    crumbs = [("Inicio", "/"), ("Ubicaciones", "/ubicaciones/")]
    if p["kind"] in ("municipio", "barrio"):
        provincia_page = next((x for x in PAGES
                               if x["kind"] == "provincia" and x["name"] == provincia), None)
        if provincia_page:
            crumbs.append((provincia, provincia_page["url"]))
    crumbs.append((ciudad, url))

    crumbs_html = '<nav class="crumbs"><div class="wrap">' + " › ".join(
        f'<a href="{u}">{n}</a>' if i < len(crumbs) - 1 else f'<span>{n}</span>'
        for i, (n, u) in enumerate(crumbs)
    ) + "</div></nav>"

    # ---- testimonial ejemplo único ----
    barrios_provincia = LOCAL_NOTES.get(provincia, {}).get("barrios") or ["centro"]
    barrio_t = barrios_provincia[h(slug) % len(barrios_provincia)]
    nombre_test = ["María", "Javier", "Lucía", "Pedro", "Sara", "Andrés",
                   "Inés", "David", "Ana", "Tomás"][h(slug) % 10]
    testimonio = (
        f"\"Tuvimos un incendio en la cocina y el olor llegó a todas las habitaciones. "
        f"En {ciudad} llamamos a {BRAND}, vinieron al día siguiente y a la semana ya "
        f"podíamos volver a casa.\""
    )
    testimonio_html = f"""<section class="section testimonio"><div class="wrap">
      <p class="eyebrow">Cliente (ejemplo)</p>
      <blockquote class="card">
        <p>{testimonio}</p>
        <footer>— {nombre_test}, {barrio_t} ({ciudad})</footer>
      </blockquote>
      <p class="small">* Testimonio de ejemplo. Sustituiremos por reseñas reales en cuanto el cliente autorice publicarlas.</p>
    </div></section>"""

    # ---- JSON-LD ----
    jsonld = [
        organization_ld(),
        local_business_ld(ciudad, url),
        service_ld(ciudad),
        breadcrumb_ld(crumbs),
        faqpage_ld(faq_pairs),
    ]

    # ---- enlaces contextuales en cuerpo ----
    contextual = (
        f'<p>Lee también <a href="/blog/que-hacer-despues-de-un-incendio/">qué hacer en las primeras 72 horas</a> '
        f'o consulta nuestra <a href="/galeria/">galería de trabajos reales</a>.</p>'
    )

    head = head_block(title, desc, url,
                      og_image=f"/assets/foto-{slug[:30]}.jpg",
                      extra_jsonld=jsonld)
    body = f"""{header_html()}
{crumbs_html}
<main>
<section class="hero hero-local">
  <div class="wrap hero-grid">
    <div>
      <p class="eyebrow">{provincia} · {ccaa}</p>
      <h1>{h1}</h1>
      <p class="lead">{intro}</p>
      <div class="cta-row">
        <a class="btn" href="tel:{PHONE}">Llamar {PHONE}</a>
        <a class="btn alt" href="https://wa.me/{PHONE_INTL}">WhatsApp</a>
      </div>
    </div>
    {form_block(url)}
  </div>
</section>

<section class="section">
  <div class="wrap layout-with-sidebar">
    <article class="article">
      <p class="eyebrow">{KEYWORD} en {ciudad}</p>
      <h2>Qué hacemos en {ciudad} tras un incendio</h2>
      {body_html}
      <h2>Zonas de cobertura en {ciudad}</h2>
      <p>{cobertura}</p>
      <p>{KW_SECUNDARIAS[h(slug) % len(KW_SECUNDARIAS)].capitalize()},
      {KW_SECUNDARIAS[(h(slug)+3) % len(KW_SECUNDARIAS)]} o
      {KW_SECUNDARIAS[(h(slug)+7) % len(KW_SECUNDARIAS)]}: cualquier
      escenario lo cubrimos con el mismo proceso técnico.</p>
      {contextual}
    </article>
    {sidebar_html}
  </div>
</section>

{testimonio_html}

<section class="section faqs"><div class="wrap">
  <h2>La gente también pregunta — {ciudad}</h2>
  {faq_html}
</div></section>

{tambien_html}

<section class="section cta-band"><div class="wrap" style="text-align:center">
  <h2>¿Has tenido un incendio en {ciudad}?</h2>
  <p>Llámanos y te valoramos hoy mismo, sin compromiso.</p>
  <div class="cta-row" style="justify-content:center">
    <a class="btn" href="tel:{PHONE}">Llamar {PHONE}</a>
    <a class="btn alt" href="https://wa.me/{PHONE_INTL}">WhatsApp</a>
  </div>
</div></section>

</main>
{footer_html()}"""
    return head + body


def render_home() -> str:
    url = "/"
    title = f"{KEYWORD} 24h | Hollín, humo, olor y seguro | {BRAND}"
    desc = (f"{KEYWORD} con respuesta 24h: hollín, humo, olor a quemado y "
            f"documentación para el seguro. Llámanos al {PHONE} y te valoramos hoy.")
    jsonld = [organization_ld(), website_ld(), local_business_ld("España", "/"),
              aggregate_rating_ld(),
              breadcrumb_ld([("Inicio", "/")])]
    head = head_block(title, desc, url, extra_jsonld=jsonld)

    # FAQ de la home (genérica, sin {city})
    home_faq = [
        ("¿Cuánto tarda una limpieza después de incendio?",
         "Depende del tamaño y del tipo de incendio. Una cocina pequeña suele estar lista en 2-3 días; un piso completo, entre 5 y 10 días; un local o nave, según superficie. Damos plazo cerrado tras la primera visita."),
        ("¿Trabajáis con todas las compañías de seguros?",
         "Sí. Preparamos la documentación en el formato que pide el perito (memoria, fotos antes/después, desglose). Si la aseguradora lo pide, hablamos directamente con ellos."),
        ("¿Hace falta sacar las cosas antes de que vengáis?",
         "No. Llegamos, fotografiamos, protegemos y empezamos a trabajar. Lo que haya que retirar lo inventariamos para el seguro."),
        ("¿Eliminar el olor a humo está incluido?",
         "Sí. Tras la limpieza física hacemos ozonización o tratamiento con hidroxilo. Si pasadas 48 horas detectas olor residual, volvemos a tratar sin coste."),
        ("¿Trabajáis solo en grandes incendios?",
         "Trabajamos a cualquier escala. La mayoría de avisos que recibimos son cocinas, fritadoras y pequeños incendios eléctricos."),
        ("¿Cuánto cuesta?",
         "Hacemos una visita previa gratuita y entregamos presupuesto cerrado antes de empezar. Si lo cubre tu seguro, lo tramitamos contigo."),
    ]
    home_faq_html = "".join(
        f'<details class="card"><summary><h3>{q}</h3></summary><p>{a}</p></details>'
        for q, a in home_faq
    )
    jsonld.append(faqpage_ld(home_faq))

    # Re-render head con FAQ incluido
    head = head_block(title, desc, url, extra_jsonld=jsonld)

    # Selección destacada de provincias (las 8 capitales / provincias top)
    destacadas = ["Madrid", "Barcelona", "Valencia", "Sevilla", "Málaga",
                  "Zaragoza", "Murcia", "Toledo"]
    dest_html = ""
    for d in destacadas:
        pg = next((x for x in PAGES
                   if x["kind"] == "provincia" and x["name"] == d), None)
        if pg:
            dest_html += f'<a class="chip chip-on" href="{pg["url"]}">→ {d}</a>'

    body = f"""{header_html()}
<main>
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <p class="eyebrow">Operativos 24/7 · 365 días</p>
      <h1>{KEYWORD}: hollín, humo y olor fuera</h1>
      <p class="lead">Tras un incendio, cada hora cuenta. Limpiamos el hollín antes de que se fije, neutralizamos el olor y dejamos la documentación lista para el seguro.</p>
      <div class="cta-row">
        <a class="btn" href="tel:{PHONE}">Llamar {PHONE}</a>
        <a class="btn alt" href="https://wa.me/{PHONE_INTL}">WhatsApp</a>
      </div>
    </div>
    {form_block("/")}
  </div>
</section>

<section class="stats-strip"><div class="wrap">
  <div class="stat"><strong>24h</strong><span>Primera valoración</span></div>
  <div class="stat"><strong>72h</strong><span>Fase crítica</span></div>
  <div class="stat"><strong>0€</strong><span>Visita técnica</span></div>
  <div class="stat"><strong>30+</strong><span>Provincias atendidas</span></div>
</div></section>

<section class="section"><div class="wrap">
  <h2>Qué hacemos en una limpieza tras incendio</h2>
  <div class="grid service-list">
    <article class="card"><p class="eyebrow">01</p><h3>Hollín y humo</h3><p>Retirada por capas para no fijar la mancha, tanto en seco como con productos específicos.</p></article>
    <article class="card"><p class="eyebrow">02</p><h3>Olor a quemado</h3><p>Ozonización o tratamiento con hidroxilo en cada estancia hasta dejar olor neutro.</p></article>
    <article class="card"><p class="eyebrow">03</p><h3>Cocina incendiada</h3><p>Desengrase de campanas, muebles, techos y azulejos. Recuperación de superficies útiles.</p></article>
    <article class="card"><p class="eyebrow">04</p><h3>Vivienda quemada</h3><p>Trabajo por estancias para priorizar lo crítico (cocina, baño, dormitorios) y devolver la vivienda al uso.</p></article>
    <article class="card"><p class="eyebrow">05</p><h3>Documentación para el seguro</h3><p>Fotos antes/después, memoria de actuación y desglose para el perito. Sin sorpresas.</p></article>
  </div>
</div></section>

<section class="section critical"><div class="wrap grid" style="grid-template-columns:1fr 1fr">
  <article>
    <p class="eyebrow">Primeras 72 horas</p>
    <h2>Cada hora cuenta para que el hollín no se fije</h2>
    <p>El hollín es ácido. Si pasa de 72 horas sin tratar empieza a corroer materiales y a fijar el olor en textiles, paredes y conductos. Llámanos pronto, aunque sea para una valoración.</p>
    <p><a class="btn" href="/servicios/limpieza-tras-incendio/">Ver el servicio detallado</a></p>
  </article>
  <div class="grid before-after">
    <div class="panel">ANTES</div>
    <div class="panel">DESPUÉS</div>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <h2>Provincias destacadas donde operamos</h2>
  <div class="chips">{dest_html}</div>
  <p><a class="btn alt" href="/ubicaciones/">Ver todas las ubicaciones</a></p>
</div></section>

<section class="section faqs"><div class="wrap">
  <h2>Preguntas frecuentes</h2>
  {home_faq_html}
</div></section>

</main>
{footer_html()}"""
    return head + body


def render_servicio_madre() -> str:
    url = "/servicios/limpieza-tras-incendio/"
    title = f"{KEYWORD}: servicio completo 24h | {BRAND}"
    desc = (f"Servicio profesional de {KEYWORD.lower()}: hollín, humo, olor, "
            f"cocina, vivienda y documentación para el seguro. Atención al {PHONE}.")
    crumbs = [("Inicio", "/"), ("Servicio", url)]
    jsonld = [organization_ld(), service_ld("España"),
              local_business_ld("España", url),
              breadcrumb_ld(crumbs)]
    head = head_block(title, desc, url, extra_jsonld=jsonld)

    body = f"""{header_html()}
<nav class="crumbs"><div class="wrap"><a href="/">Inicio</a> › <span>Servicio</span></div></nav>
<main>
<section class="hero hero-local">
  <div class="wrap hero-grid">
    <div>
      <p class="eyebrow">Servicio</p>
      <h1>{KEYWORD}: el servicio explicado</h1>
      <p class="lead">{KEYWORD} es lo único que hacemos. Limpieza y descontaminación tras un incendio: hollín, humo, olor y apoyo para el seguro. No reformamos, no reparamos, no construimos. Hacemos lo que sabemos hacer.</p>
      <div class="cta-row">
        <a class="btn" href="tel:{PHONE}">Llamar {PHONE}</a>
        <a class="btn alt" href="https://wa.me/{PHONE_INTL}">WhatsApp</a>
      </div>
    </div>
    {form_block(url)}
  </div>
</section>

<section class="section"><div class="wrap article">
  <h2>Qué incluye una {KEYWORD.lower()}</h2>
  <ul>
    <li><strong>Valoración técnica gratuita</strong> en menos de 24 horas.</li>
    <li><strong>Documentación previa</strong>: fotografías por estancias, descripción del daño y plan de actuación.</li>
    <li><strong>Limpieza de hollín</strong> por capas en techos, paredes y suelos, según el tipo de combustión (cocina, eléctrica, mobiliario).</li>
    <li><strong>Tratamiento del olor a humo</strong>: ozonización o hidroxilo en estancias afectadas hasta dejar olor neutro.</li>
    <li><strong>Limpieza de cocina incendiada</strong>: desengrase de campana, muebles, baldas, electrodomésticos exteriores y azulejos.</li>
    <li><strong>Tratamiento de textiles</strong> (ropa, cortinas, sofás, alfombras) por separado, con inventario.</li>
    <li><strong>Memoria final</strong> con fotos antes/después y desglose para el perito.</li>
  </ul>

  <h2>Qué NO incluye (y por qué)</h2>
  <ul>
    <li>No reformamos ni pintamos: si una pared está calcinada, te decimos qué reformista la repondrá. Tras la reforma podemos volver a entregar limpio.</li>
    <li>No reparamos electrodomésticos: limpiamos el exterior y dejamos los aparatos para revisión del SAT.</li>
    <li>No realizamos peritaciones de seguro: documentamos para que el perito haga su trabajo más rápido.</li>
  </ul>

  <h2>Las primeras 72 horas: por qué importan</h2>
  <p>El hollín tras un incendio es ácido. En las primeras 24 horas empieza a fijarse en superficies porosas (yeso, madera, textil) y en las 48-72 horas siguientes corroe metales, daña electrónica y deja olor que ya no sale con limpieza normal. Cuanto antes intervenimos, menos pierdes.</p>

  <h2>Cómo trabajamos: paso a paso</h2>
  <ol>
    <li><strong>Llamada</strong> al {PHONE} o formulario. Te contestamos en horas.</li>
    <li><strong>Visita técnica</strong> gratuita y sin compromiso para valorar y fotografiar.</li>
    <li><strong>Presupuesto cerrado</strong>: nada de "depende".</li>
    <li><strong>Limpieza</strong> ordenada por estancias, con tu calendario.</li>
    <li><strong>Entrega</strong>: comprobación de olor, fotos finales y memoria para el seguro.</li>
    <li><strong>Garantía</strong>: si pasadas 48 horas detectas olor residual, volvemos a pasar sin coste.</li>
  </ol>

  <p><a class="btn" href="tel:{PHONE}">Llamar {PHONE}</a></p>
</div></section>

</main>
{footer_html()}"""
    return head + body


def render_ubicaciones() -> str:
    url = "/ubicaciones/"
    title = f"Ubicaciones donde hacemos {KEYWORD} | {BRAND}"
    desc = f"Listado completo de provincias, municipios y barrios donde damos servicio de {KEYWORD.lower()}."
    crumbs = [("Inicio", "/"), ("Ubicaciones", url)]
    jsonld = [organization_ld(), breadcrumb_ld(crumbs)]
    head = head_block(title, desc, url, extra_jsonld=jsonld)

    bloques = []
    for ccaa_name, ccaa_slug, provs in CCAA:
        items = []
        for prov in provs:
            ppage = next((x for x in PAGES
                          if x["kind"] == "provincia" and x["name"] == prov), None)
            sub = []
            for child in PAGE_BY_PROV.get(prov, []):
                if child["kind"] != "provincia":
                    label = ("Barrio " + child["name"]) if child["kind"] == "barrio" else child["name"]
                    sub.append(f'<li><a href="{child["url"]}">{label}</a></li>')
            items.append(
                f'<div class="card"><h3><a href="{ppage["url"]}">{prov}</a></h3>'
                f'<ul>{"".join(sub) or "<li><em>Solo capital</em></li>"}</ul></div>'
            )
        bloques.append(
            f'<section class="section"><div class="wrap"><h2>{ccaa_name}</h2>'
            f'<div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(240px,1fr))">'
            f'{"".join(items)}</div></div></section>'
        )

    body = f"""{header_html()}
<nav class="crumbs"><div class="wrap"><a href="/">Inicio</a> › <span>Ubicaciones</span></div></nav>
<main>
<section class="hero hero-local"><div class="wrap">
  <p class="eyebrow">Cobertura</p>
  <h1>Ubicaciones donde hacemos {KEYWORD.lower()}</h1>
  <p class="lead">Atendemos en 8 comunidades autónomas con landing propia por provincia, principales municipios y barrios de Madrid.</p>
</div></section>
{"".join(bloques)}
</main>
{footer_html()}"""
    return head + body


def render_404() -> str:
    url = "/404.html"
    title = "Página no encontrada | " + BRAND
    desc = "La página que buscas no existe. Vuelve al inicio o consulta las ubicaciones donde damos servicio."
    head = head_block(title, desc, "/404.html",
                      extra_jsonld=[organization_ld()])
    body = f"""{header_html()}
<main>
<section class="hero hero-local"><div class="wrap" style="text-align:center">
  <p class="eyebrow">Error 404</p>
  <h1>Esta página no existe</h1>
  <p class="lead">No hemos encontrado lo que buscas. Si has tenido un incendio y necesitas ayuda urgente:</p>
  <div class="cta-row" style="justify-content:center">
    <a class="btn" href="tel:{PHONE}">Llamar {PHONE}</a>
    <a class="btn alt" href="/">Volver al inicio</a>
    <a class="btn alt" href="/ubicaciones/">Ver ubicaciones</a>
  </div>
</div></section>
</main>
{footer_html()}"""
    return head + body


# ----------------------------------------------------------- sitemap --

def render_sitemap() -> str:
    urls = ["/", "/servicios/limpieza-tras-incendio/", "/ubicaciones/",
            "/blog/", "/galeria/", "/testimonios/", "/faq/",
            "/aviso-legal/", "/privacidad/", "/cookies/"]
    for p in PAGES:
        urls.append(p["url"])

    parts = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        prio = "1.0" if u == "/" else ("0.8" if "/limpieza-despues-de-incendio-" in u else "0.6")
        parts.append(
            f"<url><loc>{DOMAIN}{u}</loc><lastmod>{NOW}</lastmod>"
            f"<changefreq>weekly</changefreq><priority>{prio}</priority></url>"
        )
    parts.append("</urlset>")
    return "\n".join(parts)


def render_robots() -> str:
    return f"""# robots.txt — {BRAND}
User-agent: *
Allow: /

# Bots de IA — permisos explícitos
User-agent: GPTBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: anthropic-ai
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: CCBot
Allow: /
User-agent: Applebot-Extended
Allow: /
User-agent: cohere-ai
Allow: /
User-agent: Bytespider
Allow: /

Sitemap: {DOMAIN}/sitemap.xml
"""


def render_llms() -> str:
    lines = [
        f"# {BRAND}",
        "",
        f"> Empresa especializada en {KEYWORD.lower()}: hollín, humo, olor y descontaminación tras incendio. Operamos en 8 comunidades autónomas de España.",
        "",
        f"- Web: {DOMAIN}/",
        f"- Teléfono: {PHONE}",
        f"- WhatsApp: https://wa.me/{PHONE_INTL}",
        f"- Email: {EMAIL}",
        "- Horario: L-V 07:00-22:00, S-D 08:00-16:00",
        "",
        "## Servicio",
        f"- [{KEYWORD}]({DOMAIN}/servicios/limpieza-tras-incendio/): qué incluye, qué no incluye, cómo trabajamos.",
        "",
        "## Ubicaciones principales",
    ]
    for p in PAGES:
        if p["kind"] == "provincia":
            lines.append(f"- [{p['name']}]({DOMAIN}{p['url']})")
    lines += [
        "",
        "## Información de la empresa",
        "- Servicio: solo limpieza y descontaminación tras incendio. No reformamos, no reparamos.",
        "- Respuesta 24h en las primeras 72 horas tras el incendio.",
        "- Documentación lista para el seguro: fotos antes/después y memoria por estancias.",
    ]
    return "\n".join(lines) + "\n"


def render_htaccess() -> str:
    return f"""# .htaccess — {BRAND}

DirectoryIndex index.html

# Forzar HTTPS
RewriteEngine On
RewriteCond %{{HTTPS}} !=on
RewriteRule ^ https://%{{HTTP_HOST}}%{{REQUEST_URI}} [L,R=301]

# Redirect www → sin www
RewriteCond %{{HTTP_HOST}} ^www\\.(.+)$ [NC]
RewriteRule ^ https://%1%{{REQUEST_URI}} [L,R=301]

# 301 de URLs antiguas → nueva arquitectura
RewriteRule ^provincias/([a-z0-9-]+)/?$ /{KEYWORD_SLUG}-$1/ [L,R=301]
RewriteRule ^localidades/([a-z0-9-]+)/?$ /{KEYWORD_SLUG}-$1/ [L,R=301]
RewriteRule ^zonas/([a-z0-9-]+)/?$ /ubicaciones/ [L,R=301]
RewriteRule ^barrios/madrid/([a-z0-9-]+)/?$ /{KEYWORD_SLUG}-madrid-$1/ [L,R=301]
RewriteRule ^barrios/valencia/([a-z0-9-]+)/?$ /{KEYWORD_SLUG}-valencia-$1/ [L,R=301]
RewriteRule ^servicios/eliminacion-humo-hollin/?$ /servicios/limpieza-tras-incendio/ [L,R=301]
RewriteRule ^servicios/limpieza-cocina-incendiada/?$ /servicios/limpieza-tras-incendio/ [L,R=301]
RewriteRule ^servicios/recuperacion-vivienda-quemada/?$ /servicios/limpieza-tras-incendio/ [L,R=301]
RewriteRule ^servicios/informe-seguro-incendio/?$ /servicios/limpieza-tras-incendio/ [L,R=301]

# Página 404 personalizada
ErrorDocument 404 /404.html

# Caché de estáticos
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/css                 "access plus 30 days"
  ExpiresByType application/javascript   "access plus 30 days"
  ExpiresByType image/jpeg               "access plus 90 days"
  ExpiresByType image/png                "access plus 90 days"
  ExpiresByType image/svg+xml            "access plus 90 days"
  ExpiresByType image/webp               "access plus 90 days"
  ExpiresByType font/woff2               "access plus 180 days"
  ExpiresByType text/html                "access plus 1 hour"
</IfModule>

# Compresión gzip
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css text/javascript application/javascript application/json image/svg+xml
</IfModule>

# Cabeceras de seguridad
<IfModule mod_headers.c>
  Header set X-Content-Type-Options "nosniff"
  Header set X-Frame-Options "SAMEORIGIN"
  Header set Referrer-Policy "strict-origin-when-cross-origin"
  Header set Permissions-Policy "interest-cohort=()"
</IfModule>
"""


# Placeholder pages (legales, blog, galería, testimonios, faq) — versión mínima
def render_placeholder(title_short: str, h1: str, body_text: str, path: str) -> str:
    title = f"{title_short} | {BRAND}"
    desc = body_text[:155]
    head = head_block(title, desc, path,
                      extra_jsonld=[organization_ld(),
                                    breadcrumb_ld([("Inicio", "/"), (title_short, path)])])
    body = f"""{header_html()}
<nav class="crumbs"><div class="wrap"><a href="/">Inicio</a> › <span>{title_short}</span></div></nav>
<main>
<section class="hero hero-local"><div class="wrap">
  <p class="eyebrow">{title_short}</p>
  <h1>{h1}</h1>
  <p class="lead">{body_text}</p>
</div></section>
</main>
{footer_html()}"""
    return head + body


# ----------------------------------------------------------- main --

def clean_old() -> None:
    """Elimina el contenido antiguo (provincias/, localidades/, zonas/, barrios/, spintax/) y servicios obsoletos."""
    for d in ["provincias", "localidades", "zonas", "barrios", "spintax"]:
        p = ROOT / d
        if p.exists():
            shutil.rmtree(p)
    # Servicios obsoletos
    for s in ["eliminacion-humo-hollin", "limpieza-cocina-incendiada",
              "recuperacion-vivienda-quemada", "informe-seguro-incendio"]:
        p = ROOT / "servicios" / s
        if p.exists():
            shutil.rmtree(p)


def main() -> None:
    clean_old()

    # Home
    write(ROOT / "index.html", render_home())
    # Servicio madre
    write(ROOT / "servicios" / "limpieza-tras-incendio" / "index.html",
          render_servicio_madre())
    # Geo landings
    for p in PAGES:
        slug = p["slug"]
        dirname = f"{KEYWORD_SLUG}-{slug}"
        write(ROOT / dirname / "index.html", render_geo_page(p))
    # Ubicaciones
    write(ROOT / "ubicaciones" / "index.html", render_ubicaciones())
    # 404
    write(ROOT / "404.html", render_404())

    # Placeholders (se completan en Fase 2 y 3)
    write(ROOT / "blog" / "index.html", render_placeholder(
        "Blog", f"Blog sobre {KEYWORD.lower()}",
        "Próximamente publicaremos guías sobre cómo actuar tras un incendio, cómo eliminar el olor a humo, cómo gestionar el seguro y casos reales por ciudad.",
        "/blog/"))
    write(ROOT / "galeria" / "index.html", render_placeholder(
        "Galería", "Galería de trabajos reales",
        "Publicaremos pronto fotografías reales de intervenciones por estancias, antes y después, en distintas ciudades.",
        "/galeria/"))
    write(ROOT / "testimonios" / "index.html", render_placeholder(
        "Testimonios", "Testimonios de clientes",
        "Estamos preparando una sección con reseñas reales de clientes. Hasta entonces, llámanos al " + PHONE + " para pedir referencias verificadas.",
        "/testimonios/"))
    write(ROOT / "faq" / "index.html", render_placeholder(
        "FAQ", "Preguntas frecuentes",
        "Resolvemos las dudas habituales: tiempos de actuación, cobertura del seguro, eliminación del olor a humo, tratamiento de textiles y limpieza de cocinas incendiadas.",
        "/faq/"))
    write(ROOT / "aviso-legal" / "index.html", render_placeholder(
        "Aviso Legal", "Aviso legal",
        "Datos del titular del sitio: PENDIENTE DE COMPLETAR (razón social, NIF, domicilio fiscal, registro mercantil). Avisa al equipo para rellenar antes de pasar a producción.",
        "/aviso-legal/"))
    write(ROOT / "privacidad" / "index.html", render_placeholder(
        "Política de Privacidad", "Política de privacidad",
        "Tratamos los datos del formulario (Nombre, Teléfono, Población) con la única finalidad de devolverte la llamada. No los compartimos con terceros. Datos del responsable: PENDIENTE.",
        "/privacidad/"))
    write(ROOT / "cookies" / "index.html", render_placeholder(
        "Política de Cookies", "Política de cookies",
        "Este sitio usa cookies técnicas y de medición anónima. Puedes aceptar o rechazar en el banner. No se utilizan cookies publicitarias ni de perfilado.",
        "/cookies/"))

    # Técnicos
    write(ROOT / "sitemap.xml", render_sitemap())
    write(ROOT / "robots.txt", render_robots())
    write(ROOT / "llms.txt", render_llms())
    write(ROOT / ".htaccess", render_htaccess())

    total = len(PAGES) + 1 + 1 + 1 + 1 + 7  # geo + home + servicio + ubicaciones + 404 + placeholders
    print(f"Generadas {total} páginas HTML + sitemap + robots + llms + .htaccess")
    print(f"  Geo pages: {len(PAGES)} (provincias={sum(1 for p in PAGES if p['kind']=='provincia')}, "
          f"municipios={sum(1 for p in PAGES if p['kind']=='municipio')}, "
          f"barrios={sum(1 for p in PAGES if p['kind']=='barrio')})")


if __name__ == "__main__":
    main()
