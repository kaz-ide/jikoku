import urllib.request
import re

url = "https://www.jrkyushu-timetable.jp/"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        content = resp.read()
        print("Success, length:", len(content))
        html = content.decode('cp932', errors='ignore')
        for match in re.finditer(r'href="([^"]+)"', html):
            link = match.group(1)
            if "jr" in link or "time" in link or "eki" in link:
                print("Link:", link)
except Exception as e:
    print("Error:", e)
