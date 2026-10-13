"""Day 27: CSV and JSON. 10 examples, simple to complex.

Run:  python3 advanced/day27_csv_json/more_examples.py

Files are created in a temporary folder that is deleted at the end.
"""

import csv
import io
import json
import tempfile
from collections import defaultdict
from pathlib import Path

TMP = tempfile.TemporaryDirectory()
BASE = Path(TMP.name)


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


# ---------------------------------------------------------------
show(1, "Write a CSV with csv.writer")
# WHAT: save rows as a table.
# HOW : writer.writerows(list_of_lists). newline="" avoids blank lines.
# WHY : CSV opens in Excel and almost every tool.
rows = [
    ["name", "cpu", "status"],
    ["web01", 40, "up"],
    ["web02", 92, "up"],
    ["db01", 0, "down"],
]
servers_csv = BASE / "servers.csv"
with open(servers_csv, "w", newline="") as f:
    csv.writer(f).writerows(rows)
print(servers_csv.read_text())

# ---------------------------------------------------------------
show(2, "Read a CSV as lists")
# WHAT: iterate over rows.
# HOW : csv.reader gives each row as a list of STRINGS.
# WHY : note that numbers come back as text.
with open(servers_csv) as f:
    for row in csv.reader(f):
        print(row)

# ---------------------------------------------------------------
show(3, "Read a CSV as dictionaries")
# WHAT: name each column.
# HOW : DictReader uses the first row as keys.
# WHY : row["status"] is clearer than row[2], and survives column reordering.
with open(servers_csv) as f:
    servers = list(csv.DictReader(f))
print(servers[1])
print(servers[1]["name"], type(servers[1]["cpu"]).__name__)

# ---------------------------------------------------------------
show(4, "Write dictionaries with DictWriter")
# WHAT: save a list of dicts.
# HOW : fieldnames fixes the column order; writeheader writes the first row.
# WHY : your Day 13 data shape goes straight to a file.
people = [{"name": "Asha", "age": 28}, {"name": "Ravi", "age": 31}]
people_csv = BASE / "people.csv"
with open(people_csv, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age"])
    writer.writeheader()
    writer.writerows(people)
print(people_csv.read_text().strip())

# ---------------------------------------------------------------
show(5, "Convert types, then calculate")
# WHAT: make the numbers real numbers.
# HOW : int()/float() on each field; then ordinary Python maths.
# WHY : comparing "92" > 80 raises a TypeError.
for s in servers:
    s["cpu"] = int(s["cpu"])
busy = [s["name"] for s in servers if s["cpu"] > 80]
print("busy:", busy)
print("average cpu:", sum(s["cpu"] for s in servers) / len(servers))

# ---------------------------------------------------------------
show(6, "Why not just split on commas?")
# WHAT: commas and quotes inside a field.
# HOW : the csv module quotes such fields when writing and understands the
#       quotes when reading.
# WHY : splitting on "," breaks on a name like "Smith, John".
text = 'name,comment\n"Smith, John","said ""hi"""\nAna,plain\n'
print("naive split :", text.splitlines()[1].split(","))
print("csv module  :", list(csv.reader(io.StringIO(text)))[1])
out = io.StringIO()
csv.writer(out).writerow(["Doe, Jane", 'She said "yes"'])
print("written as  :", out.getvalue().strip())

# ---------------------------------------------------------------
show(7, "Other delimiters and encodings")
# WHAT: semicolon- and tab-separated files; accents.
# HOW : delimiter=";" or "\t"; encoding="utf-8" when opening files.
# WHY : European Excel exports use semicolons; names contain accents.
semi = "name;city\nZoë;Zürich\nAna;Lyon\n"
print(list(csv.DictReader(io.StringIO(semi), delimiter=";")))
tsv = BASE / "tabs.tsv"
with open(tsv, "w", newline="", encoding="utf-8") as f:
    csv.writer(f, delimiter="\t").writerow(["Zoë", "Zürich"])
print(repr(tsv.read_text(encoding="utf-8")))

# ---------------------------------------------------------------
show(8, "CSV <-> JSON round trip")
# WHAT: convert between the two formats.
# HOW : CSV -> list of dicts -> json.dump, and back with DictWriter.
# WHY : spreadsheets for humans, JSON for programs.
json_file = BASE / "servers.json"
with open(servers_csv) as f:
    records = list(csv.DictReader(f))
json_file.write_text(json.dumps(records, indent=2))
print(json_file.read_text()[:60].replace("\n", " "), "...")
back_csv = BASE / "back.csv"
with open(back_csv, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=records[0].keys())
    writer.writeheader()
    writer.writerows(json.loads(json_file.read_text()))
print("round trip identical:", back_csv.read_text() == servers_csv.read_text())

# ---------------------------------------------------------------
show(9, "Group, summarise and export a report")
# WHAT: totals per category, saved as a new CSV.
# HOW : defaultdict(list) groups rows; compute stats per group.
# WHY : the everyday "pivot table" task.
sales_text = """region,product,amount
North,pen,120
South,pen,80
North,book,200
South,book,150
North,pen,60
"""
sales = list(csv.DictReader(io.StringIO(sales_text)))
by_region = defaultdict(list)
for row in sales:
    by_region[row["region"]].append(int(row["amount"]))
summary = [{"region": r, "orders": len(v), "total": sum(v), "average": round(sum(v) / len(v), 1)}
           for r, v in sorted(by_region.items())]
report_csv = BASE / "report.csv"
with open(report_csv, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=summary[0].keys())
    writer.writeheader()
    writer.writerows(summary)
print(report_csv.read_text().strip())

# ---------------------------------------------------------------
show(10, "Mini program: clean messy CSV data and report the problems")
# WHAT: validate rows, keep good ones, list bad ones, save both outputs.
# HOW : try/except per row (Day 16); good data to JSON, problems to a list.
# WHY : real exports are messy; the report shows what needs fixing.
messy = """name,age,email
Asha,28,asha@example.com
Ravi,abc,ravi@example.com
,41,nobody@example.com
Meena,35,meena-at-example.com
John,-3,john@example.com
Li,52,li@example.com
"""
good, bad = [], []
for line_no, row in enumerate(csv.DictReader(io.StringIO(messy)), start=2):
    try:
        if not row["name"].strip():
            raise ValueError("missing name")
        age = int(row["age"])
        if not 0 < age < 120:
            raise ValueError(f"age {age} out of range")
        if "@" not in row["email"]:
            raise ValueError("bad email")
        good.append({"name": row["name"], "age": age, "email": row["email"]})
    except ValueError as e:
        bad.append(f"line {line_no}: {e}")
clean_json = BASE / "clean.json"
clean_json.write_text(json.dumps(good, indent=2))
print(f"{len(good)} good rows saved, {len(bad)} rejected:")
for problem in bad:
    print("  ", problem)
print("average age of good rows:", sum(g["age"] for g in good) / len(good))

TMP.cleanup()
print("\n(temporary files deleted)")
