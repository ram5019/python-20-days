"""Day 25: Virtual environments and pip. 10 examples, simple to complex.

Run:  python3 advanced/day25_venv_pip/more_examples.py

Nothing here installs packages or uses the network. The examples inspect your
environment and create a throwaway virtual environment in a temp folder.
"""

import importlib.metadata as md
import importlib.util
import platform
import sys
import tempfile
import venv
from pathlib import Path


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


# ---------------------------------------------------------------
show(1, "Which Python is running this?")
# WHAT: the interpreter's path and version.
# HOW : sys.executable and sys.version_info.
# WHY : "it's installed!" problems are usually "different Python" problems.
print("Executable:", Path(sys.executable).name, "in", Path(sys.executable).parent.name)
print("Version   :", sys.version.split()[0])
print("At least 3.9?", sys.version_info >= (3, 9))

# ---------------------------------------------------------------
show(2, "Am I inside a virtual environment?")
# WHAT: detect an active venv.
# HOW : inside a venv, sys.prefix (the venv) differs from sys.base_prefix
#       (the Python it was built from).
# WHY : your scripts can warn you before you install into the wrong place.
in_venv = sys.prefix != sys.base_prefix
print("Inside a venv:", in_venv)
print("Environment folder name:", Path(sys.prefix).name)

# ---------------------------------------------------------------
show(3, "The platform you are on")
# WHAT: operating system and CPU details.
# HOW : the platform module.
# WHY : activation commands and library wheels differ per platform.
print(platform.system(), platform.machine())
activate = (r".venv\Scripts\activate" if platform.system() == "Windows"
            else "source .venv/bin/activate")
print("Activate with:", activate)

# ---------------------------------------------------------------
show(4, "List installed packages")
# WHAT: what is available in THIS environment.
# HOW : importlib.metadata.distributions().
# WHY : the same list `pip list` prints, but usable in code.
packages = sorted(
    {(d.metadata["Name"], d.version) for d in md.distributions() if d.metadata["Name"]},
    key=lambda p: p[0].lower(),
)
print(len(packages), "packages installed; first five:")
for name, version in packages[:5]:
    print(f"  {name:<24} {version}")

# ---------------------------------------------------------------
show(5, "Is a package installed, and which version?")
# WHAT: check before you import.
# HOW : md.version(name) raises PackageNotFoundError when missing.
# WHY : give a friendly message instead of a traceback.
def installed_version(name):
    try:
        return md.version(name)
    except md.PackageNotFoundError:
        return None


for lib in ("pip", "requests", "definitely-not-a-package"):
    print(f"{lib:<26}", installed_version(lib) or "not installed")

# ---------------------------------------------------------------
show(6, "Where do imports come from?")
# WHAT: the folders Python searches, and where a module lives.
# HOW : sys.path is the search list; importlib.util.find_spec finds a module
#       without importing it.
# WHY : "which copy am I importing?" is a classic debugging question.
for p in sys.path[:3]:
    print("  search path:", Path(p).name or p)
spec = importlib.util.find_spec("json")
print("json comes from:", Path(spec.origin).parent.name + "/" + Path(spec.origin).name)
print("a missing module:", importlib.util.find_spec("no_such_module_xyz"))

# ---------------------------------------------------------------
show(7, "Create a virtual environment with code")
# WHAT: what `python3 -m venv .venv` actually builds.
# HOW : venv.create(folder, with_pip=False) in a temp folder (fast, offline).
# WHY : a venv is just a folder with a copy/link of Python and a library dir.
with tempfile.TemporaryDirectory() as folder:
    env = Path(folder) / ".venv"
    venv.create(env, with_pip=False)
    print("top level:", sorted(p.name for p in env.iterdir()))
    config = (env / "pyvenv.cfg").read_text().splitlines()
    print("pyvenv.cfg has", len(config), "lines; first:", config[0].split("=")[0].strip())
    bin_dir = "Scripts" if platform.system() == "Windows" else "bin"
    print(f"{bin_dir}/ contains:", sorted(p.name for p in (env / bin_dir).iterdir())[:4], "...")

# ---------------------------------------------------------------
show(8, "Parse a requirements.txt")
# WHAT: read the format pip uses to record dependencies.
# HOW : skip comments and blank lines; split name from version rule.
# WHY : understanding the format lets you check and manage it with code.
REQUIREMENTS = """
# web stack
requests==2.31.0
flask>=3.0      # minimum version
numpy
pandas[excel]~=2.1
"""


def parse_requirements(text):
    result = []
    for line in text.splitlines():
        line = line.split("#")[0].strip()
        if not line:
            continue
        for op in ("==", ">=", "~=", "<=", ">", "<"):
            if op in line:
                name, version = line.split(op, 1)
                result.append((name.split("[")[0].strip(), op, version.strip()))
                break
        else:
            result.append((line.split("[")[0], None, None))
    return result


for item in parse_requirements(REQUIREMENTS):
    print(" ", item)

# ---------------------------------------------------------------
show(9, "Compare requirements with what is installed")
# WHAT: report missing packages and version mismatches.
# HOW : combine Example 5 (installed_version) and Example 8 (parsing).
# WHY : the heart of a "does my environment match the project?" check.
def check(requirements):
    report = []
    for name, op, wanted in requirements:
        have = installed_version(name)
        if have is None:
            report.append(f"MISSING   {name}")
        elif op == "==" and have != wanted:
            report.append(f"MISMATCH  {name}: have {have}, need =={wanted}")
        else:
            report.append(f"ok        {name} {have}")
    return report


print("\n".join(check([("pip", None, None), ("not-installed-pkg", "==", "1.0")])))

# ---------------------------------------------------------------
show(10, "Mini program: an environment doctor")
# WHAT: one report summarising Python, venv state and key libraries.
# HOW : reuse the helpers from earlier examples; end with advice.
# WHY : the first thing to run when someone says "it works on my machine".
def doctor(wanted=("pip", "requests", "numpy")):
    lines = [
        f"Python {sys.version.split()[0]} on {platform.system()}",
        f"Virtual environment: {'YES' if sys.prefix != sys.base_prefix else 'NO'}",
    ]
    missing = [lib for lib in wanted if installed_version(lib) is None]
    for lib in wanted:
        lines.append(f"  {lib:<10} {installed_version(lib) or '-'}")
    if sys.prefix == sys.base_prefix:
        lines.append("Advice: create and activate a venv before installing anything.")
    if missing:
        lines.append("Advice: pip install " + " ".join(missing))
    return "\n".join(lines)


print(doctor())
