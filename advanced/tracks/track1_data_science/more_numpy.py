"""NumPy: 10 examples, simple to complex.

Run:    python3 advanced/tracks/track1_data_science/more_numpy.py
Needs:  pip install numpy
"""

import numpy as np


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


# ---------------------------------------------------------------
show(1, "Create an array and inspect it")
# WHAT: the basic NumPy object.
# HOW : np.array(list). Every element has the same dtype; shape is the size.
# WHY : arrays are compact and fast; everything else builds on them.
a = np.array([10, 20, 30, 40])
print(a, a.dtype, a.shape, a.ndim, a.size)
print(np.array([1, 2.5, 3]).dtype)            # mixing int and float gives float

# ---------------------------------------------------------------
show(2, "Vectorised arithmetic: no loops")
# WHAT: act on every element at once.
# HOW : operators work element by element. A list would REPEAT instead.
# WHY : shorter code and (for big data) 10 to 100 times faster.
print(a + 5, a * 2, a / 10, a ** 2)
print("list * 2 :", [10, 20] * 2)
print("array * 2:", np.array([10, 20]) * 2)
print(a + np.array([1, 2, 3, 4]))             # element by element

# ---------------------------------------------------------------
show(3, "Indexing and slicing a 1-D array")
# WHAT: pick elements by position.
# HOW : same rules as lists, but a slice is a VIEW (not a copy).
# WHY : a view shares memory, so changing it changes the original.
x = np.arange(10)
print(x[0], x[-1], x[2:5], x[::3], x[::-1][:3])
view = x[2:5]
view[0] = 99
print("original changed through the view:", x)
copy = x[2:5].copy()
copy[0] = -1
print("original after changing a copy:", x[2])

# ---------------------------------------------------------------
show(4, "2-D arrays: rows and columns")
# WHAT: a table of numbers.
# HOW : m[row, col]; ":" means "all"; axis=0 collapses rows (per column),
#       axis=1 collapses columns (per row).
# WHY : spreadsheets and images are 2-D arrays.
m = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])
print(m.shape, m[1, 2], m[:, 0], m[1], m[:2, 1:])
print("column sums:", m.sum(axis=0), "| row sums:", m.sum(axis=1))
print("mean:", m.mean(), "| max per row:", m.max(axis=1))

# ---------------------------------------------------------------
show(5, "Ways to create arrays")
# WHAT: build arrays without typing the numbers.
# HOW : zeros, ones, full, arange, linspace, eye, and seeded random numbers.
# WHY : test data, grids, initial values.
print(np.zeros(3), np.ones((2, 2)), np.full(3, 7))
print(np.arange(0, 10, 3), np.linspace(0, 1, 5))
print(np.eye(3, dtype=int))
rng = np.random.default_rng(0)                 # seeded: same numbers every run
print(rng.integers(1, 7, size=8))
print(rng.random(3).round(3))

# ---------------------------------------------------------------
show(6, "Boolean masks: filter without a loop")
# WHAT: select elements by condition.
# HOW : a comparison gives a True/False array; use it as an index.
#       np.where picks between two values.
# WHY : "all the slow requests" in one line.
latency = np.array([12, 15, 220, 14, 18, 340, 13])
mask = latency > 100
print(mask)
print(latency[mask], "| count:", mask.sum(), "| share:", round(mask.mean(), 2))
print(np.where(latency > 100, "slow", "ok"))
print(latency[(latency > 13) & (latency < 100)])

# ---------------------------------------------------------------
show(7, "Reshape, flatten, transpose, stack")
# WHAT: change the shape without changing the data.
# HOW : reshape (-1 means "work it out"), ravel, .T, vstack/hstack.
# WHY : models and plots need data in particular shapes.
r = np.arange(12)
grid = r.reshape(3, 4)
print(grid)
print(grid.T.shape, grid.ravel()[:5], r.reshape(2, -1).shape)
print(np.vstack([[1, 2], [3, 4]]).tolist(), np.hstack([[1, 2], [3, 4]]).tolist())

# ---------------------------------------------------------------
show(8, "Broadcasting: arrays of different shapes")
# WHAT: combine a table with a row or a column.
# HOW : NumPy stretches the smaller array to fit when the shapes are
#       compatible.
# WHY : normalise columns, subtract averages, scale by factors.
scores = np.array([[80, 90, 70],
                   [60, 85, 95]])
print(scores - scores.mean(axis=0))            # subtract each column's mean
print(scores / scores.max(axis=1, keepdims=True))   # scale each row by its max
print(np.array([[1], [2], [3]]) * np.array([10, 20]))   # multiplication table

# ---------------------------------------------------------------
show(9, "Sorting, searching and summarising")
# WHAT: the toolbox for analysis.
# HOW : sort, argsort, argmax, cumsum, unique with counts, percentile.
# WHY : ranking and distribution questions.
data = np.array([5, 3, 8, 3, 9, 1, 8, 8])
print(np.sort(data), np.argsort(data)[:3])
print("max at", data.argmax(), "| min at", data.argmin())
print(np.cumsum([1, 2, 3, 4]), np.diff([1, 4, 9, 16]))
values, counts = np.unique(data, return_counts=True)
print(dict(zip(values.tolist(), counts.tolist())))
print(np.percentile(data, [25, 50, 75]), data.std().round(2))

# ---------------------------------------------------------------
show(10, "Mini program: analyse a day of request latencies")
# WHAT: statistics, outliers and a moving average on 24 hours of data.
# HOW : combine masks, percentiles and convolution.
# WHY : the standard first look at any metric.
rng = np.random.default_rng(1)
hourly = rng.normal(40, 8, 24).round(1)
hourly[[3, 15]] += [90, 140]                   # two bad hours
print("mean %.1f | median %.1f | p95 %.1f | max %.1f at hour %d" % (
    hourly.mean(), np.median(hourly), np.percentile(hourly, 95), hourly.max(), hourly.argmax()))
outliers = np.where(hourly > hourly.mean() + 2 * hourly.std())[0]
print("outlier hours:", outliers.tolist())
window = 3
moving = np.convolve(hourly, np.ones(window) / window, mode="valid")
print("3-hour moving average (first 5):", moving[:5].round(1))
normalised = (hourly - hourly.min()) / (hourly.max() - hourly.min())
print("normalised range:", normalised.min(), normalised.max())
