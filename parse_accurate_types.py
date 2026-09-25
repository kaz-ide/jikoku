import re
import json

with open("hakata_raw.html", "r", encoding="utf-8") as f:
    text = f.read()

# Let's inspect all cells in 鹿児島本線 久留米・大牟田方面（下り）
start_title = text.find("鹿児島本線 久留米・大牟田方面（下り）")
next_title = text.find("篠栗線 長者原・桂川・直方・折尾方面（上り）")
section = text[start_title:next_title]

hour_rows = re.findall(r'<TH[^>]*>.*?<FONT COLOR="#FFFFFF">(\d+)</FONT>.*?<!-- 特急・急行以外の列車 -->(.*?)</tr>', section, re.DOTALL)

train_types = {}

for hour, non_ltd in hour_rows:
    hour = int(hour)
    cells = re.findall(r'<td class=back\d valign="bottom" align="center" nowrap>(.*?)</td>', non_ltd, re.DOTALL)
    for c in cells:
        m_link = re.search(r'<a href="([^"]+)"[^>]*><b>(\d+)</b></a>', c)
        if not m_link:
            continue
        href, minute = m_link.group(1), int(m_link.group(2))
        dep_time = f"{hour:02d}:{minute:02d}"
        
        # Check text before minute link and after minute link
        parts = c.split(m_link.group(0))
        before = re.sub(r'<[^>]+>', ' ', parts[0]).strip()
        after = re.sub(r'<[^>]+>', ' ', parts[1]).strip()
        
        # Determine train type from before/after and color
        train_type = "普通"
        if "快" in before or "快速" in before or 'color="blue"' in c:
            if "区間快速" in before or "区快" in before or "各駅停車" in after or "区間快速" in after:
                train_type = "区間快速"
            else:
                train_type = "快速"
        elif "区快" in before or "区間快速" in before or "各駅停車" in after or "快速" in after:
            train_type = "区間快速"
            
        # destination is usually the first word in after
        after_words = [w for w in after.split() if w != "&nbsp;"]
        dest = after_words[0] if after_words else ""
        sub_info = " ".join(after_words[1:]) if len(after_words) > 1 else ""
        
        train_types[dep_time] = {
            "type": train_type,
            "dest": dest,
            "sub_info": sub_info,
            "before": before,
            "after": after
        }

with open("train_types_parsed.json", "w", encoding="utf-8") as out:
    json.dump(train_types, out, ensure_ascii=False, indent=2)

print("Parsed train types for", len(train_types), "trains.")
