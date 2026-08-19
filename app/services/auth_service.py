from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import User
from app.repositories.user_repo import UserRepository
from app.schemas.identity.user import UserCreate
from app.utils.auth import validate_password, generate_hash_password


class AuthService:
    def __init__(self, user_repo: UserRepository, session: AsyncSession) -> None:
        self._user_repo = user_repo
        self._session = session

    async def register_user(self, user_data: UserCreate) -> User:
        email = str(user_data.email).strip().lower()

        existing_user = await self._user_repo._get_by_email(email)
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

        hash_password = generate_hash_password(password=user_data.password)

        user_dict = user_data.model_dump(exclude={"password"})

        new_user = User(
            **user_dict,
            email=email,
            hash_password=hash_password
        )

        try:
            await self._user_repo._save(new_user)
            await self._session.commit()
            await self._session.refresh(new_user)

            return new_user
        except Exception:
            await self._session.rollback()
            raise

