from app.schemas.base_or_shared.orm_base import ORMBaseSchema


class LoginData(ORMBaseSchema):
    username: str
    password: str


class TokenData(ORMBaseSchema):
    access_token: str
    token_type: str