"""Day 26: APIs with requests. 10 examples, simple to complex.

Run:  python3 advanced/day26_apis/more_examples.py
Needs:  pip install requests

To keep the examples repeatable and offline, this file starts a small API
server on your own computer (127.0.0.1) and the examples call THAT server.
The requests code is exactly what you would write against a real API: only
the address changes (BASE below).
"""

import json
import re
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

try:
    import requests
except ImportError:
    raise SystemExit("This file needs requests:  pip install requests")

USERS = [
    {"id": 1, "name": "Asha", "role": "admin"},
    {"id": 2, "name": "Ravi", "role": "dev"},
    {"id": 3, "name": "Meena", "role": "dev"},
    {"id": 4, "name": "Li", "role": "ops"},
    {"id": 5, "name": "John", "role": "dev"},
]
FLAKY_CALLS = {"n": 0}


# ----------------------- the pretend API (not part of the lesson) ----------
class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def send_json(self, code, payload, headers=None):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        for key, value in (headers or {}).items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url = urlparse(self.path)
        query = parse_qs(url.query)
        if url.path == "/users":
            page = int(query.get("page", ["1"])[0])
            start = (page - 1) * 2
            self.send_json(200, {"page": page, "items": USERS[start:start + 2],
                                 "has_next": start + 2 < len(USERS)})
        elif re.fullmatch(r"/users/\d+", url.path):
            uid = int(url.path.split("/")[-1])
            match = [u for u in USERS if u["id"] == uid]
            self.send_json(200, match[0]) if match else self.send_json(404, {"error": "no such user"})
        elif url.path == "/search":
            q = query.get("q", [""])[0].lower()
            role = query.get("role", [None])[0]
            found = [u for u in USERS if q in u["name"].lower() and (not role or u["role"] == role)]
            self.send_json(200, {"count": len(found), "items": found})
        elif url.path == "/secure":
            if self.headers.get("Authorization") == "Bearer demo-token":
                self.send_json(200, {"secret": "the answer is 42"})
            else:
                self.send_json(401, {"error": "missing or bad token"})
        elif url.path == "/slow":
            time.sleep(1.0)
            self.send_json(200, {"ok": True})
        elif url.path == "/flaky":
            FLAKY_CALLS["n"] += 1
            if FLAKY_CALLS["n"] < 3:
                self.send_json(503, {"error": "try later"}, {"Retry-After": "0"})
            else:
                self.send_json(200, {"ok": True, "after_calls": FLAKY_CALLS["n"]})
        elif url.path.startswith("/status/"):
            self.send_json(int(url.path.split("/")[-1]), {"status": url.path.split("/")[-1]})
        else:
            self.send_json(404, {"error": "unknown path"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        data = json.loads(self.rfile.read(length) or b"{}")
        if self.path == "/users":
            if not data.get("name"):
                self.send_json(400, {"error": "name is required"})
            else:
                new = {"id": len(USERS) + 100, "name": data["name"], "role": data.get("role", "dev")}
                self.send_json(201, new)
        else:
            self.send_json(200, {"received": data, "content_type": self.headers.get("Content-Type")})


server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
threading.Thread(target=server.serve_forever, daemon=True).start()
BASE = f"http://127.0.0.1:{server.server_address[1]}"
# ---------------------------------------------------------------------------


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


# ---------------------------------------------------------------
show(1, "The simplest GET request")
# WHAT: ask a server for data.
# HOW : requests.get(url) returns a Response object; .status_code tells how
#       it went (200 = OK).
# WHY : every API call starts here.
r = requests.get(f"{BASE}/users/1", timeout=5)
print(r.status_code, r.ok)
print(r.headers["Content-Type"])
print(r.text)

# ---------------------------------------------------------------
show(2, "Parse the JSON body")
# WHAT: turn the reply into a Python dict.
# HOW : r.json() does Day 19's json.loads for you.
# WHY : you work with dicts and lists, not raw text.
user = r.json()
print(type(user).__name__, user["name"], user["role"])
users = requests.get(f"{BASE}/users", timeout=5).json()
print([u["name"] for u in users["items"]], "| more pages:", users["has_next"])

# ---------------------------------------------------------------
show(3, "Query parameters with params=")
# WHAT: filter and page the results.
# HOW : params={...} becomes ?q=...&role=... with correct encoding.
# WHY : never build query strings by hand.
r = requests.get(f"{BASE}/search", params={"q": "a", "role": "dev"}, timeout=5)
print("URL called:", r.url.replace(BASE, ""))
print([u["name"] for u in r.json()["items"]])

# ---------------------------------------------------------------
show(4, "Status code families")
# WHAT: see what different codes look like.
# HOW : the server returns whatever code you ask for at /status/<code>.
# WHY : 2xx success, 4xx YOUR mistake, 5xx THEIR problem.
for code in (200, 201, 400, 401, 404, 429, 500, 503):
    r = requests.get(f"{BASE}/status/{code}", timeout=5)
    family = {2: "success", 4: "client error", 5: "server error"}[r.status_code // 100]
    print(f"{r.status_code} ok={r.ok!s:<5} {family}")

# ---------------------------------------------------------------
show(5, "Handle errors with raise_for_status")
# WHAT: turn error codes into exceptions.
# HOW : r.raise_for_status() raises HTTPError for 4xx/5xx; catch it (Day 16).
# WHY : one try/except covers every failure code.
def get_json(url, **kwargs):
    try:
        r = requests.get(url, timeout=5, **kwargs)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as e:
        print("  HTTP error:", e.response.status_code, e.response.json().get("error"))
    except requests.exceptions.ConnectionError:
        print("  could not connect")
    return None


print(get_json(f"{BASE}/users/2"))
print(get_json(f"{BASE}/users/999"))

# ---------------------------------------------------------------
show(6, "Headers and authentication")
# WHAT: send a token the API requires.
# HOW : headers={"Authorization": "Bearer <token>"}.
# WHY : real APIs identify you this way. Read the token from an environment
#       variable; never hard-code real secrets.
print(get_json(f"{BASE}/secure"))
print(get_json(f"{BASE}/secure", headers={"Authorization": "Bearer demo-token"}))

# ---------------------------------------------------------------
show(7, "POST: send data")
# WHAT: create something on the server.
# HOW : json={...} sends a JSON body and sets the right header.
#       201 means "created".
# WHY : GET reads; POST creates. PUT/PATCH update; DELETE removes.
r = requests.post(f"{BASE}/users", json={"name": "Sam", "role": "ops"}, timeout=5)
print(r.status_code, r.json())
r = requests.post(f"{BASE}/users", json={"role": "ops"}, timeout=5)
print(r.status_code, r.json())
r = requests.post(f"{BASE}/echo", json={"x": [1, 2]}, timeout=5)
print(r.json())

# ---------------------------------------------------------------
show(8, "Timeouts: never wait forever")
# WHAT: give up on a slow server.
# HOW : timeout=seconds; catch requests.exceptions.Timeout.
# WHY : without a timeout, a stuck server can freeze your program.
try:
    requests.get(f"{BASE}/slow", timeout=0.3)
except requests.exceptions.Timeout:
    print("Timed out after 0.3 s, as intended")

# ---------------------------------------------------------------
show(9, "Pagination: collect every page")
# WHAT: fetch all items when the API returns a few at a time.
# HOW : loop while has_next is True.
# WHY : most list endpoints are paged.
def fetch_all_users():
    page, everyone = 1, []
    while True:
        data = get_json(f"{BASE}/users", params={"page": page})
        everyone.extend(data["items"])
        if not data["has_next"]:
            return everyone
        page += 1


all_users = fetch_all_users()
print(len(all_users), [u["name"] for u in all_users])

# ---------------------------------------------------------------
show(10, "Mini program: a reusable API client with a Session and retries")
# WHAT: one object for all calls to an API.
# HOW : a Session reuses the connection and default headers; the client
#       retries temporary failures (503/429) a few times.
# WHY : this is how real SDKs for APIs are structured.
class ApiClient:
    def __init__(self, base_url, token=None, retries=3):
        self.base_url = base_url
        self.retries = retries
        self.session = requests.Session()
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"

    def get(self, path, **params):
        for attempt in range(1, self.retries + 1):
            r = self.session.get(self.base_url + path, params=params, timeout=5)
            if r.status_code in (429, 503) and attempt < self.retries:
                print(f"  attempt {attempt}: got {r.status_code}, retrying")
                time.sleep(0.05)
                continue
            r.raise_for_status()
            return r.json()

    def user_names(self, role):
        return [u["name"] for u in self.get("/search", q="", role=role)["items"]]


client = ApiClient(BASE, token="demo-token")
print(client.get("/flaky"))
print(client.get("/secure"))
print("devs:", client.user_names("dev"))

server.shutdown()
