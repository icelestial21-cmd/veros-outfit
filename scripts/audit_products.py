import json
import os
import subprocess

web_dir = r"C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\web"
assets_dir = os.path.join(web_dir, "assets")
scratch_dir = r"C:\Users\User\.gemini\antigravity\scratch"
tg_base = r"D:\Media\Telegram_Exports\ChatExport_2026-09-26"

with open(os.path.join(web_dir, "products.json"), 'r', encoding='utf-8') as f:
    products = json.load(f)

print(f"Total products in products.json: {len(products)}")

for p in products:
    pid = p['id']
    name = p['name']
    front_rel = p.get('front_photo') or ''
    video_rel = p.get('video_url') or ''
    
    front = os.path.join(web_dir, front_rel) if front_rel else ''
    video = os.path.join(web_dir, video_rel) if video_rel else ''
    
    front_exists = os.path.exists(front) if front else False
    video_exists = os.path.exists(video) if video else False
    
    # Extract 1s frame from video if it exists
    frame_path = os.path.join(scratch_dir, f"{pid}_video_frame.jpg")
    if video_exists and not os.path.exists(frame_path):
        subprocess.run([
            "ffmpeg", "-y", "-ss", "00:00:01", "-i", video,
            "-vframes", "1", "-q:v", "2", frame_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    print(f"[{pid}] {name}")
    print(f"   Front: {front_rel} (Exists: {front_exists})")
    print(f"   Video: {video_rel} (Exists: {video_exists})")
    print(f"   Frame: {frame_path if os.path.exists(frame_path) else 'None'}")
