#!/usr/bin/env python3
"""Build hero-light.svg and hero-dark.svg for the profile README.

Pure SMIL: no JavaScript, no CSS, no external fonts, so GitHub renders it.
Edit COPY, then run: python3 hero/generate.py
"""
from pathlib import Path
import html
import random

from PIL import ImageFont

W, H = 900, 310
T = 22.0

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
FONT_SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FONT_SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_MONO = "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"

COPY = dict(
    meta="MUKUND JHA  /  DIPAYAL, DOTI",
    headline=("hi, i’m ", "mukund", "."),
    line2=("i build calm tools for the ", "terminal", "."),
    tagline="TERMINAL ENJOYER & OPEN SOURCE MAINTAINER.",
    email="mukundzha33@gmail.com",
    site="github.com/mukundzha",
)

PALETTES = {
    "light": dict(
        bg="#fbfaf6", ink="#1c1d1a", muted="#87847c", faint="#e3ded3",
        accent="#b4552d", rain="#5c675f", glow="#c97a52",
        bloom=0.10, rain_opacity=0.11, highlight=0.11,
    ),
    "dark": dict(
        bg="#0b0d0c", ink="#f1efe8", muted="#8b938d", faint="#2a302c",
        accent="#e58a63", rain="#8fa198", glow="#e58a63",
        bloom=0.14, rain_opacity=0.15, highlight=0.14,
    ),
}

EASE = {
    "lin": "0 0 1 1",
    "out": "0.16 1 0.3 1",
    "in": "0.7 0 0.84 0",
    "inout": "0.65 0 0.35 1",
    "soft": "0.33 1 0.68 1",
}

HEAD_IN = 0.85
HEAD_STAGGER = 0.065
HEAD_MOVE = 0.30
BODY_IN = 2.65
BODY_STAGGER = 0.035
BODY_MOVE = 0.95
TAG_IN = 4.90
TAG_STAGGER = 0.018
TAG_MOVE = 0.80
HIN = 8.90
HOUT = 15.60
OUT_META = 18.75
OUT_HEAD = 18.90
OUT_BODY = 18.95
OUT_TAG = 19.05
OUT_FOOT = 18.80
OUT_LEN = 0.55


def esc(value):
    return html.escape(str(value), quote=True)


def n(value):
    text = f"{float(value):.2f}".rstrip("0").rstrip(".")
    return "0" if text in ("", "-0") else text


def anim(attr, points, dur=T, begin=None):
    times, values, eases = [], [], []
    for index, point in enumerate(points):
        t, value = point[0], point[1]
        ease = point[2] if len(point) > 2 else "lin"
        if times and t / dur <= times[-1]:
            t = times[-1] * dur + 0.001
        times.append(t / dur)
        values.append(str(value))
        eases.append(ease)
    if times[0] != 0:
        times.insert(0, 0.0)
        values.insert(0, values[0])
        eases.insert(0, "lin")
    if times[-1] != 1:
        times.append(1.0)
        values.append(values[-1])
        eases.append("lin")
    key_times = ";".join(f"{t:.6f}".rstrip("0").rstrip(".") or "0" for t in times)
    splines = ";".join(EASE[e] for e in eases[:-1])
    begin_attr = f' begin="{begin}s"' if begin is not None else ""
    return (
        f'<animate attributeName="{attr}" values="{";".join(values)}" '
        f'keyTimes="{key_times}" dur="{n(dur)}s" repeatCount="indefinite"{begin_attr} '
        f'calcMode="spline" keySplines="{splines}"/>'
    )


def tween(points, dur=T):
    times, values, eases = [], [], []
    for point in points:
        t, x, y = point[0], point[1], point[2]
        ease = point[3] if len(point) > 3 else "lin"
        if times and t / dur <= times[-1]:
            t = times[-1] * dur + 0.001
        times.append(t / dur)
        values.append(f"{n(x)} {n(y)}")
        eases.append(ease)
    if times[0] != 0:
        times.insert(0, 0.0)
        values.insert(0, values[0])
        eases.insert(0, "lin")
    if times[-1] != 1:
        times.append(1.0)
        values.append(values[-1])
        eases.append("lin")
    key_times = ";".join(f"{t:.6f}".rstrip("0").rstrip(".") or "0" for t in times)
    splines = ";".join(EASE[e] for e in eases[:-1])
    return (
        f'<animateTransform attributeName="transform" type="translate" '
        f'values="{";".join(values)}" keyTimes="{key_times}" dur="{n(dur)}s" '
        f'repeatCount="indefinite" calcMode="spline" keySplines="{splines}"/>'
    )


def measure(path, size, text):
    return ImageFont.truetype(path, size).getlength(text)


class Glyph:
    __slots__ = ("ch", "x", "y", "w", "weight", "index")

    def __init__(self, ch, x, y, w, weight, index):
        self.ch, self.x, self.y, self.w, self.weight, self.index = ch, x, y, w, weight, index


def layout_runs(runs, size, x, y):
    out = []
    cursor = x
    index = 0
    for text, weight in runs:
        path = FONT_SANS_B if weight >= 600 else FONT_SANS
        font = ImageFont.truetype(path, size)
        for i, ch in enumerate(text):
            advance = font.getlength(text[: i + 1]) - font.getlength(text[:i])
            if ch != " ":
                out.append(Glyph(ch, cursor, y, advance, weight, index))
            cursor += advance
            index += 1
    return out, cursor


def layout_mono(text, size, x, y, tracking):
    font = ImageFont.truetype(FONT_MONO, size)
    advance = font.getlength("M") + tracking
    out = []
    cursor = x
    for i, ch in enumerate(text):
        if ch != " ":
            out.append(Glyph(ch, cursor, y, font.getlength(ch), 400, i))
        cursor += advance
    return out, cursor - tracking


def glyph_svg(glyph, size, t_in, fade, dx=0.0, dy=0.0, move=None):
    move = fade if move is None else move
    opacity = anim(
        "opacity",
        [(0, 0, "lin"), (t_in, 0, "out"), (t_in + fade, 1, "lin"), (T, 1, "lin")],
    )
    transform = tween(
        [(0, dx, dy, "lin"), (t_in, dx, dy, "out"), (t_in + move, 0, 0, "lin"), (T, 0, 0, "lin")]
    )
    return (
        f'<g opacity="1">{opacity}{transform}'
        f'<text x="{n(glyph.x)}" y="{n(glyph.y)}" font-size="{n(size)}" '
        f'font-weight="{glyph.weight}" textLength="{n(glyph.w)}" '
        f'lengthAdjust="spacingAndGlyphs">{esc(glyph.ch)}</text></g>'
    )


def render_runs(runs, size, x, y, schedule, family=SANS):
    elements = []
    cursor = x
    index = 0
    for text, weight, fill, group_anims in runs:
        glyphs, end = layout_runs([(text, weight)], size, cursor, y)
        inner = []
        for glyph in glyphs:
            t_in, fade, dx, dy, move = schedule(index + glyph.index)
            inner.append(glyph_svg(glyph, size, t_in, fade, dx, dy, move))
        group_fill = f' fill="{fill}"' if fill else ""
        group_family = f' font-family="{family}"' if family else ""
        elements.append(f"<g{group_fill}{group_family}>{group_anims}{''.join(inner)}</g>")
        cursor = end
        index += len(text)
    return "".join(elements), cursor


def static_text(text, x, y, size, fill, family, weight=400, tracking=0, anchor="start"):
    attrs = (
        f'x="{n(x)}" y="{n(y)}" font-family="{family}" font-size="{n(size)}" '
        f'font-weight="{weight}" fill="{fill}"'
    )
    if tracking:
        attrs += f' letter-spacing="{n(tracking)}"'
    if anchor != "start":
        attrs += f' text-anchor="{anchor}"'
    return f"<text {attrs}>{esc(text)}</text>"


def defs(p):
    return (
        "<defs>"
        '<linearGradient id="rule" x1="0" x2="1" y1="0" y2="0">'
        f'<stop offset="0" stop-color="{p["accent"]}" stop-opacity="0.85"/>'
        f'<stop offset="0.12" stop-color="{p["faint"]}" stop-opacity="0"/>'
        f'<stop offset="0.5" stop-color="{p["faint"]}" stop-opacity="0.9"/>'
        f'<stop offset="1" stop-color="{p["faint"]}" stop-opacity="0"/>'
        "</linearGradient>"
        '<radialGradient id="bloom">'
        f'<stop offset="0" stop-color="{p["glow"]}" stop-opacity="0.70"/>'
        f'<stop offset="0.55" stop-color="{p["glow"]}" stop-opacity="0.18"/>'
        f'<stop offset="1" stop-color="{p["glow"]}" stop-opacity="0"/>'
        "</radialGradient>"
        '<clipPath id="page"><rect width="' + str(W) + '" height="' + str(H) + '"/></clipPath>'
        "</defs>"
    )


def rain(p):
    rng = random.Random(23)
    alphabet = "01{}[]<>/\\|=+-*&$#@?!:;.abcdefghijklmnopqrstuvwxyz"
    columns = []
    for column in range(13):
        x = 40 + column * 69 + rng.uniform(-13, 13)
        speed = rng.uniform(10.0, 19.0)
        offset = rng.uniform(0, speed)
        opacity = rng.uniform(0.35, 1.0)
        cells = []
        for _ in range(rng.randint(7, 10)):
            y = rng.uniform(0, H)
            ch = rng.choice(alphabet)
            fill = p["accent"] if rng.random() < 0.10 else p["rain"]
            cells.append((ch, y, fill))
        marks = "".join(
            f'<text x="{n(x)}" y="{n(y + shift)}" font-family="{MONO}" '
            f'font-size="9" fill="{fill}">{esc(ch)}</text>'
            for shift in (-H, 0, H)
            for ch, y, fill in cells
        )
        columns.append(
            f'<g opacity="{opacity:.2f}"><g>'
            f'<animateTransform attributeName="transform" type="translate" '
            f'values="0 0;0 {H}" dur="{n(speed)}s" begin="-{n(offset)}s" '
            f'repeatCount="indefinite"/>{marks}</g></g>'
        )
    opacity = anim(
        "opacity",
        [(0, 0, "lin"), (1.4, 0, "out"), (3.0, p["rain_opacity"], "lin"),
         (18.0, p["rain_opacity"], "in"), (19.7, 0, "lin"), (T, 0, "lin")],
    )
    return f'<g clip-path="url(#page)" opacity="0">{opacity}{"".join(columns)}</g>'


def glow(p):
    opacity = anim(
        "opacity",
        [(0, 0, "lin"), (1.6, 0, "inout"), (4.0, p["bloom"], "lin"),
         (17.2, p["bloom"], "inout"), (19.8, 0, "lin"), (T, 0, "lin")],
    )
    cx = anim("cx", [(0, 690, "inout"), (T / 2, 760, "inout"), (T, 690, "lin")])
    cy = anim("cy", [(0, 26, "inout"), (T / 2, 86, "inout"), (T, 26, "lin")])
    return f'<circle cx="690" cy="26" r="270" fill="url(#bloom)" opacity="0">{opacity}{cx}{cy}</circle>'


def build(theme):
    p = PALETTES[theme]
    head_words = COPY["headline"]
    body_pre, body_hi, body_post = COPY["line2"]

    meta = COPY["meta"]
    tagline = COPY["tagline"]

    head_runs = [
        (head_words[0], 400, p["ink"], ""),
        (head_words[1], 400, p["ink"], ""),
        (head_words[2], 400, p["accent"], ""),
    ]
    head_layout, _ = layout_runs([("".join(head_words), 400)], 46, 64, 136)
    head_glyphs, head_end = render_runs(
        head_runs, 46, 64, 136,
        lambda i: (HEAD_IN + i * HEAD_STAGGER, HEAD_MOVE, 0, 6, HEAD_MOVE),
    )

    body_runs = [
        (body_pre, 400, p["muted"], ""),
        (body_hi, 700, p["ink"],
         anim("fill", [(0, p["ink"], "lin"), (HIN, p["ink"], "out"),
                       (HIN + 0.35, p["accent"], "lin"), (HOUT, p["accent"], "in"),
                       (HOUT + 0.35, p["ink"], "lin"), (T, p["ink"], "lin")])),
        (body_post, 400, p["muted"], ""),
    ]
    body_glyphs_svg, _ = render_runs(
        body_runs, 22, 64, 180,
        lambda i: (BODY_IN + i * BODY_STAGGER, 0.50, 10 if i % 2 else -8, 17, BODY_MOVE),
    )

    _, pre_end = layout_runs([(body_pre, 400)], 22, 64, 180)
    _, hi_end = layout_runs([(body_hi, 700)], 22, pre_end, 180)
    hl_x = pre_end - 7
    hl_w = hi_end - pre_end + 14
    highlight = (
        f'<rect x="{n(hl_x)}" y="158" width="0" height="30" rx="5" '
        f'fill="{p["accent"]}" opacity="0">'
        + anim("width", [(0, 0, "lin"), (HIN, 0, "out"), (HIN + 0.6, hl_w, "lin"), (T, hl_w, "lin")])
        + anim("opacity", [(0, 0, "lin"), (HIN, 0, "out"), (HIN + 0.25, p["highlight"], "lin"),
                           (HOUT, p["highlight"], "in"), (HOUT + 0.4, 0, "lin"), (T, 0, "lin")])
        + "</rect>"
    )

    tag_glyphs, _ = layout_mono(tagline, 10.5, 64, 248, 2.6)
    tag_svg = "".join(
        glyph_svg(g, 10.5, TAG_IN + g.index * TAG_STAGGER, 0.45, 22, 5, TAG_MOVE)
        for g in tag_glyphs
    )
    tag_group = (
        f'<g fill="{p["muted"]}" font-family="{MONO}" opacity="1">'
        + anim("opacity", [(0, 1, "lin"), (OUT_TAG, 1, "in"), (OUT_TAG + OUT_LEN, 0, "lin"), (T, 0, "lin")])
        + tag_svg
        + "</g>"
    )

    headline = (
        '<g opacity="1">'
        + anim("opacity", [(0, 1, "lin"), (OUT_HEAD, 1, "in"), (OUT_HEAD + OUT_LEN, 0, "lin"), (T, 0, "lin")])
        + head_glyphs
        + "</g>"
    )

    caret_points = [(0, 64, "lin"), (0.72, 64, "lin")]
    for glyph in head_layout:
        caret_points.append(
            (min(HEAD_IN + glyph.index * HEAD_STAGGER + 0.06, T - 0.01),
             glyph.x + glyph.w + 2, "lin")
        )
    caret_points.append((T, head_end + 2, "lin"))
    caret_x = anim("x", caret_points)
    caret_opacity = anim(
        "opacity",
        [(0, 0, "lin"), (0.58, 0, "out"), (0.70, 1, "lin"), (2.34, 1, "in"),
         (2.44, 0, "lin"), (2.66, 0, "out"), (2.76, 1, "lin"), (2.98, 1, "in"),
         (3.08, 0, "lin"), (3.28, 0, "out"), (3.38, 1, "lin"), (3.52, 1, "in"),
         (3.64, 0, "lin"), (T, 0, "lin")],
    )
    caret = (
        f'<rect x="64" y="103" width="2.4" height="38" rx="1.2" fill="{p["accent"]}" opacity="0">'
        + caret_x + caret_opacity + "</rect>"
    )

    body = (
        '<g opacity="1">'
        + anim("opacity", [(0, 1, "lin"), (OUT_BODY, 1, "in"), (OUT_BODY + OUT_LEN, 0, "lin"), (T, 0, "lin")])
        + highlight
        + body_glyphs_svg
        + "</g>"
    )

    rule = (
        '<g opacity="1">'
        + anim("opacity", [(0, 0, "lin"), (3.9, 0, "out"), (4.35, 1, "lin"),
                           (OUT_HEAD, 1, "in"), (OUT_HEAD + OUT_LEN, 0, "lin"), (T, 0, "lin")])
        + f'<line x1="64" y1="212" x2="836" y2="212" stroke="{p["faint"]}" stroke-width="1">'
        + anim("x2", [(0, 64, "lin"), (3.9, 64, "out"), (4.85, 836, "lin"), (T, 836, "lin")])
        + "</line>"
        + f'<line x1="64" y1="212" x2="88" y2="212" stroke="{p["accent"]}" stroke-width="1" opacity="0.85">'
        + anim("x2", [(0, 64, "lin"), (3.9, 64, "out"), (4.25, 88, "lin"), (T, 88, "lin")])
        + "</line>"
        + "</g>"
    )

    meta_group = (
        '<g opacity="1">'
        + anim("opacity", [(0, 0, "lin"), (0.18, 0, "out"), (0.85, 1, "lin"),
                           (OUT_META, 1, "in"), (OUT_META + OUT_LEN, 0, "lin"), (T, 0, "lin")])
        + f'<circle cx="66" cy="37" r="3" fill="{p["accent"]}">'
        + anim("opacity", [(0, 0.45, "inout"), (1.8, 0.9, "inout"), (3.6, 0.45, "lin")], dur=3.6)
        + "</circle>"
        + static_text(meta, 78, 41, 9.5, p["muted"], MONO, tracking=1.9)
        + "</g>"
    )

    footer = (
        '<g opacity="1">'
        + anim("opacity", [(0, 0, "lin"), (10.8, 0, "out"), (11.35, 1, "lin"),
                           (OUT_FOOT, 1, "in"), (OUT_FOOT + OUT_LEN, 0, "lin"), (T, 0, "lin")])
        + static_text(COPY["email"], 64, 286, 10, p["muted"], MONO, tracking=0.4)
        + static_text(COPY["site"] + " \u2197", 836, 286, 10, p["muted"], MONO, tracking=0.4, anchor="end")
        + "</g>"
    )

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" font-family="{SANS}" role="img">'
        f"<title>{esc('hi, i am mukund')}</title>"
        f"<desc>{esc('An animated typographic introduction: hi, I am Mukund. I build calm tools for the terminal. Terminal enjoyer and open source maintainer.')}</desc>"
        + defs(p)
        + f'<rect width="{W}" height="{H}" fill="{p["bg"]}"/>'
        + rain(p)
        + glow(p)
        + meta_group
        + caret
        + headline
        + body
        + rule
        + tag_group
        + footer
        + "</svg>"
    )


def main():
    root = Path(__file__).resolve().parent
    for theme in ("light", "dark"):
        svg = build(theme)
        path = root / f"hero-{theme}.svg"
        path.write_text(svg, encoding="utf-8")
        print(f"{path.name}: {len(svg) / 1024:.1f} KiB")


if __name__ == "__main__":
    main()
