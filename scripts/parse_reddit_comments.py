import re
from bs4 import BeautifulSoup

with open(r'C:\Users\User\.gemini\antigravity\brain\924eb293-9091-47f4-90d1-fb5fb8ea23ab\.system_generated\steps\17035\content.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Search for paragraph text or comments
soup = BeautifulSoup(text, 'html.parser')
paragraphs = [p.get_text().strip() for p in soup.find_all(['p', 'div']) if len(p.get_text().strip()) > 30]

print("Found paragraphs in Reddit thread:")
for p in paragraphs[:25]:
    if any(k in p.lower() for k in ['marko', 'baku', 'shop', 'legit', 'scam', 'store', 'bought', 'clothes', 'boutique']):
        print("  ->", p)
