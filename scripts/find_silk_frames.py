import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

export_path = r'D:\Media\Telegram_Exports\ChatExport_2026-09-26'
html_file = os.path.join(export_path, 'messages6.html')

with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

chunks = html.split('<div class="message ')
print(f"Total message chunks: {len(chunks)}")

target = 'copy_3FD097F2-149E-4E5E-B23E-B4FE97836874.mov'
for idx, chunk in enumerate(chunks):
    if target in chunk:
        print(f"Found target at chunk {idx}")
        start = max(1, idx - 5)
        end = min(len(chunks), idx + 10)
        for j in range(start, end):
            c = chunks[j]
            media_match = re.search(r'href="((?:photos|video_files)/[^"]+)"', c)
            media = media_match.group(1) if media_match else 'no media'
            date_match = re.search(r'title="([^"]+)"', c)
            date = date_match.group(1) if date_match else ''
            text_match = re.search(r'<div class="text">([\s\S]*?)</div>', c)
            text = text_match.group(1).strip() if text_match else ''
            text = re.sub(r'<[^>]+>', '', text).replace('\n', ' ')
            # sanitize for console
            text_clean = text.encode('ascii', errors='replace').decode('ascii')
            print(f"[{j}] {date} | {media} | {text_clean[:60]}")
        break
