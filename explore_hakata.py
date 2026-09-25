import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "https://www.jrkyushu-timetable.jp/cgi-bin/jr-k_time/tt_dep.cgi?c=28283"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=10) as resp:
    content = resp.read()
    for enc in ['cp932', 'euc-jp', 'utf-8']:
        try:
            txt = content.decode(enc)
            print(f"Decoded with {enc} successfully, length {len(txt)}")
            # look for links
            for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', txt, re.DOTALL):
                clean = re.sub(r'<[^>]+>', '', m.group(2)).strip()
                print(f"  {clean} -> {m.group(1)}")
            break
        except UnicodeDecodeError:
            pass
