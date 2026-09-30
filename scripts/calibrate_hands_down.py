import os
import subprocess
from PIL import Image, ImageDraw

# Step 1: Extract 0.00s frame at full 4K 2160x3840 from the video
src_video = r'D:\Media\Telegram_Exports\ChatExport_2026-09-26\video_files\copy_3FD097F2-149E-4E5E-B23E-B4FE97836874.mov'
raw_4k_path = r'C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\silk_t0_4k.jpg'

if not os.path.exists(raw_4k_path):
    cmd = [
        'ffmpeg', '-y',
        '-ss', '0.00',
        '-i', src_video,
        '-vframes', '1',
        '-update', '1',
        '-q:v', '1',
        raw_4k_path
    ]
    subprocess.run(cmd, check=True)

# Step 2: Load 4K image (2160 x 3840)
raw_img = Image.open(raw_4k_path)
w, h = raw_img.size
print(f"Raw frame size: {w} x {h}")

# In the raw 4K frame, the model is standing slightly back.
# Let's crop slightly into the frame so the model fills the 9:16 frame proportionally,
# preserving the full height from hair to shoes and keeping the wooden garment rack visible!
# Let's examine coordinates of the model and rack in the raw frame:
# Hair top: ~ y = 0.13 * h = 500 px
# Feet soles: ~ y = 0.68 * h = 2600 px
# Model height in raw frame = 2100 px out of 3840 px (~55% of frame height)
# If we crop the top from y = 300 to y = 3180 (height = 2880) and x from 0 to 1620 (9:16 ratio):
# 1620 / 2880 = 9 / 16!
# That brings the model closer, head at ~7% from top, shoes at ~80% from top,
# with the garment rack occupying the left side!

crop_top = 260
crop_h = 2880
crop_w = int(crop_h * 9 / 16)  # 1620
# Let's align x so the rack and model are nicely composed
# Model center is around x = 1100 in 2160 width
# If crop_w is 1620, x_start = 100 to 1720 keeps the rack (starts at ~80) and model (center ~1100)
crop_left = 120
crop_box = (crop_left, crop_top, crop_left + crop_w, crop_top + crop_h)

cropped_img = raw_img.crop(crop_box)
target_master = cropped_img.resize((1080, 1920), Image.Resampling.LANCZOS)

out_master_path = r'C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\web\assets\model_baku_master.jpg'
target_master.save(out_master_path, quality=95)
print(f"Saved master model to {out_master_path}")

# Now let's analyze landmarks on the 1080x1920 target master
# We will draw a preview calibration overlay on top of target_master to inspect landmarks!
im_test = target_master.copy()
draw = ImageDraw.Draw(im_test)

# Estimated normalized coordinates on target_master (1080 x 1920):
# Let's compute exact pixel locations
# Head crown: around y = 0.10, x = 0.58
# Shoulder Left: x = 0.46, y = 0.20
# Shoulder Right: x = 0.70, y = 0.20
# Chest: x = 0.58, y = 0.28
# Waist L: x = 0.49, y = 0.40
# Waist R: x = 0.66, y = 0.40
# Pelvis: x = 0.58, y = 0.45
# Knee L: x = 0.52, y = 0.65
# Knee R: x = 0.68, y = 0.65
# Ankle L: x = 0.48, y = 0.82
# Ankle R: x = 0.72, y = 0.83
# Wooden Rack scaleReference: x1 = 0.02, y1 = 0.12, x2 = 0.35, y2 = 0.86

landmarks = {
    'head': {'x': 0.585, 'y': 0.100},
    'shoulderL': {'x': 0.440, 'y': 0.235},
    'shoulderR': {'x': 0.730, 'y': 0.235},
    'chest': {'x': 0.585, 'y': 0.300},
    'waistL': {'x': 0.490, 'y': 0.415},
    'waistR': {'x': 0.675, 'y': 0.415},
    'pelvis': {'x': 0.585, 'y': 0.465},
    'kneeL': {'x': 0.520, 'y': 0.660},
    'kneeR': {'x': 0.685, 'y': 0.665},
    'ankleL': {'x': 0.480, 'y': 0.825},
    'ankleR': {'x': 0.715, 'y': 0.835}
}

scale_ref = {
    'x1': 0.015, 'y1': 0.115, 'x2': 0.365, 'y2': 0.865
}

# Draw skeleton & joints
W, H = 1080, 1920
connections = [
    ('head', 'chest'),
    ('shoulderL', 'shoulderR'),
    ('shoulderL', 'waistL'),
    ('shoulderR', 'waistR'),
    ('chest', 'pelvis'),
    ('waistL', 'pelvis'),
    ('waistR', 'pelvis'),
    ('pelvis', 'kneeL'),
    ('pelvis', 'kneeR'),
    ('kneeL', 'ankleL'),
    ('kneeR', 'ankleR')
]

# Draw reference box
rx1, ry1 = int(scale_ref['x1'] * W), int(scale_ref['y1'] * H)
rx2, ry2 = int(scale_ref['x2'] * W), int(scale_ref['y2'] * H)
draw.rectangle([rx1, ry1, rx2, ry2], outline=(255, 179, 0), width=4)
draw.text((rx1 + 10, ry1 + 10), "KNOWN REFERENCE: Wooden Garment Rack (165 cm)", fill=(255, 179, 0))

# Draw skeleton lines
for p1_name, p2_name in connections:
    p1 = (int(landmarks[p1_name]['x'] * W), int(landmarks[p1_name]['y'] * H))
    p2 = (int(landmarks[p2_name]['x'] * W), int(landmarks[p2_name]['y'] * H))
    draw.line([p1, p2], fill=(212, 175, 55), width=4)

# Draw joints
for name, pt in landmarks.items():
    px, py = int(pt['x'] * W), int(pt['y'] * H)
    draw.ellipse([px - 8, py - 8, px + 8, py + 8], fill=(212, 175, 55), outline=(255, 255, 255), width=2)
    draw.text((px + 12, py - 6), name, fill=(255, 255, 255))

preview_path = r'C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\preview_calibrated_hands_down.jpg'
im_test.save(preview_path, quality=90)
print(f"Saved calibration preview to {preview_path}")
