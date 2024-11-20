from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    API_ID: int
    API_HASH: str


    REF_LINK: str = "https://t.me/theYescoin_bot/Yescoin?startapp=PDOKzA"

    AUTO_TASK: bool = True

    DELAY_EACH_ACCOUNT: list[int] = [20, 30]
    
    AUTO_UPGRADE_LEVEL: bool = True

    MAX_UPGRADE_LEVEL: int = 10

    USE_PROXY_FROM_FILE: bool = False


settings = Settings()

