"""Configuración de datos del sitio.

Mantener aquí: nombre de marca, dominio, teléfono, keyword principal,
listado de Comunidades Autónomas, provincias, municipios y barrios.
"""

BRAND = "Limpiezas de Incendios Alpha"
DOMAIN = "https://longinosmagano.github.io/web-limpiezas-alpha"
# Prefijo de las URLs internas cuando el sitio se sirve en un subdirectorio
# (como project page de GitHub Pages). Cambiar a "" si pasa a dominio propio.
BASE_PATH = "/web-limpiezas-alpha"
PHONE = "681811301"
PHONE_INTL = "34681811301"
EMAIL = "contacto@limpiezasdeincendiosalpha.com"
KEYWORD = "Limpieza Despues de Incendio"
KEYWORD_SLUG = "limpieza-despues-de-incendio"

# Pool de keywords secundarias / sinónimos del núcleo
KW_VARIANTS_NUCLEO = [
    "limpieza después de incendio",
    "limpieza tras incendio",
    "limpieza post incendio",
    "limpieza por incendio",
    "limpieza tras siniestro",
    "limpieza de hollín",
    "limpieza de humo",
    "limpieza de casas quemadas",
    "limpieza vivienda post incendio",
    "descontaminación tras incendio",
]

KW_SECUNDARIAS = [
    "empresa de limpieza de incendios", "limpieza local post incendio",
    "qué hacer después de un incendio", "limpieza de siniestros",
    "empresa urgente por incendio", "eliminar olor a humo",
    "limpieza de hollín en paredes", "quitar humo después de incendio",
    "ozonización tras incendio", "limpieza muebles ahumados",
    "limpieza de ropa con olor a humo", "valoración daños por incendio",
    "perito de seguros incendio", "limpieza profesional post fuego",
    "limpieza nave industrial incendiada",
    "limpieza cocina quemada", "limpieza tras incendio eléctrico",
    "descontaminación de hollín en mobiliario", "limpieza de paredes ahumadas",
    "limpieza tras incendio en comunidad de vecinos",
    "limpieza después de fuego en vivienda", "tratamiento de humo tras incendio",
    "limpieza textil después de incendio", "neutralizar olor a quemado",
    "limpieza tras incendio en restaurante", "limpieza de oficina post incendio",
    "limpieza chimenea con hollín", "intervención urgente tras incendio",
]

# 8 CCAA en el orden fijado por la especificación, con sus provincias.
CCAA = [
    ("Comunidad de Madrid", "comunidad-de-madrid", ["Madrid"]),
    ("Comunidad Valenciana", "comunidad-valenciana", ["Valencia", "Alicante", "Castellón"]),
    ("Región de Murcia", "region-de-murcia", ["Murcia"]),
    ("Andalucía", "andalucia",
     ["Sevilla", "Málaga", "Granada", "Córdoba", "Cádiz", "Almería", "Jaén", "Huelva"]),
    ("Castilla-La Mancha", "castilla-la-mancha",
     ["Toledo", "Ciudad Real", "Albacete", "Cuenca", "Guadalajara"]),
    ("Aragón", "aragon", ["Zaragoza", "Huesca", "Teruel"]),
    ("Castilla y León", "castilla-y-leon",
     ["Valladolid", "Salamanca", "León", "Burgos",
      "Palencia", "Zamora", "Ávila", "Segovia", "Soria"]),
    ("Cataluña", "cataluna", ["Barcelona", "Tarragona", "Girona", "Lleida"]),
]

# Municipios principales por provincia (clave: nombre de provincia)
MUNICIPIOS = {
    "Madrid": ["Móstoles", "Alcalá de Henares", "Fuenlabrada", "Leganés",
               "Getafe", "Alcorcón", "Torrejón de Ardoz", "Parla"],
    "Barcelona": ["L'Hospitalet de Llobregat", "Badalona", "Terrassa", "Sabadell",
                  "Mataró", "Santa Coloma de Gramenet", "Cornellà de Llobregat",
                  "Sant Cugat del Vallès"],
    "Valencia": ["Gandía", "Torrent", "Paterna", "Sagunto",
                 "Alzira", "Mislata", "Burjassot", "Xirivella"],
    "Sevilla": ["Dos Hermanas", "Alcalá de Guadaíra", "Utrera",
                "Mairena del Aljarafe", "Écija", "Los Palacios y Villafranca",
                "Lebrija", "Coria del Río"],
    "Málaga": ["Marbella", "Mijas", "Vélez-Málaga", "Fuengirola",
               "Torremolinos", "Benalmádena", "Estepona", "Antequera"],
    "Alicante": ["Elche", "Torrevieja", "Orihuela"],
    "Murcia": ["Cartagena", "Lorca", "Molina de Segura"],
    "Zaragoza": ["Calatayud", "Ejea de los Caballeros", "Utebo"],
    "Toledo": ["Talavera de la Reina", "Illescas", "Ocaña"],
    "Granada": ["Motril", "Almuñécar", "Baza"],
    "Córdoba": ["Lucena", "Puente Genil", "Montilla"],
}

# Barrios / distritos de Madrid
BARRIOS_MADRID = [
    "Salamanca", "Chamberí", "Chamartín", "Retiro", "Centro",
    "Arganzuela", "Moncloa-Aravaca", "Tetuán", "Latina", "Carabanchel",
    "Usera", "Puente de Vallecas", "Villa de Vallecas", "Vicálvaro",
    "Ciudad Lineal", "Hortaleza", "San Blas-Canillejas", "Barajas",
    "Fuencarral-El Pardo", "Moratalaz", "Villaverde",
]

# Alias de slug para casos especiales (apóstrofo, partícula "de", etc.)
SLUG_ALIAS = {
    "l'hospitalet de llobregat": "hospitalet",
    "cornellà de llobregat": "cornella",
    "sant cugat del vallès": "sant-cugat",
    "santa coloma de gramenet": "santa-coloma",
    "alcalá de henares": "alcala-de-henares",
    "alcalá de guadaíra": "alcala-de-guadaira",
    "los palacios y villafranca": "los-palacios",
    "ejea de los caballeros": "ejea-de-los-caballeros",
    "vélez-málaga": "velez-malaga",
    "moncloa-aravaca": "moncloa",
    "san blas-canillejas": "san-blas",
    "fuencarral-el pardo": "fuencarral",
    "puente de vallecas": "puente-de-vallecas",
    "villa de vallecas": "villa-de-vallecas",
}

# --- Fotos reales ----------------------------------------------------------
# Cards antes/después por ciudad para /galeria/ y para el hero de la landing.
# Las claves coinciden con el nombre exacto de la provincia/ciudad.
INTERVENCIONES = {
    "Madrid":    ("assets/Limpieza de incendios madrid (1).webp",    "assets/1759851918028.webp"),
    "Barcelona": ("assets/1759851783934.webp",                       "assets/1759852290735.webp"),
    "Valencia":  ("assets/1759851834214.webp",                       "assets/1759851918028.webp"),
    "Sevilla":   ("assets/1759851974041.webp",                       "assets/1759852290735.webp"),
    "Málaga":    ("assets/1759852160572.webp",                       "assets/1759851918028.webp"),
    "Zaragoza":  ("assets/Limpieza Incendioss Comunidades.webp",     "assets/1759852290735.webp"),
    "Murcia":    ("assets/Limpieza de incendios en Oficina.webp",    "assets/1759851918028.webp"),
    "Toledo":    ("assets/limpieza post incendios.webp",             "assets/1759852290735.webp"),
}

# Descripciones naturales de escena para los alts (rota por hash → cada
# landing recibe un alt único pero descriptivo, no keyword-stuffed).
# Los modelos de IA leen alt para entender qué hay en la imagen.
ALT_SCENES = [
    "Equipo retirando hollín y partículas de humo de pared tras incendio doméstico",
    "Cocina tras incendio en proceso de descontaminación con ozono",
    "Salón con muebles cubiertos antes de iniciar la limpieza profesional",
    "Vivienda lista tras finalizar la limpieza post incendio",
    "Operario aplicando producto desengrasante en techos ahumados",
    "Estancia entregada después del tratamiento de olor a humo",
    "Trabajos de limpieza profesional tras siniestro de cocina",
    "Detalle de pared sin manchas tras retirada del hollín",
    "Resultado final del tratamiento integral de descontaminación",
    "Cocina recuperada tras retirar el hollín de campana y muebles",
    "Estancia tras ozonización completa: olor a humo neutralizado",
]

# Pool de fotos sueltas para cyclar como hero en landings que no están
# en INTERVENCIONES. Se selecciona por hash(slug).
HERO_POOL = [
    "assets/1759851783934.webp",
    "assets/1759851834214.webp",
    "assets/1759851918028.webp",
    "assets/1759851974041.webp",
    "assets/1759851980235.webp",
    "assets/1759852160572.webp",
    "assets/1759852290735.webp",
    "assets/Limpieza Incendioss Comunidades.webp",
    "assets/Limpieza de incendios en Oficina.webp",
    "assets/Limpieza de incendios madrid (1).webp",
    "assets/limpieza post incendios.webp",
]

# Logos de aseguradoras con las que trabajamos (trust strip en home).
ASEGURADORAS = [
    ("Mutua Madrileña", "assets/Limpieza de incendios Mutua madrileña.png"),
    ("Mapfre",          "assets/limpieza de incendios maphre.png"),
    ("AXA",             "assets/limpieza de incendios axa.jpg"),
    ("Aegon",           "assets/limpieza de incendios aegon.png"),
]

# Se completa lo conocido; el generador usa textos genéricos cuando falta.
LOCAL_NOTES = {
    "Madrid": {
        "tipo": "mezcla de fincas clásicas del ensanche y bloques de los 60-70",
        "rasgo": "alta densidad de comunidades de propietarios y administradores de fincas",
        "riesgo": "cocinas pequeñas en pisos antiguos y patios interiores que propagan el humo entre vecinos",
        "barrios": ["Centro", "Salamanca", "Chamberí", "Tetuán", "Vallecas", "Carabanchel"],
    },
    "Barcelona": {
        "tipo": "fincas modernistas del Eixample y edificios industriales reconvertidos",
        "rasgo": "viviendas con patios de luces estrechos y locales comerciales a pie de calle",
        "riesgo": "propagación de hollín por las cajas de escalera de los edificios antiguos",
        "barrios": ["Eixample", "Gràcia", "Sant Martí", "Sants", "Sant Andreu"],
    },
    "Valencia": {
        "tipo": "bloques de la huerta y casas bajas de barrios periféricos",
        "rasgo": "mucha vivienda con cocina de gas y locales hosteleros",
        "riesgo": "incendios de cocina por aceite y campanas saturadas",
        "barrios": ["Ruzafa", "El Carmen", "Benimaclet", "Patraix"],
    },
    "Sevilla": {
        "tipo": "viviendas de patio andaluz y casas bajas en barrios como Triana",
        "rasgo": "altas temperaturas que aceleran la concentración de olores",
        "riesgo": "incendios eléctricos por sobrecarga de aires acondicionados en verano",
        "barrios": ["Triana", "Macarena", "Nervión", "Los Remedios"],
    },
    "Málaga": {
        "tipo": "mezcla de casco histórico y urbanizaciones de costa",
        "rasgo": "alta presencia de viviendas turísticas y apartamentos en altura",
        "riesgo": "incendios en cocinas de pisos vacacionales y locales hosteleros",
        "barrios": ["Centro Histórico", "El Palo", "Pedregalejo", "Teatinos"],
    },
    "Zaragoza": {
        "tipo": "bloques de los 70 en barrios como Delicias y vivienda nueva en Valdespartera",
        "rasgo": "fuerte presencia de polígonos industriales y naves logísticas",
        "riesgo": "incendios eléctricos en cuadros de cuadros antiguos y olor persistente por la humedad del Ebro",
    },
    "Murcia": {
        "tipo": "viviendas unifamiliares en pedanías y bloques en el centro",
        "rasgo": "huerta y polígonos cercanos al casco urbano",
        "riesgo": "incendios en garajes, almacenes agrícolas y locales comerciales",
    },
    "Alicante": {
        "tipo": "torres de apartamentos en costa y vivienda tradicional en el casco",
        "rasgo": "fuerte componente turístico y residencias de temporada",
        "riesgo": "incendios en apartamentos vacacionales, normalmente detectados con retraso",
    },
    "Toledo": {
        "tipo": "casco histórico de piedra y bloques en los polígonos exteriores",
        "rasgo": "muchas viviendas con estructura de madera en el centro histórico",
        "riesgo": "incendios en chimeneas y cuadros eléctricos antiguos",
    },
    "Granada": {
        "tipo": "carmenes del Albaicín, viviendas en la Vega y bloques modernos",
        "rasgo": "casas con estructura mixta de madera y forjado tradicional",
        "riesgo": "incendios por braseros, estufas y cocinas con poca ventilación",
    },
    "Córdoba": {
        "tipo": "patios cordobeses, casas bajas y barrios de bloques nuevos",
        "rasgo": "núcleo urbano denso con calles estrechas que dificultan la intervención rápida",
        "riesgo": "incendios eléctricos por instalaciones antiguas en la judería y el casco",
    },
}
