import os
import re
import json

html_path = r"D:\Media\Telegram_Exports\ChatExport_2026-09-26\messages.html"
export_dir = r"D:\Media\Telegram_Exports\ChatExport_2026-09-26"

with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

chunks = content.split('<div class="message default clearfix"')

matched_posts = []

for idx, c in enumerate(chunks[1:]):
    msg_id = re.search(r'id="([^"]+)"', c)
    mid = msg_id.group(1) if msg_id else f"msg_{idx}"
    
    date_m = re.search(r'<div class="pull_right date details" title="([^"]+)">', c)
    date_str = date_m.group(1) if date_m else ""
    
    text_m = re.search(r'<div class="text">([\s\S]*?)</div>', c)
    text = ""
    if text_m:
        text = re.sub(r'<[^>]+>', ' ', text_m.group(1)).strip()
        text = re.sub(r'\s+', ' ', text)
        
    photos = re.findall(r'href="([^"]+\.jpg)"', c, re.IGNORECASE)
    full_photos = [p for p in photos if '_thumb' not in p]
    
    videos = re.findall(r'href="([^"]+\.(?:mp4|mov))"', c, re.IGNORECASE)
    full_videos = [v for v in videos if '_thumb' not in v]
    
    prices = re.findall(r'(\d+)\s*(?:\$|dollars|USD)', text, re.IGNORECASE)
    price_val = int(prices[0]) if prices else None
    
    # Check if files actually exist on disk in D:\Media\Telegram_Exports...
    existing_photos = [p for p in full_photos if os.path.exists(os.path.join(export_dir, p))]
    existing_videos = [v for v in full_videos if os.path.exists(os.path.join(export_dir, v))]
    
    if existing_photos or existing_videos:
        matched_posts.append({
            'index': idx + 1,
            'id': mid,
            'date': date_str,
            'caption': text,
            'price': price_val,
            'photos': existing_photos,
            'videos': existing_videos,
            'has_both': len(existing_photos) > 0 and len(existing_videos) > 0
        })

out_json = r"C:\Users\User\.gemini\antigravity\scratch\aligned_telegram_drops.json"
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(matched_posts, f, indent=2, ensure_ascii=False)

both = [p for p in matched_posts if p['has_both']]

out_txt = r"C:\Users\User\.gemini\antigravity\scratch\aligned_drops_report.txt"
with open(out_txt, "w", encoding="utf-8") as out:
    out.write(f"TOTAL POSTS WITH BOTH AUTHENTIC PHOTO & VIDEO: {len(both)}\n\n")
    for i, b in enumerate(both):
        out.write(f"=== Drop #{i+1} [Index: {b['index']} | ID: {b['id']}] ===\n")
        out.write(f"Date: {b['date']} | Extracted Price: ${b['price']}\n")
        out.write(f"Caption: {b['caption']}\n")
        out.write(f"Videos ({len(b['videos'])}): {b['videos']}\n")
        out.write(f"Photos ({len(b['photos'])}): {b['photos'][:6]}\n\n")

print(f"Extraction successful: {len(matched_posts)} total drops, {len(both)} with both photo and video.")
