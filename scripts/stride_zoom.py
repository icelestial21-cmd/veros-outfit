import os
import glob
from PIL import Image, ImageDraw

output_dir = r'C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\silk_stride_zoom'
os.makedirs(output_dir, exist_ok=True)

files = sorted(glob.glob(r'C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\silk_sec0_sec15\f_*.jpg'))

# Focus on f_005 to f_025
stride_files = files[4:26]
cols = 5
thumb_w = 270
thumb_h = 480
rows = (len(stride_files) + cols - 1) // cols
montage = Image.new('RGB', (cols * thumb_w, rows * thumb_h), (20, 20, 20))
draw = ImageDraw.Draw(montage)

for idx, f in enumerate(stride_files):
    im = Image.open(f).resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
    r = idx // cols
    c = idx % cols
    x = c * thumb_w
    y = r * thumb_h
    montage.paste(im, (x, y))
    fname = os.path.basename(f)
    draw.rectangle([x, y, x + thumb_w, y + 24], fill=(0, 0, 0, 180))
    draw.text((x + 4, y + 4), fname, fill=(255, 255, 255))

montage_path = r'C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\silk_stride_montage.jpg'
montage.save(montage_path, quality=85)
print(f"Saved stride montage to {montage_path}")
