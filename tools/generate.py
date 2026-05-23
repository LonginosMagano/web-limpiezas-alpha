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


# Plantillas de anchor para variar el texto de los enlaces de localidad.
# Se selecciona uno por hash(origen+destino) para diversificar sin caos.
ANCHOR_TEMPLATES = [
    "{ciudad}",
    "{keyword} en {ciudad}",
    "empresa de limpieza tras incendio en {ciudad}",
    "limpieza profesional en {ciudad}",
    "limpieza de hollín en {ciudad}",
    "servicio en {ciudad}",
    "limpieza post incendio en {ciudad}",
    "atendemos en {ciudad}",
    "hollín, humo y olor en {ciudad}",
]

def anchor_for(origen_slug: str, dst_slug: str, ciudad: str) -> str:
    """Texto de anchor variado pero determinista por par (origen, destino)."""
    idx = h(f"a-{origen_slug}->{dst_slug}") % len(ANCHOR_TEMPLATES)
    return ANCHOR_TEMPLATES[idx].format(keyword=KEYWORD, ciudad=ciudad)


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
  <a class="brand-row" href="/"><img class="logo-img" src="/assets/logo.webp" alt="{BRAND}" width="140" height="70" loading="eager"><span class="logo-text">{BRAND}</span></a>
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
    <a class="brand-row" href="/"><img class="logo-img" src="/assets/logo.webp" alt="{BRAND}" width="140" height="70" loading="eager"><span class="logo-text">{BRAND}</span></a>
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
        "logo": DOMAIN + "/assets/logo.webp",
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
     "Depende del tamaño y del tipo de fuego. Una cocina pequeña suele estar lista en dos o tres días. Un piso completo, entre cinco y diez. Un local o nave, según la superficie y lo que ardiera dentro. Tras la primera visita le damos un plazo firme, no “depende”."),
    ("¿Trabajáis con todas las compañías de seguros?",
     "Con todas. Preparamos la documentación en el formato que pide cada perito: memoria, fotos antes y después, desglose por estancias y, si lo solicita, certificado de descontaminación. Las grandes (Mapfre, Mutua Madrileña, AXA, Aegon) la han aceptado sin pegas."),
    ("¿Cuánto cuesta?",
     "Lo decimos en cifras orientativas, porque el precio real lo damos tras la visita. Una cocina pequeña suele estar entre 800 y 1.500 euros. Un piso completo, entre 2.500 y 8.000. Locales y naves van por superficie. Si lo cubre su seguro, gestionamos el cobro con la compañía."),
    ("¿Hace falta sacar las cosas antes de que vengáis?",
     "No, mejor no toque nada. Cuanto menos se mueva antes de la primera valoración, mejor para el seguro. Subimos, fotografiamos, protegemos lo que no va a tocarse y empezamos. Lo que haya que retirar lo inventariamos pieza a pieza."),
    ("¿Eliminar el olor a humo está incluido?",
     "Sí. Tras la limpieza física hacemos ozonización o tratamiento con hidroxilo en cada estancia. Y si pasadas 48 horas detecta cualquier olor residual, volvemos sin cobrar. Forma parte del trato."),
    ("¿Limpiáis ropa, cortinas y sofás?",
     "Sí, pero por separado del trabajo de obra. Lo recogemos, lo inventariamos y lo enviamos a un proceso especializado. La tintorería normal no vale: usa percloroetileno y fija el olor para siempre. Lo que se recupera vuelve sin olor; lo que no, queda documentado para el seguro."),
    ("¿Trabajáis solo en grandes siniestros?",
     "No. La mitad de los avisos que recibimos son cocinas pequeñas: una freidora, un cargador que se quemó por la noche. El proceso técnico es exactamente el mismo, solo cambia el tiempo de trabajo. No descartamos a nadie por tamaño."),
    ("¿En cuánto tiempo podéis estar en mi vivienda?",
     "Si nos llama antes de las seis de la tarde, normalmente vamos al día siguiente. Muchas veces, si la cosa es seria, la misma tarde. Las primeras 72 horas son las críticas para que el hollín no se fije, así que cuanto antes nos avise, mejor para usted."),
    ("¿Qué pasa si el seguro no cubre la limpieza?",
     "Lo planificamos por fases. Primero lo crítico (cocina, baño, zona habitable) para que pueda volver a vivir. Lo estético, en una segunda etapa. Si la denegación nos parece injusta, le orientamos para presentar reclamación al servicio de atención al cliente de la aseguradora."),
    ("¿Puedo dormir en la vivienda mientras se limpia?",
     "Mejor no, sobre todo en los primeros días. El hollín suelto y los productos no son amigables con la presencia continua, y la ozonización exige espacio cerrado sin personas ni mascotas dentro. Salvo en intervenciones muy pequeñas, no es buena idea."),
    ("¿Hacéis también reformas o pintura?",
     "No. Solo limpieza y descontaminación tras incendio. Si una pared está calcinada y hay que tirarla, le indicamos qué reformista puede hacerlo. Cuando termine la obra, volvemos a entregar todo limpio. Cada cosa con su especialista."),
    ("¿Tenéis seguro de responsabilidad civil propio?",
     "Sí. Toda nuestra actividad está cubierta con póliza de responsabilidad civil profesional. Si su aseguradora pide acreditación, se la enviamos en el momento, sin trámites."),
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

    # Foto hero con variedad real:
    #  - Las 8 capitales (Madrid, BCN, etc.) → su par único en INTERVENCIONES.
    #  - Todo el resto (municipios, barrios, otras provincias) → ciclar por
    #    hash en HERO_POOL filtrando las fotos que ya identifican a una
    #    capital, para que ninguna landing repita la foto de una capital.
    intervenciones_heroes = {pair[1] for pair in INTERVENCIONES.values()}
    pool_libre = [f for f in HERO_POOL if f not in intervenciones_heroes]
    if ciudad in INTERVENCIONES and p["kind"] == "provincia":
        hero_photo = INTERVENCIONES[ciudad][1]
    else:
        hero_photo = pool_libre[h("hero-" + slug) % len(pool_libre)] if pool_libre else HERO_POOL[h("hero-" + slug) % len(HERO_POOL)]

    fmt = dict(keyword=KEYWORD, kw_var=kw_var, ciudad=ciudad,
               provincia=provincia, brand=BRAND, phone=PHONE)

    title = title_t.format(**fmt)
    desc = meta_t.format(**fmt)
    h1 = h1_t.format(**fmt)

    # ---- intro (la keyword principal en los primeros 100 caracteres) ----
    # Rotamos 6 leads narrativos por hash(slug) para que ninguna landing
    # repita el mismo arranque que su vecina.
    INTRO_LEADS = [
        (f"{KEYWORD} en {ciudad}: limpiamos el hollín, retiramos el humo y "
         f"borramos el olor a quemado en viviendas y locales de {ciudad}. "
         f"Si llama hoy, esa misma tarde podemos estar allí mirando."),
        (f"{KEYWORD} en {ciudad}. Quitamos el hollín de paredes, techos y "
         f"muebles, tratamos el olor a humo en cada estancia y le ahorramos "
         f"el papeleo del seguro. Vamos al día siguiente, sin promesas raras."),
        (f"{KEYWORD} en {ciudad}: pisos, locales, naves. Las primeras 72 "
         f"horas son las que mandan. Subimos, valoramos sin compromiso y le "
         f"damos presupuesto cerrado antes de tocar nada."),
        (f"{KEYWORD} en {ciudad} y los pueblos de alrededor. No reformamos. "
         f"No pintamos. Solo limpiamos y descontaminamos tras incendio. Eso, "
         f"sí, lo hacemos bien y por escrito para que el seguro lo cobre."),
        (f"{KEYWORD} en {ciudad}: el equipo que mira es el mismo que limpia "
         f"y el mismo que firma la memoria final. Sin subcontratas, sin "
         f"intermediarios, sin teléfono escacharrado. Llámenos."),
        (f"{KEYWORD} en {ciudad}. Hollín, humo y olor a quemado se quitan "
         f"con paciencia y método, no con un trapo y un ambientador. Por "
         f"eso, antes de tocar la pared, llámenos y véngale a echar un ojo."),
    ]
    intro = INTRO_LEADS[h("intro-" + slug) % len(INTRO_LEADS)]

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
                anchor = anchor_for(slug, pg["slug"], m)
                chips.append(f'<a class="chip chip-on" href="{pg["url"]}">{anchor}</a>')
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
                    anchor = anchor_for(slug, pg["slug"], f"barrio {b}")
                    barrio_chips.append(f'<a class="chip chip-on" href="{pg["url"]}">{anchor}</a>')
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
            anchor = anchor_for(slug, provincia_page["slug"], provincia)
            bits.append(f'<a class="chip chip-on" href="{provincia_page["url"]}">{anchor}</a>')
        sib = [x for x in PAGE_BY_PROV.get(provincia, [])
               if x["slug"] != slug and x["kind"] != "provincia"][:8]
        for x in sib:
            anchor = anchor_for(slug, x["slug"], x["name"])
            bits.append(f'<a class="chip chip-on" href="{x["url"]}">{anchor}</a>')
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
            anchor = anchor_for(slug + "-sb", pg["slug"], pg["name"])
            sidebar_links.append(f'<a href="{pg["url"]}">{anchor}</a>')
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
                anchor = anchor_for(slug + "-c", ppage["slug"], prov)
                cercanas.append(f'<a href="{ppage["url"]}">{anchor}</a>')
    cercanas = cercanas[:8]

    # Sidebar extra: "Otros barrios" cuando estamos en una landing de barrio
    sidebar_barrios = ""
    if p["kind"] == "barrio":
        otros_b = []
        for x in PAGES:
            if x["kind"] == "barrio" and x["slug"] != slug:
                anchor = anchor_for(slug + "-bb", x["slug"], f"barrio {x['name']}")
                otros_b.append(f'<a href="{x["url"]}">{anchor}</a>')
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

    # ---- párrafo contextual con enlaces inline naturales ----
    # Anchors variados por hash(slug) para no clonar entre landings.
    contextual_pool = [
        ('cómo actuar en las primeras 72 horas', '/blog/que-hacer-despues-de-un-incendio/'),
        ('eliminar el olor a humo paso a paso', '/blog/como-eliminar-olor-humo/'),
        ('limpiar el hollín sin fijar la mancha', '/blog/limpieza-hollin-paredes/'),
        ('cuánto cuesta una limpieza tras incendio', '/blog/cuanto-cuesta-limpieza-tras-incendio/'),
        ('qué pide el perito del seguro', '/blog/documentacion-perito-seguros/'),
        ('cómo reclamar al seguro', '/blog/como-reclamar-seguro-incendio/'),
        ('cómo evitar que el hollín se fije', '/blog/como-evitar-que-hollin-se-fije/'),
        ('qué hacer con la ropa con olor a humo', '/blog/que-hago-con-la-ropa-con-olor-a-humo/'),
        ('cuánto tarda en limpiarse una casa', '/blog/cuanto-tarda-limpiarse-casa-tras-incendio/'),
        ('necesito vaciar mi piso tras el incendio', '/blog/necesito-vaciar-piso-tras-incendio/'),
    ]
    # 3 enlaces curados por hash(slug), distintos entre sí
    picked = []
    for i in range(3):
        idx = (h("ctx-" + slug) + i * 4) % len(contextual_pool)
        if contextual_pool[idx] not in picked:
            picked.append(contextual_pool[idx])
    # Frase con anchor variado hacia el servicio madre
    servicio_anchor = ANCHOR_TEMPLATES[h("serv-" + slug) % len(ANCHOR_TEMPLATES)].format(
        keyword=KEYWORD, ciudad=ciudad
    )
    contextual = (
        f'<p>Si quieres profundizar antes de llamar, lee '
        f'<a href="{picked[0][1]}">{picked[0][0]}</a>, '
        f'<a href="{picked[1][1]}">{picked[1][0]}</a> o '
        f'<a href="{picked[2][1]}">{picked[2][0]}</a>. '
        f'También puedes ver el detalle de <a href="/servicios/limpieza-tras-incendio/">'
        f'{servicio_anchor}: qué incluye y qué no</a>, y echarle un ojo a la '
        f'<a href="/galeria/">galería de trabajos reales antes y después</a>.</p>'
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
        alt="{KEYWORD} en {ciudad}: {ALT_SCENES[h('alt-' + slug) % len(ALT_SCENES)].lower()} ({kw_var}, {provincia})"
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
  <p class="faq-more"><a href="/faq/">Ver todas las preguntas frecuentes →</a> · <a href="/testimonios/">Ver reseñas de clientes →</a> · <a href="/blog/">Ir al blog completo →</a></p>
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
         "Depende del tamaño y del tipo de fuego. Una cocina pequeña suele estar lista en dos o tres días. Un piso completo, entre cinco y diez. Un local o nave, según la superficie y lo que se haya quemado dentro. Tras la primera visita le damos plazo cerrado, no “depende”."),
        ("¿Trabajáis con todas las compañías de seguros?",
         "Sí. Preparamos la documentación en el formato que pide cada perito: memoria con fotos antes y después, desglose por estancias e inventario de lo perdido. Si la aseguradora pone trabas, hablamos directamente con ellos. Las grandes ―Mapfre, Mutua, AXA, Aegon― la han aceptado sin pegas."),
        ("¿Hace falta sacar las cosas antes de que vengáis?",
         "No, mejor no toque nada. Cuanto menos se mueva antes de la valoración, mejor para el seguro. Llegamos, fotografiamos, protegemos lo que no va a tocarse y empezamos. Lo que haya que retirar lo inventariamos pieza a pieza."),
        ("¿Eliminar el olor a humo está incluido?",
         "Sí, siempre. Tras la limpieza física hacemos ozonización o tratamiento con hidroxilo en cada estancia. Si pasadas 48 horas detecta cualquier olor residual, volvemos sin cobrar. Forma parte del trato, no es una cláusula."),
        ("¿Trabajáis solo en grandes incendios?",
         "No. La mitad de los avisos que nos llegan son cocinas pequeñas: una freidora, una vela olvidada, un cargador que se quemó por la noche. El proceso técnico es el mismo, solo cambia el tiempo."),
        ("¿Cuánto cuesta?",
         "La visita técnica es gratuita y sin compromiso. Subimos, miramos, le explicamos lo que vamos a hacer y le damos presupuesto cerrado antes de empezar. Si lo cubre su seguro, gestionamos el cobro con la compañía y a usted le ahorramos el papeleo."),
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
      <p class="lead">Tras un incendio, lo último que necesita es lidiar con bayetas, ambientadores y peritos. Subimos a su casa o local, miramos en serio lo que ha pasado y empezamos a trabajar. La memoria para el seguro la entregamos nosotros. Usted descansa.</p>
      <img class="hero-img" src="/{urlsafe(HERO_POOL[0])}" alt="Operario de Limpiezas de Incendios Alpha retirando hollín de una pared tras un incendio doméstico" width="800" height="450" loading="eager">
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
    <article class="card"><p class="eyebrow">01</p><h3>Hollín y humo</h3><p>Lo retiramos por capas, primero en seco. Si pasamos un trapo húmedo el primer día, la mancha se queda en el yeso. Por eso vamos despacio y con método.</p></article>
    <article class="card"><p class="eyebrow">02</p><h3>Olor a quemado</h3><p>Ozonización o hidroxilo en cada estancia, hasta que la nariz no encuentra nada. Si a las 48 horas vuelve a oler, regresamos sin cobrar.</p></article>
    <article class="card"><p class="eyebrow">03</p><h3>Cocina incendiada</h3><p>Desengrasamos campana, muebles altos, techos y azulejos. Lo que se recupera, vuelve a estar útil. Lo que no, le decimos qué reformista lo arregla.</p></article>
    <article class="card"><p class="eyebrow">04</p><h3>Vivienda quemada</h3><p>Trabajamos por estancias. Primero cocina y baño, después dormitorios, al final el resto. Para que vuelva a dormir en casa antes de lo que cree.</p></article>
  </div>
</div></section>

<section class="section critical"><div class="wrap critical-stack">
  <article class="critical-text">
    <p class="eyebrow">Primeras 72 horas</p>
    <h2>El hollín es ácido. Y tiene prisa.</h2>
    <p>En las primeras horas tras un incendio, los restos de combustión empiezan a meterse dentro del yeso, del papel, de la ropa que estaba en el armario cerrado. Pase tres días sin tratar la vivienda y el olor ya no se va con productos normales: hay que arrancarlo. Por eso lo razonable es llamar pronto, aunque sea solo para que pasemos a echar un vistazo y valorar.</p>
    <p><a class="btn" href="/servicios/limpieza-tras-incendio/">Ver el servicio detallado</a></p>
  </article>
  <figure class="stone-wall-figure">
    <img src="/assets/limpieza-pared-piedra-hollin-chimenea.webp"
      alt="Limpieza despues de incendio: pared de piedra natural cubierta de hollín durante el proceso de descontaminación profesional. A la derecha la zona ya tratada, a la izquierda todavía con la capa de carbón ácido por retirar."
      width="800" height="1000" loading="lazy">
    <figcaption>Antes y durante, en la misma pared: la limpieza del hollín avanza por zonas.</figcaption>
  </figure>
</div></section>

<section class="section"><div class="wrap">
  <h2>Provincias destacadas donde operamos</h2>
  <div class="chips">{dest_html}</div>
  <p><a class="btn alt" href="/ubicaciones/">Ver todas las ubicaciones</a></p>
</div></section>

<section class="section faqs"><div class="wrap">
  <h2>Preguntas frecuentes</h2>
  {home_faq_html}
  <p class="faq-more"><a href="/faq/">Ver todas las preguntas frecuentes →</a></p>
</div></section>

<section class="section guias-blog"><div class="wrap">
  <h2>Guías del blog</h2>
  <p>Lo que más se busca: cómo eliminar el olor a humo, qué hacer en las primeras 72h, cuánto cuesta una limpieza tras incendio, qué pide el perito del seguro.</p>
  <div class="grid guias-grid">
    <a class="card guia-card" href="/blog/que-hacer-despues-de-un-incendio/"><span class="eyebrow">Guía</span><h3>Qué hacer después de un incendio en casa</h3><span class="ver-mas">Leer →</span></a>
    <a class="card guia-card" href="/blog/como-eliminar-olor-humo/"><span class="eyebrow">Guía</span><h3>Cómo eliminar el olor a humo</h3><span class="ver-mas">Leer →</span></a>
    <a class="card guia-card" href="/blog/cuanto-cuesta-limpieza-tras-incendio/"><span class="eyebrow">Guía</span><h3>Cuánto cuesta una limpieza tras incendio</h3><span class="ver-mas">Leer →</span></a>
    <a class="card guia-card" href="/blog/seguro-cubre-limpieza-incendio/"><span class="eyebrow">Seguros</span><h3>¿La limpieza tras incendio la cubre el seguro?</h3><span class="ver-mas">Leer →</span></a>
  </div>
  <p style="margin-top:18px"><a class="btn alt" href="/blog/">Ver las 21 guías del blog →</a></p>
</div></section>

<section class="section video-teaser"><div class="wrap">
  <p class="eyebrow">En movimiento</p>
  <h2>Mira a nuestro equipo trabajando</h2>
  <p>50 segundos de intervención real en una vivienda particular: hollín y olor a humo fuera, sin trucos de cámara.</p>
  <a class="video-teaser-thumb" href="/galeria/#video" aria-label="Ver vídeo de intervención real">
    <img src="/assets/intervencion-limpieza-poster.webp"
      alt="Fotograma del vídeo de intervención: equipo de Limpiezas de Incendios Alpha retirando hollín en una vivienda particular"
      width="720" height="1280" loading="lazy">
    <span class="play-icon" aria-hidden="true">▶</span>
    <span class="video-duration">0:50</span>
  </a>
</div></section>

<section class="section"><div class="wrap" style="text-align:center">
  <p class="eyebrow">Reseñas reales</p>
  <h2>Lo que dicen nuestros clientes</h2>
  <p>Valoración media 4.9/5 sobre intervenciones en vivienda, local y comunidad.</p>
  <p><a class="btn alt" href="/testimonios/">Ver testimonios →</a></p>
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
      <p class="lead">Esto es lo único que hacemos: limpiar y descontaminar viviendas, locales y naves tras un incendio. No reformamos paredes, no reparamos electrodomésticos, no echamos pintura nueva. Cada cosa con su especialista. Lo nuestro es el hollín, el olor a humo y la memoria para el seguro.</p>
      <div class="cta-row">
        <a class="btn" href="tel:{PHONE}">Llamar {PHONE}</a>
        <a class="btn alt" href="https://wa.me/{PHONE_INTL}">WhatsApp</a>
      </div>
    </div>
    {form_block(url)}
  </div>
</section>

<section class="section"><div class="wrap article">
  <h2>Qué hay dentro del precio</h2>
  <ul>
    <li><strong>Subimos a verlo, gratis.</strong> Sin compromiso. Si no contrata, no pasa nada.</li>
    <li><strong>Hacemos la documentación previa</strong>: fotos por estancias, descripción del daño y plan de actuación por escrito.</li>
    <li><strong>Limpieza de hollín por capas</strong>: techos, paredes y suelos. Cambia el método según se quemara aceite, plástico o cuadro eléctrico. Nuestro técnico lo ve al pasar la mano.</li>
    <li><strong>Olor a humo</strong>: ozonización o hidroxilo en cada estancia hasta que la nariz no encuentra nada.</li>
    <li><strong>Cocinas incendiadas</strong>: desengrasamos campana, muebles altos, baldas, exteriores de electrodomésticos y azulejos.</li>
    <li><strong>Textiles aparte</strong>: ropa, cortinas, sofás, alfombras. Inventario pieza a pieza y proceso especializado, nunca en tintorería normal.</li>
    <li><strong>Memoria final para el seguro</strong>: fotos antes y después, desglose por estancia y resumen ejecutivo que el perito lee en diez minutos.</li>
  </ul>

  <h2>Lo que no hacemos (y le decimos quién sí)</h2>
  <p>Hay tres cosas que no son lo nuestro, y preferimos decirlas claras antes de empezar.</p>
  <ul>
    <li>No reformamos ni pintamos. Si una pared está calcinada hay que tirarla y reponerla; le indicamos qué reformista o pintor lo hace. Cuando termine, volvemos a entregar todo limpio.</li>
    <li>No reparamos electrodomésticos. Limpiamos el exterior y dejamos los aparatos para que los revise el SAT correspondiente. Tocarlos antes invalida la garantía.</li>
    <li>No hacemos peritaciones de seguro. Eso es trabajo del perito de la compañía. Lo que sí hacemos es entregarle la documentación tan bien preparada que su trabajo se reduce a la mitad.</li>
  </ul>

  <h2>Las primeras 72 horas</h2>
  <p>El hollín tras un incendio es ácido. En las primeras horas empieza a meterse en el yeso, en la madera, en el textil del armario cerrado. En 48 ó 72 horas más empieza a corroer metales, daña la electrónica que estaba dentro y fija un olor que ya no se va con limpieza normal. Cuanto antes intervenimos, menos pierde el seguro y menos se desgasta usted.</p>

  <h2>Cómo trabajamos, paso a paso</h2>
  <ol>
    <li><strong>Llamada</strong>. Marca el {PHONE} o nos escribe por WhatsApp. Le contestamos en menos de una hora durante el día.</li>
    <li><strong>Visita técnica</strong>. Subimos, miramos y fotografiamos. Sin compromiso. Sin coste.</li>
    <li><strong>Presupuesto cerrado</strong>. Nada de “depende”: cifra firme, plazo firme.</li>
    <li><strong>Limpieza por estancias</strong>. Primero lo crítico para que pueda volver a vivir antes. El resto, en orden.</li>
    <li><strong>Entrega</strong>. Comprobamos olor con medidor en cada habitación, fotos finales y memoria en PDF.</li>
    <li><strong>Garantía</strong>. Si en las 48 horas siguientes detecta cualquier olor residual, volvemos sin cobrar.</li>
  </ol>

  <p><a class="btn" href="tel:{PHONE}">Llamar {PHONE}</a></p>
</div></section>

<section class="section"><div class="wrap">
  <h2>¿Dónde damos servicio?</h2>
  <p>Atendemos en 8 comunidades autónomas, con landing propia por capital y municipios principales. Algunas ubicaciones destacadas:</p>
  <div class="chips">
    <a class="chip chip-on" href="/limpieza-despues-de-incendio-madrid/">Limpieza tras incendio en Madrid</a>
    <a class="chip chip-on" href="/limpieza-despues-de-incendio-barcelona/">Empresa de limpieza en Barcelona</a>
    <a class="chip chip-on" href="/limpieza-despues-de-incendio-valencia/">Limpieza profesional en Valencia</a>
    <a class="chip chip-on" href="/limpieza-despues-de-incendio-sevilla/">Hollín, humo y olor en Sevilla</a>
    <a class="chip chip-on" href="/limpieza-despues-de-incendio-malaga/">Servicio en Málaga</a>
    <a class="chip chip-on" href="/limpieza-despues-de-incendio-zaragoza/">Limpieza post incendio en Zaragoza</a>
    <a class="chip chip-on" href="/limpieza-despues-de-incendio-murcia/">Atendemos en Murcia</a>
    <a class="chip chip-on" href="/limpieza-despues-de-incendio-toledo/">Limpieza de hollín en Toledo</a>
  </div>
  <p><a class="btn alt" href="/ubicaciones/">Ver las 113 ubicaciones</a></p>
</div></section>

<section class="section guias-blog"><div class="wrap">
  <h2>Antes de llamarnos, quizá te sirva leer</h2>
  <div class="grid guias-grid">
    <a class="card guia-card" href="/blog/que-hacer-despues-de-un-incendio/"><span class="eyebrow">Guía</span><h3>Qué hacer después de un incendio</h3><span class="ver-mas">Leer →</span></a>
    <a class="card guia-card" href="/blog/como-eliminar-olor-humo/"><span class="eyebrow">Guía</span><h3>Cómo eliminar el olor a humo</h3><span class="ver-mas">Leer →</span></a>
    <a class="card guia-card" href="/blog/cuanto-cuesta-limpieza-tras-incendio/"><span class="eyebrow">Guía</span><h3>Cuánto cuesta</h3><span class="ver-mas">Leer →</span></a>
    <a class="card guia-card" href="/blog/documentacion-perito-seguros/"><span class="eyebrow">Seguros</span><h3>Qué pide el perito tras un incendio</h3><span class="ver-mas">Leer →</span></a>
  </div>
  <p><a href="/faq/">Ver FAQ completa →</a> · <a href="/testimonios/">Ver testimonios →</a> · <a href="/galeria/">Galería de intervenciones →</a></p>
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
  <p class="lead">Atendemos en {len(CCAA)} comunidades autónomas, con landing propia por provincia, principales municipios y barrios. Antes de elegir tu ciudad puedes mirar <a href="/servicios/limpieza-tras-incendio/">qué incluye nuestro servicio</a> y <a href="/galeria/">ver trabajos reales antes/después</a>.</p>
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
            "logo": {"@type": "ImageObject", "url": DOMAIN + "/assets/logo.webp"},
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
            f'Mira <a href="/{KEYWORD_SLUG}-{city_slug}/">'
            f'la landing de {post["city"]} con FAQ específica</a> '
            f'o consulta <a href="/servicios/limpieza-tras-incendio/">'
            f'qué incluye nuestro servicio</a>.</p>'
            f'<p><a class="btn" href="/{KEYWORD_SLUG}-{city_slug}/">'
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
                anchor = anchor_for("post-" + slug, pg["slug"], d)
                chips.append(f'<a class="chip chip-on" href="{pg["url"]}">{anchor}</a>')
        zonas_html = (
            '<section class="section zones-cta"><div class="wrap">'
            '<h2>¿Necesitas ayuda en tu zona?</h2>'
            '<p>Cubrimos 8 comunidades autónomas con landing propia por ciudad. '
            'Si quieres entender antes <a href="/servicios/limpieza-tras-incendio/">qué incluye y qué no nuestro servicio de limpieza tras incendio</a>, mira la página del servicio. Para una valoración real, elige tu zona:</p>'
            f'<div class="chips">{"".join(chips)}</div>'
            f'<p><a class="btn alt" href="/ubicaciones/">Ver las {len(PAGES)} ubicaciones</a></p>'
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

<section class="section cta-band"><div class="wrap" style="text-align:center">
  <h2>¿Tu duda sigue sin resolverse?</h2>
  <p>Llámanos y te respondemos al momento, sin compromiso.</p>
  <div class="cta-row" style="justify-content:center">
    <a class="btn" href="tel:{PHONE}">Llamar {PHONE}</a>
    <a class="btn alt" href="https://wa.me/{PHONE_INTL}">WhatsApp</a>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <h2>Cobertura por ciudad</h2>
  <div class="chips">
    <a class="chip chip-on" href="/limpieza-despues-de-incendio-madrid/">Madrid</a>
    <a class="chip chip-on" href="/limpieza-despues-de-incendio-barcelona/">Barcelona</a>
    <a class="chip chip-on" href="/limpieza-despues-de-incendio-valencia/">Valencia</a>
    <a class="chip chip-on" href="/limpieza-despues-de-incendio-sevilla/">Sevilla</a>
    <a class="chip chip-on" href="/limpieza-despues-de-incendio-malaga/">Málaga</a>
    <a class="chip chip-on" href="/limpieza-despues-de-incendio-zaragoza/">Zaragoza</a>
    <a class="chip chip-on" href="/limpieza-despues-de-incendio-murcia/">Murcia</a>
    <a class="chip chip-on" href="/limpieza-despues-de-incendio-toledo/">Toledo</a>
  </div>
  <p><a href="/ubicaciones/">Ver las 113 ubicaciones →</a> · <a href="/servicios/limpieza-tras-incendio/">El servicio explicado →</a> · <a href="/blog/">Blog completo →</a></p>
</div></section>
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

<section class="section guias-blog"><div class="wrap">
  <h2>Lo más leído del blog</h2>
  <div class="grid guias-grid">
    <a class="card guia-card" href="/blog/que-hacer-despues-de-un-incendio/"><span class="eyebrow">Guía</span><h3>Qué hacer después de un incendio</h3><span class="ver-mas">Leer →</span></a>
    <a class="card guia-card" href="/blog/como-eliminar-olor-humo/"><span class="eyebrow">Guía</span><h3>Cómo eliminar el olor a humo</h3><span class="ver-mas">Leer →</span></a>
    <a class="card guia-card" href="/blog/seguro-cubre-limpieza-incendio/"><span class="eyebrow">Seguros</span><h3>¿La limpieza la cubre el seguro?</h3><span class="ver-mas">Leer →</span></a>
    <a class="card guia-card" href="/galeria/"><span class="eyebrow">Galería</span><h3>Trabajos reales antes/después</h3><span class="ver-mas">Ver →</span></a>
  </div>
  <p><a href="/blog/">Ver las 21 guías del blog →</a> · <a href="/faq/">FAQ completa →</a> · <a href="/ubicaciones/">Cobertura por ciudad →</a></p>
</div></section>

<section class="section cta-band"><div class="wrap" style="text-align:center">
  <h2>¿Has tenido un incendio?</h2>
  <p>Te valoramos hoy mismo, sin compromiso.</p>
  <div class="cta-row" style="justify-content:center">
    <a class="btn" href="tel:{PHONE}">Llamar {PHONE}</a>
    <a class="btn alt" href="https://wa.me/{PHONE_INTL}">WhatsApp</a>
  </div>
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
               "name": f"Galería {BRAND}", "url": DOMAIN + url},
              {"@context": "https://schema.org", "@type": "VideoObject",
               "name": f"Intervención real de {KEYWORD.lower()}",
               "description": (f"Vídeo de una intervención real de "
                               f"{KEYWORD.lower()} en una vivienda particular: "
                               f"limpieza profesional de hollín, humo y olor."),
               "thumbnailUrl": DOMAIN + "/assets/intervencion-limpieza-poster.webp",
               "contentUrl": DOMAIN + "/assets/intervencion-limpieza-tras-incendio-720.mp4",
               "uploadDate": "2026-05-23",
               "duration": "PT50S"}]
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
  <p class="lead">Cards antes/después por ciudad de intervenciones reales de nuestro equipo. Si quieres entender <a href="/servicios/limpieza-tras-incendio/">qué incluye nuestro servicio paso a paso</a> o <a href="/ubicaciones/">en qué ciudades operamos</a>, los tienes a un clic.</p>
</div></section>
<section class="section"><div class="wrap">
  <div class="grid gallery-grid">{"".join(cards)}</div>
  <p class="small">* Imágenes reales de intervenciones propias.</p>
</div></section>

<section class="section video-section" id="video"><div class="wrap">
  <p class="eyebrow">En movimiento</p>
  <h2>Mira cómo trabajamos</h2>
  <p>Fragmento real de una intervención de limpieza tras incendio: hollín y restos de combustión retirados de paredes, suelos y mobiliario con el equipo en marcha. Sin escenografía. Sin truco de montaje.</p>
  <figure class="intervention-video">
    <video controls preload="none" playsinline
      poster="/assets/intervencion-limpieza-poster.webp"
      width="720" height="1280"
      aria-label="Vídeo de intervención real de limpieza tras incendio">
      <source src="/assets/intervencion-limpieza-tras-incendio.webm" type="video/webm">
      <source src="/assets/intervencion-limpieza-tras-incendio-720.mp4" type="video/mp4">
      Tu navegador no soporta vídeo HTML5. <a href="/assets/intervencion-limpieza-tras-incendio-720.mp4">Descarga el archivo</a>.
    </video>
    <figcaption>Intervención real de {KEYWORD.lower()} grabada en una vivienda particular.</figcaption>
  </figure>
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
