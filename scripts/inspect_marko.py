import urllib.request
import re
import json

url = 'https://www.instagram.com/marko.global/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

with open(r'C:\Users\User\.gemini\antigravity\scratch\marko_page.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved HTML. Searching for key phrases...")
for line in html.split('\n'):
    if any(k in line.lower() for k in ['og:description', 'og:title', 'biography', 'followers', 'baku', 'whatsapp', 'wa.me', 'kişi']):
        print("Line:", line[:250])
