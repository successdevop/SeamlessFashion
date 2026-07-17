from typing import Annotated, Any

from fastapi import FastAPI, Depends, HTTPException, Header, Cookie
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

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

# def verify_token(x_token: Annotated[str, Header()]):
#     if x_token != "fake_super_secret_token":
#         raise HTTPException(detail="X-Token Header invalid", status_code=400)
#
# def verify_key(x_key: Annotated[str, Header()]):
#     if x_key != "fake_super_secret_key":
#         raise HTTPException(detail="X-Key Header invalid", status_code=400)
#     return x_key
#
#
# @app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
# async def read_items():
#     return [{"item":"Foo"}, {"item":"Bar"}]

# class DBSession:
#     def close(self):
#         pass
#
#
# async def get_db():
#     db = DBSession()
#     try:
#         yield db
#     finally:
#         db.close()
#
#
# def generate_dep_a()-> str:
#     return "dependency_a"
#
#
# async def dependency_a():
#     db = generate_dep_a()
#     try:
#         yield db
#     finally:
#         db.close()
#
#
# def generate_dep_b():
#     return "dependency_b"
#
#
# async def dependency_b(dep_a: Annotated[str, Depends(dependency_a)]):
#     db = generate_dep_b()
#     try:
#         yield db
#     finally:
#         db.close(dep_a)
#
#
# def generate_dep_c():
#     return "dependency_c"
#
#
# async def dependency_c(dep_b: Annotated[str, Depends(dependency_b)]):
#     db = generate_dep_c()
#     try:
#         yield db
#     finally:
#         db.close(dep_b)


# class OwnerError(Exception):
#     pass
#
#
# def get_username():
#     try:
#         yield "Rick"
#     except OwnerError as e:
#         raise HTTPException(status_code=400, detail=f"Owner Error | {str(e)}")
#
# @app.get("/item/{item_id}")
# async def get_item(item_id: str, username: Annotated[str, Depends(get_username)]):
#     if item_id not in data:
#         raise HTTPException(status_code=404, detail="Item not found")
#     item = data[item_id]
#     if item["owner"] != username:
#         raise OwnerError(username)
#     return item

# data = {
#     "plumbus": {"description": "Freshly pickled plumbus", "owner": "Morty"},
#     "portal-gun": {"description": "Gun to create portals", "owner": "Rick"}
# }
#
#
# class InternalError(Exception):
#     pass
#
# def get_username():
#     try:
#         yield "Rick"
#     except InternalError as e:
#         raise HTTPException(status_code=400, detail=f"Oops, we didn't raise again, Britney 😱 || {str(e)}")
#
# @app.get("/item/{item_id}")
# async def get_item(item_id: str, username: Annotated[str, Depends(get_username)]):
#     if item_id == "portal-gun":
#         raise InternalError(f"The portal gun is too dangerous to be owned by {username}")
#     if item_id != "plumbus":
#         raise HTTPException(status_code=400, detail="Item not found")
#     return item_id


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str

def get_user(db, username: str):
    if username not in db:
        raise HTTPException(status_code=404, detail="User not found")
    user = db[username]
    return UserInDB(**user)

def fake_decode_token(token:str):
    user = get_user(db=fake_users_db, username=token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token=token)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="inactive user")
    return current_user


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)

    if hashed_password != user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_items(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user