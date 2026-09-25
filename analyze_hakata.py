import re

with open("hakata_raw.html", "r", encoding="utf-8") as f:
    text = f.read()

# Find forms, buttons, selects, route names
print("Title:", re.findall(r'<title>(.*?)</title>', text, re.IGNORECASE))

# Look for table headers or line names
for m in re.finditer(r'<h[1-6][^>]*>(.*?)</h[1-6]>', text, re.DOTALL):
    clean = re.sub(r'<[^>]+>', '', m.group(1)).strip()
    if clean:
        print("Heading:", clean)

# Look for select options
for m in re.finditer(r'<select[^>]*name="([^"]+)"[^>]*>(.*?)</select>', text, re.DOTALL):
    name = m.group(1)
    opts = re.findall(r'<option[^>]*value="([^"]*)"[^>]*>(.*?)</option>', m.group(2))
    print(f"Select '{name}':")
    for val, opt_txt in opts[:15]:
        print(f"  {val} -> {re.sub(r'<[^>]+>', '', opt_txt).strip()}")
