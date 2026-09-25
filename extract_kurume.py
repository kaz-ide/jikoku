import re

with open("hakata_raw.html", "r", encoding="utf-8") as f:
    text = f.read()

# Find the section around "鹿児島本線 久留米・大牟田方面（下り）"
idx = text.find("鹿児島本線 久留米・大牟田方面（下り）")
if idx != -1:
    snippet = text[idx-200:idx+2500]
    with open("kurume_section.html", "w", encoding="utf-8") as out:
        out.write(snippet)
    print("Found section and saved to kurume_section.html")
else:
    print("Not found")
