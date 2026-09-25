import re

with open("hakata_raw.html", "r", encoding="utf-8") as f:
    text = f.read()

# Let's find the exact table boundary
start_title = text.find("鹿児島本線 久留米・大牟田方面（下り）")
next_title = text.find("篠栗線 長者原・桂川・直方・折尾方面（上り）")

print("Start:", start_title, "Next:", next_title)
section = text[start_title:next_title]
print("Section length:", len(section))

# Find hour rows in this section only
hour_rows = re.findall(r'<TH[^>]*>.*?<FONT COLOR="#FFFFFF">(\d+)</FONT>.*?<!-- 特急・急行以外の列車 -->(.*?)</tr>', section, re.DOTALL)
print("Hour count:", len(hour_rows))

for hour, non_ltd in hour_rows:
    links = re.findall(r'<a href="([^"]+)"[^>]*><b>(\d+)</b></a>', non_ltd)
    print(f"Hour {hour}: {len(links)} trains -> {[m[1] for m in links]}")
