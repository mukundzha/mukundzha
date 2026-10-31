# hero

`hero-light.svg` and `hero-dark.svg` are a 22-second animated typographic intro.
They are pure SMIL: no JavaScript, no CSS, no external fonts, so GitHub renders them
as ordinary images and the animation loops in place.

`generate.py` builds both files from the same layout. Edit `COPY` near the top to change
the words, or `PALETTES` to tune the light and dark themes, then:

```bash
pip install pillow
python3 hero/generate.py
```

Every glyph is its own `<text>` with a fixed `textLength`, so the layout stays put
across operating systems while individual letters type, assemble and fade.
