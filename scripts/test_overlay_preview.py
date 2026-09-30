import os
from PIL import Image, ImageDraw, ImageFont

img_path = r"C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\web\assets\model_baku_master.jpg"
out_path = r"C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\preview_calibrated_overlay.jpg"

img = Image.open(img_path).convert("RGBA")
# Resize to canvas dimensions 450x800 (9:16)
canvas_w, canvas_h = 450, 800
resized = img.resize((canvas_w, canvas_h), Image.Resampling.LANCZOS)

# Dark subtle overlay
overlay = Image.new("RGBA", (canvas_w, canvas_h), (7, 9, 14, 80))
composed = Image.alpha_composite(resized, overlay)

draw = ImageDraw.Draw(composed)

# Keypoints for model_baku_master:
head = (int(canvas_w * 0.505), int(canvas_h * 0.20))
sh_l = (int(canvas_w * 0.35), int(canvas_h * 0.32))
sh_r = (int(canvas_w * 0.66), int(canvas_h * 0.32))
thor = (int(canvas_w * 0.505), int(canvas_h * 0.40))
w_l = (int(canvas_w * 0.41), int(canvas_h * 0.57))
w_r = (int(canvas_w * 0.60), int(canvas_h * 0.57))
pelvis = (int(canvas_w * 0.505), int(canvas_h * 0.63))
knee_l = (int(canvas_w * 0.43), int(canvas_h * 0.76))
knee_r = (int(canvas_w * 0.59), int(canvas_h * 0.76))
ank_l = (int(canvas_w * 0.42), int(canvas_h * 0.91))
ank_r = (int(canvas_w * 0.60), int(canvas_h * 0.91))

gold = (212, 175, 55, 230)
green = (74, 222, 128, 255)

# Connect lines
connections = [
    (head, thor),
    (thor, pelvis),
    (sh_l, sh_r),
    (sh_l, thor),
    (sh_r, thor),
    (w_l, w_r),
    (pelvis, knee_l),
    (pelvis, knee_r),
    (knee_l, ank_l),
    (knee_r, ank_r)
]

for p1, p2 in connections:
    draw.line([p1, p2], fill=gold, width=2)

nodes = [head, sh_l, sh_r, thor, w_l, w_r, pelvis, knee_l, knee_r, ank_l, ank_r]
for x, y in nodes:
    draw.ellipse([x - 7, y - 7, x + 7, y + 7], outline=green, fill=(74, 222, 128, 80), width=2)
    draw.ellipse([x - 3, y - 3, x + 3, y + 3], fill=green)

composed.convert("RGB").save(out_path, quality=95)
print(f"Generated preview overlay at: {out_path}")
