from pathlib import Path

from PIL import Image, ImageDraw

repo = Path(__file__).resolve().parents[1]
logo_svg = repo / "assets" / "logo_r1qaJQiri6sK3rPyq-Sar.svg"
(repo / "favicon.svg").write_text(logo_svg.read_text(encoding="utf-8"), encoding="utf-8")


def draw_mc_mark(size: int) -> Image.Image:
    """Crisp navy/green MC mark scaled to `size` px."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    s = size / 64.0

    def sx(x: float) -> float:
        return x * s

    def sy(y: float) -> float:
        return y * s

    def poly(points):
        return [(sx(x), sy(y)) for x, y in points]

    radius = int(14 * s)
    draw.rounded_rectangle((0, 0, size - 1, size - 1), radius=radius, fill="#0f1419")

    # M — filled polygon approximating the SVG path
    m = [
        (12, 46),
        (12, 18),
        (17.2, 18),
        (23.1, 34.6),
        (29, 18),
        (34.2, 18),
        (34.2, 46),
        (29.4, 46),
        (29.4, 28.4),
        (24.2, 43.2),
        (21.0, 43.2),
        (15.8, 28.4),
        (15.8, 46),
    ]
    draw.polygon(poly(m), fill="#4a7c59")

    # C — approximate with thick arc stroke via pie wedges + cover
    # Outer ring-ish C using polygon along median path
    c = [
        (48.8, 25.2),
        (45.2, 22.7),
        (42.0, 21.5),
        (38.5, 21.5),
        (35.2, 22.7),
        (32.8, 25.2),
        (31.3, 28.4),
        (31.0, 32.0),
        (31.0, 34.4),
        (31.3, 38.0),
        (32.8, 41.2),
        (35.2, 43.7),
        (38.5, 44.9),
        (42.0, 44.9),
        (45.2, 43.7),
        (48.8, 41.2),
        (45.2, 38.7),
        (43.3, 40.2),
        (41.3, 40.9),
        (39.2, 40.9),
        (37.2, 40.2),
        (35.8, 38.7),
        (34.9, 36.7),
        (34.6, 34.4),
        (34.6, 32.0),
        (34.9, 29.7),
        (35.8, 27.7),
        (37.2, 26.2),
        (39.2, 25.5),
        (41.3, 25.5),
        (43.3, 26.2),
        (45.2, 27.7),
    ]
    draw.polygon(poly(c), fill="#4a7c59")

    bar_w = 28 * s
    bar_h = max(2, 3 * s)
    bx0 = (size - bar_w) / 2
    by0 = 50 * s
    draw.rounded_rectangle((bx0, by0, bx0 + bar_w, by0 + bar_h), radius=bar_h / 2, fill="#c4a35a")
    return img


base = draw_mc_mark(180)

for px, name in [(16, "favicon-16x16.png"), (32, "favicon-32x32.png"), (180, "apple-touch-icon.png")]:
    draw_mc_mark(px).save(repo / name, optimize=True)

icos = [draw_mc_mark(s) for s in (16, 32, 48)]
icos[0].save(
    repo / "favicon.ico",
    format="ICO",
    sizes=[(16, 16), (32, 32), (48, 48)],
    append_images=icos[1:],
)
print("personal site favicons built")
