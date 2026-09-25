import urllib.request
import re

url = "https://www.jrkyushu-timetable.jp/jr-k_time/ken_saga.html"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
content = urllib.request.urlopen(req, timeout=10).read()
text = content.decode('utf-8', errors='replace')
for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', text, re.DOTALL):
    clean = re.sub(r'<[^>]+>', '', m.group(2)).strip()
    link = m.group(1)
    if "鳥栖" in clean:
        print(f"Saga: {clean} -> {link}")
