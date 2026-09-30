import re
import os
import glob

base = r'D:\Media\Telegram_Exports\ChatExport_2026-09-26'
html_files = sorted(glob.glob(os.path.join(base, 'messages*.html')))

# The videos we saw:
# 1. Dolce & Gabbana white silk set (was MB-01_walk.mp4)
# 2. EA7 tracksuit (was MB-02_walk.mp4)
# 3. Gucci polo (was MB-03_walk.mp4)
# 4. Gucci cap (was MB-06_walk.mp4)
# 5. Gucci sweaters (was MB-07_walk.mp4)
# 6. LV denim jeans (was MB-11_walk.mp4)

# Let's find out what the original video filenames were in web/assets:
# Let's check which video files in D:\Media\Telegram_Exports\ChatExport_2026-09-26\video_files match them by size!
web_assets = r"C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\web\assets"
tg_vids = os.path.join(base, "video_files")

target_videos = [
    "MB-01_walk.mp4",
    "MB-02_walk.mp4",
    "MB-03_walk.mp4",
    "MB-06_walk.mp4",
    "MB-07_walk.mp4",
    "MB-11_walk.mp4",
]

matched_tg_names = {}
for tv in target_videos:
    tv_path = os.path.join(web_assets, tv)
    if os.path.exists(tv_path):
        size = os.path.getsize(tv_path)
        for f in os.listdir(tg_vids):
            fp = os.path.join(tg_vids, f)
            if os.path.getsize(fp) == size:
                matched_tg_names[tv] = f
                print(f"Matched {tv} ({size} bytes) -> {f}")
                break

print("\nSearching Telegram messages for these exact videos...")
for hf in html_files:
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()

    chunks = content.split('<div class="message ')
    for chunk in chunks[1:]:
        for tv, tg_name in matched_tg_names.items():
            if tg_name in chunk:
                msg_id = re.search(r'id="(message\d+)"', chunk)
                photos = re.findall(r'href="(photos/[^"]+)"', chunk)
                text = re.search(r'<div class="text">([\s\S]*?)</div>', chunk)
                clean_text = ''
                if text:
                    clean = re.sub(r'<[^>]+>', ' ', text.group(1))
                    clean_text = ' '.join(clean.split())
                print(f"\nFOUND {tv} ({tg_name}) in {msg_id.group(1) if msg_id else 'unknown'}:")
                print(f"  Photos in this message: {photos}")
                print(f"  Text: {clean_text}")
