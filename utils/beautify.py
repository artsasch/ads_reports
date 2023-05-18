import json


with open('base_data.json', 'r') as f:
    data = json.load(f)

with open('beautiful_base_data.json', 'w') as f:
    json.dump(data, f, indent=3)
    