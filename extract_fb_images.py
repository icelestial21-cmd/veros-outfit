import re
import requests

with open('fb_dump.html', 'r', encoding='utf-8') as f:
    text = f.read()

urls = re.findall(r'https://scontent[^\s"\'\\]+', text)
print(f"Total scontent URLs: {len(urls)}")

# Filter for profile pictures or distinct images
valid_urls = []
for u in set(urls):
    u_clean = u.replace('\\/', '/').replace('&amp;', '&')
    if any(x in u_clean for x in ['p320x320', 'p526x296', 's100x100', 's320x320', 't51.82787', 't39.30808']):
        valid_urls.append(u_clean)

print(f"Candidate images: {len(valid_urls)}")
for idx, u in enumerate(valid_urls[:5]):
    try:
        r = requests.get(u, headers={'User-Agent': 'Mozilla/5.0'})
        filename = f'web/test_artifacts/fb_img_{idx}.jpg'
        with open(filename, 'wb') as img_f:
            img_f.write(r.content)
        print(f"Saved {filename} ({len(r.content)} bytes) from {u[:80]}")
    except Exception as e:
        print(f"Failed {idx}: {e}")
