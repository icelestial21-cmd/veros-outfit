import os
import re
import glob
import sys

sys.stdout.reconfigure(encoding='utf-8')

export_path = r'D:\Media\Telegram_Exports\ChatExport_2026-09-26'
html_files = sorted(glob.glob(os.path.join(export_path, 'messages*.html')))

print(f"Scanning {len(html_files)} HTML files for video posts...")
video_posts = []

for hf in html_files:
    fname = os.path.basename(hf)
    with open(hf, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    chunks = html.split('<div class="message ')
    for c in chunks:
        vmatch = re.search(r'href="(video_files/[^"]+)"', c)
        if vmatch:
            vfile = vmatch.group(1)
            dmatch = re.search(r'title="([^"]+)"', c)
            date = dmatch.group(1) if dmatch else ''
            tmatch = re.search(r'<div class="text">([\s\S]*?)</div>', c)
            text = ''
            if tmatch:
                text = re.sub(r'<[^>]+>', '', tmatch.group(1)).strip().replace('\n', ' ')
            durmatch = re.search(r'<div class="video_duration">\s*([^<]+)\s*</div>', c)
            duration = durmatch.group(1).strip() if durmatch else ''
            video_posts.append({
                'html': fname,
                'file': vfile,
                'date': date,
                'duration': duration,
                'text': text[:80]
            })

print(f"Found {len(video_posts)} total video posts.")

# Print videos from August/September 2025 or mentioning shirt / koynek / silk
keywords = ['shirt', 'koynek', 'köynək', 'italy', 'ipək', 'ipek', 'ipəy', 'ipak', 'silk', 'klassik', 'classic']
print("\n--- Matching Videos by Text Keywords ---")
for vp in video_posts:
    t_lower = vp['text'].lower()
    if any(k in t_lower for k in keywords):
        print(f"[{vp['date']}] {vp['file']} ({vp['duration']}) | {vp['text']}")

# Also print videos within +/- 5 days of 02.09.2025
print("\n--- Videos around 02.09.2025 ---")
for vp in video_posts:
    if '09.2025' in vp['date'] or '08.2025' in vp['date']:
        d = vp['date'][:10]
        # check if early September 2025 (e.g. 25.08 to 10.09)
        if any(d.startswith(f"{day:02d}.09.2025") for day in range(1, 10)) or any(d.startswith(f"{day:02d}.08.2025") for day in range(25, 32)):
            print(f"[{vp['date']}] {vp['file']} ({vp['duration']}) | {vp['text']}")
