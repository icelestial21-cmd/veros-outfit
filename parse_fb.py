import re

with open('fb_dump.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Search for work, education, bio, or links
keywords = ['marko', 'baku', 'director', 'founder', 'owner', 'ceo', 'wear', 'global', 'salayev', 'qismət', 'gismat']
for kw in keywords:
    matches = re.findall(rf'[^.!?\n]{{0,50}}{kw}[^.!?\n]{{0,50}}', text, re.IGNORECASE)
    if matches:
        print(f"=== Keyword: {kw} ({len(matches)} matches) ===")
        for m in list(set(matches))[:10]:
            print("  *", m.strip())
