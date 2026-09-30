import sys
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.texts = []
        self.in_script = False
        
    def handle_starttag(self, tag, attrs):
        if tag in ['script', 'style']:
            self.in_script = True
            
    def handle_endtag(self, tag):
        if tag in ['script', 'style']:
            self.in_script = False
            
    def handle_data(self, data):
        if not self.in_script:
            d = data.strip()
            if len(d) > 10:
                self.texts.append(d)

with open(r'C:\Users\User\.gemini\antigravity\brain\924eb293-9091-47f4-90d1-fb5fb8ea23ab\.system_generated\steps\17035\content.md', 'r', encoding='utf-8') as f:
    text = f.read()

parser = TextExtractor()
parser.feed(text)

with open(r'C:\Users\User\.gemini\antigravity\scratch\reddit_extracted.txt', 'w', encoding='utf-8') as out:
    for t in parser.texts:
        out.write(t + "\n")

print(f"Extracted {len(parser.texts)} blocks to reddit_extracted.txt")
