import os
import re
import glob
import sys
import subprocess

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

export_dir = r"D:\Media\Telegram_Exports\ChatExport_2026-09-26"
video_dir = os.path.join(export_dir, "video_files")
photos_dir = os.path.join(export_dir, "photos")

# Let's inspect videos around IMG_3698.MP4
all_vids = sorted(os.listdir(video_dir))
print(f"Total videos: {len(all_vids)}")

# Filter IMG_*.MP4 or MOV around 3600-3800
nearby_vids = [v for v in all_vids if "36" in v or "37" in v or "38" in v or "35" in v]
print(f"Nearby videos to IMG_3698: {nearby_vids[:20]}")

# Let's check videos by size or creation date to find other videos featuring this model
img_3698_path = os.path.join(video_dir, "IMG_3698.MP4")
if os.path.exists(img_3698_path):
    stat = os.stat(img_3698_path)
    print(f"IMG_3698.MP4 size: {stat.st_size}, mtime: {stat.st_mtime}")

# Let's inspect the first 100 HTML files messages for video references
html_files = sorted(glob.glob(os.path.join(export_dir, "messages*.html")))
vids_with_text = []

for hf in html_files:
    with open(hf, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    # Split messages
    msgs = re.findall(r'<div class="message default clearfix[^"]*" id="(message\d+)">([\s\S]*?)(?=<div class="message default clearfix|\Z)', content)
    for mid, body in msgs:
        videos = re.findall(r'video_files/([^"]+)', body)
        photos = re.findall(r'photos/([^"]+)', body)
        text_match = re.search(r'<div class="text">([\s\S]*?)</div>', body)
        text = ""
        if text_match:
            text = ' '.join(re.sub(r'<[^>]+>', ' ', text_match.group(1)).split())
        
        if videos:
            vids_with_text.append({
                "mid": mid,
                "file": os.path.basename(hf),
                "videos": videos,
                "photos": photos,
                "text": text
            })

print(f"Found {len(vids_with_text)} messages containing videos.")
