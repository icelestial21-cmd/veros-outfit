import os
import glob
import sys
import subprocess
import torch
from torchvision.models.detection import ssdlite320_mobilenet_v3_large, SSDLite320_MobileNet_V3_Large_Weights
from torchvision.transforms import functional as F
from PIL import Image

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

export_dir = r"D:\Media\Telegram_Exports\ChatExport_2026-09-26"
video_dir = os.path.join(export_dir, "video_files")
output_dir = r"C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\full_body_models"
os.makedirs(output_dir, exist_ok=True)

weights = SSDLite320_MobileNet_V3_Large_Weights.DEFAULT
model = ssdlite320_mobilenet_v3_large(weights=weights)
model.eval()

# Let's inspect video files. Filter for MP4/MOV >= 2MB (real video clips)
vids = [f for f in os.listdir(video_dir) if f.lower().endswith(('.mp4', '.mov')) and not f.endswith('_thumb.jpg')]
print(f"Total video clips: {len(vids)}")

full_body_hits = []

# Check a sample of videos, especially those with human thumbnails or IMG_*
# Let's prioritize videos that had thumbnail matches or IMG_* series
priority_vids = [
    "50A1F4B6-D330-452B-95DE-A484A9639557.MP4",
    "E258DE16-B8CE-4BA0-8908-093788427F3F.MP4",
    "3400D869-6019-4C2B-B54A-32847A82B6DE.MP4",
    "B77C05CD-3662-4968-B1A7-A7B93A9477AF.MP4",
    "IMG_3698.MP4", "IMG_3699.MP4", "IMG_3700.MP4", "IMG_3701.MP4", "IMG_3702.MP4", "IMG_3703.MP4", "IMG_3704.MP4",
    "IMG_0155.MP4", "IMG_0157.MP4", "IMG_0531.MP4", "IMG_4480.MP4", "IMG_4538.MP4", "IMG_5013.MP4", "IMG_5590.MP4"
]

# Add more videos from the directory
all_prioritized = priority_vids + [v for v in vids if v not in priority_vids]

print(f"Scanning up to 80 videos for full-body standing frames...")

temp_frame = r"C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\temp_frame.jpg"

with torch.no_grad():
    for vid_name in all_prioritized[:80]:
        vid_path = os.path.join(video_dir, vid_name)
        if not os.path.exists(vid_path) or os.path.getsize(vid_path) < 1000000:
            continue
            
        # Extract 3 timestamps: 1s, 2s, 4s
        for sec in [1, 2, 4]:
            cmd = [
                "ffmpeg", "-y", "-ss", f"00:00:0{sec}", "-i", vid_path,
                "-vframes", "1", "-q:v", "2", temp_frame
            ]
            res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if not os.path.exists(temp_frame) or os.path.getsize(temp_frame) == 0:
                continue
                
            try:
                with Image.open(temp_frame) as img:
                    img_rgb = img.convert("RGB")
                    w, h = img_rgb.size
                    
                    # Must be portrait orientation
                    if h <= w:
                        continue
                        
                    tensor = F.to_tensor(img_rgb).unsqueeze(0)
                    pred = model(tensor)[0]
                    
                    boxes = pred["boxes"]
                    labels = pred["labels"]
                    scores = pred["scores"]
                    
                    for b, l, s in zip(boxes, labels, scores):
                        if l.item() == 1 and s.item() >= 0.75:
                            x1, y1, x2, y2 = b.tolist()
                            box_h = y2 - y1
                            box_w = x2 - x1
                            h_ratio = box_h / h
                            top_rel = y1 / h
                            bottom_rel = y2 / h
                            
                            # True full body: height >= 75% of image, top < 0.20, bottom > 0.85
                            if h_ratio >= 0.70 and top_rel <= 0.20 and bottom_rel >= 0.80:
                                hit_name = f"fullbody_{len(full_body_hits)+1}_{vid_name}_{sec}s.jpg"
                                dest_path = os.path.join(output_dir, hit_name)
                                img.save(dest_path)
                                full_body_hits.append({
                                    "video": vid_name,
                                    "sec": sec,
                                    "file": hit_name,
                                    "score": s.item(),
                                    "h_ratio": h_ratio,
                                    "top": top_rel,
                                    "bottom": bottom_rel,
                                    "dims": (w, h),
                                    "bbox": (x1, y1, x2, y2)
                                })
                                print(f"[{len(full_body_hits)}] FULL BODY FOUND in {vid_name} at {sec}s! (Score: {s.item():.2f}, Top: {top_rel:.2f}, Bottom: {bottom_rel:.2f}, H_Ratio: {h_ratio:.2f})")
                                break
            except Exception as e:
                continue
                
        if len(full_body_hits) >= 15:
            print("Found 15 full body frames! Done.")
            break

print(f"\nTotal full-body hits: {len(full_body_hits)}")
