# SEO Playbook — Webs de servicio local (Grupo Fénix)

> **Qué es esto**: la lista de requisitos y plantillas que hacen posicionar a
> `limpiezapostincendio.es`. Es **portátil**: cópialo a cualquier otra web del
> grupo y aplícalo punto por punto. Los textos entre `{{...}}` son placeholders
> que debes sustituir por los datos de cada marca.
>
> **Cómo usarlo**: recórrelo de arriba abajo. Cada sección tiene (1) el porqué,
> (2) la casilla de verificación y (3) la plantilla de código lista para pegar.

---

## 0. Variables de la marca (rellenar una vez por web)

| Variable | Ejemplo (referencia) | Tu web |
|---|---|---|
| `{{DOMINIO}}` | `https://limpiezapostincendio.es` | |
| `{{MARCA}}` | `Limpieza Post Incendio` | |
| `{{TELEFONO}}` | `+34 624 03 16 61` | |
| `{{EMAIL}}` | `info@limpiezapostincendio.es` | |
| `{{KEYWORD}}` | `limpieza post incendio` | |
| `{{SLUG_LOCAL}}` | `limpieza-incendios-{{poblacion}}` | |
| `{{AUTOR}}` | `David Carrasco Méndez` | |
| `{{AUTOR_SLUG}}` | `/equipo/david-carrasco/` | |
| `{{MATRIZ}}` | `Grupo Fénix` | |

---

## 1. Arquitectura de URLs (el motor del tráfico)

**Por qué**: el grueso del tráfico orgánico entra por long-tail geográfico. Una
URL por **(servicio × población)** multiplica las puertas de entrada.

- [ ] Una landing por **servicio** (`/{{servicio}}/`)
- [ ] Una landing por **provincia** (`/{{SLUG_LOCAL}}/`)
- [ ] Una landing por **municipio/distrito** importante
- [ ] Slug = `keyword + población`, en minúsculas, sin tildes, con guiones
- [ ] Distritos de una gran ciudad llevan la ciudad delante para desambiguar
      (`...-madrid-{{distrito}}`)
- [ ] Trailing slash consistente en directorios (`/.../`), forzado por servidor
- [ ] **Nunca renombrar un slug** sin 301 + actualizar sitemap + canonical + enlaces internos

---

## 2. Contenido por página (no plantillas vacías)

**Por qué**: Google premia páginas locales con cuerpo único y datos citables;
las IA citan respuestas directas y cifras concretas.

- [ ] **≥ 1.000 palabras** visibles por landing (objetivo 1.200–1.500)
- [ ] **≥ 5 `<h2>`** + subsecciones `<h3>`
- [ ] **H1** = keyword principal + ciudad, con `<em>` en la palabra clave
- [ ] **≥ 20 enlaces internos** contextuales por landing
- [ ] Datos concretos y citables (precios, plazos, % con fuente)
- [ ] Cada landing local con su **FAQ propia** (no clonada literal entre ciudades)
- [ ] Respuesta directa de **40–60 palabras** al inicio de cada post de blog
      (formato que las IA citan literalmente)

---

## 3. Datos estructurados (Schema.org JSON-LD)

**Por qué**: generan resultados enriquecidos (FAQ, breadcrumb, estrellas) y son
lo que las IA leen para entender y citar la página.

| Tipo de página | Schemas obligatorios |
|---|---|
| Home | `Organization` + `WebSite` + `BreadcrumbList` |
| Servicio | `Service` + `BreadcrumbList` |
| Provincia / municipio | `LocalBusiness` + `BreadcrumbList` + `FAQPage` + `HowTo` |
| Post de blog | `Article` (autor = **Person**) + `HowTo` + `FAQPage` + `BreadcrumbList` |
| Perfil de autor | `Person` |

- [ ] `LocalBusiness` con `areaServed`, `hasOfferCatalog`, `aggregateRating`
- [ ] `Article` con `author` = **Person** (nunca `Organization`) + `datePublished` + `dateModified`
- [ ] `BreadcrumbList` en **todas** las páginas
- [ ] `FAQPage` + `HowTo` en landings locales y posts

### Plantilla — LocalBusiness (landing local)
```html
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"LocalBusiness",
"name":"{{MARCA}} en {{Poblacion}}",
"url":"{{DOMINIO}}/{{SLUG_LOCAL}}/","telephone":"{{TELEFONO}}","email":"{{EMAIL}}",
"description":"...",
"areaServed":{"@type":"City","name":"{{Poblacion}}","containedInPlace":{"@type":"AdministrativeArea","name":"{{Provincia}}"}},
"openingHours":["Mo-Su 00:00-23:59"],
"hasOfferCatalog":{"@type":"OfferCatalog","name":"Servicios en {{Poblacion}}","itemListElement":[
 {"@type":"Offer","itemOffered":{"@type":"Service","name":"{{Servicio 1}} en {{Poblacion}}"}}
]},
"aggregateRating":{"@type":"AggregateRating","ratingValue":"4.9","reviewCount":"127","bestRating":"5"}}
</script>
```

### Plantilla — FAQPage
```html
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
 {"@type":"Question","name":"¿{{pregunta}}?","acceptedAnswer":{"@type":"Answer","text":"{{respuesta concreta con cifra}}"}}
]}
</script>
```

### Plantilla — HowTo
```html
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"HowTo","name":"Proceso de {{KEYWORD}}","step":[
 {"@type":"HowToStep","position":1,"name":"{{paso}}","text":"{{detalle}}"}
]}
</script>
```

### Plantilla — Article (post de blog, autor = Person)
```html
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Article","headline":"{{titulo}}",
"description":"{{resumen}}","image":"{{DOMINIO}}/{{imagen}}.webp",
"datePublished":"{{AAAA-MM-DD}}","dateModified":"{{AAAA-MM-DD}}",
"author":{"@type":"Person","name":"{{AUTOR}}","url":"{{DOMINIO}}{{AUTOR_SLUG}}","jobTitle":"{{cargo}}"},
"publisher":{"@type":"Organization","name":"{{MARCA}}","url":"{{DOMINIO}}","logo":{"@type":"ImageObject","url":"{{DOMINIO}}/logo.webp"}},
"mainEntityOfPage":{"@type":"WebPage","@id":"{{DOMINIO}}/blog/{{slug}}/"}}
</script>
```

> ⚠️ **No añadir `Review`/`AggregateRating` inventados**. Solo con reseñas reales
> verificables; Google penaliza valoraciones falsas.

---

## 4. E-E-A-T (autoría — el diferenciador que casi nadie tiene)

**Por qué**: Google y las IA valoran contenido con autor identificado,
cualificado y verificable. Es lo que separa una web "de relleno" de una fiable.

- [ ] Página de equipo `/equipo/` (índice)
- [ ] Perfil del autor en `{{AUTOR_SLUG}}` con schema `Person`
      (`jobTitle`, `knowsAbout[]`, `hasCredential[]`, `worksFor`)
- [ ] **Byline visible** bajo el H1 de cada post, con enlace al perfil del autor
- [ ] El `author` del `Article` schema apunta a ese mismo perfil

### Plantilla — byline visible
```html
<div class="post-byline">
  <a href="{{DOMINIO}}{{AUTOR_SLUG}}">{{AUTOR}}</a>
  · {{cargo}} · Publicado {{fecha}} · Actualizado {{fecha}}
</div>
```

---

## 5. Optimización para buscadores de IA (AEO / GEO)

**Por qué**: ChatGPT, Perplexity y Claude son una fuente de tráfico creciente y
casi nadie la trabaja.

- [ ] **`/llms.txt`** en la raíz (resumen estructurado: quiénes, servicios, FAQ, cobertura, contacto, URLs)
- [ ] `robots.txt` permite explícitamente los bots de IA
- [ ] Respuesta directa de 40–60 palabras al inicio de los posts

### Plantilla — bloque de robots.txt para bots IA
```
# Bots de IA — acceso explícito permitido
User-agent: GPTBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: anthropic-ai
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Applebot
Allow: /

Sitemap: {{DOMINIO}}/sitemap.xml
```

### Estructura de `llms.txt`
```
# {{MARCA}} — {{dominio}}
> {{una frase de qué hacéis}}

## Quiénes somos
## Servicios
## Cobertura geográfica
## Preguntas frecuentes
## Contacto
## Páginas principales (lista de URLs clave)
```

---

## 6. SEO técnico (head + servidor)

- [ ] `<title>` 30–60 chars, formato `Concepto · Localización · 24h`
- [ ] `meta description` 120–160 chars con keyword + diferenciador local + CTA
- [ ] `<link rel="canonical">` en **todas**, sin inconsistencias de slash
- [ ] Open Graph + Twitter Card completos
- [ ] **`og:image` en todas** las páginas
- [ ] `sitemap.xml` con `priority`/`changefreq` jerarquizados
- [ ] `<meta name="robots" content="index,follow">`

### Plantilla — `<head>` mínimo por página
```html
<title>{{KEYWORD}} en {{Poblacion}} | Urgente 24h</title>
<meta name="description" content="{{120-160 chars con keyword + local + CTA}}">
<meta name="robots" content="index,follow">
<link rel="canonical" href="{{DOMINIO}}/{{SLUG_LOCAL}}/">
<meta property="og:title" content="...">
<meta property="og:description" content="...">
<meta property="og:url" content="{{DOMINIO}}/{{SLUG_LOCAL}}/">
<meta property="og:type" content="website">
<meta property="og:image" content="{{DOMINIO}}/{{imagen}}.webp">
<meta property="og:locale" content="es_ES">
<meta name="twitter:card" content="summary_large_image">
```

### Servidor — Apache (`.htaccess`)
> ⚠️ **Solo si el hosting es Apache** (DreamHost, cPanel…). En **GitHub Pages no
> hay `.htaccess`**: ni 301 vía Apache ni headers de seguridad; usar otro hosting
> si se necesitan.

- [ ] Forzar HTTPS + `www → no-www` + trailing slash
- [ ] **301 de todas las URLs antiguas indexadas** (migración WordPress, slugs viejos)
- [ ] `410 Gone` para `/wp-content/`, `/wp-admin/`, posts con fecha `/AAAA/MM/DD/`
- [ ] Caché 1 año para estáticos, 1 hora para HTML
- [ ] Brotli + GZIP
- [ ] Headers de seguridad (HSTS, CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy)
- [ ] Bloquear `.git`, `.env`, `*.md`, `composer.*`, librerías PHP

```apache
# Headers de seguridad
Header always set X-Content-Type-Options nosniff
Header always set X-Frame-Options SAMEORIGIN
Header always set Referrer-Policy strict-origin-when-cross-origin
Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
Header always set Permissions-Policy "geolocation=(), microphone=(), camera=(), payment=(), usb=()"
Header always set Content-Security-Policy "default-src 'self'; img-src 'self' data: https:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; frame-ancestors 'self'; base-uri 'self'; form-action 'self'"

# No desplegar documentación
<FilesMatch "(^\.htaccess$|^\.env|^\.git|composer\.(json|lock)$|\.md$|^README)">
Require all denied
</FilesMatch>
```

---

## 7. Enlazado interno

**Por qué**: distribuye autoridad y mantiene a Google rastreando todo el sitio.

- [ ] Cada provincia enlaza a sus **municipios** ("Cercanos")
- [ ] Cada provincia enlaza a **provincias colindantes** (geografía real)
- [ ] Cada landing enlaza a los **servicios** relevantes
- [ ] **Ninguna página con < 3 enlaces entrantes**

---

## 8. Rendimiento / Core Web Vitals

- [ ] HTML estático (o SSG/prerender si es app) — evitar render solo-cliente
- [ ] **CSS crítico inline** en el `<head>` + hoja externa minificada cacheada
- [ ] Fuentes con **fallback `size-adjust`/`ascent-override`** (cero CLS por fuentes);
      idealmente no descargar fuentes
- [ ] Hero con `<link rel="preload" fetchpriority="high">` (LCP)
- [ ] `min-height` + `contain:layout` en bloques que cargan tarde (anti-CLS)
- [ ] Imágenes en **WebP** optimizadas, con `width`/`height` y `loading`
- [ ] Prefetch on hover entre páginas

---

## Resumen: la "capa de confianza" que marca la diferencia

Casi todas las webs locales tienen la **base** (LocalBusiness + FAQ + Breadcrumb +
canonical + sitemap). Lo que distingue a la que posiciona bien es la capa fina:

> **HowTo + E-E-A-T (autor/equipo) + AggregateRating real + 301 heredados + `llms.txt`/bots-IA.**

Si una web nueva del grupo solo puede priorizar 5 cosas, son esas.

---

### Nota sobre arquitecturas
- **HTML estático**: aplica todo tal cual.
- **App React/Vite (SSG/prerender)**: aplica lo mismo, pero los schemas y metas se
  inyectan en build (componente tipo `SEOHead` + generación de páginas estáticas).
  Verificar siempre el **HTML de salida** (`dist/`), no el fuente.
- **GitHub Pages**: sin `.htaccess` → sin 301 Apache ni headers de seguridad.
  Migrar a hosting Apache si esos puntos importan.
