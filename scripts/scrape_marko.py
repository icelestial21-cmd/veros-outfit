import urllib.request
import re
import json

url = 'https://www.instagram.com/marko.global/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        print(f"Total HTML length: {len(html)}")
        
        # Meta tags
        for m in re.findall(r'<meta\s+[^>]+>', html):
            if any(k in m.lower() for k in ['description', 'title', 'og:', 'al:']):
                print(m)
                
        # Look for bio or shared data
        match = re.search(r'\"biography\":\"([^\"]+)\"', html)
        if match:
            print("Biography:", match.group(1).encode('utf-8').decode('unicode_escape'))
        
        # External URL
        match_url = re.search(r'\"external_url\":\"([^\"]+)\"', html)
        if match_url:
            print("External URL:", match_url.group(1).encode('utf-8').decode('unicode_escape'))
            
        # Category
        match_cat = re.search(r'\"category_name\":\"([^\"]+)\"', html)
        if match_cat:
            print("Category:", match_cat.group(1))
            
except Exception as e:
    print(f"Error: {e}")
