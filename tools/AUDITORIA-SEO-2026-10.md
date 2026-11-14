# Auditoría SEO — limpiezadeincendiosalpha.es (16 oct 2026)

**Pregunta:** la web apenas sube posiciones. ¿Por qué y qué hay que cambiar?

**Respuesta corta:** la base técnica está bien (QA en verde, canonical, sitemap, schema,
HTML estático rápido). Lo que frena el posicionamiento no es técnico, son cuatro cosas:
(1) un bug del generador que repite párrafos en las 113 landings y deja el contenido real
por página en ~4 párrafos, (2) 113 landings casi iguales entre sí (patrón *doorway*),
(3) señales de confianza rotas que Google ya muestra en los resultados (testimonios
"de ejemplo", email de otro dominio, sin NIF, sin reseñas externas) y (4) autoridad
cero: dominio de 4 meses, sin enlaces entrantes, sin Google Business Profile y con una
web hermana (limpiezadeincendiomadrid.com) compitiendo por la misma consulta con el
mismo teléfono y dirección.

Datos de partida verificados:

| Dato | Valor |
|---|---|
| URLs en sitemap / en disco | 146 / 146 (coinciden) |
| Landings geográficas | 113 (31 provincias + 61 municipios + 21 distritos Madrid) |
| Posts de blog | 22 (21 + 1 publicado el 1 oct) |
| Palabras por landing (sin cabecera/pie) | 1.627 – 1.911 |
| Párrafos únicos de cuerpo en las 113 landings | 187 |
| Párrafos que aparecen en ≥50 landings | 13 |
| Similitud media entre landings (Jaccard 8-shingles) | 0,33 (pares hasta 0,61) |
| Palabras por post de blog | 265 – 601 (media ~400) |
| `lastmod` en sitemap | 2026-06-13 en las 146 URLs |
| Enlaces entrantes externos encontrados | 0 (solo un directorio: espainfo.com) |
| Analítica / verificación GSC en HTML | ninguna |
| Último despliegue en gh-pages | 1 oct 2026 (al día con `main`) |

---

## A. Problemas críticos (los que explican el estancamiento)

### A1. Bug: cada landing repite 3 de sus 7 párrafos
`tools/generate.py:672` elige 7 párrafos de un pool de 12 con paso 3:
`PARRAFOS[(h(slug) + i*3) % 12] for i in range(7)`. Los índices i=0/4, 1/5 y 2/6
colisionan, así que **las 113 landings tienen 3 párrafos duplicados dentro de la misma
página** (339 párrafos repetidos en total). Se ve a simple vista en cualquier landing
(sección "Qué hacemos en {ciudad}": el párrafo de los textiles y el del "trapo mojado"
aparecen dos veces).

Consecuencia: la landing "de 1.700 palabras" tiene en realidad 4 párrafos de cuerpo
(~300 palabras) y el resto es plantilla compartida. Google lo lee como contenido
inflado.

Arreglo: usar un paso coprimo con el tamaño del pool o `random.Random(slug).sample`,
y ampliar `PARRAFOS` de 12 a 30+. Pero el arreglo del bug solo evita el síntoma; el
problema de fondo es A2.

### A2. 113 landings casi idénticas (patrón doorway)
Con 12 párrafos, 15 H1, 15 títulos y 4 blurbs de cobertura rotados por hash, hay
187 párrafos distintos para 113 páginas. Pares de ciudades sin relación (Valladolid vs
Orihuela, Gandía vs Burjassot) comparten el 55-60 % del texto. Lo único local es el
nombre de la ciudad y tres variables por provincia (`tipo`, `rasgo`, `riesgo`).

Google trata esto como páginas puerta: indexa algunas (site: devuelve Madrid y
Barcelona) y deja el resto en "Rastreada: actualmente sin indexar". Es la causa más
probable de que "apenas suba".

Qué hacer:
- Elegir 25-35 landings prioritarias (capitales grandes + Madrid distritos con más
  población) y escribirlas con contenido local real: tipo de edificio dominante,
  barrios por nombre, casos atendidos, foto propia, perito/aseguradoras habituales,
  tiempos reales de desplazamiento desde la base.
- Municipios pequeños (Ocaña, Lebrija, Montilla, Coria del Río, Baza, Utebo…):
  o se escriben de verdad o se consolidan en la landing de provincia (sección
  "Municipios" con 150 palabras cada uno) y las URLs actuales pasan a 301.
  No hay que mantener 113 páginas que Google no va a indexar.
- Comprobar en Search Console → Páginas cuántas de las 146 están indexadas. Ese
  número es el KPI de este punto.

### A3. Señales de confianza rotas (y Google las enseña)
- `/testimonios/` dice literalmente "Valoración media 4.8/5 sobre 8 reseñas (ejemplo,
  sustituiremos por reales…)" y "Testimonios de ejemplo basados en perfiles reales".
  Los buscadores ya lo citan en el resumen de resultados. Hay que quitar la página o
  sustituir por reseñas reales con consentimiento.
- Email `info@limpiezasdeincendios.com` en 563 páginas y en el schema `Organization`:
  es otro dominio. NAP inconsistente. Debe ser `@limpiezadeincendiosalpha.es`.
- `NIF = ""` en `tools/data.py`: el aviso legal sale sin NIF (LSSI art. 10 lo exige y
  es señal E-E-A-T básica).
- `README.md` aún dice "Email: info@miweb.es" y el caché de Google muestra un Gmail en
  galería/testimonios. Limpiar todo rastro.
- Perfil de autora (`/equipo/marta-magali/`) sin foto real, sin `sameAs` (LinkedIn),
  sin credenciales verificables. La página `/equipo/` tiene 1 enlace saliente.

### A4. Autoridad cero y marca dividida
- Dominio online desde junio 2026. Ningún enlace entrante salvo espainfo.com. En un
  nicho donde compiten limpiezaincendio.es, abclimpiezasdeincendios.com, nano-nex.es,
  cys-ozono3.com (con certificación ITEL) y limpiezasdeincendios.com, sin enlaces no
  se sale de la página 3.
- **No hay Google Business Profile** visible. Para "limpieza incendio {ciudad}" el
  resultado dominante es el map pack; sin ficha no se aparece ahí. Crear/verificar la
  ficha con la dirección de Calle de Juan de Mena 7 (ya está en espainfo) y las de
  Valladolid, Barcelona y Zaragoza si son delegaciones reales.
- **limpiezadeincendiomadrid.com** ("Alpha — Limpieza tras Incendio en Madrid") usa
  el mismo teléfono y la misma dirección. Dos dominios de la misma empresa compitiendo
  por "limpieza incendio madrid" se canibalizan y diluyen los enlaces. Decidir uno:
  o 301 de la de Madrid a `/limpieza-despues-de-incendio-madrid/`, o diferenciarla
  de verdad (marca distinta, contenido distinto, sin copiar texto).

---

## B. Problemas importantes

### B1. Cero frescura
`NOW = "2026-06-13"` está fijado a mano en `generate.py:80`. Resultado: las 146 URLs
tienen el mismo `lastmod`, los 21 posts iniciales el mismo `datePublished`, y todos
los bylines dicen "Actualizado 2026-06-13". Google ignora un `lastmod` que no cambia
nunca. Arreglo: fecha por post en `posts.py` (`published`/`updated`) y `lastmod` real
desde `git log -1 --format=%cs -- <ruta>` en el workflow.

### B2. Blog delgado
22 posts de 265-600 palabras. Para consultas como "cuánto cuesta limpieza tras
incendio" o "seguro cubre limpieza incendio" los resultados que posicionan tienen
1.200-2.000 palabras, tablas de precios y casos. Ampliar primero los 6 posts con más
intención comercial (coste, seguro cubre, seguro no cubre, qué hacer, 72 horas,
reclamar seguro) y publicar 2 al mes con fecha real.

### B3. Keyword y títulos poco naturales
- "Limpieza Después de Incendio" en mayúsculas de título dentro de frases del cuerpo
  ("Limpieza Después de Incendio en Ocaña: limpiamos el hollín…"). Suena a relleno.
- La gente busca "limpieza incendio madrid", "limpieza tras incendio", "empresa
  limpieza incendios". "Después de" aparece poco en búsquedas reales.
- Títulos tipo "Limpieza Después de Incendio en Albacete: 24h | Alpha": "Alpha" solo
  no dice nada. Propuesta: `Limpieza tras Incendio en Albacete · Empresa 24h |
  Limpiezas Alpha`.

### B4. Home débil
900 palabras y enlaza solo a 8 provincias. Es la página con más autoridad y reparte
poco. Añadir: bloque "quiénes somos" con datos reales (años, equipo, base, NIF,
seguro RC), lista completa de provincias (como en `/ubicaciones/`), 2-3 casos reales
con foto y fecha, logos de aseguradoras con las que se ha trabajado de verdad.

### B5. GitHub Pages y el `.htaccess`
El `.htaccess` no se ejecuta en GitHub Pages. Por tanto:
- Los 301 de `/provincias/x/`, `/localidades/x/`, `/barrios/madrid/x/` no existen:
  si esas URLs se indexaron alguna vez, hoy dan 404.
- No hay HSTS ni cabeceras de seguridad.
- Google tiene indexada la home como `http://` (sin s). Verificar que "Enforce HTTPS"
  está activado en Settings → Pages. Si está, basta; si no, activarlo.
Opciones: poner Cloudflare delante (redirects + HSTS gratis) o mover a Cloudflare
Pages/Netlify con `_redirects`.

### B6. Schema: 113 LocalBusiness para un negocio
Cada landing declara un `LocalBusiness` con nombre "Alpha – {ciudad}", mismo teléfono
y dirección solo con `addressLocality`. Google lo lee como 113 negocios falsos.
Mejor: `LocalBusiness` completo (dirección, geo, horario, `sameAs`) solo en home y en
las 4 delegaciones reales; en el resto `Service` con `provider` → la organización y
`areaServed` → la ciudad. Añadir `sameAs` (GBP, LinkedIn, redes) y `hasOfferCatalog`.
No añadir `aggregateRating` hasta tener reseñas reales.

### B7. Rendimiento e imágenes
- 3 WebP de 400+ KB (`azulejos-hollin…`, `escalera-comunidad…`,
  `pared-escalera-vecinos…`); objetivo <150 KB.
- Nombres de archivo sin valor (`1759851783934.webp`, `Limpieza de incendios madrid
  (1).webp` con espacios y paréntesis). Renombrar con keyword.
- `og:image` es el mismo `hero.jpg` en las 113 landings.
- Dos familias de Google Fonts con 5 pesos. Autoalojar o usar system fonts: quita
  una conexión externa y CLS.
- `source-images/` (50 MB) está en el repo; no se despliega pero pesa en cada clone.

### B8. Sin medición
No hay GA4/Plausible ni verificación de Search Console en el HTML (puede estar vía
DNS; confirmar). Sin GSC no se puede saber qué está indexado ni qué consultas traen
impresiones. Es lo primero que hay que mirar antes de reescribir nada.

---

## C. Plan por prioridad

**Semana 1 — parar el sangrado (sin reescribir contenido)**
1. Arreglar el bug de párrafos (`generate.py:672`) y regenerar.
2. Email propio en `data.py`, NIF en aviso legal, limpiar README.
3. Quitar `/testimonios/` o sustituir por 3-5 reseñas reales con consentimiento.
4. Crear/verificar Google Business Profile (Madrid) y pedir las primeras reseñas.
5. Activar Enforce HTTPS en GitHub Pages; verificar GSC y poner GA4.
6. Decidir qué pasa con limpiezadeincendiomadrid.com (301 o diferenciar).

**Semanas 2-3 — contenido que Google pueda indexar**
7. Reescribir la home (B4) y las 10 landings principales con contenido local real
   (Madrid, Barcelona, Valencia, Sevilla, Málaga, Zaragoza, Murcia, Alicante,
   Valladolid, Toledo).
8. Fechas reales por página y `lastmod` desde git (B1).
9. Títulos y H1 con la keyword natural (B3).

**Semana 4 en adelante — autoridad**
10. Ampliar los 6 posts comerciales a 1.200+ palabras; 2 posts/mes con fecha real.
11. Consolidar municipios pequeños en su provincia con 301 (A2).
12. Enlaces: directorios del sector, administradores de fincas, colegios de
    administradores, blogs de seguros, prensa local tras incendios reales, perfil en
    LinkedIn de la responsable técnica con enlace a `/equipo/`.

**Expectativa realista:** un dominio de 4 meses sin enlaces en un nicho con 6-8
competidores asentados necesita 6-12 meses de contenido real + enlaces + ficha GBP
para entrar en primera página fuera de la marca. Lo de arriba quita lo que hoy lo
está frenando activamente; no sustituye al tiempo ni a los enlaces.
