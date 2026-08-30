from datetime import datetime, timezone, timedelta
from uuid import uuid4

from sqlalchemy.exc import IntegrityError

from app.auth import token_service
from app.auth.auth_session import AuthSession
from app.auth.passwd_policy import PasswordPolicy
from app.auth.passwd_service import PasswordService
from app.auth.refresh_token import RefreshToken
from app.auth.token_service import TokenService
from app.schemas.base_or_shared.audit import AuditLogCreate
from app.transactions_mgt.auth import AuthUnitOfWork
from app.exceptions.exceptions import EmailAlreadyExistsError, UsernameAlreadyTakenError, PhoneNumberAlreadyExistsError, \
    DatabaseIntegrityError
from app.models import User
from app.schemas.identity.user import UserCreate, TokenResponse
from app.utils.auth import generate_hash_password


class AuthService:
    def __init__(self, auth: AuthUnitOfWork, password_service: PasswordService, token_service: TokenService) -> None:
        self._authUoW = auth
        self._password_service = password_service
        self._token_service = token_service

    ## REGISTER USER
    async def register_user(self, user_data: UserCreate) -> User:
        # hash password
        password_hash = generate_hash_password(password=user_data.password)

        # check if user already exist or still exists after activating deletion process
        existing_user = await self._authUoW.users.get_by_email_including_deleted(email=user_data.email)
        if existing_user:
            if existing_user.is_deleted and existing_user.deleted_at:
                # check how days the email has been deleted
                deletion_days = datetime.now(tz=timezone.utc) - existing_user.deleted_at
                if deletion_days <= timedelta(days=30):
                    # send an email informing the customer to activate their account by logging in
                    raise EmailAlreadyExistsError()
            # customer has an active account and doesn't need activation
            raise EmailAlreadyExistsError()

        # if user doesn't exist, check if chosen username already exists
        existing_username = await self._authUoW.users.get_by_username(username=user_data.username)
        if existing_username:
            raise UsernameAlreadyTakenError()

        # check if chosen phone number already exist
        existing_phone_number = await self._authUoW.users.get_by_phone_number(phone_number=user_data.phone_number)
        if existing_phone_number:
            raise PhoneNumberAlreadyExistsError()

        # exclude plain password from being passed to model
        user_dict = user_data.model_dump(exclude={"password"})

        # create new user
        new_user = User(
            **user_dict,
            password_hash=password_hash
        )

        try:

            # manage transaction using unit_of_work pattern to make registration atomic
            await self._authUoW.users.add_and_flush(new_user)

            await self._authUoW.outbox_messages.add_and_flush(
                event_type="user.registration",
                payload={"user_id": str(new_user.id), "email": new_user.email}
            )

            audit = {
                "actor_id": new_user.id, "audit_action":"USER_REGISTERED",
                "resource_type":"User", "resource_id":new_user.id
            }

            await self._authUoW.audit_logs.add_and_flush(
                audit_schema=AuditLogCreate(**audit)
            )

            await self._authUoW.commit()
            return new_user

        except IntegrityError as exc:
            await self._authUoW.rollback()

            raise DatabaseIntegrityError() from exc

        except Exception:
            await self._authUoW.rollback()
            raise

    ## LOGIN USER
    async def login_user(self, email: str, password: str):
        is_valid, message = PasswordPolicy.validate(password=password)
        if not is_valid:
            raise ValueError(message)

        email = email.strip().lower()

        user = self._authUoW.users.get_by_email_including_deleted(email=email)
        if not user or not self._password_service.verify(password=password, hashed=user.password_hash):
            raise ValueError("Invalid email or password")

        if user and not user.email_verified:
            raise ValueError("Email not verified")

        if user:
            if not user.is_deleted and not user.is_active:
                raise ValueError("Account is inactive, contact support for activation/help")
            elif user.is_deleted and user.deleted_at:
                deletion_days = datetime.now(tz=timezone.utc) - user.deleted_at
                if deletion_days < timedelta(days=30):
                    user.is_deleted = False
                    user.deleted_at = None
                    user.is_active = True

        now = datetime.now(tz=timezone.utc)

        session = AuthSession(
            user_id=user.id,
            expires_at=now + self._token_service.refresh_token_lifetime
        )

        self._authUoW.auth_sessions.add_and_flush(auth_session=session)

        refresh_token_id = uuid4()
        family_id = uuid4()

        refresh_token = self._token_service.create_refresh_token(
            user_id=user.id,
            session_id=session.id,
            token_family_id=family_id,
            token_id=refresh_token_id
        )

        refresh_token_hash = self._password_service.hash(refresh_token)

        new_refresh_token = RefreshToken(
            id=refresh_token_id,
            session_id=session.id,
            user_id=user.id,
            token_family_id=family_id,
            token_hash=refresh_token_hash,
            expires_at=now + self._token_service.refresh_token_lifetime
        )

        self._authUoW.refresh_tokens.add_and_flush(token=new_refresh_token)

        access_token = self._token_service.create_access_token(user_id=user.id)

        await self._authUoW.commit()

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=int(self._token_service.refresh_token_lifetime.total_seconds())
        )