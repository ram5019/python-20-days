# Day 27: CSV and JSON

**Example:** `examples/day27_csv_json.py` | **Your stub:** `advanced/day27_csv_json.py`

---

## 1. The big idea

- **CSV** (comma-separated values) = a **table as plain text**: one row per line, columns separated by commas. Opens in Excel.
- **JSON** (Day 19) = **nested structured data** as text.

Python's `csv` and `json` modules read and write both. Together they cover most data you will meet: exports, reports, API responses, configs.

## 2. Why does it exist?

- Spreadsheet and report data arrives as **CSV** (exports from monitoring tools, ticketing systems, finance).
- APIs and configs speak **JSON**.
- Often you must **convert** between them, or clean and summarise.

Why not just `.split(",")`? Because real CSV has quoted commas (`"Smith, John"`), embedded newlines and escaping. The `csv` module handles all that correctly.

## 3. Simple way to understand

- **CSV** = a **spreadsheet printed flat**: simple and rectangular, every cell a piece of text.
- **JSON** = a **filing cabinet with folders inside folders**: it can hold lists and dicts of any depth.

Converting CSV → JSON = turning each spreadsheet row into a labelled folder (a dict). JSON → CSV = flattening those folders back into rows, which only works when records have similar fields.

## 4. How it works

| Task | Tool | Gives |
|------|------|-------|
| read rows as lists | `csv.reader(f)` | `["web01", "40", "up"]` |
| read rows as dicts | `csv.DictReader(f)` | `{"name": "web01", ...}` |
| write lists | `csv.writer(f).writerows(rows)` | |
| write dicts | `csv.DictWriter(f, fieldnames=...)` | |
| JSON file | `json.load` / `json.dump` (Day 19) | |

Two golden rules:
1. **Open CSV files with `newline=""`** when writing, or you get blank lines on Windows.
2. **Everything read from CSV is a string.** `"92"` is not `92`. Convert it.

## 5. Code walkthrough, block by block

### Block 1: write with `csv.writer`
A list of lists (Day 10) is the table. `writerows` writes each inner list as a line. Compare with your stub, which uses `writerow` for one row at a time.

### Block 2: read as lists
`csv.reader(f)` is lazy (like Day 24 generators): it gives one row per loop round. Look at the printout: the numbers appear as `'40'` with quotes. They are strings.

### Block 3: read as dicts
`DictReader` uses the first row as keys, so each record is a dict (Day 13). `list(...)` collects all rows. Now `servers[1]["status"]` is self-explanatory, much nicer than `row[2]`.

### Block 4: convert types
A loop turns `cpu` into `int`. Then a list comprehension (Day 21) filters for `cpu > 80`. **Without the conversion** the comparison `"92" > 80` would raise `TypeError` (Day 5).

### Block 5: write dicts
`DictWriter` needs `fieldnames` to fix the column order. `writeheader()` writes the first row, and `writerows(servers)` writes the records. Use this when your data is already a list of dicts.

### Block 6: CSV → JSON
Read with `DictReader`, dump with `json.dump` (Day 19). Three lines turn a spreadsheet export into API-ready JSON. `read_text()[:80]` previews the start of the file (Path method from Day 15 with a slice from Day 3).

### Block 7: JSON → CSV
`fieldnames=records[0].keys()` takes the columns from the first record. This assumes all records share the same keys. If they do not, collect all keys first.

### Block 8: summarise
The Day 13 counting recipe on the `status` field gives `{'up': 2, 'down': 1}`. This is exactly what Pandas (Track 1) will do in one line: `df["status"].value_counts()`.

## 6. How the blocks connect

```
Block 1  list of lists  ──► CSV file
Block 2  CSV file ──► list of lists (strings)
Block 3  CSV file ──► list of dicts
Block 4  fix types so maths/comparisons work
Block 5  list of dicts ──► CSV
Blocks 6, 7  convert between formats
Block 8  summarise the data
```

The centre of everything is the **list of dicts** shape you used in Day 13 and Day 20.

## 7. Common mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| `open(..., "w")` without `newline=""` | blank rows in output | add `newline=""` |
| Doing maths on CSV values | `TypeError` or string joining | convert with `int()` / `float()` |
| Splitting CSV lines with `.split(",")` | breaks on quoted commas | use `csv` |
| Wrong encoding (strange characters) | garbled text | `open(f, encoding="utf-8")` |
| Records with different keys → `DictWriter` error | `ValueError` | gather all keys, or `extrasaction="ignore"` |
| Reading a huge CSV into a list | memory use | loop over the reader instead |

## 8. Practice

1. In your stub, read `data.csv` as dicts and print the average age.
2. Add a new column `grade` computed from marks and write a new CSV.
3. Convert a CSV of servers to JSON, then filter only `status == "down"` and save that too.
4. Count rows per category (Day 13 pattern) from a CSV you export from any tool you use.
5. Write `csv_to_json(csv_path, json_path)` and `json_to_csv(json_path, csv_path)` helper functions.
6. Handle a missing file and a missing column with `try/except` (Day 16).

## 9. Self-check

- Why is `csv` better than `.split(",")`?
- What type are values read from a CSV file?
- What is the difference between `DictReader` and `reader`?
- Why does `newline=""` matter when writing?

**Next:** Day 28: package all of this into a **command-line tool** other people can run.
