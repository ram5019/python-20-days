"""Day 27 — CSV / JSON."""

import csv
import json
import os

def main():
    if not os.path.exists("data.csv"):
        with open("data.csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["name", "age"])
            w.writerow(["Ravi", 22])

    with open("data.csv") as f:
        print("Rows:", len(list(csv.reader(f))))

    json.dump({"a": 1}, open("data.json", "w"))

if __name__ == "__main__":
    main()