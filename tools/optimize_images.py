#!/usr/bin/env python3
"""Convierte las fotos grandes de /assets/ a WebP optimizado.

Estrategia:
- Redimensiona a max 1600px de lado mayor (suficiente para retina hasta 800px CSS)
- WebP quality 82 (sweet spot calidad/tamaño)
- Mantiene originales (.jpg/.png) por si se necesitan en redes sociales,
  documentos, etc.
- Skip si ya existe el .webp y es más nuevo que el origen.

Resultado típico: 1,5 MB JPG -> ~80-150 KB WebP.
"""
from __future__ import annotations

from pathlib import Path
from PIL import Image

ROOT = Path(__file__).parent.parent
ASSETS = ROOT / "assets"
# Los originales grandes viven fuera de /assets/ para NO publicarse en el sitio
# (GitHub Pages sirve todo el repo). El .webp optimizado sí se escribe en /assets/.
SOURCES = ROOT / "source-images"

# Lista explícita de imágenes a optimizar (las que se usan como contenido
# en INTERVENCIONES, HERO_POOL y otras fotos grandes). NO incluye el logo
# (que es marca) ni los logos de aseguradoras (que ya son pequeños).
PHOTOS = [
    "1759851783934.jpg", "1759851834214.jpg", "1759851918028.jpg",
    "1759851974041.jpg", "1759851980235.jpg", "1759852160572.jpg",
    "1759852290735.jpg",
    "Limpieza Incendioss Comunidades.jpg",
    "Limpieza de incendios en Oficina.png",
    "Limpieza de incendios madrid (1).png",
    "limpieza post incendios.png",
    # Nuevas fotos propias subidas por el cliente (octubre 2025)
    "operario-limpieza-hollin-tras-incendio.jpg",
    "cuadro-electrico-calcinado-tras-incendio.jpg",
    "television-derretida-pared-vivienda-incendio.jpg",
    "azulejos-hollin-cocina-incendiada.jpg",
    "escalera-comunidad-hollin-tras-incendio.jpg",
    "pared-escalera-vecinos-hollin-incendio.jpg",
    "limpieza-pared-piedra-hollin-chimenea.jpg",
]

MAX_SIDE = 1600
QUALITY = 82

def convert_one(path: Path) -> tuple[int, int]:
    # El origen vive en source-images/; el .webp se escribe en assets/.
    out = ASSETS / (path.stem + ".webp")
    if out.exists() and out.stat().st_mtime > path.stat().st_mtime:
        return path.stat().st_size, out.stat().st_size
    img = Image.open(path).convert("RGB")
    w, h = img.size
    scale = min(MAX_SIDE / max(w, h), 1.0)
    if scale < 1.0:
        img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
    img.save(out, "WEBP", quality=QUALITY, method=6)
    return path.stat().st_size, out.stat().st_size


def main() -> None:
    print(f"Optimizando {len(PHOTOS)} fotos a WebP (max {MAX_SIDE}px, q={QUALITY})…\n")
    total_before = total_after = 0
    for name in PHOTOS:
        src = SOURCES / name
        if not src.exists():
            print(f"  ⚠ no existe: {name}")
            continue
        before, after = convert_one(src)
        total_before += before
        total_after += after
        ratio = (1 - after / before) * 100
        print(f"  {name[:50]:50s}  {before//1024:5d} KB → {after//1024:4d} KB  (-{ratio:.0f}%)")
    print()
    print(f"Total: {total_before//1024//1024} MB → {total_after//1024} KB "
          f"(-{(1 - total_after / total_before) * 100:.1f}%)")


if __name__ == "__main__":
    main()
