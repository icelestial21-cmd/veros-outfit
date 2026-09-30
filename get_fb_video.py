import re
import requests

reel_file = r'C:\Users\User\.gemini\antigravity\brain\d332ca20-6bb7-49ba-b279-4e688f0f923a\.system_generated\steps\4017\content.md'
with open(reel_file, 'r', encoding='utf-8') as f:
    text = f.read()

urls = re.findall(r'https://video[^\s"\'\\]+', text) or re.findall(r'https://[^\s"\'\\]+\.mp4[^\s"\'\\]*', text)
print("Video URLs found:", len(urls))
for u in set(urls)[:3]:
    clean_u = u.replace('\\/', '/').replace('&amp;', '&')
    print("Found video:", clean_u[:120])
    try:
        r = requests.get(clean_u, stream=True, headers={'User-Agent': 'Mozilla/5.0'})
        with open('web/test_artifacts/gismat_reel_clip.mp4', 'wb') as f_out:
            for chunk in r.iter_content(chunk_size=1024*1024):
                f_out.write(chunk)
                if f_out.tell() > 5*1024*1024:
                    break
        print("Downloaded video clip:", f_out.tell())
        break
    except Exception as e:
        print("Download error:", e)
