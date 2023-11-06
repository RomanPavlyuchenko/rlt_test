from pydantic_settings import BaseSettings


class DefaultConfig(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class TgBot(DefaultConfig):

    token: str = 'token'

    class Config:
        env_prefix = "BOT_"


class Settings(BaseSettings):
    tg: TgBot = TgBot()


config = Settings()
