from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


BASE_DIR = Path(__file__).resolve().parents[2]

_base_config = SettingsConfigDict(
    env_file=BASE_DIR / ".env",
    env_ignore_empty=True,
    env_file_encoding="utf-8",
    extra='ignore',
    case_sensitive=True
)


class DatabaseSettings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DB: str

    DB_ECHO: bool

    model_config = _base_config

    @property
    def postgres_url(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD.get_secret_value(),
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            database=self.POSTGRES_DB
        )


class SecuritySetting(BaseSettings):
    JWT_PRIVATE_KEY: str
    JWT_PUBLIC_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    model_config = _base_config


class EmailSettings(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = False

    model_config = _base_config


# DATABASE SETTINGS
db_settings = DatabaseSettings()

# JWT SECURITY KEY
security = SecuritySetting()
PRIVATE_KEY = security.JWT_PRIVATE_KEY.replace("\\n", "\n")
PUBLIC_KEY = security.JWT_PUBLIC_KEY.replace("\\n", "\n")

# EMAIL SETTINGS
email_settings = EmailSettings()
