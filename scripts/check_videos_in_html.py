import os
import re

html_path = r"C:\Users\User\Downloads\Telegram Desktop\ChatExport_2026-09-26\messages.html"
with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

v_matches = re.findall(r'video_files/[^"\'\s<>]+', html, re.IGNORECASE)
print(f"Total video_files references in HTML: {len(v_matches)}")
if v_matches:
    print("Sample:", v_matches[:10])

# Search for any <video> tag or media div
video_tags = re.findall(r'<video[\s\S]*?</video>', html, re.IGNORECASE)
print(f"Total <video> tags: {len(video_tags)}")

# Search for media_video
media_v = re.findall(r'class="[^"]*video[^"]*"', html, re.IGNORECASE)
print(f"Total video classes: {len(media_v)}")
if media_v:
    print("Sample classes:", list(set(media_v))[:10])

# Check for links to video_files
a_tags = re.findall(r'<a[^>]+href="([^"]*video_files[^"]*)"[^>]*>', html, re.IGNORECASE)
print(f"Total <a> tags linking to video_files: {len(a_tags)}")
if a_tags:
    print("Sample <a> hrefs:", a_tags[:5])
