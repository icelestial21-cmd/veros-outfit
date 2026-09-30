import os
import json

json_path = r"C:\Users\User\.gemini\antigravity\scratch\marko_catalog_structured.json"
with open(json_path, 'r', encoding='utf-8') as f:
    items = json.load(f)

print(f"Total catalog entries: {len(items)}")

posts_with_media = [i for i in items if i['photo_count'] > 0 or i['video_count'] > 0]
print(f"Posts with media: {len(posts_with_media)}")

posts_with_video = [i for i in items if i['video_count'] > 0]
print(f"Posts with videos: {len(posts_with_video)}")

posts_with_price = [i for i in items if i['price'] is not None]
print(f"Posts with explicit price: {len(posts_with_price)}")

# Categorize into usable collections
collections = {
    "Suits & Luxury Tailoring ($70 - $110)": [],
    "Smart-Casual Knitwear & Polos ($35 - $60)": [],
    "Designer Denim & Trousers ($50 - $110)": [],
    "Footwear & Sneakers ($45 - $99)": [],
    "Essential Graphic & Logo Tees ($14 - $35)": [],
    "Customer Proof & Delivery Confirmations": []
}

for item in items:
    cap = item['caption'].lower()
    price = item['price']
    
    if any(k in cap for k in ['customer satisfaction', 'safe and sound', 'italy', 'spain', 'reached our customer', 'merchandise i was eagerly waiting']):
        collections["Customer Proof & Delivery Confirmations"].append(item)
    elif any(k in cap for k in ['size 39', 'size 40', 'size 41', 'size 42', 'size 43', 'size 44', 'shoe', 'sneaker']):
        collections["Footwear & Sneakers ($45 - $99)"].append(item)
    elif any(k in cap for k in ['size 30', 'size 31', 'size 32', 'size 33', 'size 34', 'size 35', 'size 36', 'size 38']):
        collections["Designer Denim & Trousers ($50 - $110)"].append(item)
    elif price and price >= 70:
        collections["Suits & Luxury Tailoring ($70 - $110)"].append(item)
    elif price and price in [35, 40, 45, 50, 55, 60]:
        collections["Smart-Casual Knitwear & Polos ($35 - $60)"].append(item)
    elif price and price < 35:
        collections["Essential Graphic & Logo Tees ($14 - $35)"].append(item)

out_report = r"C:\Users\User\.gemini\antigravity\scratch\usable_collections_summary.txt"
with open(out_report, 'w', encoding='utf-8') as f:
    f.write("=== MARKO BAKU USABLE ASSET CURATION REPORT ===\n\n")
    for name, list_items in collections.items():
        f.write(f"### {name}: {len(list_items)} items\n")
        for it in list_items[:5]:
            f.write(f"  - ID: {it['id']} | Date: {it['date']} | Price: ${it['price']} | Photos: {it['photo_count']} | Videos: {it['video_count']}\n")
            if it['caption']:
                f.write(f"    Snippet: {it['caption'][:80]}...\n")
        f.write("\n")

print("Collections summary written.")
