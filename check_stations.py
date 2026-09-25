import urllib.request
import re

codes = ['28283', '8291', '28144', '28626', '29394', '29007', '28155', '28389', '28533', '28742', '28903']
for c in codes:
    url = f"https://www.jrkyushu-timetable.jp/cgi-bin/jr-k_time/tt_dep.cgi?c={c}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            text = resp.read().decode('utf-8', errors='ignore')
            title = re.search(r'<title>([^<]+)</title>', text)
            print(f"{c}: {title.group(1) if title else 'no title'}")
    except Exception as e:
        print(f"{c}: Error {e}")
