import json

with open("processed_journeys.json", "r", encoding="utf-8") as f:
    data = json.load(f)

w = data["weekday"]
h = data["holiday"]

print("--- Weekday Journeys Sample ---")
for j in w[:10]:
    tf = f"[{j['transfer_info']}]" if j['is_transfer'] else "直通"
    print(f"始発:{j['origin']} | 博多:{j['hakata_dep']} -> 鳥栖:{j['tosu_arr']}/{j['tosu_dep']} -> 久留米:{j['kurume_arr']} | {tf} | {j['type_text']} | {j['days']}")

print("\n--- Check differences between Weekday and Holiday ---")
w_times = {j['hakata_dep']: j for j in w}
h_times = {j['hakata_dep']: j for j in h}

for dep in sorted(set(list(w_times.keys()) + list(h_times.keys()))):
    in_w = dep in w_times
    in_h = dep in h_times
    if not in_w or not in_h:
        print(f"Dep {dep}: in_w={in_w}, in_h={in_h}")
    else:
        jw = w_times[dep]
        jh = h_times[dep]
        diffs = []
        if jw['kurume_arr'] != jh['kurume_arr']:
            diffs.append(f"Kurume arr: {jw['kurume_arr']} vs {jh['kurume_arr']}")
        if jw['tosu_arr'] != jh['tosu_arr'] or jw['tosu_dep'] != jh['tosu_dep']:
            diffs.append(f"Tosu: {jw['tosu_arr']}/{jw['tosu_dep']} vs {jh['tosu_arr']}/{jh['tosu_dep']}")
        if jw['origin'] != jh['origin']:
            diffs.append(f"Origin: {jw['origin']} vs {jh['origin']}")
        if jw['days'] != jh['days']:
            diffs.append(f"Days: {jw['days']} vs {jh['days']}")
        if diffs:
            print(f"Dep {dep} differences: {', '.join(diffs)}")
