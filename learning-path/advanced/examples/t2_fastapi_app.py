"""Track 2b example: FastAPI, a typed, self-documenting API.

Run:    uvicorn t2_fastapi_app:app --reload      (from the examples folder)
   or:  python3 learning-path/advanced/examples/t2_fastapi_app.py
Open:   http://127.0.0.1:8000/docs     <- automatic interactive documentation
Needs:  pip install fastapi "uvicorn[standard]"
"""

from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Tickets API", version="1.0")


# BLOCK 1: a data model: the shape and rules of your data
class TicketIn(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    priority: int = Field(default=3, ge=1, le=5)      # must be 1..5


class Ticket(TicketIn):
    id: int
    status: str = "open"


db: list[Ticket] = [
    Ticket(id=1, title="Disk alert on node 3", priority=2),
    Ticket(id=2, title="Slow mount on client", priority=4, status="closed"),
]


# BLOCK 2: the simplest endpoint
@app.get("/")
def root():
    return {"message": "FastAPI is running", "docs": "/docs"}


# BLOCK 3: query parameters, validated and typed by the function signature
@app.get("/tickets", response_model=list[Ticket])
def list_tickets(status: Optional[str] = None, min_priority: int = 1):
    return [t for t in db
            if (status is None or t.status == status) and t.priority >= min_priority]


# BLOCK 4: path parameter with automatic type conversion and 404
@app.get("/tickets/{ticket_id}", response_model=Ticket)
def get_ticket(ticket_id: int):
    for t in db:
        if t.id == ticket_id:
            return t
    raise HTTPException(status_code=404, detail="Ticket not found")


# BLOCK 5: POST with a validated body. Bad input is rejected automatically (422)
@app.post("/tickets", response_model=Ticket, status_code=201)
def create_ticket(payload: TicketIn):
    new = Ticket(id=max((t.id for t in db), default=0) + 1, **payload.model_dump())
    db.append(new)
    return new


# BLOCK 6: update and delete
@app.patch("/tickets/{ticket_id}/close", response_model=Ticket)
def close_ticket(ticket_id: int):
    ticket = get_ticket(ticket_id)                    # reuse Block 4 (raises 404 if missing)
    ticket.status = "closed"
    return ticket


@app.delete("/tickets/{ticket_id}", status_code=204)
def delete_ticket(ticket_id: int):
    ticket = get_ticket(ticket_id)
    db.remove(ticket)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("t2_fastapi_app:app", host="127.0.0.1", port=8000, reload=True)
