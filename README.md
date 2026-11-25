# Loopixel importers for Godot 4 and RPG Maker

Two tiny helper scripts for sprite sheets exported from [Loopixel](https://loopixel.com) (one image in, looping sprite sheet out in five sizes: 32, 48, 64, 96 and 128 px).

## Godot 4: `loopixel_import.gd`

1. Copy your Loopixel sheet into the project and rename it `sprite_64.png` (or edit the `SHEET` constant to any `sprite_{size}.png` from the ZIP).
2. Open `loopixel_import.gd` in the Godot script editor and run it with **File > Run** (Ctrl+Shift+X).
3. It writes `res://sprite_frames.tres`. Assign it to an `AnimatedSprite2D`.

- No cell size to set: every Loopixel row has 8 frames, so the script uses sheet width / 8 (32, 48, 64, 96 and 128 all work). No atlas JSON is read.
- 4-row sheets become `walk_front`, `walk_right`, `walk_back`, `walk_left` (Loopixel row order). A 1-row sheet becomes one animation named after the file.
- Default speed is 10 fps (change `FPS`). Loop is on. Sheets that are not 8 frames wide or not 1 or 4 rows are rejected with an error.
- **Set the texture filter to Nearest** (Project Settings > Rendering > Textures > Default Texture Filter, or on the node), otherwise pixel art looks blurry.
- Tested on Godot 4.7.2 (headless, running the editor script against 48px and 64px 4-row sheets and a 64px 1-row sheet; animation names, 8 frames each and every frame region checked).

## RPG Maker MV/MZ: `loopixel_to_rpgmaker.py`

```
pip install pillow
python3 loopixel_to_rpgmaker.py sprite_48.png '$Hero.png' --frames 0,2,4
```

- Input: a 4-direction Loopixel sheet (4 rows x 8 frames), any of the five sizes. The cell size is read from the sheet width (width / 8). Use `sprite_48.png` from the ZIP: it is already RPG Maker's native 48px, so no scaling happens. Other sizes are nearest-neighbour scaled to 48px.
- Output: 144x192 PNG, 3 columns x 4 rows of 48px cells, nearest-neighbour scaled. Rows are reordered to RPG Maker's down, left, right, up. Start the file name with `$` so RPG Maker treats it as a single character (keep it in single quotes in the shell, or `$Hero` gets expanded as a variable).
- `--frames` picks which 3 of the 8 frames to use (default 0,2,4). RPG Maker expects the middle column to be the standing pose, so check the result in your project and adjust.
- Check the result in your project: row 1 faces the camera, row 2 faces left, row 3 faces right, row 4 faces away.

## Limits

- Loopixel 4-direction output is a walk cycle only, square frames at 32, 48, 64, 96 or 128 px, up to 24 colors.
- Use the 48px sheet to avoid any scaling. Converting from a larger size (e.g. 64px) downsamples to 48px, so some detail is lost.
- One-direction sheets cannot be converted to the RPG Maker layout.

## License

MIT, see `LICENSE`. Copyright 2026 Zane. Made with Loopixel: https://loopixel.com
