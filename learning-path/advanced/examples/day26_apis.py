"""Day 26 example: calling a web API with requests.

NOTE: this makes real network calls to GitHub's public API (no login needed).
Run:  python3 learning-path/advanced/examples/day26_apis.py
Needs:  pip install requests
"""

import requests

BASE = "https://api.github.com"

# BLOCK 1: the simplest GET request
response = requests.get(f"{BASE}/users/torvalds", timeout=10)
print("Status:", response.status_code)            # 200 = OK
print("Content-Type:", response.headers["Content-Type"])

# BLOCK 2: parse the JSON body (Day 19: JSON text -> dict)
user = response.json()
print(user["name"], "|", user["public_repos"], "repos")

# BLOCK 3: query parameters: let requests build the ?a=b part
resp = requests.get(
    f"{BASE}/search/repositories",
    params={"q": "language:python stars:>100000", "sort": "stars", "per_page": 3},
    timeout=10,
)
print("URL actually called:", resp.url)
for repo in resp.json()["items"]:
    print(f"  {repo['full_name']:<35} {repo['stargazers_count']:>7} stars")

# BLOCK 4: custom headers (APIs often want these)
resp = requests.get(
    f"{BASE}/repos/python/cpython",
    headers={"Accept": "application/vnd.github+json"},
    timeout=10,
)
print("cpython default branch:", resp.json()["default_branch"])

# BLOCK 5: handle failures properly (Day 16)
def get_json(url, **kwargs):
    """GET a URL and return parsed JSON, or None if anything goes wrong."""
    try:
        r = requests.get(url, timeout=10, **kwargs)
        r.raise_for_status()                      # turns 4xx/5xx into an exception
        return r.json()
    except requests.exceptions.HTTPError as e:
        print("HTTP error:", e)
    except requests.exceptions.Timeout:
        print("Request timed out")
    except requests.exceptions.ConnectionError:
        print("Could not connect (network down?)")
    return None

print(get_json(f"{BASE}/users/this-user-should-not-exist-98765"))   # 404 -> None

# BLOCK 6: a small reusable function (Day 14) built on Block 5
def repo_summary(owner, name):
    data = get_json(f"{BASE}/repos/{owner}/{name}")
    if data is None:
        return "not available"
    return f"{data['full_name']}: {data['stargazers_count']} stars, {data['open_issues_count']} open issues"

print(repo_summary("psf", "requests"))

# BLOCK 7: sending data (POST) shown against a safe echo service
# json= sends a dict as a JSON body (Day 19: dict -> JSON text)
echo = requests.post("https://httpbin.org/post", json={"name": "Ram", "role": "TSE"}, timeout=10)
print("Server received:", echo.json().get("json"))
