import os
from PIL import Image, ImageDraw

vids = [
    'copy_9F7C94A2-0D7E-4E63-9AA6-A251D66AFD99.mov_thumb.jpg',
    'IMG_7803.MOV_thumb.jpg',
    'IMG_1681.MOV_thumb.jpg',
    'IMG_9119.MOV_thumb.jpg',
    'IMG_2302.MOV_thumb.jpg',
    'IMG_1239.MOV_thumb.jpg',
    'IMG_2927.MOV_thumb.jpg',
    'IMG_4354.MOV_thumb.jpg',
    'IMG_9255.MOV_thumb.jpg',
    'IMG_2395.MOV_thumb.jpg',
    'IMG_4274.MOV_thumb.jpg',
    'IMG_1649.MOV_thumb.jpg',
    'IMG_0378.MOV_thumb.jpg',
    'IMG_1605.MOV_thumb.jpg',
    'IMG_6388.mov_thumb.jpg',
    'IMG_4600.MOV_thumb.jpg',
    'IMG_6236.mov_thumb.jpg'
]

video_dir = r"D:\Media\Telegram_Exports\ChatExport_2026-09-26\video_files"
cols = 4
thumb_w = 270
thumb_h = 480
rows = (len(vids) + cols - 1) // cols
montage = Image.new('RGB', (cols * thumb_w, rows * thumb_h), (20, 20, 20))
draw = ImageDraw.Draw(montage)

for idx, vname in enumerate(vids):
    fpath = os.path.join(video_dir, vname)
    if os.path.exists(fpath):
        im = Image.open(fpath).resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        r = idx // cols
        c = idx % cols
        x = c * thumb_w
        y = r * thumb_h
        montage.paste(im, (x, y))
        draw.rectangle([x, y, x + thumb_w, y + 24], fill=(0, 0, 0, 180))
        draw.text((x + 4, y + 4), vname.split('.')[0], fill=(255, 255, 255))

out_path = r'C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\top_matches_montage.jpg'
montage.save(out_path, quality=85)
print("Saved", out_path)
