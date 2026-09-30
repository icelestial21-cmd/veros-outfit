import os
import torch
import torchvision
from torchvision.transforms import functional as F
from PIL import Image
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

photos_dir = r"D:\Media\Telegram_Exports\ChatExport_2026-09-26\photos"
out_dir = r"C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\candidate_models"
os.makedirs(out_dir, exist_ok=True)

weights = torchvision.models.detection.SSDLite320_MobileNet_V3_Large_Weights.DEFAULT
model = torchvision.models.detection.ssdlite320_mobilenet_v3_large(weights=weights)
model.eval()

files = [f for f in os.listdir(photos_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png')) and not f.endswith('_thumb.jpg')]
print(f"Total photos to scan: {len(files)}")

candidates = []

with torch.no_grad():
    for i, fname in enumerate(files):
        fpath = os.path.join(photos_dir, fname)
        try:
            # Quick size check: skip tiny icons
            if os.path.getsize(fpath) < 150000:
                continue
            with Image.open(fpath) as img:
                w, h = img.size
                if h <= w: # must be portrait orientation
                    continue
                aspect = w / h
                if aspect > 0.75: # we want vertical 9:16 or 3:4 portrait
                    continue

                img_rgb = img.convert("RGB")
                tensor = F.to_tensor(img_rgb).unsqueeze(0)
                pred = model(tensor)[0]

                boxes = pred["boxes"]
                labels = pred["labels"]
                scores = pred["scores"]

                for b, l, s in zip(boxes, labels, scores):
                    if l.item() == 1 and s.item() >= 0.85: # confident person
                        x1, y1, x2, y2 = b.tolist()
                        top_rel = y1 / h
                        bottom_rel = y2 / h
                        h_rel = (y2 - y1) / h
                        w_rel = (x2 - x1) / w
                        center_x = ((x1 + x2) / 2) / w
                        aspect_person = (x2 - x1) / (y2 - y1)

                        # Criteria:
                        # 1. Full-body: head near top (0.02 <= top <= 0.18), feet near bottom (0.82 <= bottom <= 0.98), height >= 0.70
                        # 2. Centered/Head-on: center_x between 0.35 and 0.65
                        # 3. Slim profile: aspect_person between 0.20 and 0.42 (not bulky puffer jacket or wide pose)
                        if 0.02 <= top_rel <= 0.18 and 0.82 <= bottom_rel <= 0.98 and h_rel >= 0.72:
                            if 0.35 <= center_x <= 0.65 and 0.20 <= aspect_person <= 0.42:
                                dest = os.path.join(out_dir, f"photo_{fname}")
                                img.save(dest)
                                candidates.append({
                                    "file": fname,
                                    "top": top_rel,
                                    "bottom": bottom_rel,
                                    "center_x": center_x,
                                    "aspect_person": aspect_person,
                                    "score": s.item(),
                                    "dims": (w, h)
                                })
                                print(f"[{len(candidates)}] MATCH PHOTO: {fname} (Center X: {center_x:.2f}, Person Aspect: {aspect_person:.2f}, Top: {top_rel:.2f}, Bottom: {bottom_rel:.2f})")
                                if len(candidates) >= 20:
                                    break
        except Exception:
            continue
        if len(candidates) >= 20:
            break

print(f"Total matching candidate photos: {len(candidates)}")
