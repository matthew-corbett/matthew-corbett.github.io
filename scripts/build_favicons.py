from pathlib import Path

from PIL import Image, ImageDraw

repo = Path(__file__).resolve().parents[1]
logo_svg = repo / "assets" / "logo_r1qaJQiri6sK3rPyq-Sar.svg"
(repo / "favicon.svg").write_text(logo_svg.read_text(encoding="utf-8"), encoding="utf-8")

try:
    import cairosvg

    png = cairosvg.svg2png(bytestring=logo_svg.read_bytes(), output_width=180, output_height=180)
    base = Image.open(__import__("io").BytesIO(png)).convert("RGBA")
except Exception:
    # Fallback: simple brand mark if SVG rasterizer unavailable
    size = 180
    base = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(base)
    draw.ellipse((18, 18, size - 18, size - 18), fill="#4A4EFA")
    draw.ellipse((52, 52, size - 52, size - 52), fill="#E63CFE")
    draw.ellipse((78, 78, size - 78, size - 78), fill="#39FBBB")

for px, name in [(16, "favicon-16x16.png"), (32, "favicon-32x32.png"), (180, "apple-touch-icon.png")]:
    base.resize((px, px), Image.LANCZOS).save(repo / name, optimize=True)

icos = [base.resize((s, s), Image.LANCZOS) for s in (16, 32, 48)]
icos[0].save(
    repo / "favicon.ico",
    format="ICO",
    sizes=[(16, 16), (32, 32), (48, 48)],
    append_images=icos[1:],
)
print("personal site favicons built")
