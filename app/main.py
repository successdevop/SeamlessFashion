import logging
import time
from collections.abc import AsyncIterator
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import FastAPI, Depends, HTTPException, Header, BackgroundTasks
from contextlib import asynccontextmanager

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.sse import EventSourceResponse, ServerSentEvent
from jwt import InvalidTokenError
from pydantic import BaseModel

from pwdlib import PasswordHash
from sqlmodel import SQLModel

from app.api import api_routes
from app.database.db_session import engine

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

    my_app.include_router(api_routes)

    fake_users_db = {
        "johndoe": {
            "username": "johndoe",
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc",
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

    SECRET_KEY = "5df860686389b11fe6aa3736b46810e233f3ce5ee6d22dbadc50a26d74cbd1d3"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    class Token(BaseModel):
        access_token: str
        token_type: str

    class TokenData(BaseModel):
        username: str

    class User(BaseModel):
        username: str
        email: str | None = None
        full_name: str | None = None
        disabled: bool | None = None

    class UserInDB(User):
        hashed_password: str

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
    password_hash = PasswordHash.recommended()
    DUMMY_HASH = password_hash.hash("dummypassword")


    def get_hash_password(password: str):
        return password_hash.hash(password=password)

    def verify_password(password: str, hashed_password: str):
        return password_hash.verify(password=password, hash=hashed_password)

    def get_user(db: dict, username: str):
        if username not in db:
            return None
        user = db[username]
        return UserInDB(**user)

    def authenticate_user(db: dict, username: str, password: str):
        user = get_user(db=db, username=username)
        if not user:
            verify_password(password=password, hashed_password=DUMMY_HASH)
            return False
        if not verify_password(password=password, hashed_password=user.hashed_password):
            return False
        return user

    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(payload=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt


    async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
        credential_exception = HTTPException(
            status_code=400,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate":"Bearer"}
        )

        try:
            payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
            print(payload)

            username = payload.get("sub")
            if username is None:
                raise credential_exception

            token_data = TokenData(username=username)

        except InvalidTokenError:
            raise credential_exception

        user = get_user(fake_users_db, token_data.username)
        if user is None:
            raise credential_exception
        return user

    async def get_current_active_user(active_user: Annotated[User, Depends(get_current_user)]):
        if active_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return active_user

    @my_app.post("/token")
    def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
        user_data = authenticate_user(fake_users_db, form_data.username, form_data.password)
        if not user_data:
            raise HTTPException(
                status_code=401, detail="Incorrect username or password", headers={"WWW-Authenticate":"Bearer"}
            )

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user_data.username}, expires_delta=access_token_expires
        )

        return Token(access_token=access_token, token_type="bearer")

    @my_app.get("/users/me/")
    async def read_user_me(user: Annotated[User, Depends(get_current_active_user)]) -> User:
        return user

    @my_app.get("/users/me/items/")
    async def read_own_items(
            current_user: Annotated[User, Depends(get_current_active_user)],
    ):
        return [{"item_id": "Foo", "owner": current_user.username}]

    class Item(SQLModel):
        name: str
        price: float

    class Prompt(BaseModel):
        text: str

    items = [
        Item(name="Plumbus", price=32.99),
        Item(name="Portal Gun", price=999.99),
        Item(name="Meeseeks Box", price=49.99),
    ]

    logs = [
        "2025-01-01 INFO  Application started",
        "2025-01-01 DEBUG Connected to database",
        "2025-01-01 WARN  High memory usage detected",
    ]

    @my_app.post("/chat/stream")
    async def chat(post: Prompt) -> AsyncIterator[ServerSentEvent]:
        words = post.text.split()
        for word in words:
            yield ServerSentEvent(data=word)
        yield ServerSentEvent(raw_data='[DONE]', event="done")

    @my_app.get("/strems", response_class=EventSourceResponse)
    async def stream_data(last_event_id: Annotated[int | None, Header()] = None) -> AsyncIterator[ServerSentEvent]:
        start = last_event_id + 1 if last_event_id is not None else 0
        for i, log in enumerate(items):
            if i < start:
                continue
            yield ServerSentEvent(data=log, id=str(i))

    def write_notification(email: str, message: str):
        with open("log.txt", mode="w") as email_file:
            message = f"notification for {email}: {message}"
            email_file.write(message)

    def write_log(message: str):
        with open("log.txt", mode="a") as log:
            log.write(f"{message}\n")

    def get_query(background_task: BackgroundTasks, q: str | None = None):
        if q:
            message = f"found query: {q}\n"
            background_task.add_task(write_log, message)
        return q

    @my_app.post("/send-notifications/{email}")
    async def notifications(email: str, background_tasks: BackgroundTasks, q: Annotated[str, Depends(get_query)]):
        message = f"Message to {email}\n"
        background_tasks.add_task(write_log, message)
        return {"msg": "Message sent"}

    @my_app.post("/send-notification/{email}")
    async def send_notification(email: str, background_tasks: BackgroundTasks):
        background_tasks.add_task(write_notification, email, message="some notification")
        return {"message":"Notification sent in the background"}

    def process_data(data: User):
        time.sleep(5.0)
        print(f"processing data: {data}")

    @my_app.post("/process_data")
    async def process_endpoint(data: User, background_task: BackgroundTasks):
        background_task.add_task(process_data, data)
        return {"msg":"Task submitted successfully"}



    return my_app

app = create_app()
