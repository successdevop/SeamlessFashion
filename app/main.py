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
from typing import Annotated

from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items")
def get_items(user_agent: Annotated[str|None, Header()] = None):
    return {"User-Agent": user_agent}