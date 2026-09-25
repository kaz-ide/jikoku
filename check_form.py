import re

with open("hakata_raw.html", "r", encoding="utf-8") as f:
    text = f.read()

forms = re.findall(r'<form[^>]*>(.*?)</form>', text, re.DOTALL)
for i, form in enumerate(forms):
    print(f"--- Form {i} ---")
    action = re.search(r'action="([^"]*)"', form)
    method = re.search(r'method="([^"]*)"', form)
    print("Action:", action.group(1) if action else "None")
    print("Method:", method.group(1) if method else "None")
    inputs = re.findall(r'<input[^>]*name="([^"]*)"[^>]*value="([^"]*)"', form)
    print("Inputs:", inputs)
    selects = re.findall(r'<select[^>]*name="([^"]*)"', form)
    print("Selects:", selects)
