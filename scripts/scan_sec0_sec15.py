import os
import subprocess
import glob
from PIL import Image, ImageDraw

output_dir = r'C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\silk_sec0_sec15'
os.makedirs(output_dir, exist_ok=True)

video_path = r'D:\Media\Telegram_Exports\ChatExport_2026-09-26\video_files\copy_3FD097F2-149E-4E5E-B23E-B4FE97836874.mov'

# Extract all frames from 0.0s to 1.6s at native 30fps
cmd = [
    'ffmpeg', '-y',
    '-ss', '0.0',
    '-t', '1.6',
    '-i', video_path,
    '-vf', 'scale=540:960',
    os.path.join(output_dir, 'f_%03d.jpg')
]
subprocess.run(cmd, check=True)

# Make contact sheet
files = sorted(glob.glob(os.path.join(output_dir, 'f_*.jpg')))
cols = 6
thumb_w = 240
thumb_h = 426
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
    t = idx / 30.0
    label = f"{t:.2f}s ({os.path.basename(f)})"
    draw.rectangle([x, y, x + thumb_w, y + 24], fill=(0, 0, 0, 180))
    draw.text((x + 4, y + 4), label, fill=(255, 255, 255))

montage_path = r'C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\silk_sec0_sec15_montage.jpg'
montage.save(montage_path, quality=85)
print(f"Saved montage to {montage_path} ({len(files)} frames)")
