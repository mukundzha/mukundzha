#!/usr/bin/env python3
"""Build nebula-light.svg and nebula-dark.svg for the profile README.

A soft, animated gradient background with floating, gently drifting text.
Pure SMIL: no JavaScript, no CSS, no external fonts, so GitHub renders
them as ordinary images and the animation loops in place.

Edit COLOURS near the top to change the gradient stops, then:

```bash
pip install pillow
python3 hero/generate.py
```

Every element uses fixed positions so the layout stays put across
operating systems while individual words drift and fade.
"""

from pathlib import Path
import html

W, H = 900, 400
DUR = 20.0

# colour palettes
COLOURS = {
    "light": {
        "bg_top": "#f0f8ff",
        "bg_bot": "#e6f7ff",
        "accent": "#1e3a5f",
        "ink": "#0c1a2e",
        "muted": "#5a7a9e",
        "glow": "#2b6cb2",
    },
    "dark": {
        "bg_top": "#0a0a20",
        "bg_bot": "#102030",
        "accent": "#39ff14",
        "ink": "#e0e0e8",
        "muted": "#6a8aa0",
        "glow": "#57ccff",
    },
}

EASE = "cubic-bezier(0.4, 0, 0.2, 1)"

def esc(value):
    return html.escape(str(value), quote=True)

def anim(attr, points, dur=DUR, begin=None):
    times, values, eases = [], [], []
    for index, point in enumerate(points):
        t, value, *ease = point
        ease = ease[0] if ease else "lin"
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
    key_times = ";".join(
        f"{t:.6f}".rstrip("0").rstrip(".") or "0" for t in times
    )
    splines = ";".join(EASE for _ in eases[:-1])
    begin_attr = f' begin="{begin}s"' if begin is not None else ""
    return (
        f'<animate attributeName="{attr}" values="{";".join(values)}" '
        f'keyTimes="{key_times}" dur="{DUR}s" repeatCount="indefinite"'
        f' begin="{begin}s" calcMode="spline" keySplines="{splines}"/>'
    )

def static_text(content, x, y, font_size, colour, font_family, **kwargs):
    attrs = [
        f'x="{x}"',
        f'y="{y}"',
        f'font-size="{font_size}"',
        f'fill="{colour}"',
        f'font-family="{font_family}"',
    ]
    if "tracking" in kwargs:
        attrs.append(f'letter-spacing="{kwargs["tracking"]}"')
    if "anchor" in kwargs:
        attrs.append(f'dominant-baseline="middle"')
        attrs.append(f'text-anchor="{kwargs["anchor"]}"')
    d = " ".join(attrs)
    return f'<text {d}>{esc(content)}</text>'

def build(theme):
    c = COLOURS[theme]
    bg_top = c["bg_top"]
    bg_bot = c["bg_bot"]
    accent = c["accent"]
    ink = c["ink"]
    muted = c["muted"]
    glow = c["glow"]

    lines = []

    lines.append(f'<defs>')
    lines.append(
        f'  <linearGradient id="bgGrad" x1="0%" y1="0%" x2="0%" y2="100%">'
    )
    lines.append(f'    <stop offset="0%" stop-color="{bg_top}"/>')
    lines.append(f'    <stop offset="100%" stop-color="{bg_bot}"/>')
    lines.append(f"  </linearGradient>")
    lines.append(f"</defs>")

    words = [
        ("MUKUND", 400, 80, 20),
        ("JHA", 460, 70, 10),
        ("BUILDS", 320, 260, 15),
        ("CALM", 380, 290, 12),
        ("TOOLS", 440, 310, 18),
        ("FOR", 120, 340, 25),
        ("TERMINAL", 180, 370, 22),
        ("ENJOYERS", 250, 395, 16),
    ]

    for i, (word, x, y, size) in enumerate(words):
        drift = -0.8 if i % 2 == 0 else 0.8
        begin = i * 1.5
        lines.append(
            f'<g id="word{i}" transform="translate({x},{y})">'
        )
        lines.append(
            f'  <animateTransform '
            f' attributeName="transform" '
            f'type="translate" '
            f'values="0; {drift * 100}; 0; {-drift * 100}" '
            f'keyTimes="0; 0.25; 0.5; 1" '
            f'dur="{DUR}s" repeatCount="indefinite" '
            f'begin="{begin}s" calcMode="spline" '
            f'keySplines="cubic-bezier(0.4,0,0.2,1)"/>'
        )
        lines.append(
            f'  <animate '
            f' attributeName="opacity" '
            f'values="0.6; 1; 0.6" '
            f'keyTimes="0; 0.5; 1" '
            f'dur="{DUR}s" repeatCount="indefinite" '
            f'begin="{begin}s"/>'
        )
        lines.append(
            static_text(word, 0, 0, size, ink, "'Segoe UI', system-ui, sans-serif", anchor="start")
        )
        lines.append(f"  </g>")

    # dark theme words (same positions, swapped in SVG via CSS-like approach)
    # We'll just repeat with different begin offsets
    for i, (word, x, y, size) in enumerate(words):
        drift = 0.7 if i % 2 == 0 else -0.7
        begin = i * 1.5 + 0.5
        lines.append(
            f'<g id="word{i}" transform="translate({x},{y})">'
        )
        lines.append(
            f'  <animateTransform '
            f' attributeName="transform" '
            f'type="translate" '
            f'values="0; {drift * 100}; 0; {-drift * 100}" '
            f'keyTimes="0; 0.25; 0.5; 1" '
            f'dur="{DUR}s" repeatCount="indefinite" '
            f'begin="{begin}s" calcMode="spline" '
            f'keySplines="cubic-bezier(0.4,0,0.2,1)"/>'
        )
        lines.append(
            f'  <animate '
            f' attributeName="opacity" '
            f'values="0.5; 1; 0.5" '
            f'keyTimes="0; 0.5; 1" '
            f'dur="{DUR}s" repeatCount="indefinite" '
            f'begin="{begin}s"/>'
        )
        lines.append(
            static_text(word, 0, 0, size, ink, "'Segoe UI', system-ui, sans-serif", anchor="start")
        )
        lines.append(f"  </g>")

    # accent glow orb
    lines.append(f'<g>')
    lines.append(
        f'  <circle cx="850" cy="340" r="60" fill="none" stroke="{accent}" '
        f'stroke-width="1" opacity="0.4">'
    )
    lines.append(
        f'    <animate attributeName="r" values="60;80;60" keyTimes="0;0.5;1" '
        f'dur="{DUR}s" repeatCount="indefinite" calcMode="spline" keySplines="{EASE}"/>'
    )
    lines.append(
        f'    <animate attributeName="opacity" values="0.4;0.8;0.4" keyTimes="0;0.5;1" '
        f'dur="{DUR}s" repeatCount="indefinite" calcMode="spline" keySplines="{EASE}"/>'
    )
    lines.append(f"  </circle>")
    lines.append(f"</g>")

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" font-family="\'Segoe UI\', system-ui, sans-serif" '
        f'role="img">'
    )
    svg += f'<title>Mukund Jha — animated nebula profile README</title>'
    svg += f'<desc>'
    svg += (
        f'An animated gradient background with drifting words, '
        f'for dark and light GitHub themes.'
    )
    svg += f"</desc>"
    svg += f'<rect width="{W}" height="{H}" fill="url(#bgGrad)"/>'
    svg += "".join(lines)
    svg += f"</svg>"
    return svg

def main():
    root = Path(__file__).resolve().parent
    for theme in ("light", "dark"):
        svg = build(theme)
        path = root / f"nebula-{theme}.svg"
        path.write_text(svg, encoding="utf-8")
        size_kb = len(svg) / 1024
        print(f"{path.name}: {size_kb:.1f} KiB")

if __name__ == "__main__":
    main()
