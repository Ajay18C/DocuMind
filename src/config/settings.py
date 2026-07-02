from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

class R2Config(BaseModel):
    model_config = {"frozen": True}
    account_id: str
    access_key: str
    secret_key: str
    bucket: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    DEBUG: bool = False
    DATABASE_URL: str
    R2_CONFIG: R2Config
    FILE_STORAGE: str = "local"

settings = Settings()