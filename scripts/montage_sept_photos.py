import os
import glob
from PIL import Image, ImageDraw

export_dir = r"D:\Media\Telegram_Exports\ChatExport_2026-09-26"
photos_dir = os.path.join(export_dir, "photos")

target_photos = []
for d in ['01-09-2025', '02-09-2025', '03-09-2025', '04-09-2025', '05-09-2025']:
    matched = sorted(glob.glob(os.path.join(photos_dir, f"*@{d}_*.jpg")))
    target_photos.extend(matched)

cols = 8
thumb_w = 180
thumb_h = 240
rows = (len(target_photos) + cols - 1) // cols
montage = Image.new('RGB', (cols * thumb_w, rows * thumb_h), (20, 20, 20))
draw = ImageDraw.Draw(montage)

for idx, f in enumerate(target_photos):
    im = Image.open(f).resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
    r = idx // cols
    c = idx % cols
    x = c * thumb_w
    y = r * thumb_h
    montage.paste(im, (x, y))
    label = os.path.basename(f).split('@')[0]
    draw.rectangle([x, y, x + thumb_w, y + 18], fill=(0, 0, 0, 180))
    draw.text((x + 2, y + 2), label, fill=(255, 255, 255))

out_path = r'C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\sept_photos_montage.jpg'
montage.save(out_path, quality=85)
print("Saved", out_path)
