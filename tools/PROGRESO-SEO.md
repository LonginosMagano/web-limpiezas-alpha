# Progreso del plan SEO (ver AUDITORIA-SEO-2026-10.md)

Las tareas programadas leen y actualizan este fichero. Marcar con [x] lo hecho.

## Semana 1 (hecho el 16-10-2026, rama ccr-2de84e1f-7jiujz)
- [x] Bug de párrafos repetidos (`generate.py`, muestreo sin repetición) y pool ampliado 12 → 24
- [x] Email del propio dominio en `data.py` (**crear el buzón info@limpiezadeincendiosalpha.es si no existe**)
- [x] README sin datos falsos
- [x] /testimonios/ sin reseñas de ejemplo, con noindex, fuera de nav/sitemap; bloque "4.9/5" fuera de la home

## Pendiente manual (lo tiene que hacer una persona)
- [ ] NIF en `tools/data.py` (`NIF = ""`)
- [ ] Crear/verificar Google Business Profile (Madrid, C/ Juan de Mena 7) y pedir reseñas reales
- [ ] GitHub → Settings → Pages → "Enforce HTTPS" activado
- [ ] Search Console verificada + GA4 (o Plausible); pegar el ID en el generador
- [ ] Decidir qué hacer con limpiezadeincendiomadrid.com (301 a esta web o diferenciar)
- [ ] Reseñas reales con consentimiento → `TESTIMONIOS_PUBLICOS = True`

## Semana 2 (tarea programada "SEO · semana 2")
- [ ] Fechas reales por post (`published`/`updated` en posts.py) y `lastmod` desde git
- [ ] Títulos/H1 con keyword natural ("limpieza tras incendio en X", "empresa 24h")
- [ ] Home: quiénes somos, lista completa de provincias, casos reales

## Landings principales (tarea semanal, 2 por semana)
- [ ] Madrid
- [ ] Barcelona
- [ ] Valencia
- [ ] Sevilla
- [ ] Málaga
- [ ] Zaragoza
- [ ] Murcia
- [ ] Alicante
- [ ] Valladolid
- [ ] Toledo

## Blog: ampliar a 1.200+ palabras (tarea semanal, 1 por semana)
- [ ] cuanto-cuesta-limpieza-tras-incendio
- [ ] seguro-cubre-limpieza-incendio
- [ ] seguro-no-cubre-limpieza-incendio
- [ ] que-hacer-despues-de-un-incendio
- [ ] como-reclamar-seguro-incendio
- [ ] plazos-seguro-incendio

## Consolidación de municipios pequeños (tarea única, ~4 semanas)
- [ ] Propuesta en PR: qué municipios se consolidan en su provincia y cómo
