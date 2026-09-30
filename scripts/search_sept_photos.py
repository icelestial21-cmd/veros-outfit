import os
import glob
from PIL import Image

export_dir = r"D:\Media\Telegram_Exports\ChatExport_2026-09-26"
photos_dir = os.path.join(export_dir, "photos")

# Pattern: photo_*@DD-MM-YYYY_HH-MM-SS.jpg
# Check photos from 01-09-2025 to 05-09-2025
target_photos = []
for d in ['01-09-2025', '02-09-2025', '03-09-2025', '04-09-2025', '05-09-2025']:
    matched = glob.glob(os.path.join(photos_dir, f"*@{d}_*.jpg"))
    target_photos.extend(matched)

print(f"Found {len(target_photos)} photos in target date range.")
for p in target_photos[:30]:
    print(os.path.basename(p))
