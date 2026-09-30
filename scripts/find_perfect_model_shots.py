import os
import subprocess
import torch
from torchvision.models.detection import ssdlite320_mobilenet_v3_large, SSDLite320_MobileNet_V3_Large_Weights
from torchvision.transforms import functional as F
from PIL import Image
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

export_dir = r"D:\Media\Telegram_Exports\ChatExport_2026-09-26"
video_dir = os.path.join(export_dir, "video_files")
output_dir = r"C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\perfect_models"
os.makedirs(output_dir, exist_ok=True)

weights = SSDLite320_MobileNet_V3_Large_Weights.DEFAULT
model = ssdlite320_mobilenet_v3_large(weights=weights)
model.eval()

vids = [f for f in os.listdir(video_dir) if f.lower().endswith(('.mp4', '.mov')) and not f.endswith('_thumb.jpg')]

print(f"Searching through videos for frames with full head (top > 0.04) and full feet (bottom > 0.88)...")

temp_frame = r"C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\temp_scan.jpg"

perfect_frames = []

with torch.no_grad():
    for vid_name in vids:
        vid_path = os.path.join(video_dir, vid_name)
        if os.path.getsize(vid_path) < 2000000:
            continue
            
        # Sample at 1s, 3s, 5s
        for sec in [1.0, 2.5, 4.0, 6.0]:
            cmd = [
                "ffmpeg", "-y", "-ss", str(sec), "-i", vid_path,
                "-vframes", "1", "-q:v", "2", temp_frame
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if not os.path.exists(temp_frame) or os.path.getsize(temp_frame) == 0:
                continue
                
            try:
                with Image.open(temp_frame) as img:
                    img_rgb = img.convert("RGB")
                    w, h = img_rgb.size
                    if h <= w:
                        continue
                        
                    tensor = F.to_tensor(img_rgb).unsqueeze(0)
                    pred = model(tensor)[0]
                    
                    boxes = pred["boxes"]
                    labels = pred["labels"]
                    scores = pred["scores"]
                    
                    for b, l, s in zip(boxes, labels, scores):
                        if l.item() == 1 and s.item() >= 0.80:
                            x1, y1, x2, y2 = b.tolist()
                            top_rel = y1 / h
                            bottom_rel = y2 / h
                            h_rel = (y2 - y1) / h
                            
                            # Perfect framing: head has margin above (0.02 < top_rel < 0.20) and feet have margin below (0.82 < bottom_rel < 0.98)
                            if 0.02 <= top_rel <= 0.20 and 0.82 <= bottom_rel <= 0.98 and h_rel >= 0.70:
                                hit_name = f"model_perfect_{len(perfect_frames)+1}_{vid_name}_{sec}s.jpg"
                                dest_path = os.path.join(output_dir, hit_name)
                                img.save(dest_path)
                                perfect_frames.append({
                                    "vid": vid_name,
                                    "sec": sec,
                                    "top": top_rel,
                                    "bottom": bottom_rel,
                                    "score": s.item(),
                                    "file": hit_name
                                })
                                print(f"[{len(perfect_frames)}] PERFECT MODEL FRAME: {vid_name} at {sec}s (Top: {top_rel:.2f}, Bottom: {bottom_rel:.2f}, Score: {s.item():.2f})")
                                break
            except Exception as e:
                continue
                
        if len(perfect_frames) >= 10:
            print("Found 10 perfect model frames! Done.")
            break

print(f"Total perfect frames: {len(perfect_frames)}")
