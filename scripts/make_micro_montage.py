import os
import glob
from PIL import Image, ImageDraw, ImageFont

def make_montage(input_dir, output_path, cols=6, thumb_w=240, thumb_h=426):
    files = sorted(glob.glob(os.path.join(input_dir, '*.jpg')))
    if not files:
        print(f"No files in {input_dir}")
        return
    rows = (len(files) + cols - 1) // cols
    montage = Image.new('RGB', (cols * thumb_w, rows * thumb_h), (20, 20, 20))
    draw = ImageDraw.Draw(montage)
    
    for idx, f in enumerate(files):
        try:
            im = Image.open(f)
            im = im.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
            r = idx // cols
            c = idx % cols
            x = c * thumb_w
            y = r * thumb_h
            montage.paste(im, (x, y))
            label = os.path.basename(f)
            draw.rectangle([x, y, x + thumb_w, y + 24], fill=(0, 0, 0, 180))
            draw.text((x + 4, y + 4), label, fill=(255, 255, 255))
        except Exception as e:
            print(f"Error {f}: {e}")
            
    montage.save(output_path, quality=85)
    print(f"Saved montage to {output_path} ({len(files)} frames)")

make_montage(r'C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\silk_micro_scan',
             r'C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\silk_micro_montage.jpg',
             cols=6)

make_montage(r'C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\silk_v2_scan',
             r'C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\silk_v2_montage.jpg',
             cols=5)
