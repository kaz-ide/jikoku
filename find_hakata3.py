import urllib.request
import re

url = "https://www.jrkyushu-timetable.jp/jr-k_time/ken_hukuoka.html"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=10) as resp:
    data = resp.read()
    text = data.decode('utf-8', errors='ignore')
    for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', text, re.DOTALL):
        link, name = m.group(1), m.group(2)
        clean = re.sub(r'<[^>]+>', '', name).strip()
        if any(s in clean for s in ['博多', '鳥栖', '久留米', '二日市']):
            print(f"{clean}: {link}")
