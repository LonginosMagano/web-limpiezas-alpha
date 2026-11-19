"""Contenido local escrito a mano por landing.

Cada fichero `tools/contenido_local/<slug_con_guiones_bajos>.py` define un dict
`CONTENIDO` que sustituye los bloques rotados de la landing correspondiente
(`/limpieza-despues-de-incendio-<slug>/`). Si no existe fichero, la landing se
genera como siempre. Claves admitidas (todas opcionales salvo `cuerpo`):

- title, h1, meta:   sustituyen a los generados (el title se ajusta a 30-60).
- intro:             párrafo de apertura (la keyword natural en los primeros
                     100 caracteres, lo exige qa.py).
- cuerpo:            lista de (subtitulo_h3 | None, [párrafos]) bajo
                     "Qué hacemos en {ciudad} tras un incendio".
- zonas:             párrafo de "Zonas de cobertura".
- zonas_lista:       lista de (zona, texto corto) → <ul> debajo de `zonas`.
- faq:               lista de (pregunta, respuesta) propias de la ciudad.
"""
from __future__ import annotations

import importlib
from pathlib import Path

_DIR = Path(__file__).parent


def load_local(slug: str) -> dict | None:
    mod_name = slug.replace("-", "_")
    if not (_DIR / f"{mod_name}.py").exists():
        return None
    mod = importlib.import_module(f"contenido_local.{mod_name}")
    data = getattr(mod, "CONTENIDO", None)
    if not data or "cuerpo" not in data:
        raise ValueError(f"contenido_local/{mod_name}.py sin CONTENIDO['cuerpo']")
    return data
