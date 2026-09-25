import json

with open("train_types_parsed.json", "r", encoding="utf-8") as f:
    tt = json.load(f)

with open("final_trains.json", "r", encoding="utf-8") as f:
    trains = json.load(f)

for t in trains:
    dep = t["hakata_dep"]
    info = tt.get(dep, {})
    parsed_type = info.get("type", "普通")
    sub_info = info.get("sub_info", "").replace("&nbsp;", "").strip()
    
    t["type_badge"] = parsed_type
    
    # refine note and summary
    if t["is_transfer"]:
        # Transfer train
        # Get transfer train details
        # e.g. "鳥栖乗換 (鳥栖発 大牟田行)"
        conn_desc = t["transfer_info"]
        if sub_info:
            t["summary_note"] = f"鳥栖乗換 ({sub_info})"
            t["note"] = f"{sub_info}／鳥栖で乗換"
        else:
            t["summary_note"] = conn_desc
            t["note"] = f"鳥栖で乗換 ({conn_desc})"
    else:
        # Direct train
        if sub_info:
            t["summary_note"] = f"直通 ({sub_info})"
            t["note"] = f"{t['dest']}行 ({sub_info})"
        else:
            t["summary_note"] = f"直通 ({t['dest']}行)"
            t["note"] = f"{t['dest']}行"

# Save updated final_trains.json
with open("final_trains.json", "w", encoding="utf-8") as f:
    json.dump(trains, f, ensure_ascii=False, indent=2)

print("Updated final_trains.json with precise types!")
