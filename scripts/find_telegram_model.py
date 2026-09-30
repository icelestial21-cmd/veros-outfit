import os
import re
import glob
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

export_dir = r"D:\Media\Telegram_Exports\ChatExport_2026-09-26"
html_files = sorted(glob.glob(os.path.join(export_dir, "messages*.html")))

# Sample the first 100 messages with text and photos/videos across files
sampled = []
for hf in html_files:
    with open(hf, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    messages = re.split(r'<div class="message default clearfix[^"]*"', content)
    for msg in messages[1:]:
        text_match = re.search(r'<div class="text">([\s\S]*?)</div>', msg)
        photos = re.findall(r'href="(photos/[^"]+)"', msg)
        videos = re.findall(r'href="(video_files/[^"]+)"', msg)
        
        if text_match and (photos or videos):
            plain_text = re.sub(r'<[^>]+>', ' ', text_match.group(1)).strip()
            if len(plain_text) > 10:
                sampled.append({
                    "source": os.path.basename(hf),
                    "text": plain_text,
                    "photos": photos,
                    "videos": videos
                })
        if len(sampled) >= 20:
            break
    if len(sampled) >= 20:
        break

print(f"Sampled {len(sampled)} messages:")
for i, s in enumerate(sampled):
    print(f"\n[{i+1}] {s['source']}: {s['text'][:120]}")
    if s['photos']:
        print(f"    Photos: {s['photos'][:2]}")
    if s['videos']:
        print(f"    Videos: {s['videos'][:2]}")
