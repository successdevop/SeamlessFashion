from typing import Annotated, Literal

from fastapi import FastAPI, Path
from fastapi.params import Query
from pydantic import BaseModel, Field

app = FastAPI()

class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

    model_config = {"extra":"forbid"}


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


