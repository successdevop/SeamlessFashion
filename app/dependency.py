from typing import Annotated, Any

from fastapi import FastAPI, Depends, HTTPException, Header, Cookie

app = FastAPI()


# async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
#     return {"q": q, "skip": skip, "limit": limit}

# commonDep: type[dict] = Annotated[dict, Depends(common_parameters)]

# @app.get("/items")
# async def get_items(commons: commonDep):
#     return {"commons": commons}
#
# @app.get("/user")
# async def get_users(commons: commonDep):
#     return commons


# fake_item_db = [{"item_name":"Foo"}, {"item_name":"Bar"}, {"item_name":"Baz"}]
#
#
# class CommonQueryParams:
#     def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
#         self.q = q
#         self.skip = skip
#         self.limit = limit
#
# commonDep: type[CommonQueryParams] = Annotated[CommonQueryParams, Depends()]
#
#
# @app.get("/items2")
# async def get_items2(common: commonDep):
#     response_data = {}
#     if common.q:
#         response_data.update({"q":common.q})
#     item = fake_item_db[common.skip : common.skip + common.limit]
#     response_data.update({"items": item})
#     return response_data
#
# @app.get("/items")
# async def get_qp(common: Annotated[CommonQueryParams, Depends(CommonQueryParams)]):
#     response = {}
#     if common.q:
#         response.update({"q":common.q})
#
#     items = fake_item_db[common.skip : common.skip + common.limit]
#     response.update({"items": items})
#     return response

# def query_extractor(q: str | None = None):
#     return q
#
# def query_or_cookie_extractor(q: Annotated[str, Depends(query_extractor)], last_query: Annotated[str|None, Cookie()] = None):
#     if not q:
#         return last_query
#     return q
#
#
# @app.get("/items", summary="Get all query", response_model=dict[str, Any])
# async def read_query(query_or_default: Annotated[str|None, Depends(query_or_cookie_extractor)]):
#     return {"query_or_default": query_or_default}

def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake_super_secret_token":
        raise HTTPException(detail="X-Token Header invalid", status_code=400)

def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake_super_secret_key":
        raise HTTPException(detail="X-Key Header invalid", status_code=400)
    return x_key


@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item":"Foo"}, {"item":"Bar"}]