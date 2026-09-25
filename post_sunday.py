import urllib.request
import urllib.parse
import re

url = "https://www.jrkyushu-timetable.jp/cgi-bin/jr-k_time/tt_dep.cgi"
data = urllib.parse.urlencode({
    'c': '28283',
    'year_month': '202609',
    'date': '27',
    'disp_tt': '表示'
}).encode('cp932')

req = urllib.request.Request(url, data=data, headers={"User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        content = resp.read()
        print("POST Sunday length:", len(content))
        with open("hakata_sunday_post.html", "wb") as f:
            f.write(content)
except Exception as e:
    print("Error:", e)
