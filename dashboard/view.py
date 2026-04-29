import json

print("📊 ROUTER LIVE LOGS\n")

try:
    with open("logs/router.jsonl") as f:
        for line in f.readlines()[-15:]:
            print(json.loads(line))
except:
    print("No logs yet")
