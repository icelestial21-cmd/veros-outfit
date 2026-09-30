import os
import re
import json

html_path = r"C:\Users\User\Downloads\Telegram Desktop\ChatExport_2026-09-26\messages.html"
export_dir = r"C:\Users\User\Downloads\Telegram Desktop\ChatExport_2026-09-26"

with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

chunks = content.split('<div class="message default clearfix"')

catalog_items = []

for c in chunks[1:]:
    msg_id = re.search(r'id="([^"]+)"', c)
    mid = msg_id.group(1) if msg_id else "unknown"
    
    date_m = re.search(r'<div class="pull_right date details" title="([^"]+)">', c)
    date_str = date_m.group(1) if date_m else ""
    
    text_m = re.search(r'<div class="text">([\s\S]*?)</div>', c)
    text = ""
    if text_m:
        text = re.sub(r'<[^>]+>', ' ', text_m.group(1)).strip()
        text = re.sub(r'\s+', ' ', text)
        
    photos = re.findall(r'href="([^"]+\.jpg)"', c, re.IGNORECASE)
    # Filter out photo thumbs
    full_photos = [p for p in photos if '_thumb' not in p]
    
    videos = re.findall(r'href="([^"]+\.(?:mp4|mov))"', c, re.IGNORECASE)
    full_videos = [v for v in videos if '_thumb' not in v]
    
    # Extract price
    prices = re.findall(r'(\d+)\s*(?:\$|dollars|USD)', text, re.IGNORECASE)
    price_val = int(prices[0]) if prices else None
    
    # Categorize product based on text or context
    category = "General Apparel"
    lower_t = text.lower()
    if any(k in lower_t for k in ['t-shirt', 't-shirts', 'tshirt']):
        category = "T-Shirts & Polos"
    elif any(k in lower_t for k in ['shoe', 'shoes', 'sneaker', 'sneakers', 'size 40', 'size 41', 'size 42', 'size 43', 'size 44']):
        category = "Footwear & Sneakers"
    elif any(k in lower_t for k in ['pant', 'pants', 'trousers', 'jean', 'jeans', 'size 30', 'size 31', 'size 32', 'size 33', 'size 34', 'size 35', 'size 36', 'size 38']):
        category = "Denim & Trousers"
    elif any(k in lower_t for k in ['jacket', 'coat', 'blazer', 'suit', 'outerwear']) or (price_val and price_val >= 70):
        category = "Luxury Tailoring & Outerwear"
    elif any(k in lower_t for k in ['sweater', 'hoodie', 'knit', 'knitwear', 'handmade']):
        category = "Knitwear & Sweaters"
    elif price_val and price_val <= 20:
        category = "Essential T-Shirts"
    elif price_val and price_val in [35, 40, 45, 50, 55, 60]:
        category = "Smart Casual & Polos"
        
    if full_photos or full_videos or text:
        catalog_items.append({
            'id': mid,
            'date': date_str,
            'caption': text,
            'price': price_val,
            'category': category,
            'photo_count': len(full_photos),
            'video_count': len(full_videos),
            'photos': full_photos,
            'videos': full_videos
        })

out_json = r"C:\Users\User\.gemini\antigravity\scratch\marko_catalog_structured.json"
with open(out_json, 'w', encoding='utf-8') as f:
    json.dump(catalog_items, f, indent=2, ensure_ascii=False)

print(f"Parsed {len(catalog_items)} total catalog items.")
print(f"Items with videos: {len([i for i in catalog_items if i['video_count'] > 0])}")
print(f"Items with full photos: {len([i for i in catalog_items if i['photo_count'] > 0])}")
print(f"Items with both photo and video: {len([i for i in catalog_items if i['photo_count'] > 0 and i['video_count'] > 0])}")

categories = {}
for item in catalog_items:
    c = item['category']
    categories[c] = categories.get(c, 0) + 1

print("\nBreakdown by Category:")
for c, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
    print(f"  - {c}: {count} items")
