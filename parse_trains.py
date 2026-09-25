import re
import urllib.request
import json
import time

with open("hakata_raw.html", "r", encoding="utf-8") as f:
    text = f.read()

# Locate the table for "鹿児島本線 久留米・大牟田方面（下り）"
idx = text.find("鹿児島本線 久留米・大牟田方面（下り）")
# Find end of this table
end_idx = text.find("</TABLE>", idx)
table_html = text[idx:end_idx]

# Pattern to find each hour row
# <tr> <TH ...> <DIV ...> <FONT COLOR="#FFFFFF">5</FONT> </DIV> </TH> <!-- 特急・急行 --> <td>...</td> <!-- 特急・急行以外の列車 --> <td>...</td> </tr>
hour_rows = re.findall(r'<TH[^>]*>.*?<FONT COLOR="#FFFFFF">(\d+)</FONT>.*?<!-- 特急・急行以外の列車 -->(.*?)</tr>', table_html, re.DOTALL)

trains = []
for hour, non_ltd_html in hour_rows:
    hour = int(hour)
    # inside non_ltd_html, find each td cell
    cells = re.findall(r'<td class=back\d valign="bottom" align="center" nowrap>(.*?)</td>', non_ltd_html, re.DOTALL)
    for c in cells:
        # extract minute & href
        m_link = re.search(r'<a href="([^"]+)"[^>]*><b>(\d+)</b></a>', c)
        if not m_link:
            continue
        href, minute = m_link.group(1), int(m_link.group(2))
        # extract destination
        # destination is usually right after </font><br> ...
        # let's clean text
        lines = [line.strip() for line in re.sub(r'<[^>]+>', '\n', c).split('\n') if line.strip()]
        # lines might be ['13', '大牟田'] or ['20', '荒尾', '南福岡～大牟田間快速']
        dest = lines[1] if len(lines) > 1 else ""
        type_info = " ".join(lines[2:]) if len(lines) > 2 else "普通"
        trains.append({
            "hour": hour,
            "minute": minute,
            "dep_time": f"{hour:02d}:{minute:02d}",
            "dest": dest,
            "type_info": type_info,
            "url": "https://www.jrkyushu-timetable.jp" + href
        })

print(f"Found {len(trains)} non-express trains on weekday:")
for t in trains[:15]:
    print(f"  {t['dep_time']} -> {t['dest']} ({t['type_info']}) : {t['url']}")

with open("weekday_trains.json", "w", encoding="utf-8") as f:
    json.dump(trains, f, ensure_ascii=False, indent=2)
