"""Generate SAAC LinkedIn banner 1584x396 — dev monospace, LinkedIn-safe."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1584, 396
BG = (13, 17, 23)
CYAN = (56, 189, 248)
WHITE = (248, 250, 252)
GRAY = (148, 163, 184)
GRID = (30, 41, 59)
GREEN = (34, 197, 94)
BORDER = (51, 65, 85)

DIR = Path(__file__).resolve().parent
OUT_PNG = DIR / "SAAC_LinkedIn_Banner.png"
OUT_JPG = DIR / "SAAC_LinkedIn_Banner.jpg"


def load_mono(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for name in ("CascadiaMono.ttf", "consola.ttf", "lucon.ttf", "cour.ttf"):
        path = Path("C:/Windows/Fonts") / name
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def draw_terminal_box(draw: ImageDraw.ImageDraw, xy: tuple, label: str) -> None:
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=8, outline=BORDER, width=2, fill=(17, 24, 39))
    for i, c in enumerate((GREEN, (234, 179, 8), (239, 68, 68))):
        draw.ellipse([(x1 + 14 + i * 18, y1 + 12), (x1 + 24 + i * 18, y1 + 22)], fill=c)
    draw.text((x1 + 78, y1 + 8), label, font=load_mono(14), fill=GRAY)


def main() -> None:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    for x in range(0, W, 40):
        draw.line([(x, 0), (x, H)], fill=GRID, width=1)
    for y in range(0, H, 40):
        draw.line([(0, y), (W, y)], fill=GRID, width=1)

    draw.rectangle([(0, H - 3), (W, H)], fill=GREEN)

    font_huge = load_mono(108)
    font_title = load_mono(34)
    font_kw = load_mono(30)
    font_tag = load_mono(26)

    # Left: terminal block (clear of profile photo ~ bottom-left)
    box = (200, 52, 720, H - 52)
    draw_terminal_box(draw, box, "saac-framework")
    bx, by = box[0] + 28, box[1] + 44
    draw.text((bx, by), "SAAC", font=font_huge, fill=WHITE)
    draw.text((bx, by + 108), "SEO As A Code", font=font_title, fill=CYAN)
    draw.text((bx, by + 148), "> ready_", font=load_mono(22), fill=GRAY)

    # Right: pipeline
    keywords = "GSC | GA4 | CrUX | AI SEO"
    tagline = "// data -> diagnose -> prioritize"
    bbox = draw.textbbox((0, 0), keywords, font=font_kw)
    kw_w = bbox[2] - bbox[0]
    x_kw = W - kw_w - 64
    y_kw = H // 2 - 42
    draw.text((x_kw, y_kw), keywords, font=font_kw, fill=WHITE)
    bbox2 = draw.textbbox((0, 0), tagline, font=font_tag)
    tg_w = bbox2[2] - bbox2[0]
    draw.text((W - tg_w - 64, y_kw + 46), tagline, font=font_tag, fill=CYAN)

    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT_PNG, format="PNG")
    img.save(OUT_JPG, format="JPEG", quality=92, optimize=True, subsampling=0)

    with Image.open(OUT_PNG) as check:
        check.load()
        print(f"PNG: {OUT_PNG} ({check.size[0]}x{check.size[1]}, {OUT_PNG.stat().st_size} B)")
    print(f"JPG: {OUT_JPG} ({OUT_JPG.stat().st_size} B) — usa este si LinkedIn rechaza PNG")


if __name__ == "__main__":
    main()
