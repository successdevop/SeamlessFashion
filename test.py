# import random
# from typing import Annotated
#
# from pydantic import AfterValidator
#
# data = {
#     "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
#     "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
#     "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
# }
#
# def check_valid_id(id: str):
#     if not id.startswith(("isbn-", "imdb-")):
#         raise ValueError("Invalid ID format, it must start with 'isbn-' or 'imdb-'")
#     return id
#
# def read_items_(q: Annotated[str|None, AfterValidator(check_valid_id)] = None):
#     if q:
#         item = data[q]
#         print(item)
#     else:
#         result = random.choice(list(data.items()))
#         print(result)
#
#     # return {"id": q, "item": item}
# from typing import Annotated
#
#
# def say_hello(name: Annotated[str, "this is just metadata"]) -> str:
#     return f"Hello {name}"
#
# print(say_hello(""))

# import asyncio
# import asyncpg
#
# from app.config.config import db_settings
#
#
# async def test_connection():
#     print("Loaded user:", db_settings.POSTGRES_USER)
#     print("Loaded server:", db_settings.POSTGRES_SERVER)
#     print("Loaded port:", db_settings.POSTGRES_PORT)
#     print("Loaded database:", db_settings.POSTGRES_DB)
#     print("Password length:", len(db_settings.POSTGRES_PASSWORD))
#
#     conn = await asyncpg.connect(
#         host=db_settings.POSTGRES_SERVER,
#         port=db_settings.POSTGRES_PORT,
#         user=db_settings.POSTGRES_USER,
#         password=db_settings.POSTGRES_PASSWORD.get_secret_value(),
#         database=db_settings.POSTGRES_DB,
#     )
#
#     print("Successfully connected to PostgreSQL!")
#
#     await conn.close()
#
#
# asyncio.run(test_connection())

import asyncio

from sqlalchemy.ext.asyncio import create_async_engine

from app.config.config import db_settings


# async def test_connection():
#     url = db_settings.postgres_url
#
#     print(url.render_as_string(hide_password=True))
#
#     engine = create_async_engine(url)
#
#     async with engine.connect() as connection:
#         print("SQLAlchemy connection successful!")
#
#     await engine.dispose()
#
#
# asyncio.run(test_connection())

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=3072,
)

private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption(),
)

public_pem = private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
)

print(private_pem.decode())
print(public_pem.decode())
