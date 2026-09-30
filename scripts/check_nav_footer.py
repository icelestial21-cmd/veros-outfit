import re
import os

web_dir = r"C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\web"
pages = ['index.html', 'collections.html', 'lookbook.html', 'product.html']

for page in pages:
    fp = os.path.join(web_dir, page)
    with open(fp, 'r', encoding='utf-8') as f:
        html = f.read()

    print(f"\n=================== {page} ===================")
    nav_match = re.search(r'<nav\b[^>]*>([\s\S]*?)</nav>', html)
    if nav_match:
        links = re.findall(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>([\s\S]*?)</a>', nav_match.group(1))
        print("Header Nav Links:")
        for h, text in links:
            clean = re.sub(r'<[^>]+>', '', text).strip()
            print(f"  - [{clean}] -> {h}")
    else:
        print("NO NAV FOUND")

    footer_match = re.search(r'<footer\b[^>]*>([\s\S]*?)</footer>', html)
    if footer_match:
        print("\nFooter snippet (first 300 chars):")
        print(footer_match.group(1)[:300].strip())
    else:
        print("NO FOOTER FOUND")
