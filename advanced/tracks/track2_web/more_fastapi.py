"""FastAPI: 10 examples, simple to complex.

Run:    python3 advanced/tracks/track2_web/more_fastapi.py
Needs:  pip install fastapi httpx          (uvicorn only to serve for real)

Each example builds a small app and calls it with FastAPI's test client. To
serve one for real, save it as app.py and run:  uvicorn app:app --reload
then open http://127.0.0.1:8000/docs for the automatic documentation.
"""

import warnings
from typing import Optional

from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from fastapi.testclient import TestClient


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


# ---------------------------------------------------------------
show(1, "The smallest API")
# WHAT: a GET endpoint returning JSON.
# HOW : the decorator names the method and path; a returned dict becomes JSON.
# WHY : compare with Flask: same idea, less code.
app = FastAPI()


@app.get("/")
def root():
    return {"message": "FastAPI is running"}


client = TestClient(app)
r = client.get("/")
print(r.status_code, r.json())

# ---------------------------------------------------------------
show(2, "Path parameters with automatic type checking")
# WHAT: a typed URL variable.
# HOW : the type hint (item_id: int) converts AND validates. A bad value gives
#       a 422 error with details, with no code from you.
# WHY : validation by declaration.
app = FastAPI()


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "double": item_id * 2}


client = TestClient(app)
print(client.get("/items/21").json())
r = client.get("/items/abc")
print(r.status_code, r.json()["detail"][0]["msg"])

# ---------------------------------------------------------------
show(3, "Query parameters: defaults, optional and constraints")
# WHAT: ?q=...&limit=... with rules.
# HOW : function parameters not in the path become query parameters;
#       Query(...) adds constraints.
# WHY : search, paging and filters.
app = FastAPI()


@app.get("/search")
def search(q: Optional[str] = None, limit: int = Query(10, ge=1, le=50), sort: str = "name"):
    return {"q": q, "limit": limit, "sort": sort}


client = TestClient(app)
print(client.get("/search?q=disk&limit=5").json())
print(client.get("/search").json())
r = client.get("/search?limit=500")
print(r.status_code, r.json()["detail"][0]["msg"])

# ---------------------------------------------------------------
show(4, "Request bodies with Pydantic models")
# WHAT: validated JSON input.
# HOW : a class with typed fields; Field() adds rules. FastAPI parses and
#       validates the body BEFORE your function runs.
# WHY : the whole "if not name:" validation layer disappears.
class ItemIn(BaseModel):
    name: str = Field(min_length=2, max_length=30)
    price: float = Field(gt=0)
    tags: list[str] = []


app = FastAPI()


@app.post("/items", status_code=201)
def create_item(item: ItemIn):
    return {"created": item.name, "price_with_tax": round(item.price * 1.2, 2), "tags": item.tags}


client = TestClient(app)
print(client.post("/items", json={"name": "pen", "price": 2.5, "tags": ["office"]}).json())
r = client.post("/items", json={"name": "x", "price": -1})
print(r.status_code, [e["loc"][-1] for e in r.json()["detail"]])

# ---------------------------------------------------------------
show(5, "response_model: control what is returned")
# WHAT: never leak internal fields.
# HOW : response_model filters the output to the fields of another model.
# WHY : hide passwords and internal ids without remembering to delete them.
class UserIn(BaseModel):
    name: str
    password: str


class UserOut(BaseModel):
    id: int
    name: str


app = FastAPI()


@app.post("/users", response_model=UserOut, status_code=201)
def create_user(user: UserIn):
    return {"id": 1, "name": user.name, "password": user.password}     # extra field


client = TestClient(app)
print(client.post("/users", json={"name": "Sam", "password": "hunter2"}).json())

# ---------------------------------------------------------------
show(6, "Errors: HTTPException and custom handlers")
# WHAT: send the right status code and message.
# HOW : raise HTTPException(status, detail); register a handler for your own
#       exception class.
# WHY : consistent, informative errors.
class OutOfStock(Exception):
    def __init__(self, item):
        self.item = item


app = FastAPI()


@app.exception_handler(OutOfStock)
async def out_of_stock_handler(request, exc):
    return JSONResponse(status_code=409, content={"error": f"{exc.item} is out of stock"})


@app.get("/stock/{name}")
def stock(name: str):
    if name == "ghost":
        raise HTTPException(status_code=404, detail="no such product")
    if name == "pen":
        raise OutOfStock("pen")
    return {"name": name, "qty": 5}


client = TestClient(app)
print(client.get("/stock/book").json())
print(client.get("/stock/ghost").status_code, client.get("/stock/ghost").json())
print(client.get("/stock/pen").status_code, client.get("/stock/pen").json())

# ---------------------------------------------------------------
show(7, "Dependencies: reusable pieces with Depends")
# WHAT: share logic (auth, paging, database) between endpoints.
# HOW : a function listed in Depends(...) runs first; its result is passed in.
# WHY : write the API-key check once; use it on any endpoint.
app = FastAPI()


def paging(page: int = 1, size: int = Query(2, le=10)):
    return {"skip": (page - 1) * size, "size": size}


def require_key(x_api_key: str = Header(default="")):
    if x_api_key != "secret":
        raise HTTPException(status_code=401, detail="bad API key")
    return "service-account"


DATA = list(range(1, 8))


@app.get("/numbers")
def numbers(p: dict = Depends(paging), user: str = Depends(require_key)):
    return {"user": user, "items": DATA[p["skip"]:p["skip"] + p["size"]]}


client = TestClient(app)
print(client.get("/numbers").status_code)
print(client.get("/numbers?page=2", headers={"X-Api-Key": "secret"}).json())

# ---------------------------------------------------------------
show(8, "async endpoints")
# WHAT: let one worker serve many requests while waiting.
# HOW : write `async def` and `await` anything that waits (database, other
#       APIs). Plain `def` endpoints are also fine: FastAPI runs them in a
#       thread pool.
# WHY : high concurrency for I/O-bound services.
import asyncio

app = FastAPI()


@app.get("/slow-add")
async def slow_add(a: int, b: int):
    await asyncio.sleep(0.01)             # stands in for a database/API wait
    return {"sum": a + b}


@app.get("/plain")
def plain():
    return {"kind": "regular def, run in a thread"}


client = TestClient(app)
print(client.get("/slow-add?a=2&b=3").json(), client.get("/plain").json())

# ---------------------------------------------------------------
show(9, "Routers, tags and the OpenAPI schema")
# WHAT: organise endpoints; see the auto-generated docs data.
# HOW : APIRouter(prefix, tags) groups routes; /openapi.json describes the
#       whole API (the /docs page is drawn from it).
# WHY : big APIs stay tidy, and clients get a machine-readable contract.
users = APIRouter(prefix="/users", tags=["users"])
orders = APIRouter(prefix="/orders", tags=["orders"])


@users.get("/{uid}")
def get_user(uid: int):
    return {"uid": uid}


@orders.get("/")
def list_orders():
    return []


app = FastAPI(title="Shop API", version="2.0")
app.include_router(users)
app.include_router(orders)
client = TestClient(app)
schema = client.get("/openapi.json").json()
print(schema["info"]["title"], schema["info"]["version"])
print(sorted(schema["paths"]))
print({p: list(m) for p, m in schema["paths"].items()})

# ---------------------------------------------------------------
show(10, "Mini program: an orders API")
# WHAT: models, validation, dependencies and CRUD in one small service.
# HOW : a stock dict stands in for a database; business rules raise
#       HTTPException with the right code.
# WHY : a realistic template to extend with a real database.
class OrderIn(BaseModel):
    product: str
    qty: int = Field(ge=1, le=100)


class Order(OrderIn):
    id: int
    total: float


STOCK = {"pen": {"price": 1.5, "qty": 50}, "book": {"price": 12.0, "qty": 2}}
ORDERS: dict[int, Order] = {}
app = FastAPI(title="Orders")


@app.post("/orders", response_model=Order, status_code=201)
def place_order(order: OrderIn):
    product = STOCK.get(order.product)
    if product is None:
        raise HTTPException(404, f"unknown product {order.product!r}")
    if product["qty"] < order.qty:
        raise HTTPException(409, f"only {product['qty']} left")
    product["qty"] -= order.qty
    new = Order(id=len(ORDERS) + 1, total=round(product["price"] * order.qty, 2), **order.model_dump())
    ORDERS[new.id] = new
    return new


@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int):
    if order_id not in ORDERS:
        raise HTTPException(404, "order not found")
    return ORDERS[order_id]


@app.get("/stock")
def stock_levels():
    return {name: info["qty"] for name, info in STOCK.items()}


client = TestClient(app)
print(client.post("/orders", json={"product": "pen", "qty": 10}).json())
print(client.post("/orders", json={"product": "book", "qty": 5}).json())
print(client.post("/orders", json={"product": "lamp", "qty": 1}).json())
print(client.post("/orders", json={"product": "pen", "qty": 0}).status_code)
print(client.get("/orders/1").json()["total"], client.get("/orders/9").status_code)
print(client.get("/stock").json())
