"""Artículos del blog.

Cada post tiene:
- slug, title (titular = pregunta directa cuando aplica)
- meta (meta description única)
- category: "general" | "seguros" | "ciudad"
- quick_answer: 40-60 palabras (lo que Google extrae como fragmento destacado)
- sections: lista de {h2, paragraphs, list_items?, table?}
- howto_steps: lista de {name, text} si aplica → añade schema HowTo
- faq: lista de (pregunta, respuesta)
- related: slugs relacionados
- city: nombre de ciudad si aplica (para posts locales)
"""

POSTS = [
    # ---------------- GENERALES ----------------
    {
        "slug": "que-hacer-despues-de-un-incendio",
        "title": "Qué hacer después de un incendio en casa: guía paso a paso",
        "meta": "Qué hacer después de un incendio en casa: pasos en las primeras 72 horas, contacto con el seguro, limpieza del hollín y eliminación del olor a humo.",
        "category": "general",
        "quick_answer": "Después de un incendio en casa: no entres sin permiso de bomberos, llama al seguro y haz fotos antes de tocar nada. Ventila con cuidado, no limpies hollín en seco con bayetas, retira textiles dañados y llama cuanto antes a una empresa especializada porque las primeras 72 horas son críticas.",
        "sections": [
            {"h2": "¿Por qué importan las primeras 72 horas?",
             "paragraphs": [
                "El hollín es ácido y empieza a fijarse en superficies porosas en cuestión de horas. Si pasas más de 72 horas sin tratarlo, las paredes, los techos, los plásticos y los textiles absorben el olor a humo de forma permanente y los metales se empiezan a corroer.",
                "Por eso lo primero no es limpiar: es proteger, documentar y llamar a quien sepa intervenir sin fijar más daño del que ya hay.",
             ]},
            {"h2": "Qué NO hacer",
             "paragraphs": [
                "Estos errores son los más caros tras un incendio en una vivienda:",
             ],
             "list_items": [
                "<strong>No limpies el hollín con un trapo húmedo.</strong> Lo fijas en la pared y deja una mancha que ya no sale.",
                "<strong>No conectes electrodomésticos</strong> hasta que el SAT confirme que es seguro.",
                "<strong>No pintes encima del hollín.</strong> El olor traspasa la pintura en días.",
                "<strong>No tires nada a la basura</strong> sin haberlo fotografiado para el seguro.",
                "<strong>No uses ambientadores</strong>: enmascaran pero no eliminan, y luego es peor.",
             ]},
        ],
        "howto_steps": [
            {"name": "Confirma con bomberos que se puede entrar", "text": "Solo cuando los bomberos certifican que la estructura es segura puedes acceder a la vivienda."},
            {"name": "Avisa al seguro en menos de 24 horas", "text": "Llama a tu compañía de seguros y abre el parte. Te asignarán perito."},
            {"name": "Haz fotos generales y de detalle antes de mover nada", "text": "Una serie por estancia, otra por daño concreto. Sirven para el perito y para la empresa de limpieza."},
            {"name": "Ventila con cuidado, sin corrientes fuertes", "text": "Las corrientes fuertes esparcen el hollín a habitaciones sin daño. Mejor ventanas semiabiertas."},
            {"name": "Llama a una empresa especializada en limpieza tras incendio", "text": "Cuanto antes intervengan, menos pierdes. Pide presupuesto cerrado y memoria para el seguro."},
            {"name": "No vuelvas a dormir en la vivienda hasta haber neutralizado el olor", "text": "El olor a humo concentrado es tóxico. Espera a la entrega final con ozonización completada."},
        ],
        "faq": [
            ("¿Cuánto tarda la limpieza tras un incendio doméstico?",
             "Entre 2 y 10 días según el tamaño: una cocina pequeña suele estar lista en 2-3 días, un piso completo entre 5 y 10."),
            ("¿La cubre el seguro?",
             "En la mayoría de pólizas de hogar, sí. Te entregamos la memoria que pide el perito."),
            ("¿Y si solo se ha quemado una habitación?",
             "Trabajamos por estancias: aislamos la zona afectada, descontaminamos y limpiamos el hollín que se haya extendido al resto."),
        ],
        "related": ["como-eliminar-olor-humo", "limpieza-hollin-paredes", "seguro-cubre-limpieza-incendio"],
    },
    {
        "slug": "como-eliminar-olor-humo",
        "title": "Cómo eliminar el olor a humo después de un incendio",
        "meta": "Cómo eliminar el olor a humo tras un incendio: por qué los ambientadores no funcionan, qué es la ozonización y cuándo llamar a profesionales.",
        "category": "general",
        "quick_answer": "Para eliminar el olor a humo después de un incendio, primero hay que retirar todo el hollín de paredes, techos, conductos y textiles, y después aplicar ozonización o tratamiento con hidroxilo en cada estancia. Los ambientadores y la pintura no eliminan el olor: lo enmascaran y vuelve a los pocos días.",
        "sections": [
            {"h2": "Por qué vuelve el olor a humo aunque hayas limpiado",
             "paragraphs": [
                "El olor a humo no está solo en las superficies visibles. Se mete dentro de la pared (yeso poroso), en los huecos de armarios, en los conductos del aire acondicionado, en el interior de los muebles y, sobre todo, en los textiles. Si limpias solo lo que ves, en 3-5 días el olor regresa.",
                "Por eso una limpieza tras incendio bien hecha trata la estancia completa, no la mancha.",
             ]},
            {"h2": "Qué es la ozonización (y por qué funciona)",
             "paragraphs": [
                "El ozono (O₃) oxida las moléculas de humo a nivel químico. No las tapa: las destruye. Se aplica con un generador en una estancia cerrada, sin personas ni mascotas dentro, durante varias horas. Tras el tratamiento se ventila y el olor neutro vuelve.",
                "El hidroxilo es una alternativa más lenta pero compatible con presencia humana. Lo usamos en locales que no pueden cerrarse del todo.",
             ]},
            {"h2": "Qué hacer con la ropa y los textiles",
             "list_items": [
                "Sofás, alfombras y colchones: tratamiento con extracción húmeda + ozonización.",
                "Ropa: lavado especializado a temperatura controlada (no en seco normal).",
                "Cortinas: si son de fibra natural, casi siempre recuperables; si son sintéticas, valorar.",
                "Peluches y textiles de niños: tratamiento individual o sustitución según contaminación.",
             ]},
        ],
        "faq": [
            ("¿Cuánto dura la ozonización de un piso?",
             "Entre 6 y 24 horas por estancia, según la concentración de olor."),
            ("¿Es peligroso el ozono?",
             "Sí si hay personas o animales dentro durante el tratamiento. Por eso solo lo aplican profesionales."),
            ("¿Y si solo huele un poco?",
             "Aun así trátalo. El olor leve se vuelve a fijar con la humedad y reaparece más fuerte."),
        ],
        "related": ["limpieza-hollin-paredes", "como-limpiar-ropa-humo", "que-hacer-despues-de-un-incendio"],
    },
    {
        "slug": "limpieza-hollin-paredes",
        "title": "Cómo limpiar el hollín de paredes y techos sin fijar la mancha",
        "meta": "Cómo limpiar el hollín de paredes y techos tras un incendio: técnica seca, productos específicos y errores que dejan la mancha para siempre.",
        "category": "general",
        "quick_answer": "El hollín de paredes y techos se limpia primero en seco con esponjas químicas tipo chemsponge, después con productos desengrasantes específicos en capas finas, y nunca con bayeta húmeda en primer pase. Si se moja antes de retirar la capa seca, el hollín se fija al yeso y solo se va con pintura nueva sobre imprimación selladora.",
        "sections": [
            {"h2": "Por qué la bayeta húmeda es el peor enemigo",
             "paragraphs": [
                "El hollín está formado por partículas finísimas de carbono con grasa quemada. Si pasas un trapo mojado, lo conviertes en barro y lo empujas dentro de los poros del yeso. A partir de ahí, ya no hay producto que lo saque sin levantar la pintura.",
                "El primer pase siempre tiene que ser en seco: esponja química o microfibra seca, retirando capas hasta dejar la superficie limpia de polvo de hollín.",
             ]},
            {"h2": "Proceso correcto",
             "paragraphs": ["Esto es lo que hacemos en cada vivienda:"],
             "list_items": [
                "Protección de suelos y muebles que no van a tocarse.",
                "Aspirado HEPA del polvo de hollín suelto.",
                "Limpieza en seco con esponja química (chemsponge) en techos y paredes.",
                "Lavado con desengrasante específico solo cuando la capa seca está retirada.",
                "Imprimación selladora si el hollín fue muy intenso o si quedan zonas con olor.",
             ]},
            {"h2": "Cuándo hace falta repintar y cuándo no",
             "paragraphs": [
                "Si el hollín no penetró (incendio breve, paredes pintadas con plástico): basta con limpieza seca + lavado y queda como nueva.",
                "Si el hollín se fijó (incendio intenso, paredes en gotelé o yeso poroso): se limpia, se aplica imprimación selladora antihollín y luego se repinta.",
                "Si la pared está calcinada: hay que picar y reponer. Eso ya no es limpieza, es obra.",
             ]},
        ],
        "faq": [
            ("¿Vale el quitamanchas normal del supermercado?",
             "No. Necesitas un desengrasante específico para hollín, normalmente con base alcalina."),
            ("¿Y el ozono limpia las paredes?",
             "No. El ozono neutraliza el olor pero no retira la mancha. Primero limpieza, después ozono."),
        ],
        "related": ["como-eliminar-olor-humo", "que-hacer-despues-de-un-incendio"],
    },
    {
        "slug": "cuanto-cuesta-limpieza-tras-incendio",
        "title": "Cuánto cuesta una limpieza tras incendio en una vivienda",
        "meta": "Cuánto cuesta una limpieza tras incendio: rangos de precio por tipo (cocina, piso, local), qué incluye un presupuesto serio y cómo lo cubre el seguro.",
        "category": "general",
        "quick_answer": "Una limpieza tras incendio cuesta entre 800 y 3.000 euros para una cocina, entre 2.500 y 8.000 para un piso completo y entre 5.000 y 30.000 para un local o nave, según superficie y tipo de hollín. En la mayoría de pólizas de hogar el coste lo cubre el seguro con la memoria que entrega la empresa.",
        "sections": [
            {"h2": "Qué hace variar el precio",
             "list_items": [
                "Superficie afectada y nivel de hollín.",
                "Tipo de combustión: cocina (grasa) vs eléctrica (carbón seco) vs sintéticos (pegajoso).",
                "Necesidad o no de retirar textiles y mobiliario para tratamiento aparte.",
                "Número de estancias que necesitan ozonización.",
                "Si hace falta limpieza de fachada o trasteros además de la vivienda.",
             ]},
            {"h2": "Rangos orientativos (vivienda)",
             "table": [
                ("Tipo", "Rango habitual", "Plazo"),
                ("Cocina pequeña con hollín local", "800 – 1.500 €", "1-2 días"),
                ("Cocina con propagación a salón", "1.500 – 3.000 €", "2-3 días"),
                ("Piso completo con hollín y olor", "2.500 – 8.000 €", "5-10 días"),
                ("Vivienda grande / chalet", "6.000 – 15.000 €", "1-3 semanas"),
                ("Local comercial pequeño", "3.000 – 8.000 €", "3-7 días"),
                ("Nave industrial", "Desde 8.000 €", "Según superficie"),
             ]},
            {"h2": "Qué debe incluir un presupuesto serio",
             "list_items": [
                "Visita técnica gratuita previa.",
                "Desglose por estancias y por concepto.",
                "Memoria con fotos antes/después para el seguro incluida.",
                "Tratamiento de olor (ozono/hidroxilo) incluido.",
                "Garantía: si pasadas 48h hay olor residual, vuelta sin coste.",
                "Plazo cerrado de ejecución.",
             ]},
        ],
        "faq": [
            ("¿Hay que pagar la visita técnica?",
             "No. La visita y el presupuesto son gratis y sin compromiso."),
            ("¿Quién paga si lo cubre el seguro?",
             "Tú adelantas o pagamos contra la aseguradora, según la póliza. Lo dejamos claro antes."),
        ],
        "related": ["seguro-cubre-limpieza-incendio", "documentacion-perito-seguros"],
    },
    {
        "slug": "limpiar-vivienda-quemada-por-donde-empezar",
        "title": "Necesito limpiar una vivienda quemada: por dónde empezar",
        "meta": "Necesito limpiar una vivienda quemada: por dónde empezar paso a paso, qué priorizar y cuándo llamar a una empresa de limpieza tras incendio.",
        "category": "general",
        "quick_answer": "Si necesitas limpiar una vivienda quemada, no empieces por lo más visible. El orden correcto es: confirmar acceso seguro, hacer fotos completas, separar lo recuperable de lo perdido, ventilar sin corrientes y llamar a una empresa de limpieza tras incendio antes de tocar el hollín. Improvisar fija la mancha y multiplica el coste.",
        "sections": [
            {"h2": "Prioridades por estancia",
             "list_items": [
                "<strong>Cocina:</strong> casi siempre el foco. Desengrase de campana, muebles altos, azulejos y techos.",
                "<strong>Salón y dormitorios:</strong> lo afectado suele ser el olor y el hollín fino. Estancia por estancia.",
                "<strong>Baños:</strong> normalmente menos daño, pero los conductos pueden traer olor desde la cocina.",
                "<strong>Trasteros y armarios cerrados:</strong> a veces es donde más se concentra el olor por falta de ventilación.",
             ]},
            {"h2": "Qué se recupera y qué no",
             "paragraphs": [
                "Recuperable casi siempre: paredes, techos, suelos, mobiliario de melamina, azulejos, electrodomésticos exteriores tras revisión SAT.",
                "Recuperable con tratamiento: ropa, sofás, alfombras, cortinas, colchones (en muchos casos sí).",
                "Habitualmente no recuperable: alimentos abiertos, plásticos blandos derretidos, productos cosméticos y medicamentos expuestos al humo, mobiliario calcinado, electrónica con humo en el interior.",
             ]},
        ],
        "howto_steps": [
            {"name": "Confirma que es seguro entrar", "text": "Solo si bomberos lo autorizan. Si no, espera."},
            {"name": "Inventario fotográfico", "text": "Foto general por estancia + foto detalle de cada daño antes de mover nada."},
            {"name": "Separa lo evidentemente perdido", "text": "Saca a un punto de la vivienda (no a la basura) lo claramente irrecuperable, anotándolo."},
            {"name": "Llama a la empresa de limpieza", "text": "Pide visita técnica y presupuesto cerrado antes de tocar el hollín."},
            {"name": "Mientras llegamos, ventila con suavidad", "text": "Ventanas semiabiertas, sin corrientes que esparzan el hollín a otras estancias."},
        ],
        "faq": [
            ("¿Puedo dormir en la vivienda mientras se limpia?",
             "Mejor no. El hollín suelto y los productos de limpieza no son compatibles con permanencia continua."),
            ("¿Necesito que esté el dueño durante el trabajo?",
             "Solo al principio (visita técnica y presupuesto) y al final (entrega). El resto del tiempo trabajamos con llaves."),
        ],
        "related": ["que-hacer-despues-de-un-incendio", "cuanto-cuesta-limpieza-tras-incendio"],
    },
    {
        "slug": "como-limpiar-ropa-humo",
        "title": "Cómo limpiar la ropa con olor a humo después de un incendio",
        "meta": "Cómo limpiar la ropa con olor a humo tras un incendio: por qué la tintorería normal fija el olor y qué tratamientos sí funcionan.",
        "category": "general",
        "quick_answer": "La ropa con olor a humo después de un incendio no se limpia con tintorería normal: el perclo fija el olor para siempre. Lo correcto es lavarla a temperatura controlada con desodorizantes específicos y, en piezas delicadas, hacer ozonización antes del lavado. Las prendas con quemaduras visibles se descartan y se inventarían para el seguro.",
        "sections": [
            {"h2": "Por qué la tintorería habitual no sirve",
             "paragraphs": [
                "La limpieza en seco convencional utiliza percloroetileno, que reacciona con las partículas de humo y las deja fijadas en la fibra. Es el error más caro: cuando lo ves no tiene marcha atrás. La ropa parece limpia, pero el olor dura años.",
             ]},
            {"h2": "Proceso recomendado",
             "list_items": [
                "Inventario y separación por tipo de fibra y nivel de contaminación.",
                "Pre-tratamiento con ozono en cámara para neutralizar el humo.",
                "Lavado especializado a temperatura controlada con desodorizantes específicos.",
                "Secado y control: si tras dos lavados el olor persiste, se descarta.",
             ]},
        ],
        "faq": [
            ("¿Y los abrigos y prendas que solo van a tinte?",
             "Pásalos por tratamiento especializado antes de cualquier limpieza en seco. Nunca al revés."),
            ("¿Se cubre por el seguro?",
             "Sí, normalmente como continente o como contenido según la póliza."),
        ],
        "related": ["como-eliminar-olor-humo", "que-hacer-despues-de-un-incendio"],
    },
    # ---------------- CLÚSTER SEGUROS ----------------
    {
        "slug": "seguro-cubre-limpieza-incendio",
        "title": "¿La limpieza tras incendio la cubre el seguro?",
        "meta": "¿La limpieza tras incendio la cubre el seguro? Qué dicen las pólizas de hogar y comunidad y cómo presentar la documentación para que paguen sin trabas.",
        "category": "seguros",
        "quick_answer": "En la mayoría de pólizas de hogar y comunidad, la limpieza tras incendio está cubierta como parte de la garantía de daños por incendio, siempre que se presente memoria con fotos antes/después y desglose por estancias. La empresa de limpieza entrega esa documentación lista para el perito, lo que acelera el pago del seguro.",
        "sections": [
            {"h2": "Qué cubre la garantía de incendio",
             "list_items": [
                "Daños directos del fuego.",
                "Daños del humo y el hollín.",
                "Daños por el agua o productos de extinción.",
                "Limpieza, desescombro y descontaminación post-incendio.",
                "En algunas pólizas, alojamiento alternativo si la vivienda no es habitable.",
             ]},
            {"h2": "Qué pide el perito normalmente",
             "list_items": [
                "Parte abierto en menos de 7 días desde el siniestro (mejor 24h).",
                "Fotos generales y de detalle de los daños.",
                "Presupuesto desglosado de la limpieza.",
                "Memoria final con fotos antes/después por estancia.",
                "Inventario de bienes muebles afectados.",
             ]},
        ],
        "faq": [
            ("¿Y si el seguro pone problemas?",
             "Lo más habitual es que pidan más documentación. Por eso entregamos memoria lista y fotos por estancia desde el inicio."),
            ("¿Hay franquicia?",
             "Depende de la póliza. Lo revisas con tu mediador antes de aceptar el presupuesto."),
        ],
        "related": ["documentacion-perito-seguros", "como-reclamar-seguro-incendio", "plazos-seguro-incendio"],
    },
    {
        "slug": "documentacion-perito-seguros",
        "title": "Qué documentación pide el perito de seguros tras un incendio",
        "meta": "Qué documentación pide el perito de seguros tras un incendio: lista exacta de papeles, fotos y memorias que aceleran el pago.",
        "category": "seguros",
        "quick_answer": "El perito de seguros tras un incendio pide: parte abierto en compañía, copia de la póliza, fotos generales y de detalle de los daños, presupuesto desglosado de la limpieza y reparaciones, inventario de bienes afectados y, si hubo bomberos, copia del atestado. Una empresa de limpieza profesional entrega la mayor parte de esa documentación lista.",
        "sections": [
            {"h2": "Documentos del asegurado",
             "list_items": [
                "Parte abierto en la compañía.",
                "Copia de la póliza vigente.",
                "DNI y datos bancarios para el cobro.",
                "Si hay alquiler: contrato vigente.",
                "Si hay terceros afectados (vecinos, comunidad): datos de contacto.",
             ]},
            {"h2": "Documentos que entrega la empresa de limpieza",
             "list_items": [
                "Presupuesto desglosado por estancias y por concepto.",
                "Memoria técnica con fotos antes/después.",
                "Inventario de bienes retirados o tratados.",
                "Factura con concepto detallado al cierre.",
                "Certificado de descontaminación si se solicita.",
             ]},
        ],
        "faq": [
            ("¿En qué formato entregáis la memoria?",
             "PDF con índice por estancias, foto antes y foto después de cada zona y resumen ejecutivo de una página para el perito."),
            ("¿Cuándo se entrega?",
             "Al finalizar la limpieza, junto con la factura."),
        ],
        "related": ["seguro-cubre-limpieza-incendio", "como-reclamar-seguro-incendio"],
    },
    {
        "slug": "como-reclamar-seguro-incendio",
        "title": "Cómo reclamar al seguro después de un incendio",
        "meta": "Cómo reclamar al seguro después de un incendio paso a paso: plazos, documentación y cómo presentar la memoria para que paguen rápido.",
        "category": "seguros",
        "quick_answer": "Para reclamar al seguro después de un incendio: abre parte en menos de 7 días (mejor 24h), guarda todas las fotos antes de mover nada, encarga la limpieza a una empresa que entregue memoria por estancias, presenta esa memoria con el presupuesto al perito y, si la compañía retrasa el pago, presenta queja formal y acude al Servicio de Reclamaciones del Banco de España.",
        "sections": [
            {"h2": "Pasos para una reclamación rápida",
             "paragraphs": ["Cuanto más limpio llega el expediente al perito, antes paga la compañía."],
            },
        ],
        "howto_steps": [
            {"name": "Abre el parte cuanto antes", "text": "Llama a tu compañía en las primeras 24 horas. Da fecha, hora aproximada y descripción breve del siniestro."},
            {"name": "Documenta antes de tocar nada", "text": "Fotos generales y de detalle por estancia. Si bomberos intervinieron, pide copia del atestado."},
            {"name": "Encarga la limpieza con memoria incluida", "text": "Trabaja con una empresa que entregue memoria por estancias y fotos antes/después."},
            {"name": "Presenta el expediente al perito", "text": "Memoria + presupuesto + inventario + fotos = expediente listo."},
            {"name": "Si tarda en pagar, presenta queja formal", "text": "Por escrito al Servicio de Atención al Cliente de la aseguradora; si no responden en 2 meses, al Banco de España."},
        ],
        "faq": [
            ("¿Qué plazo tiene el seguro para pagar?",
             "40 días desde la presentación completa del expediente, según la Ley de Contrato de Seguro."),
            ("¿Y si no estoy conforme con el peritaje?",
             "Puedes pedir un segundo perito a tu cargo o un tercero por desacuerdo."),
        ],
        "related": ["seguro-cubre-limpieza-incendio", "documentacion-perito-seguros", "plazos-seguro-incendio"],
    },
    {
        "slug": "seguro-hogar-vs-comunidad-incendio",
        "title": "Diferencias entre seguro de hogar y seguro de comunidad ante un incendio",
        "meta": "Diferencias entre seguro de hogar y seguro de comunidad ante un incendio: quién paga qué, cómo se reparten los daños y qué hacer si afecta a varios vecinos.",
        "category": "seguros",
        "quick_answer": "Ante un incendio, el seguro de comunidad cubre los elementos comunes del edificio (estructura, fachadas, zaguán) y el seguro de hogar cubre el interior de la vivienda y los bienes muebles. Si hay daños cruzados a vecinos, intervienen ambas pólizas a la vez y el perito reparte responsabilidades.",
        "sections": [
            {"h2": "Qué cubre cada uno",
             "list_items": [
                "<strong>Seguro de comunidad:</strong> elementos comunes (fachada, escalera, ascensor, cubierta), responsabilidad civil de la comunidad.",
                "<strong>Seguro de hogar (continente):</strong> elementos fijos de la vivienda (paredes, suelos, instalaciones, baños y cocina fijos).",
                "<strong>Seguro de hogar (contenido):</strong> muebles, ropa, electrodomésticos, objetos personales.",
                "<strong>Responsabilidad civil del hogar:</strong> daños causados a vecinos si el incendio se originó en tu vivienda.",
             ]},
            {"h2": "Qué hacer si afecta a más de un vecino",
             "paragraphs": [
                "Cada afectado abre su propio parte en su compañía. La administración de la comunidad coordina al perito de la comunidad y, en daños cruzados, las aseguradoras llegan a acuerdos entre ellas mediante el convenio CIDE/ASCIDE de responsabilidad civil.",
                "Lo importante: no esperes a saber quién paga. Empieza la limpieza con la empresa especializada y deja que las aseguradoras se entiendan después.",
             ]},
        ],
        "faq": [
            ("¿Y si el incendio empezó en una zona común?",
             "Lo cubre el seguro de comunidad. Cada vecino afectado abre paralelamente su parte por daños propios."),
            ("¿Quién paga el alojamiento mientras se limpia?",
             "Si tu póliza de hogar incluye esa garantía, ella. Si no, depende del origen del siniestro."),
        ],
        "related": ["seguro-cubre-limpieza-incendio", "como-reclamar-seguro-incendio"],
    },
    {
        "slug": "seguro-no-cubre-limpieza-incendio",
        "title": "Qué hacer si el seguro no cubre la limpieza tras incendio",
        "meta": "Qué hacer si el seguro no cubre la limpieza tras incendio: revisa las cláusulas, pide informe pericial alternativo y financia el trabajo por fases si es necesario.",
        "category": "seguros",
        "quick_answer": "Si el seguro no cubre la limpieza tras incendio, primero revisa las cláusulas exactas que aplican y pide reclamación por escrito al Servicio de Atención al Cliente. En paralelo, prioriza la intervención: empieza por lo crítico (cocina y baño) y deja lo estético para una segunda fase. Una empresa profesional siempre puede planificar en etapas.",
        "sections": [
            {"h2": "Causas habituales de denegación",
             "list_items": [
                "Negligencia probada (por ejemplo, dejar olla en fuego desatendida).",
                "Causa excluida en póliza (incendio intencional, sobrecargas de instalación no homologada).",
                "Falta de mantenimiento de instalaciones eléctricas o de gas.",
                "Retraso en avisar a la compañía.",
             ]},
            {"h2": "Qué puedes hacer",
             "list_items": [
                "Pedir el motivo exacto de denegación por escrito.",
                "Presentar reclamación formal al SAC de la aseguradora.",
                "Acudir al Defensor del Asegurado y, después, al Banco de España.",
                "Encargar peritaje independiente que contradiga el de la aseguradora.",
                "Planificar la limpieza en fases si el coste pesa.",
             ]},
        ],
        "faq": [
            ("¿Vale la pena pelearlo?",
             "Casi siempre sí. Una buena memoria técnica revierte muchas denegaciones iniciales."),
            ("¿Cuánto tarda una reclamación?",
             "El SAC tiene 2 meses; el Banco de España resuelve en 6-12 meses."),
        ],
        "related": ["seguro-cubre-limpieza-incendio", "como-reclamar-seguro-incendio"],
    },
    {
        "slug": "plazos-seguro-incendio",
        "title": "Plazos del seguro tras un incendio: cuándo recibirás el pago",
        "meta": "Plazos del seguro tras un incendio: cuánto tardan en venir el perito, en pagar y en cerrar el siniestro. Cómo acortar los tiempos.",
        "category": "seguros",
        "quick_answer": "Tras un incendio, el seguro envía al perito en 3-7 días, emite informe en 2-4 semanas y paga en hasta 40 días desde el expediente completo, según la Ley de Contrato de Seguro. El plazo se acorta si presentas memoria con fotos antes/después y presupuesto desglosado desde el inicio.",
        "sections": [
            {"h2": "Tabla de plazos típicos",
             "table": [
                ("Hito", "Plazo legal", "Plazo real"),
                ("Aviso a compañía", "7 días desde el siniestro", "Mejor en 24h"),
                ("Visita del perito", "—", "3-7 días"),
                ("Informe pericial", "—", "2-4 semanas"),
                ("Anticipo del 50%", "40 días desde aviso", "Si hay urgencia, pídelo"),
                ("Pago final", "40 días desde expediente completo", "Llega en 30-60 días"),
             ]},
            {"h2": "Cómo acortar los plazos",
             "list_items": [
                "Abrir parte en menos de 24h.",
                "Memoria + presupuesto + fotos antes/después en el primer envío.",
                "Empresa de limpieza que se comunique directamente con el perito.",
                "Pedir anticipo del 50% como permite la Ley de Contrato de Seguro.",
             ]},
        ],
        "faq": [
            ("¿Y si no pagan en 40 días?",
             "La compañía debe intereses del artículo 20 de la LCS, que son moratorios al 20% anual."),
        ],
        "related": ["como-reclamar-seguro-incendio", "documentacion-perito-seguros"],
    },
    # ---------------- CIUDAD ----------------
    {
        "slug": "como-limpiar-hollin-madrid",
        "title": "Cómo limpiar el hollín en Madrid: claves para pisos del Ensanche y bloques de los 70",
        "meta": "Cómo limpiar el hollín en Madrid: técnicas específicas según el tipo de vivienda madrileña, cuándo llamar a profesionales y plazos en cocinas pequeñas.",
        "category": "ciudad",
        "city": "Madrid",
        "quick_answer": "Para limpiar el hollín en Madrid, la clave está en la antigüedad del edificio: en pisos del Ensanche o de los años 60-70 con yeso poroso y patios interiores estrechos, el hollín se propaga rápido entre vecinos. Lo correcto es aislar la estancia, limpiar en seco con esponja química y aplicar ozonización en cada habitación afectada.",
        "sections": [
            {"h2": "Por qué Madrid tiene casuística propia",
             "paragraphs": [
                "Madrid mezcla fincas clásicas del Ensanche con muchos bloques de los 60-70 y vivienda nueva en barrios como Valdebebas. Cada arquitectura plantea retos distintos: en los edificios antiguos, los patios de luces y las cajas de escalera estrechas hacen que el humo afecte a vecinos sin tocar su vivienda directamente.",
                "Por eso en Madrid trabajamos mucho con comunidades de propietarios y administradores de fincas, no solo con propietarios particulares.",
             ]},
            {"h2": "Recomendación por barrios",
             "list_items": [
                "<strong>Centro y Salamanca:</strong> mucho yeso poroso, ozonización imprescindible.",
                "<strong>Tetuán, Carabanchel, Vallecas:</strong> bloques con conductos de gas comunes, atención al riesgo de propagación.",
                "<strong>Chamartín y Chamberí:</strong> fincas señoriales, textiles de calidad que conviene tratar y no descartar.",
                "<strong>Periferia (Vicálvaro, Villaverde):</strong> casas más nuevas, limpieza más rápida.",
             ]},
        ],
        "faq": [
            ("¿En cuánto tiempo podéis estar en Madrid?",
             "Si nos avisas antes de las 18h, normalmente el mismo día."),
            ("¿Trabajáis con administradores de fincas?",
             "Sí, es buena parte de los siniestros que atendemos en Madrid."),
        ],
        "related": ["limpieza-hollin-paredes", "que-hacer-despues-de-un-incendio"],
    },
    {
        "slug": "limpieza-incendio-barcelona-eixample",
        "title": "Limpieza tras incendio en Barcelona: claves del Eixample y los patios de luces",
        "meta": "Limpieza tras incendio en Barcelona: cómo trabajamos en fincas del Eixample, locales de Gràcia y bloques industriales reconvertidos.",
        "category": "ciudad",
        "city": "Barcelona",
        "quick_answer": "En Barcelona, la limpieza tras incendio en el Eixample tiene dos retos: los patios de luces estrechos propagan el hollín entre vecinos y los techos altos con molduras dificultan la limpieza en seco. Se trabaja por estancias, con andamios ligeros para techos y ozonización completa de la caja de escalera si fue afectada.",
        "sections": [
            {"h2": "Particularidades de Barcelona",
             "paragraphs": [
                "Las fincas modernistas del Eixample y de Gràcia conservan techos altos, molduras y suelos hidráulicos. Un incendio en una cocina puede afectar a estos elementos delicados, que no se limpian igual que un techo de placa lisa.",
                "Además, los patios de luces y los huecos de escalera estrechos hacen que el humo suba a viviendas que no se vieron directamente afectadas por el fuego.",
             ]},
        ],
        "faq": [
            ("¿Limpiáis suelos hidráulicos?",
             "Sí, con productos compatibles que no dañan la pátina."),
            ("¿Atendéis L'Hospitalet, Badalona y Sant Cugat?",
             "Sí, tenemos landings específicas para esos municipios."),
        ],
        "related": ["limpieza-hollin-paredes", "que-hacer-despues-de-un-incendio"],
    },
    {
        "slug": "incendio-vivienda-turistica-malaga",
        "title": "Qué hacer tras un incendio en una vivienda turística en Málaga",
        "meta": "Qué hacer tras un incendio en una vivienda turística en Málaga: pasos para volver a alquilar rápido, gestión del seguro y limpieza profunda.",
        "category": "ciudad",
        "city": "Málaga",
        "quick_answer": "Tras un incendio en una vivienda turística en Málaga, la prioridad es doble: gestionar el siniestro con el seguro y volver a alquilar cuanto antes para no perder reservas de temporada. Se hace limpieza acelerada por estancias, ozonización rápida y entrega de memoria al seguro en paralelo al trabajo de limpieza.",
        "sections": [
            {"h2": "Particularidades de la vivienda turística",
             "paragraphs": [
                "En Málaga, gran parte de la vivienda turística está concentrada en zonas como Centro Histórico, Pedregalejo o la Costa del Sol. Un incendio en una de estas viviendas implica cancelaciones inmediatas y pérdida de ingresos por noche.",
                "Por eso planificamos el trabajo en turnos ampliados, priorizando estancias críticas (cocina, dormitorios, baño principal) para que el dueño pueda relistar el alojamiento en plataformas en cuanto la primera fase esté lista.",
             ]},
            {"h2": "Coordinación con plataformas y huéspedes",
             "list_items": [
                "Entrega de informe técnico que sirve para justificar cancelaciones en Airbnb/Booking.",
                "Plan por fases para reabrir habitaciones progresivamente si es posible.",
                "Memoria final para reclamar lucro cesante al seguro si la póliza lo cubre.",
             ]},
        ],
        "faq": [
            ("¿En cuánto tiempo está lista una vivienda turística estándar?",
             "Un apartamento de 60-80 m² suele estar listo en 3-5 días con turnos extendidos."),
            ("¿Cubrís Marbella, Mijas, Fuengirola?",
             "Sí, todos los municipios principales de la provincia."),
        ],
        "related": ["que-hacer-despues-de-un-incendio", "como-eliminar-olor-humo"],
    },
]

CATEGORY_LABEL = {
    "general": "Guía general",
    "seguros": "Seguros",
    "ciudad": "Por ciudad",
}
