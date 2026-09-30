import os
import subprocess
import glob
from PIL import Image, ImageDraw

output_dir = r'C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\silk_sec3_sec5'
os.makedirs(output_dir, exist_ok=True)

video_path = r'D:\Media\Telegram_Exports\ChatExport_2026-09-26\video_files\copy_3FD097F2-149E-4E5E-B23E-B4FE97836874.mov'

# Extract frames between 3.0s and 5.2s at 10 fps (every 0.1s)
cmd = [
    'ffmpeg', '-y',
    '-ss', '3.0',
    '-t', '2.5',
    '-i', video_path,
    '-vf', 'fps=10,scale=540:960',
    os.path.join(output_dir, 'f_%03d.jpg')
]
subprocess.run(cmd, check=True)

# Make contact sheet
files = sorted(glob.glob(os.path.join(output_dir, 'f_*.jpg')))
cols = 5
thumb_w = 270
thumb_h = 480
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
    # timestamp: 3.0 + idx * 0.1
    t = 3.0 + idx * 0.1
    label = f"{t:.1f}s ({os.path.basename(f)})"
    draw.rectangle([x, y, x + thumb_w, y + 24], fill=(0, 0, 0, 180))
    draw.text((x + 4, y + 4), label, fill=(255, 255, 255))

montage_path = r'C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\silk_sec3_sec5_montage.jpg'
montage.save(montage_path, quality=85)
print(f"Saved montage to {montage_path} ({len(files)} frames)")
