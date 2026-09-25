import re

with open("hakata_sunday.html", "r", encoding="utf-8") as f:
    text = f.read()

start_title = text.find("鹿児島本線 久留米・大牟田方面（下り）")
next_title = text.find("篠栗線 長者原・桂川・直方・折尾方面（上り）")
section = text[start_title:next_title]

hour_rows = re.findall(r'<TH[^>]*>.*?<FONT COLOR="#FFFFFF">(\d+)</FONT>.*?<!-- 特急・急行以外の列車 -->(.*?)</tr>', section, re.DOTALL)
print("Sunday Hour count:", len(hour_rows))

for hour, non_ltd in hour_rows:
    links = re.findall(r'<a href="([^"]+)"[^>]*><b>(\d+)</b></a>', non_ltd)
    print(f"Sunday Hour {hour}: {len(links)} trains -> {[m[1] for m in links]}")
