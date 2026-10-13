"""Matplotlib: 10 examples, simple to complex.

Run:    python3 advanced/tracks/track1_data_science/more_matplotlib.py
Needs:  pip install matplotlib numpy pandas
Creates 10 PNG charts in a folder called 'charts' next to this file. Open them.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")                     # draw into files; no window needed
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

OUT = Path(__file__).parent / "charts"
OUT.mkdir(exist_ok=True)
rng = np.random.default_rng(3)


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=100)
    plt.close(fig)                        # always close, or figures pile up
    print("  saved", name)


# ---------------------------------------------------------------
show(1, "The simplest line chart")
# WHAT: plot y against x.
# HOW : plt.plot, then title and axis labels. We use fig, ax = plt.subplots(),
#       the object-oriented style recommended for everything.
# WHY : line charts show change over time.
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4, 5], [2, 4, 3, 7, 6])
ax.set_title("Tickets per day")
ax.set_xlabel("Day")
ax.set_ylabel("Tickets")
save(fig, "01_line.png")

# ---------------------------------------------------------------
show(2, "Styles, markers and several lines with a legend")
# WHAT: compare series.
# HOW : label= on each line, then ax.legend(); marker, linestyle, color.
# WHY : a legend turns lines into a story.
hours = np.arange(24)
reads = 100 + 40 * np.sin(hours / 24 * 2 * np.pi)
writes = 60 + 20 * np.cos(hours / 24 * 2 * np.pi)
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(hours, reads, marker="o", markersize=3, label="read IOPS")
ax.plot(hours, writes, linestyle="--", color="tab:red", label="write IOPS")
ax.set(title="IOPS over a day", xlabel="Hour", ylabel="IOPS (k)")
ax.legend()
ax.grid(alpha=0.3)
save(fig, "02_two_lines.png")

# ---------------------------------------------------------------
show(3, "Bar chart: compare categories")
# WHAT: sizes side by side.
# HOW : ax.bar(labels, values); add the numbers on top with bar_label.
# WHY : bars compare categories; lines are for sequences.
sites = ["Paris", "Tokyo", "Austin", "Pune"]
counts = [12, 8, 5, 9]
fig, ax = plt.subplots()
bars = ax.bar(sites, counts, color=["#4c78a8", "#f58518", "#54a24b", "#b279a2"])
ax.bar_label(bars)
ax.set_ylabel("Nodes")
ax.set_title("Nodes per site")
save(fig, "03_bar.png")

# ---------------------------------------------------------------
show(4, "Horizontal bars, sorted")
# WHAT: a ranking that reads easily.
# HOW : barh with the data sorted; long labels fit better horizontally.
# WHY : leaderboards and "top N" charts.
names = ["web01", "db01", "cache02", "queue01", "web02"]
cpu = np.array([40, 85, 22, 61, 15])
order = np.argsort(cpu)
fig, ax = plt.subplots()
ax.barh(np.array(names)[order], cpu[order], color="tab:green")
ax.axvline(80, color="red", linestyle="--", label="alert level")
ax.set_xlabel("CPU %")
ax.legend()
save(fig, "04_barh.png")

# ---------------------------------------------------------------
show(5, "Scatter plot: relationship between two numbers")
# WHAT: does one value follow another?
# HOW : ax.scatter(x, y); colour or size can show a third variable. Add a
#       trend line with polyfit.
# WHY : spotting correlation and outliers.
x = rng.uniform(0, 100, 60)
y = 2.5 * x + rng.normal(0, 20, 60)
size = rng.uniform(10, 120, 60)
fig, ax = plt.subplots()
sc = ax.scatter(x, y, c=y, s=size, cmap="viridis", alpha=0.8)
slope, intercept = np.polyfit(x, y, 1)
ax.plot([0, 100], [intercept, intercept + slope * 100], color="black")
fig.colorbar(sc, label="value")
ax.set(title=f"Slope ≈ {slope:.2f}", xlabel="Load", ylabel="Latency")
save(fig, "05_scatter.png")

# ---------------------------------------------------------------
show(6, "Histogram: how values are spread")
# WHAT: the shape of a distribution.
# HOW : ax.hist(data, bins=...); mark the mean and the 95th percentile.
# WHY : averages hide the tail; the histogram shows it.
latency = rng.gamma(shape=2.0, scale=10.0, size=2000)
fig, ax = plt.subplots()
ax.hist(latency, bins=40, color="tab:blue", alpha=0.8)
ax.axvline(latency.mean(), color="orange", label=f"mean {latency.mean():.0f}")
ax.axvline(np.percentile(latency, 95), color="red", linestyle="--", label="p95")
ax.set(title="Latency distribution", xlabel="ms")
ax.legend()
save(fig, "06_hist.png")

# ---------------------------------------------------------------
show(7, "Several charts in one figure")
# WHAT: a grid of panels.
# HOW : plt.subplots(rows, cols) returns an array of axes.
# WHY : show related views together.
fig, axes = plt.subplots(2, 2, figsize=(9, 6))
axes[0, 0].plot(hours, reads)
axes[0, 0].set_title("Line")
axes[0, 1].bar(sites, counts)
axes[0, 1].set_title("Bar")
axes[1, 0].hist(latency, bins=30)
axes[1, 0].set_title("Histogram")
axes[1, 1].scatter(x, y, s=10)
axes[1, 1].set_title("Scatter")
fig.suptitle("Four views")
save(fig, "07_subplots.png")

# ---------------------------------------------------------------
show(8, "Annotations: point at what matters")
# WHAT: label a spike on the chart.
# HOW : ax.annotate with an arrow; ax.axhspan shades a range.
# WHY : a chart should tell the reader where to look.
series = 50 + rng.normal(0, 4, 48)
series[30] = 120
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(series)
ax.axhspan(40, 60, color="green", alpha=0.1, label="normal range")
ax.annotate("incident", xy=(30, 120), xytext=(36, 105),
            arrowprops={"arrowstyle": "->", "color": "red"})
ax.legend()
ax.set(title="Response time", xlabel="Half-hour", ylabel="ms")
save(fig, "08_annotated.png")

# ---------------------------------------------------------------
show(9, "Stacked bars and a box plot")
# WHAT: parts of a whole; spread per group.
# HOW : bar(..., bottom=...) stacks; boxplot shows median and quartiles.
# WHY : two more standard chart types.
ok = np.array([20, 25, 22, 30])
warn = np.array([3, 5, 2, 6])
err = np.array([1, 2, 4, 1])
days = ["Mon", "Tue", "Wed", "Thu"]
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4))
ax1.bar(days, ok, label="ok")
ax1.bar(days, warn, bottom=ok, label="warn")
ax1.bar(days, err, bottom=ok + warn, label="error")
ax1.legend()
ax1.set_title("Events per day")
groups = [rng.normal(m, 6, 80) for m in (40, 55, 48)]
ax2.boxplot(groups, tick_labels=["web", "db", "cache"])
ax2.set_title("Latency by tier")
save(fig, "09_stacked_box.png")

# ---------------------------------------------------------------
show(10, "Mini program: a dashboard straight from a DataFrame")
# WHAT: Pandas data to a finished multi-panel report image.
# HOW : df.plot draws onto axes you provide; styling is set once.
# WHY : the usual path: load -> group -> plot -> share.
df = pd.DataFrame({
    "day": pd.date_range("2026-10-01", periods=14),
    "requests": (1000 + 200 * np.sin(np.arange(14) / 2) + rng.normal(0, 40, 14)).round(),
    "errors": rng.poisson(8, 14),
})
df["error_rate"] = df["errors"] / df["requests"] * 100
fig, axes = plt.subplots(1, 3, figsize=(13, 3.8))
df.plot(x="day", y="requests", ax=axes[0], legend=False, title="Requests")
df.plot(x="day", y="error_rate", ax=axes[1], legend=False, color="red", title="Error rate %")
df["errors"].plot(kind="hist", ax=axes[2], bins=6, title="Errors per day")
for ax in axes[:2]:
    ax.tick_params(axis="x", rotation=45)
save(fig, "10_dashboard.png")

print("\nAll charts are in:", OUT)
