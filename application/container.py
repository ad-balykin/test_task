from aiohttp import BaseConnector
from asyncpg import Pool
from logging import Logger
from typing import Any

from .config import AppConfig
from application.infrastructure.db_context import DBContextFactory
from application.infrastructure.repositories.course import CourseRepository
from application.infrastructure.adapters.binance import BinanceAdapter
from application.domain.services.courses_service import CoursesService
from application.domain.runners.course_runner import CourseRunner


class CompositionContainer:
    def __init__(  # noqa: WPS211
            self,
            config: AppConfig,
            http_connector: BaseConnector,
            logger: Logger,
    ) -> None:
        self.config = config
        self.http_connector = http_connector
        self.logger = logger
        self.current_connection = None

        self._dependencies: dict[str, Any] = {}

    def __getattr__(self, item: str) -> Any:
        try:
            return self._dependencies[item]
        except KeyError as missing_dependency:
            raise Exception(f"Dependency {missing_dependency} is missing or not added yet") from None

    def make_dependencies(self) -> None:
        self._dependencies["db_context_factory"] = DBContextFactory(
            config=self.config,
            logger=self.logger,
        )

        self._dependencies["course_repository"] = CourseRepository(logger=self.logger)

        self._dependencies["BinanceAdapter"] = BinanceAdapter(
            endpoint=self.config.binance_url,
            connector=self.http_connector,
        )

        self._dependencies["courses_service"] = CoursesService(
            adapters_mapping={
                "binance": self._dependencies["BinanceAdapter"],
            },
            course_repository=self.course_repository,
            db_context_factory=self.db_context_factory,
            logger=self.logger,
        )

        self._dependencies["courses_runner"] = CourseRunner(
            courses_service=self.courses_service,
            course_repository=self.course_repository,
            logger=self.logger,
            config=self.config,
            db_context_factory=self.db_context_factory,
        )
