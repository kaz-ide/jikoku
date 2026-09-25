import urllib.request
import re

url = "https://www.jrkyushu-timetable.jp/jr-k_time/top.html"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        content = resp.read()
        html = content.decode('shift_jis', errors='ignore')
        print("Page length:", len(html))
        # find hakata
        matches = re.findall(r'href="([^"]+)"[^>]*>([^<]*博多[^<]*)<', html)
        print("Matches:", matches)
        # find all links to timetables
        all_links = [m.group(1) for m in re.finditer(r'href="([^"]+)"', html)]
        hakata_links = [l for l in all_links if "28" in l or "haka" in l.lower()]
        print("Hakata related links:", hakata_links[:10])
except Exception as e:
    print("Error:", e)
