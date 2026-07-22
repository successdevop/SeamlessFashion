# # from datetime import datetime, timedelta, time
# # from typing import Annotated, Literal
# # from uuid import UUID
# #
# # from fastapi import FastAPI, Path
# # from fastapi.params import Query, Body
# # from pydantic import BaseModel, Field, HttpUrl
# #
# # app = FastAPI()
# #
# # class FilterParams(BaseModel):
# #     limit: int = Field(100, gt=0, le=100)
# #     offset: int = Field(0, ge=0)
# #     order_by: Literal["created_at", "updated_at"] = "created_at"
# #     tags: list[str] = []
# #
# #     model_config = {"extra":"forbid"}
# #
# #
# # class Image(BaseModel):
# #     url: HttpUrl
# #     name: str
# #
# #
# # class Item(BaseModel):
# #     name: str = Field(examples=["Foo"])
# #     description: str | None = Field(default=None, examples=["A very nice item"])
# #     price: float= Field(examples=[35.4])
# #     tax: float | None = Field(default=None, examples=[3.2])
# #     tags: set[str] = Field(examples=[["foo", "doe"]])
# #     image: list[Image] | None = Field(examples=[{"name": "Google", "url":"https://www.google.com"}])
# #
# #     # model_config = {
# #     #     "json_schema_extra":{
# #     #         "examples":[
# #     #             {"name": "Foo", "description": "A very nice item", "price": 35.4, "tax":3.2}
# #     #         ]
# #     #     }
# #     # }
# #
# #
# # class Item2(BaseModel):
# #     name: str
# #     description: str | None = None
# #     price: float
# #     tax: float | None = None
# #
# #
# # class User(BaseModel):
# #     username: str
# #     full_name: str | None = None
# #
# #
# # class Offer(BaseModel):
# #     name: str
# #     description: str | None = None
# #     price: float
# #     items: list[Item]
# #
# #
# # @app.patch("/items/item_id")
# # def update_item(item_id: UUID, start_datetime: Annotated[datetime, Body()], end_datetime: Annotated[datetime, Body()],
# #                 process_after: Annotated[timedelta, Body()], repeat_at: Annotated[time | None, Body()] = None):
# #     start_process = start_datetime + process_after
# #     duration = end_datetime - start_process
# #
# #     return {
# #         "item_id": item_id,
# #         "start_datetime": start_datetime,
# #         "end_datetime": end_datetime,
# #         "process_after": process_after,
# #         "repeat_at": repeat_at,
# #         "start_process": start_process,
# #         "duration": duration
# #     }
# #
# #
# # @app.put("/items/{item_id}")
# # def update(item_id: int,
# #            item: Annotated[Item2, Body(
# #                examples=[
# #                    {
# #                        "name":"Foo",
# #                        "description":"A very nice item",
# #                        "price": 35.4,
# #                        "tax": 3.2
# #                    },
# #                    {
# #                        "name": "Bar",
# #                        "price": "35.4",
# #                    },
# #                    {
# #                        "name": "Baz",
# #                        "price": "thirty five point four",
# #                    },
# #                ])]):
# #     return {"item_id": item_id, "item":item}
# #
# #
# # # @app.post("/index-weights")
# # # def create_index_weights(weights: dict[int, float]):
# # #     return weights
# # #
# # #
# # # @app.post("/image/multiple")
# # # def create_images(images: list[Image]):
# # #     return images
# # #
# # #
# # # @app.post("/offers")
# # # def create_offers(offer: Offer):
# # #     return offer
# # #
# # #
# # # @app.put("/items/{item_id}")
# # # def read_data(item_id: int, item: Item):
# # #     result = {"item_id": item_id, "item_data": item}
# # #     return result
# #
# from typing import Annotated, Any
#
# from fastapi import FastAPI, Header, Cookie, Response, Form, File, UploadFile, HTTPException
# from fastapi.exceptions import RequestValidationError
# from fastapi.responses import PlainTextResponse
# from pydantic import BaseModel, Field, EmailStr
# from starlette.requests import Request
# from starlette.responses import RedirectResponse, JSONResponse, HTMLResponse
# from starlette.exceptions import HTTPException as StarletteHTTPException
#
# app = FastAPI()
#
#
# class Cookies(BaseModel):
#     session_id: str
#     fatebook_tracker: str | None = None
#     googall_tracker: str | None = None
#
#
# class CommonHeaders(BaseModel):
#     host: str
#     save_data: bool
#     if_modified_since: str | None = None
#     traceparent: str | None = None
#     x_tags: list[str] = []
#
#
# class Item(BaseModel):
#     name: str = Field(examples=['LG TV'])
#     description: str | None = Field(default=None, examples=['LG TV is the always the best'])
#     price: float= Field(examples=[40.015])
#     tax: float | None = Field(default=None, examples=[12.63])
#     tags: list[str] = Field(default=None, examples=[["foo", "doe", "john"]])
#
#
# @app.post("/items", response_model=Item)
# def create_items(item: Item):
#     return item
#
#
# @app.get("/items", response_model=list[Item])
# def get_items():
#     return [
#         Item(name="Plate", price=34.5),
#         Item(name="Cooking gas", price=90.12)
#     ]
#
#
# @app.get("/cookies")
# def get_cookies(cookies: Annotated[Cookies, Cookie()]):
#     return {"cookies": cookies}
#
#
# @app.get("/headers")
# def get_headers(headers: Annotated[CommonHeaders, Header()]):
#     return {"headers": headers}
#
#
# class BaseUser(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: str | None = None
#
#
# class User(BaseUser):
#     password: str
#
#
# class UserPublic(BaseUser):
#     pass
#
#
# class UserInDB(BaseUser):
#     hash_password: str
#
#
# def fake_password_hasher(raw_password: str) -> str:
#     return f"supersecret {raw_password}"
#
#
# def fake_save_user(user_data: User):
#     hashed_password = fake_password_hasher(user_data.password)
#     new_user = UserInDB(**user_data.model_dump(), hash_password=hashed_password)
#     print("User saved! ...")
#     return new_user
#
#
# @app.post("/user/register", response_model=UserPublic)
# def create_user(user: User):
#     return fake_save_user(user_data=user)
#
#
# @app.post("/user")
# def create_user(user: User) -> BaseUser:
#     return user
#
#
# @app.get("/portal", response_model=None)
# def get_portal(teleport: bool = False) -> Response | dict:
#     if teleport:
#         return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
#     # return JSONResponse(content={"message":"Here is your dimensional portal"})
#     return {"message": "Here is your dimensional portal"}
#
#
# @app.get("/teleport")
# def get_teleport() -> RedirectResponse:
#     return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
#
#
# class Items(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float = 10.5
#     tags: list[str] = []
#
#
# items = {
#     "foo": {"name": "Foo", "price": 50.2},
#     "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
#     "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
# }
#
#
# @app.get("/items/{item_id}", response_model=Items, response_model_exclude_unset=True)
# def get_item(item_id: str):
#     return items[item_id]
#
#
# @app.get("/items/{item_id}/name", response_model=Items, response_model_include={"name", "description"})
# def read_item_name(item_id: str):
#     return items[item_id]
#
#
# @app.get("/items/{item_id}/public", response_model=Items, response_model_exclude={"tax"})
# def get_public(item_id: str):
#     return items[item_id]
#
#
# class BaseItem(BaseModel):
#     description: str
#     type: str
#
#
# class CarItem(BaseItem):
#     type: str = "car"
#
#
# class PlaneItem(BaseItem):
#     type: str = "plane"
#     size: int
#
#
# items_1 = {
#     "item1": {"description": "All my friends drive a low rider", "type": "car"},
#     "item2": {
#         "description": "Music is my aeroplane, it's my aeroplane",
#         "type": "plane",
#         "size": 5,
#     },
# }
#
#
# @app.get("/baseitem/{item_id}", response_model=PlaneItem|CarItem)
# def get_base_item(item_id: str):
#     return items_1[item_id]
#
#
# @app.post("/login", response_model=dict[str, str], response_model_exclude_unset=True, status_code=200)
# def login_user(username: Annotated[str, Form(alias="user-name", min_length=8)], password: Annotated[str, Form(min_length=8)]):
#     if not username or not password:
#         return {"detail":"user not found"}
#     return {"detail":"login successful"}
#
# class FormData(BaseModel):
#     username: str
#     password: str | None = None
#
#     model_config = {"extra": "forbid"}
#
#
# @app.post("/login_", response_model=dict[str, str], status_code=200)
# def login_user(login_info: Annotated[FormData, Form()]):
#     if not login_info.password or not login_info.username:
#         return {"details": "Login failed"}
#     return {"details": "Login successful"}
#
#
# @app.post("/files/")
# def create_file(info: Annotated[list[bytes], File(description="A file read by bytes")]):
#     return {"file_size": [len(info) for info in info]}
#
#
# @app.post("/upload_files/")
# def create_upload_file(info: Annotated[list[UploadFile], File(description="A file read by upload file")]):
#     return {"file_name": [info.filename for info in info]}
#
#
# @app.get("/")
# def main():
#     content = """
#     <body>
#     <form action="/files/" enctype="multipart/form-data" method="POST">
#     <input name="info" type="file" multiple>
#     <input name="info" type="file" multiple>
#     <input type="submit">
#     </form>
#     <form action="/upload_files/" enctype="multipart/form-data" method="POST">
#     <input name="info" type="file" multiple>
#     <input type="submit">
#     </form>
#     </body>
#     """
#     return HTMLResponse(content=content)
#
#
# @app.post("/files")
# def upload_form(file: Annotated[bytes, File()], uploadfile: Annotated[UploadFile, File()], username: Annotated[str, Form()]):
#     return {
#         "file_size": len(file),
#         "file_content_type": uploadfile.content_type,
#         "username": username.upper()
#     }
#
#
# item = {"foo": "The Foo Wrestlers"}
#
# @app.get("/exception/{e_id}")
# def raise_item_exception(e_id: str):
#     if e_id not in item:
#         raise HTTPException(status_code=404, detail="Not found", headers={"X-Error":"There goes my error"})
#     return {"item": item[e_id]}
#
#
# class UnicornException(Exception):
#     def __init__(self, name):
#         self.name = name
#
# @app.exception_handler(UnicornException)
# def unicorn_exception_handler(request: Request, exc: UnicornException):
#     return JSONResponse(
#         status_code=418,
#         content={"message":f"Oops! {exc.name} did something. There goes a rainbow..."}
#     )
#
# @app.get("/unicorns/{name}", deprecated=True)
# def read_unicorns(name: str):
#     if name == "yolo":
#         raise UnicornException(name=name)
#     return {"unicorn_name": name}
#
#
# @app.exception_handler(StarletteHTTPException)
# def http_exception_handler(request, exc):
#     return PlainTextResponse(str(exc.detail), status_code=exc.status_code)
#
#
# @app.exception_handler(RequestValidationError)
# def validation_exception_handler(request, exc: RequestValidationError):
#     message = "Validations errors"
#     for error in exc.errors():
#         message += f"\nField: {error['loc']}, Error: {error['msg']}"
#     return PlainTextResponse(message, status_code=400)
#
# @app.get("/exceptions/{e_id}", tags=["item"],
#          description="this is used to check for id and return it if it exists", response_description="Item retrieved")
# def read_excep(e_id: int):
#     if e_id == 3:
#         raise HTTPException(detail=f"Nope! I don't like {e_id}", status_code=418)
#     return {"e_id": e_id}
