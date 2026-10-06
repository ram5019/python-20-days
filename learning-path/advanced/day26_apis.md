# Day 26: APIs with `requests`

**Example:** `examples/day26_apis.py` | **Your stub:** `advanced/day26_apis.py` | **Needs:** `pip install requests`

---

## 1. The big idea

An **API** (Application Programming Interface) is a way for one program to **ask another program for data or actions** over the network. Most web APIs work like this:

```
your program ──HTTP request──►  server
your program ◄──HTTP response──  server   (usually JSON, Day 19)
```

`requests` is the Python library that makes sending these requests simple.

## 2. Why does it exist?

Almost everything has an API: weather, GitHub, Slack, cloud providers, storage clusters, ticketing systems. Instead of clicking through a website, your code can **fetch, create and automate** at any scale. For Part B, **Web, Automation and Cloud all rely on this skill**.

## 3. Simple way to understand

A **restaurant**.

- You (the client) sit at the table and place an **order** (request).
- The **menu** is the API documentation: it lists what you may ask for.
- The kitchen (server) prepares it and the waiter brings back a **plate** (response).
- The **status code** is how the waiter answers: 200 "here you go", 404 "we don't have that", 401 "table not authorised", 500 "kitchen is on fire".

## 4. How it works

### The main methods

| HTTP method | Meaning | `requests` call |
|-------------|---------|-----------------|
| GET | read data | `requests.get(url)` |
| POST | create / send data | `requests.post(url, json=...)` |
| PUT / PATCH | update | `requests.put(...)` / `.patch(...)` |
| DELETE | remove | `requests.delete(url)` |

### Status code families

| Code | Meaning |
|------|---------|
| 2xx (200, 201) | success |
| 3xx | redirect |
| 4xx (400, 401, 403, 404, 429) | **your** side: bad request, not logged in, forbidden, not found, rate-limited |
| 5xx (500, 503) | **server** side problem |

### The response object

| Attribute | Gives |
|-----------|-------|
| `r.status_code` | number like 200 |
| `r.json()` | body parsed into dict/list |
| `r.text` | body as a string |
| `r.headers` | dict of headers |
| `r.url` | final URL called |
| `r.raise_for_status()` | raises an exception for 4xx/5xx |

**Always pass `timeout=`**. Without it a stuck server can hang your program forever.

## 5. Code walkthrough, block by block

### Block 1: simplest GET
Sends a request to a public GitHub endpoint and prints the status (`200`) and the content type (`application/json`). Your stub uses exactly this call.

### Block 2: parse the JSON
`response.json()` is Day 19's `json.loads` already done for you. You get a normal dict, so `user["name"]` works.

### Block 3: query parameters
`params={...}` becomes `?q=...&sort=...` at the end of the URL, **correctly encoded**. `resp.url` shows the real URL. The response holds a list under `"items"`, so the loop is plain Day 8 over a list of dicts (Day 13). The f-string alignment (`:<35`, `:>7`) lines the output up as a table (Day 20).

### Block 4: headers
Headers carry extra information: what format you accept, who you are, authentication tokens (`Authorization: Bearer ...`). Real APIs need these often. **Never hard-code a token in your code**; read it from an environment variable (`os.environ["TOKEN"]`).

### Block 5: robust error handling
`get_json` wraps everything in `try/except` (Day 16):
- `raise_for_status()` converts a 404 or 500 into an `HTTPError`.
- `Timeout` and `ConnectionError` cover network trouble.
- Every failure path ends with `return None`, so the caller needs only one check.

The test call asks for a user that does not exist, so you see a clean "HTTP error: 404" message instead of a crash.

### Block 6: reusable function
`repo_summary` builds on `get_json`. This layering (low-level fetch → higher-level meaning) is the same idea as Day 20's layers: **fetch once, interpret elsewhere**.

### Block 7: POST with JSON
`json={...}` converts the dict to JSON text and sets the right header automatically. `httpbin.org` is a free testing service that echoes back what you sent, so you can verify the request without touching a real system.

## 6. How the blocks connect

```
Block 1  GET + status
Block 2  read the JSON body
Block 3  add query parameters
Block 4  add headers
Block 5  handle failure         ← the difference between a script and a tool
Block 6  wrap it in functions
Block 7  send data (POST)
```

## 7. Common mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| No `timeout=` | program may hang | always set it |
| Calling `.json()` on an error page | `JSONDecodeError` | check status first / `raise_for_status()` |
| Building URLs by gluing `?a=` + value by hand | wrong encoding | use `params=` |
| Hard-coding passwords/tokens | security leak | environment variables |
| Ignoring rate limits (429) | blocked | slow down, read the docs, `time.sleep` |
| `data=` vs `json=` confusion | server cannot read it | `json=` for JSON APIs |
| Assuming a key exists | `KeyError` | `.get("key")` (Day 13) |

## 8. Practice

1. In your stub, print the name and number of followers for any GitHub user.
2. Add a loop that fetches three users and prints a table.
3. Use `params=` to search repositories for your favourite topic.
4. Cause a 404 and a timeout (`timeout=0.001`) and make the program report both politely.
5. Write `save_response(url, filename)` that fetches JSON and saves it with `json.dump` (Day 19).
6. Read the docs of another public API (for example a weather or public-holidays API) and call one endpoint.

## 9. Self-check

- What do 200, 404 and 500 mean?
- Why use `raise_for_status()`?
- What is the difference between `params=` and `json=`?
- Why should secrets never be written into code?

**Next:** Day 27: work with the two most common file formats for data, CSV and JSON.
