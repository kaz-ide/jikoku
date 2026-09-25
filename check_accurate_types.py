import json

with open("train_types_parsed.json", "r", encoding="utf-8") as f:
    tt = json.load(f)

with open("final_trains.json", "r", encoding="utf-8") as f:
    trains = json.load(f)

for t in trains:
    dep = t["hakata_dep"]
    info = tt.get(dep, {})
    print(f"Hakata {dep}: Type={info.get('type')}, Dest={info.get('dest')}, Sub={info.get('sub_info')} (before: '{info.get('before')}')")
