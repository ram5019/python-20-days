"""Day 27 example: CSV and JSON.

Run:  python3 learning-path/advanced/examples/day27_csv_json.py
(Creates and removes temporary files next to this script.)
"""

import csv
import json
from pathlib import Path

BASE = Path(__file__).parent
CSV_FILE = BASE / "demo_servers.csv"
JSON_FILE = BASE / "demo_servers.json"

# BLOCK 1: write a CSV with csv.writer
rows = [
    ["name", "cpu", "status"],
    ["web01", 40, "up"],
    ["web02", 92, "up"],
    ["db01", 0, "down"],
]
with open(CSV_FILE, "w", newline="") as f:         # newline="" avoids blank lines
    writer = csv.writer(f)
    writer.writerows(rows)

# BLOCK 2: read a CSV as lists
with open(CSV_FILE) as f:
    for row in csv.reader(f):
        print(row)                                  # every value is a STRING

# BLOCK 3: read a CSV as dicts (header row becomes the keys)
with open(CSV_FILE) as f:
    servers = list(csv.DictReader(f))
print(servers[1])                                   # {'name': 'web02', 'cpu': '92', ...}

# BLOCK 4: convert types yourself
for s in servers:
    s["cpu"] = int(s["cpu"])
busy = [s["name"] for s in servers if s["cpu"] > 80]
print("Busy servers:", busy)

# BLOCK 5: write dicts to CSV
with open(CSV_FILE, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "cpu", "status"])
    writer.writeheader()
    writer.writerows(servers)

# BLOCK 6: CSV -> JSON
with open(CSV_FILE) as f:
    data = list(csv.DictReader(f))
with open(JSON_FILE, "w") as f:
    json.dump(data, f, indent=2)
print(JSON_FILE.read_text()[:80], "...")

# BLOCK 7: JSON -> CSV
with open(JSON_FILE) as f:
    records = json.load(f)
with open(CSV_FILE, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=records[0].keys())
    writer.writeheader()
    writer.writerows(records)
print("Round trip complete:", len(records), "records")

# BLOCK 8: summarise (Day 13 counting pattern)
status_count = {}
for r in records:
    status_count[r["status"]] = status_count.get(r["status"], 0) + 1
print(status_count)                                 # {'up': 2, 'down': 1}

# clean up
CSV_FILE.unlink()
JSON_FILE.unlink()
