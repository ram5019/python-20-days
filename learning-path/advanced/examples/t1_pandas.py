"""Track 1b example: Pandas.

Run:  python3 learning-path/advanced/examples/t1_pandas.py
Needs:  pip install pandas
"""

import io
import pandas as pd

# BLOCK 1: build a DataFrame (a table) from a dict of columns
df = pd.DataFrame({
    "node":    ["n1", "n2", "n3", "n4", "n5", "n6"],
    "site":    ["chn", "chn", "sgp", "sgp", "sgp", "chn"],
    "cpu_pct": [35, 91, 48, 77, 95, 22],
    "status":  ["up", "up", "up", "down", "up", "up"],
})
print(df)

# BLOCK 2: first look at any dataset
print(df.shape)                    # (6, 4)
print(df.dtypes)
print(df.describe())               # stats for numeric columns
print(df.head(2))

# BLOCK 3: select columns and rows
print(df["cpu_pct"])               # one column (a Series)
print(df[["node", "cpu_pct"]])     # several columns
print(df.iloc[0])                  # first row by position
print(df.loc[df["node"] == "n3"])  # rows by condition

# BLOCK 4: filtering with conditions (use & | and parentheses)
busy = df[df["cpu_pct"] > 80]
print(busy)
sgp_down = df[(df["site"] == "sgp") & (df["status"] == "down")]
print(sgp_down)

# BLOCK 5: add and change columns (vectorised, no loop)
df["cpu_frac"] = df["cpu_pct"] / 100
df["hot"] = df["cpu_pct"] > 80
print(df[["node", "cpu_frac", "hot"]])

# BLOCK 6: sorting
print(df.sort_values("cpu_pct", ascending=False).head(3))

# BLOCK 7: groupby: the heart of data analysis
print(df.groupby("site")["cpu_pct"].mean())
print(df.groupby("site").agg(nodes=("node", "count"), avg_cpu=("cpu_pct", "mean")))

# BLOCK 8: counting values
print(df["status"].value_counts())            # same job as Day 13's counting loop

# BLOCK 9: read CSV (Day 27) into a DataFrame
csv_text = """time,level,message
10:00,INFO,started
10:05,ERROR,disk full
10:07,ERROR,disk full
10:09,WARN,slow
"""
logs = pd.read_csv(io.StringIO(csv_text))     # normally: pd.read_csv("file.csv")
print(logs["level"].value_counts())

# BLOCK 10: missing data
data = pd.DataFrame({"a": [1, None, 3], "b": ["x", "y", None]})
print(data.isna().sum())                      # missing per column
print(data.fillna({"a": 0, "b": "unknown"}))
print(data.dropna())

# BLOCK 11: write results out
out = df.groupby("site")["cpu_pct"].mean().reset_index()
print(out.to_csv(index=False))                # to_csv("file.csv") writes a file
