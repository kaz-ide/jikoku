import urllib.request
import re

def check(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        text = resp.read().decode('cp932', errors='replace')
        for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', text, re.DOTALL):
            link, name = m.group(1), m.group(2)
            clean = re.sub(r'<[^>]+>', '', name).strip()
            if any(s in clean for s in ['博多', '鳥栖', '久留米', '二日市']):
                print(f"{clean}: {link}")

print("--- Fukuoka ---")
check("https://www.jrkyushu-timetable.jp/jr-k_time/ken_hukuoka.html")
print("--- Saga ---")
check("https://www.jrkyushu-timetable.jp/jr-k_time/ken_saga.html")
