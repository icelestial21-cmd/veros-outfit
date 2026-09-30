import os
import json
import subprocess

json_path = r"C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\web\products.json"
assets_dir = r"C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\web\assets"
scratch_dir = r"C:\Users\User\.gemini\antigravity\scratch\frame_checks"
os.makedirs(scratch_dir, exist_ok=True)

with open(json_path, "r", encoding="utf-8") as f:
    products = json.load(f)

print(f"Total products: {len(products)}")

for p in products:
    pid = p["id"]
    name = p["name"]
    video = p.get("video_url")
    front = p.get("front_photo")
    print(f"\n[{pid}] {name}")
    print(f"  Front: {front}")
    print(f"  Video: {video}")
    print(f"  Copy: {p.get('fabric_story', '')[:80]}...")
    
    # If video exists, extract frame at 1s to inspect
    if video and os.path.exists(os.path.join(r"C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\web", video)):
        vpath = os.path.join(r"C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\web", video)
        out_frame = os.path.join(scratch_dir, f"{pid}_frame1s.jpg")
        cmd = f'ffmpeg -ss 00:00:01 -i "{vpath}" -vframes 1 -q:v 2 -y "{out_frame}"'
        subprocess.run(cmd, shell=True, capture_output=True)
        print(f"  Extracted video frame to: {out_frame}")
