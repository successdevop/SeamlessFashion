import logging
import random
from datetime import datetime, timedelta, time, timezone
from typing import Annotated, Any, Union, Optional
from uuid import UUID, uuid4

import jwt
from fastapi import FastAPI, Query, Path, Body, Cookie, Header, Response, File, UploadFile, Depends, HTTPException
from contextlib import asynccontextmanager

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import InvalidTokenError
from pydantic import AfterValidator, BaseModel
from starlette.responses import RedirectResponse, JSONResponse, HTMLResponse

from pwdlib import PasswordHash

from app.api.auth.auth import auth
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

    my_app.include_router(auth)

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

    return my_app

app = create_app()
