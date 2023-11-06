from pydantic_settings import BaseSettings


class DefaultConfig(BaseSettings):
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class TgBot(DefaultConfig):

    token: str = 'token'

    class Config:
        env_prefix = 'BOT_'


class DBConfig(DefaultConfig):
    mongo_url: str = 'url'

    class Config:
        env_prefix = 'DB_'


class Settings(BaseSettings):
    tg: TgBot = TgBot()
    db: DBConfig = DBConfig()


config = Settings()
