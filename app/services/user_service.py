from fastapi import HTTPException, status
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import User
from app.repositories.user_repo import UserCrud
from app.schemas.identity.user import UserCreate
from app.utils.auth import validate_password, generate_hash_password


class UserService(UserCrud):
    def __init__(self, model: type[SQLModel], session: AsyncSession):
        super().__init__(model=type[model], session=session)

    async def register_user(self, user_data: UserCreate):
        if await self.get_by_email(email=user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exist"
            )

        bool_value, str_value = validate_password(user_data.password)
        if not bool_value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str_value
            )

        hash_password = generate_hash_password(password=user_data.password)

        user_dict = user_data.model_dump(exclude_unset=True)

        new_user = User(
            **user_dict,
            hash_password=hash_password
        )

        user = await self.save(new_user)
        return user