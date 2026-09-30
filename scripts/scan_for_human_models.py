import os
import glob
import sys
import shutil
import torch
from torchvision.models.detection import ssdlite320_mobilenet_v3_large, SSDLite320_MobileNet_V3_Large_Weights
from torchvision.transforms import functional as F
from PIL import Image

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

export_dir = r"D:\Media\Telegram_Exports\ChatExport_2026-09-26"
photos_dir = os.path.join(export_dir, "photos")
video_dir = os.path.join(export_dir, "video_files")
output_dir = r"C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\candidate_models"
os.makedirs(output_dir, exist_ok=True)

print("Loading SSDLite model...")
weights = SSDLite320_MobileNet_V3_Large_Weights.DEFAULT
model = ssdlite320_mobilenet_v3_large(weights=weights)
model.eval()

# COCO label 1 is 'person'
PERSON_CLASS_ID = 1

# Gather candidate images:
# 1. Video thumbnails
candidates = sorted(glob.glob(os.path.join(video_dir, "*.mp4_thumb.jpg")))
print(f"Found {len(candidates)} video thumbnails.")

# 2. Photos: sample photos (every 5th or 10th photo to cover the 7500 photos quickly, plus photos with 'photo_' pattern)
all_photos = sorted(glob.glob(os.path.join(photos_dir, "photo_*.jpg")))
print(f"Found {len(all_photos)} photos. Sampling every 10th photo...")
sampled_photos = all_photos[::10]
candidates.extend(sampled_photos)

print(f"Total images to evaluate: {len(candidates)}")

best_models = []

with torch.no_grad():
    for idx, img_path in enumerate(candidates):
        try:
            with Image.open(img_path) as img:
                img_rgb = img.convert("RGB")
                w, h = img_rgb.size
                
                # We want vertical/portrait orientation preferably
                tensor = F.to_tensor(img_rgb).unsqueeze(0)
                pred = model(tensor)[0]
                
                # Check for person
                boxes = pred["boxes"]
                labels = pred["labels"]
                scores = pred["scores"]
                
                for b, l, s in zip(boxes, labels, scores):
                    if l.item() == PERSON_CLASS_ID and s.item() >= 0.70:
                        x1, y1, x2, y2 = b.tolist()
                        box_h = y2 - y1
                        box_w = x2 - x1
                        box_h_ratio = box_h / h
                        box_w_ratio = box_w / w
                        
                        # Full or substantial upper/full body (at least 45% of image height)
                        if box_h_ratio >= 0.45:
                            score = s.item()
                            best_models.append({
                                "path": img_path,
                                "name": os.path.basename(img_path),
                                "score": score,
                                "h_ratio": box_h_ratio,
                                "w_ratio": box_w_ratio,
                                "dims": (w, h),
                                "bbox": (x1, y1, x2, y2)
                            })
                            print(f"[{len(best_models)}] Found Model: {os.path.basename(img_path)} (Score: {score:.2f}, HeightRatio: {box_h_ratio:.2f})")
                            break
                            
            if len(best_models) >= 25:
                print("Found 25 excellent model candidates! Stopping search.")
                break
        except Exception as e:
            continue
            
        if (idx + 1) % 100 == 0:
            print(f"  Processed {idx + 1}/{len(candidates)} images...")

# Sort by height ratio (full body) and score
best_models.sort(key=lambda x: (x["h_ratio"], x["score"]), reverse=True)

print(f"\nTop {min(10, len(best_models))} Candidates:")
for i, m in enumerate(best_models[:10]):
    print(f"[{i+1}] {m['name']}: HeightRatio={m['h_ratio']:.2f}, Score={m['score']:.2f}, Dims={m['dims']}")
    # Copy to candidate models directory
    dest = os.path.join(output_dir, f"model_candidate_{i+1}_{m['name']}")
    shutil.copy2(m["path"], dest)

print(f"\nCandidates copied to: {output_dir}")
