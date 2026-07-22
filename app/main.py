from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database.db_session import init_db, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("++++++++++++++")
    print("Server is starting...")
    print("++++++++++++++")
    await init_db()

    yield
    print("++++++++++++++")
    print("Server is stopping...")
    print("++++++++++++++")
    await engine.dispose()
    print("++++++++++++++")
    print("Server connection closed")
    print("++++++++++++++")


app = FastAPI(
    title="A multi-tenant fashion commerce platform",
    description="SeamlessFashion is an enterprise-grade fashion commerce platform that enables fashion brands, "
                "clothing businesses, and designers to operate complete online businesses from a single platform",
    lifespan=lifespan
)