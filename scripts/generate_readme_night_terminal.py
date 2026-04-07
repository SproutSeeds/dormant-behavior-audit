#!/usr/bin/env python3
"""Generate a minimal starry-night terminal animation for the GitHub README."""

from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "benchmarks" / "public" / "assets"
OUT_PATH = OUT_DIR / "readme-night-terminal.gif"

WIDTH = 960
HEIGHT = 540
FRAMES = 72
FRAME_MS = 140

BACKGROUND_TOP = (4, 8, 22)
BACKGROUND_BOTTOM = (10, 18, 44)
STAR_BASE = (190, 212, 255)
TERMINAL_BG = (7, 12, 24, 225)
TERMINAL_BORDER = (111, 130, 170, 120)
TEXT_PRIMARY = (226, 236, 255)
TEXT_MUTED = (136, 158, 196)
TEXT_ACCENT = (139, 213, 175)
TEXT_SOFT = (150, 170, 220)


LINES = [
    ("$ open benchmarks/BENCHMARK_CHARTER.md", TEXT_ACCENT),
    ("  benchmark-first, evidence-rich, local-first", TEXT_MUTED),
    ("$ inspect benchmarks/reference/dormant_puzzle_v1", TEXT_ACCENT),
    ("  reference bundle online: claims, evidence, validation", TEXT_SOFT),
    ("$ python3 scripts/reproduce_submission.py", TEXT_ACCENT),
    ("  replay complete -> compare claim_consistency_report.md", TEXT_MUTED),
    ("$ package release assets", TEXT_ACCENT),
    ("  report, scoreboard, collaboration brief, release notes", TEXT_SOFT),
]


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/SFNSMono.ttf",
        "/Library/Fonts/Andale Mono.ttf",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def lerp(a: int, b: int, t: float) -> int:
    return round(a + (b - a) * t)


def gradient_background() -> Image.Image:
    image = Image.new("RGBA", (WIDTH, HEIGHT))
    pixels = image.load()
    for y in range(HEIGHT):
        t = y / (HEIGHT - 1)
        color = tuple(lerp(BACKGROUND_TOP[i], BACKGROUND_BOTTOM[i], t) for i in range(3)) + (255,)
        for x in range(WIDTH):
            pixels[x, y] = color
    return image


def build_stars(seed: int = 7) -> list[dict[str, float]]:
    random.seed(seed)
    stars: list[dict[str, float]] = []
    for _ in range(85):
        stars.append(
            {
                "x": random.uniform(0, WIDTH),
                "y": random.uniform(0, HEIGHT),
                "r": random.uniform(0.8, 2.0),
                "phase": random.uniform(0, math.tau),
                "speed": random.uniform(0.25, 0.9),
                "alpha": random.uniform(0.18, 0.75),
            }
        )
    return stars


def draw_stars(base: Image.Image, stars: list[dict[str, float]], frame_idx: int) -> Image.Image:
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for star in stars:
        pulse = 0.55 + 0.45 * math.sin((frame_idx / FRAMES) * math.tau * star["speed"] + star["phase"])
        alpha = round(255 * star["alpha"] * pulse)
        fill = STAR_BASE + (alpha,)
        x, y, r = star["x"], star["y"], star["r"]
        draw.ellipse((x - r, y - r, x + r, y + r), fill=fill)
        if pulse > 0.92:
            glow_r = r * 3.2
            draw.ellipse(
                (x - glow_r, y - glow_r, x + glow_r, y + glow_r),
                fill=(140, 170, 255, round(alpha * 0.11)),
            )
    return Image.alpha_composite(base, overlay)


def terminal_box(frame: Image.Image) -> tuple[Image.Image, tuple[int, int, int, int]]:
    x0, y0, x1, y1 = 150, 118, 810, 422
    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.rounded_rectangle((x0 - 6, y0 - 6, x1 + 6, y1 + 6), radius=24, fill=(45, 78, 150, 60))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=10))
    frame = Image.alpha_composite(frame, glow)

    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.rounded_rectangle((x0, y0, x1, y1), radius=20, fill=TERMINAL_BG, outline=TERMINAL_BORDER, width=1)
    draw.rounded_rectangle((x0, y0, x1, y0 + 42), radius=20, fill=(15, 23, 43, 210))
    draw.rectangle((x0, y0 + 22, x1, y0 + 42), fill=(15, 23, 43, 210))

    for idx, color in enumerate(((252, 95, 86), (253, 188, 64), (45, 205, 112))):
        cx = x0 + 24 + idx * 18
        cy = y0 + 20
        draw.ellipse((cx - 5, cy - 5, cx + 5, cy + 5), fill=color + (230,))

    frame = Image.alpha_composite(frame, overlay)
    return frame, (x0, y0, x1, y1)


def line_progress(frame_idx: int, line_idx: int, text: str) -> int:
    start = 6 + line_idx * 8
    if frame_idx < start:
        return 0
    return min(len(text), max(0, (frame_idx - start) * 2))


def render_frame(base: Image.Image, stars: list[dict[str, float]], mono: ImageFont.ImageFont, sans: ImageFont.ImageFont, frame_idx: int) -> Image.Image:
    frame = draw_stars(base, stars, frame_idx)
    frame, (x0, y0, x1, y1) = terminal_box(frame)
    draw = ImageDraw.Draw(frame)

    draw.text((x0 + 265, y0 + 12), "dormant behavior audit // slow tour", font=sans, fill=TEXT_MUTED)

    draw.text((x0 + 34, y0 + 68), "night shift :: reproducible release path", font=sans, fill=(164, 187, 232))

    base_y = y0 + 110
    line_gap = 28
    cursor_line = None
    cursor_x = None
    cursor_y = None

    for idx, (text, color) in enumerate(LINES):
        visible = line_progress(frame_idx, idx, text)
        if visible == 0:
            continue
        shown = text[:visible]
        y = base_y + idx * line_gap
        draw.text((x0 + 36, y), shown, font=mono, fill=color)
        if visible < len(text):
            cursor_line = idx
            bbox = draw.textbbox((x0 + 36, y), shown, font=mono)
            cursor_x = bbox[2] + 2
            cursor_y = y
            break

    if cursor_line is None and frame_idx < FRAMES - 8:
        for idx, (text, _color) in reversed(list(enumerate(LINES))):
            if line_progress(frame_idx, idx, text) >= len(text):
                y = base_y + idx * line_gap
                bbox = draw.textbbox((x0 + 36, y), text, font=mono)
                cursor_x = bbox[2] + 2
                cursor_y = y
                break

    if cursor_x is not None and cursor_y is not None and (frame_idx // 3) % 2 == 0:
        draw.rectangle((cursor_x, cursor_y + 4, cursor_x + 10, cursor_y + 22), fill=(185, 232, 207))

    draw.text(
        (x0 + 36, y1 - 48),
        "charter -> reference bundle -> reproduction -> claim checks -> release",
        font=sans,
        fill=TEXT_MUTED,
    )

    return frame.convert("P", palette=Image.ADAPTIVE, colors=96)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    mono = load_font(21)
    sans = load_font(16)
    base = gradient_background()
    stars = build_stars()
    frames = [render_frame(base, stars, mono, sans, idx) for idx in range(FRAMES)]
    frames[0].save(
        OUT_PATH,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_MS,
        loop=0,
        optimize=True,
        disposal=2,
    )
    print(f"Saved {OUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
