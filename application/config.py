from pydantic import BaseModel
from pydantic_settings import BaseSettings
from typing import Literal


class PostgresConfig(BaseModel):
    user: str
    password: str
    host: str
    port: int = 5432
    db_name: str

    min_size: int = 10
    max_size: int = 10

    @property
    def dsn(self) -> str:
        return "postgresql://{user}:{password}@{host}:{port}/{db_name}".format(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            db_name=self.db_name,
        )


class CourseRunnerConfig(BaseModel):
    iteration_delay: int = 4


class AppConfig(BaseSettings):
    debug: bool
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    postgres_config: PostgresConfig
    courses_runner_config: CourseRunnerConfig = CourseRunnerConfig()

    binance_url: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"
