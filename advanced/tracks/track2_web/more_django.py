"""Django: 10 examples, simple to complex (models, queries, templates, views, forms).

Run:    python3 advanced/tracks/track2_web/more_django.py
Needs:  pip install django

A normal Django project is many files (see t2_django_notes.md). Here Django is
configured inline with an in-memory SQLite database, so ALL ten examples fit
in one runnable file and leave nothing on disk.
"""

import django
from django.conf import settings

settings.configure(
    DEBUG=True,
    SECRET_KEY="demo-only-not-secret",
    ALLOWED_HOSTS=["*"],
    ROOT_URLCONF="__main__",
    INSTALLED_APPS=[],
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
    TEMPLATES=[{"BACKEND": "django.template.backends.django.DjangoTemplates"}],
    DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
    USE_TZ=True,
)
django.setup()

from django import forms
from django.db import connection, models
from django.db.models import Avg, Count, F, Max, Q
from django.http import Http404, JsonResponse
from django.template import engines
from django.test import Client
from django.urls import path


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


# ---------------------------------------------------------------
show(1, "Define models (they ARE your database tables)")
# WHAT: Python classes that become tables.
# HOW : fields describe the columns; migrations normally create the tables.
#       Here schema_editor creates them directly.
# WHY : you never write CREATE TABLE.
class Team(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        app_label = "demo"

    def __str__(self):
        return self.name


class Server(models.Model):
    name = models.CharField(max_length=50)
    cpu = models.IntegerField(default=0)
    status = models.CharField(max_length=10, default="up")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="servers", null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "demo"

    def __str__(self):
        return f"{self.name} ({self.status}, {self.cpu}%)"


with connection.schema_editor() as editor:
    editor.create_model(Team)
    editor.create_model(Server)
print("tables:", sorted(t for t in connection.introspection.table_names()))

# ---------------------------------------------------------------
show(2, "Create and fetch objects")
# WHAT: insert and read rows.
# HOW : Model.objects.create(...); .get(pk=...) for exactly one row.
# WHY : the ORM turns method calls into SQL.
ops = Team.objects.create(name="ops")
dev = Team.objects.create(name="dev")
Server.objects.create(name="web01", cpu=40, team=ops)
Server.objects.create(name="web02", cpu=91, team=ops)
Server.objects.create(name="db01", cpu=0, status="down", team=dev)
s = Server(name="cache01", cpu=22, team=dev)
s.save()
print(Server.objects.get(name="web01"))
print("count:", Server.objects.count(), "| pk of cache01:", s.pk)
try:
    Server.objects.get(name="nobody")
except Server.DoesNotExist:
    print("DoesNotExist raised for a missing row")

# ---------------------------------------------------------------
show(3, "Querying: filter, exclude, order, slice")
# WHAT: ask for subsets of rows.
# HOW : methods chain and are lazy: SQL only runs when you use the result.
# WHY : the Django version of Pandas filtering or list comprehensions.
print(list(Server.objects.filter(status="up").values_list("name", flat=True)))
print(list(Server.objects.exclude(status="up").values_list("name", flat=True)))
print(list(Server.objects.order_by("-cpu").values_list("name", "cpu")[:2]))
print(Server.objects.filter(cpu__gt=50).exists(), Server.objects.filter(cpu__gt=500).exists())
print(Server.objects.filter(status="up").query.__str__()[-60:])

# ---------------------------------------------------------------
show(4, "Lookups and Q objects")
# WHAT: richer conditions.
# HOW : field__lookup=value (contains, gte, in, startswith...); Q() combines
#       conditions with | (or), & (and), ~ (not).
# WHY : search forms and complex filters.
print(list(Server.objects.filter(name__startswith="web").values_list("name", flat=True)))
print(list(Server.objects.filter(cpu__in=[0, 22]).values_list("name", flat=True)))
print(list(Server.objects.filter(Q(cpu__gt=80) | Q(status="down")).values_list("name", flat=True)))
print(list(Server.objects.filter(~Q(status="up"), team__name="dev").values_list("name", flat=True)))

# ---------------------------------------------------------------
show(5, "Update and delete")
# WHAT: change or remove rows, one or many.
# HOW : change an attribute and save(); or .update() / .delete() on a query
#       (one SQL statement). F("field") refers to a column's own value.
# WHY : bulk operations are far faster than looping.
web01 = Server.objects.get(name="web01")
web01.cpu = 55
web01.save()
changed = Server.objects.filter(team__name="ops").update(cpu=F("cpu") + 5)
print("rows updated:", changed, "| web01 now", Server.objects.get(name="web01").cpu)
Server.objects.create(name="temp01", cpu=1)
deleted, _ = Server.objects.filter(name="temp01").delete()
print("deleted:", deleted)

# ---------------------------------------------------------------
show(6, "Relationships: ForeignKey and reverse access")
# WHAT: rows that belong to other rows.
# HOW : server.team gives the Team; team.servers (related_name) gives all its
#       servers; double underscore follows relations in filters;
#       select_related fetches both tables in ONE query.
# WHY : relational data without writing joins.
srv = Server.objects.get(name="db01")
print(srv.team, "| ops servers:", list(ops.servers.values_list("name", flat=True)))
print(list(Server.objects.filter(team__name="dev").values_list("name", flat=True)))
from django.test.utils import CaptureQueriesContext

with CaptureQueriesContext(connection) as ctx:
    names = [f"{x.name}->{x.team.name}" for x in Server.objects.select_related("team")]
print(names, "| queries used:", len(ctx))

# ---------------------------------------------------------------
show(7, "Aggregation and annotation")
# WHAT: counts and averages, overall and per group.
# HOW : aggregate() gives one result; annotate() adds a value to every row
#       of a group query.
# WHY : reports.
print(Server.objects.aggregate(avg=Avg("cpu"), busiest=Max("cpu"), total=Count("id")))
per_team = (Server.objects.values("team__name")
            .annotate(n=Count("id"), avg_cpu=Avg("cpu")).order_by("team__name"))
for row in per_team:
    print(f"  {row['team__name']:<4} servers={row['n']} avg_cpu={row['avg_cpu']:.1f}")
# (In a real project with the app in INSTALLED_APPS you could also write
#  Team.objects.annotate(n=Count("servers")) from the other side.)
print(list(Server.objects.values("status").annotate(n=Count("id")).order_by("status")))

# ---------------------------------------------------------------
show(8, "Templates")
# WHAT: HTML (or text) with placeholders and logic.
# HOW : {{ value }}, {% for %}, {% if %}, filters like |upper |default
#       |floatformat |length. Output is escaped automatically.
# WHY : separate design from code.
template = engines["django"].from_string("""
Servers ({{ servers|length }}):
{% for s in servers %}- {{ s.name|upper }}: {{ s.cpu }}%{% if s.status != "up" %} [DOWN]{% endif %}
{% empty %}none
{% endfor %}Note: {{ note }} | owner: {{ owner|default:"unknown" }}
""")
print(template.render({"servers": Server.objects.order_by("name"), "note": "<b>x</b>"}))

# ---------------------------------------------------------------
show(9, "URLs and views, tested with the test Client")
# WHAT: connect URLs to functions that return responses.
# HOW : urlpatterns lists path() entries (with converters like <int:pk>);
#       views return JsonResponse or rendered HTML; Http404 gives a 404.
# WHY : the request/response core of every Django site.
def server_list(request):
    status = request.GET.get("status")
    qs = Server.objects.all() if not status else Server.objects.filter(status=status)
    return JsonResponse(list(qs.values("id", "name", "cpu", "status")), safe=False)


def server_detail(request, pk):
    try:
        s = Server.objects.select_related("team").get(pk=pk)
    except Server.DoesNotExist:
        raise Http404("no such server")
    return JsonResponse({"name": s.name, "team": s.team.name if s.team else None})


urlpatterns = [
    path("servers/", server_list),
    path("servers/<int:pk>/", server_detail),
]
client = Client(HTTP_HOST="localhost")
print(client.get("/servers/?status=down").json())
print(client.get("/servers/1/").json())
print(client.get("/servers/999/").status_code)

# ---------------------------------------------------------------
show(10, "Mini program: a validated form that creates a row")
# WHAT: accept, validate and save user input.
# HOW : a Form class declares fields and rules; is_valid() runs them and
#       gives cleaned_data or errors; the view saves on success.
# WHY : the standard flow for every input page: validate, then save or
#       show errors.
class ServerForm(forms.Form):
    name = forms.CharField(min_length=3, max_length=50)
    cpu = forms.IntegerField(min_value=0, max_value=100)
    team = forms.ModelChoiceField(queryset=Team.objects.all(), required=False)

    def clean_name(self):
        name = self.cleaned_data["name"].strip().lower()
        if Server.objects.filter(name=name).exists():
            raise forms.ValidationError("a server with this name already exists")
        return name


def add_server(request):
    form = ServerForm(request.POST)
    if form.is_valid():
        s = Server.objects.create(**form.cleaned_data)
        return JsonResponse({"created": s.name, "id": s.pk}, status=201)
    return JsonResponse({"errors": {k: v[0] for k, v in form.errors.items()}}, status=400)


urlpatterns.append(path("servers/add/", add_server))
client = Client(HTTP_HOST="localhost")
print(client.post("/servers/add/", {"name": "Edge01", "cpu": "30", "team": ops.pk}).json())
print(client.post("/servers/add/", {"name": "edge01", "cpu": "30"}).json())
print(client.post("/servers/add/", {"name": "x", "cpu": "300"}).json())
print("total servers now:", Server.objects.count(), "| ops team has:", ops.servers.count())
