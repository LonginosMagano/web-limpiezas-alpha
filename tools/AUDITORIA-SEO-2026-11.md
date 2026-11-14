# Auditoría SEO v2 — limpiezadeincendiosalpha.es (14 nov 2026)

Segunda revisión, un mes después de la primera (`AUDITORIA-SEO-2026-10.md`).
**Pregunta:** la web sigue sin mejorar posiciones. ¿Por qué y qué hacemos?

## 0. Respuesta corta

1. **Nada de lo planificado ha llegado a producción.** La web que ve Google hoy es
   exactamente la del 1 de octubre: sigue con los 3 párrafos repetidos en cada
   landing, los testimonios marcados "de ejemplo" y todas las URLs con
   `lastmod` 2026-06-13. La rama de la semana 1 (`ccr-2de84e1f-7jiujz`) no se
   fusionó en `main`, y las cuatro tareas programadas hicieron su trabajo pero no
   pudieron subirlo: arrancaban en sesiones nuevas sin el repositorio autorizado
   y el push devolvía 403. Ese trabajo (semana 2, landings de Madrid y Barcelona,
   un post ampliado, la propuesta de consolidación) se perdió con sus contenedores.
   **No es que las mejoras no funcionen: es que no se han aplicado.**
2. **Hallazgo nuevo y estructural: la empresa tiene varias webs compitiendo por la
   misma búsqueda.** Para "limpieza incendio Madrid" el mismo propietario tiene al
   menos cinco dominios (ver §2). Dos de ellos comparten teléfono, dirección y
   email con esta web. Google no puede decidir cuál es la web de la empresa, los
   pocos enlaces y reseñas que haya se reparten, y la ficha de Google Business
   solo puede enlazar a una. Mientras eso no se resuelva, cualquier web del grupo
   crece a costa de las otras.
3. Lo demás sigue como en octubre: autoridad cero, sin ficha de Google Business,
   sin reseñas reales, sin NIF, sin Search Console/GA4 visibles, blog delgado y
   113 landings casi idénticas.

## 1. Estado real en producción (comprobado en vivo el 14-11-2026)

| Comprobación | Resultado |
|---|---|
| Último despliegue (`gh-pages`) | 1 oct 2026, commit `12cab06` |
| Rama semana 1 fusionada en `main` | **No** |
| Ramas `seo/*` de las tareas programadas en GitHub | **Ninguna** (push 403 en las 4 ejecuciones) |
| Párrafos duplicados en `/limpieza-despues-de-incendio-ocana/` en vivo | **3** (el bug sigue) |
| `/testimonios/` en vivo contiene "ejemplo" | **Sí** (2 veces) |
| `lastmod` del sitemap en vivo | 2026-06-13 en las 147 URLs |
| `www` → sin www | 301 correcto |
| URL sin barra final | 301 correcto |
| `/noexiste/` y `/provincias/madrid/` | 404 (sin 301 de URLs antiguas, esperado en GitHub Pages) |
| Cabeceras | `cache-control: max-age=600`, sin HSTS, sin cabeceras de seguridad (GitHub Pages) |
| PageSpeed Insights | No medido: cuota diaria de la API agotada. Pendiente |

Qué hicieron las tareas programadas (según sus propias transcripciones):
- 23-oct "semana 2": fechas reales por post, títulos/H1 naturales, home con "Quiénes
  somos" y 34 provincias. QA 0 errores. **Commit local `fb6d5ff`, perdido.**
- 10-nov "landings": Madrid (1.036 palabras) y Barcelona (932) con contenido local,
  mecanismo `tools/contenido_local/{slug}.py`. QA 0 errores. **Perdido.**
- 12-nov "blog" y 13-nov "consolidación": misma situación.

Causa: las tareas creaban sesiones nuevas en las que el repositorio no estaba
autorizado para push. Corregido el 14-11: las tareas se disparan ahora dentro de
la sesión que sí tiene el repo, y empujan a la rama `ccr-2de84e1f-7jiujz`. Solo
hace falta fusionar esa rama en `main` para desplegar.

## 2. La red de dominios (hallazgo nuevo)

Comprobado el 14-11-2026 descargando cada página:

| Dominio | Marca visible | Teléfono | Email | Dirección |
|---|---|---|---|---|
| limpiezadeincendiosalpha.es (esta) | Limpiezas de Incendios Alpha | 681 811 301 | info@limpiezasdeincendios.com (en vivo) | C/ Juan de Mena 7, Madrid |
| limpiezadeincendiomadrid.com | "Alpha — Limpieza tras Incendio en Madrid" | **681 811 301** | **info@limpiezasdeincendios.com** | **C/ Juan de Mena 7, Madrid** |
| limpiezasdeincendios.com | Limpiezas de Incendios | 623 224 353 | info@limpiezasdeincendios.com | — |
| nano-nex.es/limpieza-de-incendios-madrid/ | Nano Nex | 632 107 272 / 911 086 565 | info@nano-nex.es | — |
| limpiezaincendiosnanonexmadrid.com.es | Nano Nex | 911 086 565 | info@nanonex.es | Plaza de Castilla |

- El texto **no** está duplicado entre dominios (0 frases de 8 palabras en común
  entre esta web y las otras dos de Madrid). El problema no es copia, es
  **identidad**: dos webs con el mismo NAP (nombre-dirección-teléfono) son, para
  Google, la misma empresa con dos webs. Eso diluye enlaces, reseñas y señales de
  marca, e impide que la ficha de Google Business empuje a las dos.
- Esta web enlaza 4 veces al dominio limpiezasdeincendios.com (vía email) y la
  web hermana de Madrid enlaza 1 vez a esta. Son señales cruzadas que refuerzan
  la lectura de "red".
- Varias webs del mismo dueño, nuevas, con plantillas y estructura similares
  (landings por ciudad, blog, FAQ) en el mismo nicho es el patrón que Google
  describe como "sitios doorway" a escala de dominios. No se puede saber desde
  fuera si hay una acción, pero es la hipótesis más coherente con que **ninguna**
  de ellas destaque.

**Decisión necesaria (del propietario, no técnica):**
- Opción A (recomendada): **un dominio por marca real**. Si "Alpha" es la marca,
  limpiezadeincendiomadrid.com hace 301 página a página hacia esta web (su home →
  `/limpieza-despues-de-incendio-madrid/`), y esta web deja de usar el email del
  dominio limpiezasdeincendios.com. Nano Nex, si es otra empresa, mantiene su
  web con su NAP y no comparte nada (ni dirección, ni teléfono, ni plantilla).
- Opción B: mantener varias webs, pero **diferenciadas de verdad**: marca, NAP,
  diseño, autor y contenido distintos, sin enlaces cruzados. Es más caro y más
  lento que la A, y aun así reparte la autoridad.
- Lo que no funciona: lo actual (misma empresa, misma dirección, varios dominios).

## 3. Lo que no ha cambiado desde octubre (sigue abierto)

Todo el bloque A y B del informe de octubre sigue vigente porque nada se desplegó.
Resumen de lo que más pesa, por orden:

1. **Autoridad cero.** Ningún enlace entrante salvo un directorio. Un dominio de
   5 meses en un nicho con 6-8 competidores asentados (ABC Limpiezas,
   Nano Nex, Ozono3 con certificación ITEL, Multifranquicias…) no entra en
   primera página sin enlaces ni ficha local.
2. **Sin Google Business Profile ni reseñas.** El bloque de mapa domina estas
   búsquedas. Sin ficha no se aparece ahí.
3. **113 landings casi idénticas** (187 párrafos distintos para 113 páginas en
   producción). Google indexa 6 URLs según `site:` (home, Madrid, Barcelona,
   galería, testimonios, un post). El resto no.
4. **Confianza:** testimonios "de ejemplo" visibles, email de otro dominio, sin
   NIF, autora sin señales verificables.
5. **Frescura:** todo con fecha 2026-06-13; 21 posts el mismo día; media 400
   palabras por post.
6. **Sin medición:** sin Search Console ni GA4 en el HTML. Sin GSC no sabemos ni
   cuántas URLs están indexadas ni qué consultas dan impresiones. Es el dato que
   falta para dejar de trabajar a ciegas.

## 4. Plan reparado

**Esta semana (bloqueos que dependen de una persona):**
1. Fusionar `ccr-2de84e1f-7jiujz` en `main` (despliega la semana 1 y este informe).
2. Decidir §2 (un dominio por marca). Si es la opción A, preparar los 301 en el
   hosting de limpiezadeincendiomadrid.com.
3. Crear/verificar la ficha de Google Business de Alpha con la URL de esta web y
   pedir las 5 primeras reseñas a clientes reales.
4. Dar acceso a Search Console (o exportar "Páginas" e "Rendimiento") para medir.
5. NIF en `tools/data.py`; crear el buzón info@limpiezadeincendiosalpha.es.

**Automático (tareas reparadas, ahora en la sesión con acceso al repo, rama
`ccr-2de84e1f-7jiujz`):**
- Lunes 16-11: rehacer la semana 2 (fechas reales, títulos naturales, home).
- Martes semanales desde el 17-11: 2 landings principales con contenido local.
- Jueves semanales desde el 19-11: 1 post comercial ampliado a 1.200+ palabras.
- 11-12: propuesta de consolidación de municipios pequeños.
Cada ejecución deja commits en la rama; hay que fusionar la rama en `main` al
menos una vez por semana para que llegue a producción.

**Métrica de éxito (mensual):** URLs indexadas en GSC (hoy ~6 de 147), impresiones
y clics por consulta, reseñas en GBP, enlaces entrantes. Si en 8 semanas con todo
lo anterior desplegado no hay movimiento en impresiones, el problema es §2 y hay
que ejecutar la opción A sin más demora.
