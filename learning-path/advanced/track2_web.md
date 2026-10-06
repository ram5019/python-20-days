# Track 2: Web, Flask, FastAPI, Django

**Examples:** `examples/t2_flask_app.py`, `examples/t2_fastapi_app.py`, `examples/t2_django_notes.md`
**Install:** `pip install flask` | `pip install fastapi "uvicorn[standard]"` | `pip install django`
**Prerequisites:** Day 14 (functions), Day 19 (JSON), Day 23 (decorators), Day 26 (APIs)

---

## 1. The big idea

A **web framework** lets your Python code **answer requests from browsers and other programs**. This is the other side of Day 26: there you were the **client** asking an API; now you are the **server** answering.

```
browser / program ──request──►  your Python app  ──► (data, files, logic)
                  ◄──response──   (HTML or JSON)
```

All three frameworks do the same core job: **map a URL to a Python function**.

## 2. Why do these exist?

You could write a server with raw sockets and parse HTTP by hand, but you would be rebuilding routing, validation, templates, security and error handling. Frameworks give you all of that so you only write **your** logic.

Useful for you: internal dashboards, a small status API for team tools, a webhook receiver for alerts, and a front end over your scripts (like Day 20's student manager, but as a web page).

## 3. Simple way to understand

A **restaurant again** (Day 26 was the customer, now you run it):

- The **URL** is the menu item the customer orders.
- The **route** is the instruction card linking each menu item to a **cook** (your function).
- The cook prepares a **dish**: a web page (HTML) or a data box (JSON).
- The **status code** tells the customer how it went.

Choosing a framework:

| | Flask | FastAPI | Django |
|---|-------|---------|--------|
| Size | small, minimal | small, modern | large, "batteries included" |
| Best for | quick apps, learning, small tools | **APIs**, typed and validated | big sites with users, database and admin |
| Database | bring your own | bring your own | built-in ORM + admin |
| Docs | none by default | **automatic** interactive docs | admin site |
| Learning curve | gentlest | gentle, a bit more concepts | steepest, most to learn |

**Rule of thumb:** Flask to learn the ideas, FastAPI for APIs, Django when you need a full site with a database and admin screen.

---

## Part 1: Flask (`t2_flask_app.py`)

### Run it
```bash
python3 learning-path/advanced/examples/t2_flask_app.py
```
Open http://127.0.0.1:5000/ and try `/hello/ram`, `/tickets`, `/api/tickets`, `/api/tickets?status=open`.

### Code walkthrough

| Block | Code idea | What it does |
|-------|-----------|--------------|
| setup | `app = Flask(__name__)` and a list of dicts | creates the app; `tickets` is a fake database (Day 13), lost on restart |
| 1 | `@app.route("/")` over `def home()` | a **decorator** (Day 23) registers the function for that URL; the return value is the page |
| 2 | `"/hello/<name>"` | `<name>` captures part of the URL and passes it as the argument |
| 3 | `jsonify(...)`, `request.args.get("status")` | returns JSON; reads `?status=open` from the URL; the list comprehension (Day 21) filters |
| 4 | `<int:ticket_id>`, `return jsonify(...), 404` | the converter makes it an `int`; a tuple sets the **status code** |
| 5 | `methods=["POST"]`, `request.get_json()` | receives a JSON body (Day 19); returns **400** for bad input, **201** when created |
| 6 | `render_template_string(PAGE, tickets=tickets)` | fills an HTML **template** with data; `{% for %}` is Day 8 inside HTML |
| end | `app.run(debug=True)` | starts the dev server; `debug=True` auto-reloads (**never in production**) |

**How the blocks connect:** each block adds one concept to the same app: route → URL parameter → JSON → errors → input → HTML. Blocks 3 to 5 together are a complete **CRUD-style API** (list, read, create).

### Try the POST from a second terminal
```bash
curl -X POST http://127.0.0.1:5000/api/tickets \
     -H "Content-Type: application/json" -d '{"title": "Check fans"}'
```
(Or use `requests.post(..., json=...)` from Day 26. You are calling your own server.)

---

## Part 2: FastAPI (`t2_fastapi_app.py`)

### Run it
```bash
cd learning-path/advanced/examples
uvicorn t2_fastapi_app:app --reload
```
Open **http://127.0.0.1:8000/docs**. You get **interactive documentation for free**: click an endpoint, press "Try it out", and send real requests from the browser.

### The key difference: type hints become validation
In Flask you checked `if not title:` by hand. In FastAPI you **declare the shape** and the framework enforces it.

### Code walkthrough

| Block | Code idea | What it does |
|-------|-----------|--------------|
| 1 | `class TicketIn(BaseModel)` with `Field(min_length=3)`, `ge=1, le=5` | a **Pydantic model**: a class (Day 18) that describes valid data. Invalid input is rejected **automatically** with a 422 error and a clear message |
| 1 | `class Ticket(TicketIn)` adds `id`, `status` | **inheritance** (Day 18, Block 6): the stored ticket = input fields + extras |
| 2 | `@app.get("/")` | same decorator idea as Flask, with the HTTP method in the name |
| 3 | `status: Optional[str] = None`, `min_priority: int = 1` | **function parameters become query parameters**; types are converted and checked; defaults make them optional |
| 4 | `ticket_id: int` in the path | non-numeric → automatic 422; `HTTPException(404)` for missing |
| 5 | `payload: TicketIn` | the request body is parsed and validated into an object; `201` on success |
| 6 | `PATCH` and `DELETE` | other HTTP verbs; `close_ticket` **reuses** `get_ticket` (a function calling a function, Day 14) |

`response_model=` makes sure the response matches the model and documents it.

**How the blocks connect:** models (1) are used by endpoints (3 to 6), and the same models generate the documentation page. Describe your data once; get validation, conversion and docs.

**Tested:** I ran it with FastAPI's test client: list/filter (200), unknown id (404), invalid priority (422), create (201), close, delete (204).

---

## Part 3: Django (`examples/t2_django_notes.md`)

Django is bigger, so it has a **step-by-step walkthrough** (tested, in `t2_django_notes.md`) rather than a single file.

### The ideas in short

| Piece | File | Job | Flask/FastAPI equivalent |
|-------|------|-----|--------------------------|
| Model | `models.py` | defines a **database table** as a class | (you bring SQLAlchemy yourself) |
| View | `views.py` | function that handles a request | the route function |
| URLs | `urls.py` | URL → view table | the `@app.route` decorators, in one place |
| Template | `templates/...html` | HTML with placeholders | `render_template_string` |
| Admin | `admin.py` | **free web UI to edit data** | none |
| Migrations | `manage.py migrate` | keep the database in sync with models | none built in |

### The flow of one request
```
browser → mysite/urls.py → tickets/urls.py → views.ticket_list
                                              │ asks
                                              ▼
                                       models.Ticket (ORM → database)
                                              │ data
                                              ▼
                                    templates/tickets/list.html → HTML → browser
```

---

## 7. Common mistakes (all three)

| Mistake | Result | Fix |
|---------|--------|-----|
| Running with `debug=True`/`DEBUG=True` in production | leaks internals, security risk | turn off; use a production server |
| Storing data in a list/dict in the app | lost on restart, wrong with multiple workers | use a real database (SQLite, PostgreSQL) |
| Forgetting `return` in a view | `None` is not a valid response | always return something |
| Not validating input | crashes or bad data | check by hand (Flask) or use models (FastAPI) |
| Putting secrets in code | leaked credentials | environment variables |
| Using the dev server in production | slow and unsafe | gunicorn / uvicorn behind a proxy |
| Wrong HTTP method → `405 Method Not Allowed` | request rejected | match `methods=[...]` |
| Port already in use | startup error | stop the other process or choose another port |

## 8. Practice (in order)

1. **Flask:** add `/api/tickets/<id>/close` that marks a ticket as closed (use `methods=["POST"]`).
2. **Flask:** make `/tickets` show open tickets in bold and closed in grey (an `{% if %}` in the template).
3. **Flask:** save tickets to a JSON file (Day 19) so they survive restarts.
4. **FastAPI:** add a `GET /stats` endpoint returning counts per status (Day 13 counting).
5. **FastAPI:** send an invalid body from `/docs` and read the error message.
6. **FastAPI:** write a small client script using `requests` (Day 26) that creates a ticket and lists them.
7. **Django:** follow `t2_django_notes.md` end to end, then do its practice list.
8. **Compare:** build the same "ticket list" in the other framework. What was easier or harder?

## 9. Self-check

- What does a route do?
- Why does FastAPI reject `priority: 9` without you writing an `if`?
- Which status codes mean: created, bad input, not found, validation error?
- Why is a Python list a poor database for a web app?
- When would you choose Django over Flask?
- In Django, what do `makemigrations` and `migrate` each do?

**Next:** Track 3: Automation, where your code reads web pages and drives a browser.
