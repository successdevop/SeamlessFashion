from datetime import datetime, timezone

from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession

from app.transactions_mgt.auth import AuthUnitOfWork
from app.exceptions.exceptions import EmailAlreadyExistsError, UsernameAlreadyTakenError, PhoneNumberAlreadyExistsError, \
    InvalidPasswordError, DatabaseIntegrityError
from app.models import User
from app.schemas.identity.user import UserCreate
from app.utils.auth import validate_password, generate_hash_password


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def register_user(self, user_data: UserCreate) -> User:
        async with AuthUnitOfWork(session=self._session) as authUoW:

            existing_user = await authUoW.users.get_by_email_including_deleted(email=user_data.email)
            if existing_user:
                if existing_user.is_deleted and existing_user.deleted_at:
                    days = datetime.now(tz=timezone.utc) - existing_user.deleted_at
                    if days.days <= 30:
                        # send an email informing the customer to activate their account by logging in
                        raise EmailAlreadyExistsError()
                # customer has an active account and doesn't need activation
                raise EmailAlreadyExistsError()

            existing_username = await authUoW.users.get_by_username(username=user_data.username)
            if existing_username:
                raise UsernameAlreadyTakenError()

            existing_phone_number = await authUoW.users.get_by_phone_number(phone_number=user_data.phone_number)
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
                await authUoW.users.save(new_user)

                await authUoW.outbox_message.save(
                    event_type="user.registration",
                    payload={"user_id": str(new_user.id), "email": new_user.email}
                )

                await authUoW.commit()
                await authUoW.refresh(new_user)

                return new_user

            except IntegrityError as exc:
                await self._session.rollback()

                raise DatabaseIntegrityError() from exc

            except Exception:
                await self._session.rollback()
                raise

