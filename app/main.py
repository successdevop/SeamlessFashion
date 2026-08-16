import logging
import random
from datetime import datetime, timedelta, time
from typing import Annotated, Any, Union, Optional
from uuid import UUID, uuid4

from fastapi import FastAPI, Query, Path, Body, Cookie, Header, Response, File, UploadFile, Depends, HTTPException
from contextlib import asynccontextmanager

from pydantic import AfterValidator, BaseModel
from starlette.responses import RedirectResponse, JSONResponse, HTMLResponse

from app.database.db_session import engine
from app.schemas.base_or_shared.address import AddressCreate
from app.schemas.identity.user import UserBase

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.info("Application starting...")

    try:
        # Startup logic
        logger.info("Application startup completed")

        yield

    except Exception:
        logger.exception("Application runtime failed")
        raise

    finally:
        logger.info("Application shutting down...")

        await engine.dispose()

        logger.info("Database connection pool closed")


def create_app() -> FastAPI:
    my_app = FastAPI(
        title="A multi-tenant fashion commerce platform",
        description="SeamlessFashion is an enterprise-grade fashion commerce platform that enables fashion brands, "
                    "clothing businesses, and designers to operate complete online businesses from a single platform",
        lifespan=lifespan,
    )

    data = {
        "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
        "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
        "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
    }

    items = {
        "foo": {"name": "Foo", "price": 50.2},
        "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
        "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
    }

    class Item(BaseModel):
        name: str
        description: str | None = None
        price: float
        tax: float = 10.5
        tags: set[str] = set()
        # address: AddressCreate

    class Offer(BaseModel):
        name: str
        description: str | None = None
        price: float
        items: list[Item]

    class BaseItem(BaseModel):
        description: str
        type: str

    class CarItem(BaseItem):
        type: str = "car"

    class PlaneItem(BaseItem):
        type: str = "plane"
        size: int

    items1 = {
        "item1": {"description": "All my friends drive a low rider", "type": "car"},
        "item2": {
            "description": "Music is my aeroplane, it's my aeroplane",
            "type": "plane",
            "size": 5,
        },
    }

    data = {
        "plumbus": {"description": "Freshly pickled plumbus", "owner": "Morty"},
        "portal-gun": {"description": "Gun to create portals", "owner": "Rick"},
    }

    async def verify_token(x_token: Annotated[str, Header()]):
        if x_token != "fake_secret_token":
            raise HTTPException(status_code=400, detail="X Token header invalid")
        return x_token

    async def verify_key(x_key: Annotated[str, Header()]):
        if x_key != "fake_secret_key":
            raise HTTPException(status_code=400, detail="X Key header invalid")
        return x_key

    class OwnerError(Exception):
        pass

    class InternalError(Exception):
        pass

    def get_another_username():
        try:
            yield "Rick"
        except InternalError:
            print("We don't swallow the internal error here, we raise again 😎")
            raise

    @my_app.get("/users/{user_id}")
    def get_another_user(user_id: str, username: Annotated[str, Depends(get_another_username)]):
        if user_id == "portal-gun":
            raise InternalError(f"The portal-gun is too dangerous to be owned by {username}")

        if user_id != "plumbus":
            raise HTTPException(status_code=404, detail="Not found")
        return user_id

    def get_username():
        try:
            yield "Rick"
        except OwnerError as e:
            raise HTTPException(status_code=400, detail=f"Owner error: {e}")

    @my_app.get("/user/{user_id}")
    def get_user(user_id: str, username: Annotated[str, Depends(get_username)]):
        if user_id not in data:
            raise HTTPException(status_code=404, detail="Not found")
        user = data[user_id]
        if user["owner"] != username:
            raise OwnerError(username)
        return user

    @my_app.get("/items", dependencies=[Depends(verify_token), Depends(verify_key)])
    async def query_or_cookie():
        return {"msg":"returned value is correct"}

    return my_app

app = create_app()
