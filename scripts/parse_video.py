import re

with open(r'C:\Users\User\.gemini\antigravity\brain\924eb293-9091-47f4-90d1-fb5fb8ea23ab\.system_generated\steps\17019\content.md', 'r', encoding='utf-8') as f:
    text = f.read()

matches = re.findall(r'"title":"([^"]+)"', text)
print("Titles found:", matches[:5])
author = re.findall(r'"author":"([^"]+)"', text)
print("Author:", author[:5])
short_desc = re.findall(r'"shortDescription":"([^"]+)"', text)
print("Short desc:", [s[:200] for s in short_desc[:3]])
