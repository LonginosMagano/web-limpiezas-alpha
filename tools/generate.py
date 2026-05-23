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
from urllib.parse import quote


def urlsafe(p: str) -> str:
    """URL-encode una ruta de asset preservando "/", ".", "-" y "_"."""
    return quote(p, safe="/.-_")

import sys
sys.path.insert(0, str(Path(__file__).parent))
from data import (
    BRAND, DOMAIN, BASE_PATH, PHONE, PHONE_INTL, EMAIL, KEYWORD, KEYWORD_SLUG,
    KW_VARIANTS_NUCLEO, KW_SECUNDARIAS,
    CCAA, MUNICIPIOS, BARRIOS_MADRID, SLUG_ALIAS, LOCAL_NOTES,
    INTERVENCIONES, HERO_POOL, ASEGURADORAS, ALT_SCENES,
)


def with_base(html: str) -> str:
    """Prefija href="/foo" y src="/foo" con BASE_PATH para que el sitio
    funcione cuando se sirve desde un subdirectorio (GitHub Pages project).
    Ignora rutas protocol-relative ("//..."), absolutas (http(s)://),
    fragmentos (#...), tel:/mailto:/wa.me y rutas ya prefijadas."""
    if not BASE_PATH:
        return html
    bp = BASE_PATH.rstrip("/")
    # Solo paths que empiezan por "/" pero no por "//" y no por BASE_PATH ya.
    html = re.sub(r'href="/(?!/)(?!' + re.escape(bp[1:]) + r'/)',
                  f'href="{bp}/', html)
    html = re.sub(r'src="/(?!/)(?!' + re.escape(bp[1:]) + r'/)',
                  f'src="{bp}/', html)
    # Atributo action="/" en formularios (por si lo añadimos algún día)
    html = re.sub(r'action="/(?!/)(?!' + re.escape(bp[1:]) + r'/)',
                  f'action="{bp}/', html)
    return html
from templates import TITLE, META, H1, PARRAFOS, COBERTURA_BLURB, FAQ_LOCAL_POOL
from posts import POSTS, CATEGORY_LABEL

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
    # Aplicar prefijo de BASE_PATH a enlaces internos en archivos HTML.
    if path.suffix == ".html":
        content = with_base(content)
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
    favicon = "/assets/favicon.ico"
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
<link rel="icon" type="image/x-icon" href="{favicon}">
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
  <a class="brand-row" href="/"><img class="logo-img" src="/assets/logo.png" alt="{BRAND}" width="140" height="70" loading="eager"><span class="logo-text">{BRAND}</span></a>
  <button class="nav-toggle" aria-label="Abrir menú" aria-expanded="false" aria-controls="primary-nav">
    <span></span><span></span><span></span>
  </button>
  <nav class="nav" id="primary-nav">
    <a href="/servicios/limpieza-tras-incendio/">Servicio</a>
    <a href="/ubicaciones/">Ubicaciones</a>
    <a href="/blog/">Blog</a>
    <a href="/testimonios/">Testimonios</a>
    <a href="/faq/">FAQ</a>
    <a class="btn nav-cta" href="tel:{PHONE}">Llamar {PHONE}</a>
  </nav>
  <a class="btn nav-desktop-cta" href="tel:{PHONE}">Llamar {PHONE}</a>
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
    <a class="brand-row" href="/"><img class="logo-img" src="/assets/logo.png" alt="{BRAND}" width="140" height="70" loading="eager"><span class="logo-text">{BRAND}</span></a>
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
  // Hamburger mobile menu
  (function(){{
    var t = document.querySelector(".nav-toggle"),
        n = document.getElementById("primary-nav");
    if (!t || !n) return;
    t.addEventListener("click", function(){{
      var open = n.classList.toggle("open");
      t.setAttribute("aria-expanded", open ? "true" : "false");
      t.classList.toggle("open", open);
    }});
    n.querySelectorAll("a").forEach(function(a){{
      a.addEventListener("click", function(){{
        n.classList.remove("open");
        t.classList.remove("open");
        t.setAttribute("aria-expanded", "false");
      }});
    }});
  }})();
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
        "logo": DOMAIN + "/assets/logo.png",
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

def hero_svg_for(slug: str, ciudad: str) -> str:
    """SVG estilizado para usar como hero LCP de cada landing.
    Se escribe en /assets/landings/limpieza-despues-de-incendio-{slug}.svg
    para tener nombre de archivo descriptivo con keyword + ciudad."""
    initial = (ciudad or "?")[0].upper()
    # Variación cromática suave por hash para no clonar visualmente
    hue = h(slug) % 60  # 0..59 → naranjas/rojos
    accent = f"hsl({10 + hue % 30}, 88%, 52%)"
    text = ciudad.upper()[:18]
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450" role="img"
 aria-label="{KEYWORD} en {ciudad}">
  <title>{KEYWORD} en {ciudad}</title>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0b0f14"/>
      <stop offset="1" stop-color="#1b222b"/>
    </linearGradient>
    <radialGradient id="glow" cx="78%" cy="22%" r="55%">
      <stop offset="0" stop-color="{accent}" stop-opacity=".55"/>
      <stop offset="1" stop-color="{accent}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="800" height="450" fill="url(#bg)"/>
  <rect width="800" height="450" fill="url(#glow)"/>
  <g transform="translate(60,80)">
    <text x="0" y="0" fill="{accent}" font-family="Oswald, Arial" font-weight="700"
      font-size="20" letter-spacing="4">{ciudad.upper()[:20]}</text>
    <text x="0" y="58" fill="#f7f7f4" font-family="Oswald, Arial" font-weight="700"
      font-size="46">LIMPIEZA TRAS</text>
    <text x="0" y="108" fill="#f7f7f4" font-family="Oswald, Arial" font-weight="700"
      font-size="46">INCENDIO</text>
    <text x="0" y="170" fill="#cbd0d4" font-family="Archivo, Arial"
      font-size="18">Hollín · Humo · Olor · Seguro</text>
    <rect x="0" y="200" width="160" height="42" fill="{accent}" rx="3"/>
    <text x="14" y="228" fill="#170b00" font-family="Archivo, Arial"
      font-weight="900" font-size="16">RESPUESTA 24H</text>
  </g>
  <!-- llama estilizada -->
  <g transform="translate(560,90)" opacity=".9">
    <path d="M80 30 C 60 80 30 90 50 150 C 60 180 100 200 110 170 C 120 200 160 180 170 150 C 190 90 160 80 140 30 C 130 60 110 60 110 30 C 100 60 90 60 80 30 Z"
      fill="{accent}"/>
    <path d="M95 80 C 85 110 80 130 95 150 C 110 170 130 160 125 130 C 115 110 115 100 95 80 Z"
      fill="#ffd9b3" opacity=".7"/>
  </g>
</svg>'''


# Datos de testimonios (ejemplo — marcar como tales hasta tener reales)
TESTIMONIOS = [
    {"nombre": "María L.", "ciudad": "Madrid", "barrio": "Salamanca",
     "rating": 5, "texto": "Se quemó la cocina y olía a humo en todas las habitaciones. Llegaron al día siguiente, en 4 días estaba todo limpio y el olor desapareció. La memoria que entregaron al seguro la aceptaron sin pegas."},
    {"nombre": "Javier R.", "ciudad": "Barcelona", "barrio": "Eixample",
     "rating": 5, "texto": "Un incendio eléctrico en el cuadro afectó al hollín de medio piso. Coordinaron con el administrador del edificio y trabajaron también en la escalera. Muy profesionales."},
    {"nombre": "Lucía F.", "ciudad": "Valencia", "barrio": "Ruzafa",
     "rating": 4, "texto": "El presupuesto fue claro desde el inicio. Tardaron 5 días en dejar el piso para volver a alquilar. El olor a humo no ha vuelto a aparecer."},
    {"nombre": "Pedro G.", "ciudad": "Sevilla", "barrio": "Triana",
     "rating": 5, "texto": "Una freidora prendió en el local. Nos dejaron limpiar parte y reabrir al tercer día mientras seguían con la cocina. Salvaron mucha pérdida por cierre."},
    {"nombre": "Sara M.", "ciudad": "Málaga", "barrio": "Centro Histórico",
     "rating": 5, "texto": "Apartamento turístico con un susto a las 11 de la noche. A las 9 de la mañana ya estaban allí valorando. Tres días después, listo para huéspedes."},
    {"nombre": "Andrés P.", "ciudad": "Zaragoza", "barrio": "Delicias",
     "rating": 4, "texto": "Trabajaron con el perito del seguro directamente. No tuve que mover papeles. La factura coincidió exactamente con el presupuesto."},
    {"nombre": "Inés D.", "ciudad": "Murcia", "barrio": "El Carmen",
     "rating": 5, "texto": "Hubo más hollín del previsto en armarios y cajones cerrados. Volvieron una segunda vez sin coste para revisar el olor. Cumplieron lo que prometieron."},
    {"nombre": "Tomás V.", "ciudad": "Toledo", "barrio": "Casco Histórico",
     "rating": 5, "texto": "Casa antigua con vigas de madera. Nos asesoraron qué se podía limpiar y qué había que reponer con un reformista. Trato muy honesto."},
]

# FAQ global
FAQ_GLOBAL = [
    ("¿Cuánto tarda una limpieza tras incendio?",
     "Depende del tamaño y del tipo de incendio. Una cocina pequeña suele estar lista en 2-3 días; un piso completo, entre 5 y 10 días; un local o nave, según superficie. Damos plazo cerrado tras la primera visita."),
    ("¿Trabajáis con todas las compañías de seguros?",
     "Sí. Preparamos la documentación en el formato que pide el perito (memoria, fotos antes/después, desglose por estancias). Si la aseguradora lo pide, hablamos directamente con ellos."),
    ("¿Cuánto cuesta?",
     "Hacemos una visita previa gratuita y entregamos presupuesto cerrado antes de empezar. Rangos orientativos: 800-1.500 € una cocina, 2.500-8.000 € un piso completo, según superficie y tipo de hollín. Si lo cubre tu seguro, tramitamos con la aseguradora."),
    ("¿Hace falta sacar las cosas antes de que vengáis?",
     "No. Llegamos, fotografiamos, protegemos y empezamos a trabajar. Lo que haya que retirar lo inventariamos para el seguro."),
    ("¿Eliminar el olor a humo está incluido?",
     "Sí. Tras la limpieza física hacemos ozonización o tratamiento con hidroxilo en las estancias afectadas. Si pasadas 48 horas detectas olor residual, volvemos a tratar sin coste."),
    ("¿Limpiáis ropa, cortinas y sofás?",
     "Sí, pero por separado del trabajo de obra: inventariamos, retiramos y enviamos a tratamiento especializado. La limpieza en seco normal fija el olor para siempre, así que nunca se hace así."),
    ("¿Trabajáis solo en grandes siniestros?",
     "No. La mayoría de avisos son cocinas, fritadoras y pequeños incendios eléctricos. Trabajamos a cualquier escala con el mismo proceso técnico."),
    ("¿En cuánto tiempo podéis estar en mi vivienda?",
     "Si nos llamas antes de las 18h, normalmente el mismo día o al día siguiente. Las primeras 72 horas son críticas para que el hollín no se fije."),
    ("¿Qué pasa si el seguro no cubre la limpieza?",
     "Lo planificamos por fases: priorizamos cocina, baño y zona habitable y dejamos lo estético para una segunda fase. Si la denegación es injusta, te orientamos para reclamar al SAC de la aseguradora."),
    ("¿Puedo dormir en la vivienda mientras se limpia?",
     "Mejor no. El hollín suelto y los productos de limpieza no son compatibles con permanencia continua, y la ozonización exige espacio cerrado sin personas."),
    ("¿Hacéis también reformas o pintura?",
     "No. Solo limpieza y descontaminación tras incendio. Si una pared está calcinada y hay que reponerla, te indicamos qué reformista puede hacerlo. Cuando termine la obra, podemos volver a entregar todo limpio."),
    ("¿Tenéis seguro de responsabilidad civil propio?",
     "Sí. Toda nuestra actividad está cubierta con póliza de responsabilidad civil profesional. Te lo acreditamos si tu aseguradora lo solicita."),
]

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

    # Foto hero: usa la intervención específica si existe (Madrid, BCN…)
    # o cicla por hash sobre el pool de fotos reales.
    if provincia in INTERVENCIONES:
        hero_photo = INTERVENCIONES[provincia][1]
    elif ciudad in INTERVENCIONES:
        hero_photo = INTERVENCIONES[ciudad][1]
    else:
        hero_photo = HERO_POOL[h("hero-" + slug) % len(HERO_POOL)]

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

    # ---- interlinking: "También cubrimos" + "Barrios donde operamos" ----
    tambien_html = ""
    barrios_section = ""
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
        if chips:
            tambien_html = (
                '<section class="section"><div class="wrap">'
                f'<h2>También cubrimos en {provincia}</h2>'
                f'<div class="chips">{"".join(chips)}</div>'
                '</div></section>'
            )
        # Bloque propio de barrios (solo Madrid de momento)
        if provincia == "Madrid":
            barrio_chips = []
            for b in BARRIOS_MADRID:
                pg = next((x for x in PAGES if x["kind"] == "barrio" and x["name"] == b), None)
                if pg:
                    barrio_chips.append(f'<a class="chip chip-on" href="{pg["url"]}">→ Barrio {b}</a>')
            if barrio_chips:
                barrios_section = (
                    '<section class="section barrios-band"><div class="wrap">'
                    f'<h2>Barrios donde operamos en {provincia}</h2>'
                    '<p>Atendemos los 21 distritos. Cada uno tiene su página con FAQ local:</p>'
                    f'<div class="chips">{"".join(barrio_chips)}</div>'
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

    # Sidebar extra: "Otros barrios" cuando estamos en una landing de barrio
    sidebar_barrios = ""
    if p["kind"] == "barrio":
        otros_b = []
        for x in PAGES:
            if x["kind"] == "barrio" and x["slug"] != slug:
                otros_b.append(f'<a href="{x["url"]}">Barrio {x["name"]}</a>')
        otros_b = otros_b[:12]
        if otros_b:
            sidebar_barrios = (
                f'<div class="card"><h3>Otros barrios de Madrid</h3>'
                f'{"".join(otros_b)}'
                f'</div>'
            )

    sidebar_html = f"""<aside class="sidebar">
      <div class="card">
        <h3>Otras poblaciones de {provincia}</h3>
        {''.join(sidebar_links) or '<p>Próximamente.</p>'}
        <p><a class="btn alt" href="/ubicaciones/">Ver todas las ubicaciones</a></p>
      </div>
      {sidebar_barrios}
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
        f'<p>Lee también <a href="/blog/que-hacer-despues-de-un-incendio/">qué hacer en las primeras 72 horas</a>, '
        f'<a href="/blog/como-eliminar-olor-humo/">cómo eliminar el olor a humo</a> '
        f'o consulta nuestra <a href="/galeria/">galería de trabajos reales</a>.</p>'
    )

    # ---- bloque "Guías del blog" para link juice landing → posts ----
    # Selección curada: si la landing es Madrid/Barcelona/Málaga enlaza al
    # post específico de esa ciudad además de 3 generales rotados por hash.
    from posts import POSTS as _POSTS  # import local para evitar ciclo
    blog_links = []
    # Post de ciudad si existe (Madrid, Barcelona, Málaga)
    city_post = next((p for p in _POSTS if p.get("city") == ciudad), None)
    if city_post:
        blog_links.append((f"/blog/{city_post['slug']}/", city_post["title"]))
    # 3-4 posts generales (rotación por hash para no clonar)
    generales = [p for p in _POSTS if p["category"] in ("general", "seguros")]
    for i in range(4 if not city_post else 3):
        pg_post = generales[(h("blog-" + slug) + i * 7) % len(generales)]
        link = (f"/blog/{pg_post['slug']}/", pg_post["title"])
        if link not in blog_links:
            blog_links.append(link)
    guias_html = (
        '<section class="section guias-blog"><div class="wrap">'
        f'<h2>Guías y consejos relacionados</h2>'
        '<div class="grid guias-grid">'
        + "".join(
            f'<a class="card guia-card" href="{href}">'
            f'<span class="eyebrow">Guía</span>'
            f'<h3>{title}</h3>'
            f'<span class="ver-mas">Leer →</span></a>'
            for href, title in blog_links
        )
        + '</div></div></section>'
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
      <img class="hero-img" src="/{urlsafe(hero_photo)}"
        alt="{ALT_SCENES[h('alt-' + slug) % len(ALT_SCENES)]} en {ciudad} | {KEYWORD}"
        width="800" height="450" loading="eager">
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
{barrios_section}

{guias_html}

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
      <img class="hero-img" src="/{urlsafe(HERO_POOL[0])}" alt="{KEYWORD} — intervención real" width="800" height="450" loading="eager">
      <div class="cta-row">
        <a class="btn" href="tel:{PHONE}">Llamar {PHONE}</a>
        <a class="btn alt" href="https://wa.me/{PHONE_INTL}">WhatsApp</a>
      </div>
    </div>
    {form_block("/")}
  </div>
</section>

<section class="trust-strip"><div class="wrap">
  <p class="eyebrow">Trabajamos con tu aseguradora</p>
  <div class="trust-logos">
{"".join(f'    <img src="/{urlsafe(src)}" alt="Logo {name}" loading="lazy" height="48">' + chr(10) for name, src in ASEGURADORAS)}  </div>
</div></section>

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
    <div class="panel-img"><img src="/{urlsafe(INTERVENCIONES['Madrid'][0])}" alt="Antes — {KEYWORD}" width="800" height="450" loading="lazy"><span class="label-ba">ANTES</span></div>
    <div class="panel-img"><img src="/{urlsafe(INTERVENCIONES['Madrid'][1])}" alt="Después — {KEYWORD}" width="800" height="450" loading="lazy"><span class="label-ba active">DESPUÉS</span></div>
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

    n_provs = sum(1 for p in PAGES if p["kind"] == "provincia")
    n_muns = sum(1 for p in PAGES if p["kind"] == "municipio")
    n_barr = sum(1 for p in PAGES if p["kind"] == "barrio")

    # Bloques por CCAA: cabecera grande con número + nombre + métricas;
    # provincias en grid de cards con sus municipios como chips.
    bloques = []
    for idx, (ccaa_name, ccaa_slug, provs) in enumerate(CCAA, 1):
        prov_cards = []
        ccaa_muns = 0
        ccaa_barr = 0
        for prov in provs:
            ppage = next((x for x in PAGES
                          if x["kind"] == "provincia" and x["name"] == prov), None)
            children = [c for c in PAGE_BY_PROV.get(prov, []) if c["kind"] != "provincia"]
            muns = [c for c in children if c["kind"] == "municipio"]
            barrs = [c for c in children if c["kind"] == "barrio"]
            ccaa_muns += len(muns)
            ccaa_barr += len(barrs)

            chips = []
            for c in muns + barrs:
                label = ("Barrio " + c["name"]) if c["kind"] == "barrio" else c["name"]
                chips.append(f'<a class="chip chip-on" href="{c["url"]}">{label}</a>')
            chips_html = (
                f'<div class="chips">{"".join(chips)}</div>'
                if chips else '<p class="small">Atendemos toda la provincia desde la capital.</p>'
            )
            stats = f'<span class="loc-stat">{len(muns)} municipios</span>'
            if barrs:
                stats += f' · <span class="loc-stat">{len(barrs)} barrios</span>'
            prov_cards.append(
                f'<article class="card loc-prov">'
                f'<header class="loc-prov-head">'
                f'<h3><a href="{ppage["url"]}">{prov}</a></h3>'
                f'<p class="small">{stats}</p>'
                f'</header>'
                f'{chips_html}'
                f'<p><a class="ver-landing" href="{ppage["url"]}">Ver landing de {prov} →</a></p>'
                f'</article>'
            )
        bloques.append(f"""<section class="section loc-ccaa">
  <div class="wrap">
    <div class="loc-ccaa-head">
      <span class="loc-num">{idx:02d}</span>
      <div>
        <p class="eyebrow">Comunidad autónoma</p>
        <h2>{ccaa_name}</h2>
        <p class="small loc-meta">{len(provs)} provincia{'s' if len(provs)>1 else ''} · {ccaa_muns} municipios · {ccaa_barr} barrios</p>
      </div>
    </div>
    <div class="grid loc-prov-grid">{"".join(prov_cards)}</div>
  </div>
</section>""")

    body = f"""{header_html()}
<nav class="crumbs"><div class="wrap"><a href="/">Inicio</a> › <span>Ubicaciones</span></div></nav>
<main>
<section class="hero hero-local"><div class="wrap">
  <p class="eyebrow">Cobertura</p>
  <h1>Ubicaciones donde hacemos {KEYWORD.lower()}</h1>
  <p class="lead">Atendemos en {len(CCAA)} comunidades autónomas, con landing propia por provincia, principales municipios y barrios.</p>
  <div class="loc-totals">
    <div class="loc-total"><strong>{len(CCAA)}</strong><span>Comunidades</span></div>
    <div class="loc-total"><strong>{n_provs}</strong><span>Provincias</span></div>
    <div class="loc-total"><strong>{n_muns}</strong><span>Municipios</span></div>
    <div class="loc-total"><strong>{n_barr}</strong><span>Barrios Madrid</span></div>
  </div>
  <div class="loc-search">
    <input type="search" id="loc-search-input" placeholder="Busca tu ciudad, municipio o barrio…" autocomplete="off" aria-label="Buscar ubicación">
    <p class="small loc-search-count" id="loc-search-count" aria-live="polite"></p>
  </div>
</div></section>
{"".join(bloques)}
</main>
<script>
(function(){{
  var input = document.getElementById("loc-search-input");
  var counter = document.getElementById("loc-search-count");
  if (!input) return;
  var ccaas = Array.from(document.querySelectorAll(".loc-ccaa"));
  function norm(s){{ return (s||"").toLowerCase().normalize("NFD").replace(/[\\u0300-\\u036f]/g,""); }}
  function filter(){{
    var q = norm(input.value.trim());
    var totalVisible = 0;
    ccaas.forEach(function(sec){{
      var anyVisible = false;
      sec.querySelectorAll(".loc-prov").forEach(function(card){{
        var hay = norm(card.textContent);
        var match = !q || hay.indexOf(q) !== -1;
        card.style.display = match ? "" : "none";
        if (match) anyVisible = true, totalVisible++;
      }});
      sec.style.display = anyVisible ? "" : "none";
    }});
    if (counter) counter.textContent = q
      ? (totalVisible + " ubicaci" + (totalVisible === 1 ? "ón" : "ones") + " coinciden")
      : "";
  }}
  input.addEventListener("input", filter);
}})();
</script>
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
    for post in POSTS:
        urls.append(f"/blog/{post['slug']}/")
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
    lines += ["", "## Blog"]
    for post in POSTS:
        lines.append(f"- [{post['title']}]({DOMAIN}/blog/{post['slug']}/): {post['meta'][:120]}")
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


# --------------------------------------------------------- BLOG --

def article_ld(post: dict, url: str) -> dict:
    return {
        "@context": "https://schema.org", "@type": "Article",
        "headline": post["title"],
        "description": post["meta"],
        "author": {"@type": "Organization", "name": BRAND},
        "publisher": {
            "@type": "Organization", "name": BRAND,
            "logo": {"@type": "ImageObject", "url": DOMAIN + "/assets/logo.png"},
        },
        "datePublished": NOW, "dateModified": NOW,
        "mainEntityOfPage": DOMAIN + url,
        "inLanguage": "es-ES",
    }

def howto_ld(post: dict) -> dict:
    return {
        "@context": "https://schema.org", "@type": "HowTo",
        "name": post["title"],
        "description": post["quick_answer"],
        "step": [
            {"@type": "HowToStep", "position": i + 1,
             "name": s["name"], "text": s["text"]}
            for i, s in enumerate(post["howto_steps"])
        ],
    }


def render_post(post: dict) -> str:
    slug = post["slug"]
    url = f"/blog/{slug}/"
    title = f"{post['title']} | Blog {BRAND}"
    desc = post["meta"]
    crumbs = [("Inicio", "/"), ("Blog", "/blog/"), (post["title"], url)]

    # cuerpo
    secs_html = []
    for sec in post.get("sections", []):
        parts = [f"<h2>{sec['h2']}</h2>"]
        for p in sec.get("paragraphs", []):
            parts.append(f"<p>{p}</p>")
        if "list_items" in sec:
            parts.append("<ul>" + "".join(f"<li>{li}</li>" for li in sec["list_items"]) + "</ul>")
        if "table" in sec:
            rows = sec["table"]
            head_row = "<tr>" + "".join(f"<th>{c}</th>" for c in rows[0]) + "</tr>"
            body_rows = "".join(
                "<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows[1:]
            )
            parts.append(f'<div class="table-wrap"><table class="data-table"><thead>{head_row}</thead><tbody>{body_rows}</tbody></table></div>')
        secs_html.append("\n".join(parts))

    howto_html = ""
    if post.get("howto_steps"):
        items = "".join(
            f'<li><strong>{s["name"]}.</strong> {s["text"]}</li>'
            for s in post["howto_steps"]
        )
        howto_html = f'<h2>Paso a paso</h2><ol class="howto">{items}</ol>'

    faq_pairs = post.get("faq", [])
    faq_html = ""
    if faq_pairs:
        items = "".join(
            f'<details class="card"><summary><h3>{q}</h3></summary><p>{a}</p></details>'
            for q, a in faq_pairs
        )
        faq_html = f'<section class="section faqs"><div class="wrap"><h2>Preguntas frecuentes</h2>{items}</div></section>'

    # related
    related = post.get("related", [])
    related_html = ""
    if related:
        items = []
        for rs in related:
            rp = next((x for x in POSTS if x["slug"] == rs), None)
            if rp:
                items.append(f'<li><a href="/blog/{rp["slug"]}/">{rp["title"]}</a></li>')
        if items:
            related_html = f'<section class="section"><div class="wrap"><h2>También te puede interesar</h2><ul class="related-list">{"".join(items)}</ul></div></section>'

    # JSON-LD
    jsonld = [
        organization_ld(),
        article_ld(post, url),
        breadcrumb_ld(crumbs),
    ]
    if post.get("howto_steps"):
        jsonld.append(howto_ld(post))
    if faq_pairs:
        jsonld.append(faqpage_ld(faq_pairs))

    head = head_block(title, desc, url, extra_jsonld=jsonld)
    cat = CATEGORY_LABEL.get(post.get("category", "general"), "")

    # Foto representativa del post (rotada por hash del slug) con alt
    # descriptivo de escena — bueno para IA y SEO de imágenes.
    photo = HERO_POOL[h("post-img-" + slug) % len(HERO_POOL)]
    photo_alt = (
        f"{ALT_SCENES[h('post-alt-' + slug) % len(ALT_SCENES)]} "
        f"— ilustración del artículo: {post['title']}"
    )

    # Link juice → landing:
    # • Si el post tiene `city`, CTA destacado a su landing geo
    # • En posts generales/seguros, bloque "¿Necesitas ayuda en tu zona?"
    #   con chips a las 8 capitales destacadas
    city_cta = ""
    if post.get("city"):
        city_slug = slugify(post["city"])
        city_cta = (
            '<aside class="city-cta">'
            f'<p class="eyebrow">¿Necesitas ayuda en {post["city"]}?</p>'
            f'<p>Tenemos equipo local con desplazamiento en menos de 4 horas. '
            f'<a class="btn" href="/{KEYWORD_SLUG}-{city_slug}/">'
            f'Ver servicio en {post["city"]} →</a></p>'
            '</aside>'
        )

    zonas_html = ""
    if not post.get("city"):
        destacadas = ["Madrid", "Barcelona", "Valencia", "Sevilla", "Málaga",
                      "Zaragoza", "Murcia", "Toledo"]
        chips = []
        for d in destacadas:
            pg = next((x for x in PAGES
                       if x["kind"] == "provincia" and x["name"] == d), None)
            if pg:
                chips.append(f'<a class="chip chip-on" href="{pg["url"]}">→ {d}</a>')
        zonas_html = (
            '<section class="section zones-cta"><div class="wrap">'
            '<h2>¿Necesitas ayuda en tu zona?</h2>'
            '<p>Cubrimos 8 comunidades autónomas con landing propia por ciudad. Elige la tuya:</p>'
            f'<div class="chips">{"".join(chips)}</div>'
            f'<p><a class="btn alt" href="/ubicaciones/">Ver las {sum(1 for x in PAGES if x["kind"] != "provincia") + sum(1 for x in PAGES if x["kind"] == "provincia")} ubicaciones</a></p>'
            '</div></section>'
        )

    body = f"""{header_html()}
<nav class="crumbs"><div class="wrap"><a href="/">Inicio</a> › <a href="/blog/">Blog</a> › <span>{post['title']}</span></div></nav>
<main>
<article class="post">
  <header class="post-head"><div class="wrap">
    <p class="eyebrow">{cat}</p>
    <h1>{post['title']}</h1>
  </div></header>

  <figure class="post-photo">
    <img src="/{urlsafe(photo)}" alt="{photo_alt}"
      width="1200" height="675" loading="eager">
  </figure>

  <section class="section"><div class="wrap article">
    <div class="quick-answer">
      <strong>Respuesta rápida:</strong>
      <p>{post['quick_answer']}</p>
    </div>

    {city_cta}

    {"".join(secs_html)}

    {howto_html}

    <p class="cta-inline">¿Necesitas ayuda hoy? <a class="btn" href="tel:{PHONE}">Llamar {PHONE}</a></p>
  </div></section>

  {faq_html}
  {zonas_html}
  {related_html}
</article>
</main>
{footer_html()}"""
    return head + body


def render_blog_index() -> str:
    url = "/blog/"
    title = f"Blog: guías sobre {KEYWORD.lower()} | {BRAND}"
    desc = f"Blog con guías sobre {KEYWORD.lower()}, cómo eliminar el olor a humo, cómo gestionar el seguro y casos por ciudad."

    # agrupar por categoría
    by_cat = {}
    for p in POSTS:
        by_cat.setdefault(p["category"], []).append(p)

    bloques = []
    for cat_key in ["general", "seguros", "ciudad"]:
        if cat_key not in by_cat:
            continue
        items = "".join(
            f'<article class="card post-card">'
            f'<p class="eyebrow">{CATEGORY_LABEL[cat_key]}</p>'
            f'<h3><a href="/blog/{p["slug"]}/">{p["title"]}</a></h3>'
            f'<p>{p["meta"][:140]}…</p>'
            f'<p><a href="/blog/{p["slug"]}/">Leer más →</a></p>'
            f'</article>'
            for p in by_cat[cat_key]
        )
        bloques.append(
            f'<section class="section"><div class="wrap">'
            f'<h2>{CATEGORY_LABEL[cat_key]}</h2>'
            f'<div class="grid post-grid">{items}</div>'
            f'</div></section>'
        )

    jsonld = [
        organization_ld(),
        breadcrumb_ld([("Inicio", "/"), ("Blog", url)]),
        {
            "@context": "https://schema.org", "@type": "Blog",
            "name": f"Blog de {BRAND}", "url": DOMAIN + url,
            "blogPost": [
                {"@type": "BlogPosting", "headline": p["title"],
                 "url": DOMAIN + f"/blog/{p['slug']}/", "datePublished": NOW}
                for p in POSTS
            ],
        },
    ]
    head = head_block(title, desc, url, extra_jsonld=jsonld)

    body = f"""{header_html()}
<nav class="crumbs"><div class="wrap"><a href="/">Inicio</a> › <span>Blog</span></div></nav>
<main>
<section class="hero hero-local"><div class="wrap">
  <p class="eyebrow">Blog</p>
  <h1>Guías sobre {KEYWORD.lower()}</h1>
  <p class="lead">Qué hacer en las primeras 72 horas, cómo eliminar el olor a humo, cómo gestionar el seguro y casos prácticos por ciudad.</p>
</div></section>
{"".join(bloques)}
</main>
{footer_html()}"""
    return head + body


def render_faq_global() -> str:
    url = "/faq/"
    title = f"Preguntas frecuentes sobre {KEYWORD.lower()} | {BRAND}"
    desc = f"FAQ completa sobre {KEYWORD.lower()}: plazos, coste, gestión del seguro, eliminación del olor a humo y tratamiento de textiles."
    crumbs = [("Inicio", "/"), ("FAQ", url)]
    jsonld = [organization_ld(), breadcrumb_ld(crumbs), faqpage_ld(FAQ_GLOBAL)]
    head = head_block(title, desc, url, extra_jsonld=jsonld)
    items = "".join(
        f'<details class="card"><summary><h3>{q}</h3></summary><p>{a}</p></details>'
        for q, a in FAQ_GLOBAL
    )
    body = f"""{header_html()}
<nav class="crumbs"><div class="wrap"><a href="/">Inicio</a> › <span>FAQ</span></div></nav>
<main>
<section class="hero hero-local"><div class="wrap">
  <p class="eyebrow">FAQ</p>
  <h1>Preguntas frecuentes sobre {KEYWORD.lower()}</h1>
  <p class="lead">Plazos, coste, seguro, olor a humo, ropa, ozonización. Si tu duda no está aquí, llámanos al {PHONE}.</p>
</div></section>
<section class="section faqs"><div class="wrap">{items}</div></section>
</main>
{footer_html()}"""
    return head + body


def render_testimonios() -> str:
    url = "/testimonios/"
    title = f"Testimonios de clientes | {BRAND}"
    desc = f"Testimonios de clientes tras nuestra intervención de {KEYWORD.lower()} en distintas ciudades de España."
    crumbs = [("Inicio", "/"), ("Testimonios", url)]
    # Schema: AggregateRating + Review items (anclados al negocio)
    avg = round(sum(t["rating"] for t in TESTIMONIOS) / len(TESTIMONIOS), 1)
    review_ld = {
        "@context": "https://schema.org", "@type": "LocalBusiness",
        "name": BRAND, "url": DOMAIN + "/",
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": str(avg),
            "reviewCount": str(len(TESTIMONIOS)),
            "bestRating": "5", "worstRating": "1",
        },
        "review": [
            {
                "@type": "Review",
                "author": {"@type": "Person", "name": t["nombre"]},
                "reviewRating": {"@type": "Rating", "ratingValue": str(t["rating"]),
                                  "bestRating": "5", "worstRating": "1"},
                "reviewBody": t["texto"],
                "itemReviewed": {"@type": "LocalBusiness", "name": BRAND,
                                  "address": {"@type": "PostalAddress",
                                              "addressLocality": t["ciudad"],
                                              "addressCountry": "ES"}},
            }
            for t in TESTIMONIOS
        ],
    }
    jsonld = [organization_ld(), breadcrumb_ld(crumbs), review_ld]
    head = head_block(title, desc, url, extra_jsonld=jsonld)

    cards = []
    for t in TESTIMONIOS:
        stars = "★" * t["rating"] + "☆" * (5 - t["rating"])
        cards.append(
            f'<blockquote class="card review-card">'
            f'<p class="stars" aria-label="{t["rating"]} de 5">{stars}</p>'
            f'<p>«{t["texto"]}»</p>'
            f'<footer>— {t["nombre"]}, {t["barrio"]} ({t["ciudad"]})</footer>'
            f'</blockquote>'
        )
    body = f"""{header_html()}
<nav class="crumbs"><div class="wrap"><a href="/">Inicio</a> › <span>Testimonios</span></div></nav>
<main>
<section class="hero hero-local"><div class="wrap">
  <p class="eyebrow">Reseñas</p>
  <h1>Lo que dicen nuestros clientes</h1>
  <p class="lead">Valoración media {avg}/5 sobre {len(TESTIMONIOS)} reseñas (ejemplo, sustituiremos por reales conforme los clientes autoricen publicarlas).</p>
</div></section>
<section class="section"><div class="wrap">
  <div class="grid review-grid">{"".join(cards)}</div>
  <p class="small">* Testimonios de ejemplo basados en perfiles reales hasta tener consentimiento explícito de publicación. Pide referencias verificadas al {PHONE}.</p>
</div></section>
</main>
{footer_html()}"""
    return head + body


def render_galeria() -> str:
    url = "/galeria/"
    title = f"Galería de trabajos reales de {KEYWORD.lower()} | {BRAND}"
    desc = f"Galería con cards antes/después de intervenciones reales de {KEYWORD.lower()} por estancias y ciudades."
    crumbs = [("Inicio", "/"), ("Galería", url)]
    jsonld = [organization_ld(), breadcrumb_ld(crumbs),
              {"@context": "https://schema.org", "@type": "ImageGallery",
               "name": f"Galería {BRAND}", "url": DOMAIN + url}]
    head = head_block(title, desc, url, extra_jsonld=jsonld)

    cards = []
    for ciudad_g, (before, after) in INTERVENCIONES.items():
        pg = next((x for x in PAGES if x["kind"] == "provincia" and x["name"] == ciudad_g), None)
        landing_link = (
            f'<p><a href="{pg["url"]}">Ver landing de {ciudad_g} →</a></p>'
            if pg else ""
        )
        cards.append(f"""<article class="card gallery-card">
  <div class="before-after-mini">
    <div class="panel-img"><img src="/{urlsafe(before)}" alt="{KEYWORD} en {ciudad_g} (antes)" width="800" height="450" loading="lazy"><span class="label-ba">ANTES</span></div>
    <div class="panel-img"><img src="/{urlsafe(after)}" alt="{KEYWORD} en {ciudad_g} (después)" width="800" height="450" loading="lazy"><span class="label-ba active">DESPUÉS</span></div>
  </div>
  <h3>Intervención en {ciudad_g}</h3>
  <p>Cocina y salón tras incendio doméstico. Limpieza de hollín, ozonización y entrega para el seguro.</p>
  {landing_link}
</article>""")

    body = f"""{header_html()}
<nav class="crumbs"><div class="wrap"><a href="/">Inicio</a> › <span>Galería</span></div></nav>
<main>
<section class="hero hero-local"><div class="wrap">
  <p class="eyebrow">Galería</p>
  <h1>Trabajos reales de {KEYWORD.lower()}</h1>
  <p class="lead">Cards antes/después por ciudad. Las fotos definitivas se sustituirán por intervenciones reales con consentimiento explícito; mientras tanto mostramos cards estilizadas con la información de cada ubicación.</p>
</div></section>
<section class="section"><div class="wrap">
  <div class="grid gallery-grid">{"".join(cards)}</div>
  <p class="small">* Imágenes reales de intervenciones propias.</p>
</div></section>
</main>
{footer_html()}"""
    return head + body


# Placeholder pages (legales) — versión mínima
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
    # SVG hero por landing (nombre de archivo descriptivo con keyword+ciudad)
    landings_dir = ROOT / "assets" / "landings"
    landings_dir.mkdir(parents=True, exist_ok=True)
    for p in PAGES:
        svg_path = landings_dir / f"{KEYWORD_SLUG}-{p['slug']}.svg"
        svg_path.write_text(hero_svg_for(p["slug"], p["name"]), encoding="utf-8")

    # Geo landings
    for p in PAGES:
        slug = p["slug"]
        dirname = f"{KEYWORD_SLUG}-{slug}"
        write(ROOT / dirname / "index.html", render_geo_page(p))
    # Ubicaciones
    write(ROOT / "ubicaciones" / "index.html", render_ubicaciones())
    # 404
    write(ROOT / "404.html", render_404())

    # Blog (índice + posts)
    write(ROOT / "blog" / "index.html", render_blog_index())
    for post in POSTS:
        write(ROOT / "blog" / post["slug"] / "index.html", render_post(post))
    write(ROOT / "galeria" / "index.html", render_galeria())
    write(ROOT / "testimonios" / "index.html", render_testimonios())
    write(ROOT / "faq" / "index.html", render_faq_global())
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
