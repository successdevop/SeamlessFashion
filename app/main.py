import logging
import random
from typing import Annotated, Any

from fastapi import FastAPI, Query, Path
from contextlib import asynccontextmanager

from pydantic import AfterValidator

from app.database.db_session import engine
from app.schemas.base_or_shared.address import AddressCreate

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

    # @my_app.get("/book/")
    # async def get_id(book_id: Annotated[str | None, AfterValidator(check_valid_id)] = None):
    #     if book_id:
    #         item = data.get(book_id)
    #     else:
    #         book_id, item = random.choice(list(data.items()))
    #     return {"id": book_id, "item": item}


    @my_app.post("/items/{item_id}")
    def create(*, item_id: int,
               q: Annotated[str|None, Query(
                   title="query-string",
                   alias="item-query",
                   description="Query string for the items to search in the database that have a good match",
                   min_length=3,
                   max_length=50,
                   pattern="^fixedquery$",
                   deprecated=True,
                   include_in_schema=False
               )] = None,
               address: Annotated[AddressCreate, Query()]
               ):
        address_dict = address.model_dump()
        if q:
            address_dict.update({"q":q})
        if address.zip_postal_code is not None:
            new_item = "added new field/column"
            address_dict.update({"new_field": new_item})
        return {"id": item_id, **address_dict}

    # @my_app.get("/items/{item_id}")
    # async def read_item(
    #         item_id: Annotated[int, Path(title="the ID of the item to get", ge=1, le=10)],
    #         q: Annotated[str | None, Query(alias="item-query")] = None
    # ):
    #     res: dict[str, Any] = {"id": item_id}
    #     if q:
    #         res.update({"q": q})
    #
    #     return res

    return my_app

app = create_app()
