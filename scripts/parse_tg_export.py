import re
import os

path = r'C:\Users\User\Downloads\Telegram Desktop\ChatExport_2026-09-26\messages.html'

with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Extract messages
messages = re.findall(r'<div class="message default clearfix" id="([^"]+)">([\s\S]*?)(?=<div class="message default clearfix"|$)', html)

extracted_posts = []

for msg_id, msg_content in messages:
    date_m = re.search(r'<div class="pull_right date details" title="([^"]+)">', msg_content)
    date_str = date_m.group(1) if date_m else "Unknown date"
    
    # Text
    text_m = re.search(r'<div class="text">([\s\S]*?)</div>', msg_content)
    text = ""
    if text_m:
        text = re.sub(r'<[^>]+>', ' ', text_m.group(1)).strip()
        text = re.sub(r'\s+', ' ', text)
        
    # Media
    photos = re.findall(r'href="([^"]+\.jpg)"', msg_content)
    videos = re.findall(r'href="([^"]+\.(?:mp4|mov))"', msg_content)
    
    extracted_posts.append({
        'id': msg_id,
        'date': date_str,
        'text': text,
        'photos': photos,
        'videos': videos
    })

out_path = r'C:\Users\User\.gemini\antigravity\scratch\telegram_catalog_parsed.txt'
with open(out_path, 'w', encoding='utf-8') as out:
    out.write(f"MARKO BAKU TELEGRAM CATALOG EXTRACTION ANALYSIS\n")
    out.write(f"Total Messages Analyzed: {len(extracted_posts)}\n\n")
    for i, p in enumerate(extracted_posts):
        out.write(f"--- Post #{i+1} [ID: {p['id']}] Date: {p['date']} ---\n")
        if p['text']:
            out.write(f"Caption: {p['text']}\n")
        if p['photos']:
            out.write(f"Photos ({len(p['photos'])}): {', '.join(p['photos'][:5])}\n")
        if p['videos']:
            out.write(f"Videos ({len(p['videos'])}): {', '.join(p['videos'][:3])}\n")
        out.write("\n")

print(f"Successfully processed {len(extracted_posts)} posts to {out_path}")

# Check current export folder status
export_dir = r'C:\Users\User\Downloads\Telegram Desktop\ChatExport_2026-09-26'
photo_count = len(os.listdir(os.path.join(export_dir, 'photos'))) if os.path.exists(os.path.join(export_dir, 'photos')) else 0
video_count = len(os.listdir(os.path.join(export_dir, 'video_files'))) if os.path.exists(os.path.join(export_dir, 'video_files')) else 0
print(f"Current Assets Downloaded: {photo_count} photos, {video_count} video files.")
