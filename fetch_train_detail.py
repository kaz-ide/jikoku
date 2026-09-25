import urllib.request
import re

url = "https://www.jrkyushu-timetable.jp/jr-k_time/2610/0001/00011001.html?c=28283&ym=202609&d=25"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
content = urllib.request.urlopen(req, timeout=10).read()
text = content.decode('utf-8', errors='replace')
with open("train_detail_sample.html", "w", encoding="utf-8") as f:
    f.write(text)
print("Saved train detail, length:", len(text))

# Let's see what's inside
lines = [re.sub(r'<[^>]+>', '', l).strip() for l in text.splitlines() if re.sub(r'<[^>]+>', '', l).strip()]
for l in lines[:40]:
    print(l)
