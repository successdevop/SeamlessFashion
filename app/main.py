from typing import Annotated, Literal

from fastapi import FastAPI, Path
from fastapi.params import Query, Body
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()

class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

    model_config = {"extra":"forbid"}


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: list[Image] | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]


@app.post("/index-weights")
def create_index_weights(weights: dict[int, float]):
    return weights


@app.post("/image/multiple")
def create_images(images: list[Image]):
    return images


@app.post("/offers")
def create_offers(offer: Offer):
    return offer


@app.put("/items/{item_id}")
def read_data(item_id: int, item: Item):
    result = {"item_id": item_id, "item_data": item}
    return result

