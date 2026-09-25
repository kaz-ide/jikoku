import urllib.request
import urllib.parse
import re
import json
import time

def fetch_hakata_trains(date_val):
    # date_val: '25' for Friday (weekday), '27' for Sunday (holiday)
    url = "https://www.jrkyushu-timetable.jp/cgi-bin/jr-k_time/tt_dep.cgi"
    data = urllib.parse.urlencode({
        'c': '28283',
        'year_month': '202609',
        'date': date_val,
        'disp_tt': '表示'
    }).encode('cp932')
    req = urllib.request.Request(url, data=data, headers={"User-Agent": "Mozilla/5.0"})
    content = urllib.request.urlopen(req, timeout=10).read()
    text = content.decode('utf-8', errors='replace')
    
    start_title = text.find("鹿児島本線 久留米・大牟田方面（下り）")
    next_title = text.find("篠栗線 長者原・桂川・直方・折尾方面（上り）")
    section = text[start_title:next_title]
    
    hour_rows = re.findall(r'<TH[^>]*>.*?<FONT COLOR="#FFFFFF">(\d+)</FONT>.*?<!-- 特急・急行以外の列車 -->(.*?)</tr>', section, re.DOTALL)
    
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
                "day_type": "weekday" if date_val == '25' else "holiday",
                "hour": hour,
                "minute": minute,
                "dep_time": f"{hour:02d}:{minute:02d}",
                "dest": dest,
                "type_text": type_text,
                "href": href
            })
    return trains

weekday_trains = fetch_hakata_trains('25')
holiday_trains = fetch_hakata_trains('27')

print(f"Weekday trains: {len(weekday_trains)}, Holiday trains: {len(holiday_trains)}")
with open("hakata_train_list.json", "w", encoding="utf-8") as f:
    json.dump({"weekday": weekday_trains, "holiday": holiday_trains}, f, ensure_ascii=False, indent=2)
