import re

def check_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    title = re.search(r'<meta property="og:title" content="(.*?)"', text)
    desc = re.search(r'<meta property="og:description" content="(.*?)"', text)
    title_tag = re.search(r'<title>(.*?)</title>', text)
    print("Path:", path)
    print("Title tag:", title_tag.group(1) if title_tag else "None")
    print("OG Title:", title.group(1) if title else "None")
    print("OG Desc:", desc.group(1) if desc else "None")

check_file(r'C:\Users\User\.gemini\antigravity\brain\924eb293-9091-47f4-90d1-fb5fb8ea23ab\.system_generated\steps\17005\content.md')
check_file(r'C:\Users\User\.gemini\antigravity\brain\924eb293-9091-47f4-90d1-fb5fb8ea23ab\.system_generated\steps\16990\content.md')
