"""Day 26 — APIs."""

import requests

def main():
    r = requests.get("https://api.github.com/users/torvalds", timeout=10)
    d = r.json()
    print(d.get("name"), d.get("public_repos"))

if __name__ == "__main__":
    main()