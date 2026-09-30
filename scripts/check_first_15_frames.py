import os
import subprocess
import glob
from PIL import Image, ImageDraw

out_dir = r'C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\silk_first_half_second'
os.makedirs(out_dir, exist_ok=True)

video_path = r'D:\Media\Telegram_Exports\ChatExport_2026-09-26\video_files\copy_3FD097F2-149E-4E5E-B23E-B4FE97836874.mov'

# Extract first 15 frames at 30fps
cmd = [
    'ffmpeg', '-y',
    '-ss', '0.0',
    '-i', video_path,
    '-vframes', '15',
    '-vf', 'scale=1080:1920',
    os.path.join(out_dir, 'f_%02d.jpg')
]
subprocess.run(cmd, check=True)

files = sorted(glob.glob(os.path.join(out_dir, 'f_*.jpg')))
print(f"Extracted {len(files)} frames.")

# Create montage focusing on the torso & hands
montage = Image.new('RGB', (5 * 216, 3 * 384), (20, 20, 20))
draw = ImageDraw.Draw(montage)

for idx, f in enumerate(files):
    im = Image.open(f).resize((216, 384), Image.Resampling.LANCZOS)
    r = idx // 5
    c = idx % 5
    x = c * 216
    y = r * 384
    montage.paste(im, (x, y))
    draw.rectangle([x, y, x + 216, y + 24], fill=(0, 0, 0, 180))
    draw.text((x + 4, y + 4), f"Frame {idx} ({idx/30.0:.2f}s)", fill=(255, 255, 255))

montage_path = r'C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\first_15_frames_montage.jpg'
montage.save(montage_path, quality=90)
print("Saved montage to", montage_path)
