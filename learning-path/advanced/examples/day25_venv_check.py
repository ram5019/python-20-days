"""Day 25 example: inspect your Python environment.

Run it twice and compare the output:
  1) python3 learning-path/advanced/examples/day25_venv_check.py
  2) after:  python3 -m venv .venv && source .venv/bin/activate
             python learning-path/advanced/examples/day25_venv_check.py
"""

import sys
import importlib.metadata as md

# BLOCK 1: which Python is running?
print("Python executable:", sys.executable)
print("Python version   :", sys.version.split()[0])

# BLOCK 2: are we inside a virtual environment?
in_venv = sys.prefix != sys.base_prefix
print("Inside a venv    :", in_venv)
if in_venv:
    print("venv location    :", sys.prefix)

# BLOCK 3: list installed packages (name + version)
packages = sorted(
    ((d.metadata["Name"], d.version) for d in md.distributions()),
    key=lambda p: p[0].lower(),
)
print(f"\n{len(packages)} packages installed")
for name, version in packages[:10]:
    print(f"  {name:<25} {version}")

# BLOCK 4: is a particular library available?
def has_package(name):
    try:
        md.version(name)
        return True
    except md.PackageNotFoundError:
        return False

for lib in ["requests", "pandas", "numpy"]:
    print(f"{lib:<10} installed: {has_package(lib)}")

# BLOCK 5: where does Python look for imports?
print("\nImport search path (first 3):")
for p in sys.path[:3]:
    print("  ", p)
