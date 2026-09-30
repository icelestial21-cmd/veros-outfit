import os
import subprocess
import glob
from PIL import Image, ImageDraw

vids = [
    'IMG_1681.MOV',
    'IMG_2302.MOV',
    'IMG_2927.MOV',
    'IMG_9255.MOV',
    'IMG_0378.MOV',
    'IMG_1605.MOV',
    'IMG_6236.mov'
]

output_dir = r'C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\scan_other_models'
os.makedirs(output_dir, exist_ok=True)
video_dir = r"D:\Media\Telegram_Exports\ChatExport_2026-09-26\video_files"

montage_items = []

for v in vids:
    vpath = os.path.join(video_dir, v)
    if not os.path.exists(vpath):
        continue
    # Extract 4 frames: at 1s, 2s, 3s, 4s
    for s in [1, 2, 3, 4]:
        out_img = os.path.join(output_dir, f"{v}_sec{s}.jpg")
        cmd = ['ffmpeg', '-y', '-ss', str(s), '-i', vpath, '-vf', 'scale=270:480', '-vframes', '1', out_img]
        subprocess.run(cmd, capture_output=True)
        if os.path.exists(out_img):
            montage_items.append((out_img, f"{v} {s}s"))

cols = 7
thumb_w = 200
thumb_h = 356
rows = (len(montage_items) + cols - 1) // cols
montage = Image.new('RGB', (cols * thumb_w, rows * thumb_h), (20, 20, 20))
draw = ImageDraw.Draw(montage)

for idx, (img_path, label) in enumerate(montage_items):
    im = Image.open(img_path).resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
    r = idx // cols
    c = idx % cols
    x = c * thumb_w
    y = r * thumb_h
    montage.paste(im, (x, y))
    draw.rectangle([x, y, x + thumb_w, y + 20], fill=(0, 0, 0, 180))
    draw.text((x + 4, y + 2), label, fill=(255, 255, 255))

out_path = r'C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\montage_all_model_vids.jpg'
montage.save(out_path, quality=85)
print("Saved", out_path)
