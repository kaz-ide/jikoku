import urllib.request
import re

url = "https://www.jrkyushu-timetable.jp/jr-k_time/top.html"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=10) as resp:
    content = resp.read()
    # Check meta charset
    m = re.search(b'charset=["\']?([a-zA-Z0-9_-]+)', content)
    print("Charset:", m.group(1) if m else "unknown")
    text = content.decode('utf-8', errors='replace')
    links = re.findall(r'href="([^"]+)"', text)
    print("Total links:", len(links))
    for l in links[:30]:
        print(l)
