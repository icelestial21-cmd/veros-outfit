import json

json_path = r"C:\Users\User\.gemini\antigravity\scratch\aligned_telegram_drops.json"
with open(json_path, 'r', encoding='utf-8') as f:
    drops = json.load(f)

both = [d for d in drops if d['has_both']]

out_txt = r"C:\Users\User\.gemini\antigravity\scratch\aligned_drops_report.txt"
with open(out_txt, 'w', encoding='utf-8') as out:
    out.write(f"TOTAL POSTS WITH BOTH AUTHENTIC PHOTO & VIDEO: {len(both)}\n\n")
    for i, b in enumerate(both):
        out.write(f"=== Drop #{i+1} [Index: {b['index']} | ID: {b['id']}] ===\n")
        out.write(f"Date: {b['date']} | Extracted Price: ${b['price']}\n")
        out.write(f"Caption: {b['caption']}\n")
        out.write(f"Videos ({len(b['videos'])}): {b['videos']}\n")
        out.write(f"Photos ({len(b['photos'])}): {b['photos'][:6]}\n")
        out.write("\n")

print(f"Report written for {len(both)} verified aligned drops.")
