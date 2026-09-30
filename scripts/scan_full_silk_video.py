import os
import subprocess
import glob
from PIL import Image, ImageDraw

output_dir = r'C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\silk_full_timeline'
os.makedirs(output_dir, exist_ok=True)

video_path = r'D:\Media\Telegram_Exports\ChatExport_2026-09-26\video_files\copy_3FD097F2-149E-4E5E-B23E-B4FE97836874.mov'

# Extract 1 frame per second across all 71 seconds
cmd = [
    'ffmpeg', '-y',
    '-i', video_path,
    '-vf', 'fps=1,scale=360:640',
    os.path.join(output_dir, 'sec_%03d.jpg')
]
subprocess.run(cmd, check=True)

# Make montage of 71 frames (8 cols x 9 rows)
files = sorted(glob.glob(os.path.join(output_dir, 'sec_*.jpg')))
cols = 8
thumb_w = 200
thumb_h = 356
rows = (len(files) + cols - 1) // cols
montage = Image.new('RGB', (cols * thumb_w, rows * thumb_h), (20, 20, 20))
draw = ImageDraw.Draw(montage)

for idx, f in enumerate(files):
    im = Image.open(f).resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
    r = idx // cols
    c = idx % cols
    x = c * thumb_w
    y = r * thumb_h
    montage.paste(im, (x, y))
    label = os.path.basename(f).replace('sec_', '').replace('.jpg', 's')
    draw.rectangle([x, y, x + thumb_w, y + 20], fill=(0, 0, 0, 180))
    draw.text((x + 4, y + 2), label, fill=(255, 255, 255))

montage_path = r'C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\silk_full_montage.jpg'
montage.save(montage_path, quality=85)
print(f"Saved full timeline montage to {montage_path}")
