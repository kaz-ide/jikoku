import json
import re

with open("hakata_train_list.json", "r", encoding="utf-8") as f:
    h_data = json.load(f)

with open("detailed_hakata.json", "r", encoding="utf-8") as f:
    d_hakata = json.load(f)

with open("tosu_trains.json", "r", encoding="utf-8") as f:
    t_data = json.load(f)

with open("detailed_tosu.json", "r", encoding="utf-8") as f:
    d_tosu = json.load(f)

def time_to_min(t_str):
    if not t_str or ":" not in t_str:
        return 9999
    h, m = map(int, t_str.split(":"))
    # handle past midnight (e.g. 00:xx)
    if h < 4:
        h += 24
    return h * 60 + m

def min_to_time(m_val):
    if m_val >= 9999:
        return ""
    h = (m_val // 60) % 24
    m = m_val % 60
    return f"{h:02d}:{m:02d}"

def analyze_schedule(day_key):
    # day_key: 'weekday' or 'holiday'
    # Hakata departures
    h_trains = h_data[day_key]
    
    # Collect all Tosu departures towards Kurume for this day
    # Tosu trains that stop at Kurume
    tosu_kurume_trains = []
    for t in t_data[day_key]:
        url = "https://www.jrkyushu-timetable.jp" + t["href"]
        info = d_tosu.get(url)
        if not info:
            continue
        # check if it stops at Kurume
        kurume = info.get("kurume")
        tosu = info.get("tosu")
        if tosu and kurume and not kurume.get("pass", False):
            tosu_dep = tosu.get("dep")
            kurume_arr = kurume.get("arr")
            if tosu_dep and kurume_arr:
                tosu_kurume_trains.append({
                    "url": url,
                    "train_no": info["train_no"],
                    "origin": info["origin"],
                    "dest": info["dest"],
                    "tosu_dep": tosu_dep,
                    "tosu_dep_min": time_to_min(tosu_dep),
                    "kurume_arr": kurume_arr,
                    "kurume_arr_min": time_to_min(kurume_arr),
                    "days": info["days"]
                })
    
    # Sort tosu_kurume_trains by tosu_dep_min
    tosu_kurume_trains.sort(key=lambda x: x["tosu_dep_min"])
    
    # Now analyze each Hakata train
    valid_journeys = []
    
    for t in h_trains:
        url = "https://www.jrkyushu-timetable.jp" + t["href"]
        info = d_hakata.get(url)
        if not info:
            continue
        
        hakata = info.get("hakata")
        tosu = info.get("tosu")
        kurume = info.get("kurume")
        
        if not hakata or not hakata.get("dep"):
            continue
        
        hakata_dep = hakata["dep"]
        hakata_dep_min = time_to_min(hakata_dep)
        origin = info["origin"]
        origin_dep = info["origin_dep"]
        days = info["days"]
        train_no = info["train_no"]
        dest = info["dest"]
        type_text = t["type_text"]
        
        # Case 1: Direct train from Hakata to Kurume
        if kurume and not kurume.get("pass", False) and kurume.get("arr"):
            tosu_arr = tosu["arr"] if tosu else ""
            tosu_dep = tosu["dep"] if tosu else ""
            kurume_arr = kurume["arr"]
            valid_journeys.append({
                "origin": origin,
                "hakata_dep": hakata_dep,
                "hakata_dep_min": hakata_dep_min,
                "tosu_arr": tosu_arr,
                "tosu_dep": tosu_dep,
                "kurume_arr": kurume_arr,
                "kurume_arr_min": time_to_min(kurume_arr),
                "is_transfer": False,
                "transfer_info": "",
                "train_no": train_no,
                "dest": dest,
                "type_text": type_text,
                "days": days
            })
        elif tosu and not tosu.get("pass", False) and tosu.get("arr"):
            # Case 2: Train reaches Tosu (e.g. terminates at Tosu, or goes to Nagasaki line/Kohoku),
            # but connects to a train from Tosu to Kurume!
            tosu_arr = tosu["arr"]
            tosu_arr_min = time_to_min(tosu_arr)
            
            # Find a connecting train at Tosu
            # Transfer condition: connection arrives at Tosu >= tosu_arr_min + 1 min,
            # and departs within reasonable time (e.g. <= tosu_arr_min + 30 min)
            possible_connections = [
                ct for ct in tosu_kurume_trains
                if ct["tosu_dep_min"] >= tosu_arr_min + 1 and ct["tosu_dep_min"] <= tosu_arr_min + 30
            ]
            if possible_connections:
                conn = possible_connections[0] # earliest connection
                valid_journeys.append({
                    "origin": origin,
                    "hakata_dep": hakata_dep,
                    "hakata_dep_min": hakata_dep_min,
                    "tosu_arr": tosu_arr,
                    "tosu_dep": conn["tosu_dep"],
                    "kurume_arr": conn["kurume_arr"],
                    "kurume_arr_min": conn["kurume_arr_min"],
                    "is_transfer": True,
                    "transfer_info": f"鳥栖乗換 ({conn['origin']}発 {conn['dest']}行)",
                    "train_no": f"{train_no}→{conn['train_no']}",
                    "dest": dest,
                    "type_text": type_text,
                    "days": days
                })
        else:
            # Case 3: Terminates before Tosu (e.g. Futsukaichi, Minami-Fukuoka) -> Exclude per prompt
            pass

    # Now filter out dominated trains:
    # "二日市行など、結局後続列車に乗らないと久留米に着かない列車は省いて"
    # Also if a train departs Hakata earlier but arrives at Kurume later than (or equal to) a later departing train,
    # it is dominated! (e.g. a slow local overtaken by a rapid)
    # Let's check dominated trains.
    valid_journeys.sort(key=lambda x: x["hakata_dep_min"])
    
    # Filter: a train is valid if there is NO subsequent train departing Hakata later that arrives earlier
    # Actually, if train B departs AFTER train A, and arrives BEFORE or AT THE SAME TIME as train A,
    # then nobody taking Hakata -> Kurume would take train A (train A is overtaken or useless).
    filtered_journeys = []
    n = len(valid_journeys)
    for i in range(n):
        t_a = valid_journeys[i]
        overtaken = False
        for j in range(i + 1, n):
            t_b = valid_journeys[j]
            # t_b departs later or same time
            if t_b["kurume_arr_min"] <= t_a["kurume_arr_min"]:
                overtaken = True
                break
        if not overtaken:
            filtered_journeys.append(t_a)
        else:
            print(f"[{day_key}] Dominated/Overtaken: Hakata {t_a['hakata_dep']} -> Kurume {t_a['kurume_arr']} (overtaken by Hakata {t_b['hakata_dep']} -> Kurume {t_b['kurume_arr']})")

    return filtered_journeys

w_journeys = analyze_schedule("weekday")
h_journeys = analyze_schedule("holiday")

print(f"\nFinal Valid Journeys - Weekday: {len(w_journeys)}, Holiday: {len(h_journeys)}")

with open("processed_journeys.json", "w", encoding="utf-8") as f:
    json.dump({"weekday": w_journeys, "holiday": h_journeys}, f, ensure_ascii=False, indent=2)
