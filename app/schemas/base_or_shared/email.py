from pydantic import EmailStr

from app.schemas.base_or_shared.orm_base import ORMBaseSchema


class EmailCreate(ORMBaseSchema):
    recipients: list[EmailStr]