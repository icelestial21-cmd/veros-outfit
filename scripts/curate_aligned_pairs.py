import json
import os

with open(r"C:\Users\User\.gemini\antigravity\scratch\aligned_telegram_drops.json", "r", encoding="utf-8") as f:
    drops = json.load(f)

both = [d for d in drops if d['has_both']]

out_file = r"C:\Users\User\.gemini\antigravity\scratch\curated_aligned_pairs.txt"
with open(out_file, "w", encoding="utf-8") as out:
    for idx, d in enumerate(both):
        out.write(f"Pair #{idx+1} [Post {d['id']}] - Date: {d['date']}\n")
        out.write(f"Extracted Price: ${d['price']}\n")
        out.write(f"Caption: {d['caption'][:150]}\n")
        out.write(f"Video (first): {d['videos'][0] if d['videos'] else 'None'}\n")
        out.write(f"Photos ({len(d['photos'])}): {', '.join(d['photos'][:4])}\n")
        out.write("-" * 50 + "\n")

print(f"Curated {len(both)} pairs written to {out_file}")
