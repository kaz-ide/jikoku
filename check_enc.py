with open("hakata_raw.html", "rb") as f:
    raw = f.read()

import re
m = re.search(b'charset=["\']?([a-zA-Z0-9_-]+)', raw)
if m:
    print("Meta charset in bytes:", m.group(1))

# Check title in hex
pos = raw.find(b'<title>')
if pos != -1:
    print("Title raw bytes:", raw[pos:pos+50])
    for enc in ['shift_jis', 'cp932', 'euc-jp', 'utf-8']:
        try:
            print(f"{enc}:", raw[pos:pos+50].decode(enc))
        except Exception as e:
            print(f"{enc} failed:", e)
