#!/usr/bin/env python3
"""Convert a Loopixel 4-direction walk sheet (4 rows x 8 frames, any Loopixel size) to an RPG Maker MV/MZ
single-character sheet (3 columns x 4 rows of 48px = 144x192). MIT licensed.

Loopixel row order : front(down), right, back(up), left
RPG Maker row order: down, left, right, up

Cell size is read from the sheet (width / 8). Best input is sprite_48.png from the ZIP (native 48px, no
scaling); 32/64/96/128px sheets are nearest-neighbour scaled to 48px.

Usage: python3 loopixel_to_rpgmaker.py sprite_48.png out.png [--frames 0,2,4]
Name the output with a leading "$" (e.g. $Hero.png) so RPG Maker treats it as a single character.
"""
import argparse
from PIL import Image

OUT_CELL = 48
LOOPIXEL_ROWS = {"down": 0, "right": 1, "up": 2, "left": 3}
RPGM_ORDER = ["down", "left", "right", "up"]


def convert(src, dst, frames):
    sheet = Image.open(src).convert("RGBA")
    CELL = sheet.size[0] // 8
    if CELL < 1 or sheet.size[0] % 8 or sheet.size[1] != 4 * CELL:
        raise SystemExit("Need a Loopixel 4-direction walk sheet (8 frames x 4 rows of square cells), got %dx%d" % sheet.size)
    out = Image.new("RGBA", (3 * OUT_CELL, 4 * OUT_CELL), (0, 0, 0, 0))
    for r, name in enumerate(RPGM_ORDER):
        sr = LOOPIXEL_ROWS[name]
        for c, f in enumerate(frames):
            cell = sheet.crop((f * CELL, sr * CELL, (f + 1) * CELL, (sr + 1) * CELL))
            if CELL != OUT_CELL:
                cell = cell.resize((OUT_CELL, OUT_CELL), Image.NEAREST)
            out.paste(cell, (c * OUT_CELL, r * OUT_CELL))
    out.save(dst)
    print("wrote %s %s using frames %s" % (dst, out.size, frames))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--frames", default="0,2,4", help="3 frame indexes 0-7, default 0,2,4")
    a = ap.parse_args()
    fr = [int(x) for x in a.frames.split(",")]
    if len(fr) != 3 or any(not 0 <= x < 8 for x in fr):
        raise SystemExit("--frames needs exactly 3 indexes between 0 and 7")
    convert(a.src, a.dst, fr)
