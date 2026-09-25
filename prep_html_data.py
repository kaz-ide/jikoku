import json

with open("enriched_timetable.json", "r", encoding="utf-8") as f:
    trains = json.load(f)

# Let's inspect all 47 trains to verify every field
for t in trains:
    # clean note and badge
    badge = t["type_badge"]
    note = t["note"]
    if t["is_transfer"]:
        if "二日市" in note:
            t["type_badge"] = "区間快速"
            t["type_class"] = "bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-300 border border-amber-300 dark:border-amber-700"
            t["summary_note"] = "鳥栖で乗換 (快速区間: 博多〜二日市)"
        else:
            t["type_badge"] = "普通"
            t["type_class"] = "bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300 border border-slate-300 dark:border-slate-700"
            t["summary_note"] = "鳥栖で乗換"
    else:
        if badge == "快速":
            t["type_class"] = "bg-blue-100 text-blue-800 dark:bg-blue-900/40 dark:text-blue-300 border border-blue-300 dark:border-blue-700 font-bold"
            t["summary_note"] = f"直通 ({t['dest']}行)"
        elif badge == "区間快速":
            t["type_class"] = "bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-300 border border-amber-300 dark:border-amber-700"
            t["summary_note"] = f"直通 ({t['note']})"
        else:
            t["type_class"] = "bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300 border border-slate-300 dark:border-slate-700"
            t["summary_note"] = f"直通 ({t['dest']}行)"

with open("final_trains.json", "w", encoding="utf-8") as f:
    json.dump(trains, f, ensure_ascii=False, indent=2)

print("Saved final_trains.json!")
