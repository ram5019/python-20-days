"""Track 1a example: NumPy.

Run:  python3 learning-path/advanced/examples/t1_numpy.py
Needs:  pip install numpy
"""

import numpy as np

# BLOCK 1: create arrays
a = np.array([10, 20, 30, 40])
print(a, a.dtype, a.shape)                # [10 20 30 40] int64 (4,)

# BLOCK 2: math on the WHOLE array at once (no loop!)
print(a + 5)                              # [15 25 35 45]
print(a * 2)                              # [20 40 60 80]
print(a / 10)                             # [1. 2. 3. 4.]
# compare with a plain list: [10, 20] * 2 repeats the list instead of doubling values

# BLOCK 3: array vs list speed
import time
big_list = list(range(2_000_000))
big_arr = np.arange(2_000_000)

t = time.perf_counter()
_ = [x * 2 for x in big_list]
list_time = time.perf_counter() - t

t = time.perf_counter()
_ = big_arr * 2
numpy_time = time.perf_counter() - t
print(f"list: {list_time:.4f}s   numpy: {numpy_time:.4f}s")

# BLOCK 4: useful constructors
print(np.zeros(3))                        # [0. 0. 0.]
print(np.ones((2, 3)))                    # 2 rows, 3 columns of 1.0
print(np.arange(0, 10, 2))                # [0 2 4 6 8]
print(np.linspace(0, 1, 5))               # 5 evenly spaced values from 0 to 1

# BLOCK 5: 2-D arrays (matrices / tables)
m = np.array([[1, 2, 3],
              [4, 5, 6]])
print(m.shape)                            # (2, 3)
print(m[1, 2])                            # row 1, column 2 -> 6
print(m[:, 0])                            # all rows, column 0 -> [1 4]

# BLOCK 6: statistics along an axis
print(m.sum(), m.mean())                  # 21 3.5
print(m.sum(axis=0))                      # per column [5 7 9]
print(m.sum(axis=1))                      # per row    [ 6 15]

# BLOCK 7: boolean masks (filter without a loop)
latency_ms = np.array([12, 15, 220, 14, 18, 340, 13])
slow = latency_ms > 100
print(slow)                               # [False False  True ...]
print(latency_ms[slow])                   # [220 340]
print("slow count:", slow.sum())          # True counts as 1

# BLOCK 8: real-world statistics
print("mean  :", latency_ms.mean())
print("median:", np.median(latency_ms))
print("p95   :", np.percentile(latency_ms, 95))
print("max   :", latency_ms.max(), "at index", latency_ms.argmax())

# BLOCK 9: reshape
r = np.arange(12).reshape(3, 4)
print(r)
