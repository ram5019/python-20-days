# Track 1: Data Science, NumPy, Pandas, Matplotlib

**Examples:** `examples/t1_numpy.py`, `examples/t1_pandas.py`, `examples/t1_matplotlib.py`
**Install:** `pip install numpy pandas matplotlib`
**Prerequisites:** Days 10 to 13 (lists, dicts), Day 21 (comprehensions), Day 27 (CSV)

---

## 1. The big idea

Three libraries that work as a team:

| Library | Role | Think of it as |
|---------|------|----------------|
| **NumPy** | fast **numbers** in arrays | a calculator that works on a million values at once |
| **Pandas** | **tables** of data (DataFrames) | Excel inside Python, with superpowers |
| **Matplotlib** | **charts** | the drawing tool |

```
raw data (CSV/JSON/API)
      │
      ▼  Pandas: load, clean, filter, group, summarise
  DataFrame ──► (built on) NumPy arrays
      │
      ▼  Matplotlib: turn the summary into a picture
   chart.png
```

## 2. Why do these exist?

You can already do all of this with lists, dicts and loops. The problems:

- **Speed.** Python loops are slow on millions of values. NumPy does the loop in fast compiled code.
- **Convenience.** Day 13's counting loop, Day 27's CSV handling, and sorting by a field are each 5 to 10 lines of work. Pandas does each in one.
- **Insight.** Numbers in a table are hard to read. One chart shows a spike instantly.

Practical uses for you: analyse cluster metrics, find which nodes produce the most alerts, summarise weeks of support-case data, plot latency before and after a change.

## 3. Simple way to understand

- **NumPy array** = an **egg carton**: all the same type, tightly packed, and you can do something to the **whole carton** in one move (`carton * 2`), instead of cracking each egg.
- **DataFrame** = a **spreadsheet**: rows are records, columns are named fields. Each column is a NumPy array underneath.
- **Series** = one column of a DataFrame.
- **Matplotlib figure** = a **blank canvas**; you add lines, bars, labels, then save.

---

## Part 1: NumPy

### The key idea: vectorisation
Apply an operation to **every element without writing a loop**.

```python
a = np.array([10, 20, 30])
a * 2        # array([20, 40, 60])
```
A list does `[10, 20, 30] * 2` → repeats the list! NumPy does the math.

### Code walkthrough (`t1_numpy.py`)

| Block | What it does | Why it matters |
|-------|--------------|----------------|
| 1 | `np.array([...])`, shows `dtype` and `shape` | arrays have a single type and a size |
| 2 | `a + 5`, `a * 2`, `a / 10` | arithmetic on all items at once |
| 3 | times a list comprehension against `big_arr * 2` | shows the speed advantage (often 10 to 100× faster) |
| 4 | `zeros`, `ones`, `arange`, `linspace` | quick ways to create arrays; `arange` is `range` for arrays |
| 5 | 2-D array; `m[1, 2]`, `m[:, 0]` | `[row, column]` indexing; `:` means "all" (slicing, Day 3) |
| 6 | `m.sum(axis=0)` | `axis=0` collapses **down** columns; `axis=1` collapses **across** rows |
| 7 | `latency_ms > 100` gives a **boolean mask**; `latency_ms[mask]` filters | a comprehension's `if`, without a loop; `True` counts as 1 so `.sum()` counts matches |
| 8 | mean, median, percentile, max, `argmax` | the statistics support engineers use (p95 latency) |
| 9 | `reshape(3, 4)` | same data, different shape |

**How the blocks connect:** create (1, 4) → compute on all (2, 3) → shape and index (5, 9) → summarise (6) → filter and measure (7, 8).

---

## Part 2: Pandas

### The key ideas
1. A **DataFrame** is a table. A **Series** is one column.
2. Operate on **columns**, not on rows in a loop.
3. Use **boolean conditions** to filter, and **groupby** to summarise.

### Code walkthrough (`t1_pandas.py`)

| Block | What it does | Python equivalent you already know |
|-------|--------------|------------------------------------|
| 1 | `pd.DataFrame({...})` from a dict of lists | a list of dicts (Day 13), turned sideways |
| 2 | `shape`, `dtypes`, `describe()`, `head()` | **always run these first on new data** |
| 3 | `df["col"]`, `df[["a","b"]]`, `iloc` (by position), `loc` (by label/condition) | indexing and slicing, Days 3 and 10 |
| 4 | `df[df["cpu_pct"] > 80]`; combine with `&` and `|`, **each condition in parentheses** | a loop with `if` and `append` (Day 11) |
| 5 | `df["cpu_frac"] = df["cpu_pct"] / 100` | a list comprehension, over a whole column |
| 6 | `sort_values(..., ascending=False)` | `sorted(..., key=...)`, Day 22 |
| 7 | `groupby("site")["cpu_pct"].mean()`; `.agg(...)` for several stats | grouping with dicts of lists (Day 13, Block 7) |
| 8 | `value_counts()` | your hand-written counting loop (Day 13) |
| 9 | `pd.read_csv(...)` | `csv.DictReader` (Day 27); here it reads from a string for the demo |
| 10 | `isna().sum()`, `fillna`, `dropna` | real data always has gaps |
| 11 | `to_csv(index=False)` | `csv.DictWriter` (Day 27) |

**Groupby in plain words (Block 7):** "split the table by site, **apply** a calculation to each piece, then **combine** the results." Split, apply, combine.

**How the blocks connect:** build (1) → look (2) → select (3) → filter (4) → derive (5) → order (6) → summarise (7, 8) → load real data (9) → clean (10) → save (11). This is the standard analysis workflow.

---

## Part 3: Matplotlib

### The key ideas
1. Create a figure → add things → label → **save** → **close**.
2. Choose the chart type for the question you are asking.

| Question | Chart |
|----------|-------|
| How does it change over time? | line |
| Which category is bigger? | bar |
| How are the values spread? | histogram |
| Is there a relationship between two numbers? | scatter |

### Code walkthrough (`t1_matplotlib.py`)

| Block | What it does |
|-------|--------------|
| setup | `matplotlib.use("Agg")` makes it draw into files so no window is needed; creates a `charts/` folder |
| 1 | `plt.plot(x, y)` plus title and axis labels, then `savefig`, then `close()` |
| 2 | two lines with `label=` and `plt.legend()`; marker and dashed styles; a grid |
| 3 | `plt.bar(categories, values)` |
| 4 | `plt.hist(data, bins=30)` plus `axvline` marking the 95th percentile (uses NumPy) |
| 5 | `plt.subplots(1, 2)` returns a **figure** and **axes**: the object-oriented style you use for anything non-trivial |
| 6 | `df.plot(kind="bar", ...)`: Pandas calls Matplotlib for you |

Run it, then open the PNGs in `charts/`.

**How the three libraries connect:** NumPy generates the numbers (Block 2 uses `sin` and random noise) → Pandas organises them (Block 6) → Matplotlib draws them.

---

## 7. Common mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| `df[df.a > 1 and df.b < 5]` | `ValueError` | use `&` and parentheses: `(df.a > 1) & (df.b < 5)` |
| Looping over DataFrame rows to do maths | very slow | operate on whole columns |
| Chained assignment `df[df.x > 1]["y"] = 0` | change is lost / warning | use `df.loc[df.x > 1, "y"] = 0` |
| Forgetting `plt.close()` | charts pile up on top of each other | close after saving |
| Mixing NumPy shapes `(3,)` and `(3,1)` | surprising broadcasting | print `.shape` often |
| Not checking data types after `read_csv` | numbers stored as text | `df.dtypes`, convert with `astype` |
| Treating the first look as the truth | wrong conclusions | check `describe()` and `isna()` |

## 8. Practice (in order)

1. **NumPy:** make an array of 20 random temperatures; print how many are above the mean and their average.
2. **NumPy:** convert a list of latencies in seconds to milliseconds without a loop.
3. **Pandas:** export any CSV from tools you use (or build one with Day 27) and run the "first look" commands (Block 2).
4. **Pandas:** group it by one column and compute counts and an average; sort the result.
5. **Pandas:** fix missing values in a column in two different ways and compare the effect on the mean.
6. **Matplotlib:** plot your Task 4 result as a bar chart with a title and axis labels.
7. **Mini-project:** take a log CSV (time, level, message), count errors per hour with `groupby`, and plot them as a line chart.

## 9. Self-check

- Why is `array * 2` different from `list * 2`?
- What does `axis=0` mean?
- What is a boolean mask?
- What are the three steps of `groupby`?
- Why must each condition be in parentheses when combining with `&`?
- Which chart type answers "how are my latencies distributed?"

**Next:** Track 2: Web, where you serve data to others over the network.
