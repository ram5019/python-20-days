# Day 25: Virtual Environments and pip

**Example:** `examples/day25_venv_check.py` | **Your stub:** `advanced/day25_venv_notes.py`

---

## 1. The big idea

- **pip** installs third-party libraries (`pip install requests`).
- A **virtual environment (venv)** is a **private folder of libraries for one project**, so projects do not interfere with each other or with your system Python.

## 2. Why does it exist?

Project A needs `requests 2.25`. Project B needs `requests 2.34`. Installing both globally is impossible: one overwrites the other. Also, installing everything into your system Python can break tools your operating system relies on.

A venv solves this: **one environment per project**, each with exactly the versions that project needs. You can delete it and recreate it any time without risk. It also lets you **record** the exact libraries (`requirements.txt`) so a teammate, or a server, can recreate the same setup.

This matters for **every** track in Part B.

## 3. Simple way to understand

A **separate toolbox per job**.

- System Python = the shared toolbox in the garage that everyone uses and no one dares reorganise.
- A venv = a **personal toolbox for this project** with only the tools it needs.
- `pip install` = buy a tool and put it **in the active toolbox**.
- `activate` = pick up that toolbox. `deactivate` = put it down.

## 4. How it works: the commands

```bash
cd ~/Desktop/python-20-days
python3 -m venv .venv             # 1. create (once)
source .venv/bin/activate         # 2. activate (every new terminal)
                                  #    prompt now shows (.venv)
pip install requests              # 3. install into THIS venv only
pip list                          # see what's installed
pip freeze > requirements.txt     # 4. record exact versions
pip install -r requirements.txt   # 5. recreate elsewhere
deactivate                        # 6. leave the venv
```

| Command | Meaning |
|---------|---------|
| `python3 -m venv .venv` | create an environment in folder `.venv` |
| `source .venv/bin/activate` | macOS/Linux activation (Windows: `.venv\Scripts\activate`) |
| `pip install name` | install |
| `pip install name==1.2.3` | install a specific version |
| `pip uninstall name` | remove |
| `pip freeze` | list exact versions |

Add `.venv/` to `.gitignore`. A venv is **not committed**; `requirements.txt` is.

## 5. Code walkthrough, block by block

### Block 1: which Python?
`sys.executable` is the path of the interpreter running your script. Outside a venv it is something like `/usr/bin/python3`; inside one it points into `.venv/bin/`. This one line answers "am I using the Python I think I am?", the most common source of "but it's installed!" confusion.

### Block 2: inside a venv?
Inside a venv, `sys.prefix` (the environment) differs from `sys.base_prefix` (the original installation). The comparison gives a True/False (Day 5), and the `if` (Day 6) prints the location only when relevant.

### Block 3: installed packages
`importlib.metadata.distributions()` lists everything installed in **the current environment**. The generator expression (Day 24) pulls out name/version pairs and `sorted(..., key=lambda ...)` (Day 22) orders them case-insensitively. Run this inside a fresh venv and you will see only a couple of packages (pip and friends), proving the isolation.

### Block 4: availability check
`md.version(name)` raises `PackageNotFoundError` if the package is absent. The function wraps it in `try/except` (Day 16) and returns True/False. Useful at the top of a script: "is the library I need installed?"

### Block 5: the import path
`sys.path` is the list of folders Python searches when you `import` something (Day 17). The venv's `site-packages` appears there when active, which is how `import requests` finds the right copy.

## 6. How the blocks connect

```
Block 1  which interpreter?
Block 2  is it a venv's?
Block 3  what is installed there?
Block 4  is a specific library there?
Block 5  how imports find it
```

All five are different views of one fact: **"the active environment decides what you can import."**

## 7. Common mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| Installing without activating | libraries go to system Python | check the `(.venv)` prompt |
| `ModuleNotFoundError` though you installed it | different Python/venv | `which python`, `python -m pip install ...` |
| Committing `.venv/` to git | huge repo | add to `.gitignore` |
| Moving/renaming the venv folder | broken paths | delete and recreate it |
| Forgetting `requirements.txt` | teammate cannot reproduce | `pip freeze > requirements.txt` |
| Mixing `pip` and `pip3` from different Pythons | wrong install target | use `python -m pip ...` |

## 8. Practice

1. Create a venv in a scratch folder, activate it, run `day25_venv_check.py`, then run it again after `deactivate`. Compare.
2. Install `requests`, then check it with `has_package("requests")`.
3. Create `requirements.txt` with `pip freeze`, delete the venv, recreate it and reinstall from the file.
4. Install a specific older version (`pip install requests==2.31.0`), verify with `pip list`, then upgrade.
5. Open your stub `day25_venv_notes.py` and write your own cheat sheet of these commands.

## 9. Self-check

- What problem does a venv solve?
- What does `activate` change?
- Why is `requirements.txt` committed but `.venv/` is not?
- How can you tell which Python is running a script?

**Next:** Day 26: use your new `requests` library to talk to live web services (APIs).
