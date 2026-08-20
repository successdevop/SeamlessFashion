from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession

from app.exceptions.exceptions import EmailAlreadyExistsError, UsernameAlreadyTakenError, PhoneNumberAlreadyExistsError, \
    InvalidPasswordError, DatabaseIntegrityError
from app.models import User
from app.repositories.user_repo import UserRepository
from app.schemas.identity.user import UserCreate
from app.utils.auth import validate_password, generate_hash_password


class AuthService:
    def __init__(self, user_repo: UserRepository, session: AsyncSession) -> None:
        self._user_repo = user_repo
        self._session = session

    async def register_user(self, user_data: UserCreate) -> User:

        existing_user = await self._user_repo.get_by_email_including_deleted(email=user_data.email)
        if existing_user:
            raise EmailAlreadyExistsError()

        existing_username = await self._user_repo.get_by_username(username=user_data.username)
        if existing_username:
            raise UsernameAlreadyTakenError()

        existing_phone_number = await self._user_repo.get_by_phone_number(phone_number=user_data.phone_number)
        if existing_phone_number:
            raise PhoneNumberAlreadyExistsError()

        is_valid, message = validate_password(user_data.password)
        if not is_valid:
            raise InvalidPasswordError()

        password_hash = generate_hash_password(password=user_data.password)

        user_dict = user_data.model_dump(exclude={"password"})

        new_user = User(
            **user_dict,
            password_hash=password_hash
        )

        try:
            await self._user_repo.save(new_user)
            await self._session.commit()
            await self._session.refresh(new_user)

            return new_user

        except IntegrityError as exc:
            await self._session.rollback()

            raise DatabaseIntegrityError() from exc

        except Exception:
            await self._session.rollback()
            raise

