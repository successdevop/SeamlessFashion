import logging
import random
from datetime import datetime, timedelta, time
from typing import Annotated, Any
from uuid import UUID, uuid4

from fastapi import FastAPI, Query, Path, Body, Cookie, Header
from contextlib import asynccontextmanager

from pydantic import AfterValidator, BaseModel

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

    def check_valid_id(id: str):
        if not id.startswith(("isbn-", "imdb-")):
            raise ValueError("Invalid ID format. It must start with 'isbn-' or 'imdb-'")
        return id

    class Item(BaseModel):
        name: str
        description: str | None = None
        price: float
        tax: float | None = None
        tags: set[str] = set()
        address: AddressCreate

        model_config = {
            "json_schema_extra":{
                "examples":[
                    {
                        "name": "John doe",
                        "description": "A very nice item",
                        "price": 35.4,
                        "tax":3.2
                    }
                ]
            }
        }

    class Offer(BaseModel):
        name: str
        description: str | None = None
        price: float
        items: list[Item]

    @my_app.post("/items/{item_id}")
    def read_item(
            item_id: UUID,
            start_datetime: Annotated[datetime, Body()],
            end_datetime: Annotated[datetime, Body()],
            process_after: Annotated[timedelta, Body()],
            repeat_at: Annotated[time | None, Body()]
    ):
        start_process = start_datetime + process_after
        duration = end_datetime - start_process

        return {

            "item_id": item_id,
            "start_datetime": start_datetime,
            "end_datetime": end_datetime,
            "process_after": process_after,
            "repeat_at": repeat_at,
            "start_process": start_process,
            "duration": duration
        }

    @my_app.get("/cookie")
    def cookie(ads_id: Annotated[str|None, Cookie()]):
        return ads_id

    class CommonHeaders(BaseModel):
        host: str
        save_data: bool
        if_modified_since: str | None = None
        trace_parent: str | None = None
        x_tags: list[str] = []

    @my_app.get("/header")
    def headers(headers: Annotated[CommonHeaders, Header()]):
        return headers


    return my_app

app = create_app()
