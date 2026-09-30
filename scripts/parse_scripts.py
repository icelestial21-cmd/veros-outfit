import re
import json

with open(r'C:\Users\User\.gemini\antigravity\scratch\marko_page.html', 'r', encoding='utf-8') as f:
    text = f.read()

scripts = re.findall(r'<script type="application/json"[^>]*>(.*?)</script>', text, re.DOTALL)
print(f"Found {len(scripts)} json scripts.")

for i, s in enumerate(scripts):
    if 'marko' in s.lower() or 'baku' in s.lower():
        print(f"Script {i} contains marko/baku, length: {len(s)}")
        matches = re.findall(r'.{0,60}(?:marko|baku|follower|following|biography|geyiml|zahid).{0,60}', s, re.IGNORECASE)
        for m in matches[:10]:
            print(f"   -> {m}")
