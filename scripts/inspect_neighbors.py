import re
import os
import glob
import sys

sys.stdout.reconfigure(encoding='utf-8')

base = r'D:\Media\Telegram_Exports\ChatExport_2026-09-26'
html_files = sorted(glob.glob(os.path.join(base, 'messages*.html')))

target_msg_nums = [13, 51, 79, 99, 955]

for hf in html_files:
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()

    chunks = content.split('<div class="message ')
    for chunk in chunks[1:]:
        msg_id_match = re.search(r'id="message(\d+)"', chunk)
        if not msg_id_match:
            continue
        num = int(msg_id_match.group(1))
        
        # Check if within 5 of any target
        for t in target_msg_nums:
            if abs(num - t) <= 4:
                photos = re.findall(r'href="(photos/[^"]+)"', chunk)
                videos = re.findall(r'href="(video_files/[^"]+)"', chunk)
                text_match = re.search(r'<div class="text">([\s\S]*?)</div>', chunk)
                clean_text = ''
                if text_match:
                    clean = re.sub(r'<[^>]+>', ' ', text_match.group(1))
                    clean_text = ' '.join(clean.split())
                print(f"[Target {t}] Message {num}:")
                if photos: print(f"   Photos: {photos}")
                if videos: print(f"   Videos: {videos}")
                if clean_text: print(f"   Text: {clean_text[:120]}")
