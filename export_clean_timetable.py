import json

with open("processed_journeys.json", "r", encoding="utf-8") as f:
    data = json.load(f)

journeys = data["weekday"]

with open("valid_timetable.txt", "w", encoding="utf-8") as out:
    out.write(f"【JR博多駅 → JR久留米駅 有効列車時刻表（全{len(journeys)}本）】\n")
    out.write("No. | 始発駅 | 博多発 | 鳥栖着 | 鳥栖発 | 久留米着 | 種別/直通・乗換 | 備考\n")
    out.write("-" * 80 + "\n")
    for i, j in enumerate(journeys, 1):
        transfer_desc = "直通" if not j["is_transfer"] else j["transfer_info"]
        type_str = j["type_text"].replace("&nbsp;", "").strip()
        if not type_str:
            type_str = "普通"
        out.write(f"{i:2d} | {j['origin']:4s} | {j['hakata_dep']} | {j['tosu_arr']} | {j['tosu_dep']} | {j['kurume_arr']} | {type_str} ({transfer_desc}) | {j['days']}\n")

print("Wrote valid_timetable.txt successfully!")
