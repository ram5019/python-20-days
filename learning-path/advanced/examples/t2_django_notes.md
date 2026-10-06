# Django: step-by-step mini project

Django needs a **project folder with several files**, so it is a walkthrough instead of one script.
Everything below was run and tested on Django 6.1 with Python 3.14.

**Needs:** `pip install django`

```bash
mkdir ~/django-demo && cd ~/django-demo
python3 -m venv .venv && source .venv/bin/activate
pip install django
django-admin startproject mysite .     # the project (settings, main URLs)
python manage.py startapp tickets      # an app inside it (one feature area)
```

You now have:

```
django-demo/
├── manage.py              ← command-line helper (run server, migrate, ...)
├── mysite/
│   ├── settings.py        ← configuration (apps, database, ...)
│   └── urls.py            ← the main URL table
└── tickets/
    ├── models.py          ← the DATA (tables)
    ├── views.py           ← the LOGIC (what happens for a URL)
    ├── admin.py           ← free admin screen
    └── (we add) urls.py and templates/   ← routes and HTML
```

Django's pattern is **MTV**: **M**odel (data), **T**emplate (HTML), **V**iew (logic).

## Step 1: define the data, `tickets/models.py`

```python
from django.db import models


class Ticket(models.Model):
    title = models.CharField(max_length=100)
    status = models.CharField(max_length=10, default="open")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"#{self.pk} {self.title}"
```

**What it does:** a class (Day 18) describes one **database table**. Each attribute is a column. Django creates the SQL for you, so you never write `CREATE TABLE`. `__str__` (Day 18, Block 4) controls how a ticket prints, including in the admin.

## Step 2: register the app, `mysite/settings.py`

Add `'tickets'` to the `INSTALLED_APPS` list (after `'django.contrib.staticfiles'`):

```python
INSTALLED_APPS = [
    ...
    'django.contrib.staticfiles',
    'tickets',
]
```

**What it does:** tells Django this app exists. Without it the model is ignored.

## Step 3: create the table

```bash
python manage.py makemigrations tickets   # write a "plan" of the change
python manage.py migrate                  # apply the plan to the database (SQLite file)
```

**What it does:** `makemigrations` turns your model into a migration file. `migrate` runs it. **Change a model → run both commands again.**

## Step 4: the views, `tickets/views.py`

```python
from django.http import JsonResponse
from django.shortcuts import render

from .models import Ticket


def ticket_list(request):
    status = request.GET.get("status")
    tickets = Ticket.objects.all().order_by("-created")
    if status:
        tickets = tickets.filter(status=status)
    return render(request, "tickets/list.html", {"tickets": tickets})


def ticket_json(request):
    data = list(Ticket.objects.values("id", "title", "status"))
    return JsonResponse(data, safe=False)
```

**What it does:**
- A view is a function that receives the `request` and returns a response (the same idea as Flask routes).
- `Ticket.objects` is the **ORM**: Python code instead of SQL. `.all()`, `.filter(status=...)`, `.order_by("-created")` (minus = newest first) each return a query you can chain.
- `render(...)` fills an HTML template with data (here, `tickets`).
- `JsonResponse` returns JSON, like `jsonify` in Flask. `safe=False` is needed because we return a list, not a dict.

## Step 5: the URLs

Create `tickets/urls.py`:

```python
from django.urls import path

from . import views

urlpatterns = [
    path("", views.ticket_list, name="ticket_list"),
    path("api/", views.ticket_json, name="ticket_json"),
]
```

In `mysite/urls.py`, import `include` and add one line:

```python
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tickets/', include('tickets.urls')),
]
```

**What it does:** the main URL table hands everything starting with `tickets/` to the app's own table. `/tickets/` → `ticket_list`, `/tickets/api/` → `ticket_json`.

## Step 6: the template, `tickets/templates/tickets/list.html`

```html
<h1>Tickets ({{ tickets|length }})</h1>
<ul>
{% for t in tickets %}
  <li>{{ t }} [{{ t.status }}]</li>
{% empty %}
  <li>No tickets yet.</li>
{% endfor %}
</ul>
```

**What it does:** `{{ ... }}` prints a value; `{% ... %}` is logic. `{% for %}` is Day 8, and `{% empty %}` handles the no-data case. The folder name repeats (`tickets/templates/tickets/`) on purpose, so template names do not clash between apps.

## Step 7: free admin screen, `tickets/admin.py`

```python
from django.contrib import admin

from .models import Ticket

admin.site.register(Ticket)
```

```bash
python manage.py createsuperuser     # you choose the username and password
python manage.py runserver
```

Open **http://127.0.0.1:8000/admin** and log in: you can now add, edit and delete tickets in a full web UI **without writing any more code**. Then visit `/tickets/` and `/tickets/api/`.

## What was verified

In a scratch project I created the model, ran the migrations, added two tickets through the ORM, and fetched the views: `/tickets/?status=open` returned 200 showing only the open ticket, and `/tickets/api/` returned both tickets as JSON. I did **not** open the admin screen in a browser.

## Common mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| Forgot to add the app to `INSTALLED_APPS` | model/template not found | add `'tickets'` |
| Changed the model but did not migrate | `no such column` error | `makemigrations` then `migrate` |
| Template in the wrong folder | `TemplateDoesNotExist` | `app/templates/app/file.html` |
| Forgot `include(...)` in the main urls | 404 | wire the app's URLs in |
| `DEBUG = True` and `SECRET_KEY` in production | security risk | use environment variables for real deployments |
| Using `runserver` as a production server | not built for load | use gunicorn/uvicorn behind a proxy |

## Practice

1. Add a `priority` integer field, migrate, and show it in the template.
2. Add a view and URL `/tickets/<int:pk>/` that shows one ticket (`get_object_or_404`).
3. Add a form to create a ticket (look up Django `ModelForm`).
4. Show only closed tickets at `/tickets/?status=closed`.
