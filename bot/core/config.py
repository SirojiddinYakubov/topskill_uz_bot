import pathlib
from typing import Optional, Any, Union

from pydantic.class_validators import validator
from pydantic.env_settings import BaseSettings
from pydantic.networks import AnyHttpUrl

BASE_DIR = pathlib.Path(__file__).parents[2]


class Settings(BaseSettings):
    BOT_API: str
    BOT_HASH: str
    SVC_PORT: Union[int, str]

    FRONT_BASE_URL: Optional[AnyHttpUrl] = "https://topskill.uz"
    BACK_BASE_URL: Optional[AnyHttpUrl] = "https://topskill.uz"
    WEBHOOK_HOST: Optional[AnyHttpUrl] = "https://topskill.uz"

    TOKEN_API: Optional[str]

    @validator("TOKEN_API", pre=True, allow_reuse=True)
    def assemble_token_api(cls, v: Optional[str], values: dict[str, Any]) -> str:
        return f"{values.get('BOT_API')}:{values.get('BOT_HASH')}"

    REDIS_HOST: str
    REDIS_PORT: Union[str, int]

    MONGODB_USER: str
    MONGODB_PASSWORD: str
    MONGODB_HOST: str
    MONGODB_PORT: Union[str, int]
    MONGODB_DATABASE: str

    MONGO_URI: Optional[str]

    @validator("MONGO_URI", pre=True, allow_reuse=True)
    def assemble_mongo_uri(cls, v: Optional[str], values: dict[str, Any]) -> str:
        return "mongodb://{user}:{password}@{host}:{port}/{database}?retryWrites=true&w=majority".format(
            user=values.get('MONGODB_USER'),
            password=values.get('MONGODB_PASSWORD'),
            host=values.get('MONGODB_HOST'),
            port=values.get('MONGODB_PORT'),
            database=values.get('MONGODB_DATABASE')
        )

    ADMIN_ID: Union[str, int]

    OTP_CODE_VALID_SECONDS: Optional[int] = 30000000

    ESKIZ_EMAIL: str
    ESKIZ_PASSWORD: str
    ESKIZ_TOKEN: Optional[str]

    AWS_BUCKET_URL: str

    class Config:
        env_file = f"{BASE_DIR}/.env"


settings = Settings()
