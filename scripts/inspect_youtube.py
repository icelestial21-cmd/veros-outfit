import re
import json

with open(r'C:\Users\User\.gemini\antigravity\brain\924eb293-9091-47f4-90d1-fb5fb8ea23ab\.system_generated\steps\16990\content.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Find all links in the YouTube page
links = set(re.findall(r'https?://[^\s\"\'<>]+', text))
print("Links found in YouTube channel:")
for l in sorted(links):
    if any(k in l.lower() for k in ['instagram', 'facebook', 'tiktok', 'wa.me', 'whatsapp', 't.me', 'marko']):
        print("  ->", l)

# Search for video titles or text snippets
titles = re.findall(r'"title":\{"runs":\[\{"text":"(.*?)"\}\]', text)
print("\nVideo / Section Titles:")
for t in set(titles):
    print("  ->", t)

# Search for channel description or about text
about = re.findall(r'"description":\{"simpleText":"(.*?)"\}', text)
print("\nAbout text:")
for a in set(about):
    print("  ->", a)
