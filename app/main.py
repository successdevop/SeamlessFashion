import logging

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database.db_session import engine

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

    @my_app.get("/")
    async def root():
        return {"message": "Hello World"}

    return my_app

app = create_app()
