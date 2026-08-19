from fastapi import HTTPException, status

from app.models import User
from app.repositories.user_repo import UserCrud
from app.schemas.identity.user import UserCreate
from app.utils.auth import validate_password, generate_hash_password


class AuthService:
    def __init__(self, user_crud: UserCrud) -> None:
        self.user_crud = user_crud

    async def register_user(self, user_data: UserCreate) -> User:
        email = str(user_data.email).strip().lower()

        existing_user = await self.user_crud.get_by_email(email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exist"
            )

        is_valid, message = validate_password(user_data.password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )

        password_hash = generate_hash_password(password=user_data.password)

        user_dict = user_data.model_dump(exclude={"password"})

        new_user = User(
            **user_dict,
            email=email,
            hash_password=password_hash
        )

        try:
            await self.user_crud.save(new_user)
            await self.user_crud.session.commit()
            return new_user
        except Exception:
            await self.user_crud.session.rollback()
            raise 

