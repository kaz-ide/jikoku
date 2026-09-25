import urllib.request
import urllib.parse
import re
import json

def fetch_tosu(date_val):
    url = "https://www.jrkyushu-timetable.jp/cgi-bin/jr-k_time/tt_dep.cgi"
    data = urllib.parse.urlencode({
        'c': '28399',
        'year_month': '202609',
        'date': date_val,
        'disp_tt': '表示'
    }).encode('cp932')
    req = urllib.request.Request(url, data=data, headers={"User-Agent": "Mozilla/5.0"})
    content = urllib.request.urlopen(req, timeout=10).read()
    text = content.decode('utf-8', errors='replace')
    
    # save raw
    with open(f"tosu_{date_val}_raw.html", "w", encoding="utf-8") as f:
        f.write(text)
    
    # find lines
    # look for "久留米・大牟田方面"
    idx = text.find("久留米・大牟田")
    if idx == -1:
        idx = text.find("鹿児島本線")
    print(f"Date {date_val}: idx={idx}")
    
    # find next table
    end_idx = text.find("<caption", idx + 100)
    if end_idx == -1:
        end_idx = text.find("</TABLE>", idx + 500)
    section = text[idx:idx+40000]
    
    # find hour rows
    hour_rows = re.findall(r'<TH[^>]*>.*?<FONT COLOR="#FFFFFF">(\d+)</FONT>.*?<!-- 特急・急行以外の列車 -->(.*?)</tr>', section, re.DOTALL)
    print(f"Date {date_val}: hour rows found = {len(hour_rows)}")
    trains = []
    for hour, non_ltd in hour_rows:
        hour = int(hour)
        cells = re.findall(r'<td class=back\d valign="bottom" align="center" nowrap>(.*?)</td>', non_ltd, re.DOTALL)
        for c in cells:
            m_link = re.search(r'<a href="([^"]+)"[^>]*><b>(\d+)</b></a>', c)
            if not m_link:
                continue
            href, minute = m_link.group(1), int(m_link.group(2))
            clean_lines = [l.strip() for l in re.sub(r'<[^>]+>', '\n', c).splitlines() if l.strip()]
            dest = clean_lines[1] if len(clean_lines) > 1 else ""
            type_text = " ".join(clean_lines[2:]) if len(clean_lines) > 2 else "普通"
            trains.append({
                "hour": hour,
                "minute": minute,
                "dep_time": f"{hour:02d}:{minute:02d}",
                "dest": dest,
                "type_text": type_text,
                "href": href
            })
    return trains

tosu_w = fetch_tosu('25')
tosu_h = fetch_tosu('27')

print(f"Tosu weekday: {len(tosu_w)}, holiday: {len(tosu_h)}")
with open("tosu_trains.json", "w", encoding="utf-8") as f:
    json.dump({"weekday": tosu_w, "holiday": tosu_h}, f, ensure_ascii=False, indent=2)
