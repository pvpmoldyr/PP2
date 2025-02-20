import json
with open("json/sample-data.json", 'r') as file:
    data = json.load(file)


print("Interface Status")
print("=" * 90)
print(f"{'DN':<50} {'Description':<20} {'Speed':<9} {'MTU':<6}")
print("-" * 90)

for item in data["imdata"]:
    attributes = item["l1PhysIf"]["attributes"]
    dn = attributes.get("dn", "")
    descr = attributes.get("descr", "")
    speed = attributes.get("speed", "")
    mtu = attributes.get("mtu", "")
    print(f"{dn:<50} {descr:<20} {speed:<9} {mtu:<6}")
