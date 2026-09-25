import json

with open("detailed_hakata.json", "r", encoding="utf-8") as f:
    d_hakata = json.load(f)

with open("detailed_tosu.json", "r", encoding="utf-8") as f:
    d_tosu = json.load(f)

# Collect all days
days_count = {}
for u, info in d_hakata.items():
    d = info.get("days", "")
    days_count[d] = days_count.get(d, 0) + 1

for u, info in d_tosu.items():
    d = info.get("days", "")
    days_count[d] = days_count.get(d, 0) + 1

with open("days_summary.txt", "w", encoding="utf-8") as out:
    out.write("Days summary:\n")
    for d, c in days_count.items():
        out.write(f"  '{d}': {c}\n")
    
    out.write("\nTrains with non-'毎日運転':\n")
    for u, info in d_hakata.items():
        d = info.get("days", "")
        if d != "毎日運転":
            out.write(f"Hakata: {info.get('train_no')} ({info.get('origin')}->{info.get('dest')}) Days: {d} Hakata dep: {info.get('hakata', {}).get('dep')}\n")
    for u, info in d_tosu.items():
        d = info.get("days", "")
        if d != "毎日運転":
            out.write(f"Tosu: {info.get('train_no')} ({info.get('origin')}->{info.get('dest')}) Days: {d} Tosu dep: {info.get('tosu', {}).get('dep')}\n")
