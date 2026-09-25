import json

with open("processed_journeys.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for i, j in enumerate(data["weekday"], 1):
    print(f"{i:2d}: 博多{j['hakata_dep']} -> 久留米{j['kurume_arr']} | 始発:{j['origin']} 行先:{j['dest']} | 種別:{j['type_text']} | {j['transfer_info']}")
