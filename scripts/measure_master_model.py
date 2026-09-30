import os
from PIL import Image

p = r"C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\web\assets\model_baku_master.jpg"
img = Image.open(p)
w, h = img.size

# Let's inspect relative coordinates on the 2160x3840 image:
# In model_baku_master.jpg:
# Top of cap: y ~ 690 (rel ~ 0.18)
# Eyes/face: y ~ 880 (rel ~ 0.23)
# Neck/collar: y ~ 1150 (rel ~ 0.30)
# Shoulders: y ~ 1230 (rel ~ 0.32), Left: x ~ 780 (0.36), Right: x ~ 1400 (0.65)
# Chest: y ~ 1500 (rel ~ 0.39)
# Waist: y ~ 2150 (rel ~ 0.56), Left: x ~ 900 (0.42), Right: x ~ 1280 (0.59)
# Pelvis/Hips: y ~ 2400 (rel ~ 0.62)
# Knees: y ~ 2900 (rel ~ 0.75), Left: x ~ 940 (0.435), Right: x ~ 1260 (0.583)
# Ankles/Sneakers: y ~ 3450 (rel ~ 0.90), Left: x ~ 900 (0.42), Right: x ~ 1300 (0.60)
# Bottom of soles: y ~ 3600 (rel ~ 0.94)

print(f"Image dimensions: {w}x{h}")
print("Relative anatomical landmark map:")
landmarks = {
    "cranial_top": (0.50, 0.18),
    "cranial_center": (0.51, 0.24),
    "shoulder_left": (0.35, 0.32),
    "shoulder_right": (0.66, 0.32),
    "thoracic_center": (0.51, 0.40),
    "waist_left": (0.41, 0.57),
    "waist_right": (0.60, 0.57),
    "pelvis_center": (0.51, 0.63),
    "knee_left": (0.43, 0.76),
    "knee_right": (0.59, 0.76),
    "ankle_left": (0.42, 0.91),
    "ankle_right": (0.60, 0.91)
}

for k, (rx, ry) in landmarks.items():
    print(f"  {k:16}: x={int(rx*w)}, y={int(ry*h)} (rel: {rx:.3f}, {ry:.3f})")
