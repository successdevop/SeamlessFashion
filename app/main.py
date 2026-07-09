from typing import Annotated, Literal

from fastapi import FastAPI, Path
from fastapi.params import Query, Body
from pydantic import BaseModel, Field

app = FastAPI()

class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

    model_config = {"extra":"forbid"}


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


@app.put("/items/{item_id}")
def read_data(item_id: int, item: Item, user: User):
    result = {"item_id": item_id, "item_data": item, "user_data": user}
    return result


@app.put("/item/{item_id}")
def read_item(item_id: Annotated[int, Path(title="Item ID")], q: str | None = None, item: Item | None = None):
    result = {"item_id": item_id}
    if q:
        result.update({"q":q})
    if item:
        result.update({"item": item})
    return result


@app.get("/item")
def get_data(filter_query: Annotated[FilterParams, Query()]):
    print(filter_query.order_by)
    return filter_query


@app.get("/items/{item_id}")
def read_items(*, item_id: Annotated[int, Path(title="The ID of the item to get")],
               q: Annotated[str|None, Query(alias="item-query")] = None,
               size: Annotated[float, Query(gt=0, le=10.5)]):
    result = {"item_id": item_id}
    if q:
        result.update({"q":q})
    if size:
        result.update({"size":size})
    return result


@app.post("/items/{id}")
def create(id: Annotated[int, Path()], item: Item, user: User, importance: Annotated[int, Body()]):
    return {"id": id, "item_data": item, "user_data": user, "importance": importance}


@app.put("/update/{item_id}")
def update_data(item_id: int, item: Item, user: User, importance: Annotated[int, Body()], q: str | None = None):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results
