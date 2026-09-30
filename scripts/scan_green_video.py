import os
import subprocess
import glob
from PIL import Image, ImageDraw

output_dir = r'C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\green_full_scan'
os.makedirs(output_dir, exist_ok=True)

video_path = r'D:\Media\Telegram_Exports\ChatExport_2026-09-26\video_files\copy_2A3903C2-6A37-477A-9907-6F6444F03BBF.mov'

cmd = [
    'ffmpeg', '-y',
    '-i', video_path,
    '-vf', 'fps=1,scale=540:960',
    os.path.join(output_dir, 'sec_%02d.jpg')
]
subprocess.run(cmd, check=True)

files = sorted(glob.glob(os.path.join(output_dir, 'sec_*.jpg')))
cols = 4
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
    draw.rectangle([x, y, x + thumb_w, y + 24], fill=(0, 0, 0, 180))
    draw.text((x + 4, y + 4), os.path.basename(f), fill=(255, 255, 255))

montage_path = r'C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\green_full_montage.jpg'
montage.save(montage_path, quality=85)
print(f"Saved green full montage to {montage_path}")
