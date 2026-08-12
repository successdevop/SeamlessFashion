import logging

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database.db_session import engine
from app.enums.user_enums import VerificationStatusEnum
from app.schemas.base_or_shared.address import AddressCreate, AddressRead

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    print("++++++++++++++")
    logger.info("Application starting...")
    print("++++++++++++++")
    try:
        print("++++++++++++++")
        logger.info("Database initialized successfully")
        print("++++++++++++++")
        yield
    except Exception:
        print("++++++++++++++")
        logger.exception("Application startup failed")
        print("++++++++++++++")
        raise
    finally:
        print("++++++++++++++")
        logger.info("Application shutting down...")
        print("++++++++++++++")
        await engine.dispose()
        print("++++++++++++++")
        logger.info("Database Connection pool closed")
        print("++++++++++++++")


def create_app() -> FastAPI:
    my_app = FastAPI(
        title="A multi-tenant fashion commerce platform",
        description="SeamlessFashion is an enterprise-grade fashion commerce platform that enables fashion brands, "
                    "clothing businesses, and designers to operate complete online businesses from a single platform",
        lifespan=lifespan
    )

    fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

    @my_app.get("/model/{model_name}")
    async def root(model_name: VerificationStatusEnum):
        if model_name is VerificationStatusEnum.REJECTED:
            return {"model_name": model_name, "message":"Deep learning FTW!"}

        if model_name.value == "pending_review":
            return {"model_name": model_name, "message":"LeCNN all the images"}

        return {"model_name": model_name, "message": "Have some residuals"}

    @my_app.get("/users/{user_id}/items/{item_id}")
    async def read_user_me(user_id:int, item_id: str, q: str | None = None, short: bool = False):
        item = {"user_id": user_id, "item_id": item_id}
        if q:
            item.update({"q":q})

        if not short:
            item.update({"description":"This is an amazing item that has a long description"})

        return item

    @my_app.post("/item")
    async def read_items(item: AddressCreate):
        return item

    @my_app.get("/us")
    async def check():
        return "hello"

    return my_app

app = create_app()
