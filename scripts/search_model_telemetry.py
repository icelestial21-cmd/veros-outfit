import os
import re
import glob
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

export_dir = r"D:\Media\Telegram_Exports\ChatExport_2026-09-26"
html_files = sorted(glob.glob(os.path.join(export_dir, "messages*.html")))

search_patterns = [
    r'model',
    r'boy\s*\d+',
    r'\d+\s*sm',
    r'\d+\s*kq',
    r'\d+\s*kg',
    r'əynində',
    r'eyninde',
    r'boyu',
    r'çəki',
    r'ceki',
    r'рост',
    r'вес'
]

compiled = [re.compile(p, re.IGNORECASE) for p in search_patterns]

found = []

for hf in html_files:
    with open(hf, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    parts = re.split(r'<div class="message default clearfix[^"]*"', content)
    for part in parts[1:]:
        text_match = re.search(r'<div class="text">([\s\S]*?)</div>', part)
        if not text_match:
            continue
        text_raw = text_match.group(1)
        plain = re.sub(r'<[^>]+>', ' ', text_raw).strip()
        
        matches_found = [p.pattern for p in compiled if p.search(plain)]
        if matches_found:
            photos = re.findall(r'href="(photos/[^"]+)"', part)
            videos = re.findall(r'href="(video_files/[^"]+)"', part)
            found.append({
                "file": os.path.basename(hf),
                "matched_patterns": matches_found,
                "text": plain,
                "photos": photos,
                "videos": videos
            })

for i, h in enumerate(found):
    print(f"\n[{i+1}] ({h['file']}) Matches: {h['matched_patterns']}")
    print(f"    Text: {h['text'][:200]}")
    if h['photos']:
        print(f"    Photos ({len(h['photos'])}): {h['photos'][:4]}")
    if h['videos']:
        print(f"    Videos ({len(h['videos'])}): {h['videos'][:2]}")
