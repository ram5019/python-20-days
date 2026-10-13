"""Pandas: 10 examples, simple to complex.

Run:    python3 advanced/tracks/track1_data_science/more_pandas.py
Needs:  pip install pandas
"""

import io

import pandas as pd


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


# A small dataset used by several examples
nodes = pd.DataFrame({
    "node": ["n1", "n2", "n3", "n4", "n5", "n6"],
    "site": ["par", "par", "tyo", "tyo", "tyo", "par"],
    "cpu": [35, 91, 48, 77, 95, 22],
    "status": ["up", "up", "up", "down", "up", "up"],
})

# ---------------------------------------------------------------
show(1, "A DataFrame is a table")
# WHAT: build one and look at it.
# HOW : pd.DataFrame from a dict of columns. Each column is a Series.
# WHY : the central Pandas object.
print(nodes)
print(type(nodes["cpu"]).__name__, nodes.shape)

# ---------------------------------------------------------------
show(2, "First look at any dataset")
# WHAT: the five commands to run on new data.
# HOW : head, shape, dtypes, describe, info/isna.
# WHY : know what you have before analysing it.
print(nodes.head(3))
print(nodes.dtypes.to_dict())
print(nodes.describe().round(1))
print(nodes.isna().sum().to_dict())

# ---------------------------------------------------------------
show(3, "Select columns and rows")
# WHAT: pick what you need.
# HOW : df["col"], df[["a","b"]]; .iloc by position; .loc by label/condition.
# WHY : the three selection styles cover everything.
print(nodes["node"].tolist())
print(nodes[["node", "cpu"]].head(2))
print(nodes.iloc[0].to_dict())
print(nodes.loc[nodes["node"] == "n3", ["node", "cpu"]])

# ---------------------------------------------------------------
show(4, "Filter rows with conditions")
# WHAT: keep rows that match.
# HOW : a True/False Series as the index. Combine with & | ~ and put EACH
#       condition in parentheses (not and/or).
# WHY : the Pandas version of "loop, test, append".
print(nodes[nodes["cpu"] > 80])
print(nodes[(nodes["site"] == "tyo") & (nodes["status"] == "up")]["node"].tolist())
print(nodes[nodes["site"].isin(["par"]) | (nodes["cpu"] > 90)]["node"].tolist())
print(nodes.query("cpu < 50 and status == 'up'")["node"].tolist())

# ---------------------------------------------------------------
show(5, "Create and change columns")
# WHAT: derived columns, with no loop.
# HOW : operate on whole columns; map/apply for custom logic; assign with
#       df["new"] = ...
# WHY : feature building and cleaning.
df = nodes.copy()
df["cpu_frac"] = df["cpu"] / 100
df["hot"] = df["cpu"] > 80
df["site_upper"] = df["site"].str.upper()
df["tier"] = df["cpu"].apply(lambda c: "high" if c > 80 else "normal")
df.loc[df["status"] == "down", "cpu"] = 0
print(df[["node", "cpu", "hot", "site_upper", "tier"]])

# ---------------------------------------------------------------
show(6, "Sort, rank and take the top N")
# WHAT: order the rows.
# HOW : sort_values (several columns allowed); nlargest; rank.
# WHY : "the 3 busiest nodes".
print(nodes.sort_values("cpu", ascending=False).head(3)[["node", "cpu"]])
print(nodes.sort_values(["site", "cpu"], ascending=[True, False])["node"].tolist())
print(nodes.nlargest(2, "cpu")["node"].tolist())

# ---------------------------------------------------------------
show(7, "groupby: split, apply, combine")
# WHAT: statistics per category.
# HOW : group by a column, then aggregate. agg gives named outputs.
# WHY : the core of data analysis.
print(nodes.groupby("site")["cpu"].mean().round(1))
print(nodes.groupby("site").agg(nodes=("node", "count"),
                                avg_cpu=("cpu", "mean"),
                                max_cpu=("cpu", "max")).round(1))
print(nodes.groupby(["site", "status"]).size())

# ---------------------------------------------------------------
show(8, "Counting values and cross-tabulating")
# WHAT: frequency tables.
# HOW : value_counts for one column; crosstab/pivot_table for two.
# WHY : replaces the manual counting loop of Day 13.
print(nodes["status"].value_counts().to_dict())
print(pd.crosstab(nodes["site"], nodes["status"]))
print(nodes.pivot_table(index="site", columns="status", values="cpu", aggfunc="mean"))

# ---------------------------------------------------------------
show(9, "Read data, fix missing values, merge tables")
# WHAT: the realistic pipeline start.
# HOW : read_csv (here from text); fillna/dropna; merge joins two tables on
#       a key.
# WHY : real data has gaps and lives in several files.
csv_text = """node,owner,rack
n1,ana,A1
n2,,A1
n3,li,B2
n9,sam,C3
"""
owners = pd.read_csv(io.StringIO(csv_text))
print(owners.isna().sum().to_dict())
owners["owner"] = owners["owner"].fillna("unassigned")
merged = nodes.merge(owners, on="node", how="left")
print(merged[["node", "cpu", "owner", "rack"]])
print("nodes without an owner row:", merged[merged["rack"].isna()]["node"].tolist())
print(nodes.merge(owners, on="node", how="inner").shape)

# ---------------------------------------------------------------
show(10, "Mini program: a cluster report")
# WHAT: load, clean, summarise and export in one flow.
# HOW : chain the earlier steps; write the result to CSV text.
# WHY : a typical "turn raw data into a table someone can read" task.
events = pd.read_csv(io.StringIO("""time,node,level
2026-10-13 09:00,n1,INFO
2026-10-13 09:05,n2,ERROR
2026-10-13 09:07,n2,ERROR
2026-10-13 10:15,n4,ERROR
2026-10-13 10:20,n5,WARN
2026-10-13 11:02,n2,ERROR
"""), parse_dates=["time"])
events["hour"] = events["time"].dt.hour
errors = events[events["level"] == "ERROR"]
per_node = (errors.groupby("node").size().rename("errors").reset_index()
            .merge(nodes[["node", "site", "cpu"]], on="node")
            .sort_values("errors", ascending=False))
print(per_node)
print("errors per hour:", errors.groupby("hour").size().to_dict())
print(per_node.to_csv(index=False))
