import re
import os
import glob
import sys
from html import unescape

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

base = r'D:\Media\Telegram_Exports\ChatExport_2026-09-26'
html_files = sorted(glob.glob(os.path.join(base, 'messages*.html')))

raw_messages = []

for hf in html_files:
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()

    chunks = content.split('<div class="message ')
    for chunk in chunks[1:]:
        msg_id_match = re.search(r'id="(message\d+)"', chunk)
        msg_id = msg_id_match.group(1) if msg_id_match else None
        
        photos = re.findall(r'href="(photos/[^"]+)"', chunk)
        videos = re.findall(r'href="(video_files/[^"]+)"', chunk)
        
        text_match = re.search(r'<div class="text">([\s\S]*?)</div>', chunk)
        clean_text = ''
        if text_match:
            raw_text = text_match.group(1)
            raw_text = re.sub(r'<br\s*/?>', '\n', raw_text)
            clean = re.sub(r'<[^>]+>', ' ', raw_text)
            clean_text = unescape(' '.join(clean.split()))

        date_match = re.search(r'title="([^"]+)"', chunk)
        date_str = date_match.group(1) if date_match else ''

        num_id = int(msg_id.replace('message', '')) if msg_id else 0

        raw_messages.append({
            'num_id': num_id,
            'id': msg_id,
            'file': os.path.basename(hf),
            'photos': photos,
            'videos': videos,
            'text': clean_text,
            'date': date_str
        })

raw_messages.sort(key=lambda x: x['num_id'])

# Group adjacent messages (e.g. within difference of 5 message IDs or same date)
# Let's inspect messages that have text with prices or brand names
print(f"Total messages: {len(raw_messages)}")

drops = []
for i, m in enumerate(raw_messages):
    text = m['text']
    # Check if text contains brand, price, or size
    if any(keyword in text.lower() for keyword in ['manat', 'azn', 'razmer', 'size', 'qiymət', 'qiymet', '$', 'endirim', 'baku', 'brand']):
        # Look backwards and forwards 3 messages for associated photos and videos
        nearby_photos = []
        nearby_videos = []
        for offset in range(-3, 4):
            idx = i + offset
            if 0 <= idx < len(raw_messages):
                nearby_photos.extend(raw_messages[idx]['photos'])
                nearby_videos.extend(raw_messages[idx]['videos'])
        
        drops.append({
            'lead_msg': m,
            'photos': list(dict.fromkeys(nearby_photos)),
            'videos': list(dict.fromkeys(nearby_videos))
        })

print(f"Found {len(drops)} drops with price/product keywords.")
with open(r'C:\Users\User\.gemini\antigravity\scratch\telegram_drops_summary.txt', 'w', encoding='utf-8') as out:
    for d in drops[:50]:
        lm = d['lead_msg']
        out.write(f"=== MSG {lm['id']} ({lm['date']}) ===\n")
        out.write(f"TEXT: {lm['text']}\n")
        out.write(f"PHOTOS ({len(d['photos'])}): {d['photos'][:5]}\n")
        out.write(f"VIDEOS ({len(d['videos'])}): {d['videos'][:3]}\n\n")

print("Wrote summary of 50 drops to C:\\Users\\User\\.gemini\\antigravity\\scratch\\telegram_drops_summary.txt")
