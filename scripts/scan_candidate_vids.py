import os
import subprocess
import glob
from PIL import Image, ImageDraw

def scan_video(vname, out_dir, montage_path, fps=2, max_frames=24):
    os.makedirs(out_dir, exist_ok=True)
    vpath = os.path.join(r"D:\Media\Telegram_Exports\ChatExport_2026-09-26\video_files", vname)
    cmd = [
        'ffmpeg', '-y',
        '-i', vpath,
        '-vf', f'fps={fps},scale=360:640',
        '-vframes', str(max_frames),
        os.path.join(out_dir, 'f_%03d.jpg')
    ]
    subprocess.run(cmd, check=True)
    files = sorted(glob.glob(os.path.join(out_dir, 'f_*.jpg')))
    cols = 6
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
        draw.rectangle([x, y, x + thumb_w, y + 20], fill=(0, 0, 0, 180))
        draw.text((x + 4, y + 2), f"{idx * (1.0/fps):.1f}s", fill=(255, 255, 255))
    montage.save(montage_path, quality=85)
    print(f"Saved {montage_path}")

scan_video('IMG_1649.MOV', 
           r'C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\scan_1649',
           r'C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\montage_1649.jpg',
           fps=1, max_frames=24)

scan_video('IMG_7803.MOV', 
           r'C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\scan_7803',
           r'C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\montage_7803.jpg',
           fps=1, max_frames=24)
