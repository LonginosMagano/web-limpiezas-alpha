#!/usr/bin/env python3
"""Genera una OG image (1200x630) por cada post del blog y página clave.

Diseño:
- Fondo oscuro con resplandor naranja en una esquina
- Tira naranja vertical a la izquierda como acento de marca
- Título grande (wrapping automático)
- Eyebrow con la categoría / sección
- Brand y URL al pie
- Mini-logo placeholder con la letra A en círculo naranja

Salida: /assets/og/{slug}.webp (cada uno ~25-50 KB).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from data import BRAND, DOMAIN, KEYWORD
from posts import POSTS, CATEGORY_LABEL

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent.parent
OUT_DIR = ROOT / "assets" / "og"
OUT_DIR.mkdir(parents=True, exist_ok=True)

W, H = 1200, 630
BG = (11, 15, 20)         # #0b0f14
GLOW = (255, 107, 0)      # accent
INK = (247, 247, 244)     # #f7f7f4
MUTED = (203, 208, 212)   # #cbd0d4
ACCENT = (255, 107, 0)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines, cur = [], []
    for w in words:
        test = " ".join(cur + [w])
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            cur.append(w)
        else:
            if cur:
                lines.append(" ".join(cur))
            cur = [w]
    if cur:
        lines.append(" ".join(cur))
    return lines


def make_og(title: str, eyebrow: str, slug: str) -> Path:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Resplandor naranja en esquina superior derecha
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for r, alpha in [(450, 80), (320, 110), (220, 140), (140, 170), (80, 200)]:
        gd.ellipse((W - r - 40, -r // 2, W + r - 40, r + 80),
                   fill=(255, 107, 0, alpha))
    img.paste(Image.alpha_composite(
        Image.new("RGBA", (W, H), BG + (255,)),
        glow
    ).convert("RGB"))
    d = ImageDraw.Draw(img)

    # Banda vertical naranja izquierda (acento de marca)
    d.rectangle((0, 0, 14, H), fill=ACCENT)

    # Logo placeholder (círculo "A")
    cx, cy = 95, 80
    d.ellipse((cx - 32, cy - 32, cx + 32, cy + 32), fill=ACCENT)
    fa = ImageFont.truetype(FONT_BOLD, 38)
    d.text((cx, cy + 2), "A", font=fa, fill=(11, 5, 0), anchor="mm")

    # Brand name
    fb = ImageFont.truetype(FONT_BOLD, 22)
    d.text((140, cy + 2), BRAND, font=fb, fill=INK, anchor="lm")

    # Eyebrow
    fe = ImageFont.truetype(FONT_BOLD, 22)
    d.text((58, 195), eyebrow.upper(), font=fe, fill=ACCENT, anchor="lt")

    # Título (wrapping)
    ft = ImageFont.truetype(FONT_BOLD, 60)
    lines = wrap_text(d, title, ft, max_width=W - 130)
    # Limitar a 4 líneas (truncar con … si pasa)
    if len(lines) > 4:
        lines = lines[:4]
        if not lines[-1].endswith("…"):
            lines[-1] = lines[-1].rstrip(".,;:") + "…"
    y = 240
    for ln in lines:
        d.text((58, y), ln, font=ft, fill=INK, anchor="lt")
        y += 72

    # Footer con URL
    ff = ImageFont.truetype(FONT_REG, 22)
    domain_short = DOMAIN.replace("https://", "").rstrip("/")
    d.text((58, H - 50), domain_short, font=ff, fill=MUTED, anchor="lt")

    # Tira inferior de marca
    d.rectangle((0, H - 8, W, H), fill=ACCENT)

    out = OUT_DIR / f"{slug}.webp"
    img.save(out, "WEBP", quality=85, method=6)
    return out


def main() -> None:
    total_bytes = 0
    count = 0
    for post in POSTS:
        out = make_og(
            title=post["title"],
            eyebrow=CATEGORY_LABEL.get(post["category"], "Blog"),
            slug=post["slug"],
        )
        sz = out.stat().st_size
        total_bytes += sz
        count += 1
        print(f"  {out.name:50s} {sz // 1024:4d} KB")
    print(f"\n  {count} OG images · {total_bytes // 1024} KB total "
          f"(avg {total_bytes // count // 1024} KB)")


if __name__ == "__main__":
    main()
