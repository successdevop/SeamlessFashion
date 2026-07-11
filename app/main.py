# from datetime import datetime, timedelta, time
# from typing import Annotated, Literal
# from uuid import UUID
#
# from fastapi import FastAPI, Path
# from fastapi.params import Query, Body
# from pydantic import BaseModel, Field, HttpUrl
#
# app = FastAPI()
#
# class FilterParams(BaseModel):
#     limit: int = Field(100, gt=0, le=100)
#     offset: int = Field(0, ge=0)
#     order_by: Literal["created_at", "updated_at"] = "created_at"
#     tags: list[str] = []
#
#     model_config = {"extra":"forbid"}
#
#
# class Image(BaseModel):
#     url: HttpUrl
#     name: str
#
#
# class Item(BaseModel):
#     name: str = Field(examples=["Foo"])
#     description: str | None = Field(default=None, examples=["A very nice item"])
#     price: float= Field(examples=[35.4])
#     tax: float | None = Field(default=None, examples=[3.2])
#     tags: set[str] = Field(examples=[["foo", "doe"]])
#     image: list[Image] | None = Field(examples=[{"name": "Google", "url":"https://www.google.com"}])
#
#     # model_config = {
#     #     "json_schema_extra":{
#     #         "examples":[
#     #             {"name": "Foo", "description": "A very nice item", "price": 35.4, "tax":3.2}
#     #         ]
#     #     }
#     # }
#
#
# class Item2(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
#
#
# class User(BaseModel):
#     username: str
#     full_name: str | None = None
#
#
# class Offer(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     items: list[Item]
#
#
# @app.patch("/items/item_id")
# def update_item(item_id: UUID, start_datetime: Annotated[datetime, Body()], end_datetime: Annotated[datetime, Body()],
#                 process_after: Annotated[timedelta, Body()], repeat_at: Annotated[time | None, Body()] = None):
#     start_process = start_datetime + process_after
#     duration = end_datetime - start_process
#
#     return {
#         "item_id": item_id,
#         "start_datetime": start_datetime,
#         "end_datetime": end_datetime,
#         "process_after": process_after,
#         "repeat_at": repeat_at,
#         "start_process": start_process,
#         "duration": duration
#     }
#
#
# @app.put("/items/{item_id}")
# def update(item_id: int,
#            item: Annotated[Item2, Body(
#                examples=[
#                    {
#                        "name":"Foo",
#                        "description":"A very nice item",
#                        "price": 35.4,
#                        "tax": 3.2
#                    },
#                    {
#                        "name": "Bar",
#                        "price": "35.4",
#                    },
#                    {
#                        "name": "Baz",
#                        "price": "thirty five point four",
#                    },
#                ])]):
#     return {"item_id": item_id, "item":item}
#
#
# # @app.post("/index-weights")
# # def create_index_weights(weights: dict[int, float]):
# #     return weights
# #
# #
# # @app.post("/image/multiple")
# # def create_images(images: list[Image]):
# #     return images
# #
# #
# # @app.post("/offers")
# # def create_offers(offer: Offer):
# #     return offer
# #
# #
# # @app.put("/items/{item_id}")
# # def read_data(item_id: int, item: Item):
# #     result = {"item_id": item_id, "item_data": item}
# #     return result
#
from typing import Annotated, Any

from fastapi import FastAPI, Header, Cookie, Response
from pydantic import BaseModel, Field, EmailStr
from starlette.responses import RedirectResponse, JSONResponse

app = FastAPI()


class Cookies(BaseModel):
    session_id: str
    fatebook_tracker: str | None = None
    googall_tracker: str | None = None


class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tags: list[str] = []


class Item(BaseModel):
    name: str = Field(examples=['LG TV'])
    description: str | None = Field(default=None, examples=['LG TV is the always the best'])
    price: float= Field(examples=[40.015])
    tax: float | None = Field(default=None, examples=[12.63])
    tags: list[str] = Field(default=None, examples=[["foo", "doe", "john"]])


@app.post("/items", response_model=Item)
def create_items(item: Item):
    return item


@app.get("/items", response_model=list[Item])
def get_items():
    return [
        Item(name="Plate", price=34.5),
        Item(name="Cooking gas", price=90.12)
    ]


@app.get("/cookies")
def get_cookies(cookies: Annotated[Cookies, Cookie()]):
    return {"cookies": cookies}


@app.get("/headers")
def get_headers(headers: Annotated[CommonHeaders, Header()]):
    return {"headers": headers}


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class User(BaseUser):
    password: str


@app.post("/user")
def create_user(user: User) -> BaseUser:
    return user


@app.get("/portal", response_model=None)
def get_portal(teleport: bool = False) -> Response | dict:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    # return JSONResponse(content={"message":"Here is your dimensional portal"})
    return {"message": "Here is your dimensional portal"}


@app.get("/teleport")
def get_teleport() -> RedirectResponse:
    return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")


class Items(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Items, response_model_exclude_unset=True)
def get_item(item_id: str):
    return items[item_id]


@app.get("/items/{item_id}/name", response_model=Items, response_model_include={"name", "description"})
def read_item_name(item_id: str):
    return items[item_id]


@app.get("/items/{item_id}/public", response_model=Items, response_model_exclude={"tax"})
def get_public(item_id: str):
    return items[item_id]