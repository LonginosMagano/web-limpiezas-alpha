"""15 plantillas rotativas para title, meta description y H1.

Rotación determinista por hash(slug) % 15. Cada plantilla recibe los
placeholders {keyword}, {kw_var}, {ciudad}, {provincia}, {brand}.
"""

TITLE = [
    "{keyword} en {ciudad} | {brand}",
    "{keyword} en {ciudad}: respuesta 24h | {brand}",
    "{keyword} en {ciudad}: empresa profesional | {brand}",
    "{keyword} en {ciudad} con respuesta urgente | {brand}",
    "{keyword} en {ciudad} | Hollín, humo y olor | {brand}",
    "{keyword} en {ciudad}: servicio 24/7 | {brand}",
    "{keyword} en {ciudad} con apoyo al seguro | {brand}",
    "{keyword} en {ciudad}: servicio especializado | {brand}",
    "{keyword} en {ciudad}: hollín, humo y descontaminación | {brand}",
    "{keyword} en {ciudad} | Valoración sin compromiso | {brand}",
    "{keyword} en {ciudad}: limpieza experta tras siniestro | {brand}",
    "{keyword} en {ciudad}: empresa con experiencia | {brand}",
    "{keyword} en {ciudad} | Hollín, humo y olor a humo fuera | {brand}",
    "{keyword} en {ciudad}: planificación, limpieza y entrega | {brand}",
    "{keyword} en {ciudad} | Equipo especializado | {brand}",
]

META = [
    "{keyword} en {ciudad}: limpieza profesional de hollín, humo y olor tras incendio. Llámanos al {phone} y te atendemos en horas.",
    "{keyword} en {ciudad}: eliminamos hollín, humo, olor a quemado y dejamos la vivienda lista para volver. Valoración rápida en {phone}.",
    "{keyword} en {ciudad} con respuesta urgente. Intervención en las primeras 72h, documentación para el seguro y trato directo en {phone}.",
    "{keyword} en {ciudad}: te ayudamos con el hollín, el olor a humo y el seguro tras un incendio. Llámanos al {phone}.",
    "{keyword} en {ciudad} con un equipo que actúa rápido: hollín, humo, contaminación cruzada y ozonización. Pide tu valoración al {phone}.",
    "{keyword} en {ciudad} con oficio y prisa controlada. Limpiamos vivienda, local o nave y dejamos todo listo para el seguro.",
    "{keyword} en {ciudad} profesional. Llegamos en horas, organizamos las primeras 72h y documentamos los daños para el seguro.",
    "{keyword} en {ciudad} con experiencia probada: limpieza, descontaminación y olor controlado. Atención rápida al {phone}.",
    "{keyword} en {ciudad}: si has tenido un incendio te ayudamos con la limpieza y la gestión del seguro. Pide cita al {phone}.",
    "{keyword} en {ciudad}: limpieza de hollín y olor a humo. Pásanos los datos y te llamamos para valorar la actuación.",
    "{keyword} en {ciudad}: cocina, salón, ropa, paredes y techos. Llámanos al {phone} y planificamos la intervención hoy.",
    "{keyword} en {ciudad}: nuestro equipo cubre la zona con intervención técnica, ozonización y memoria para el seguro.",
    "{keyword} en {ciudad} para vivienda, comunidad o local. Valoración sin compromiso al {phone}.",
    "{keyword} en {ciudad} con criterio técnico y trato cercano. Hollín, humo y olor a quemado bajo control.",
    "{keyword} en {ciudad}: empresa local. Te llamamos, valoramos y planificamos la limpieza en menos de 24h.",
]

H1 = [
    "{keyword} en {ciudad}",
    "{keyword} en {ciudad} con respuesta 24h",
    "{keyword} en {ciudad}: empresa profesional",
    "{keyword} en {ciudad}: servicio especializado",
    "{keyword} en {ciudad}: hollín, humo y olor fuera",
    "{keyword} en {ciudad}: servicio 24/7",
    "{keyword} en {ciudad}: te ayudamos tras el siniestro",
    "{keyword} en {ciudad} con apoyo al seguro",
    "{keyword} en {ciudad}: actuamos en las primeras horas",
    "{keyword} en {ciudad}: vivienda, local o nave",
    "{keyword} en {ciudad} para volver pronto a casa",
    "{keyword} en {ciudad}: equipo, oficio y urgencia",
    "{keyword} en {ciudad} sin sorpresas en presupuesto",
    "{keyword} en {ciudad} con experiencia comprobada",
    "{keyword} en {ciudad} planificada y segura",
]

# Plantillas de párrafos para construir cuerpo único por landing.
# Cada landing combina 6-8 párrafos elegidos por hash(slug) y rellena
# con {ciudad}, {provincia}, {tipo}, {rasgo}, {riesgo}, {barrios}, {kw_var}.
PARRAFOS = [
    "En {ciudad}, donde predominan {tipo}, una intervención tras un incendio "
    "tiene particularidades que no se ven en otros lugares. {rasgo}, y eso "
    "obliga a un orden de actuación distinto al de un piso aislado: primero "
    "ventilación cruzada controlada, después limpieza de hollín por capas y, "
    "por último, neutralización del olor con ozono o hidroxilo.",

    "El primer error que vemos en {ciudad} es entrar a limpiar sin protección "
    "y sin un plan. El hollín que queda en paredes y muebles es ácido: si se "
    "pasa una bayeta húmeda sin más, se fija. Por eso en cada {kw_var} en "
    "{ciudad} primero aislamos, fotografiamos para el seguro y solo después "
    "empezamos a retirar la contaminación.",

    "La {kw_var} en {ciudad} no es solo limpiar lo visible. El humo entra en "
    "armarios, dentro de cajones cerrados, en el interior de la nevera, en "
    "los conductos del aire acondicionado. Si no se trata, el olor vuelve a "
    "los pocos días. Nosotros descontaminamos por estancias completas, no "
    "solo donde se ve la mancha.",

    "Trabajar en {ciudad} significa adaptarse al lugar: {riesgo}. Por eso "
    "cuando llegamos preguntamos por el tipo de inmueble, la antigüedad, si "
    "hay vecinos afectados y si los bomberos usaron agua o polvo. Esa "
    "información cambia por completo el plan de limpieza.",

    "En vivienda particular en {ciudad} la prioridad suele ser una: que la "
    "familia vuelva a casa cuanto antes. Por eso priorizamos cocina, baño y "
    "dormitorios, dejamos los textiles fuera para tratamiento aparte y "
    "reservamos lo decorativo para una segunda fase, cuando la contaminación "
    "principal ya está bajo control.",

    "Si el siniestro afecta a un local o una nave en {ciudad}, sumamos un "
    "factor extra: la pérdida diaria por cierre. Por eso ofrecemos turnos "
    "ampliados, planificamos limpieza por zonas para reabrir parte de la "
    "actividad y entregamos la documentación lista para el seguro y la "
    "compañía aseguradora.",

    "El hollín en {ciudad} se comporta distinto según la mezcla de "
    "combustible que ardió: si el incendio fue de cocina (aceite, grasa) la "
    "capa es untuosa; si fue eléctrico o de mobiliario sintético, queda "
    "una capa seca de carbón muy fina que se mete en cada grieta. Nuestro "
    "equipo identifica el tipo en la primera visita.",

    "El olor a humo persistente es el motivo número uno por el que nos "
    "llaman semanas después del incendio. En {ciudad} muchos clientes "
    "intentaron limpiar por su cuenta, repintaron las paredes y, aun así, "
    "el olor seguía. La causa casi siempre está dentro de los textiles, los "
    "conductos y los huecos de pared. Ahí entramos nosotros.",

    "Para una {kw_var} en {ciudad} bien hecha es clave la documentación. "
    "Hacemos un álbum por estancias antes y después, anotamos el tipo de "
    "daño y entregamos una memoria que el perito puede leer en 10 minutos. "
    "Es la diferencia entre que el seguro pague rápido o pague tarde.",

    "Si el incendio en {ciudad} fue grande y hay riesgo estructural, "
    "trabajamos coordinados con los técnicos del seguro y con la propiedad. "
    "No tocamos nada que sea evidencia hasta que el perito lo autoriza. "
    "Primero foto, después protección, después limpieza.",

    "Los textiles tras un incendio en {ciudad} son delicados. Ropa, "
    "cortinas, sofás y colchones absorben hollín en profundidad y mantienen "
    "el olor durante meses. Los recogemos y los enviamos a tratamiento "
    "especializado en lugar de limpiarlos en seco, que es lo que fija el "
    "olor para siempre.",

    "Cada {kw_var} en {ciudad} acaba con una entrega formal: limpieza "
    "comprobada, neutralización de olor verificada con medidor y "
    "documentación entregada. Si en las 48 horas siguientes el cliente "
    "detecta olor residual, volvemos a pasar sin coste para asegurar que "
    "la vivienda vuelve a estar habitable.",
]

# Snippets para "Zonas de cobertura específica" — rotan también.
COBERTURA_BLURB = [
    "Cubrimos {ciudad} y los municipios cercanos con desplazamiento en menos de 4 horas para una primera valoración.",
    "Nuestro equipo se mueve con vehículos equipados desde la zona de {provincia} y llega a {ciudad} con material listo para limpiar.",
    "Atendemos en {ciudad}, su entorno metropolitano y otros núcleos de {provincia}. Si hay urgencia, salimos el mismo día.",
    "Operamos en {ciudad} sin subcontratar: el equipo que valora es el mismo que limpia y el mismo que entrega la documentación al seguro.",
]

# FAQs locales (4 preguntas con rotación por hash).
FAQ_LOCAL_POOL = [
    {"q": "¿En cuánto tiempo podéis estar en {ciudad}?",
     "a": "Si nos llamas antes de las 18h, normalmente hacemos la primera visita en {ciudad} en menos de 24 horas, y muchas veces el mismo día. Las primeras 72 horas son críticas para que el hollín no se fije, así que priorizamos las llamadas con urgencia real."},
    {"q": "¿La {kw_var} en {ciudad} la cubre el seguro?",
     "a": "En la mayoría de pólizas de hogar, comunidad y local, la limpieza profesional tras incendio está cubierta. Te entregamos una memoria con fotos antes/después, descripción del daño y desglose por estancias, justo lo que el perito necesita para tramitar."},
    {"q": "¿Trabajáis en pisos pequeños o solo en grandes siniestros?",
     "a": "Trabajamos en cualquier escala. En {ciudad} la mayoría de avisos son cocinas pequeñas con mucho olor y hollín concentrado. Llevamos el mismo proceso técnico, solo cambia la duración."},
    {"q": "¿Hay que sacar los muebles antes de que vengáis?",
     "a": "No. Llegamos, protegemos lo que no se va a tocar, retiramos lo dañado bajo inventario y limpiamos sobre el sitio lo recuperable. Cuanto menos se mueva antes de la valoración, mejor para el seguro."},
    {"q": "¿Tratáis también el olor a humo o solo lo visible?",
     "a": "El olor es lo más difícil. Tras limpiar el hollín, hacemos descontaminación con ozono o hidroxilo en las estancias afectadas. Si el olor persiste pasadas 48h, volvemos a tratar sin coste."},
    {"q": "¿Puedo entrar a la vivienda en {ciudad} antes de que limpiéis?",
     "a": "Solo lo justo para sacar cosas críticas (documentos, medicación) y con mascarilla. El hollín ácido y los restos de extinción son agresivos para la piel y los pulmones, así que cuanto menos tiempo, mejor."},
    {"q": "¿Necesito presupuesto previo o vais directos?",
     "a": "Hacemos primero una visita técnica gratuita en {ciudad}, valoramos el daño, te explicamos el plan y entregamos presupuesto antes de tocar nada. Sin compromiso ni letra pequeña."},
    {"q": "¿Limpiáis también la ropa y los textiles?",
     "a": "Sí, pero por separado. La ropa, cortinas, alfombras y sofás los inventariamos, los retiramos y los enviamos a un tratamiento especializado que elimina el olor sin fijarlo, que es el error típico de la limpieza en seco normal."},
]
