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
    # 1 — apertura cinematográfica con sensorial
    "Hay un olor que no se olvida. Quien ha entrado por primera vez en una "
    "vivienda calcinada lo sabe: ácido, denso, como si alguien hubiera quemado "
    "plástico al lado de un café muy oscuro. Y se queda. En las cortinas, en "
    "las páginas del libro de la mesita, en el papel del baño. Ese es el olor "
    "que venimos a quitar en {ciudad}. No con un ambientador ni un trapo "
    "húmedo. Con un proceso que lleva su tiempo y que aprendimos haciéndolo "
    "muchas veces.",

    # 2 — el primer error y por qué importa
    "El primer error que vemos al llegar a una vivienda en {ciudad} suele "
    "ser siempre el mismo: alguien ha pasado un trapo mojado por la pared, "
    "queriendo ayudar. Lo entendemos. Es lo natural. Pero ese trapo acaba "
    "de fijar el hollín dentro del yeso, y a partir de ahí ya solo se va con "
    "imprimación y pintura nueva. Por eso, antes de tocar nada, llámenos. "
    "Buena parte de nuestro trabajo aquí, en muchos casos, consiste en "
    "deshacer lo que ya se hizo por desconocimiento.",

    # 3 — el olor que vuelve
    "El olor a humo es traicionero. Las primeras horas casi no se nota, "
    "porque el cerebro se acostumbra y deja de registrarlo. Pero pase tres "
    "días fuera de casa y vuelva al piso: ahí está, intacto, igual o peor "
    "que la primera noche. ¿Por qué? Porque el humo no se queda en la "
    "superficie. Entra en el armario cerrado, en el conducto de la campana, "
    "dentro del colchón. Una limpieza superficial en {ciudad} no sirve. Hay "
    "que tratar la estancia entera, hasta los rincones que no han visto la "
    "luz en años.",

    # 4 — adaptarse al lugar
    "No todas las viviendas son iguales, ni siquiera dentro de {ciudad}. Lo "
    "primero que preguntamos al llegar es la edad del edificio, el tipo de "
    "tabique, si los bomberos usaron agua o polvo y si la cocina tenía "
    "campana. Parece una conversación de cinco minutos. Lo es. Pero cada "
    "respuesta cambia el plan. Aquí {riesgo}: lo hemos visto tantas veces "
    "que ya casi lo intuimos antes de subir.",

    # 5 — volver a casa
    "En una vivienda particular la pregunta siempre es la misma: ¿cuándo "
    "puedo volver? Por eso vamos por fases. Primero cocina y baño, porque "
    "sin esos dos espacios no se vive. Después el dormitorio principal, "
    "para que esa misma semana pueda dormir aquí. Y al final el resto. "
    "Le entregamos la casa en partes, no de golpe, para que vuelva a su "
    "vida cuanto antes. No es marketing. Es lo razonable.",

    # 6 — locales y negocios
    "Cuando arde un local en {ciudad}, el reloj que mandan no es solo el "
    "del hollín. Es el de los días que se está perdiendo dinero. Por eso "
    "adaptamos turnos: limpiamos por la noche, abrimos una zona mientras "
    "trabajamos en otra, y le damos al gestor el certificado en cuanto "
    "Sanidad lo pide. Hemos vuelto a poner restaurantes en marcha en cinco "
    "días desde el siniestro. Peluquerías. Oficinas. Cada negocio tiene su "
    "propia prisa.",

    # 7 — qué clase de hollín
    "El hollín no es uno solo. Si el fuego fue de cocina ―aceite, grasa―, "
    "lo que queda en las paredes es viscoso, casi mantecoso al tacto. Si "
    "fue eléctrico, un cuadro, un electrodoméstico, lo que queda es un "
    "polvo seco de carbono que se mete en cada grieta. Y si ardieron "
    "muebles sintéticos, el residuo es pegajoso y huele distinto. Cada uno "
    "se trata diferente. Nuestro técnico lo identifica al pasar la mano "
    "por la pared. No hace falta nada más.",

    # 8 — el cliente que llama tarde
    "Buena parte de los clientes nos llaman semanas después del incendio. "
    "Han intentado limpiar, han repintado, alguno ha probado con el "
    "hidrolimpiador del cuñado. Y el olor sigue. Ese es el momento en que "
    "entienden que una limpieza tras incendio en {ciudad} no es como una "
    "limpieza normal. El olor que se ha metido en los huecos solo se va "
    "con tratamiento profesional. Cuanto antes nos llame, menos paga al "
    "final. Suena tópico, pero así funciona.",

    # 9 — documentación para el seguro
    "Detrás de la limpieza viene el papeleo del seguro, que es donde "
    "mucha gente pierde la batalla. Le ahorramos esa parte. Hacemos un "
    "álbum por estancias antes y después, lo entregamos en PDF con índice "
    "y un resumen de una página que el perito lee en diez minutos. Esa "
    "memoria la han aceptado sin pegas las grandes aseguradoras: Mapfre, "
    "Mutua Madrileña, AXA, Aegon. Es la diferencia entre cobrar en seis "
    "semanas o en seis meses.",

    # 10 — incendios serios, daños estructurales
    "Si el incendio en {ciudad} fue serio y hay riesgo estructural, no "
    "entramos a limpiar como en una vivienda recién evacuada. Coordinamos "
    "con el arquitecto y con el perito antes de tocar nada. Primero foto. "
    "Después protección. Después limpieza. Hemos tenido casos en los que "
    "de la primera valoración a la entrega final pasaron dos meses. Cada "
    "paso por escrito. Cada coordinación con quien tocara. Improvisar, "
    "aquí, no es una opción.",

    # 11 — textiles
    "Los textiles son lo más delicado. Sofás, colchones, alfombras, "
    "cortinas y, sobre todo, la ropa: nada se limpia igual que una pared. "
    "Lo que hace la tintorería normal ―meter la prenda en seco― fija el "
    "olor para toda la vida. Es el error que más vemos. Por eso recogemos "
    "todo, lo inventariamos pieza a pieza y lo enviamos a un proceso "
    "especializado. Lo que se recupera vuelve sin olor. Lo que no, queda "
    "documentado para el seguro. Esa decisión la tomamos nosotros, no el "
    "cliente, porque hace falta tiento.",

    # 12 — la entrega
    "Cuando terminamos no nos limitamos a guardar las herramientas. "
    "Pasamos un medidor de olor por cada estancia, comprobamos rincones y, "
    "si algo no nos cuadra, volvemos a tratar. La memoria final se entrega "
    "en mano o por correo. Si en las 48 horas siguientes detecta cualquier "
    "olor residual, volvemos sin cobrar. No por marketing. Porque tras un "
    "incendio uno ya ha tenido bastante para que encima discutamos por una "
    "segunda visita.",

    "Antes de encender una sola máquina hacemos una cosa que parece menor: "
    "abrir ventanas en cruz y medir. Medimos partículas en suspensión y "
    "humedad en cada habitación de la vivienda en {ciudad}, y anotamos el "
    "resultado en la memoria. No es postureo técnico. Es lo que nos dice si "
    "el hollín sigue flotando y se va a volver a posar en lo que acabemos de "
    "limpiar. Si está en el aire, primero se filtra; si ya está en la pared, "
    "primero se aspira en seco. El orden lo decide el medidor, no la prisa.",

    "Las comunidades de vecinos son un caso aparte. Un incendio en un cuarto "
    "piso deja hollín en la caja de escalera hasta el portal, en los buzones "
    "y en el ascensor, y la factura la paga el seguro de la comunidad, no el "
    "del vecino. En {ciudad} tratamos con el administrador de fincas desde la "
    "primera visita: él recibe el presupuesto por zonas comunes, el "
    "propietario el suyo por la vivienda, y ninguno de los dos tiene que "
    "pelearse por qué parte le toca a quién. Dos partes, dos memorias.",

    "El hollín es conductor. Esa frase la repetimos en cada cuadro eléctrico "
    "que vemos ennegrecido. Un enchufe que parece solo sucio puede tener "
    "carbón dentro, y conectar la luz sin limpiarlo es la forma más rápida de "
    "tener un segundo incendio. Por eso en viviendas de {ciudad} con fuego "
    "eléctrico pedimos que no se restablezca el suministro hasta que hayamos "
    "limpiado mecanismos y cajas de registro, y lo dejamos por escrito en la "
    "memoria para que el perito lo vea.",

    "Hay cosas que no se limpian: se tiran. Colchones empapados por los "
    "bomberos, un sofá con la espuma chamuscada, alimentos abiertos en una "
    "cocina llena de humo. Lo decimos claro desde la primera visita porque "
    "nadie quiere pagar por limpiar algo que al mes volverá a oler. Lo que "
    "retiramos se fotografía, se pesa y se inventaria pieza a pieza para que "
    "el seguro lo reponga. En {ciudad} gestionamos también el contenedor y la "
    "retirada, para que usted no tenga que buscar quién se lo lleva.",

    "El plazo que damos es el plazo que cumplimos, y lo decimos con una "
    "cifra, no con un \"depende\". Una cocina de tamaño normal en {ciudad} "
    "suele estar lista en dos o tres días de trabajo. Un piso completo con "
    "humo en todas las estancias, entre cinco y diez. Si al desmontar aparece "
    "algo que no se veía (hollín detrás de un armario empotrado, un falso "
    "techo lleno), se lo contamos ese mismo día y ajustamos el plazo antes de "
    "seguir, no al final.",

    "Trabajamos con esponja química en seco antes de que cualquier líquido "
    "toque la pared. Es una esponja de caucho vulcanizado que arranca el "
    "hollín por adherencia, sin arrastrarlo. Después, y solo después, viene "
    "el desengrasante alcalino, y por último el aclarado. Si en una vivienda "
    "de {ciudad} nos encontramos gotelé o pintura al temple, el proceso "
    "cambia: esas superficies no admiten agua y hay que ir pasada a pasada en "
    "seco. Por eso preguntamos qué pintura tiene antes de dar un precio.",

    "Un olor que vuelve a los diez días no es mala suerte: es hollín que se "
    "quedó en un sitio que nadie abrió. Dentro del extractor de la campana. "
    "En los conductos de la calefacción. En el hueco del tambor de la "
    "persiana. Por eso en {ciudad} desmontamos lo que haga falta en la "
    "primera visita y no damos la limpieza por cerrada hasta pasar el medidor "
    "por esos huecos. Cuesta una hora más. Ahorra una segunda intervención "
    "entera.",

    "La ozonización no es echar un aparato en la habitación y marcharse. El "
    "ozono en concentración alta degrada gomas, textiles y hasta algunas "
    "pinturas, así que lo dosificamos por metros cúbicos y por tiempo, con la "
    "estancia precintada y sin nadie dentro. Después se ventila hasta que el "
    "medidor marca cero. En viviendas de {ciudad} con mascotas o niños lo "
    "planificamos para una tarde en la que la familia esté fuera, y avisamos "
    "al vecino de al lado por si nota olor a tormenta.",

    "Cuando el incendio ha sido en un piso alquilado, al propietario le "
    "preocupa una cosa: cuánto tarda en poder volver a alquilarlo. Y al "
    "inquilino, otra: qué parte le pueden reclamar. Lo tratamos por separado. "
    "Al propietario le damos fecha de entrega y la memoria para su seguro; al "
    "inquilino, el inventario de lo suyo que se recupera y lo que no. En "
    "{ciudad} hemos visto muchos pisos de alquiler con {riesgo}, y casi "
    "siempre el conflicto viene de no haber documentado al principio.",

    "La ropa y los textiles se tratan fuera de la vivienda, en un proceso de "
    "lavado con tensioactivos específicos y secado controlado que no fija el "
    "olor. Lo que mucha gente no sabe es que la tintorería convencional "
    "trabaja en seco con percloroetileno, y eso sella el humo dentro de la "
    "fibra para siempre. Por eso recogemos las prendas inventariadas, las "
    "etiquetamos por habitación y las devolvemos en {ciudad} con la lista de "
    "lo que ha vuelto limpio y lo que no ha tenido remedio.",

    "Muchos avisos nos llegan desde el propio perito del seguro, que ya ha "
    "visto el piso y sabe que una limpieza mal hecha le dará más problemas "
    "que una bien hecha. Trabajar con peritos nos ha enseñado qué necesitan "
    "en la memoria: fotos con fecha y estancia, superficie en metros de cada "
    "pared tratada, producto usado y horas por fase. En {ciudad} esa memoria "
    "la tiene el perito antes de que terminemos, para que la valoración no se "
    "retrase por nuestra parte.",

    "Hay algo que nos piden a menudo y a lo que decimos que no: pintar encima "
    "para que no se vea. La pintura sobre hollín se despega en semanas y el "
    "olor sigue debajo. Si una pared en {ciudad} está tan dañada que no "
    "admite limpieza, lo decimos, lo fotografiamos y lo dejamos en la memoria "
    "como superficie a reponer, para que lo haga un pintor cuando nosotros "
    "hayamos terminado. Primero se descontamina, luego se decora. Al revés no "
    "funciona nunca.",
]

# Snippets para "Zonas de cobertura específica" — rotan también.
COBERTURA_BLURB = [
    "Cubrimos {ciudad} y los pueblos de alrededor con la furgoneta cargada desde el primer aviso. Si llama por la mañana, esa misma tarde podemos estar allí mirando.",
    "El equipo se mueve por toda {provincia}. En {ciudad} en concreto, si la urgencia lo justifica, salimos el mismo día. Si no, al siguiente sin falta.",
    "Trabajamos en {ciudad} y los municipios cercanos sin subcontratar. La persona que valora el daño es la misma que limpia y la misma que firma la memoria final. Sin teléfono escacharrado entre intermediarios.",
    "Atendemos {ciudad} y casi todo el territorio de {provincia} con desplazamiento rápido. Le decimos al teléfono si podemos esa tarde o al día siguiente, sin promesas que no podamos cumplir.",
]

# FAQs locales (4 preguntas con rotación por hash).
FAQ_LOCAL_POOL = [
    {"q": "¿En cuánto tiempo podéis estar en {ciudad}?",
     "a": "Si nos llama antes de las seis de la tarde, normalmente vamos al día siguiente, y muchas veces esa misma tarde si el caso es serio. Las primeras 72 horas son las críticas para que el hollín no se fije, así que cuanto antes nos avise, mejor para usted. Contestamos al teléfono o WhatsApp en menos de una hora durante el día."},
    {"q": "¿La {kw_var} en {ciudad} la cubre el seguro?",
     "a": "Casi siempre. En las pólizas de hogar y de comunidad la limpieza tras incendio entra dentro de la cobertura de daños, y le entregamos la memoria con fotos antes/después y desglose por estancias, que es lo que pide el perito para abonarlo. Si la aseguradora pone trabas, le acompañamos en la reclamación."},
    {"q": "¿Trabajáis en pisos pequeños o solo en grandes siniestros?",
     "a": "Trabajamos en todo. En {ciudad} la mitad de los avisos son cocinas pequeñas: una freidora, una vela olvidada, un cargador que se quemó por la noche. El proceso técnico es el mismo; solo cambia el tiempo. No descartamos a nadie por tamaño."},
    {"q": "¿Hay que sacar los muebles antes de que vengáis?",
     "a": "No, mejor no toque nada. Cuanto menos se mueva antes de nuestra valoración, mejor para el seguro. Llegamos, fotografiamos, protegemos lo que no va a tocarse y empezamos. Lo que haya que retirar lo inventariamos pieza a pieza."},
    {"q": "¿Tratáis también el olor a humo o solo lo visible?",
     "a": "El olor es lo más difícil de quitar y lo tratamos siempre. Tras la limpieza física hacemos ozonización o tratamiento con hidroxilo en cada estancia. Si pasadas 48 horas detecta cualquier olor residual, volvemos sin coste. Forma parte del trato."},
    {"q": "¿Puedo entrar a la vivienda en {ciudad} antes de que limpiéis?",
     "a": "Lo justo y con mascarilla. El hollín ácido y los restos del extintor no son amables con la piel ni los pulmones. Si tiene que recuperar documentos importantes, medicación o algo personal, hágalo y salga rápido. Lo demás puede esperar a que estemos nosotros."},
    {"q": "¿Necesito presupuesto previo o vais directos?",
     "a": "Hacemos primero una visita técnica gratuita en {ciudad}. Subimos, miramos, le explicamos lo que vamos a hacer y le entregamos un presupuesto cerrado antes de tocar nada. Sin compromiso ni cláusulas raras. Si al final decide no contratarnos, tampoco pasa nada."},
    {"q": "¿Limpiáis también la ropa y los textiles?",
     "a": "Sí, pero por separado. La ropa, las cortinas, las alfombras, los sofás: todo se inventaría, se retira y se trata en un proceso especializado. La tintorería normal no vale: el percloroetileno que usan fija el olor para siempre. Lo que se recupera vuelve a casa sin olor; lo que no, queda documentado para el seguro."},
]
