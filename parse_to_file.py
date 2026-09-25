import re

with open("hakata_raw.html", "r", encoding="utf-8") as f:
    text = f.read()

with open("hakata_parsed.txt", "w", encoding="utf-8") as out:
    # Find all table headers, links, and captions
    for m in re.finditer(r'<caption[^>]*>(.*?)</caption>', text, re.DOTALL):
        out.write("Caption: " + re.sub(r'<[^>]+>', '', m.group(1)).strip() + "\n")
    for m in re.finditer(r'<h[1-6][^>]*>(.*?)</h[1-6]>', text, re.DOTALL):
        out.write("Heading: " + re.sub(r'<[^>]+>', '', m.group(1)).strip() + "\n")
    for m in re.finditer(r'<th[^>]*>(.*?)</th>', text, re.DOTALL):
        t = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if t:
            out.write("TH: " + t + "\n")

print("Parsed successfully!")
