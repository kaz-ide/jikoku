import json

with open("hakata_train_list.json", "r", encoding="utf-8") as f:
    h_data = json.load(f)

with open("detailed_hakata.json", "r", encoding="utf-8") as f:
    d_hakata = json.load(f)

print("--- Hakata 7:00 - 8:59 trains ---")
for t in h_data["weekday"]:
    if t["hour"] in [7, 8]:
        url = "https://www.jrkyushu-timetable.jp" + t["href"]
        info = d_hakata.get(url, {})
        kurume = info.get("kurume")
        tosu = info.get("tosu")
        dest = info.get("dest")
        origin = info.get("origin")
        print(f"Hakata {t['dep_time']} -> {dest} (始発:{origin}) | Tosu: {tosu} | Kurume: {kurume}")
