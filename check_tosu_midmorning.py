import json

with open("tosu_trains.json", "r", encoding="utf-8") as f:
    t_data = json.load(f)

with open("detailed_tosu.json", "r", encoding="utf-8") as f:
    d_tosu = json.load(f)

print("--- Tosu departures 09:30 - 10:30 ---")
for t in t_data["weekday"]:
    if t["hour"] in [9, 10]:
        url = "https://www.jrkyushu-timetable.jp" + t["href"]
        info = d_tosu.get(url, {})
        kurume = info.get("kurume")
        tosu = info.get("tosu")
        dest = info.get("dest")
        origin = info.get("origin")
        print(f"Tosu {t['dep_time']} -> {dest} (始発:{origin}) | Kurume arr: {kurume.get('arr') if kurume else 'None'}")
