import urllib.request

url = "https://www.jrkyushu-timetable.jp/cgi-bin/jr-k_time/tt_dep.cgi?c=28283"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
content = urllib.request.urlopen(req, timeout=10).read()
with open("hakata_raw.html", "wb") as f:
    f.write(content)
print("Saved raw HTML, size:", len(content))

for enc in ["utf-8", "euc-jp", "cp932", "iso-2022-jp"]:
    try:
        t = content.decode(enc)
        print(f"Decoded with {enc} cleanly!")
    except Exception as e:
        print(f"Failed {enc}: {e}")
