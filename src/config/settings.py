from typing import Literal

from pydantic import BaseModel, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class R2Config(BaseModel):
    model_config = {"frozen": True}
    account_id: str
    access_key: str
    secret_key: str
    bucket: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    DEBUG: bool = False
    DATABASE_URL: str
    FILE_STORAGE: Literal["local", "r2"] = "local"
    R2_CONFIG: R2Config | None = None
    PDF_PARSER: Literal["pdfium"] = "pdfium"
    OCR_ENGINE: Literal["paddle"] = "paddle"
    OCR_LANGUAGE: str = "en"
    CHUNKER: Literal["fixed", "semantic"] = "semantic"
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 200
    EMBEDDING_ENGINE: Literal["voyage"] = "voyage"
    VOYAGE_API_KEY: str
    RETRIEVER: Literal["topk"] = "topk"
    OPENROUTER_API_KEY: str

    @model_validator(mode="after")
    def _require_r2_config_when_selected(self) -> "Settings":
        if self.FILE_STORAGE == "r2" and self.R2_CONFIG is None:
            raise ValueError("R2_CONFIG is required when FILE_STORAGE='r2'")
        return self

    @model_validator(mode="after")
    def _require_overlap_smaller_than_chunk_size(self) -> "Settings":
        if self.CHUNK_OVERLAP >= self.CHUNK_SIZE:
            raise ValueError("CHUNK_OVERLAP must be smaller than CHUNK_SIZE")
        return self

settings = Settings()
