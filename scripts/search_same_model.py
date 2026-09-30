import os
import glob
import sys
import torch
import torchvision.transforms as T
from torchvision.models import mobilenet_v3_small, MobileNet_V3_Small_Weights
from PIL import Image
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

# Load model
weights = MobileNet_V3_Small_Weights.DEFAULT
model = mobilenet_v3_small(weights=weights)
model.eval()

# Remove classifier to get feature embedding
feature_extractor = model.features

transform = T.Compose([
    T.Resize((224, 224)),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Reference face / upper body from master model
ref_img_path = r'C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\web\assets\model_baku_master.jpg'
ref_img = Image.open(ref_img_path).convert('RGB')
# Crop face and head: top 5% to 25%, horizontal 35% to 65%
w, h = ref_img.size
ref_face = ref_img.crop((int(w * 0.35), int(h * 0.05), int(w * 0.65), int(h * 0.25)))
ref_face.save(r'C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\ref_model_face.jpg')

with torch.no_grad():
    ref_tensor = transform(ref_face).unsqueeze(0)
    ref_feat = feature_extractor(ref_tensor).mean(dim=[2, 3]).squeeze().numpy()
    ref_feat = ref_feat / np.linalg.norm(ref_feat)

print("Reference embedding generated.")

# Search all video thumbnails
export_dir = r"D:\Media\Telegram_Exports\ChatExport_2026-09-26"
video_thumbs = sorted(glob.glob(os.path.join(export_dir, "video_files", "*_thumb.jpg")))
print(f"Scanning {len(video_thumbs)} video thumbnails...")

matches = []

with torch.no_grad():
    for vt in video_thumbs:
        try:
            im = Image.open(vt).convert('RGB')
            vw, vh = im.size
            if vh < vw:  # Skip horizontal videos
                continue
            # Crop upper region where head is typically located
            crop = im.crop((int(vw * 0.25), int(vh * 0.05), int(vw * 0.75), int(vh * 0.35)))
            tensor = transform(crop).unsqueeze(0)
            feat = feature_extractor(tensor).mean(dim=[2, 3]).squeeze().numpy()
            feat = feat / np.linalg.norm(feat)
            sim = float(np.dot(ref_feat, feat))
            if sim > 0.65:
                matches.append((sim, vt))
        except Exception:
            pass

matches.sort(key=lambda x: x[0], reverse=True)
print(f"\nTop {min(20, len(matches))} video matches:")
for sim, vt in matches[:20]:
    print(f"{sim:.3f} -> {os.path.basename(vt)}")
