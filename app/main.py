import logging
import random
from datetime import datetime, timedelta, time
from typing import Annotated, Any, Union
from uuid import UUID, uuid4

from fastapi import FastAPI, Query, Path, Body, Cookie, Header, Response
from contextlib import asynccontextmanager

from pydantic import AfterValidator, BaseModel
from starlette.responses import RedirectResponse, JSONResponse

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
        lifespan=lifespan
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

    def check_valid_id(id: str):
        if not id.startswith(("isbn-", "imdb-")):
            raise ValueError("Invalid ID format. It must start with 'isbn-' or 'imdb-'")
        return id

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

    # @my_app.get("/union", response_model=PlaneItem | CarItem)
    # def read_items(item_id: str):
    #     return items1[item_id]
    #
    # @my_app.post("/items/{id}", response_model=Item, response_model_exclude_unset=True)
    # def read_item(id: str):
    #     return items[id]

    @my_app.get("/items")
    def items(teleport: bool = False) -> Response | dict:
        if teleport:
            return RedirectResponse(url="https://www.google.com")
        return {"msg":"done"}

    return my_app

app = create_app()
