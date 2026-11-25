@tool
extends EditorScript
## Loopixel -> Godot 4 SpriteFrames importer (MIT). Run via File > Run (Ctrl+Shift+X).
## Reads a Loopixel sheet and writes a SpriteFrames .tres. Every Loopixel row has 8 frames, so the cell size is sheet width / 8 (any of 32, 48, 64, 96, 128).
## 4 rows -> walk_front / walk_right / walk_back / walk_left. 1 row -> action name from file name.

const SHEET := "res://sprite_64.png"     # your Loopixel sheet
const OUT := "res://sprite_frames.tres"
const FPS := 10.0                         # Loopixel previews play at 10 fps; change to taste
const DIRS := ["walk_front", "walk_right", "walk_back", "walk_left"]

func _run() -> void:
	var tex: Texture2D = load(SHEET)
	if tex == null:
		push_error("Cannot load " + SHEET)
		return
	var cols := 8                             # Loopixel rows always hold 8 frames
	if tex.get_width() % cols != 0:
		push_error("Sheet width %d is not 8 frames wide. Use a sprite_{size}.png from the Loopixel ZIP." % tex.get_width())
		return
	var cell: int = int(tex.get_width() / cols)
	var rows: int = int(tex.get_height() / cell)
	if tex.get_height() % cell != 0 or not (rows == 1 or rows == 4):
		push_error("Expected 1 or 4 rows of %dpx frames, got a %dx%d sheet." % [cell, tex.get_width(), tex.get_height()])
		return
	var sf := SpriteFrames.new()
	sf.remove_animation("default")
	for r in rows:
		var anim: String = DIRS[r] if rows == 4 else SHEET.get_file().get_basename()
		sf.add_animation(anim)
		sf.set_animation_speed(anim, FPS)
		sf.set_animation_loop(anim, true)
		for c in cols:
			var at := AtlasTexture.new()
			at.atlas = tex
			at.region = Rect2(c * cell, r * cell, cell, cell)
			sf.add_frame(anim, at)
	var err := ResourceSaver.save(sf, OUT)
	print("Saved ", OUT, " (", rows, " row(s) x ", cols, " frames) err=", err)
