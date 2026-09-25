import json

with open("processed_journeys.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open("detailed_hakata.json", "r", encoding="utf-8") as f:
    d_hakata = json.load(f)

# Stations between Hakata and Kurume
all_stations = [
    "博多", "竹下", "笹原", "南福岡", "春日", "大野城", "水城", "都府楼南", 
    "二日市", "天拝山", "原田", "けやき台", "基山", "弥生が丘", "田代", "鳥栖", 
    "肥前旭", "久留米"
]

enriched_journeys = []

for j in data["weekday"]:
    url = None
    # find train url in d_hakata
    for u, info in d_hakata.items():
        if info.get("hakata", {}).get("dep") == j["hakata_dep"] and info.get("train_no") in j["train_no"]:
            url = u
            break
    
    stops = []
    if url:
        info = d_hakata[url]
        # find stops between Hakata and Tosu/Kurume
        for s in info.get("stops", []):
            st = s["station"]
            if st in all_stations and not s.get("pass", False):
                stops.append(st)
    
    # Determine type
    raw_type = j["type_text"].replace("&nbsp;", "").strip()
    
    # Analyze rapid section
    type_category = "普通"
    type_badge = "普通"
    note = ""
    
    if "快速" in raw_type:
        if "区間快速" in raw_type or "から各駅停車" in raw_type or "まで各駅停車" in raw_type or "間快速" in raw_type:
            type_category = "区間快速"
            type_badge = "区間快速"
            # Extract note
            note = raw_type
        else:
            type_category = "快速"
            type_badge = "快速"
    elif "二日市から各駅停車" in raw_type:
        type_category = "区間快速"
        type_badge = "区間快速"
        note = "二日市から各駅停車"
    elif "鳥栖から各駅停車" in raw_type:
        type_category = "区間快速"
        type_badge = "区間快速"
        note = "鳥栖から各駅停車"
    elif "南福岡まで各駅停車" in raw_type:
        type_category = "区間快速"
        type_badge = "区間快速"
        note = "南福岡まで各駅停車"
    elif len(stops) < 14 and not j["is_transfer"]:
        type_category = "快速"
        type_badge = "快速"
    
    # If transfer
    if j["is_transfer"]:
        # parse transfer info
        # e.g. "鳥栖乗換 (鳥栖発 大牟田行)"
        transfer_desc = j["transfer_info"]
        if "二日市から各駅停車" in raw_type:
            type_badge = "区間快速"
            note = "博多〜二日市間快速／鳥栖で乗換"
        else:
            type_badge = "普通"
            note = "鳥栖で乗換"
    else:
        transfer_desc = "直通"
        if not note and type_category == "快速":
            note = f"{j['dest']}行"
        elif not note:
            note = f"{j['dest']}行"
    
    # Calculate travel time
    travel_time = j["kurume_arr_min"] - j["hakata_dep_min"]
    
    enriched_journeys.append({
        "no": len(enriched_journeys) + 1,
        "origin": j["origin"],
        "dest": j["dest"],
        "hakata_dep": j["hakata_dep"],
        "tosu_arr": j["tosu_arr"],
        "tosu_dep": j["tosu_dep"],
        "kurume_arr": j["kurume_arr"],
        "travel_time": travel_time,
        "is_transfer": j["is_transfer"],
        "transfer_info": transfer_desc,
        "type_category": type_category,
        "type_badge": type_badge,
        "note": note,
        "days": "毎日運転" # All validated trains operate daily
    })

with open("enriched_timetable.json", "w", encoding="utf-8") as f:
    json.dump(enriched_journeys, f, ensure_ascii=False, indent=2)

print(f"Enriched {len(enriched_journeys)} trains!")
for ej in enriched_journeys[:10]:
    print(f"{ej['no']:2d} | 始発:{ej['origin']:4s} | 博多:{ej['hakata_dep']} -> 鳥栖:{ej['tosu_arr']}/{ej['tosu_dep']} -> 久留米:{ej['kurume_arr']} ({ej['travel_time']}分) | [{ej['type_badge']}] {ej['note']} ({ej['transfer_info']})")
