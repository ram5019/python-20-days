"""Track 1c example: Matplotlib.

Run:  python3 learning-path/advanced/examples/t1_matplotlib.py
Needs:  pip install matplotlib numpy
Creates PNG charts in a folder called 'charts' next to this script.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")              # draw to files (no window needed)
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).parent / "charts"
OUT.mkdir(exist_ok=True)

# BLOCK 1: the simplest line chart
x = [1, 2, 3, 4, 5]
y = [2, 4, 3, 7, 6]
plt.plot(x, y)
plt.title("My first chart")
plt.xlabel("Day")
plt.ylabel("Tickets")
plt.savefig(OUT / "01_line.png")
plt.close()                        # always close to start fresh

# BLOCK 2: markers, labels and a legend; two lines in one chart
hours = np.arange(0, 24)
read_iops = 100 + 40 * np.sin(hours / 24 * 2 * np.pi) + np.random.default_rng(1).normal(0, 5, 24)
write_iops = 60 + 20 * np.cos(hours / 24 * 2 * np.pi)

plt.figure(figsize=(8, 4))
plt.plot(hours, read_iops, marker="o", label="read")
plt.plot(hours, write_iops, linestyle="--", label="write")
plt.title("IOPS over a day")
plt.xlabel("Hour")
plt.ylabel("IOPS (k)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "02_two_lines.png")
plt.close()

# BLOCK 3: bar chart (compare categories)
sites = ["chn", "sgp", "tyo"]
nodes = [12, 8, 5]
plt.bar(sites, nodes, color=["#4c78a8", "#f58518", "#54a24b"])
plt.title("Nodes per site")
plt.ylabel("Nodes")
plt.savefig(OUT / "03_bar.png")
plt.close()

# BLOCK 4: histogram (distribution of values)
latency = np.random.default_rng(2).gamma(shape=2.0, scale=10.0, size=1000)
plt.hist(latency, bins=30)
plt.axvline(np.percentile(latency, 95), color="red", linestyle="--", label="p95")
plt.title("Latency distribution")
plt.xlabel("ms")
plt.legend()
plt.savefig(OUT / "04_hist.png")
plt.close()

# BLOCK 5: several charts in one figure with subplots (object-oriented style)
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].plot(x, y)
axes[0].set_title("Line")
axes[1].bar(sites, nodes)
axes[1].set_title("Bar")
fig.suptitle("Two charts, one image")
fig.tight_layout()
fig.savefig(OUT / "05_subplots.png")
plt.close(fig)

# BLOCK 6: chart straight from a Pandas DataFrame
import pandas as pd
df = pd.DataFrame({"site": sites, "nodes": nodes})
ax = df.plot(kind="bar", x="site", y="nodes", legend=False, title="From pandas")
ax.figure.savefig(OUT / "06_from_pandas.png")
plt.close(ax.figure)

print("Charts saved in:", OUT)
for p in sorted(OUT.glob("*.png")):
    print("  ", p.name)
