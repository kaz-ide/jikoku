import urllib.request

url_sun = "https://www.jrkyushu-timetable.jp/cgi-bin/jr-k_time/tt_dep.cgi?c=28283&ym=202609&d=27"
req = urllib.request.Request(url_sun, headers={"User-Agent": "Mozilla/5.0"})
content = urllib.request.urlopen(req, timeout=10).read()
with open("hakata_sunday.html", "wb") as f:
    f.write(content)
print("Saved Sunday HTML, size:", len(content))
