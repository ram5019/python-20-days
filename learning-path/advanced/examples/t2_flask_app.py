"""Track 2a example: Flask, a small web app and JSON API.

Run:    python3 learning-path/advanced/examples/t2_flask_app.py
Open:   http://127.0.0.1:5000
Needs:  pip install flask
Stop:   Ctrl + C
"""

from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

# In-memory "database" (a list of dicts, Day 13). Resets when the app restarts.
tickets = [
    {"id": 1, "title": "Disk alert on node 3", "status": "open"},
    {"id": 2, "title": "Slow mount on client", "status": "closed"},
]


# BLOCK 1: the simplest route: URL -> function -> text
@app.route("/")
def home():
    return "Hello from Flask! Try /tickets or /hello/Ram"


# BLOCK 2: a URL parameter
@app.route("/hello/<name>")
def hello(name):
    return f"Hello, {name.title()}!"


# BLOCK 3: return JSON (an API endpoint)
@app.route("/api/tickets")
def list_tickets():
    status = request.args.get("status")              # /api/tickets?status=open
    result = [t for t in tickets if status is None or t["status"] == status]
    return jsonify(result)


# BLOCK 4: one item, with a proper 404
@app.route("/api/tickets/<int:ticket_id>")
def get_ticket(ticket_id):
    for t in tickets:
        if t["id"] == ticket_id:
            return jsonify(t)
    return jsonify({"error": "not found"}), 404


# BLOCK 5: receive data (POST)
@app.route("/api/tickets", methods=["POST"])
def create_ticket():
    data = request.get_json(silent=True) or {}
    title = data.get("title", "").strip()
    if not title:
        return jsonify({"error": "title is required"}), 400
    new = {"id": max((t["id"] for t in tickets), default=0) + 1,
           "title": title, "status": "open"}
    tickets.append(new)
    return jsonify(new), 201                         # 201 = created


# BLOCK 6: an HTML page built from a template
PAGE = """
<!doctype html>
<title>Tickets</title>
<h1>Tickets ({{ tickets|length }})</h1>
<ul>
{% for t in tickets %}
  <li>#{{ t.id }} {{ t.title }} <b>[{{ t.status }}]</b></li>
{% endfor %}
</ul>
"""

@app.route("/tickets")
def tickets_page():
    return render_template_string(PAGE, tickets=tickets)


if __name__ == "__main__":
    app.run(debug=True)                              # debug=True: auto-reload, dev only
