import os
import re

html_path = r"C:\Users\User\Downloads\Telegram Desktop\ChatExport_2026-09-26\messages.html"
if not os.path.exists(html_path):
    print("messages.html not found!")
    exit(1)

with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Channel title
title_m = re.search(r'<div class="text bold">([^<]+)</div>', content)
print(f"Channel Title: {title_m.group(1).strip() if title_m else 'Unknown'}")

# Total messages
default_msgs = re.findall(r'<div class="message default clearfix" id="([^"]+)">', content)
print(f"Total default message elements: {len(default_msgs)}")

service_msgs = re.findall(r'<div class="message service" id="([^"]+)">', content)
print(f"Total service messages: {len(service_msgs)}")

# Analyze media files on disk
export_dir = r"C:\Users\User\Downloads\Telegram Desktop\ChatExport_2026-09-26"
photos_dir = os.path.join(export_dir, 'photos')
videos_dir = os.path.join(export_dir, 'video_files')

photos = os.listdir(photos_dir) if os.path.exists(photos_dir) else []
videos = os.listdir(videos_dir) if os.path.exists(videos_dir) else []

print(f"Disk Photos: {len(photos)}")
print(f"Disk Videos: {len(videos)}")

# Check video sizes
video_sizes = [os.path.getsize(os.path.join(videos_dir, v)) for v in videos]
total_vid_size_mb = sum(video_sizes) / (1024 * 1024) if video_sizes else 0
print(f"Total Video Volume: {total_vid_size_mb:.2f} MB across {len(videos)} files")
if video_sizes:
    print(f"Avg Video Size: {(total_vid_size_mb / len(video_sizes)):.2f} MB (Max: {max(video_sizes)/(1024*1024):.2f} MB)")

# Extract pricing and SKU patterns
prices = []
whatsapp_contacts = set()
instagram_links = set()
codes = []

# Split by message default clearfix
chunks = content.split('<div class="message default clearfix"')
for c in chunks[1:]:
    text_m = re.search(r'<div class="text">([\s\S]*?)</div>', c)
    if text_m:
        raw_text = re.sub(r'<[^>]+>', ' ', text_m.group(1))
        found_prices = re.findall(r'(\d+)\s*(?:\$|dollars|USD)', raw_text, re.IGNORECASE)
        prices.extend([int(p) for p in found_prices])
        
        wa = re.findall(r'wa\.me/([^\s<"]+)', raw_text)
        whatsapp_contacts.update(wa)
        
        ig = re.findall(r'instagram\.com/([^\s<"]+)', raw_text)
        instagram_links.update(ig)
        
        kod = re.findall(r'KOD:\s*([^\s\n<"]+)', raw_text)
        codes.extend(kod)

print(f"Found {len(prices)} price references.")
if prices:
    print(f"Price range: ${min(prices)} - ${max(prices)}")
    print(f"Price distribution: {sorted(list(set(prices)))}")

print(f"WhatsApp Contacts: {whatsapp_contacts}")
print(f"Instagram Links: {instagram_links}")
print(f"Sample Product Codes: {codes[:10]}")
