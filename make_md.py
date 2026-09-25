import json

with open("final_trains.json", "r", encoding="utf-8") as f:
    trains = json.load(f)

# Group into morning, day, evening, night
bands = {
    "朝（5時〜9時台）": [],
    "日中（10時〜15時台）": [],
    "夕方（16時〜19時台）": [],
    "夜間（20時〜23時台）": []
}

for t in trains:
    h = int(t["hakata_dep"].split(":")[0])
    if 5 <= h < 10:
        bands["朝（5時〜9時台）"].append(t)
    elif 10 <= h < 16:
        bands["日中（10時〜15時台）"].append(t)
    elif 16 <= h < 20:
        bands["夕方（16時〜19時台）"].append(t)
    else:
        bands["夜間（20時〜23時台）"].append(t)

with open("markdown_tables.txt", "w", encoding="utf-8") as out:
    for name, list_t in bands.items():
        out.write(f"### {name} （{len(list_t)}本）\n\n")
        out.write("| 始発駅 | 博多発 | 鳥栖着 | 鳥栖発 | 久留米着 | 種別 / 所要 | 備考・接続 |\n")
        out.write("| :--- | :---: | :---: | :---: | :---: | :---: | :--- |\n")
        for t in list_t:
            badge = f"**{t['type_badge']}**"
            time_str = f"{t['travel_time']}分"
            if t['is_transfer']:
                tosu_str = f"{t['tosu_arr']}着 ➔ {t['tosu_dep']}発"
                note_str = f"鳥栖乗換 ({t['transfer_info'].replace('鳥栖乗換 ', '')})"
            else:
                tosu_str = f"{t['tosu_arr']} / {t['tosu_dep']}"
                note_str = f"直通 ({t['dest']}行)"
            out.write(f"| {t['origin']} | **{t['hakata_dep']}** | {t['tosu_arr']} | {t['tosu_dep']} | **{t['kurume_arr']}** | {badge} ({time_str}) | {note_str} |\n")
        out.write("\n")

print("Generated markdown tables!")
