"""Flask: 10 examples, simple to complex.

Run:    python3 advanced/tracks/track2_web/more_flask.py
Needs:  pip install flask

Each example builds a small app and calls it with Flask's test client, so you
see requests and responses without starting a server. To serve any app for
real, add:   app.run(debug=True)   and open http://127.0.0.1:5000
"""

from flask import (Blueprint, Flask, abort, jsonify, redirect, render_template_string,
                   request, url_for)


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


# ---------------------------------------------------------------
show(1, "The smallest app: one route")
# WHAT: map a URL to a function.
# HOW : @app.route registers the function; its return value is the page.
# WHY : everything in Flask is "URL -> function".
app = Flask(__name__)


@app.route("/")
def home():
    return "Hello from Flask!"


client = app.test_client()
r = client.get("/")
print(r.status_code, r.data.decode())

# ---------------------------------------------------------------
show(2, "URL variables and converters")
# WHAT: capture part of the URL.
# HOW : <name> or <int:id>. The converter type-checks: /users/abc gives 404.
# WHY : one route serves many resources.
app = Flask(__name__)


@app.route("/hello/<name>")
def hello(name):
    return f"Hello, {name.title()}!"


@app.route("/users/<int:user_id>/posts/<int:post_id>")
def post(user_id, post_id):
    return f"user {user_id}, post {post_id}"


client = app.test_client()
print(client.get("/hello/sam").data.decode())
print(client.get("/users/7/posts/42").data.decode())
print(client.get("/users/abc/posts/1").status_code)

# ---------------------------------------------------------------
show(3, "Query parameters")
# WHAT: read ?key=value from the URL.
# HOW : request.args.get(name, default, type=...).
# WHY : search, filters and paging.
app = Flask(__name__)


@app.route("/search")
def search():
    q = request.args.get("q", "")
    limit = request.args.get("limit", 10, type=int)
    return jsonify({"query": q, "limit": limit})


client = app.test_client()
print(client.get("/search?q=disk&limit=3").get_json())
print(client.get("/search").get_json())

# ---------------------------------------------------------------
show(4, "A JSON API endpoint")
# WHAT: return data instead of a web page.
# HOW : jsonify(dict_or_list). A tuple (body, status) sets the status code.
# WHY : APIs are how programs talk to your app (Day 26 was the client side).
app = Flask(__name__)
SERVERS = [{"id": 1, "name": "web01", "cpu": 40}, {"id": 2, "name": "db01", "cpu": 85}]


@app.route("/api/servers")
def servers():
    return jsonify(SERVERS)


@app.route("/api/servers/<int:server_id>")
def server(server_id):
    for s in SERVERS:
        if s["id"] == server_id:
            return jsonify(s)
    return jsonify({"error": "not found"}), 404


client = app.test_client()
print(client.get("/api/servers").get_json())
r = client.get("/api/servers/9")
print(r.status_code, r.get_json())

# ---------------------------------------------------------------
show(5, "POST with validation and status codes")
# WHAT: receive and validate JSON.
# HOW : request.get_json(); 400 for bad input, 201 for created.
# WHY : never trust what clients send.
app = Flask(__name__)
ITEMS = []


@app.post("/api/items")
def create_item():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    qty = data.get("qty", 1)
    if not name:
        return jsonify({"error": "name is required"}), 400
    if not isinstance(qty, int) or qty < 1:
        return jsonify({"error": "qty must be a positive integer"}), 400
    item = {"id": len(ITEMS) + 1, "name": name, "qty": qty}
    ITEMS.append(item)
    return jsonify(item), 201


client = app.test_client()
for payload in ({"name": "pen", "qty": 3}, {"name": ""}, {"name": "ink", "qty": -1}):
    r = client.post("/api/items", json=payload)
    print(r.status_code, r.get_json())

# ---------------------------------------------------------------
show(6, "Custom error handlers and abort()")
# WHAT: friendly, consistent error responses.
# HOW : abort(code) stops the request; @app.errorhandler formats it.
# WHY : clients get JSON errors instead of HTML error pages.
app = Flask(__name__)


@app.route("/secret")
def secret():
    abort(403)


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "no such page", "path": request.path}), 404


@app.errorhandler(403)
def forbidden(error):
    return jsonify({"error": "forbidden"}), 403


client = app.test_client()
print(client.get("/nowhere").get_json())
print(client.get("/secret").status_code, client.get("/secret").get_json())

# ---------------------------------------------------------------
show(7, "HTML templates")
# WHAT: build pages from data.
# HOW : Jinja2 syntax: {{ value }} prints, {% for %} / {% if %} are logic,
#       |filter transforms. Variables are escaped automatically (safe from
#       script injection).
# WHY : separates presentation from logic.
app = Flask(__name__)
PAGE = """
<h1>{{ title|upper }}</h1>
<ul>
{% for s in servers %}
  <li class="{{ 'hot' if s.cpu > 80 else 'ok' }}">{{ s.name }}: {{ s.cpu }}%</li>
{% else %}
  <li>No servers</li>
{% endfor %}
</ul>
<p>{{ note }}</p>
"""


@app.route("/dashboard")
def dashboard():
    return render_template_string(PAGE, title="status", servers=[
        type("S", (), s)() for s in SERVERS], note="<script>alert(1)</script>")


html = app.test_client().get("/dashboard").data.decode()
print(html.strip())

# ---------------------------------------------------------------
show(8, "Forms, redirects and url_for")
# WHAT: handle an HTML form post, then redirect.
# HOW : request.form reads form fields; redirect(url_for("name")) avoids
#       hard-coded URLs; the "post/redirect/get" pattern prevents resubmits.
# WHY : the standard way web forms work.
app = Flask(__name__)
NOTES = []


@app.route("/notes", methods=["GET", "POST"])
def notes():
    if request.method == "POST":
        NOTES.append(request.form["text"])
        return redirect(url_for("notes"))
    return "<br>".join(NOTES) or "no notes"


client = app.test_client()
r = client.post("/notes", data={"text": "buy milk"})
print(r.status_code, "->", r.headers["Location"])
client.post("/notes", data={"text": "call Ana"})
print(client.get("/notes").data.decode())

# ---------------------------------------------------------------
show(9, "Blueprints: split an app into parts")
# WHAT: group related routes.
# HOW : Blueprint(name, __name__, url_prefix=...), then app.register_blueprint.
# WHY : keeps big apps organised, one file per feature.
admin = Blueprint("admin", __name__, url_prefix="/admin")
api = Blueprint("api", __name__, url_prefix="/api/v1")


@admin.route("/users")
def admin_users():
    return "admin: user list"


@api.route("/ping")
def ping():
    return jsonify(pong=True)


app = Flask(__name__)
app.register_blueprint(admin)
app.register_blueprint(api)
client = app.test_client()
print(client.get("/admin/users").data.decode(), "|", client.get("/api/v1/ping").get_json())
print(sorted(str(rule) for rule in app.url_map.iter_rules() if rule.endpoint != "static"))

# ---------------------------------------------------------------
show(10, "Mini program: a to-do API with CRUD, hooks and a check")
# WHAT: create, read, update, delete, plus request logging and an API key.
# HOW : before_request runs for every request (auth); after_request adds a
#       header; routes share one in-memory store.
# WHY : the shape of a real small service. (Use a database for real data.)
app = Flask(__name__)
TODOS = {}
NEXT_ID = {"n": 1}
LOG = []


@app.before_request
def check_key():
    LOG.append(f"{request.method} {request.path}")
    if request.path.startswith("/todos") and request.headers.get("X-Api-Key") != "secret":
        return jsonify({"error": "bad or missing API key"}), 401


@app.after_request
def add_header(response):
    response.headers["X-Served-By"] = "demo"
    return response


@app.get("/todos")
def list_todos():
    done = request.args.get("done")
    items = list(TODOS.values())
    if done is not None:
        items = [t for t in items if t["done"] == (done == "true")]
    return jsonify(items)


@app.post("/todos")
def add_todo():
    title = (request.get_json(silent=True) or {}).get("title", "").strip()
    if not title:
        return jsonify({"error": "title required"}), 400
    todo = {"id": NEXT_ID["n"], "title": title, "done": False}
    TODOS[todo["id"]] = todo
    NEXT_ID["n"] += 1
    return jsonify(todo), 201


@app.patch("/todos/<int:todo_id>")
def update_todo(todo_id):
    todo = TODOS.get(todo_id) or abort(404)
    todo.update({k: v for k, v in (request.get_json() or {}).items() if k in ("title", "done")})
    return jsonify(todo)


@app.delete("/todos/<int:todo_id>")
def delete_todo(todo_id):
    TODOS.pop(todo_id, None)
    return "", 204


client = app.test_client()
H = {"X-Api-Key": "secret"}
print(client.get("/todos").status_code)
client.post("/todos", json={"title": "write report"}, headers=H)
client.post("/todos", json={"title": "fix bug"}, headers=H)
client.patch("/todos/1", json={"done": True}, headers=H)
print(client.get("/todos?done=true", headers=H).get_json())
print(client.delete("/todos/2", headers=H).status_code, len(client.get("/todos", headers=H).get_json()))
print(client.get("/todos", headers=H).headers["X-Served-By"], "| requests logged:", len(LOG))
