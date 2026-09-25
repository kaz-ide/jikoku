import re

with open("train_detail_sample.html", "r", encoding="utf-8") as f:
    text = f.read()

def parse_train_detail_html(text):
    # Train number
    m_no = re.search(r'列車番号</td>\s*<td[^>]*>\s*([A-Za-z0-9]+)', text)
    train_no = m_no.group(1).strip() if m_no else ""
    
    # Days operated
    m_days = re.search(r'運転日</td>\s*<td[^>]*>\s*([^<]+)', text)
    days = m_days.group(1).strip() if m_days else ""
    
    # Remarks
    m_rem = re.search(r'備考</td>\s*<td[^>]*>\s*([^<]+)', text)
    remarks = m_rem.group(1).strip() if m_rem else ""
    
    # Station stops
    # Stations are in table rows:
    # <tr> <!-- 駅名 --> <td ...> <a ...>駅名</a> </td> <!-- 時刻 --> <td ...> XX:XX 着<br>XX:XX 発 </td> ...
    station_rows = re.findall(r'<!-- 駅名 -->\s*<td[^>]*>\s*<a[^>]*>([^<]+)</a>\s*</td>\s*<!-- 時刻 -->\s*<td[^>]*>(.*?)</td>', text, re.DOTALL)
    
    stops = []
    for st_name, time_td in station_rows:
        st_name = st_name.strip()
        # parse arrival and departure
        # might be: "<br>05:13 発" or "05:20 着<br>05:21 発" or "06:12 着<br>" or "レ" (pass)
        clean_time = re.sub(r'<[^>]+>', ' ', time_td).strip()
        arr_m = re.search(r'(\d{2}:\d{2})\s*着', clean_time)
        dep_m = re.search(r'(\d{2}:\d{2})\s*発', clean_time)
        arr = arr_m.group(1) if arr_m else None
        dep = dep_m.group(1) if dep_m else None
        is_pass = "レ" in clean_time or "通過" in clean_time
        stops.append({
            "station": st_name,
            "arr": arr,
            "dep": dep,
            "pass": is_pass
        })
    
    origin = stops[0]["station"] if stops else ""
    origin_dep = stops[0]["dep"] if stops else ""
    dest = stops[-1]["station"] if stops else ""
    dest_arr = stops[-1]["arr"] if stops else ""
    
    # Find Hakata, Tosu, Kurume
    hakata = next((s for s in stops if s["station"] == "博多"), None)
    tosu = next((s for s in stops if s["station"] == "鳥栖"), None)
    kurume = next((s for s in stops if s["station"] == "久留米"), None)
    
    return {
        "train_no": train_no,
        "days": days,
        "remarks": remarks,
        "origin": origin,
        "origin_dep": origin_dep,
        "dest": dest,
        "dest_arr": dest_arr,
        "hakata": hakata,
        "tosu": tosu,
        "kurume": kurume,
        "all_stops_count": len(stops)
    }

res = parse_train_detail_html(text)
import pprint
pprint.pprint(res)
