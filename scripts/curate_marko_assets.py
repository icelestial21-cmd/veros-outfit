import os
import shutil
import json

src_export = r"D:\Media\Telegram_Exports\ChatExport_2026-09-26"
photos_dir = os.path.join(src_export, "photos")
videos_dir = os.path.join(src_export, "video_files")

target_assets = r"C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\web\assets"
os.makedirs(target_assets, exist_ok=True)

# 1. Customer Proof Deliveries
proofs = [
    ("photo_234@25-09-2024_14-51-38.jpg", "delivery_proof_package.jpg", "Milano, Italy — Signature Unboxing"),
    ("photo_235@26-09-2024_16-17-05.jpg", "delivery_proof_italy.jpg", "Rome, Italy — Transit Receipt"),
    ("photo_644@08-10-2024_14-20-59.jpg", "delivery_proof_spain.jpg", "Madrid, Spain — Verified Delivery")
]

for src_name, dst_name, desc in proofs:
    s = os.path.join(photos_dir, src_name)
    d = os.path.join(target_assets, dst_name)
    if os.path.exists(s):
        shutil.copy2(s, d)
        print(f"Copied proof: {dst_name}")

# 2. Select Runway Videos
# Pick high quality MP4s under 15MB for fast web loading
candidate_videos = [
    ("IMG_3698.MP4", "hero_runway_loop.mp4"),
    ("IMG_5174.MP4", "video_lookbook_1.mp4"),
    ("IMG_7121.MP4", "video_lookbook_2.mp4"),
    ("IMG_8812.MP4", "video_lookbook_3.mp4"),
    ("IMG_5590.MP4", "video_lookbook_4.mp4")
]

for src_name, dst_name in candidate_videos:
    s = os.path.join(videos_dir, src_name)
    d = os.path.join(target_assets, dst_name)
    if os.path.exists(s):
        shutil.copy2(s, d)
        print(f"Copied video: {dst_name}")

# 3. Product Photography Catalog Curation
# We will define 12 master flagship products representing the full spectrum of Marko Baku
products = [
    {
        "id": "MB-01",
        "name": "Baku Monogram Heavyweight Silk-Cotton Tee",
        "category": "Knits & Polos",
        "price": 55,
        "badge": "New Collection 2025",
        "sizes": ["M", "L", "XL", "XXL", "3XL"],
        "src_photo": "photo_214@16-09-2024_16-19-05.jpg",
        "detail_photo": "photo_215@16-09-2024_16-25-05.jpg",
        "video": "video_lookbook_1.mp4",
        "description": "Double-mercerized 280 GSM cotton with micro-ribbed crew collar and subtle chest emblem. Tailored slim-contemporary drape.",
        "fabric": "95% Pima Cotton, 5% Elastane",
        "origin": "Tailored in Baku / Fabric from Como, Italy"
    },
    {
        "id": "MB-02",
        "name": "Caspian Textured Quarter-Zip Knit Polo",
        "category": "Knits & Polos",
        "price": 45,
        "badge": "Signature Staple",
        "sizes": ["M", "L", "XL", "XXL"],
        "src_photo": "photo_54@01-08-2024_01-10-17.jpg",
        "detail_photo": "photo_55@01-08-2024_01-10-17.jpg",
        "video": "video_lookbook_2.mp4",
        "description": "Textured waffle weave breathable summer knit with matte gunmetal zipper and tailored ribbed cuffs.",
        "fabric": "100% Breathable Combed Cotton",
        "origin": "Atelier Marko Baku"
    },
    {
        "id": "MB-03",
        "name": "Old-World Suede Overshirt Jacket",
        "category": "Suits & Outerwear",
        "price": 90,
        "badge": "Luxury Outerwear",
        "sizes": ["M", "L", "XL", "XXL", "3XL"],
        "src_photo": "photo_227@22-09-2024_14-30-41.jpg",
        "detail_photo": "photo_845@22-10-2024_10-58-33.jpg",
        "video": "hero_runway_loop.mp4",
        "description": "Supple micro-suede cut into a structured modular overshirt silhouette with horn buttons and chest bellows pockets.",
        "fabric": "Ultra-Fine Vegan Micro-Suede / Cupro Lining",
        "origin": "Artisanal Baku Workshop"
    },
    {
        "id": "MB-04",
        "name": "Tailored Pleated Straight-Leg Trousers",
        "category": "Denim & Trousers",
        "price": 55,
        "badge": "Essential Sartorial",
        "sizes": ["30", "31", "32", "33", "34", "36"],
        "src_photo": "photo_714@09-10-2024_12-09-00.jpg",
        "detail_photo": "photo_715@09-10-2024_12-09-00.jpg",
        "video": "",
        "description": "Double forward pleats with side adjusters and a clean 1.5-inch turn-up hem. Mid-rise tailoring engineered for sneaker pairings.",
        "fabric": "80% Fine Wool Blend, 18% Viscose, 2% Lycra",
        "origin": "Tailored in Baku"
    },
    {
        "id": "MB-05",
        "name": "Minimalist Low-Top Calfskin Sneaker",
        "category": "Footwear",
        "price": 88,
        "badge": "Limited Run",
        "sizes": ["39", "40", "41", "42", "43", "44"],
        "src_photo": "photo_228@25-09-2024_03-42-19.jpg",
        "detail_photo": "photo_229@25-09-2024_03-47-09.jpg",
        "video": "",
        "description": "Monochrome clean-toe luxury sneaker on a durable Margom-style cupsole with cushioned calf leather insoles.",
        "fabric": "100% Full-Grain Calf Leather",
        "origin": "Handmade"
    },
    {
        "id": "MB-06",
        "name": "Prestige Autumn Tracksuit Set (Jacket + Pants)",
        "category": "Suits & Outerwear",
        "price": 110,
        "badge": "Full Set",
        "sizes": ["M", "L", "XL", "XXL", "3XL"],
        "src_photo": "photo_722@10-10-2024_15-59-57.jpg",
        "detail_photo": "photo_723@10-10-2024_15-59-57.jpg",
        "video": "video_lookbook_3.mp4",
        "description": "Heavy interlock technical jersey tracksuit featuring a zip jacket with funnel neck and tapered piped trousers.",
        "fabric": "70% Viscose, 25% Polyamide, 5% Elastane",
        "origin": "Marko Atelier Production"
    },
    {
        "id": "MB-07",
        "name": "Signature Waffle Weave Resort Polo",
        "category": "Knits & Polos",
        "price": 40,
        "badge": "High Demand",
        "sizes": ["M", "L", "XL", "XXL"],
        "src_photo": "photo_529@06-10-2024_06-59-06.jpg",
        "detail_photo": "photo_530@06-10-2024_06-59-06.jpg",
        "video": "",
        "description": "Relaxed open-collar Johnny polo in heavy breathable knit waffle fabric for high summer and tropical wear.",
        "fabric": "100% Organic Pima Cotton",
        "origin": "Baku Atelier"
    },
    {
        "id": "MB-08",
        "name": "Deep Indigo Japanese Selvedge-Cut Denim",
        "category": "Denim & Trousers",
        "price": 60,
        "badge": "Premium Denim",
        "sizes": ["30", "32", "34", "36", "38"],
        "src_photo": "photo_738@11-10-2024_14-28-48.jpg",
        "detail_photo": "photo_739@11-10-2024_14-28-48.jpg",
        "video": "",
        "description": "13.5 oz raw indigo ring-spun denim with clean selvedge outseam, copper rivets, and a modern slim-straight silhouette.",
        "fabric": "99% Cotton, 1% Comfort Stretch",
        "origin": "Crafted in Baku"
    },
    {
        "id": "MB-09",
        "name": "Monochrome Runner Trainer",
        "category": "Footwear",
        "price": 45,
        "badge": "Seasonal Promotion",
        "sizes": ["40", "41", "42", "43", "44"],
        "src_photo": "photo_589@07-10-2024_11-13-58.jpg",
        "detail_photo": "photo_590@07-10-2024_11-13-58.jpg",
        "video": "",
        "description": "Lightweight breathable mesh athletic runner trimmed in soft split suede with ergonomic EVA foam cushioning.",
        "fabric": "Technical Mesh & Suede",
        "origin": "Imported Sole"
    },
    {
        "id": "MB-10",
        "name": "Luxury Silk-Blend Fine Gauge Crewneck",
        "category": "Knits & Polos",
        "price": 60,
        "badge": "Luxury Tier",
        "sizes": ["M", "L", "XL", "XXL", "3XL"],
        "src_photo": "photo_397@01-10-2024_15-45-52.jpg",
        "detail_photo": "photo_398@01-10-2024_15-45-52.jpg",
        "video": "video_lookbook_4.mp4",
        "description": "16-gauge silk and merino wool blend sweater engineered for seamless layering under blazers and leather jackets.",
        "fabric": "70% Merino Wool, 30% Silk",
        "origin": "Atelier Marko"
    },
    {
        "id": "MB-11",
        "name": "Ready-to-Wear Daily Graphic T-Shirt",
        "category": "Essentials",
        "price": 14,
        "badge": "Wholesale Bundle Tier",
        "sizes": ["M", "L", "XL", "XXL"],
        "src_photo": "photo_1@30-07-2024_15-00-59.jpg",
        "detail_photo": "photo_2@30-07-2024_15-00-59.jpg",
        "video": "",
        "description": "Classic 210 GSM drop-shoulder boxy tee with high-density archival graphic print. Free worldwide shipping on bundles of 10+.",
        "fabric": "100% Combed Ringspun Cotton",
        "origin": "Baku Ready-to-Wear"
    },
    {
        "id": "MB-12",
        "name": "Tailored Double-Breasted Travel Blazer",
        "category": "Suits & Outerwear",
        "price": 99,
        "badge": "Atelier Tailoring",
        "sizes": ["48", "50", "52", "54"],
        "src_photo": "photo_797@13-10-2024_14-17-08.jpg",
        "detail_photo": "photo_798@13-10-2024_14-17-08.jpg",
        "video": "",
        "description": "Soft-shouldered unstructured Neapolitan-inspired blazer with peak lapels, patch pockets, and unlined interior for effortless drape.",
        "fabric": "Tropical Wool Hopsack",
        "origin": "Atelier Bespoke Division"
    }
]

# Copy product photos
for p in products:
    # Main photo
    s1 = os.path.join(photos_dir, p['src_photo'])
    d1 = os.path.join(target_assets, f"{p['id']}_main.jpg")
    if os.path.exists(s1):
        shutil.copy2(s1, d1)
        p['main_image'] = f"assets/{p['id']}_main.jpg"
    else:
        print(f"Warning: Missing {s1}")
        
    # Detail photo
    s2 = os.path.join(photos_dir, p['detail_photo'])
    d2 = os.path.join(target_assets, f"{p['id']}_detail.jpg")
    if os.path.exists(s2):
        shutil.copy2(s2, d2)
        p['detail_image'] = f"assets/{p['id']}_detail.jpg"
    else:
        p['detail_image'] = p.get('main_image', '')

    # Set video relative path
    if p['video']:
        p['video_url'] = f"assets/{p['video']}"
    else:
        p['video_url'] = ""

out_json = os.path.join(r"C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\web", "products.json")
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(products, f, indent=2, ensure_ascii=False)

print(f"Successfully staged {len(products)} products and saved catalog to {out_json}")
