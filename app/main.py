from typing import Annotated

from fastapi import FastAPI, Path
from fastapi.params import Query

app = FastAPI()


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