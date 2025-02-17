from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class TestDataBase(BaseModel):
    url: PostgresDsn
    echo: bool
    echo_pool: bool
    pool_size: int
    max_overflow: int


class TestSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("tests/core/.template.env", "tests/core/.env.docker"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="TEST__",
    )
    db: TestDataBase
