# Day 19: JSON

**Time:** ~2 hours | **Example:** `examples/day19_json.py` | **Your practice file:** `week4_realworld/day19_json.py`

---

## 1. The big idea

**JSON** (JavaScript Object Notation) is a **text format** for structured data. It looks almost exactly like Python dictionaries and lists. Python's `json` module converts between the two:

```
Python dict/list  ──json.dumps──►  JSON text
Python dict/list  ◄──json.loads──  JSON text
```

## 2. Why does this exist?

On Day 15 you could save **text** to a file. But your real data is dicts and lists (Day 13). You could not just `f.write(student)`: that fails with a `TypeError` because `write` wants a string.

JSON solves it: it turns structured data into a string you can write to disk, and back into structure when you read it. And it is the **universal language of data exchange**: REST APIs, config files, logs, Kubernetes manifests, and the WEKA tooling you work with all use it. Learning JSON means you can talk to almost any system.

## 3. Simple way to understand

**Packing a suitcase for a flight.**

- Your data in memory is a **fully assembled wardrobe** (dict/list: structured, but it cannot travel).
- `dumps` / `dump` = **fold and pack it flat** into a suitcase (text).
- The suitcase can be stored (file) or shipped (network).
- `loads` / `load` = **unpack and hang it up again** (dict/list).

Two special words: **serialise** = pack (object → text), **deserialise** = unpack (text → object).

## 4. How it works

### Type mapping

| Python | JSON |
|--------|------|
| `dict` | object `{ }` |
| `list`, `tuple` | array `[ ]` |
| `str` | string `"..."` |
| `int`, `float` | number |
| `True` / `False` | `true` / `false` |
| `None` | `null` |

JSON rules: keys must be **strings in double quotes**; no trailing commas; no comments.

### The four functions: remember the "s"

| Function | From → To | The "s" means |
|----------|-----------|---------------|
| `json.dumps(obj)` | object → **s**tring | string |
| `json.loads(text)` | **s**tring → object | string |
| `json.dump(obj, file)` | object → file | (no s: file) |
| `json.load(file)` | file → object | (no s: file) |

`indent=2` makes the output human-readable.

## 5. Code walkthrough, block by block

### Block 1: dict → JSON text

```python
data = {"name": "Ravi", "age": 30, "active": True,
        "manager": None, "skills": ["Python", "SQL"]}
text = json.dumps(data, indent=2)
print(text)
print(type(text))    # str
```

**What it does:** builds a normal dictionary (with a nested list from Day 10) and converts it to a string. Look at the printed result: `True` became `true` and `None` became `null`. The type is `str`: it is only text now, so `text["name"]` would fail. This is your stub's first half.

### Block 2: JSON text → dict

```python
parsed = json.loads(text)
print(type(parsed))        # dict
print("Skills:", parsed["skills"])
print(parsed == data)      # True
```

**What it does:** the reverse. `loads` rebuilds the dict, so key access works again. The `True` shows a **round trip** loses nothing: data → text → data gives back the same thing. That is your stub's second half.

### Block 3: the mapping in action

```python
print(json.dumps([True, False, None, 1.5, "x"]))
# [true, false, null, 1.5, "x"]
```

**What it does:** a tiny experiment proving the type table above. Experiments like this are the fastest way to learn what a library does.

### Block 4: save to a file

```python
with open(FILE, "w") as f:
    json.dump(data, f, indent=2)
```

**What it does:** `json.dump` (no `s`) combines **Day 15's** `with open(..., "w")` and Block 1's conversion in one step: it writes JSON directly into the open file. The file now contains readable text you can open in any editor.

### Block 5: load from a file

```python
with open(FILE) as f:
    loaded = json.load(f)
print("Loaded name:", loaded["name"])
```

**What it does:** the other direction: read the file and rebuild the dict. This pair (Blocks 4 and 5) makes data **persist** between runs.

### Block 6: a list of records

```python
students = [{"name": "Asha", "marks": 88}, {"name": "Meena", "marks": 95}]
with open(FILE, "w") as f:
    json.dump(students, f, indent=2)

with open(FILE) as f:
    students = json.load(f)
students.append({"name": "Ravi", "marks": 72})
with open(FILE, "w") as f:
    json.dump(students, f, indent=2)
```

**What it does:** this is the **load → change → save** cycle, the engine of every small data app:

```
   ┌──── load from file ────┐
   ▼                        │
 modify in memory           │
 (append/edit/delete)       │
   │                        │
   └──── save to file ──────┘
```

The middle step is plain Day 11 list work on a list of Day 13 dicts. JSON simply feeds data in and out. **This is exactly the structure of your Day 20 project.**

### Block 7: safe loading

```python
def load_records(path):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("File is corrupted, starting empty")
        return []
```

**What it does:** applies **Day 16** to JSON. Two things can go wrong when loading:
- The file does not exist (first run) → start with an empty list.
- The file exists but is not valid JSON (hand-edited, half-written) → `JSONDecodeError`.

Each case is handled separately, and the function **always returns a list**, so the rest of the program does not need to worry.

### Block 8: what JSON cannot store

```python
from datetime import date
try:
    json.dumps({"today": date.today()})
except TypeError as e:
    print("Cannot serialise:", e)
print(json.dumps({"today": str(date.today())}))
```

**What it does:** JSON only knows the basic types in the mapping table. A `date`, a `set` or one of your own class objects (Day 18) raises `TypeError`. The fix is to **convert to a basic type first** (`str(date)`, `list(some_set)`, or a dict made from your object's attributes).

## 6. How the blocks connect

```
Blocks 1, 2   convert in memory           dumps / loads    (string ↔ object)
Block 3       the type-mapping rules
Blocks 4, 5   the same conversion + files dump / load      (Day 15 + 19)
Block 6       load → modify → save cycle   (Days 10, 11, 13 + 19)
Block 7       make loading safe            (Day 16)
Block 8       know the limits
```

Pipeline: **dict → JSON text → file → JSON text → dict**.

## 7. Common mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| Mixing up `dump`/`dumps` and `load`/`loads` | `AttributeError`/`TypeError` | the **s** = string |
| Single quotes in a JSON file | `JSONDecodeError` | JSON needs `"double"` quotes |
| Trailing comma in a hand-written file | `JSONDecodeError` | remove it |
| Opening with `"w"` before reading | file erased, then load fails | read first, write later |
| Using `json.dumps` on a set/date/object | `TypeError` | convert to basic types |
| Numeric dict keys come back as strings | `{1: "a"}` → `{"1": "a"}` | remember JSON keys are always strings |
| Forgetting `indent` | one unreadable line | add `indent=2` |

## 8. Practice

1. Fill in `day19_json.py` (your stub works already): extend the data with a nested dict `{"address": {"city": "Chennai"}}` and print `parsed["address"]["city"]`.
2. Save a list of 3 servers (name, ip, status) to `servers.json`, then reload and print only the ones with status `down`.
3. Write `load_json(path, default)` and `save_json(path, data)` helper functions and use them everywhere.
4. Build a tiny **settings file**: load `config.json` if it exists, else create it with defaults.
5. Open a JSON file in a text editor, break it on purpose, and watch `JSONDecodeError`.
6. Convert a `Student` object (Day 18) to a dict (`{"name": s.name, "marks": s.marks}`), save it, and rebuild the object.

## 9. Self-check

- What is the difference between `dumps` and `dump`?
- What does `None` become in JSON? And `True`?
- Why can't you save a `set` directly?
- What is the load → modify → save cycle?
- Which two errors should safe loading handle?

**Next:** Day 20: the final project. You will combine **functions, dicts, lists, loops, files, JSON and error handling** into one program.
