import json

with open("hakata_train_list.json", "r", encoding="utf-8") as f:
    h_data = json.load(f)

w_list = [f"{t['dep_time']} {t['dest']} ({t['type_text']})" for t in h_data["weekday"]]
h_list = [f"{t['dep_time']} {t['dest']} ({t['type_text']})" for t in h_data["holiday"]]

print("Weekday only trains:")
for t in set(w_list) - set(h_list):
    print("  W:", t)

print("Holiday only trains:")
for t in set(h_list) - set(w_list):
    print("  H:", t)
