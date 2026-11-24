# Progreso del plan SEO (ver AUDITORIA-SEO-2026-10.md y AUDITORIA-SEO-2026-11.md)

> **14-11-2026:** la rama de la semana 1 sigue sin fusionar en `main` y las 4 tareas
> programadas (23-10, 10-11, 12-11, 13-11) hicieron el trabajo pero no pudieron hacer
> push (sesiones nuevas sin el repo autorizado). Ese trabajo se perdió. Las tareas se
> han vuelto a crear dentro de la sesión con acceso al repo y empujan a esta rama.
> **Nada llega a producción hasta fusionar `ccr-2de84e1f-7jiujz` en `main`.**

Las tareas programadas leen y actualizan este fichero. Marcar con [x] lo hecho.

## Semana 1 (hecho el 16-10-2026, rama ccr-2de84e1f-7jiujz)
- [x] Bug de párrafos repetidos (`generate.py`, muestreo sin repetición) y pool ampliado 12 → 24
- [x] Email del propio dominio en `data.py` (**crear el buzón info@limpiezadeincendiosalpha.es si no existe**)
- [x] README sin datos falsos
- [x] /testimonios/ sin reseñas de ejemplo, con noindex, fuera de nav/sitemap; bloque "4.9/5" fuera de la home

## Pendiente manual (lo tiene que hacer una persona)
- [ ] **Fusionar `ccr-2de84e1f-7jiujz` en `main`** (sin esto no se despliega nada)
- [ ] **Decidir un dominio por marca** (ver auditoría v2 §2): 301 de limpiezadeincendiomadrid.com a esta web o diferenciación real
- [ ] NIF en `tools/data.py` (`NIF = ""`)
- [ ] Crear/verificar Google Business Profile (Madrid, C/ Juan de Mena 7) y pedir reseñas reales
- [ ] GitHub → Settings → Pages → "Enforce HTTPS" activado
- [ ] Search Console verificada + GA4 (o Plausible); pegar el ID en el generador
- [ ] Decidir qué hacer con limpiezadeincendiomadrid.com (301 a esta web o diferenciar)
- [ ] Reseñas reales con consentimiento → `TESTIMONIOS_PUBLICOS = True`

## Semana 2 (hecho el 16-11-2026, rama ccr-2de84e1f-7jiujz)
- [x] Fechas reales por post (`POST_DATES` en posts.py: 21 iniciales 2026-05-23, Móstoles 2026-10-01); `lastmod` del sitemap = fecha del último commit del fichero, o la de hoy si cambió al regenerar (CI con `fetch-depth: 0`). Al ampliar un post, poner su `updated` en `POST_DATES`.
- [x] Títulos/H1/meta/intro con la keyword natural rotada por slug (`KW_NATURAL`: "limpieza tras incendio", "limpieza de incendios", "limpieza después de incendio"); títulos de 47-60 caracteres; `qa.py` acepta las variantes.
- [x] Home: bloque "Quiénes somos" (sede, 10 delegaciones enlazadas, responsable técnica, RC), 3 casos reales (Móstoles con fecha + Madrid + Barcelona) y las 34 provincias enlazadas por comunidad.

## Landings principales (tarea semanal, 2 por semana)
Mecanismo: `tools/contenido_local/<slug>.py` con `CONTENIDO` (title, h1, meta, intro, cuerpo, zonas, zonas_lista, faq). Ver el `__init__.py` de la carpeta.
- [x] Madrid (17-11-2026)
- [x] Barcelona (17-11-2026)
- [x] Valencia (24-11-2026)
- [x] Sevilla (24-11-2026)
- [ ] Málaga
- [ ] Zaragoza
- [ ] Murcia
- [ ] Alicante
- [ ] Valladolid
- [ ] Toledo

## Blog: ampliar a 1.200+ palabras (tarea semanal, 1 por semana)
- [x] cuanto-cuesta-limpieza-tras-incendio (19-11-2026, ~1.600 palabras, 2 tablas, 5 pasos, 6 FAQ)
- [ ] seguro-cubre-limpieza-incendio
- [ ] seguro-no-cubre-limpieza-incendio
- [ ] que-hacer-despues-de-un-incendio
- [ ] como-reclamar-seguro-incendio
- [ ] plazos-seguro-incendio

## Consolidación de municipios pequeños (tarea única, ~4 semanas)
- [ ] Propuesta en PR: qué municipios se consolidan en su provincia y cómo
