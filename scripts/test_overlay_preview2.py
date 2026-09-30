import os
from PIL import Image, ImageDraw

img_path = r"C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\web\assets\model_baku_master.jpg"
out_path = r"C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\preview_calibrated_overlay2.jpg"

img = Image.open(img_path).convert("RGBA")
canvas_w, canvas_h = 450, 800
resized = img.resize((canvas_w, canvas_h), Image.Resampling.LANCZOS)

overlay = Image.new("RGBA", (canvas_w, canvas_h), (7, 9, 14, 60))
composed = Image.alpha_composite(resized, overlay)
draw = ImageDraw.Draw(composed)

# Exact landmarks on the 450x800 frame:
head = (int(canvas_w * 0.615), int(canvas_h * 0.22))
sh_l = (int(canvas_w * 0.49), int(canvas_h * 0.315))
sh_r = (int(canvas_w * 0.74), int(canvas_h * 0.315))
thor = (int(canvas_w * 0.615), int(canvas_h * 0.40))
w_l = (int(canvas_w * 0.52), int(canvas_h * 0.575))
w_r = (int(canvas_w * 0.71), int(canvas_h * 0.575))
pelvis = (int(canvas_w * 0.62), int(canvas_h * 0.63))
knee_l = (int(canvas_w * 0.55), int(canvas_h * 0.76))
knee_r = (int(canvas_w * 0.70), int(canvas_h * 0.76))
ank_l = (int(canvas_w * 0.54), int(canvas_h * 0.91))
ank_r = (int(canvas_w * 0.75), int(canvas_h * 0.91))

gold = (212, 175, 55, 230)
green = (74, 222, 128, 255)

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
    draw.ellipse([x - 6, y - 6, x + 6, y + 6], outline=green, fill=(74, 222, 128, 90), width=2)
    draw.ellipse([x - 2.5, y - 2.5, x + 2.5, y + 2.5], fill=green)

composed.convert("RGB").save(out_path, quality=95)
print(f"Generated preview overlay 2 at: {out_path}")
