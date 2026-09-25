import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "https://www.jrkyushu-timetable.jp/cgi-bin/jr-k_time/tt_dep.cgi?c=28283"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=10) as resp:
    content = resp.read()
    txt = content.decode('shift_jis', errors='replace')
    print("Page length:", len(txt))
    # print headers, table titles
    for m in re.finditer(r'<h[1-6][^>]*>(.*?)</h[1-6]>', txt, re.DOTALL):
        print("H:", re.sub(r'<[^>]+>', '', m.group(1)).strip())
    # find lines/directions
    for m in re.finditer(r'<select[^>]*name="line"[^>]*>(.*?)</select>', txt, re.DOTALL):
        print("Lines:", m.group(1))
    for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', txt, re.DOTALL):
        href = m.group(1)
        text = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        if any(w in text for w in ['鹿児島本線', '久留米', '大牟田', '鳥栖', '普通', '快速', '下り', '平日', '土曜']):
            print(f"Match: {text} -> {href}")
