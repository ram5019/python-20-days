# Advanced Python Path

You finished the 20 days. This path has **two parts**:

- **Part A: Core upgrade (Days 21 to 28).** Sharper Python plus the skills every track needs: virtual environments, APIs, CSV/JSON, command-line tools.
- **Part B: Five specialisation tracks.** Pick the ones that match your goals. Each has one lesson and runnable examples.

Same lesson layout as before: **idea, why, analogy, code blocks explained, how the blocks connect, mistakes, practice.**

---

## Part A: Core upgrade (do in order)

| Day | Topic | One-line purpose | Your stub in `advanced/` |
|-----|-------|------------------|--------------------------|
| 21 | Comprehensions | Build lists/dicts/sets in one readable line | `day21_comprehensions.py` |
| 22 | lambda, map, filter | Tiny throwaway functions and data pipelines | `day22_lambda_map_filter.py` |
| 23 | Decorators | Add behaviour to a function without editing it | `day23_decorators.py` |
| 24 | Generators | Process huge data one item at a time | `day24_generators.py` |
| 25 | venv and pip | Keep each project's libraries separate | `day25_venv_notes.py` |
| 26 | APIs with requests | Get live data from other systems | `day26_apis.py` |
| 27 | CSV and JSON | Read and write the two most common data files | `day27_csv_json.py` |
| 28 | Command-line tools | Build a real CLI with `argparse` | `day28_weather_cli.py` |

Lessons: `day21_*.md` to `day28_*.md` in this folder. Examples: `examples/`.

## Part B: Specialisation tracks (pick what you need)

| Track | Libraries | Lesson | Examples (in `examples/`) |
|-------|-----------|--------|---------------------------|
| 📊 Data Science | NumPy, Pandas, Matplotlib | `track1_data_science.md` | `t1_numpy.py`, `t1_pandas.py`, `t1_matplotlib.py` |
| 🌐 Web | Flask, FastAPI, Django | `track2_web.md` | `t2_flask_app.py`, `t2_fastapi_app.py`, `t2_django_notes.md` |
| 🤖 Automation | BeautifulSoup, Selenium | `track3_automation.md` | `t3_beautifulsoup.py`, `t3_selenium.py` |
| 🧠 AI/ML | scikit-learn, PyTorch | `track4_ai_ml.md` | `t4_sklearn.py`, `t4_pytorch.py` |
| ☁️ Cloud/DevOps | boto3, Azure SDK, OCI SDK | `track5_cloud_devops.md` | `t5_boto3.py`, `t5_boto3_mock.py`, `t5_azure.py`, `t5_oci.py` |

**Suggested order if unsure:** Part A first, then Data Science (Pandas is useful everywhere), then whichever track matches your work.

---

## Setup for Part B: virtual environment (Day 25 explains why)

```bash
cd ~/Desktop/python-20-days
python3 -m venv .venv
source .venv/bin/activate

pip install numpy pandas matplotlib          # Track 1
pip install flask fastapi "uvicorn[standard]" httpx   # Track 2 (Django: pip install django)
pip install beautifulsoup4 requests selenium # Track 3
pip install scikit-learn torch               # Track 4 (torch is large)
pip install boto3 "moto[s3,ec2,sts]" oci                  # Track 5: AWS (+ fake AWS for practice), OCI
pip install azure-identity azure-mgmt-resource azure-mgmt-resource-subscriptions azure-mgmt-compute   # Track 5: Azure
```

Install **only what you need for the track you are studying**. Each lesson lists its own libraries at the top.

> Tip: if `pip install torch` fails, check that your Python version is supported at pytorch.org. Very new Python releases sometimes lag behind.

## Safety notes

- Cloud examples (Track 5) **never** contain real credentials. They read credentials from the environment or standard config files. Never paste keys into code or commit them to git.
- Web scraping (Track 3): check a site's terms and `robots.txt` first, and be gentle with request rates.
- Examples that call the network or a cloud account say so at the top of the file.

## How the two parts connect

```
Part A                               Part B
Day 21-24  cleaner, faster code  ──► all tracks (pandas/numpy lean on comprehensions,
                                      generators, decorators in Flask/FastAPI)
Day 25     venv + pip            ──► installing every library below
Day 26     APIs / requests       ──► Web, Automation, Cloud (everything is an API)
Day 27     CSV + JSON            ──► Data Science (pandas reads both), Cloud (JSON everywhere)
Day 28     CLI with argparse     ──► Automation and DevOps scripts
```
