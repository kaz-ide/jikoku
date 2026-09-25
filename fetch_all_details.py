import urllib.request
import re
import json
import time
import os

CACHE_DIR = "cache_trains"
os.makedirs(CACHE_DIR, exist_ok=True)

def fetch_url(url):
    # generate filename from url
    fname = os.path.join(CACHE_DIR, re.sub(r'[^a-zA-Z0-9]', '_', url) + ".html")
    if os.path.exists(fname):
        with open(fname, "r", encoding="utf-8") as f:
            return f.read()
    
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        content = urllib.request.urlopen(req, timeout=10).read()
        text = content.decode('utf-8', errors='replace')
        with open(fname, "w", encoding="utf-8") as f:
            f.write(text)
        time.sleep(0.1) # polite delay
        return text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_train_detail_html(text):
    if not text:
        return None
    m_no = re.search(r'列車番号</td>\s*<td[^>]*>\s*([A-Za-z0-9]+)', text)
    train_no = m_no.group(1).strip() if m_no else ""
    
    m_days = re.search(r'運転日</td>\s*<td[^>]*>\s*([^<]+)', text)
    days = m_days.group(1).strip() if m_days else ""
    
    m_rem = re.search(r'備考</td>\s*<td[^>]*>\s*([^<]+)', text)
    remarks = m_rem.group(1).strip() if m_rem else ""
    
    station_rows = re.findall(r'<!-- 駅名 -->\s*<td[^>]*>\s*<a[^>]*>([^<]+)</a>\s*</td>\s*<!-- 時刻 -->\s*<td[^>]*>(.*?)</td>', text, re.DOTALL)
    
    stops = []
    for st_name, time_td in station_rows:
        st_name = st_name.strip()
        clean_time = re.sub(r'<[^>]+>', ' ', time_td).strip()
        arr_m = re.search(r'(\d{2}:\d{2})\s*着', clean_time)
        dep_m = re.search(r'(\d{2}:\d{2})\s*発', clean_time)
        arr = arr_m.group(1) if arr_m else None
        dep = dep_m.group(1) if dep_m else None
        is_pass = "レ" in clean_time or "通過" in clean_time
        stops.append({
            "station": st_name,
            "arr": arr,
            "dep": dep,
            "pass": is_pass
        })
    
    origin = stops[0]["station"] if stops else ""
    origin_dep = stops[0]["dep"] if stops else ""
    dest = stops[-1]["station"] if stops else ""
    dest_arr = stops[-1]["arr"] if stops else ""
    
    hakata = next((s for s in stops if s["station"] == "博多"), None)
    tosu = next((s for s in stops if s["station"] == "鳥栖"), None)
    kurume = next((s for s in stops if s["station"] == "久留米"), None)
    futsukaichi = next((s for s in stops if s["station"] == "二日市"), None)
    
    return {
        "train_no": train_no,
        "days": days,
        "remarks": remarks,
        "origin": origin,
        "origin_dep": origin_dep,
        "dest": dest,
        "dest_arr": dest_arr,
        "hakata": hakata,
        "futsukaichi": futsukaichi,
        "tosu": tosu,
        "kurume": kurume,
        "all_stops_count": len(stops),
        "stops": [{"station": s["station"], "arr": s["arr"], "dep": s["dep"]} for s in stops]
    }

# Load Hakata train list
with open("hakata_train_list.json", "r", encoding="utf-8") as f:
    h_data = json.load(f)

# Process Hakata trains
detailed_hakata = {}
all_urls = set()
for t in h_data["weekday"] + h_data["holiday"]:
    url = "https://www.jrkyushu-timetable.jp" + t["href"]
    all_urls.add(url)

print(f"Total unique URLs to fetch: {len(all_urls)}")
for i, url in enumerate(all_urls):
    if (i + 1) % 20 == 0:
        print(f"Fetched {i + 1}/{len(all_urls)}...")
    html = fetch_url(url)
    info = parse_train_detail_html(html)
    if info:
        detailed_hakata[url] = info

with open("detailed_hakata.json", "w", encoding="utf-8") as f:
    json.dump(detailed_hakata, f, ensure_ascii=False, indent=2)

print("Done fetching Hakata trains!")
