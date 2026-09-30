import re

html_path = r"C:\Users\User\Downloads\Telegram Desktop\ChatExport_2026-09-26\messages.html"
with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

srv = re.findall(r'<div class="message service" id="([^"]+)">([\s\S]*?)</div>\s*</div>', html)
print(f"Total service messages: {len(srv)}")
for mid, content in srv[:10]:
    clean = re.sub(r'<[^>]+>', ' ', content).strip()
    clean = re.sub(r'\s+', ' ', clean)
    print(f"[{mid}] {clean}")
